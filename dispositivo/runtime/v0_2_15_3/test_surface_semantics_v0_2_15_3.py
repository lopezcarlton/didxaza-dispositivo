import unittest
from types import SimpleNamespace
from didxaza_runtime_v0_2_6_evidence_adjudication import EvidenceAtom,EvidenceGraph
from didxaza_runtime_v0_2_7_1_integration_fixes import derivation_atom_conclusion_only
from didxaza_runtime_v0_2_15_2_evidence_integrity import EvidenceAdjudicatorV0152
from didxaza_runtime_v0_2_15_3_surface_semantics_resolution_integrity import (
    DecisionSimulatorV0153,resolve_claims_v0153,qualify_claim_v0153,
    sanitize_analysis_atom_v0153,scope_compatible_v0153,canonical_community_scope,
)

def atom(i,ctype,value,*,scope=('UNKNOWN',),surface=True,prov='SOURCE_DIRECT',epi='DOCUMENTED',start=0,end=1):
    return EvidenceAtom(atom_id=i,target_ref='T',target_start=start,target_end=end,claim_type=ctype,value=value,
        provenance_type=prov,source_ids=(i,),dialect_scope=scope,epistemic_status=epi,evidence_strength='STRONG',surface_claim=surface)

class SurfaceSemanticsTests(unittest.TestCase):
    def adjudicate(self,*atoms): return EvidenceAdjudicatorV0152(EvidenceGraph(atoms)).adjudicate()
    def test_person_exact_is_surface_and_resolution_agrees(self):
        cs=self.adjudicate(atom('p','DOCUMENTED_PERSON_FORM',{'surface':'lii'},scope=('JUCHITAN_HISTORICAL_SOURCE',),end=3))
        self.assertTrue(qualify_claim_v0153(cs[0]).can_support_surface)
        rv=resolve_claims_v0153(cs,target_ref='T',requested_dialect_scope=('JUCHITAN',))
        self.assertEqual(rv.surface_status,'DOCUMENTED_EXACT');self.assertFalse(rv.orthographic_unresolved)
        d=DecisionSimulatorV0153().simulate_target(cs,target_ref='T',scope='SPAN',observed_text='lii',requested_dialect_scope=('JUCHITAN',),target_start=0,target_end=3)
        self.assertEqual(d.action,'RT-A-EXACT')
    def test_possession_exact_is_surface(self):
        cs=self.adjudicate(atom('p','DOCUMENTED_POSSESSION_FORM',{'surface':'xtibe'},scope=('JUCHITAN_HISTORICAL_SOURCE',),end=5))
        self.assertFalse(resolve_claims_v0153(cs,target_ref='T',requested_dialect_scope=('JUCHITAN',)).orthographic_unresolved)
    def test_derivational_analysis_never_surface_positive(self):
        a=atom('d','DERIVATIONAL_ANALYSIS',{'surface':'x'},surface=True,prov='DERIVATIONAL_ANALYSIS')
        cs=self.adjudicate(a);q=qualify_claim_v0153(cs[0])
        self.assertEqual(q.qualification,'ANALYSIS_POSITIVE');self.assertFalse(q.can_support_surface)
    def test_legacy_derivation_surface_claim_is_sanitized(self):
        x=SimpleNamespace(entry_id='E',der_types=('CAUSATIVE',),source_ids=('S',),headword_evidence_raw='x',pdlma_evidence_raw='x')
        a=derivation_atom_conclusion_only(x,target_ref='T',start=0,end=1)
        self.assertTrue(a.surface_claim)
        b=sanitize_analysis_atom_v0153(a)
        self.assertFalse(b.surface_claim);self.assertTrue(b.raw_payload['legacy_surface_claim_sanitized'])
    def test_exact_surface_requires_exact_target_span(self):
        cs=self.adjudicate(atom('s','DOCUMENTED_SURFACE_ATTESTATION',{'surface':'na laca'},start=0,end=2))
        sim=DecisionSimulatorV0153()
        d=sim.simulate_target(cs,target_ref='T',scope='SPAN',observed_text='na laca',target_start=0,target_end=7)
        self.assertNotEqual(d.action,'RT-A-EXACT')
    def test_span_coordinates_required(self):
        cs=self.adjudicate(atom('s','DOCUMENTED_SURFACE_ATTESTATION',{'surface':'x'}))
        with self.assertRaises(ValueError): DecisionSimulatorV0153().simulate_target(cs,target_ref='T',scope='SPAN',observed_text='x')
    def test_historical_scope_alias_matches_juchitan(self):
        self.assertTrue(scope_compatible_v0153(('JUCHITAN_HISTORICAL_SOURCE',),('JUCHITAN',)))
        self.assertFalse(scope_compatible_v0153(('JUCHITAN_HISTORICAL_SOURCE',),('XADANI',)))
        self.assertEqual(canonical_community_scope(('JUCHITAN_HISTORICAL_SOURCE',)),('JUCHITAN',))
    def test_unknown_not_fallback_to_named_scope(self):
        self.assertFalse(scope_compatible_v0153(('UNKNOWN',),('JUCHITAN',)))
    def test_provenance_type_is_in_grouping_identity(self):
        cs=self.adjudicate(atom('a','DOCUMENTED_SURFACE_ATTESTATION',{'surface':'x'},prov='SOURCE_DIRECT'),atom('b','DOCUMENTED_SURFACE_ATTESTATION',{'surface':'x'},prov='ENGINEERING_HEURISTIC'))
        self.assertEqual(len(cs),2);self.assertEqual({x.claim.provenance_types for x in cs},{('SOURCE_DIRECT',),('ENGINEERING_HEURISTIC',)})
    def test_replacement_stays_non_surface(self):
        cs=self.adjudicate(atom('r','ORTHOGRAPHIC_REPLACEMENT_CANDIDATE',{'surface':'x','original':'x','replacement':'y','start_original':0,'end_original':1,'operation_type':'SUB'}))
        self.assertFalse(qualify_claim_v0153(cs[0]).can_support_surface)

if __name__=='__main__':unittest.main()
