#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
from dataclasses import replace
from typing import Any, Iterable
import uuid

from didxaza_runtime_v0_2_6_evidence_adjudication import EvidenceAtom
from didxaza_runtime_v0_2_7_decision_simulation import DecisionSimulation,CandidateEdit,validate_candidate_edits,_validation_scope_matches,_explicit_validation,_replacement_candidate
from didxaza_runtime_v0_2_9_surface_evidence_coverage import prerequisite_only_blocked,_policy_open
from didxaza_runtime_v0_2_13_resolution_vectors import ResolutionVector,_claim,_status,_get,_policy_value
from didxaza_runtime_v0_2_15_2_evidence_integrity import (
    EvidenceAdjudicatorV0152,QualifiedEvidenceV0152,qualify_claim_v0152,
    SURFACE_POSITIVE_ALLOWLIST,REPLACEMENT_TYPES,HYPOTHESIS_TYPES,RETRIEVAL_TYPES,ANALYSIS_TYPES,
)

RUNTIME_VERSION='0.2.15.3'
RUNTIME_STAGE='SURFACE_SEMANTICS_RESOLUTION_INTEGRITY'
AUTO_CORRECT_ENABLED=False
ORTHOGRAPHIC_SUGGESTIONS_ENABLED=False
EDIT_EXECUTION_ENABLED=False
USER_VISIBLE_SUGGESTIONS_ENABLED=False

# One authoritative set for documentary surface evidence in this checkpoint.
SURFACE_EVIDENCE_TYPES=SURFACE_POSITIVE_ALLOWLIST
ANALYSIS_ONLY_TYPES=frozenset({
    'BOUND_ANALYSIS','BOUND_STRUCTURAL_HYPOTHESIS','MORPHOLOGICAL_ANALYSIS',
    'DERIVATIONAL_ANALYSIS','NA_ANALYSIS','DOCUMENTARY_PERSON','DOCUMENTARY_TAM',
    'DOCUMENTARY_POSSESSION','PICKETT_LEXICAL_RECORD',
})
HISTORICAL_SCOPE_ALIASES={'JUCHITAN_HISTORICAL_SOURCE':'JUCHITAN'}


def canonical_community_scope(scope:Iterable[str]|None)->tuple[str,...]:
    vals=tuple(scope or ('UNKNOWN',))
    mapped=[]
    for x in vals:
        if not x: continue
        mapped.append(HISTORICAL_SCOPE_ALIASES.get(x,x))
    if not mapped:return ('UNKNOWN',)
    # If UNKNOWN co-occurs with named scope, keep UNKNOWN as uncertainty, but named scope does not become universal.
    return tuple(sorted(set(mapped)))


def scope_compatible_v0153(claim_scope:tuple[str,...],requested_scope:tuple[str,...])->bool:
    if not requested_scope or requested_scope==('UNKNOWN',):return True
    cs=canonical_community_scope(claim_scope)
    rs=canonical_community_scope(requested_scope)
    if not cs or cs==('UNKNOWN',):return False
    return set(rs).issubset(set(cs))


def sanitize_analysis_atom_v0153(atom:EvidenceAtom)->EvidenceAtom:
    '''Analysis-only atoms cannot claim orthographic surface evidence, even if a legacy helper set surface_claim=True.'''
    if atom.claim_type in ANALYSIS_ONLY_TYPES and atom.surface_claim:
        payload=dict(atom.raw_payload or {})
        payload['legacy_surface_claim_sanitized']=True
        return replace(atom,surface_claim=False,raw_payload=payload)
    return atom


def qualify_claim_v0153(a:Any)->QualifiedEvidenceV0152:
    c=_claim(a); ct=_get(c,'claim_type','')
    if ct in ANALYSIS_ONLY_TYPES:
        st=_status(a); cid=_get(c,'claim_id','')
        if st=='CONFLICTING':
            return QualifiedEvidenceV0152(cid,ct,'CONFLICT',False,True,'ADJUDICATED_CONFLICT')
        if ct in RETRIEVAL_TYPES or _get(c,'epistemic_status','UNKNOWN')=='RETRIEVED_ONLY':
            return QualifiedEvidenceV0152(cid,ct,'RETRIEVAL_ONLY',False,False,'RETRIEVAL_IS_NOT_SURFACE_VALIDATION')
        if st=='SUPPORTED':
            return QualifiedEvidenceV0152(cid,ct,'ANALYSIS_POSITIVE',False,True,'ANALYSIS_ONLY_TYPE_NEVER_ATTESTS_SURFACE')
        return QualifiedEvidenceV0152(cid,ct,'HYPOTHESIS_ONLY',False,True,'ANALYSIS_NOT_SUPPORTED_AT_SURFACE')
    return qualify_claim_v0152(a)


def qualify_bundle_v0153(claims:Iterable[Any])->dict[str,Any]:
    qs=tuple(qualify_claim_v0153(a) for a in claims)
    return {
        'surface_positive':any(q.can_support_surface for q in qs),
        'analysis_positive':any(q.qualification=='ANALYSIS_POSITIVE' for q in qs),
        'retrieval_only':any(q.qualification=='RETRIEVAL_ONLY' for q in qs),
        'hypothesis_only':any(q.qualification=='HYPOTHESIS_ONLY' for q in qs),
        'conflict':any(q.qualification=='CONFLICT' for q in qs),
        'intervention_proposal':any(q.qualification=='INTERVENTION_PROPOSAL' for q in qs),
        'qualifications':qs,
    }


def _exact_surface_documented_v0153(a,observed_text,target_start,target_end):
    c=a.claim
    if c.claim_type not in SURFACE_EVIDENCE_TYPES:return False
    if a.adjudication_status!='SUPPORTED' or not c.surface_claim:return False
    if c.conflict_status!='NONE' or c.blockers or observed_text is None:return False
    if c.target_start!=target_start or c.target_end!=target_end:return False
    q=qualify_claim_v0153(a)
    if not q.can_support_surface:return False
    candidates=[]
    if isinstance(c.value,str):candidates.append(c.value)
    if isinstance(c.value,dict):
        for k in ('surface','headword','observed_surface','documented_surface'):
            if isinstance(c.value.get(k),str):candidates.append(c.value[k])
    return observed_text in candidates


class DecisionSimulatorV0153:
    def simulate_target(self,claims,*,target_ref,scope,observed_text=None,requested_dialect_scope=('UNKNOWN',),target_start=None,target_end=None):
        claims=tuple(c for c in claims if c.claim.target_ref==target_ref)
        claim_ids=tuple(c.claim.claim_id for c in claims)
        if scope not in {'TOKEN','SPAN','UTTERANCE'}:raise ValueError('scope must be TOKEN, SPAN, or UTTERANCE')
        if scope!='UTTERANCE' and (target_start is None or target_end is None):
            raise ValueError('TOKEN/SPAN decisions require target_start and target_end in v0.2.15.3')
        if not claims:
            return DecisionSimulation(str(uuid.uuid4()),target_ref,'RT-E-PRESERVE',scope,(),(),(),('NO_ADJUDICATED_CLAIMS','INSUFFICIENT_EVIDENCE'))
        if any(c.adjudication_status=='CONFLICTING' for c in claims):
            return DecisionSimulation(str(uuid.uuid4()),target_ref,'RT-D-REVIEW',scope,claim_ids,(),(),('CONFLICT_PRESENT',))
        hard_blocked=[c for c in claims if c.adjudication_status=='BLOCKED' and not prerequisite_only_blocked(c)]
        if hard_blocked:
            return DecisionSimulation(str(uuid.uuid4()),target_ref,'RT-D-REVIEW',scope,claim_ids,(),(),('HARD_BLOCKER_PRESENT',))
        policy_open=any(_policy_open(c) for c in claims if not prerequisite_only_blocked(c))
        if policy_open:
            if any(c.claim.claim_type=='ORTHOGRAPHIC_REPLACEMENT_CANDIDATE' for c in claims):
                return DecisionSimulation(str(uuid.uuid4()),target_ref,'RT-D-REVIEW',scope,claim_ids,(),(),('ORTHOGRAPHIC_POLICY_OPEN_BLOCKS_PROPOSED_INTERVENTION',))
            return DecisionSimulation(str(uuid.uuid4()),target_ref,'RT-E-PRESERVE',scope,claim_ids,(),(),('ORTHOGRAPHIC_POLICY_OPEN_PRESERVE_ORIGINAL','PRESERVE_DOES_NOT_MEAN_CORRECT'),utterance_validation=False)
        substantive=[c for c in claims if c.adjudication_status=='SUPPORTED']
        if substantive and not any(scope_compatible_v0153(c.claim.dialect_scope,requested_dialect_scope) for c in substantive):
            return DecisionSimulation(str(uuid.uuid4()),target_ref,'RT-D-REVIEW',scope,claim_ids,(),(),('DIALECT_SCOPE_INCOMPATIBLE_OR_UNKNOWN',))
        validated=[c for c in claims if _explicit_validation(c) and c.claim.claim_type in SURFACE_EVIDENCE_TYPES and scope_compatible_v0153(c.claim.dialect_scope,requested_dialect_scope) and _validation_scope_matches(c,scope)]
        if validated:
            reasons=['EXPLICIT_ACCEPTANCE_AT_EXACT_TARGET_SCOPE']
            if any(c.claim.validation_status=='PROJECT_EDITORIAL_DECISION' for c in validated):reasons.append('PROJECT_EDITORIAL_DECISION_NOT_UNIVERSALIZED')
            return DecisionSimulation(str(uuid.uuid4()),target_ref,'RT-A-ACCEPT_AT_SCOPE',scope,tuple(c.claim.claim_id for c in validated),(),(),tuple(reasons),utterance_validation=(scope=='UTTERANCE'))
        if scope!='UTTERANCE':
            exact=[c for c in claims if _exact_surface_documented_v0153(c,observed_text,target_start,target_end) and scope_compatible_v0153(c.claim.dialect_scope,requested_dialect_scope)]
            if exact:
                return DecisionSimulation(str(uuid.uuid4()),target_ref,'RT-A-EXACT',scope,tuple(c.claim.claim_id for c in exact),(),(),('EXACT_DOCUMENTED_SURFACE_AT_THIS_SCOPE',),utterance_validation=False)
        repl=[(c,_replacement_candidate(c)) for c in claims]
        repl=[(c,v) for c,v in repl if v is not None and scope_compatible_v0153(c.claim.dialect_scope,requested_dialect_scope)]
        if repl:
            edits=[]
            for c,v in repl:
                edits.append(CandidateEdit(edit_id=str(uuid.uuid4()),target_ref=target_ref,start_original=int(v['start_original']),end_original=int(v['end_original']),original=str(v['original']),replacement=str(v['replacement']),operation_type=str(v['operation_type']),claim_ids=(c.claim.claim_id,),rule_ids=c.claim.rule_ids,dialect_scope=c.claim.dialect_scope))
            if observed_text is not None:validate_candidate_edits(edits,observed_text)
            return DecisionSimulation(str(uuid.uuid4()),target_ref,'RT-C-SUGGEST',scope,tuple(c.claim.claim_id for c,_ in repl),(),tuple(edits),('SUPPORTED_REPLACEMENT_CANDIDATE_SIMULATION_ONLY',),utterance_validation=False)
        reasons=['NO_POSITIVE_BASIS_FOR_INTERVENTION','PRESERVE_DOES_NOT_MEAN_CORRECT']
        if any(prerequisite_only_blocked(c) for c in claims):reasons.append('PREREQUISITE_EVIDENCE_MISSING_NOT_REVIEW_CONFLICT')
        return DecisionSimulation(str(uuid.uuid4()),target_ref,'RT-E-PRESERVE',scope,claim_ids,(),(),tuple(reasons),utterance_validation=False)


def resolve_claims_v0153(claims:Iterable[Any],*,target_ref:str,requested_dialect_scope=('UNKNOWN',))->ResolutionVector:
    claims=tuple(claims)
    if not claims:
        return ResolutionVector(target_ref,'UNKNOWN','NONE','NONE','UNKNOWN','UNKNOWN','PRESERVE',True,False,False,(),(),('NO_EVIDENCE',))
    supported_surface=[];validated_surface=[];surface_conflict=[];morph=[];bound=[];semantic=[];scopes=set();open_ids=[];support_ids=[]
    for a in claims:
        c=_claim(a);st=_status(a);cid=_get(c,'claim_id','');ct=_get(c,'claim_type','');val=_get(c,'validation_status','NONE');scope=tuple(_get(c,'dialect_scope',()) or ())
        scopes.update(canonical_community_scope(scope))
        q=qualify_claim_v0153(a)
        if q.qualification=='CONFLICT' and ct in SURFACE_EVIDENCE_TYPES:
            surface_conflict.append(a);open_ids.append(cid)
        elif q.can_support_surface and scope_compatible_v0153(scope,requested_dialect_scope):
            supported_surface.append(a);support_ids.append(cid)
            if val in {'SPEAKER_ORTHOGRAPHICALLY_VALIDATED','PROJECT_EDITORIAL_DECISION'}:validated_surface.append(a)
        if ct in {'MORPHOLOGICAL_ANALYSIS','DERIVATIONAL_ANALYSIS','PERSON_SUFFIX_CANDIDATE','POSSESSION_PREFIX_CANDIDATE','NA_ANALYSIS','DOCUMENTARY_PERSON','DOCUMENTARY_TAM','DOCUMENTARY_POSSESSION'}:morph.append(a)
        if ct in {'BOUND_ANALYSIS','BOUND_STRUCTURAL_HYPOTHESIS'}:bound.append(a)
        if ct in {'DOCUMENTARY_PHRASE_MEANING','SOURCE_SENTENCE_ALTERNATIVE'}:semantic.append(a)
    if surface_conflict:surface_status='CONFLICTING_SURFACE'
    elif validated_surface:surface_status='VALIDATED_AT_SCOPE'
    elif supported_surface:surface_status='DOCUMENTED_EXACT'
    else:surface_status='UNATTESTED'
    if any(_status(a)=='CONFLICTING' for a in morph):morphology_status='CONFLICTING'
    elif any(_status(a)=='SUPPORTED' for a in morph):morphology_status='SUPPORTED'
    elif any(_status(a)=='BLOCKED' and all(str(x).startswith('REQUIRES_') for x in tuple(_get(_claim(a),'blockers',()) or ())) for a in morph):morphology_status='PREREQUISITE_MISSING'
    elif morph:morphology_status='PROVISIONAL'
    else:morphology_status='NONE'
    if any(_status(a)=='CONFLICTING' for a in bound):bound_status='CONFLICTING'
    elif any('OPEN' in _policy_value(_claim(a)) or 'PENDING' in _policy_value(_claim(a)) for a in bound):bound_status='DOCUMENTED_POLICY_OPEN' if any(_status(a)=='SUPPORTED' for a in bound) else 'STRUCTURALLY_SUPPORTED'
    elif any(_status(a)=='SUPPORTED' for a in bound):bound_status='DOCUMENTED_POLICY_CLOSED'
    elif bound:bound_status='STRUCTURALLY_SUPPORTED'
    else:bound_status='NONE'
    semantic_status='DOCUMENTED_PHRASE' if any(_status(a)=='SUPPORTED' for a in semantic) else 'UNKNOWN'
    dialect_status='UNKNOWN' if not scopes or scopes=={'UNKNOWN'} else 'SCOPED_NOT_UNIVERSAL'
    morph_open=(morphology_status in {'CONFLICTING','PREREQUISITE_MISSING','PROVISIONAL'} or any(_status(a) in {'BLOCKED','PROVISIONAL','UNRESOLVED','CONFLICTING'} for a in morph))
    bound_open=bound_status in {'DOCUMENTED_POLICY_OPEN','STRUCTURALLY_SUPPORTED','CONFLICTING'}
    analysis_open=morph_open or bound_open
    review_required=(surface_status=='CONFLICTING_SURFACE' or morphology_status=='CONFLICTING' or bound_status=='CONFLICTING' or any(_status(a)=='BLOCKED' and not all(str(x).startswith('REQUIRES_') for x in tuple(_get(_claim(a),'blockers',()) or ())) for a in claims))
    for a in claims:
        c=_claim(a);cid=_get(c,'claim_id','')
        if _status(a) in {'BLOCKED','PROVISIONAL','UNRESOLVED','CONFLICTING'}:open_ids.append(cid)
        if _status(a)=='SUPPORTED':support_ids.append(cid)
    orthographic_unresolved=surface_status not in {'DOCUMENTED_EXACT','VALIDATED_AT_SCOPE'}
    intervention_status='REVIEW' if review_required else 'PRESERVE'
    reasons=[]
    if surface_status=='DOCUMENTED_EXACT':reasons.append('SURFACE_DOCUMENTED_EXACT')
    if surface_status=='VALIDATED_AT_SCOPE':reasons.append('SURFACE_VALIDATED_AT_SCOPE')
    if orthographic_unresolved:reasons.append('SURFACE_NOT_DOCUMENTED_EXACT_AT_REQUESTED_SCOPE')
    if morphology_status=='CONFLICTING':reasons.append('MORPHOLOGY_CONFLICT')
    if morphology_status=='PREREQUISITE_MISSING':reasons.append('MORPHOLOGY_PREREQUISITE_MISSING')
    if bound_status=='DOCUMENTED_POLICY_OPEN':reasons.append('BOUND_POLICY_OPEN')
    if bound_status=='CONFLICTING':reasons.append('BOUND_CONFLICT')
    if analysis_open:reasons.append('ANALYSIS_REMAINS_OPEN')
    if review_required:reasons.append('REVIEW_REQUIRED')
    return ResolutionVector(target_ref,surface_status,morphology_status,bound_status,semantic_status,dialect_status,intervention_status,orthographic_unresolved,analysis_open,review_required,tuple(dict.fromkeys(support_ids)),tuple(dict.fromkeys(open_ids)),tuple(reasons))


def status()->dict[str,Any]:
    return {
        'runtime_version':RUNTIME_VERSION,'runtime_stage':RUNTIME_STAGE,
        'single_surface_evidence_allowlist':tuple(sorted(SURFACE_EVIDENCE_TYPES)),
        'person_possession_exact_documentary_surface':True,
        'analysis_only_surface_promotion':False,
        'derivational_analysis_surface_claim_sanitized':True,
        'exact_surface_requires_exact_target_span':True,
        'historical_scope_aliases':dict(HISTORICAL_SCOPE_ALIASES),
        'provenance_type_in_adjudication_key':True,
        'auto_correct_enabled':False,'orthographic_suggestions_enabled':False,
        'edit_execution_enabled':False,'user_visible_suggestions_enabled':False,
        'pdlma_to_surface':'PROHIBITED','near_match_to_surface':'PROHIBITED',
    }
