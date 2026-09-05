#!/usr/bin/env python3
"""Technical regression tests for current exact existing-layer fallback.

These tests assert retrieval behavior over already materialized runtime evidence.
They do not assert linguistic correctness, orthographic correctness, translation,
or rule discovery. Biyubi is registered but intentionally unmounted in this
public-repository regression suite. Candidate-only or documented-morphology
observations must not alter any exact-evidence assertion below.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNTIME = HERE.parent / "runtime" / "v0_2_15_3"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(RUNTIME))

from analyzer_v0_35_migrated_adapter import (  # noqa: E402
    build_migrated_analyzer,
    migrated_execution_state,
)


class ExactExistingLayerFallbackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = build_migrated_analyzer()

    @classmethod
    def tearDownClass(cls):
        cls.engine.close()

    def _single_fallback(self, surface: str):
        result = self.engine.analyze(surface, item_id="TECHNICAL_FALLBACK_REGRESSION")
        rows = result["supplemental_exact_existing_layer_evidence"]
        self.assertEqual(len(rows), 1)
        return result, rows[0]

    def test_execution_state_declares_current_fallback(self):
        state = migrated_execution_state()
        self.assertEqual(state["current_adapter_version"], "0.35.10")
        self.assertTrue(state["exact_existing_layer_fallback_enabled"])
        self.assertTrue(state["punctuation_light_fallback_lookup_enabled"])
        self.assertTrue(state["voces_documentary_exact_layer_enabled"])
        self.assertTrue(state["documentary_candidate_layer_enabled"])
        self.assertTrue(state["documented_person_fusion_candidate_layer_enabled"])
        self.assertTrue(state["documented_person_fusion_analysis_enabled"])
        self.assertTrue(state["verb_analysis_bridge_enabled"])
        self.assertTrue(state["documentary_verb_form_candidate_layer_enabled"])
        self.assertFalse(state["candidate_layer_policy"]["candidate_is_exact_evidence"])
        self.assertFalse(state["candidate_layer_policy"]["candidate_promotes_analysis_status"])
        self.assertTrue(state["documented_morphology_policy"]["exact_surface_evidence_kept_separate"])
        self.assertFalse(state["documented_morphology_policy"]["generation_license"])
        self.assertFalse(state["documented_morphology_policy"]["correction_authority"])
        self.assertEqual(
            set(state["fallback_layers"]),
            {
                "surface_attestation_v029",
                "pickett_lexical_record_v0211",
                "cross_source_exact_surface_v0212",
                "documentary_alignment_v0210",
                "voces_promoted_documentary_exact_v0357",
            },
        )
        self.assertEqual(len(state["controlled_external_sources"]), 1)
        biyubi = state["controlled_external_sources"][0]
        self.assertEqual(
            biyubi["source_id"],
            "SRC-BIYUBI-DICCIONARIO-DIDXAZA-ESPANOL",
        )
        self.assertEqual(biyubi["registered_data_rows"], 23601)
        self.assertEqual(biyubi["mount_status"], "NOT_MOUNTED")
        self.assertFalse(biyubi["payload_in_public_repository"])
        self.assertFalse(biyubi["orthographic_authority"])
        self.assertFalse(state["cor001_benchmark_allowed"])
        self.assertFalse(state["research_authority_assertion"])

    def test_siou_is_attested_outside_primary_lexicon(self):
        result, row = self._single_fallback("siou’")
        self.assertEqual(row["fallback_status"], "ATTESTED_OUTSIDE_PRIMARY_LEXICON")
        self.assertEqual(row["evidence_counts"]["surface_attestation_v029"], 1)
        self.assertEqual(row["evidence_counts"]["pickett_lexical_record_v0211"], 0)
        self.assertIn("BIB054_DICTIONARIA", row["source_ids"])
        self.assertEqual(result["primary_analysis_status"], "ABSTAIN_NO_COMPONENT_EVIDENCE")
        self.assertEqual(result["analysis_status"], "PARTIAL_ANALYSIS_NON_LICENSING")
        self.assertEqual(result["matched_token_count"], 0)
        self.assertEqual(result["effective_evidence_token_count"], 1)
        self.assertEqual(result["biyubi_source_status"], "NOT_MOUNTED")

    def test_naxi_is_attested_in_pickett_and_dictionaria_examples(self):
        result, row = self._single_fallback("naxí")
        self.assertEqual(row["fallback_status"], "ATTESTED_OUTSIDE_PRIMARY_LEXICON")
        self.assertEqual(row["evidence_counts"]["pickett_lexical_record_v0211"], 1)
        self.assertEqual(row["evidence_counts"]["surface_attestation_v029"], 2)
        self.assertIn("BIB003_PICKETT_VOCABULARIO", row["source_ids"])
        self.assertIn("BIB054_DICTIONARIA", row["source_ids"])
        self.assertEqual(result["matched_token_count"], 0)
        self.assertEqual(result["effective_evidence_token_count"], 1)

    def test_dxandi_is_attested_in_pickett_and_dictionaria_example(self):
        result, row = self._single_fallback("dxandí’")
        self.assertEqual(row["fallback_status"], "ATTESTED_OUTSIDE_PRIMARY_LEXICON")
        self.assertEqual(row["evidence_counts"]["pickett_lexical_record_v0211"], 1)
        self.assertEqual(row["evidence_counts"]["surface_attestation_v029"], 1)
        self.assertIn("BIB003_PICKETT_VOCABULARIO", row["source_ids"])
        self.assertIn("BIB054_DICTIONARIA", row["source_ids"])
        self.assertEqual(result["matched_token_count"], 0)
        self.assertEqual(result["effective_evidence_token_count"], 1)

    def test_guyu_remains_unresolved_not_incorrect(self):
        result, row = self._single_fallback("gu’yu’")
        self.assertEqual(
            row["fallback_status"],
            "UNRESOLVED_NO_EXACT_EXISTING_LAYER_EVIDENCE",
        )
        self.assertEqual(sum(row["evidence_counts"].values()), 0)
        self.assertEqual(result["primary_analysis_status"], "ABSTAIN_NO_COMPONENT_EVIDENCE")
        self.assertEqual(result["analysis_status"], "ABSTAIN_NO_COMPONENT_EVIDENCE")
        self.assertEqual(result["effective_evidence_token_count"], 0)
        self.assertEqual(result["unresolved_token_indexes_after_exact_fallback"], [0])
        self.assertEqual(result["unresolved_token_indexes_after_biyubi"], [0])
        self.assertEqual(result["unresolved_token_indexes_after_voces_documentary_exact"], [0])
        self.assertEqual(result["still_exactly_unresolved_token_indexes"], [0])
        self.assertEqual(result["unresolved_token_indexes_after_documented_morphology"], [0])
        self.assertEqual(result["unresolved_token_indexes_after_documentary_verb_form_candidates"], [0])
        self.assertTrue(result["fallback_policy"]["unresolved_not_incorrect"])
        self.assertTrue(result["fallback_policy"]["biyubi_absence_not_incorrect"])
        self.assertTrue(result["exact_evidence_state_unchanged_by_candidates"])
        self.assertTrue(result["exact_evidence_state_unchanged_by_person_fusion_candidates"])
        self.assertTrue(result["exact_evidence_metrics_preserved_separately"])

    def test_real_text_lines_gain_effective_coverage_without_inflating_primary_matches(self):
        line2 = self.engine.analyze(
            "Nuu xquie naxhi ne nuu naxí",
            item_id="TECHNICAL_REAL_TEXT_L02",
        )
        self.assertEqual(line2["matched_token_count"], 5)
        self.assertEqual(line2["effective_evidence_token_count"], 6)
        self.assertEqual(line2["unresolved_token_indexes_after_exact_fallback"], [])

        line3 = self.engine.analyze(
            "Tecu dxandí’ ni riní’",
            item_id="TECHNICAL_REAL_TEXT_L03",
        )
        self.assertEqual(line3["matched_token_count"], 3)
        self.assertEqual(line3["effective_evidence_token_count"], 4)
        self.assertEqual(line3["unresolved_token_indexes_after_exact_fallback"], [])

        line1 = self.engine.analyze(
            "Biaa gu’yu’ siou’",
            item_id="TECHNICAL_REAL_TEXT_L01",
        )
        self.assertEqual(line1["matched_token_count"], 1)
        self.assertEqual(line1["effective_evidence_token_count"], 2)
        self.assertEqual(line1["unresolved_token_indexes_after_exact_fallback"], [1])

        for result in (line1, line2, line3):
            self.assertEqual(result["current_adapter_version"], "0.35.10")
            self.assertTrue(result["fallback_policy"]["matched_token_count_not_inflated_by_fallback"])
            self.assertTrue(result["fallback_policy"]["candidate_layer_does_not_increase_effective_evidence_coverage"])
            self.assertTrue(result["fallback_policy"]["person_fusion_candidate_does_not_increase_effective_evidence_coverage"])
            self.assertTrue(result["exact_evidence_state_unchanged_by_candidates"])
            self.assertTrue(result["exact_evidence_state_unchanged_by_person_fusion_candidates"])
            self.assertTrue(result["exact_evidence_metrics_preserved_separately"])
            self.assertFalse(result["documentary_verb_form_candidates_change_exact_evidence_metrics"])
            self.assertFalse(result["documentary_verb_form_candidates_change_analysis_status"])
            self.assertFalse(result["generation_license_assertion"])
            self.assertFalse(result["correction_assertion"])
            self.assertFalse(result["orthographic_authority_assertion"])
            self.assertFalse(result["rule_discovery_assertion"])

    def test_punctuation_light_lookup_recovers_probe_002_attestations(self):
        expected_sources = {
            "sicarú,": {"BIB003_PICKETT_VOCABULARIO", "BIB054_DICTIONARIA"},
            "beeu,": {"BIB003_PICKETT_VOCABULARIO", "BIB054_DICTIONARIA"},
            "Ibá',": {"BIB003_PICKETT_VOCABULARIO"},
            "Ibá'.": {"BIB003_PICKETT_VOCABULARIO"},
        }
        for surface, sources in expected_sources.items():
            result, row = self._single_fallback(surface)
            self.assertEqual(row["fallback_status"], "ATTESTED_OUTSIDE_PRIMARY_LEXICON")
            self.assertEqual(set(row["source_ids"]), sources)
            self.assertEqual(row["lookup_normalization"], "PUNCTUATION_LIGHT_INDEX")
            self.assertNotEqual(row["token_raw"], row["punctuation_light_lookup_key"])
            self.assertEqual(result["effective_evidence_token_count"], 1)
            self.assertTrue(result["fallback_policy"]["punctuation_light_lookup_enabled"])
            self.assertTrue(
                result["fallback_policy"]["punctuation_is_comparison_only_not_input_rewrite"]
            )
            self.assertEqual(result["surface_original"], surface)

    def test_punctuation_light_does_not_create_evidence_for_unresolved_token(self):
        result, row = self._single_fallback("guendaranaxhii,")
        self.assertEqual(
            row["fallback_status"],
            "UNRESOLVED_NO_EXACT_EXISTING_LAYER_EVIDENCE",
        )
        self.assertEqual(row["punctuation_light_lookup_key"], "guendaranaxhii")
        self.assertEqual(sum(row["evidence_counts"].values()), 0)
        self.assertEqual(result["surface_original"], "guendaranaxhii,")
        self.assertEqual(result["unresolved_token_indexes_after_exact_fallback"], [0])
        self.assertEqual(result["unresolved_token_indexes_after_biyubi"], [0])
        self.assertEqual(result["unresolved_token_indexes_after_voces_documentary_exact"], [0])
        self.assertEqual(result["still_exactly_unresolved_token_indexes"], [0])
        self.assertEqual(result["unresolved_token_indexes_after_documented_morphology"], [0])
        self.assertEqual(result["unresolved_token_indexes_after_documentary_verb_form_candidates"], [0])
        self.assertTrue(result["exact_evidence_state_unchanged_by_candidates"])
        self.assertTrue(result["exact_evidence_state_unchanged_by_person_fusion_candidates"])
        self.assertTrue(result["exact_evidence_metrics_preserved_separately"])


if __name__ == "__main__":
    unittest.main()
