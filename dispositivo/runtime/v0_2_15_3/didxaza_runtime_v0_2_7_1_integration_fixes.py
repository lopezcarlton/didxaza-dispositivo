#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""General integration fixes discovered by the first fresh COR001 diagnostic.

The fixes are tested independently of COR001:
1) Derivational conclusion identity is separated from lexeme provenance.
2) Evidentiary prerequisite blockers (REQUIRES_*) do not force human review.

No linguistic rule is added.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, Optional
import uuid

from didxaza_runtime_v0_2_6_evidence_adjudication import (
    EvidenceAtom, AdjudicatedClaim
)
from didxaza_runtime_v0_2_7_decision_simulation import (
    DecisionSimulator, DecisionSimulation,
    _claim_policy_open, _scope_compatible, _explicit_validation,
    _validation_scope_matches, _exact_surface_documented, _replacement_candidate,
    CandidateEdit, validate_candidate_edits
)

VERSION="0.2.7.1-INTEGRATION-FIX"

def derivation_atom_conclusion_only(analysis, *, target_ref, start, end, dialect_scope=("UNKNOWN",)):
    """Structural conclusion is claim value; lexeme identity remains provenance payload."""
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

def prerequisite_only_blocked(a: AdjudicatedClaim) -> bool:
    if a.adjudication_status!="BLOCKED":
        return False
    blockers=tuple(a.claim.blockers or ())
    return bool(blockers) and all(str(b).startswith("REQUIRES_") for b in blockers)

class DecisionSimulatorIntegrationFixed(DecisionSimulator):
    def simulate_target(self, claims: Iterable[AdjudicatedClaim], *, target_ref: str,
                        scope: str, observed_text: Optional[str]=None,
                        requested_dialect_scope=("UNKNOWN",)):
        claims=tuple(c for c in claims if c.claim.target_ref==target_ref)
        claim_ids=tuple(c.claim.claim_id for c in claims)
        if scope not in {"TOKEN","SPAN","UTTERANCE"}:
            raise ValueError("simulate_target scope must be TOKEN, SPAN, or UTTERANCE")
        if not claims:
            return DecisionSimulation(
                str(uuid.uuid4()),target_ref,"RT-E-PRESERVE",scope,(),(),(),
                ("NO_ADJUDICATED_CLAIMS","INSUFFICIENT_EVIDENCE")
            )

        # Substantive conflict always requires review.
        if any(c.adjudication_status=="CONFLICTING" for c in claims):
            return DecisionSimulation(
                str(uuid.uuid4()),target_ref,"RT-D-REVIEW",scope,claim_ids,(),(),
                ("CONFLICT_PRESENT",)
            )

        # A prerequisite-only blocked hypothesis is unresolved evidence, not a policy conflict.
        hard_blocked=[
            c for c in claims
            if c.adjudication_status=="BLOCKED" and not prerequisite_only_blocked(c)
        ]
        if hard_blocked:
            return DecisionSimulation(
                str(uuid.uuid4()),target_ref,"RT-D-REVIEW",scope,claim_ids,(),(),
                ("HARD_BLOCKER_PRESENT",)
            )

        policy_open=any(_claim_policy_open(c) for c in claims if not prerequisite_only_blocked(c))
        # An open policy blocks intervention in that dimension. It does not
        # require human review merely to preserve the observed original.
        # If a future explicit replacement candidate exists under an open
        # policy, review is required instead of suggesting it.
        if policy_open:
            has_replacement=any(
                c.claim.claim_type=="ORTHOGRAPHIC_REPLACEMENT_CANDIDATE"
                for c in claims
            )
            if has_replacement:
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

        validated=[c for c in claims if _explicit_validation(c)]
        compatible_validated=[
            c for c in validated
            if _scope_compatible(c.claim.dialect_scope,requested_dialect_scope)
            and _validation_scope_matches(c,scope)
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
                ("EXACT_DOCUMENTED_SURFACE_AT_THIS_SCOPE",),utterance_validation=False
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
                ("SUPPORTED_REPLACEMENT_CANDIDATE_SIMULATION_ONLY",),utterance_validation=False
            )

        reasons=["NO_POSITIVE_BASIS_FOR_INTERVENTION","PRESERVE_DOES_NOT_MEAN_CORRECT"]
        if any(prerequisite_only_blocked(c) for c in claims):
            reasons.append("PREREQUISITE_EVIDENCE_MISSING_NOT_REVIEW_CONFLICT")
        return DecisionSimulation(
            str(uuid.uuid4()),target_ref,"RT-E-PRESERVE",scope,claim_ids,(),(),tuple(reasons),
            utterance_validation=False
        )
