#!/usr/bin/env python3
"""Technical regression tests for Analyzer v0.35.1 exact fallback.

These tests assert retrieval behavior over already materialized runtime evidence.
They do not assert linguistic correctness, orthographic correctness, translation,
or rule discovery.
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
        self.assertEqual(state["current_adapter_version"], "0.35.1")
        self.assertTrue(state["exact_existing_layer_fallback_enabled"])
        self.assertEqual(
            set(state["fallback_layers"]),
            {
                "surface_attestation_v029",
                "pickett_lexical_record_v0211",
                "cross_source_exact_surface_v0212",
                "documentary_alignment_v0210",
            },
        )
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
        self.assertTrue(result["fallback_policy"]["unresolved_not_incorrect"])

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
            self.assertTrue(result["fallback_policy"]["matched_token_count_not_inflated_by_fallback"])
            self.assertFalse(result["generation_license_assertion"])
            self.assertFalse(result["correction_assertion"])
            self.assertFalse(result["orthographic_authority_assertion"])
            self.assertFalse(result["rule_discovery_assertion"])


if __name__ == "__main__":
    unittest.main()
