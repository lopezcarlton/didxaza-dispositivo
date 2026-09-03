#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
from dataclasses import dataclass
from collections import defaultdict
from typing import Optional, Mapping, Iterable, Any
from pathlib import Path
import csv,re

from didxaza_runtime_v0_2_0_foundation import (
    AUTO_CORRECT_ENABLED, ORTHOGRAPHIC_SUGGESTIONS_ENABLED,
    normalize_apostrophes, strip_tone_marks,
)

RUNTIME_VERSION="0.2.5"
RUNTIME_STAGE="MORPHOLOGY_II"
MORPHOLOGY_II_STATUS="IMPLEMENTED_DOCUMENTED_ONLY"
NA_ANALYSIS_STATUS="ANALYSIS_CONFLICT_PRESERVED"
FORM_GENERATION_STATUS="DISABLED"

DER_TYPES=("NOMINALIZER","GENDA_FAMILY","NOMINALIZED_FORM","ADJ_SIMILITIVE","ADJ_DEVERBAL","POSSESSED_NOUN","DERIVED_NOUN")
VALENCE_TYPES=("BASIC_ROOT","MEDIOPASSIVE","MORE_ACTIVE","CAUSATIVE","EQUIPOLLENT_PAIR","DYAD","TRIAD")

@dataclass(frozen=True)
class DerivationEntry:
    entry_id:str
    headword_raw:str
    pdlma_raw:str
    pos:str
    additional_information:str
    attribution:str
    der_types:tuple[str,...]

@dataclass(frozen=True)
class DerivationAnalysis:
    entry_id:str
    observed_surface:str
    headword_evidence_raw:str
    pdlma_evidence_raw:str
    der_types:tuple[str,...]
    source_ids:tuple[str,...]
    epistemic_status:str="SOURCE_DOCUMENTED"
    surface_generation_allowed:bool=False

@dataclass(frozen=True)
class PossessionCandidate:
    observed_surface:str
    prefix_candidate:str
    status:str="PROVISIONAL"
    blocking_condition:str="REQUIRES_DOCUMENTED_LEMMA_OR_POSSESSED_SURFACE"

@dataclass(frozen=True)
class CausativeAnalysis:
    entry_id:str
    observed_surface:str
    headword_evidence_raw:str
    pdlma_evidence_raw:str
    analysis_codes_raw:str
    causative_status:str="DOCUMENTED_LEXEME_CODE"
    source_ids:tuple[str,...]=("BIB054_DICTIONARIA","BIB059_PBK2016","BIB060_PB2015")
    generated_surface:bool=False

@dataclass(frozen=True)
class ValenceRelation:
    relation_id:str
    relation_type:str
    member_entry_ids:tuple[str,...]
    source_id:str
    source_location:str
    speaker_accepts:tuple[str,...]=()
    speaker_rejects:tuple[str,...]=()
    status:str="DOCUMENTED"

    def __post_init__(self):
        if self.relation_type not in VALENCE_TYPES:
            raise ValueError(f"Unsupported valence relation: {self.relation_type}")

def surface_index(s:str)->str:
    return re.sub(r"\s+"," ",normalize_apostrophes(strip_tone_marks(s or "")).lower().strip())

def derive_types(row:Mapping[str,str])->tuple[str,...]:
    eid=(row.get("ID","") or "").lower()
    pos=row.get("Part_Of_Speech","") or ""
    ai=row.get("Additional_Information","") or ""
    out=[]
    if pos=="nmr": out.append("NOMINALIZER")
    if eid.startswith("genda"): out.append("GENDA_FAMILY")
    if pos=="nom": out.append("NOMINALIZED_FORM")
    if "a:sim" in ai: out.append("ADJ_SIMILITIVE")
    if re.search(r"\ba:dv",ai): out.append("ADJ_DEVERBAL")
    if "s:pos" in ai: out.append("POSSESSED_NOUN")
    if "s:der" in ai: out.append("DERIVED_NOUN")
    return tuple(out)

class MorphologyIIInventory:
    def __init__(self,entries:Iterable[Mapping[str,str]]):
        self.derivations={}
        self.by_surface=defaultdict(list)
        self.causatives={}
        self.causative_by_surface=defaultdict(list)
        for r in entries:
            types=derive_types(r)
            if types:
                e=DerivationEntry(
                    r.get("ID","") or "",r.get("Headword","") or "",r.get("PDLMA","") or "",
                    r.get("Part_Of_Speech","") or "",r.get("Additional_Information","") or "",
                    r.get("Attribution","") or "",types
                )
                self.derivations[e.entry_id]=e
                idx=surface_index(e.headword_raw)
                if idx:self.by_surface[idx].append(e.entry_id)
            if r.get("Part_Of_Speech")=="v" and "caus" in (r.get("Additional_Information","") or ""):
                eid=r.get("ID","") or ""
                rec={
                    "entry_id":eid,"headword":r.get("Headword","") or "",
                    "pdlma":r.get("PDLMA","") or "",
                    "analysis_codes":r.get("Additional_Information","") or "",
                }
                self.causatives[eid]=rec
                idx=surface_index(rec["headword"])
                if idx:self.causative_by_surface[idx].append(eid)

    @classmethod
    def from_csv(cls,path:str|Path):
        with Path(path).open("r",encoding="utf-8-sig",newline="") as f:
            return cls(csv.DictReader(f))

    def type_counts(self):
        d=defaultdict(int)
        for e in self.derivations.values():
            for t in e.der_types:d[t]+=1
        return dict(d)

    def analyze_derivation_surface(self,surface:str):
        out=[]
        for eid in self.by_surface.get(surface_index(surface),[]):
            e=self.derivations[eid]
            out.append(DerivationAnalysis(
                eid,surface,e.headword_raw,e.pdlma_raw,e.der_types,
                ("BIB054_DICTIONARIA",)
            ))
        return tuple(out)

    def possession_candidate(self,surface:str)->Optional[PossessionCandidate]:
        idx=surface_index(surface)
        # Exact Dictionaria possessed noun is handled by analyze_derivation_surface.
        if idx.startswith("xh") and len(idx)>2:
            return PossessionCandidate(surface,"xh-")
        if idx.startswith("x") and len(idx)>1:
            return PossessionCandidate(surface,"x-")
        return None

    def analyze_causative_surface(self,surface:str):
        out=[]
        for eid in self.causative_by_surface.get(surface_index(surface),[]):
            r=self.causatives[eid]
            out.append(CausativeAnalysis(eid,surface,r["headword"],r["pdlma"],r["analysis_codes"]))
        return tuple(out)

class ValenceRegistry:
    def __init__(self,relations:Iterable[ValenceRelation]=()):
        self._relations={r.relation_id:r for r in relations}
        self._by_member=defaultdict(list)
        for r in relations:
            for eid in r.member_entry_ids:self._by_member[eid].append(r.relation_id)

    def relations_for_entry(self,entry_id:str):
        return tuple(self._relations[r] for r in self._by_member.get(entry_id,[]))

    def add(self,r:ValenceRelation):
        self._relations[r.relation_id]=r
        for eid in r.member_entry_ids:self._by_member[eid].append(r.relation_id)

def genda_policy()->dict[str,str]:
    return {
        "documented_family":"YES",
        "gp_productive_forms":"GUENDA_OR_ENDA",
        "dictionaria_surface_variation":"PRESERVE_SOURCE",
        "normalize_genda_to_guenda":"NO",
        "productive_join":"NO",
        "surface_policy":"OPEN",
    }

def na_policy()->dict[str,str]:
    return {
        "status":"ANALYSIS_CONFLICT_PRESERVED",
        "gp_analysis":"STATIVE",
        "pbk_analysis":"PARTICIPIAL_IN_MANY_CASES",
        "strip_na_by_graphy":"NO",
        "add_na_to_adjective":"NO",
        "lexical_blocker_example":"nabé",
    }

def causative_rules()->tuple[dict[str,str],...]:
    return (
        {"id":"CAUS-U","analysis":"=u=","status":"DOCUMENTED_ANALYTICAL"},
        {"id":"CAUS-G","analysis":"=g=","status":"DOCUMENTED_ANALYTICAL"},
        {"id":"CAUS-ZI","analysis":"=zi=","status":"DOCUMENTED_ANALYTICAL"},
        {"id":"CAUS-USI","analysis":"u-si may reflect u-g-zi","status":"DOCUMENTED_ANALYTICAL"},
        {"id":"CAUS-GZ-S","analysis":"g+z→s","status":"MORPHOPHONOLOGICAL_ONLY"},
    )

def status()->dict[str,Any]:
    return {
        "runtime_version":RUNTIME_VERSION,
        "runtime_stage":RUNTIME_STAGE,
        "morphology_ii_status":MORPHOLOGY_II_STATUS,
        "form_generation_status":FORM_GENERATION_STATUS,
        "na_analysis_status":NA_ANALYSIS_STATUS,
        "valence_surface_inference":"PROHIBITED",
        "genda_surface_policy":"OPEN",
        "auto_correct_enabled":AUTO_CORRECT_ENABLED,
        "orthographic_suggestions_enabled":ORTHOGRAPHIC_SUGGESTIONS_ENABLED,
    }
