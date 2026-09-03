#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Iterable, Any
import uuid

from didxaza_runtime_v0_2_6_evidence_adjudication import AdjudicatedClaim

RUNTIME_VERSION = "0.2.7"
RUNTIME_STAGE = "DECISION_SIMULATION"

AUTO_CORRECT_ENABLED = False
ORTHOGRAPHIC_SUGGESTIONS_ENABLED = False
EDIT_EXECUTION_ENABLED = False
USER_VISIBLE_SUGGESTIONS_ENABLED = False

ACTIONS = frozenset({
    "RT-A-EXACT",
    "RT-A-ACCEPT_AT_SCOPE",
    "RT-B-PARTIAL",
    "RT-C-SUGGEST",
    "RT-D-REVIEW",
    "RT-E-PRESERVE",
})
SCOPES = frozenset({"TOKEN","SPAN","UTTERANCE","PARTIAL"})

OPEN_POLICY_CODES = frozenset({
    "PENDING_CLITIC_POLICY",
    "CLITIC_SPACING_POLICY_OPEN",
    "GENDA_SURFACE_POLICY_OPEN",
    "GLOTOTONYM_SURFACE_PROJECT_DECISION",
    "VISIBLE_TONE_PENDING_POLICY",
    "SURFACE_FORM_POLICY_OPEN",
})

@dataclass(frozen=True)
class CandidateEdit:
    edit_id: str
    target_ref: str
    start_original: int
    end_original: int
    original: str
    replacement: str
    operation_type: str
    claim_ids: tuple[str,...]
    rule_ids: tuple[str,...]
    dialect_scope: tuple[str,...]
    simulation_only: bool = True
    executable: bool = False
    visible_to_user: bool = False

    def __post_init__(self):
        if self.start_original < 0 or self.end_original < self.start_original:
            raise ValueError("Invalid CandidateEdit offsets")
        if not self.simulation_only or self.executable or self.visible_to_user:
            raise ValueError("v0.2.7 CandidateEdit must remain simulation-only/non-executable/non-visible")

@dataclass(frozen=True)
class UnresolvedSpan:
    target_ref: str
    start_original: int
    end_original: int
    text: str
    reason_codes: tuple[str,...]
    claim_ids: tuple[str,...] = ()

    def __post_init__(self):
        if self.start_original < 0 or self.end_original < self.start_original:
            raise ValueError("Invalid UnresolvedSpan offsets")

@dataclass(frozen=True)
class DecisionSimulation:
    decision_id: str
    target_ref: str
    action: str
    action_scope: str
    claim_ids: tuple[str,...]
    unresolved_spans: tuple[UnresolvedSpan,...]
    candidate_edits: tuple[CandidateEdit,...]
    reason_codes: tuple[str,...]
    utterance_validation: bool = False
    simulation_only: bool = True
    edit_execution_enabled: bool = False
    user_visible_suggestions_enabled: bool = False

    def __post_init__(self):
        if self.action not in ACTIONS:
            raise ValueError(f"Unsupported action: {self.action}")
        if self.action_scope not in SCOPES:
            raise ValueError(f"Unsupported scope: {self.action_scope}")
        if not self.simulation_only or self.edit_execution_enabled or self.user_visible_suggestions_enabled:
            raise ValueError("v0.2.7 decisions are simulation-only with execution/visibility disabled")

def _claim_policy_open(a: AdjudicatedClaim) -> bool:
    c=a.claim
    values=[]
    if isinstance(c.value,dict):
        for key in ("orthographic_policy","surface_policy","policy","status"):
            v=c.value.get(key)
            if isinstance(v,str): values.append(v)
    values.extend(c.blockers)
    return any(v in OPEN_POLICY_CODES or "OPEN" in v or "PENDING_POLICY" in v for v in values)

def _scope_compatible(claim_scope: tuple[str,...], requested_scope: tuple[str,...]) -> bool:
    if not requested_scope or requested_scope==("UNKNOWN",):
        return True
    if not claim_scope or claim_scope==("UNKNOWN",):
        return False
    return set(requested_scope).issubset(set(claim_scope))

def _exact_surface_documented(a: AdjudicatedClaim, observed_text: Optional[str]) -> bool:
    c=a.claim
    # Replacement proposals are never exact attestations. They must travel
    # exclusively through the RT-C-SUGGEST simulation gate.
    if c.claim_type=="ORTHOGRAPHIC_REPLACEMENT_CANDIDATE":
        return False
    if a.adjudication_status!="SUPPORTED":
        return False
    if c.epistemic_status!="DOCUMENTED" or not c.surface_claim:
        return False
    if c.conflict_status!="NONE" or c.blockers:
        return False
    if observed_text is None:
        return False

    # Claims may encode the documented surface in different explicit fields.
    candidates=[]
    if isinstance(c.value,str):
        candidates.append(c.value)
    if isinstance(c.value,dict):
        for k in ("surface","headword","observed_surface","documented_surface","original"):
            if isinstance(c.value.get(k),str):
                candidates.append(c.value[k])
    return observed_text in candidates

def _validation_scope_matches(a: AdjudicatedClaim, requested_action_scope: str) -> bool:
    c=a.claim
    if requested_action_scope=="UTTERANCE":
        # A span-targeted validation can never validate the full utterance.
        return c.target_start is None and c.target_end is None
    if requested_action_scope in {"TOKEN","SPAN"}:
        return True
    return False

def _explicit_validation(a: AdjudicatedClaim) -> bool:
    return (
        a.adjudication_status=="SUPPORTED"
        and a.claim.validation_status in {
            "SPEAKER_ORTHOGRAPHICALLY_VALIDATED",
            "PROJECT_EDITORIAL_DECISION",
        }
        and a.claim.surface_claim
        and a.claim.conflict_status=="NONE"
        and not a.claim.blockers
    )

def _replacement_candidate(a: AdjudicatedClaim):
    c=a.claim
    if c.claim_type!="ORTHOGRAPHIC_REPLACEMENT_CANDIDATE":
        return None
    if a.adjudication_status!="SUPPORTED":
        return None
    if c.conflict_status!="NONE" or c.blockers or _claim_policy_open(a):
        return None
    if not c.surface_claim:
        return None
    if not isinstance(c.value,dict):
        return None
    required=("start_original","end_original","original","replacement","operation_type")
    if not all(k in c.value for k in required):
        return None
    return c.value

def validate_candidate_edits(edits: Iterable[CandidateEdit], original_text: str):
    edits=sorted(tuple(edits),key=lambda e:(e.start_original,e.end_original))
    prev_end=-1
    for e in edits:
        if e.end_original > len(original_text):
            raise ValueError("CandidateEdit outside original text bounds")
        if original_text[e.start_original:e.end_original] != e.original:
            raise ValueError("CandidateEdit original does not match original text")
        if e.start_original < prev_end:
            raise ValueError("Overlapping CandidateEdits are not allowed")
        prev_end=e.end_original
    return tuple(edits)

class DecisionSimulator:
    def simulate_target(
        self,
        claims: Iterable[AdjudicatedClaim],
        *,
        target_ref: str,
        scope: str,
        observed_text: Optional[str]=None,
        requested_dialect_scope: tuple[str,...]=("UNKNOWN",),
    ) -> DecisionSimulation:
        claims=tuple(c for c in claims if c.claim.target_ref==target_ref)
        claim_ids=tuple(c.claim.claim_id for c in claims)

        if scope not in {"TOKEN","SPAN","UTTERANCE"}:
            raise ValueError("simulate_target scope must be TOKEN, SPAN, or UTTERANCE")

        if not claims:
            return DecisionSimulation(
                str(uuid.uuid4()),target_ref,"RT-E-PRESERVE",scope,(),(),(),
                ("NO_ADJUDICATED_CLAIMS","INSUFFICIENT_EVIDENCE")
            )

        if any(c.adjudication_status in {"CONFLICTING","BLOCKED"} for c in claims):
            return DecisionSimulation(
                str(uuid.uuid4()),target_ref,"RT-D-REVIEW",scope,claim_ids,(),(),
                ("CONFLICT_OR_BLOCKER_PRESENT",)
            )

        if any(_claim_policy_open(c) for c in claims):
            return DecisionSimulation(
                str(uuid.uuid4()),target_ref,"RT-D-REVIEW",scope,claim_ids,(),(),
                ("ORTHOGRAPHIC_POLICY_OPEN",)
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

        validated=[c for c in claims if _explicit_validation(c)]
        compatible_validated=[
            c for c in validated
            if _scope_compatible(c.claim.dialect_scope,requested_dialect_scope)
            and _validation_scope_matches(c, scope)
        ]
        if compatible_validated:
            reasons=["EXPLICIT_ACCEPTANCE_AT_EXACT_TARGET_SCOPE"]
            if any(c.claim.validation_status=="PROJECT_EDITORIAL_DECISION" for c in compatible_validated):
                reasons.append("PROJECT_EDITORIAL_DECISION_NOT_UNIVERSALIZED")
            return DecisionSimulation(
                str(uuid.uuid4()),target_ref,"RT-A-ACCEPT_AT_SCOPE",scope,
                tuple(c.claim.claim_id for c in compatible_validated),(),(),tuple(reasons),
                utterance_validation=(scope=="UTTERANCE")
            )

        exact=[
            c for c in claims
            if _exact_surface_documented(c,observed_text)
            and _scope_compatible(c.claim.dialect_scope,requested_dialect_scope)
        ]
        if exact:
            return DecisionSimulation(
                str(uuid.uuid4()),target_ref,"RT-A-EXACT",scope,
                tuple(c.claim.claim_id for c in exact),(),(),
                ("EXACT_DOCUMENTED_SURFACE_AT_THIS_SCOPE",),
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

        return DecisionSimulation(
            str(uuid.uuid4()),target_ref,"RT-E-PRESERVE",scope,claim_ids,(),(),
            ("NO_POSITIVE_BASIS_FOR_INTERVENTION","PRESERVE_DOES_NOT_MEAN_CORRECT"),
            utterance_validation=False
        )

    def simulate_partial(
        self,
        *,
        target_ref: str,
        resolved_decisions: Iterable[DecisionSimulation],
        unresolved_spans: Iterable[UnresolvedSpan],
    ) -> DecisionSimulation:
        resolved=tuple(resolved_decisions)
        unresolved=tuple(unresolved_spans)
        if not unresolved:
            raise ValueError("RT-B-PARTIAL requires at least one unresolved span")
        accepted=tuple(
            d for d in resolved if d.action in {"RT-A-EXACT","RT-A-ACCEPT_AT_SCOPE"}
        )
        if not accepted:
            raise ValueError("RT-B-PARTIAL requires at least one resolved/accepted subspan")
        claim_ids=tuple(dict.fromkeys(cid for d in resolved for cid in d.claim_ids))
        return DecisionSimulation(
            decision_id=str(uuid.uuid4()),target_ref=target_ref,
            action="RT-B-PARTIAL",action_scope="PARTIAL",
            claim_ids=claim_ids,unresolved_spans=unresolved,candidate_edits=(),
            reason_codes=("MIXED_RESOLVED_AND_UNRESOLVED_SPANS","FULL_UTTERANCE_NOT_VALIDATED"),
            utterance_validation=False
        )

def status()->dict[str,Any]:
    return {
        "runtime_version":RUNTIME_VERSION,
        "runtime_stage":RUNTIME_STAGE,
        "decision_simulation":"IMPLEMENTED",
        "candidate_edit":"IMPLEMENTED_SIMULATION_ONLY",
        "unresolved_span":"IMPLEMENTED",
        "auto_correct_enabled":False,
        "orthographic_suggestions_enabled":False,
        "edit_execution_enabled":False,
        "user_visible_suggestions_enabled":False,
        "cor001_run_status":"NOT_RUN_FOR_V0_2_7",
    }
