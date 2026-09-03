#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "generator_v0"))
from runtime_reuse_adapter_v0 import load_generator_view, safe_generator_claim_view

RUNTIME = Path('/mnt/data/didxaza_v0_2_15_3_surface_semantics_resolution_integrity_CLOSED_PASS(1).zip')
DB = Path('/mnt/data/BASE_CORRECTOR_DIDXAZA_SURFACE_SEMANTICS_v2_20(1).sqlite')


class TestRuntimeReuse(unittest.TestCase):
    def test_existing_generator_view_is_reused_after_hash_gate(self):
        tmp, generator_view, mod, v153 = load_generator_view(RUNTIME, DB)
        try:
            good = mod.EvidenceAtom(
                atom_id=str(uuid.uuid4()), target_ref='NC001:TEST', target_start=None, target_end=None,
                claim_type='DOCUMENTARY_PHRASE_MEANING', value={'meaning':'test'}, provenance_type='SOURCE_DIRECT',
                source_ids=('TEST_SOURCE',), dialect_scope=('JUCHITAN',), epistemic_status='DOCUMENTED',
                evidence_strength='DIRECT', conflict_status='NONE', surface_claim=False,
            )
            retrieval = mod.atom_from_retrieval(target_ref='NC001:TEST2', value={'lemma':'x'}, source_ids=('TEST_SOURCE',), dialect_scope=('JUCHITAN',))
            graph = mod.EvidenceGraph((good, retrieval))
            adjudicated = mod.EvidenceAdjudicator(graph).adjudicate()
            view = safe_generator_claim_view(adjudicated, generator_view=generator_view)
            self.assertEqual(len(view), 1)
            self.assertEqual(view[0].claim.target_ref, 'NC001:TEST')
            self.assertEqual(v153.status()['runtime_version'], '0.2.15.3')
            self.assertEqual(v153.status()['near_match_to_surface'], 'PROHIBITED')
        finally:
            tmp.cleanup()


if __name__ == '__main__':
    unittest.main()
