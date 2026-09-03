#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Iterable
import hashlib, json, uuid

from didxaza_runtime_v0_2_6_evidence_adjudication import EvidenceClaim,AdjudicatedClaim,EvidenceGraph
from didxaza_runtime_v0_2_7_decision_simulation import (
    DecisionSimulation,CandidateEdit,validate_candidate_edits,
    _scope_compatible,_validation_scope_matches,_explicit_validation,_replacement_candidate,
)
from didxaza_runtime_v0_2_9_surface_evidence_coverage import prerequisite_only_blocked,_policy_open

RUNTIME_VERSION='0.2.15.2'
RUNTIME_STAGE='EVIDENCE_INTEGRITY_REPAIR'
AUTO_CORRECT_ENABLED=False
ORTHOGRAPHIC_SUGGESTIONS_ENABLED=False
EDIT_EXECUTION_ENABLED=False
USER_VISIBLE_SUGGESTIONS_ENABLED=False

SURFACE_POSITIVE_ALLOWLIST=frozenset({
    'DOCUMENTED_SURFACE_ATTESTATION','SURFACE_ACCEPTABILITY',
    'DOCUMENTED_PERSON_FORM','DOCUMENTED_POSSESSION_FORM',
})
REPLACEMENT_TYPES=frozenset({'ORTHOGRAPHIC_REPLACEMENT_CANDIDATE'})
RETRIEVAL_TYPES=frozenset({'LEXICAL_ATTESTATION','PICKETT_LEXICAL_RECORD','SOURCE_SENTENCE_ALTERNATIVE'})
HYPOTHESIS_TYPES=frozenset({'PERSON_SUFFIX_CANDIDATE','POSSESSION_PREFIX_CANDIDATE'})
ANALYSIS_TYPES=frozenset({
    'BOUND_ANALYSIS','BOUND_STRUCTURAL_HYPOTHESIS','MORPHOLOGICAL_ANALYSIS',
    'DERIVATIONAL_ANALYSIS','NA_ANALYSIS','DOCUMENTARY_PERSON','DOCUMENTARY_TAM',
    'DOCUMENTARY_POSSESSION','PICKETT_LEXICAL_RECORD',
})
_STRENGTH_RANK={'UNKNOWN':0,'WEAK':1,'MODERATE':2,'STRONG':3,'DIRECT':4}

def _value_key(value:Any)->str:
    return json.dumps(value,ensure_ascii=False,sort_keys=True,default=str)

def _uniq(seq):
    return tuple(dict.fromkeys(x for x in seq if x is not None))

def _canon_scope(scope):
    vals=tuple(x for x in (scope or ('UNKNOWN',)) if x)
    if not vals:return ('UNKNOWN',)
    return tuple(sorted(set(vals)))

def _stable_claim_id(parts)->str:
    raw=json.dumps(parts,ensure_ascii=False,sort_keys=True,default=str,separators=(',',':'))
    return 'CLM-'+hashlib.sha256(raw.encode('utf-8')).hexdigest()[:24]

class EvidenceAdjudicatorV0152:
    '''Provenance-coherent adjudication: promotion properties never cross atoms.'''
    def __init__(self,graph:EvidenceGraph):
        self.graph=graph

    def _coherent_claims(self,atoms):
        groups=defaultdict(list)
        for a in atoms:
            key=(
                a.target_ref,a.target_start,a.target_end,a.claim_type,_value_key(a.value),
                _canon_scope(a.dialect_scope),a.epistemic_status,a.validation_status,
                bool(a.surface_claim),a.provenance_type,tuple(sorted(a.blockers or ())),
                a.conflict_status,
            )
            groups[key].append(a)
        out=[]
        for key,group in groups.items():
            (target_ref,start,end,claim_type,_,scope,epistemic,validation,
             surface_claim,provenance_type,blockers,conflict)=key
            source_ids=_uniq(x for a in group for x in a.source_ids)
            rule_ids=_uniq(x for a in group for x in a.rule_ids)
            evidence_strength=max((a.evidence_strength for a in group),
                                  key=lambda x:_STRENGTH_RANK.get(x,0),default='UNKNOWN')
            claim_id=_stable_claim_id({
                'target_ref':target_ref,'start':start,'end':end,'claim_type':claim_type,
                'value':group[0].value,'scope':scope,'epistemic':epistemic,
                'validation':validation,'surface_claim':surface_claim,
                'provenance_type':provenance_type,'blockers':blockers,'conflict':conflict,
                'source_ids':source_ids,'rule_ids':rule_ids,
            })
            out.append(EvidenceClaim(
                claim_id=claim_id,target_ref=target_ref,target_start=start,target_end=end,
                claim_type=claim_type,value=group[0].value,
                atom_ids=tuple(a.atom_id for a in group),provenance_types=(provenance_type,),
                source_ids=source_ids,rule_ids=rule_ids,dialect_scope=scope,
                epistemic_status=epistemic,validation_status=validation,
                evidence_strength=evidence_strength,conflict_status=conflict,
                blockers=blockers,surface_claim=surface_claim,
            ))
        return out

    def adjudicate(self,target_ref=None):
        atoms=list(self.graph.atoms() if target_ref is None else self.graph.atoms_for_target(target_ref))
        claims=self._coherent_claims(atoms)
        by_type=defaultdict(list)
        for c in claims:
            by_type[(c.target_ref,c.target_start,c.target_end,c.claim_type)].append(c)
        conflict_ids=set()
        for group in by_type.values():
            if len({_value_key(c.value) for c in group})<=1:continue
            substantive=[c for c in group if c.evidence_strength in {'DIRECT','STRONG','MODERATE'} and c.epistemic_status not in {'UNKNOWN','RETRIEVED_ONLY'}]
            if len({_value_key(c.value) for c in substantive})>1:
                conflict_ids.update(c.claim_id for c in substantive)
        out=[]
        for c in claims:
            notes=[]
            if c.claim_id in conflict_ids or c.conflict_status in {'PRESENT','UNRESOLVED_SOURCE_CONFLICT'}:
                status='CONFLICTING';notes.append('INCOMPATIBLE_SUPPORTED_VALUES_PRESERVED')
            elif c.blockers or c.conflict_status=='BLOCKED_BY_POLICY':
                status='BLOCKED';notes.append('BLOCKING_CONDITION_PRESENT')
            elif c.epistemic_status in {'DOCUMENTED','STRUCTURALLY_SUPPORTED'}:
                status='SUPPORTED'
            elif c.epistemic_status in {'PROVISIONAL','RETRIEVED_ONLY'}:
                status='PROVISIONAL'
            else:
                status='UNRESOLVED'
            if c.provenance_types==('ENGINEERING_HEURISTIC',) and status=='SUPPORTED':
                status='PROVISIONAL';notes.append('HEURISTIC_CANNOT_PROMOTE_TO_SUPPORTED')
            if c.provenance_types==('LEXICAL_RETRIEVAL',) and status=='SUPPORTED':
                status='PROVISIONAL';notes.append('RETRIEVAL_ONLY_NOT_VALIDATION')
            out.append(AdjudicatedClaim(c,status,tuple(notes)))
        return tuple(out)

@dataclass(frozen=True)
class QualifiedEvidenceV0152:
    claim_id:str
    claim_type:str
    qualification:str
    can_support_surface:bool
    can_support_analysis:bool
    reason:str

def _claim(a): return a.claim if hasattr(a,'claim') else a['claim']
def _status(a): return a.adjudication_status if hasattr(a,'adjudication_status') else a['adjudication_status']
def _get(c,k,d=None): return getattr(c,k,d) if not isinstance(c,dict) else c.get(k,d)

def qualify_claim_v0152(a:Any)->QualifiedEvidenceV0152:
    c=_claim(a);st=_status(a);cid=_get(c,'claim_id','');ct=_get(c,'claim_type','')
    epi=_get(c,'epistemic_status','UNKNOWN');surface=bool(_get(c,'surface_claim',False))
    validation=_get(c,'validation_status','NONE')
    if st=='CONFLICTING':
        return QualifiedEvidenceV0152(cid,ct,'CONFLICT',False,True,'ADJUDICATED_CONFLICT')
    if ct in REPLACEMENT_TYPES:
        return QualifiedEvidenceV0152(cid,ct,'INTERVENTION_PROPOSAL',False,False,'REPLACEMENT_CANDIDATE_NEVER_COUNTS_AS_SURFACE_EVIDENCE')
    if ct in HYPOTHESIS_TYPES:
        return QualifiedEvidenceV0152(cid,ct,'HYPOTHESIS_ONLY',False,True,'GRAPHIC_CANDIDATE_REQUIRES_DOCUMENTARY_CONFIRMATION')
    if ct in RETRIEVAL_TYPES or epi=='RETRIEVED_ONLY':
        return QualifiedEvidenceV0152(cid,ct,'RETRIEVAL_ONLY',False,False,'RETRIEVAL_IS_NOT_SURFACE_VALIDATION')
    explicit_valid=validation in {'SPEAKER_ORTHOGRAPHICALLY_VALIDATED','PROJECT_EDITORIAL_DECISION'}
    if ct in SURFACE_POSITIVE_ALLOWLIST and surface and st=='SUPPORTED':
        if ct=='SURFACE_ACCEPTABILITY':
            if explicit_valid:
                return QualifiedEvidenceV0152(cid,ct,'SURFACE_POSITIVE',True,False,'EXPLICIT_ORTHOGRAPHIC_VALIDATION')
        elif epi=='DOCUMENTED' or explicit_valid:
            return QualifiedEvidenceV0152(cid,ct,'SURFACE_POSITIVE',True,ct in ANALYSIS_TYPES,'ALLOWLISTED_SUPPORTED_DOCUMENTED_SURFACE')
    if ct in ANALYSIS_TYPES and st=='SUPPORTED':
        return QualifiedEvidenceV0152(cid,ct,'ANALYSIS_POSITIVE',False,True,'ANALYSIS_DOES_NOT_ATTEST_SURFACE')
    if ct in ANALYSIS_TYPES:
        return QualifiedEvidenceV0152(cid,ct,'HYPOTHESIS_ONLY',False,True,'ANALYSIS_NOT_SUPPORTED_AT_SURFACE')
    return QualifiedEvidenceV0152(cid,ct,'NONE',False,False,'NO_POSITIVE_EVIDENCE')

def qualify_bundle_v0152(claims:Iterable[Any])->dict[str,Any]:
    qs=tuple(qualify_claim_v0152(a) for a in claims)
    return {
        'surface_positive':any(q.can_support_surface for q in qs),
        'analysis_positive':any(q.qualification=='ANALYSIS_POSITIVE' for q in qs),
        'retrieval_only':any(q.qualification=='RETRIEVAL_ONLY' for q in qs),
        'hypothesis_only':any(q.qualification=='HYPOTHESIS_ONLY' for q in qs),
        'conflict':any(q.qualification=='CONFLICT' for q in qs),
        'intervention_proposal':any(q.qualification=='INTERVENTION_PROPOSAL' for q in qs),
        'qualifications':qs,
    }

def _exact_surface_documented_v0152(a,observed_text):
    c=a.claim
    if c.claim_type not in SURFACE_POSITIVE_ALLOWLIST:return False
    if a.adjudication_status!='SUPPORTED' or not c.surface_claim:return False
    if c.conflict_status!='NONE' or c.blockers or observed_text is None:return False
    if c.claim_type=='SURFACE_ACCEPTABILITY':
        if c.validation_status not in {'SPEAKER_ORTHOGRAPHICALLY_VALIDATED','PROJECT_EDITORIAL_DECISION'}:return False
    elif c.epistemic_status!='DOCUMENTED':return False
    candidates=[]
    if isinstance(c.value,str):candidates.append(c.value)
    if isinstance(c.value,dict):
        for k in ('surface','headword','observed_surface','documented_surface'):
            if isinstance(c.value.get(k),str):candidates.append(c.value[k])
    return observed_text in candidates

class DecisionSimulatorV0152:
    def simulate_target(self,claims,*,target_ref,scope,observed_text=None,requested_dialect_scope=('UNKNOWN',)):
        claims=tuple(c for c in claims if c.claim.target_ref==target_ref)
        claim_ids=tuple(c.claim.claim_id for c in claims)
        if scope not in {'TOKEN','SPAN','UTTERANCE'}:raise ValueError('scope must be TOKEN, SPAN, or UTTERANCE')
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
        if substantive and not any(_scope_compatible(c.claim.dialect_scope,requested_dialect_scope) for c in substantive):
            return DecisionSimulation(str(uuid.uuid4()),target_ref,'RT-D-REVIEW',scope,claim_ids,(),(),('DIALECT_SCOPE_INCOMPATIBLE_OR_UNKNOWN',))
        validated=[c for c in claims if _explicit_validation(c) and c.claim.claim_type in SURFACE_POSITIVE_ALLOWLIST and _scope_compatible(c.claim.dialect_scope,requested_dialect_scope) and _validation_scope_matches(c,scope)]
        if validated:
            reasons=['EXPLICIT_ACCEPTANCE_AT_EXACT_TARGET_SCOPE']
            if any(c.claim.validation_status=='PROJECT_EDITORIAL_DECISION' for c in validated):reasons.append('PROJECT_EDITORIAL_DECISION_NOT_UNIVERSALIZED')
            return DecisionSimulation(str(uuid.uuid4()),target_ref,'RT-A-ACCEPT_AT_SCOPE',scope,tuple(c.claim.claim_id for c in validated),(),(),tuple(reasons),utterance_validation=(scope=='UTTERANCE'))
        if scope!='UTTERANCE':
            exact=[c for c in claims if _exact_surface_documented_v0152(c,observed_text) and _scope_compatible(c.claim.dialect_scope,requested_dialect_scope)]
            if exact:
                reasons=[]
                for c in exact:
                    for r in c.claim.rule_ids:
                        if r in {'EXACT_DOCUMENTED_HEADWORD_SURFACE','EXACT_DOCUMENTED_EXAMPLE_SURFACE'}:reasons.append(r)
                if not reasons:reasons=['EXACT_DOCUMENTED_SURFACE_AT_THIS_SCOPE']
                return DecisionSimulation(str(uuid.uuid4()),target_ref,'RT-A-EXACT',scope,tuple(c.claim.claim_id for c in exact),(),(),tuple(dict.fromkeys(reasons)),utterance_validation=False)
        repl=[(c,_replacement_candidate(c)) for c in claims]
        repl=[(c,v) for c,v in repl if v is not None and _scope_compatible(c.claim.dialect_scope,requested_dialect_scope)]
        if repl:
            edits=[]
            for c,v in repl:
                edits.append(CandidateEdit(edit_id=str(uuid.uuid4()),target_ref=target_ref,start_original=int(v['start_original']),end_original=int(v['end_original']),original=str(v['original']),replacement=str(v['replacement']),operation_type=str(v['operation_type']),claim_ids=(c.claim.claim_id,),rule_ids=c.claim.rule_ids,dialect_scope=c.claim.dialect_scope))
            if observed_text is not None:validate_candidate_edits(edits,observed_text)
            return DecisionSimulation(str(uuid.uuid4()),target_ref,'RT-C-SUGGEST',scope,tuple(c.claim.claim_id for c,_ in repl),(),tuple(edits),('SUPPORTED_REPLACEMENT_CANDIDATE_SIMULATION_ONLY',),utterance_validation=False)
        reasons=['NO_POSITIVE_BASIS_FOR_INTERVENTION','PRESERVE_DOES_NOT_MEAN_CORRECT']
        if any(prerequisite_only_blocked(c) for c in claims):reasons.append('PREREQUISITE_EVIDENCE_MISSING_NOT_REVIEW_CONFLICT')
        return DecisionSimulation(str(uuid.uuid4()),target_ref,'RT-E-PRESERVE',scope,claim_ids,(),(),tuple(reasons),utterance_validation=False)

def status():
    return {
        'runtime_version':RUNTIME_VERSION,'runtime_stage':RUNTIME_STAGE,
        'provenance_coherent_aggregation':True,'validation_bound_to_scope':True,
        'surface_positive_allowlist':tuple(sorted(SURFACE_POSITIVE_ALLOWLIST)),
        'replacement_candidate_surface_positive':False,
        'source_coverage_as_dialect_scope':'PROHIBITED',
        'auto_correct_enabled':False,'orthographic_suggestions_enabled':False,
        'edit_execution_enabled':False,'user_visible_suggestions_enabled':False,
        'pdlma_to_surface':'PROHIBITED',
    }
