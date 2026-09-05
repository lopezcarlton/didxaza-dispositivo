#!/usr/bin/env python3
"""Independent technical tests for VerbAnalysisBridge v0.1.

The fixtures come from the already-materialized 2,385-record verb inventory or
from synthetic negative strings. No NEW_WRITTEN_ANALYSIS_TARGET is used as a
benchmark, regression source, or rule-discovery source. These v0.1 invariants
remain independently testable under later wrappers.
"""

from __future__ import annotations

import unittest

from analyzer_v0_35_9_verb_analysis_bridge import (
    STATUS_NONE,
    STATUS_PUNCT,
    STATUS_RAW,
    _split_documented_headword_variants,
)
from analyzer_v0_35_migrated_adapter import build_migrated_analyzer, migrated_execution_state


class VerbAnalysisBridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = build_migrated_analyzer()

    @classmethod
    def tearDownClass(cls):
        cls.engine.close()

    def test_execution_state_exposes_v01_invariants_under_latest_wrapper(self):
        state = migrated_execution_state()
        self.assertEqual(state["current_adapter_version"], "0.35.15")
        self.assertTrue(state["verb_analysis_bridge_enabled"])
        self.assertEqual(state["verb_analysis_bridge_version"], "0.2")
        self.assertTrue(state["valency_compatibility_bridge_enabled"])
        self.assertTrue(state["explicit_valency_relation_bridge_enabled"])
        self.assertTrue(state["verb_morphological_hypothesis_view_enabled"])
        self.assertTrue(state["causative_group_coordinate_view_enabled"])
        self.assertTrue(state["contextual_documentary_support_view_enabled"])
        policy = state["verb_analysis_bridge_policy"]
        self.assertTrue(policy["exposes_documented_class"])
        self.assertTrue(policy["exposes_documented_pdlma_paradigm_fields"])
        self.assertFalse(policy["tone_stripping"])
        self.assertFalse(policy["pdlma_to_ap"])
        self.assertFalse(policy["nonheadword_tam_inference"])
        self.assertFalse(policy["valency_analysis_in_v02"])
        self.assertFalse(policy["generation_license"])
        self.assertFalse(policy["correction_authority"])
        self.assertFalse(state["valency_compatibility_policy"]["surface_prefix_inference"])
        self.assertFalse(state["valency_compatibility_policy"]["pb2015_group_assignment"])
        self.assertFalse(state["explicit_valency_relation_policy"]["surface_relation_inference"])
        self.assertFalse(state["causative_group_coordinate_policy"]["visible_prefix_detection"])
        self.assertFalse(state["contextual_documentary_support_policy"]["resolves_hypothesis"])

    def test_known_class_a_headword_exposes_record_and_paradigm(self):
        result = self.engine.analyze("ra", item_id="TECHNICAL_VERB_BRIDGE_A")
        self.assertEqual(result["current_adapter_version"], "0.35.15")
        self.assertIn(0, result["documented_exact_verb_token_indexes"])
        row = result["documented_exact_verb_analyses"][0]
        self.assertEqual(row["verb_headword_status"], STATUS_RAW)
        matches = [record for record in row["documented_records"] if record["entry_id"] == "a"]
        self.assertEqual(len(matches), 1)
        record = matches[0]
        self.assertEqual(record["verb_class"], "A")
        self.assertEqual(record["headword_channel"], "JZ_AP_DOCUMENTED_HEADWORD")
        self.assertTrue(record["documented_paradigm"]["HABITUAL"]["available"])
        self.assertTrue(record["documented_paradigm"]["COMPLETIVE"]["available"])
        self.assertFalse(record["documented_paradigm"]["COMPLETIVE"]["ap_surface_projection_assertion"])
        self.assertEqual(
            record["provenance"]["documentary_record_source"],
            "SRC-DICTIONARIA-DIDXAZA-SPANISH-ENGLISH-DICTIONARY",
        )
        self.assertFalse(record["generation_license_assertion"])
        self.assertFalse(record["correction_assertion"])
        self.assertFalse(result["valency_compatibility_changes_analysis_status"])
        self.assertFalse(result["explicit_valency_relation_changes_analysis_status"])
        self.assertFalse(result["verb_morphological_hypothesis_changes_analysis_status"])
        self.assertFalse(result["causative_group_coordinate_changes_analysis_status"])
        self.assertFalse(result["contextual_documentary_support_changes_analysis_status"])

    def test_homographic_headword_preserves_multiple_records(self):
        result = self.engine.analyze("ra'sa'", item_id="TECHNICAL_VERB_BRIDGE_HOMOGRAPH")
        row = result["documented_exact_verb_analyses"][0]
        entry_ids = {record["entry_id"] for record in row["documented_records"]}
        self.assertIn("a7sa1", entry_ids)
        self.assertIn("a7sa2", entry_ids)
        self.assertGreaterEqual(row["documented_record_count"], 2)
        self.assertTrue(row["ambiguity_preserved"])

    def test_sentence_capitalization_and_outer_punctuation_are_labelled_not_rewritten(self):
        result = self.engine.analyze("Ra,", item_id="TECHNICAL_VERB_BRIDGE_PUNCT")
        row = result["documented_exact_verb_analyses"][0]
        self.assertEqual(row["token_raw"], "Ra,")
        self.assertEqual(row["comparison_surface"], "Ra")
        self.assertEqual(row["verb_headword_status"], STATUS_PUNCT)
        self.assertFalse(row["comparison_policy"]["apostrophe_normalization"])
        self.assertFalse(row["comparison_policy"]["tone_stripping"])

    def test_synthetic_unknown_is_not_claimed_as_verb(self):
        result = self.engine.analyze(
            "ZZZ_SYNTHETIC_NONVERB_92841",
            item_id="TECHNICAL_VERB_BRIDGE_NEGATIVE",
        )
        self.assertEqual(result["documented_exact_verb_token_indexes"], [])
        row = result["verb_headword_observations"][0]
        self.assertEqual(row["verb_headword_status"], STATUS_NONE)
        self.assertFalse(row["verb_category_documented"])
        self.assertEqual(row["documented_records"], [])
        self.assertEqual(result["valency_compatibility_informative_token_indexes"], [])
        self.assertEqual(result["explicit_valency_relation_informative_token_indexes"], [])
        self.assertEqual(result["verb_morphological_hypothesis_informative_token_indexes"], [])
        self.assertEqual(result["causative_group_coordinate_informative_token_indexes"], [])
        self.assertEqual(result["contextual_documentary_support_informative_token_indexes"], [])

    def test_twenty_record_panel_covers_classes_a_b_c_d(self):
        """Five pre-existing records per PBK class, selected independently of target text."""
        selected = {"A": [], "B": [], "C": [], "D": []}
        for record in self.engine.morph1.records.values():
            if record.verb_class not in selected or len(selected[record.verb_class]) >= 5:
                continue
            variants = [
                v for v in _split_documented_headword_variants(record.headword_raw)
                if v and not any(ch.isspace() for ch in v)
            ]
            if variants:
                selected[record.verb_class].append((record.entry_id, variants[0]))
            if all(len(rows) >= 5 for rows in selected.values()):
                break

        self.assertEqual({cls: len(rows) for cls, rows in selected.items()}, {"A": 5, "B": 5, "C": 5, "D": 5})

        checked = 0
        for expected_class, rows in selected.items():
            for entry_id, surface in rows:
                result = self.engine.analyze(surface, item_id=f"TECHNICAL_PANEL_{expected_class}_{entry_id}")
                matching_records = [
                    record
                    for observation in result["documented_exact_verb_analyses"]
                    for record in observation["documented_records"]
                    if record["entry_id"] == entry_id
                ]
                self.assertTrue(matching_records, (expected_class, entry_id, surface))
                self.assertEqual(matching_records[0]["verb_class"], expected_class)
                self.assertFalse(matching_records[0]["pdlma_to_ap_assertion"])
                self.assertFalse(result["valency_compatibility_changes_exact_evidence_metrics"])
                self.assertFalse(result["explicit_valency_relation_changes_exact_evidence_metrics"])
                self.assertFalse(result["verb_morphological_hypothesis_changes_exact_evidence_metrics"])
                self.assertFalse(result["causative_group_coordinate_changes_exact_evidence_metrics"])
                self.assertFalse(result["contextual_documentary_support_changes_exact_evidence_metrics"])
                checked += 1
        self.assertEqual(checked, 20)


if __name__ == "__main__":
    unittest.main()
