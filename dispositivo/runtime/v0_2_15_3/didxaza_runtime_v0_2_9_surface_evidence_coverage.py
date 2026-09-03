#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass
from collections import defaultdict
from typing import Optional, Iterable, Mapping, Any
from pathlib import Path
import csv, re, unicodedata, uuid

from didxaza_runtime_v0_2_6_evidence_adjudication import (
    EvidenceAtom, AdjudicatedClaim
)
from didxaza_runtime_v0_2_7_decision_simulation import (
    DecisionSimulator, DecisionSimulation, CandidateEdit,
    _scope_compatible, _explicit_validation, _validation_scope_matches,
    _exact_surface_documented, _replacement_candidate, validate_candidate_edits
)

RUNTIME_VERSION="0.2.9"
RUNTIME_STAGE="SURFACE_EVIDENCE_COVERAGE"
AUTO_CORRECT_ENABLED=False
ORTHOGRAPHIC_SUGGESTIONS_ENABLED=False
EDIT_EXECUTION_ENABLED=False
USER_VISIBLE_SUGGESTIONS_ENABLED=False

APOS_EQUIVALENTS=("'","’","ʼ","ꞌ")
SOURCE_COVERAGE=("LA_VENTOSA","JUCHITAN","SANTA_MARIA_XADANI")

@dataclass(frozen=True)
class SurfaceAttestation:
    surface_raw:str
    surface_key:str
    source_kind:str
    source_id:str
    source_location:str
    attribution:str
    example_id:Optional[str]=None
    entry_id:Optional[str]=None
    sense_ids:tuple[str,...]=()
    n_tokens:int=1
    semantic_equivalence:bool=False
    dialect_scope:tuple[str,...]=("UNKNOWN",)
    source_coverage:tuple[str,...]=SOURCE_COVERAGE

def surface_key(text:str)->str:
    """Strict documentary surface key.

    Permitted: NFC, case normalization, apostrophe typography, whitespace.
    Forbidden: tone/diacritic stripping, vowel collapse, PDLMA conversion.
    """
    s=unicodedata.normalize("NFC",text or "").casefold()
    for a in APOS_EQUIVALENTS[1:]:
        s=s.replace(a,"'")
    return re.sub(r"\s+"," ",s.strip())

def _tokenize_surface(text:str):
    out=[]
    for m in re.finditer(r"\S+",text or ""):
        raw=m.group()
        left=0; right=len(raw)
        while left<right and not (
            raw[left].isalnum() or raw[left] in APOS_EQUIVALENTS
            or unicodedata.category(raw[left]).startswith(("L","M"))
        ):
            left+=1
        while right>left and not (
            raw[right-1].isalnum() or raw[right-1] in APOS_EQUIVALENTS
            or unicodedata.category(raw[right-1]).startswith(("L","M"))
        ):
            right-=1
        if left<right:
            out.append(raw[left:right])
    return out

class SurfaceAttestationIndex:
    def __init__(self, entries:Iterable[Mapping[str,str]], examples:Iterable[Mapping[str,str]], max_example_tokens:int=4):
        if max_example_tokens < 1:
            raise ValueError("max_example_tokens must be >=1")
        self.max_example_tokens=max_example_tokens
        self.by_key=defaultdict(list)
        self.headword_count=0
        self.example_count=0
        self.example_ngram_count=0

        for e in entries:
            raw=e.get("Headword","") or ""
            key=surface_key(raw)
            if not key: continue
            self.headword_count+=1
            att=SurfaceAttestation(
                surface_raw=raw,surface_key=key,
                source_kind="HEADWORD",source_id="BIB054_DICTIONARIA",
                source_location=f"entry:{e.get('ID','')}",
                attribution=e.get("Attribution","") or "",
                entry_id=e.get("ID","") or None,
                n_tokens=max(1,len(_tokenize_surface(raw))),
                semantic_equivalence=False,
                dialect_scope=("UNKNOWN",),
                source_coverage=SOURCE_COVERAGE,
            )
            self.by_key[key].append(att)

        for ex in examples:
            self.example_count+=1
            tokens=_tokenize_surface(ex.get("Primary_Text","") or "")
            maxn=min(max_example_tokens,len(tokens))
            sense_ids=tuple(x for x in re.split(r"[;\s]+",ex.get("Sense_IDs","") or "") if x)
            for n in range(1,maxn+1):
                for i in range(0,len(tokens)-n+1):
                    raw=" ".join(tokens[i:i+n])
                    key=surface_key(raw)
                    if not key: continue
                    self.example_ngram_count+=1
                    att=SurfaceAttestation(
                        surface_raw=raw,surface_key=key,
                        source_kind="EXAMPLE_NGRAM",source_id="BIB054_DICTIONARIA",
                        source_location=f"example:{ex.get('ID','')}",
                        attribution=ex.get("Attribution","") or "",
                        example_id=ex.get("ID","") or None,
                        sense_ids=sense_ids,n_tokens=n,
                        semantic_equivalence=False,
                        dialect_scope=("UNKNOWN",),
                        source_coverage=SOURCE_COVERAGE,
                    )
                    self.by_key[key].append(att)

    @classmethod
    def from_csv(cls, entries_csv:str|Path, examples_csv:str|Path, max_example_tokens:int=4):
        with Path(entries_csv).open(encoding="utf-8-sig",newline="") as f:
            entries=list(csv.DictReader(f))
        with Path(examples_csv).open(encoding="utf-8-sig",newline="") as f:
            examples=list(csv.DictReader(f))
        return cls(entries,examples,max_example_tokens=max_example_tokens)

    def lookup_exact(self,text:str)->tuple[SurfaceAttestation,...]:
        return tuple(self.by_key.get(surface_key(text),()))

    def has_exact(self,text:str)->bool:
        return bool(self.lookup_exact(text))

def surface_attestation_atom(
    att:SurfaceAttestation, *,
    target_ref:str,start:int,end:int,observed_surface:str
)->EvidenceAtom:
    if surface_key(att.surface_raw) != surface_key(observed_surface):
        raise ValueError("Surface attestation is not exact under strict documentary key")
    reason=(
        "EXACT_DOCUMENTED_HEADWORD_SURFACE"
        if att.source_kind=="HEADWORD"
        else "EXACT_DOCUMENTED_EXAMPLE_SURFACE"
    )
    return EvidenceAtom(
        atom_id=str(uuid.uuid4()),target_ref=target_ref,
        target_start=start,target_end=end,
        claim_type="DOCUMENTED_SURFACE_ATTESTATION",
        value={
            "surface":observed_surface,
            "semantic_equivalence":False,
        },
        provenance_type="SOURCE_DIRECT",
        source_ids=(att.source_id,),
        rule_ids=(reason,),
        dialect_scope=att.dialect_scope,
        epistemic_status="DOCUMENTED",
        evidence_strength="STRONG",
        raw_payload={
            "surface_raw":att.surface_raw,
            "source_location":att.source_location,
            "attribution":att.attribution,
            "example_id":att.example_id,
            "entry_id":att.entry_id,
            "sense_ids":att.sense_ids,
            "source_coverage":att.source_coverage,
            "semantic_equivalence":False,
        },
        surface_claim=True,
    )

# ---- Formalized integration fixes discovered during v0.2.8 ----

def derivation_atom_conclusion_only(analysis, *, target_ref, start, end, dialect_scope=("UNKNOWN",)):
    return EvidenceAtom(
        atom_id=str(uuid.uuid4()),target_ref=target_ref,target_start=start,target_end=end,
        claim_type="DERIVATIONAL_ANALYSIS",
        value={"der_types":tuple(sorted(getattr(analysis,"der_types",()) or ()))},
        provenance_type="DERIVATIONAL_ANALYSIS",
        source_ids=tuple(getattr(analysis,"source_ids",()) or ()),
        dialect_scope=dialect_scope or ("UNKNOWN",),
        epistemic_status="DOCUMENTED",evidence_strength="STRONG",
        raw_payload={
            "entry_id":getattr(analysis,"entry_id",None),
            "headword_evidence_raw":getattr(analysis,"headword_evidence_raw",None),
            "pdlma_evidence_raw":getattr(analysis,"pdlma_evidence_raw",None),
        },
        surface_claim=True,
    )

def prerequisite_only_blocked(a:AdjudicatedClaim)->bool:
    if a.adjudication_status!="BLOCKED":
        return False
    blockers=tuple(a.claim.blockers or ())
    return bool(blockers) and all(str(b).startswith("REQUIRES_") for b in blockers)

def _policy_open(a:AdjudicatedClaim)->bool:
    values=[]
    c=a.claim
    if isinstance(c.value,dict):
        for k in ("orthographic_policy","surface_policy","policy","status"):
            v=c.value.get(k)
            if isinstance(v,str): values.append(v)
    values.extend(c.blockers)
    return any(
        ("OPEN" in str(v)) or ("PENDING_POLICY" in str(v))
        or str(v)=="PENDING_CLITIC_POLICY"
        for v in values
    )

class DecisionSimulatorV029(DecisionSimulator):
    def simulate_target(self,claims,*,target_ref,scope,observed_text=None,requested_dialect_scope=("UNKNOWN",)):
        claims=tuple(c for c in claims if c.claim.target_ref==target_ref)
        claim_ids=tuple(c.claim.claim_id for c in claims)
        if scope not in {"TOKEN","SPAN","UTTERANCE"}:
            raise ValueError("scope must be TOKEN, SPAN, or UTTERANCE")
        if not claims:
            return DecisionSimulation(
                str(uuid.uuid4()),target_ref,"RT-E-PRESERVE",scope,(),(),(),
                ("NO_ADJUDICATED_CLAIMS","INSUFFICIENT_EVIDENCE")
            )

        if any(c.adjudication_status=="CONFLICTING" for c in claims):
            return DecisionSimulation(
                str(uuid.uuid4()),target_ref,"RT-D-REVIEW",scope,claim_ids,(),(),
                ("CONFLICT_PRESENT",)
            )

        hard_blocked=[
            c for c in claims
            if c.adjudication_status=="BLOCKED" and not prerequisite_only_blocked(c)
        ]
        if hard_blocked:
            return DecisionSimulation(
                str(uuid.uuid4()),target_ref,"RT-D-REVIEW",scope,claim_ids,(),(),
                ("HARD_BLOCKER_PRESENT",)
            )

        policy_open=any(_policy_open(c) for c in claims if not prerequisite_only_blocked(c))
        if policy_open:
            if any(c.claim.claim_type=="ORTHOGRAPHIC_REPLACEMENT_CANDIDATE" for c in claims):
                return DecisionSimulation(
                    str(uuid.uuid4()),target_ref,"RT-D-REVIEW",scope,claim_ids,(),(),
                    ("ORTHOGRAPHIC_POLICY_OPEN_BLOCKS_PROPOSED_INTERVENTION",)
                )
            return DecisionSimulation(
                str(uuid.uuid4()),target_ref,"RT-E-PRESERVE",scope,claim_ids,(),(),
                ("ORTHOGRAPHIC_POLICY_OPEN_PRESERVE_ORIGINAL","PRESERVE_DOES_NOT_MEAN_CORRECT"),
                utterance_validation=False
            )

        substantive=[c for c in claims if c.adjudication_status=="SUPPORTED"]
        if substantive and not any(
            _scope_compatible(c.claim.dialect_scope,requested_dialect_scope)
            for c in substantive
        ):
            return DecisionSimulation(
                str(uuid.uuid4()),target_ref,"RT-D-REVIEW",scope,claim_ids,(),(),
                ("DIALECT_SCOPE_INCOMPATIBLE_OR_UNKNOWN",)
            )

        validated=[
            c for c in claims if _explicit_validation(c)
            and _scope_compatible(c.claim.dialect_scope,requested_dialect_scope)
            and _validation_scope_matches(c,scope)
        ]
        if validated:
            reasons=["EXPLICIT_ACCEPTANCE_AT_EXACT_TARGET_SCOPE"]
            if any(c.claim.validation_status=="PROJECT_EDITORIAL_DECISION" for c in validated):
                reasons.append("PROJECT_EDITORIAL_DECISION_NOT_UNIVERSALIZED")
            return DecisionSimulation(
                str(uuid.uuid4()),target_ref,"RT-A-ACCEPT_AT_SCOPE",scope,
                tuple(c.claim.claim_id for c in validated),(),(),tuple(reasons),
                utterance_validation=(scope=="UTTERANCE")
            )

        # Exact documentary surface claims are accepted only at TOKEN/SPAN.
        if scope!="UTTERANCE":
            exact=[
                c for c in claims
                if _exact_surface_documented(c,observed_text)
                and _scope_compatible(c.claim.dialect_scope,requested_dialect_scope)
            ]
            if exact:
                reasons=[]
                for c in exact:
                    for r in c.claim.rule_ids:
                        if r in {"EXACT_DOCUMENTED_HEADWORD_SURFACE","EXACT_DOCUMENTED_EXAMPLE_SURFACE"}:
                            reasons.append(r)
                if not reasons: reasons=["EXACT_DOCUMENTED_SURFACE_AT_THIS_SCOPE"]
                return DecisionSimulation(
                    str(uuid.uuid4()),target_ref,"RT-A-EXACT",scope,
                    tuple(c.claim.claim_id for c in exact),(),(),tuple(dict.fromkeys(reasons)),
                    utterance_validation=False
                )

        repl=[(c,_replacement_candidate(c)) for c in claims]
        repl=[(c,v) for c,v in repl if v is not None and _scope_compatible(c.claim.dialect_scope,requested_dialect_scope)]
        if repl:
            edits=[]
            for c,v in repl:
                edits.append(CandidateEdit(
                    edit_id=str(uuid.uuid4()),target_ref=target_ref,
                    start_original=int(v["start_original"]),end_original=int(v["end_original"]),
                    original=str(v["original"]),replacement=str(v["replacement"]),
                    operation_type=str(v["operation_type"]),
                    claim_ids=(c.claim.claim_id,),rule_ids=c.claim.rule_ids,
                    dialect_scope=c.claim.dialect_scope
                ))
            if observed_text is not None:
                validate_candidate_edits(edits,observed_text)
            return DecisionSimulation(
                str(uuid.uuid4()),target_ref,"RT-C-SUGGEST",scope,
                tuple(c.claim.claim_id for c,_ in repl),(),tuple(edits),
                ("SUPPORTED_REPLACEMENT_CANDIDATE_SIMULATION_ONLY",),
                utterance_validation=False
            )

        reasons=["NO_POSITIVE_BASIS_FOR_INTERVENTION","PRESERVE_DOES_NOT_MEAN_CORRECT"]
        if any(prerequisite_only_blocked(c) for c in claims):
            reasons.append("PREREQUISITE_EVIDENCE_MISSING_NOT_REVIEW_CONFLICT")
        return DecisionSimulation(
            str(uuid.uuid4()),target_ref,"RT-E-PRESERVE",scope,claim_ids,(),(),tuple(reasons),
            utterance_validation=False
        )

def status()->dict[str,Any]:
    return {
        "runtime_version":RUNTIME_VERSION,
        "runtime_stage":RUNTIME_STAGE,
        "surface_attestation_index":"IMPLEMENTED",
        "example_surface_evidence":"IMPLEMENTED_EXACT_ONLY",
        "surface_to_nonhabitual_tam_mapping":"NOT_IMPLEMENTED",
        "pdlma_to_surface":"PROHIBITED",
        "auto_correct_enabled":False,
        "orthographic_suggestions_enabled":False,
        "edit_execution_enabled":False,
        "user_visible_suggestions_enabled":False,
    }
