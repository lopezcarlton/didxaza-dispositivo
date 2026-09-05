#!/usr/bin/env python3
"""Technical regressions for documented 1SG fusion analysis.

These tests verify source-constrained analysis behavior only. They do not make
any real-text analysis target a benchmark or rule source. The v0.35.6 helper is
kept independently testable under the current v0.35.8 wrapper.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNTIME = HERE.parent / "runtime" / "v0_2_15_3"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(RUNTIME))

from analyzer_v0_35_6_documented_person_fusion_analysis_adapter import (  # noqa: E402
    _orthographically_licensed_grave_final_i,
)
from analyzer_v0_35_migrated_adapter import (  # noqa: E402
    build_migrated_analyzer,
    migrated_execution_state,
)


class OrthographicProsodyLicenseTests(unittest.TestCase):
    def test_riniti_is_licensed_as_grave_final_i(self):
        licensed, detail = _orthographically_licensed_grave_final_i("riniti")
        self.assertTrue(licensed)
        self.assertEqual(
            detail["prosodic_license_status"],
            "GRAVE_LICENSED_BY_GP_SPANISH_STRESS_ORTHOGRAPHY",
        )
        self.assertGreaterEqual(detail["orthographic_vowel_nucleus_count_minimum_estimate"], 2)

    def test_monosyllable_is_blocked(self):
        licensed, detail = _orthographically_licensed_grave_final_i("bi")
        self.assertFalse(licensed)
        self.assertIn(
            "MONOSYLLABLE_OR_UNDERDETERMINED_SYLLABLE_COUNT",
            detail["blockers"],
        )

    def test_written_stress_accent_blocks_this_rule(self):
        licensed, detail = _orthographically_licensed_grave_final_i("ridí")
        self.assertFalse(licensed)
        self.assertIn("WRITTEN_STRESS_ACCENT_PRESENT", detail["blockers"])

    def test_glottal_headword_blocks_this_rule(self):
        licensed, detail = _orthographically_licensed_grave_final_i("ri'ni")
        self.assertFalse(licensed)
        self.assertIn(
            "GLOTTAL_MARK_PRESENT_PROSODIC_PATH_NOT_THIS_RULE",
            detail["blockers"],
        )


class CurrentAnalyzerDocumentedFusionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = build_migrated_analyzer()

    @classmethod
    def tearDownClass(cls):
        cls.engine.close()

    def test_execution_state_declares_v0358_and_knowledge_rule(self):
        state = migrated_execution_state()
        self.assertEqual(state["current_adapter_version"], "0.35.8")
        self.assertTrue(state["documented_person_fusion_analysis_enabled"])
        rules = state["documented_morphology_policy"]["implemented_rules"]
        self.assertEqual(len(rules), 1)
        self.assertEqual(rules[0]["knowledge_rule_id"], "HALL-0022")
        self.assertFalse(state["documented_morphology_policy"]["generation_license"])
        self.assertFalse(state["documented_morphology_policy"]["correction_authority"])

    def test_rinite_is_documented_1sg_analysis_not_exact_attestation(self):
        result = self.engine.analyze("Rinite'", item_id="TECHNICAL_RINITI_1SG")

        # Exact evidence stays exactly where earlier layers left it.
        self.assertEqual(result["matched_token_count"], 0)
        self.assertEqual(result["effective_evidence_after_biyubi_token_count"], 0)
        self.assertEqual(result["still_exactly_unresolved_token_indexes"], [0])
        self.assertTrue(result["exact_evidence_metrics_preserved_separately"])

        # Documented morphology can nevertheless analyze the observed token.
        self.assertEqual(result["documented_person_fusion_analyzed_token_indexes"], [0])
        self.assertEqual(result["unresolved_token_indexes_after_documented_morphology"], [])
        self.assertEqual(result["effective_analysis_token_count_after_documented_morphology"], 1)
        self.assertEqual(result["analysis_status"], "PARTIAL_ANALYSIS_NON_LICENSING")
        self.assertEqual(
            result["analysis_status_promotion_basis"],
            "DOCUMENTED_MORPHOLOGICAL_RULE_APPLICATION_TO_OBSERVED_SURFACE",
        )

        analyses = result["documented_person_fusion_analyses"]
        self.assertEqual(len(analyses), 1)
        analysis = analyses[0]
        self.assertEqual(analysis["person"], "1SG")
        self.assertEqual(analysis["documented_lemma_surface"].casefold(), "riniti")
        self.assertEqual(analysis["observed_surface_relation"], "FINAL_I_TO_E_GLOTTAL_1SG")
        self.assertEqual(analysis["knowledge_authority"]["record_id"], "HALL-0022")
        self.assertEqual(
            analysis["epistemic_status"],
            "SOURCE_DOCUMENTED_RULE_APPLICATION_TO_OBSERVED_SURFACE",
        )
        self.assertFalse(analysis["exact_surface_match_assertion"])
        self.assertFalse(analysis["generated_surface"])
        self.assertFalse(analysis["correction_assertion"])
        self.assertFalse(analysis["generation_license_assertion"])

    def test_other_candidates_are_not_promoted_by_this_rule(self):
        for surface in ("rucuidxiilu'", "quidxu'", "xquendasicarulu'", "binebiaya'"):
            result = self.engine.analyze(surface, item_id="TECHNICAL_NONPROMOTION_CONTROL")
            self.assertEqual(result["documented_person_fusion_analyses"], [])
            self.assertEqual(result["unresolved_token_indexes_after_documented_morphology"], [0])
            self.assertEqual(result["effective_analysis_token_count_after_documented_morphology"], 0)


if __name__ == "__main__":
    unittest.main()
