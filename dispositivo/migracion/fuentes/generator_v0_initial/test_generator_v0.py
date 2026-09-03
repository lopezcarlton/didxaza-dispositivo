#!/usr/bin/env python3
from __future__ import annotations

import inspect
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "generator_v0"))

from generator_v0 import LicensedGeneratorV0, GenerationRequest
from mvp_review_candidate_adapter_v0 import adapt_v01_review_candidate, v02_state_is_generation_license


class TestGeneratorV0(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.eng = LicensedGeneratorV0()

    def test_c01_exact_attested_assembly(self):
        r = self.eng.generate(GenerationRequest("C01", "NC001-V01", "COMPLETIVE", "1SG", {"TEMPORAL_CONTEXT":"ALREADY"}))
        self.assertEqual(r.status, "LICENSED_GENERATION")
        self.assertEqual(r.surface, "Ma' benda'")
        self.assertEqual(r.evidence_ids, ("EVID-GP-EEDA-C-1SG-001",))
        self.assertEqual(r.novelty, "ZERO_NOVELTY_ATTESTED_ASSEMBLY")

    def test_c02_exact_attested_assembly(self):
        r = self.eng.generate(GenerationRequest("C02", "NC001-V01", "HABITUAL", "3SG_HUMAN", {"NEG_PATTERN":"QUE_PRED_GUIRA_DXI"}))
        self.assertEqual(r.status, "LICENSED_GENERATION")
        self.assertEqual(r.surface, "Qué reedabe guirá' dxi")

    def test_no_paradigm_completion(self):
        r = self.eng.generate(GenerationRequest("C01", "NC001-V01", "COMPLETIVE", "2SG", {"TEMPORAL_CONTEXT":"ALREADY"}))
        self.assertEqual((r.status, r.reason), ("ABSTAIN", "MISSING_CELL"))

    def test_attested_cell_does_not_self_license_combination(self):
        r = self.eng.generate(GenerationRequest("C01", "NC001-V01", "COMPLETIVE", "3SG_HUMAN", {"TEMPORAL_CONTEXT":"ALREADY"}))
        self.assertEqual((r.status, r.reason), ("ABSTAIN", "NO_EXACT_GENERATION_LICENSE"))

    def test_blocked_constructions(self):
        cases = [
            (GenerationRequest("C03", "NC001-V01", "COMPLETIVE", "1SG", {}), "MISSING_QUESTION_PATTERN"),
            (GenerationRequest("C04", "NC001-V01", "COMPLETIVE", "3SG_HUMAN", {"INTERROGATIVE":"WHEN"}), "INTERROGATIVE_DOMAIN_SCOPE_MISMATCH"),
            (GenerationRequest("C05", "NC001-V01", "HABITUAL", "1SG", {}), "MISSING_NOUN_POSSESSION_LICENSE_SET"),
            (GenerationRequest("C06", "NC001-V05", "HABITUAL", "1SG", {}), "DEPENDENT_POTENTIAL_OUT_OF_SCOPE"),
        ]
        for req, reason in cases:
            with self.subTest(req=req):
                r = self.eng.generate(req)
                self.assertEqual((r.status, r.reason), ("ABSTAIN", reason))

    def test_scope_and_tam_guards(self):
        r = self.eng.generate(GenerationRequest("C01", "NC001-V01", "POTENTIAL", "1SG", {"TEMPORAL_CONTEXT":"ALREADY"}))
        self.assertEqual(r.reason, "TAM_OUT_OF_SCOPE")
        r = self.eng.generate(GenerationRequest("C01", "NC001-V01", "COMPLETIVE", "1SG", {"TEMPORAL_CONTEXT":"ALREADY"}, target_scope="UNKNOWN"))
        self.assertEqual(r.reason, "TARGET_SCOPE_UNLICENSED")

    def test_round_trip_license_features(self):
        req = GenerationRequest("C01", "NC001-V01", "COMPLETIVE", "1SG", {"TEMPORAL_CONTEXT":"ALREADY"})
        r = self.eng.generate(req)
        back = self.eng.analyze_licensed_surface(r.surface)
        self.assertEqual(len(back), 1)
        self.assertEqual(back[0]["tam"], req.tam)
        self.assertEqual(back[0]["person"], req.person)
        self.assertEqual(back[0]["construction_id"], req.construction_id)

    def test_generator_source_has_no_legacy_similarity_path(self):
        import generator_v0 as gv
        src = inspect.getsource(gv)
        for forbidden in ["SequenceMatcher", "COR001", "surface_similarity", "clean_paradigm_surface", "unicodedata.normalize"]:
            self.assertNotIn(forbidden, src)

    def test_mvp_review_candidate_reused_as_non_licensing(self):
        legacy = {
            "observed":"cha hui", "proposed":"chaahui'", "span_start_token":4, "span_end_token":6,
            "candidate_type":"MERGE_SURFACE_REVIEW", "status":"REVIEW_CANDIDATE", "semantic_anchor":"despacio",
            "surface_similarity":0.91, "confidence":"HIGH_REVIEW", "rationale":"legacy", "evidence":[],
            "blockers":["REQUIRES_NATIVE_OR_PRIMARY_TEXT_VALIDATION"]
        }
        x = adapt_v01_review_candidate(legacy)
        self.assertEqual(x.status, "REVIEW_CANDIDATE")
        self.assertFalse(x.may_license_generation)
        self.assertFalse(x.may_auto_correct)
        self.assertFalse(hasattr(x, "confidence"))
        self.assertFalse(hasattr(x, "surface_similarity"))

    def test_v02_review_states_never_auto_license_generator(self):
        for state in ["REVIEW_CANDIDATE", "OWNER_SUPPORTED_REVIEW_CANDIDATE", "PROBABLE_TRANSCRIPTION_CORRECTION", "COMPETING_SEGMENTATION_HYPOTHESES", "NATIVE_SPEAKER_VALIDATED"]:
            self.assertFalse(v02_state_is_generation_license(state))


if __name__ == "__main__":
    unittest.main()
