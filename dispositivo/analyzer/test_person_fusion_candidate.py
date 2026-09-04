#!/usr/bin/env python3
"""Technical regressions for Analyzer v0.35.5 person-fusion candidates.

The tests assert only a documented morphological RELATION candidate. They do
not promote the observed token to exact evidence, do not assert orthographic
correctness, and do not authorize generation.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNTIME = HERE.parent / "runtime" / "v0_2_15_3"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(RUNTIME))

from analyzer_v0_35_migrated_adapter import build_migrated_analyzer  # noqa: E402


class PersonFusionCandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = build_migrated_analyzer()

    @classmethod
    def tearDownClass(cls):
        cls.engine.close()

    def test_rinite_links_to_documented_riniti_without_changing_exact_state(self):
        result = self.engine.analyze("Rinite'", item_id="TECHNICAL_GP_1SG_RINITI")
        rows = result["supplemental_documented_person_fusion_candidates"]

        self.assertEqual(result["current_adapter_version"], "0.35.5")
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row["token_raw"], "Rinite'")
        self.assertEqual(row["candidate_status"], "DOCUMENTED_LEXEME_PLUS_GP_1SG_FUSION_CANDIDATE")
        self.assertEqual(row["person_candidate"], "1SG")
        self.assertEqual(row["reconstructed_habitual_headword_key"], "riniti")
        self.assertEqual(row["documented_entry_id"], "niti")
        self.assertEqual(row["documented_headword_raw"], "riniti")
        self.assertIn("Perderse", row["documented_definition_es"])
        self.assertEqual(row["rule_id"], "JLC-PERS-002")
        self.assertEqual(row["rule_source_location"], "Cuadro 17")
        self.assertEqual(row["prosodic_class_status"], "NOT_ENCODED_REQUIRES_CONFIRMATION")
        self.assertFalse(row["exact_surface_match_assertion"])
        self.assertFalse(row["full_person_resolution_assertion"])
        self.assertFalse(row["correction_assertion"])

        self.assertEqual(result["matched_token_count"], 0)
        self.assertEqual(result["effective_evidence_after_biyubi_token_count"], 0)
        self.assertEqual(result["still_exactly_unresolved_token_indexes"], [0])
        self.assertEqual(result["documented_person_fusion_candidate_token_indexes"], [0])
        self.assertTrue(result["exact_evidence_state_unchanged_by_person_fusion_candidates"])
        self.assertEqual(result["analysis_status"], "ABSTAIN_NO_COMPONENT_EVIDENCE")

    def test_missing_glottal_does_not_trigger_i_to_e1sg_candidate(self):
        result = self.engine.analyze("Rinite", item_id="TECHNICAL_GP_1SG_NEGATIVE_NO_GLOTTAL")
        self.assertEqual(result["supplemental_documented_person_fusion_candidates"], [])

    def test_unrelated_unresolved_tokens_do_not_receive_person_fusion_link(self):
        for surface in ("quidxu'", "rucuidxiilu'", "guendaranaxhii"):
            result = self.engine.analyze(surface, item_id="TECHNICAL_GP_1SG_NEGATIVE")
            self.assertEqual(result["supplemental_documented_person_fusion_candidates"], [])
            self.assertIn(0, result["still_exactly_unresolved_token_indexes"])

    def test_candidate_layer_preserves_non_authority_flags(self):
        result = self.engine.analyze("Rinite'", item_id="TECHNICAL_GP_1SG_POLICY")
        self.assertFalse(result["generation_license_assertion"])
        self.assertFalse(result["correction_assertion"])
        self.assertFalse(result["orthographic_authority_assertion"])
        self.assertFalse(result["rule_discovery_assertion"])
        policy = result["fallback_policy"]
        self.assertTrue(policy["person_fusion_candidate_requires_documented_habitual_headword"])
        self.assertTrue(policy["person_fusion_candidate_requires_prosodic_confirmation_for_resolution"])
        self.assertFalse(policy["person_fusion_candidate_generic_edit_distance"])
        self.assertFalse(policy["person_fusion_candidate_tone_stripping"])
        self.assertFalse(policy["person_fusion_candidate_pdlma_to_surface"])


if __name__ == "__main__":
    unittest.main()
