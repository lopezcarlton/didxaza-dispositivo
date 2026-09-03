#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass
from collections import defaultdict
from typing import Optional, Mapping, Any, Iterable
from pathlib import Path
import csv
import re

from didxaza_runtime_v0_2_0_foundation import (
    AUTO_CORRECT_ENABLED,
    ORTHOGRAPHIC_SUGGESTIONS_ENABLED,
    normalize_apostrophes,
    strip_tone_marks,
)

RUNTIME_VERSION = "0.2.4"
RUNTIME_STAGE = "BOUND"
BOUND_ANALYSIS_STATUS = "IMPLEMENTED_CONSERVATIVE_STRUCTURAL"
SPACE_NORMALIZATION_STATUS = "DISABLED"
DIALECT_RESOLUTION_STATUS = "NOT_IMPLEMENTED"

@dataclass(frozen=True)
class BoundEntry:
    entry_id: str
    headword_raw: str
    pdlma_raw: str
    pos: str
    additional_information: str
    attribution: str
    boundary_class: str
    headword_has_space: bool
    pdlma_has_plus: bool
    pdlma_has_equals: bool
    pdlma_has_hash: bool
    phrasal_code: bool

@dataclass(frozen=True)
class BoundAnalysis:
    analysis_type: str
    observed_surface: str
    entry_id: Optional[str]
    headword_evidence_raw: Optional[str]
    pdlma_evidence_raw: Optional[str]
    orthographic_tokens_original: tuple[str, ...]
    grammatical_unit_status: str
    surface_spacing_status: str
    orthographic_policy: str
    evidence_ids: tuple[str, ...]
    source_ids: tuple[str, ...]
    notes: tuple[str, ...] = ()

@dataclass(frozen=True)
class CompoundTests:
    obligatory_contiguity: Optional[bool] = None
    single_inflection_domain: Optional[bool] = None
    host_at_compound_edge: Optional[bool] = None
    incorporated_argument: Optional[bool] = None
    fixed_order: Optional[bool] = None
    component_obligatory: Optional[bool] = None
    internal_inflection_repeated: Optional[bool] = None
    internal_interruption_possible: Optional[bool] = None
    independent_argument_internal: Optional[bool] = None
    conventional_meaning: Optional[bool] = None
    phonetic_reduction: Optional[bool] = None
    pause_absent: Optional[bool] = None

@dataclass(frozen=True)
class StructuralBoundResult:
    classification: str
    strong_support: tuple[str, ...]
    supporting_only: tuple[str, ...]
    blockers: tuple[str, ...]
    weak_ignored: tuple[str, ...]
    orthographic_policy: str = "NO_SPACING_ACTION"

GP_COMPOUNDS = frozenset({
    "racala'dxi'","riuulá'dxi'","riní'ique","runiruaa","rinabadiidxa'","redané","racané",
    "ba'duscuela","nisaguié","gu'xhuyú","yanniná'","yanniñee","larigueta","layabeedxe'",
    "guidiruaa","ba'duhuiini'","guendaró","guendaré'","guendaribana'","guendanabani",
})
GP_PHRASES = frozenset({
    "ricá bí","riguu beedxe'","rudii doo","rucaachi scuela","ricá bieque",
    "rindá' naxhi","rindá' dxaba'","raca huará","guidiladi yaga",
})
GP_DEPENDENT_PARTICLES = {
    "di'":"NEG","pe'":"ENF","xa":"INV","saa":"RECIP","si":"AS_SOON_AS",
    "xhaata'":"EXCESSIVE","ru'":"STILL","ga":"WHILE","ca":"THEN_OBVIOUS",
}

def comparison_surface(text: str) -> str:
    return re.sub(r"\s+"," ",normalize_apostrophes(strip_tone_marks(text or "")).lower().strip())

_GP_COMPOUND_INDEX={comparison_surface(x):x for x in GP_COMPOUNDS}
_GP_PHRASE_INDEX={comparison_surface(x):x for x in GP_PHRASES}

def dictionaria_boundary_class(headword: str, pdlma: str, additional_information: str) -> Optional[str]:
    h=(headword or "").strip()
    p=pdlma or ""
    ai=additional_information or ""
    phrasal=":lf" in ai
    has_space=" " in h
    has_plus="+" in p
    has_equals="=" in p
    has_root="-" in p
    if phrasal: return "PHRASAL_LEXEME"
    if has_space and has_equals: return "MULTIWORD_WITH_INTERNAL_COMPOSITION"
    if has_space: return "MULTIWORD_HEADWORD"
    if has_plus: return "CLITIC_STRUCTURE"
    if has_equals: return "AFFIX_OR_COMPOUND_STRUCTURE"
    if has_root: return "ROOT_STRUCTURE_ONLY"
    return None

class BoundInventory:
    def __init__(self, entries: Iterable[Mapping[str,str]]):
        self.entries={}
        self.by_surface=defaultdict(list)
        for row in entries:
            h=row.get("Headword","") or ""
            p=row.get("PDLMA","") or ""
            ai=row.get("Additional_Information","") or ""
            bc=dictionaria_boundary_class(h,p,ai)
            if bc is None: continue
            e=BoundEntry(
                entry_id=row.get("ID","") or "",
                headword_raw=h,pdlma_raw=p,
                pos=row.get("Part_Of_Speech","") or "",
                additional_information=ai,
                attribution=row.get("Attribution","") or "",
                boundary_class=bc,
                headword_has_space=" " in h.strip(),
                pdlma_has_plus="+" in p,
                pdlma_has_equals="=" in p,
                pdlma_has_hash="#" in p,
                phrasal_code=":lf" in ai,
            )
            self.entries[e.entry_id]=e
            idx=comparison_surface(e.headword_raw)
            if idx:self.by_surface[idx].append(e.entry_id)

    @classmethod
    def from_csv(cls,path:str|Path):
        with Path(path).open("r",encoding="utf-8-sig",newline="") as f:
            return cls(csv.DictReader(f))

    def class_counts(self):
        out=defaultdict(int)
        for e in self.entries.values(): out[e.boundary_class]+=1
        return dict(out)

    def exact_surface_analyses(self, observed_surface:str):
        idx=comparison_surface(observed_surface)
        tokens=tuple((observed_surface or "").split())
        out=[]
        if idx in _GP_COMPOUND_INDEX:
            out.append(BoundAnalysis(
                "COMPOUND_DOCUMENTED",observed_surface,None,_GP_COMPOUND_INDEX[idx],None,tokens,
                "GRAMMATICAL_WORD_DOCUMENTED_GP","EXACT_GP_SURFACE_DOCUMENTED",
                "PRESERVE_EXACT_DOCUMENTED_SURFACE_ONLY",("BOUND-CP-012",),
                ("BIB004_GRAMATICA_POPULAR",)
            ))
        if idx in _GP_PHRASE_INDEX:
            out.append(BoundAnalysis(
                "PHRASE_DOCUMENTED",observed_surface,None,_GP_PHRASE_INDEX[idx],None,tokens,
                "MULTIPLE_GRAMMATICAL_WORDS_DOCUMENTED_GP","EXACT_GP_SURFACE_DOCUMENTED",
                "PRESERVE_EXACT_DOCUMENTED_SURFACE_ONLY",("BOUND-CP-013",),
                ("BIB004_GRAMATICA_POPULAR",)
            ))
        for eid in self.by_surface.get(idx,[]):
            e=self.entries[eid]
            if e.boundary_class=="PHRASAL_LEXEME":
                atype="PHRASAL_LEXEME_DOCUMENTED"; gram="LEXICAL_UNIT_CAN_BE_MULTIWORD"
                policy="PRESERVE_DOCUMENTED_HEADWORD_SPACING"; evid=("BOUND-CP-022",)
            elif e.boundary_class in {"MULTIWORD_HEADWORD","MULTIWORD_WITH_INTERNAL_COMPOSITION"}:
                atype="MULTIWORD_LEXEME_DOCUMENTED"; gram="LEXICAL_UNIT_DOCUMENTED_BOUND_NOT_INFERRED"
                policy="PRESERVE_DOCUMENTED_HEADWORD_SPACING"; evid=("BOUND-CP-021",)
            elif e.boundary_class=="CLITIC_STRUCTURE":
                atype="CLITIC_RELATION_DOCUMENTED"; gram="CLITIC_RELATION_ANALYTICAL"
                policy="PENDING_CLITIC_POLICY"; evid=("BOUND-CP-018","BOUND-CP-016")
            elif e.boundary_class=="AFFIX_OR_COMPOUND_STRUCTURE":
                atype="INTERNAL_BOUND_OR_COMPOUND_RELATION"; gram="INTERNAL_ANALYTICAL_RELATION"
                policy="NO_SPACING_ACTION"; evid=("BOUND-CP-019",)
            else:
                atype="ROOT_STRUCTURE_DOCUMENTED"; gram="ROOT_BOUNDARY_ANALYTICAL"
                policy="NO_SPACING_ACTION"; evid=("BOUND-CP-002",)
            notes=[]
            if e.pdlma_has_hash: notes.append("PDLMA_HASH_WORD_BOUNDARY_ANALYSIS_ONLY")
            if e.pdlma_has_plus: notes.append("PDLMA_PLUS_CLITIC_ANALYSIS_ONLY")
            if e.pdlma_has_equals: notes.append("PDLMA_EQUALS_INTERNAL_RELATION_ONLY")
            out.append(BoundAnalysis(
                atype,observed_surface,e.entry_id,e.headword_raw,e.pdlma_raw,tokens,gram,
                "MULTIWORD_HEADWORD_DOCUMENTED" if e.headword_has_space else "JOINED_HEADWORD_DOCUMENTED",
                policy,evid,("BIB054_DICTIONARIA",),tuple(notes)
            ))
        return tuple(out)

def evaluate_compound_tests(t:CompoundTests)->StructuralBoundResult:
    strong=[]; support=[]; blockers=[]; weak=[]
    if t.obligatory_contiguity is True:strong.append("CONTIGUITY_REQUIRED")
    elif t.obligatory_contiguity is False:blockers.append("CONTIGUITY_CAN_BREAK")
    if t.single_inflection_domain is True:strong.append("ONE_INFLECTION_DOMAIN")
    elif t.single_inflection_domain is False:blockers.append("MULTIPLE_INFLECTION_DOMAINS")
    if t.host_at_compound_edge is True:strong.append("HOST_AT_COMPOUND_EDGE")
    elif t.host_at_compound_edge is False:blockers.append("HOST_INTERNAL_OR_MULTIPLE")
    if t.incorporated_argument is True:strong.append("ARGUMENT_INTERNAL_TO_COMPOUND")
    if t.internal_inflection_repeated is True:blockers.append("REPEATED_TAM_OR_PERSON")
    if t.internal_interruption_possible is True:blockers.append("INTERNAL_INTERRUPTION_POSSIBLE")
    if t.independent_argument_internal is True:blockers.append("ARGUMENT_INDEPENDENT_OR_INTERCALABLE")
    if t.fixed_order is True:support.append("ORDER_FIXED")
    if t.component_obligatory is True:support.append("COMPONENT_OBLIGATORY")
    elif t.component_obligatory is False:blockers.append("COMPONENT_OPTIONAL")
    if t.conventional_meaning is True:weak.append("CONVENTIONAL_MEANING_NOT_SUFFICIENT")
    if t.phonetic_reduction is True:weak.append("PHONETIC_REDUCTION_NOT_SUFFICIENT")
    if t.pause_absent is True:weak.append("PAUSE_ABSENCE_NOT_SUFFICIENT")
    if blockers:
        classification="PHRASE_PROBABLE" if any(x in blockers for x in ("REPEATED_TAM_OR_PERSON","MULTIPLE_INFLECTION_DOMAINS")) else "AMBIGUOUS_BOUND"
    elif len(strong)>=3:
        classification="GRAMMATICAL_WORD_PROBABLE"
    else:
        classification="NO_BOUNDARY_EVIDENCE" if not strong and not support else "AMBIGUOUS_BOUND"
    return StructuralBoundResult(classification,tuple(strong),tuple(support),tuple(blockers),tuple(weak),"NO_SPACING_ACTION")


def morphology_repeated_inflection_blocker(component_analyses) -> CompoundTests:
    """Derive only a safe negative BOUND test from Morphology I analyses.

    component_analyses: iterable of iterables of MorphAnalysis-like objects,
    one iterable per putative root/component.

    If two or more distinct components each have at least one documented TAM
    analysis, the sequence has repeated independent inflection evidence and
    this blocks a one-grammatical-word inference.

    IMPORTANT: If only one component is analyzable, we do NOT infer a single
    inflection domain. Missing analysis is not positive evidence.
    """
    inflected_components = 0
    for analyses in component_analyses:
        if any(
            getattr(a, "tam", None) is not None
            and getattr(a, "tam_status", None) == "DOCUMENTED"
            for a in analyses
        ):
            inflected_components += 1
    if inflected_components >= 2:
        return CompoundTests(
            single_inflection_domain=False,
            internal_inflection_repeated=True,
        )
    return CompoundTests(
        single_inflection_domain=None,
        internal_inflection_repeated=None,
    )

def dependent_particle_analysis(token:str)->Optional[BoundAnalysis]:
    idx=comparison_surface(token)
    by_idx={comparison_surface(k):(k,v) for k,v in GP_DEPENDENT_PARTICLES.items()}
    if idx not in by_idx:return None
    raw,role=by_idx[idx]
    return BoundAnalysis(
        "CLITIC_RELATION_DOCUMENTED",token,None,raw,None,tuple(token.split()),
        f"DEPENDENT_PARTICLE_{role}","POLICY_OPEN","PENDING_CLITIC_POLICY",
        ("BOUND-CP-015","BOUND-CP-016"),("BIB004_GRAMATICA_POPULAR","BIB061_XNEZA2015")
    )

def genda_boundary_status():
    return {"grammatical_unity":"CAN_BE_DOCUMENTED_BY_LEXEME_DERIVATION","surface_form_policy":"OPEN","automatic_target":"NONE"}

def glotonym_boundary_status():
    return {"compound_analysis":"DOCUMENTED_DIIDXA_PLUS_ZA","surface_form_policy":"PROJECT_DECISION","automatic_target":"NONE"}

def status()->dict[str,Any]:
    return {
        "runtime_version":RUNTIME_VERSION,
        "runtime_stage":RUNTIME_STAGE,
        "bound_analysis_status":BOUND_ANALYSIS_STATUS,
        "space_normalization_status":SPACE_NORMALIZATION_STATUS,
        "pdlma_to_spacing_rule":"PROHIBITED",
        "clitic_spacing_policy":"OPEN",
        "dialect_resolution_status":DIALECT_RESOLUTION_STATUS,
        "auto_correct_enabled":AUTO_CORRECT_ENABLED,
        "orthographic_suggestions_enabled":ORTHOGRAPHIC_SUGGESTIONS_ENABLED,
    }
