#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass
from collections import defaultdict
from pathlib import Path
from typing import Iterable, Mapping, Optional, Any
import csv, re, uuid

from didxaza_runtime_v0_2_6_evidence_adjudication import EvidenceAtom
from didxaza_runtime_v0_2_9_surface_evidence_coverage import (
    surface_key, DecisionSimulatorV029
)

RUNTIME_VERSION="0.2.10"
RUNTIME_STAGE="DOCUMENTARY_ALIGNMENT_SOURCE_EXPANSION_I"

AUTO_CORRECT_ENABLED=False
ORTHOGRAPHIC_SUGGESTIONS_ENABLED=False
EDIT_EXECUTION_ENABLED=False
USER_VISIBLE_SUGGESTIONS_ENABLED=False

@dataclass(frozen=True)
class DocumentaryAlignment:
    alignment_id:str
    surface_raw:str
    surface_key:str
    analysis_type:str
    analysis_value:str
    source_id:str
    source_location:str
    dialect_scope:tuple[str,...]
    status:str
    semantic_note:str=""

@dataclass(frozen=True)
class PhraseSurfaceAttestation:
    phrase_alignment_id:str
    phrase_surface_raw:str
    span_surface_raw:str
    span_key:str
    token_start:int
    token_end:int
    source_id:str
    source_location:str
    analysis_value:str
    semantic_equivalence:bool=False

class DocumentaryAlignmentIndex:
    def __init__(self, rows:Iterable[Mapping[str,str]], max_phrase_ngram_tokens:int=4):
        self.alignments={}
        self.by_surface=defaultdict(list)
        self.phrase_ngrams=defaultdict(list)
        self.max_phrase_ngram_tokens=max_phrase_ngram_tokens
        for r in rows:
            scope=tuple(x for x in (r.get("dialect_scope","") or "UNKNOWN").split(";") if x)
            a=DocumentaryAlignment(
                alignment_id=r["alignment_id"],
                surface_raw=r["surface_raw"],
                surface_key=surface_key(r["surface_raw"]),
                analysis_type=r["analysis_type"],
                analysis_value=r["analysis_value"],
                source_id=r["source_id"],
                source_location=r["source_location"],
                dialect_scope=scope or ("UNKNOWN",),
                status=r.get("status","DOCUMENTED_EXACT") or "DOCUMENTED_EXACT",
                semantic_note=r.get("semantic_note","") or "",
            )
            if a.status!="DOCUMENTED_EXACT":
                raise ValueError("Only DOCUMENTED_EXACT alignments are allowed in v0.2.10")
            self.alignments[a.alignment_id]=a
            self.by_surface[a.surface_key].append(a)

            if a.analysis_type=="FREQUENT_PHRASE":
                toks=_tokens(a.surface_raw)
                maxn=min(max_phrase_ngram_tokens,len(toks))
                for n in range(1,maxn+1):
                    for i in range(len(toks)-n+1):
                        raw=" ".join(toks[i:i+n])
                        p=PhraseSurfaceAttestation(
                            phrase_alignment_id=a.alignment_id,
                            phrase_surface_raw=a.surface_raw,
                            span_surface_raw=raw,
                            span_key=surface_key(raw),
                            token_start=i,token_end=i+n,
                            source_id=a.source_id,source_location=a.source_location,
                            analysis_value=a.analysis_value,
                            semantic_equivalence=False,
                        )
                        self.phrase_ngrams[p.span_key].append(p)

    @classmethod
    def from_csv(cls,path:str|Path,max_phrase_ngram_tokens:int=4):
        with Path(path).open(encoding="utf-8-sig",newline="") as f:
            return cls(csv.DictReader(f),max_phrase_ngram_tokens=max_phrase_ngram_tokens)

    def lookup_exact(self,text:str)->tuple[DocumentaryAlignment,...]:
        return tuple(self.by_surface.get(surface_key(text),()))

    def lookup_phrase_ngram(self,text:str)->tuple[PhraseSurfaceAttestation,...]:
        return tuple(self.phrase_ngrams.get(surface_key(text),()))

def _tokens(text:str):
    out=[]
    for x in re.findall(r"\S+",text or ""):
        x=x.strip(".,;:!?¡¿")
        if x:out.append(x)
    return out

def alignment_surface_atom(a:DocumentaryAlignment,*,target_ref:str,start:int,end:int,observed_surface:str)->EvidenceAtom:
    if surface_key(a.surface_raw)!=surface_key(observed_surface):
        raise ValueError("Alignment is not exact for observed surface")
    return EvidenceAtom(
        atom_id=str(uuid.uuid4()),target_ref=target_ref,target_start=start,target_end=end,
        claim_type="DOCUMENTED_SURFACE_ATTESTATION",
        value={"surface":observed_surface,"semantic_equivalence":False},
        provenance_type="SOURCE_DIRECT",
        source_ids=(a.source_id,),
        rule_ids=(a.alignment_id,),
        dialect_scope=a.dialect_scope,
        epistemic_status="DOCUMENTED",
        evidence_strength="STRONG",
        raw_payload={
            "alignment_id":a.alignment_id,
            "analysis_type":a.analysis_type,
            "analysis_value":a.analysis_value,
            "source_location":a.source_location,
            "documented_surface":a.surface_raw,
            "semantic_note":a.semantic_note,
        },
        surface_claim=True,
    )

def alignment_analysis_atom(a:DocumentaryAlignment,*,target_ref:str,start:int,end:int)->EvidenceAtom:
    return EvidenceAtom(
        atom_id=str(uuid.uuid4()),target_ref=target_ref,target_start=start,target_end=end,
        claim_type=f"DOCUMENTARY_{a.analysis_type}",
        value=a.analysis_value,
        provenance_type="SOURCE_DIRECT",
        source_ids=(a.source_id,),
        rule_ids=(a.alignment_id,),
        dialect_scope=a.dialect_scope,
        epistemic_status="DOCUMENTED",
        evidence_strength="DIRECT",
        raw_payload={
            "surface_raw":a.surface_raw,
            "source_location":a.source_location,
            "semantic_note":a.semantic_note,
        },
        surface_claim=False,
    )

def phrase_ngram_surface_atom(p:PhraseSurfaceAttestation,*,target_ref:str,start:int,end:int,observed_surface:str)->EvidenceAtom:
    if p.span_key!=surface_key(observed_surface):
        raise ValueError("Phrase ngram is not exact")
    return EvidenceAtom(
        atom_id=str(uuid.uuid4()),target_ref=target_ref,target_start=start,target_end=end,
        claim_type="DOCUMENTED_SURFACE_ATTESTATION",
        value={"surface":observed_surface,"semantic_equivalence":False},
        provenance_type="SOURCE_DIRECT",
        source_ids=(p.source_id,),
        rule_ids=(p.phrase_alignment_id,),
        dialect_scope=("JUCHITAN_HISTORICAL_SOURCE",),
        epistemic_status="DOCUMENTED",
        evidence_strength="STRONG",
        raw_payload={
            "phrase_alignment_id":p.phrase_alignment_id,
            "phrase_surface_raw":p.phrase_surface_raw,
            "source_location":p.source_location,
            "analysis_value":p.analysis_value,
            "semantic_equivalence":False,
            "token_start":p.token_start,
            "token_end":p.token_end,
        },
        surface_claim=True,
    )

def full_phrase_semantic_atom(a:DocumentaryAlignment,*,target_ref:str,start:int,end:int,observed_surface:str)->EvidenceAtom:
    if a.analysis_type!="FREQUENT_PHRASE":
        raise ValueError("Only FREQUENT_PHRASE alignment has documentary full-phrase semantics")
    if surface_key(a.surface_raw)!=surface_key(observed_surface):
        raise ValueError("Full phrase must match exactly")
    return EvidenceAtom(
        atom_id=str(uuid.uuid4()),target_ref=target_ref,target_start=start,target_end=end,
        claim_type="DOCUMENTARY_PHRASE_MEANING",
        value=a.analysis_value,
        provenance_type="SOURCE_DIRECT",
        source_ids=(a.source_id,),
        rule_ids=(a.alignment_id,),
        dialect_scope=a.dialect_scope,
        epistemic_status="DOCUMENTED",
        evidence_strength="DIRECT",
        raw_payload={"phrase_surface_raw":a.surface_raw,"source_location":a.source_location},
        surface_claim=False,
    )

def status()->dict[str,Any]:
    return {
        "runtime_version":RUNTIME_VERSION,
        "runtime_stage":RUNTIME_STAGE,
        "documentary_alignment":"IMPLEMENTED_EXACT_ONLY",
        "rule_based_surface_generation":"DISABLED",
        "inverse_person_generation":"DISABLED",
        "productive_possession_generation":"DISABLED",
        "tam_from_graphic_prefix_only":"PROHIBITED",
        "negative_marker_from_spanish_no":"PROHIBITED",
        "pdlma_to_surface":"PROHIBITED",
        "auto_correct_enabled":False,
        "orthographic_suggestions_enabled":False,
        "edit_execution_enabled":False,
        "user_visible_suggestions_enabled":False,
    }
