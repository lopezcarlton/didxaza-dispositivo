#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Optional, Any, Iterable, Mapping
from collections import defaultdict
import json
import uuid

from didxaza_runtime_v0_2_0_foundation import (
    AUTO_CORRECT_ENABLED,
    ORTHOGRAPHIC_SUGGESTIONS_ENABLED,
    ContextProfile,
)
from didxaza_runtime_v0_2_2_context_provenance import ValidationEvent

RUNTIME_VERSION = "0.2.6"
RUNTIME_STAGE = "EVIDENCE_ADJUDICATION"
AUTO_CORRECT_ENABLED_V026 = False
ORTHOGRAPHIC_SUGGESTIONS_ENABLED_V026 = False
DECISION_ENGINE_STATUS = "NOT_IMPLEMENTED"
EDIT_ENGINE_STATUS = "NOT_IMPLEMENTED"

PROVENANCE_TYPES = frozenset({
    "SOURCE_DIRECT",
    "LEXICAL_RETRIEVAL",
    "MORPHOLOGICAL_ANALYSIS",
    "BOUND_ANALYSIS",
    "DERIVATIONAL_ANALYSIS",
    "SPEAKER_EVENT",
    "PROJECT_EDITORIAL_EVENT",
    "ENGINEERING_HEURISTIC",
})

EPISTEMIC_STATUSES = frozenset({
    "RETRIEVED_ONLY",
    "DOCUMENTED",
    "STRUCTURALLY_SUPPORTED",
    "PROVISIONAL",
    "UNKNOWN",
})

VALIDATION_STATUSES = frozenset({
    "NONE",
    "SPEAKER_PRODUCED",
    "SPEAKER_REVIEWED",
    "SPEAKER_ORTHOGRAPHICALLY_VALIDATED",
    "PROJECT_EDITORIAL_DECISION",
})

EVIDENCE_STRENGTHS = ("UNKNOWN", "WEAK", "MODERATE", "STRONG", "DIRECT")
_STRENGTH_RANK = {x:i for i,x in enumerate(EVIDENCE_STRENGTHS)}

CONFLICT_STATUSES = frozenset({
    "NONE",
    "PRESENT",
    "UNRESOLVED_SOURCE_CONFLICT",
    "BLOCKED_BY_POLICY",
})

ADJUDICATION_STATUSES = frozenset({
    "SUPPORTED",
    "PROVISIONAL",
    "CONFLICTING",
    "UNRESOLVED",
    "BLOCKED",
})


@dataclass(frozen=True)
class EvidenceAtom:
    atom_id: str
    target_ref: str
    target_start: Optional[int]
    target_end: Optional[int]
    claim_type: str
    value: Any
    provenance_type: str
    source_ids: tuple[str, ...] = ()
    rule_ids: tuple[str, ...] = ()
    dialect_scope: tuple[str, ...] = ("UNKNOWN",)
    epistemic_status: str = "UNKNOWN"
    validation_status: str = "NONE"
    evidence_strength: str = "UNKNOWN"
    conflict_status: str = "NONE"
    blockers: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()
    raw_payload: Mapping[str, Any] = field(default_factory=dict)
    surface_claim: bool = False

    def __post_init__(self):
        if self.provenance_type not in PROVENANCE_TYPES:
            raise ValueError(f"Unsupported provenance_type: {self.provenance_type}")
        if self.epistemic_status not in EPISTEMIC_STATUSES:
            raise ValueError(f"Unsupported epistemic_status: {self.epistemic_status}")
        if self.validation_status not in VALIDATION_STATUSES:
            raise ValueError(f"Unsupported validation_status: {self.validation_status}")
        if self.evidence_strength not in _STRENGTH_RANK:
            raise ValueError(f"Unsupported evidence_strength: {self.evidence_strength}")
        if self.conflict_status not in CONFLICT_STATUSES:
            raise ValueError(f"Unsupported conflict_status: {self.conflict_status}")
        if (self.target_start is None) ^ (self.target_end is None):
            raise ValueError("target_start and target_end must both be set or both null")

@dataclass(frozen=True)
class EvidenceClaim:
    claim_id: str
    target_ref: str
    target_start: Optional[int]
    target_end: Optional[int]
    claim_type: str
    value: Any
    atom_ids: tuple[str, ...]
    provenance_types: tuple[str, ...]
    source_ids: tuple[str, ...]
    rule_ids: tuple[str, ...]
    dialect_scope: tuple[str, ...]
    epistemic_status: str
    validation_status: str
    evidence_strength: str
    conflict_status: str
    blockers: tuple[str, ...]
    surface_claim: bool

@dataclass(frozen=True)
class AdjudicatedClaim:
    claim: EvidenceClaim
    adjudication_status: str
    adjudication_notes: tuple[str, ...] = ()

    def __post_init__(self):
        if self.adjudication_status not in ADJUDICATION_STATUSES:
            raise ValueError(f"Unsupported adjudication_status: {self.adjudication_status}")

def _uniq(seq):
    return tuple(dict.fromkeys(x for x in seq if x is not None))

def _value_key(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)

def _stronger_strength(values: Iterable[str]) -> str:
    vals = list(values)
    if not vals:
        return "UNKNOWN"
    return max(vals, key=lambda x:_STRENGTH_RANK[x])

def _validation_summary(values: Iterable[str]) -> str:
    vals=set(values)
    # Explicit validation is kept distinct. Project editorial never overwrites
    # speaker validation; if both are present, the claim records project decision
    # as a distinct status only when no speaker orthographic validation exists.
    if "SPEAKER_ORTHOGRAPHICALLY_VALIDATED" in vals:
        return "SPEAKER_ORTHOGRAPHICALLY_VALIDATED"
    if "PROJECT_EDITORIAL_DECISION" in vals:
        return "PROJECT_EDITORIAL_DECISION"
    if "SPEAKER_REVIEWED" in vals:
        return "SPEAKER_REVIEWED"
    if "SPEAKER_PRODUCED" in vals:
        return "SPEAKER_PRODUCED"
    return "NONE"

def atom_from_retrieval(
    *,
    target_ref: str,
    value: Any,
    source_ids: tuple[str,...],
    dialect_scope: tuple[str,...] = ("UNKNOWN",),
    raw_payload: Mapping[str,Any] = {},
) -> EvidenceAtom:
    return EvidenceAtom(
        atom_id=str(uuid.uuid4()), target_ref=target_ref,
        target_start=None, target_end=None,
        claim_type="LEXICAL_ATTESTATION", value=value,
        provenance_type="LEXICAL_RETRIEVAL",
        source_ids=source_ids,
        dialect_scope=dialect_scope or ("UNKNOWN",),
        epistemic_status="RETRIEVED_ONLY",
        evidence_strength="MODERATE",
        raw_payload=raw_payload,
        surface_claim=False,
    )

def atom_from_engineering_heuristic(
    *,
    target_ref: str,
    claim_type: str,
    value: Any,
    heuristic_id: str,
    raw_payload: Mapping[str,Any] = {},
) -> EvidenceAtom:
    return EvidenceAtom(
        atom_id=str(uuid.uuid4()), target_ref=target_ref,
        target_start=None, target_end=None,
        claim_type=claim_type, value=value,
        provenance_type="ENGINEERING_HEURISTIC",
        rule_ids=(heuristic_id,),
        epistemic_status="PROVISIONAL",
        evidence_strength="WEAK",
        raw_payload=raw_payload,
        surface_claim=False,
    )

def atom_from_morph_analysis(
    analysis,
    *,
    target_ref: str,
    dialect_scope: tuple[str,...] = ("UNKNOWN",),
) -> EvidenceAtom:
    documented = getattr(analysis, "tam_status", None) == "DOCUMENTED"
    surface_claim = bool(getattr(analysis, "orthographic_surface_claim", False))
    value = {
        "entry_id": getattr(analysis, "entry_id", None),
        "tam": getattr(analysis, "tam", None),
        "verb_class": getattr(analysis, "verb_class", None),
        "root_analysis_raw": getattr(analysis, "root_analysis_raw", None),
        "input_layer": getattr(analysis, "input_layer", None),
    }
    return EvidenceAtom(
        atom_id=str(uuid.uuid4()), target_ref=target_ref,
        target_start=None, target_end=None,
        claim_type="MORPHOLOGICAL_ANALYSIS", value=value,
        provenance_type="MORPHOLOGICAL_ANALYSIS",
        source_ids=tuple(getattr(analysis, "source_ids", ()) or ()),
        rule_ids=tuple(getattr(analysis, "rule_ids", ()) or ()),
        dialect_scope=dialect_scope or ("UNKNOWN",),
        epistemic_status="DOCUMENTED" if documented else "PROVISIONAL",
        evidence_strength="STRONG" if documented else "MODERATE",
        raw_payload={
            "pdlma_evidence_raw": getattr(analysis, "pdlma_evidence_raw", None),
            "headword_evidence_raw": getattr(analysis, "headword_evidence_raw", None),
        },
        surface_claim=surface_claim,
    )

def atom_from_bound_analysis(
    analysis,
    *,
    target_ref: str,
    dialect_scope: tuple[str,...] = ("UNKNOWN",),
) -> EvidenceAtom:
    atype = getattr(analysis, "analysis_type", "")
    gram = getattr(analysis, "grammatical_unit_status", "")
    if atype in {
        "COMPOUND_DOCUMENTED","PHRASE_DOCUMENTED","PHRASAL_LEXEME_DOCUMENTED",
        "MULTIWORD_LEXEME_DOCUMENTED","CLITIC_RELATION_DOCUMENTED",
        "INTERNAL_BOUND_OR_COMPOUND_RELATION","ROOT_STRUCTURE_DOCUMENTED",
    }:
        epistemic="DOCUMENTED"; strength="STRONG"
    else:
        epistemic="PROVISIONAL"; strength="MODERATE"
    return EvidenceAtom(
        atom_id=str(uuid.uuid4()), target_ref=target_ref,
        target_start=None, target_end=None,
        claim_type="BOUND_ANALYSIS",
        value={
            "analysis_type":atype,
            "grammatical_unit_status":gram,
            "orthographic_policy":getattr(analysis,"orthographic_policy",None),
        },
        provenance_type="BOUND_ANALYSIS",
        source_ids=tuple(getattr(analysis,"source_ids",()) or ()),
        rule_ids=tuple(getattr(analysis,"evidence_ids",()) or ()),
        dialect_scope=dialect_scope or ("UNKNOWN",),
        epistemic_status=epistemic,
        evidence_strength=strength,
        raw_payload={
            "headword_evidence_raw":getattr(analysis,"headword_evidence_raw",None),
            "pdlma_evidence_raw":getattr(analysis,"pdlma_evidence_raw",None),
            "observed_surface":getattr(analysis,"observed_surface",None),
        },
        surface_claim=False,
    )

def atom_from_structural_bound_result(
    result,
    *,
    target_ref: str,
    dialect_scope: tuple[str,...] = ("UNKNOWN",),
) -> EvidenceAtom:
    classification=getattr(result,"classification","NO_BOUNDARY_EVIDENCE")
    if classification=="GRAMMATICAL_WORD_PROBABLE":
        epistemic="STRUCTURALLY_SUPPORTED"; strength="MODERATE"; conflict="NONE"
    elif classification=="PHRASE_PROBABLE":
        epistemic="STRUCTURALLY_SUPPORTED"; strength="MODERATE"; conflict="NONE"
    elif classification=="AMBIGUOUS_BOUND":
        epistemic="PROVISIONAL"; strength="WEAK"; conflict="PRESENT"
    else:
        epistemic="UNKNOWN"; strength="WEAK"; conflict="NONE"
    blockers=tuple(getattr(result,"blockers",()) or ())
    if blockers and classification=="AMBIGUOUS_BOUND":
        conflict="PRESENT"
    return EvidenceAtom(
        atom_id=str(uuid.uuid4()), target_ref=target_ref,
        target_start=None,target_end=None,
        claim_type="BOUND_STRUCTURAL_HYPOTHESIS",
        value=classification,
        provenance_type="BOUND_ANALYSIS",
        dialect_scope=dialect_scope or ("UNKNOWN",),
        epistemic_status=epistemic,
        evidence_strength=strength,
        conflict_status=conflict,
        blockers=blockers,
        raw_payload={
            "strong_support":tuple(getattr(result,"strong_support",()) or ()),
            "supporting_only":tuple(getattr(result,"supporting_only",()) or ()),
            "weak_ignored":tuple(getattr(result,"weak_ignored",()) or ()),
        },
        surface_claim=False,
    )

def atom_from_derivation_analysis(
    analysis,
    *,
    target_ref: str,
    dialect_scope: tuple[str,...] = ("UNKNOWN",),
) -> EvidenceAtom:
    return EvidenceAtom(
        atom_id=str(uuid.uuid4()), target_ref=target_ref,
        target_start=None,target_end=None,
        claim_type="DERIVATIONAL_ANALYSIS",
        value={
            "entry_id":getattr(analysis,"entry_id",None),
            "der_types":tuple(getattr(analysis,"der_types",()) or ()),
        },
        provenance_type="DERIVATIONAL_ANALYSIS",
        source_ids=tuple(getattr(analysis,"source_ids",()) or ()),
        dialect_scope=dialect_scope or ("UNKNOWN",),
        epistemic_status="DOCUMENTED",
        evidence_strength="STRONG",
        raw_payload={
            "headword_evidence_raw":getattr(analysis,"headword_evidence_raw",None),
            "pdlma_evidence_raw":getattr(analysis,"pdlma_evidence_raw",None),
        },
        surface_claim=True,
    )

def atom_from_validation_event(
    event: ValidationEvent,
    *,
    claim_type: str,
    value: Any,
    dialect_scope: tuple[str,...] = ("UNKNOWN",),
) -> EvidenceAtom:
    ptype = "PROJECT_EDITORIAL_EVENT" if event.validation_kind=="PROJECT_EDITORIAL_DECISION" else "SPEAKER_EVENT"
    epistemic = "DOCUMENTED" if event.validation_kind in {
        "SPEAKER_ORTHOGRAPHICALLY_VALIDATED","PROJECT_EDITORIAL_DECISION"
    } else "PROVISIONAL"
    strength = "DIRECT" if event.validation_kind in {
        "SPEAKER_ORTHOGRAPHICALLY_VALIDATED","PROJECT_EDITORIAL_DECISION"
    } else "MODERATE"
    return EvidenceAtom(
        atom_id=str(uuid.uuid4()),
        target_ref=event.target_ref,
        target_start=event.target_start,
        target_end=event.target_end,
        claim_type=claim_type,
        value=value,
        provenance_type=ptype,
        source_ids=(),
        dialect_scope=dialect_scope or ((event.community,) if event.community else ("UNKNOWN",)),
        epistemic_status=epistemic,
        validation_status=event.validation_kind,
        evidence_strength=strength,
        raw_payload={
            "validation_id":event.validation_id,
            "speaker_id":event.speaker_id,
            "community":event.community,
            "notes":event.notes,
        },
        surface_claim=event.validation_kind in {
            "SPEAKER_ORTHOGRAPHICALLY_VALIDATED","PROJECT_EDITORIAL_DECISION"
        },
    )

def atom_for_explicit_conflict(
    *,
    atom_id: str,
    target_ref: str,
    claim_type: str,
    value: Any,
    source_id: str,
    rule_id: str,
    dialect_scope: tuple[str,...] = ("UNKNOWN",),
    note: str = "",
) -> EvidenceAtom:
    return EvidenceAtom(
        atom_id=atom_id,target_ref=target_ref,target_start=None,target_end=None,
        claim_type=claim_type,value=value,
        provenance_type="SOURCE_DIRECT",
        source_ids=(source_id,),rule_ids=(rule_id,),
        dialect_scope=dialect_scope or ("UNKNOWN",),
        epistemic_status="DOCUMENTED",evidence_strength="STRONG",
        conflict_status="UNRESOLVED_SOURCE_CONFLICT",
        notes=(note,) if note else (),
    )

class EvidenceGraph:
    def __init__(self, atoms: Iterable[EvidenceAtom] = ()):
        self._atoms: dict[str,EvidenceAtom] = {}
        for a in atoms:self.add(a)

    def add(self, atom: EvidenceAtom):
        self._atoms[atom.atom_id]=atom

    def atom(self, atom_id:str)->EvidenceAtom:
        return self._atoms[atom_id]

    def atoms(self)->tuple[EvidenceAtom,...]:
        return tuple(self._atoms.values())

    def atoms_for_target(self,target_ref:str)->tuple[EvidenceAtom,...]:
        return tuple(a for a in self._atoms.values() if a.target_ref==target_ref)

class EvidenceAdjudicator:
    def __init__(self, graph: EvidenceGraph):
        self.graph=graph

    def _compatible_claims(self, atoms: list[EvidenceAtom]) -> list[EvidenceClaim]:
        groups=defaultdict(list)
        for a in atoms:
            key=(a.target_ref,a.target_start,a.target_end,a.claim_type,_value_key(a.value))
            groups[key].append(a)
        out=[]
        for (target_ref,start,end,claim_type,_), group in groups.items():
            provenance=_uniq(x for a in group for x in (a.provenance_type,))
            source_ids=_uniq(x for a in group for x in a.source_ids)
            rule_ids=_uniq(x for a in group for x in a.rule_ids)
            scope=_uniq(x for a in group for x in a.dialect_scope) or ("UNKNOWN",)
            blockers=_uniq(x for a in group for x in a.blockers)
            # Exact documented evidence dominates only as summary; raw atoms remain.
            epis={a.epistemic_status for a in group}
            if "DOCUMENTED" in epis:
                epistemic="DOCUMENTED"
            elif "STRUCTURALLY_SUPPORTED" in epis:
                epistemic="STRUCTURALLY_SUPPORTED"
            elif "PROVISIONAL" in epis:
                epistemic="PROVISIONAL"
            elif "RETRIEVED_ONLY" in epis:
                epistemic="RETRIEVED_ONLY"
            else:
                epistemic="UNKNOWN"
            conflicts={a.conflict_status for a in group}
            conflict="NONE"
            if "UNRESOLVED_SOURCE_CONFLICT" in conflicts:
                conflict="UNRESOLVED_SOURCE_CONFLICT"
            elif "BLOCKED_BY_POLICY" in conflicts:
                conflict="BLOCKED_BY_POLICY"
            elif "PRESENT" in conflicts:
                conflict="PRESENT"
            out.append(EvidenceClaim(
                claim_id=str(uuid.uuid4()),target_ref=target_ref,
                target_start=start,target_end=end,
                claim_type=claim_type,value=group[0].value,
                atom_ids=tuple(a.atom_id for a in group),
                provenance_types=provenance,source_ids=source_ids,rule_ids=rule_ids,
                dialect_scope=scope,epistemic_status=epistemic,
                validation_status=_validation_summary(a.validation_status for a in group),
                evidence_strength=_stronger_strength(a.evidence_strength for a in group),
                conflict_status=conflict,blockers=blockers,
                surface_claim=any(a.surface_claim for a in group),
            ))
        return out

    def adjudicate(self, target_ref: Optional[str] = None) -> tuple[AdjudicatedClaim,...]:
        atoms=list(self.graph.atoms() if target_ref is None else self.graph.atoms_for_target(target_ref))
        claims=self._compatible_claims(atoms)

        # Detect incompatible values for the same target/scope-independent claim type.
        by_type=defaultdict(list)
        for c in claims:
            by_type[(c.target_ref,c.target_start,c.target_end,c.claim_type)].append(c)

        conflict_ids=set()
        for _, group in by_type.items():
            distinct={_value_key(c.value) for c in group}
            if len(distinct) <= 1:
                continue
            substantive=[
                c for c in group
                if c.evidence_strength in {"DIRECT","STRONG","MODERATE"}
                and c.epistemic_status not in {"UNKNOWN","RETRIEVED_ONLY"}
            ]
            if len({_value_key(c.value) for c in substantive}) > 1:
                conflict_ids.update(c.claim_id for c in substantive)

        out=[]
        for c in claims:
            notes=[]
            if c.claim_id in conflict_ids or c.conflict_status in {"PRESENT","UNRESOLVED_SOURCE_CONFLICT"}:
                status="CONFLICTING"
                notes.append("INCOMPATIBLE_SUPPORTED_VALUES_PRESERVED")
            elif c.blockers or c.conflict_status=="BLOCKED_BY_POLICY":
                status="BLOCKED"
                notes.append("BLOCKING_CONDITION_PRESENT")
            elif c.epistemic_status=="DOCUMENTED":
                status="SUPPORTED"
            elif c.epistemic_status=="STRUCTURALLY_SUPPORTED":
                status="SUPPORTED"
            elif c.epistemic_status in {"PROVISIONAL","RETRIEVED_ONLY"}:
                status="PROVISIONAL"
            else:
                status="UNRESOLVED"

            # Engineering heuristics cannot be the sole path to SUPPORTED.
            if c.provenance_types==("ENGINEERING_HEURISTIC",) and status=="SUPPORTED":
                status="PROVISIONAL"
                notes.append("HEURISTIC_CANNOT_PROMOTE_TO_SUPPORTED")

            # Retrieval alone can never be SUPPORTED linguistic truth.
            if c.provenance_types==("LEXICAL_RETRIEVAL",) and status=="SUPPORTED":
                status="PROVISIONAL"
                notes.append("RETRIEVAL_ONLY_NOT_VALIDATION")

            out.append(AdjudicatedClaim(c,status,tuple(notes)))
        return tuple(out)

def tutor_view(claims: Iterable[AdjudicatedClaim]):
    """Claims suitable as factual input for future pedagogical rendering."""
    out=[]
    for a in claims:
        if a.adjudication_status not in {"SUPPORTED","PROVISIONAL","CONFLICTING"}:
            continue
        # Heuristic-only claims are not exposed as pedagogical facts.
        if a.claim.provenance_types==("ENGINEERING_HEURISTIC",):
            continue
        out.append(a)
    return tuple(out)

def generator_view(claims: Iterable[AdjudicatedClaim]):
    """Safe default constraints for future corpus/elicitation generator."""
    return tuple(
        a for a in claims
        if a.adjudication_status=="SUPPORTED"
        and a.claim.epistemic_status in {"DOCUMENTED","STRUCTURALLY_SUPPORTED"}
        and a.claim.conflict_status=="NONE"
    )

def corrector_view(claims: Iterable[AdjudicatedClaim]):
    """Analysis-only corrector input. No edits/actions exist in v0.2.6."""
    return tuple(claims)

def status()->dict[str,Any]:
    return {
        "runtime_version":RUNTIME_VERSION,
        "runtime_stage":RUNTIME_STAGE,
        "evidence_adjudication":"IMPLEMENTED",
        "numeric_global_confidence":"PROHIBITED",
        "decision_engine_status":DECISION_ENGINE_STATUS,
        "edit_engine_status":EDIT_ENGINE_STATUS,
        "auto_correct_enabled":False,
        "orthographic_suggestions_enabled":False,
    }
