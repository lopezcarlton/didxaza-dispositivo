import unittest
from didxaza_runtime_v0_2_6_evidence_adjudication import EvidenceAtom,EvidenceGraph
from didxaza_runtime_v0_2_15_2_evidence_integrity import (
    EvidenceAdjudicatorV0152,DecisionSimulatorV0152,qualify_claim_v0152
)

def atom(i, *, scope, epi='DOCUMENTED', validation='NONE', surface=True,
         value=None, ctype='DOCUMENTED_SURFACE_ATTESTATION', provenance='SOURCE_DIRECT', source='SRC'):
    return EvidenceAtom(
        atom_id=i,target_ref='T',target_start=0,target_end=1,claim_type=ctype,
        value={'surface':'x'} if value is None else value,
        provenance_type=provenance,source_ids=(source,),dialect_scope=(scope,),
        epistemic_status=epi,validation_status=validation,
        evidence_strength='STRONG',surface_claim=surface
    )

class AdversarialRepairTests(unittest.TestCase):
    def test_validation_does_not_leak_across_dialects(self):
        atoms=[
            atom('J',scope='JUCHITAN',validation='SPEAKER_ORTHOGRAPHICALLY_VALIDATED'),
            atom('X',scope='XADANI',validation='NONE'),
        ]
        claims=EvidenceAdjudicatorV0152(EvidenceGraph(atoms)).adjudicate()
        self.assertEqual(len(claims),2)
        d=DecisionSimulatorV0152().simulate_target(
            claims,target_ref='T',scope='SPAN',observed_text='x',requested_dialect_scope=('XADANI',)
        )
        self.assertNotEqual(d.action,'RT-A-ACCEPT_AT_SCOPE')
        self.assertEqual(d.action,'RT-A-EXACT')

    def test_documented_and_surface_claim_do_not_cross_product(self):
        atoms=[
            atom('J2',scope='JUCHITAN',epi='DOCUMENTED',surface=False,ctype='TEST_SURFACE'),
            atom('X2',scope='XADANI',epi='PROVISIONAL',surface=True,ctype='TEST_SURFACE'),
        ]
        claims=EvidenceAdjudicatorV0152(EvidenceGraph(atoms)).adjudicate()
        self.assertEqual(len(claims),2)
        self.assertFalse(any(qualify_claim_v0152(c).can_support_surface for c in claims))

    def test_replacement_candidate_never_surface_positive(self):
        atoms=[atom(
            'R',scope='JUCHITAN',ctype='ORTHOGRAPHIC_REPLACEMENT_CANDIDATE',
            value={'surface':'x','start_original':0,'end_original':1,
                   'original':'x','replacement':'y','operation_type':'SUB'}
        )]
        claims=EvidenceAdjudicatorV0152(EvidenceGraph(atoms)).adjudicate()
        q=qualify_claim_v0152(claims[0])
        self.assertEqual(q.qualification,'INTERVENTION_PROPOSAL')
        self.assertFalse(q.can_support_surface)

    def test_unknown_scope_does_not_gain_named_community(self):
        atoms=[atom('U',scope='UNKNOWN')]
        claim=EvidenceAdjudicatorV0152(EvidenceGraph(atoms)).adjudicate()[0]
        self.assertEqual(claim.claim.dialect_scope,('UNKNOWN',))

    def test_claim_ids_are_deterministic_for_same_semantics(self):
        a1=[atom('A1',scope='JUCHITAN')]
        a2=[atom('DIFFERENT_ATOM_ID',scope='JUCHITAN')]
        c1=EvidenceAdjudicatorV0152(EvidenceGraph(a1)).adjudicate()[0].claim.claim_id
        c2=EvidenceAdjudicatorV0152(EvidenceGraph(a2)).adjudicate()[0].claim.claim_id
        self.assertEqual(c1,c2)

if __name__=='__main__': unittest.main()
