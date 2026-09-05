#!/usr/bin/env python3
"""Independent regressions for VerbAnalysisBridge v0.2.

No NEW_WRITTEN_ANALYSIS_TARGET is used as benchmark, regression source or rule
source. Positive fixtures are discovered from the already-versioned Dictionaria
examples and 2,385-record verb inventory; negatives are synthetic.
"""

from __future__ import annotations

import unittest

from analyzer_v0_35_10_documentary_verb_form_candidates import (
    CANDIDATE_STATUS,
    COMPARISON_OPERATION,
    pdlma_hyphen_collapse_candidate_key,
    strict_documentary_key,
)
from analyzer_v0_35_migrated_adapter import build_migrated_analyzer, migrated_execution_state


class DocumentaryVerbFormCandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = build_migrated_analyzer()

    @classmethod
    def tearDownClass(cls):
        cls.engine.close()

    def test_execution_state_declares_candidate_only_v02(self):
        state = migrated_execution_state()
        self.assertEqual(state["current_adapter_version"], "0.35.10")
        self.assertEqual(state["verb_analysis_bridge_version"], "0.2")
        self.assertTrue(state["documentary_verb_form_candidate_layer_enabled"])
        stats = state["documentary_verb_form_candidate_index_stats"]
        self.assertGreater(stats["verb_sense_links"], 0)
        self.assertGreater(stats["single_verb_linked_examples"], 0)
        self.assertGreater(stats["examples_with_literal_hyphen_collapse_match"], 0)
        self.assertGreater(stats["candidate_relations"], 0)
        self.assertGreater(stats["indexed_token_keys"], 0)
        self.assertEqual(stats["comparison_operation"], COMPARISON_OPERATION)
        policy = state["verb_analysis_bridge_policy"]
        self.assertTrue(policy["documentary_nonheadword_form_candidates"])
        self.assertTrue(policy["candidate_requires_exact_ap_example_token"])
        self.assertTrue(policy["candidate_requires_unique_linked_verb_entry"])
        self.assertTrue(policy["candidate_requires_literal_pdlma_match_after_ascii_hyphen_removal_only"])
        self.assertFalse(policy["candidate_token_role_asserted"])
        self.assertFalse(policy["candidate_tam_of_observed_surface_asserted"])
        self.assertFalse(policy["candidate_promotes_analysis_status"])
        self.assertFalse(policy["pdlma_to_ap"])
        self.assertFalse(policy["generation_license"])
        self.assertFalse(policy["correction_authority"])

    def test_documentary_key_preserves_tone_and_only_unifies_apostrophe_typography(self):
        self.assertNotEqual(strict_documentary_key("xí"), strict_documentary_key("xi"))
        self.assertEqual(strict_documentary_key("gu’yu’"), strict_documentary_key("gu'yu'"))
        self.assertNotEqual(strict_documentary_key("gu'yu'"), strict_documentary_key("guyu"))

    def test_pdlma_candidate_comparison_removes_only_ascii_hyphen(self):
        target = strict_documentary_key("gundani")
        self.assertEqual(pdlma_hyphen_collapse_candidate_key("gu-ndani"), target)
        self.assertNotEqual(pdlma_hyphen_collapse_candidate_key("gu.ndani"), target)
        self.assertNotEqual(pdlma_hyphen_collapse_candidate_key("gu-nda!ni"), target)
        self.assertNotEqual(pdlma_hyphen_collapse_candidate_key("gu-nda7ni"), target)
        self.assertNotEqual(pdlma_hyphen_collapse_candidate_key("gú-ndani"), target)

    def test_indexed_candidate_exposes_only_analytical_coordinates(self):
        candidate = None
        for rows in self.engine._example_token_index.values():
            if not rows:
                continue
            token = rows[0]["token_surface_in_example"]
            candidate = self.engine._candidate_payload(token, 0)
            if candidate:
                break
        self.assertIsNotNone(candidate)
        self.assertEqual(candidate["candidate_status"], CANDIDATE_STATUS)
        self.assertTrue(candidate["underlying_exact_documentary_token_attestation"])
        self.assertFalse(candidate["candidate_adds_exact_surface_evidence"])
        self.assertFalse(candidate["candidate_promotes_analysis_status"])
        self.assertFalse(candidate["candidate_resolves_token"])
        self.assertGreater(candidate["compatible_verb_entry_count"], 0)
        entry = candidate["compatible_verb_entries"][0]
        self.assertTrue(entry["tam_candidates"])
        self.assertTrue(entry["root_analysis_raw"])
        self.assertTrue(entry["matching_documented_pdlma_variants"])
        self.assertEqual(entry["comparison_policy"]["operation"], COMPARISON_OPERATION)
        self.assertTrue(entry["comparison_policy"]["ascii_hyphen_removed"])
        self.assertFalse(entry["comparison_policy"]["tone_stripping"])
        self.assertFalse(entry["comparison_policy"]["diacritic_stripping"])
        self.assertFalse(entry["comparison_policy"]["glottal_7_to_apostrophe"])
        self.assertFalse(entry["comparison_policy"]["bang_removal"])
        self.assertFalse(entry["comparison_policy"]["dot_removal"])
        self.assertFalse(entry["comparison_policy"]["segment_substitution"])
        self.assertFalse(entry["observed_token_is_verb_assertion"])
        self.assertFalse(entry["tam_of_observed_surface_assertion"])
        self.assertFalse(entry["root_segmentation_of_observed_token_assertion"])
        self.assertFalse(entry["pdlma_to_ap_assertion"])
        self.assertFalse(entry["generation_license_assertion"])
        self.assertFalse(entry["correction_assertion"])

    def test_real_snapshot_has_nonheadword_candidate_without_promoting_analysis(self):
        chosen = None
        base_result = None
        # Find a documentary candidate independently of the blind target that is
        # not already recognized by v0.1 as an exact verb headword and is not the
        # separately promoted 1SG person-fusion case.
        for rows in self.engine._example_token_index.values():
            if not rows:
                continue
            token = rows[0]["token_surface_in_example"]
            candidate_base = self.engine.base.analyze(
                token, item_id="TECHNICAL_V02_DISCOVERY"
            )
            if candidate_base.get("documented_exact_verb_token_indexes"):
                continue
            if candidate_base.get("documented_person_fusion_analyzed_token_indexes"):
                continue
            chosen = token
            base_result = candidate_base
            break

        self.assertIsNotNone(chosen, "No non-headword structural candidate found in documentary snapshot")
        self.assertIsNotNone(base_result)
        result = self.engine.analyze(chosen, item_id="TECHNICAL_V02_INTEGRATION")
        self.assertEqual(result["current_adapter_version"], "0.35.10")
        self.assertEqual(result["documentary_verb_form_candidate_token_indexes"], [0])
        self.assertTrue(result["documentary_verb_form_candidates"])
        candidate = result["documentary_verb_form_candidates"][0]
        self.assertFalse(candidate["candidate_resolves_token"])

        # v0.2 enriches research coordinates only. Whatever v0.1 had must remain
        # unchanged in exact coverage and promoted analysis state.
        self.assertEqual(
            result["unresolved_token_indexes_after_documentary_verb_form_candidates"],
            base_result["unresolved_token_indexes_after_documented_morphology"],
        )
        self.assertEqual(result["matched_token_count"], base_result["matched_token_count"])
        self.assertEqual(
            result["effective_evidence_token_count"],
            base_result["effective_evidence_token_count"],
        )
        self.assertEqual(result["analysis_status"], base_result["analysis_status"])
        self.assertFalse(result["documentary_verb_form_candidates_change_exact_evidence_metrics"])
        self.assertFalse(result["documentary_verb_form_candidates_change_analysis_status"])
        self.assertFalse(result["generation_license_assertion"])
        self.assertFalse(result["correction_assertion"])

    def test_synthetic_unknown_receives_no_documentary_verb_candidate(self):
        result = self.engine.analyze(
            "ZZZ_SYNTHETIC_V02_NONFORM_83741",
            item_id="TECHNICAL_V02_NEGATIVE",
        )
        self.assertEqual(result["documentary_verb_form_candidate_token_indexes"], [])
        self.assertEqual(result["documentary_verb_form_candidates"], [])


if __name__ == "__main__":
    unittest.main()
