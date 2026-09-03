#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable,Any

RUNTIME_VERSION="0.2.13"
RUNTIME_STAGE="RESOLUTION_VECTORS_SURFACE_ALIGNMENT_II"
AUTO_CORRECT_ENABLED=False
ORTHOGRAPHIC_SUGGESTIONS_ENABLED=False
EDIT_EXECUTION_ENABLED=False
USER_VISIBLE_SUGGESTIONS_ENABLED=False

SURFACE_TYPES={"DOCUMENTED_SURFACE_ATTESTATION","SURFACE_ACCEPTABILITY"}

@dataclass(frozen=True)
class ResolutionVector:
    target_ref:str
    surface_status:str
    morphology_status:str
    bound_status:str
    semantic_status:str
    dialect_status:str
    intervention_status:str
    orthographic_unresolved:bool
    analysis_open:bool
    review_required:bool
    supporting_claim_ids:tuple[str,...]
    open_claim_ids:tuple[str,...]
    reason_codes:tuple[str,...]

def _claim(a):
    return a.claim if hasattr(a,"claim") else a["claim"]

def _status(a):
    return a.adjudication_status if hasattr(a,"adjudication_status") else a["adjudication_status"]

def _get(c,name,default=None):
    return getattr(c,name,default) if not isinstance(c,dict) else c.get(name,default)

def _policy_value(c):
    v=_get(c,"value")
    if not isinstance(v,dict): return ""
    return " ".join(str(v.get(k,"")) for k in ("orthographic_policy","surface_policy","policy","status"))

def resolve_claims(claims:Iterable[Any],*,target_ref:str)->ResolutionVector:
    claims=tuple(claims)
    if not claims:
        return ResolutionVector(
            target_ref,"UNKNOWN","NONE","NONE","UNKNOWN","UNKNOWN","PRESERVE",
            True,False,False,(),(),("NO_EVIDENCE",)
        )

    supported_surface=[]
    validated_surface=[]
    surface_conflict=[]
    morph=[]
    bound=[]
    semantic=[]
    scopes=set()
    open_ids=[]
    support_ids=[]

    for a in claims:
        c=_claim(a); st=_status(a)
        cid=_get(c,"claim_id","")
        ct=_get(c,"claim_type","")
        val=_get(c,"validation_status","NONE")
        scope=tuple(_get(c,"dialect_scope",()) or ())
        scopes.update(scope)
        if ct in SURFACE_TYPES and _get(c,"surface_claim",False):
            if st=="SUPPORTED":
                supported_surface.append(a); support_ids.append(cid)
                if val in {"SPEAKER_ORTHOGRAPHICALLY_VALIDATED","PROJECT_EDITORIAL_DECISION"}:
                    validated_surface.append(a)
            elif st=="CONFLICTING":
                surface_conflict.append(a); open_ids.append(cid)

        if ct in {"MORPHOLOGICAL_ANALYSIS","DERIVATIONAL_ANALYSIS","PERSON_SUFFIX_CANDIDATE",
                  "POSSESSION_PREFIX_CANDIDATE","NA_ANALYSIS","DOCUMENTARY_PERSON",
                  "DOCUMENTARY_TAM","DOCUMENTARY_POSSESSION"}:
            morph.append(a)
        if ct in {"BOUND_ANALYSIS","BOUND_STRUCTURAL_HYPOTHESIS"}:
            bound.append(a)
        if ct in {"DOCUMENTARY_PHRASE_MEANING","SOURCE_SENTENCE_ALTERNATIVE"}:
            semantic.append(a)

    # Surface dimension.
    if surface_conflict:
        surface_status="CONFLICTING_SURFACE"
    elif validated_surface:
        surface_status="VALIDATED_AT_SCOPE"
    elif supported_surface:
        surface_status="DOCUMENTED_EXACT"
    else:
        surface_status="UNATTESTED"

    # Morphology dimension.
    if any(_status(a)=="CONFLICTING" for a in morph):
        morphology_status="CONFLICTING"
    elif any(_status(a)=="SUPPORTED" for a in morph):
        # Supported analysis may coexist with provisional candidates; still mark analysis open below.
        morphology_status="SUPPORTED"
    elif any(
        _status(a)=="BLOCKED" and all(str(x).startswith("REQUIRES_") for x in tuple(_get(_claim(a),"blockers",()) or ()))
        for a in morph
    ):
        morphology_status="PREREQUISITE_MISSING"
    elif morph:
        morphology_status="PROVISIONAL"
    else:
        morphology_status="NONE"

    # BOUND dimension.
    if any(_status(a)=="CONFLICTING" for a in bound):
        bound_status="CONFLICTING"
    elif any("OPEN" in _policy_value(_claim(a)) or "PENDING" in _policy_value(_claim(a)) for a in bound):
        bound_status="DOCUMENTED_POLICY_OPEN" if any(_status(a)=="SUPPORTED" for a in bound) else "STRUCTURALLY_SUPPORTED"
    elif any(_status(a)=="SUPPORTED" for a in bound):
        bound_status="DOCUMENTED_POLICY_CLOSED"
    elif bound:
        bound_status="STRUCTURALLY_SUPPORTED"
    else:
        bound_status="NONE"

    semantic_status="DOCUMENTED_PHRASE" if any(_status(a)=="SUPPORTED" for a in semantic) else "UNKNOWN"
    dialect_status="UNKNOWN" if not scopes or scopes=={"UNKNOWN"} else "SCOPED_NOT_UNIVERSAL"

    morph_open = (
        morphology_status in {"CONFLICTING","PREREQUISITE_MISSING","PROVISIONAL"}
        or any(_status(a) in {"BLOCKED","PROVISIONAL","UNRESOLVED","CONFLICTING"} for a in morph)
    )
    bound_open = bound_status in {"DOCUMENTED_POLICY_OPEN","STRUCTURALLY_SUPPORTED","CONFLICTING"}
    analysis_open=morph_open or bound_open
    review_required=(
        surface_status=="CONFLICTING_SURFACE"
        or morphology_status=="CONFLICTING"
        or bound_status=="CONFLICTING"
        or any(
            _status(a)=="BLOCKED" and not all(str(x).startswith("REQUIRES_") for x in tuple(_get(_claim(a),"blockers",()) or ()))
            for a in claims
        )
    )

    for a in claims:
        c=_claim(a); cid=_get(c,"claim_id","")
        if _status(a) in {"BLOCKED","PROVISIONAL","UNRESOLVED","CONFLICTING"}:
            open_ids.append(cid)
        if _status(a)=="SUPPORTED":
            support_ids.append(cid)

    orthographic_unresolved=surface_status not in {"DOCUMENTED_EXACT","VALIDATED_AT_SCOPE"}
    if review_required:
        intervention_status="REVIEW"
    else:
        intervention_status="PRESERVE"

    reasons=[]
    if surface_status=="DOCUMENTED_EXACT": reasons.append("SURFACE_DOCUMENTED_EXACT")
    if surface_status=="VALIDATED_AT_SCOPE": reasons.append("SURFACE_VALIDATED_AT_SCOPE")
    if orthographic_unresolved: reasons.append("SURFACE_NOT_DOCUMENTED_EXACT")
    if morphology_status=="CONFLICTING": reasons.append("MORPHOLOGY_CONFLICT")
    if morphology_status=="PREREQUISITE_MISSING": reasons.append("MORPHOLOGY_PREREQUISITE_MISSING")
    if bound_status=="DOCUMENTED_POLICY_OPEN": reasons.append("BOUND_POLICY_OPEN")
    if bound_status=="CONFLICTING": reasons.append("BOUND_CONFLICT")
    if analysis_open: reasons.append("ANALYSIS_REMAINS_OPEN")
    if review_required: reasons.append("REVIEW_REQUIRED")

    return ResolutionVector(
        target_ref,surface_status,morphology_status,bound_status,semantic_status,dialect_status,
        intervention_status,orthographic_unresolved,analysis_open,review_required,
        tuple(dict.fromkeys(support_ids)),tuple(dict.fromkeys(open_ids)),tuple(reasons)
    )

def status()->dict[str,Any]:
    return {
        "runtime_version":RUNTIME_VERSION,
        "runtime_stage":RUNTIME_STAGE,
        "resolution_vector":"IMPLEMENTED",
        "surface_and_analysis_separated":True,
        "open_bound_policy_erases_surface_attestation":False,
        "auto_correct_enabled":False,
        "orthographic_suggestions_enabled":False,
        "edit_execution_enabled":False,
        "user_visible_suggestions_enabled":False,
        "pdlma_to_surface":"PROHIBITED",
    }
