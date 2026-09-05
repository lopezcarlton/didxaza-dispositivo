#!/usr/bin/env python3
"""Regressions for ExplicitValencyRelationBridge v0.1 under Analyzer v0.35.14.

Fixtures come only from the versioned PB2015 relation crosswalk and the existing
2,385-record Dictionaria derivative. No NEW_WRITTEN_ANALYSIS_TARGET or COR001
material is used as benchmark, regression fixture, or rule source.
"""

from __future__ import annotations

import unittest

from analyzer_v0_35_11_valency_compatibility_bridge import ROUTE_STRUCTURAL
from analyzer_v0_35_12_explicit_valency_relations import (
    COMPARISON_POLICY,
    STATUS_MULTIPLE,
    STATUS_NONE,
    STATUS_UNIQUE,
)
from analyzer_v0_35_9_verb_analysis_bridge import _split_documented_headword_variants
from analyzer_v0_35_migrated_adapter import build_migrated_analyzer, migrated_execution_state


class ExplicitValencyRelationBridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = build_migrated_analyzer()

    @classmethod
    def tearDownClass(cls):
        cls.engine.close()

    def _single_token_headword(self, entry_id: str) -> str:
        record = self.engine.morph1.records[entry_id]
        for variant in _split_documented_headword_variants(record.headword_raw):
            if variant and not any(ch.isspace() for ch in variant):
                return variant
        self.fail(f"No single-token headword for {entry_id}")

    def _entry_relation_rows(self, result, entry_id: str):
        return [
            entry
            for obs in result["explicit_valency_relation_observations"]
            for entry in obs["entries"]
            if entry["entry_id"] == entry_id
        ]

    def test_index_stats_are_exactly_the_measured_strict_crosswalk(self):
        state = migrated_execution_state()
        self.assertEqual(state["current_adapter_version"], "0.35.14")
        self.assertTrue(state["explicit_valency_relation_bridge_enabled"])
        self.assertEqual(state["explicit_valency_relation_bridge_version"], "0.1")
        self.assertTrue(state["verb_morphological_hypothesis_view_enabled"])
        self.assertTrue(state["causative_group_coordinate_view_enabled"])
        stats = state["explicit_valency_relation_index_stats"]
        self.assertEqual(stats["selected_relation_members"], 65)
        self.assertEqual(stats["selected_relation_sets"], 26)
        self.assertEqual(stats["members_with_unique_strict_match"], 26)
        self.assertEqual(stats["members_with_zero_strict_match"], 38)
        self.assertEqual(stats["members_with_multiple_strict_matches"], 1)
        self.assertEqual(stats["fully_unique_strict_relation_sets"], 6)
        self.assertEqual(stats["comparison_policy"], COMPARISON_POLICY)
        self.assertFalse(stats["pdlma_to_ap"])
        self.assertFalse(stats["automatic_group_assignment"])
        self.assertFalse(stats["surface_relation_inference"])

    def test_chuku_preserves_multiple_source_explicit_memberships(self):
        surface = self._single_token_headword("chuku")
        result = self.engine.analyze(surface, item_id="TECHNICAL_PB2015_MULTI_MEMBERSHIP")
        rows = self._entry_relation_rows(result, "chuku")
        self.assertTrue(rows)
        memberships = rows[0]["documented_memberships"]
        by_set = {
            row["relation_set_id"]: row["current_member"]["relation_role"]
            for row in memberships
        }
        self.assertEqual(by_set["PB15-C1-RUKU"], "CAUSATIVE")
        self.assertEqual(by_set["PB15-C2-CHUKU"], "BASIC")
        self.assertEqual(by_set["PB15-EXC-RUKU"], "G_DERIVED_STEM")
        self.assertGreaterEqual(len(memberships), 3)
        self.assertFalse(rows[0]["relation_asserted_from_surface_morphology"])
        self.assertFalse(rows[0]["pdlma_to_ap_assertion"])
        self.assertFalse(result["verb_morphological_hypothesis_changes_analysis_status"])
        self.assertFalse(result["causative_group_coordinate_changes_analysis_status"])

    def test_fully_resolved_set_exposes_both_documented_members(self):
        surface = self._single_token_headword("ruku")
        result = self.engine.analyze(surface, item_id="TECHNICAL_PB2015_COMPLETE_SET")
        rows = self._entry_relation_rows(result, "ruku")
        self.assertTrue(rows)
        target = next(
            membership
            for membership in rows[0]["documented_memberships"]
            if membership["relation_set_id"] == "PB15-C1-RUKU"
        )
        self.assertTrue(target["fully_uniquely_resolved"])
        self.assertEqual(target["source_group"], "C1")
        roles = {member["relation_role"] for member in target["members"]}
        self.assertEqual(roles, {"BASIC", "CAUSATIVE"})
        self.assertTrue(
            all(member["dictionaria_match_status"] == STATUS_UNIQUE for member in target["members"])
        )

    def test_partial_set_preserves_unresolved_partner_without_inference(self):
        surface = self._single_token_headword("adxe")
        result = self.engine.analyze(surface, item_id="TECHNICAL_PB2015_PARTIAL_SET")
        rows = self._entry_relation_rows(result, "adxe")
        self.assertTrue(rows)
        target = next(
            membership
            for membership in rows[0]["documented_memberships"]
            if membership["relation_set_id"] == "PB15-V3-ADXE"
        )
        self.assertFalse(target["fully_uniquely_resolved"])
        self.assertEqual(target["current_member"]["relation_role"], "BASIC")
        partner = next(
            member for member in target["members"] if member["relation_role"] == "CAUSATIVE"
        )
        self.assertEqual(partner["source_form_pdlma_raw"], "-u-g-adxe")
        self.assertEqual(partner["dictionaria_match_status"], STATUS_NONE)
        self.assertEqual(partner["resolved_entry_ids"], [])
        self.assertFalse(partner["pdlma_form_is_project_surface_assertion"])

    def test_uunda_ambiguity_is_visible_but_not_assigned_to_either_entry(self):
        surface = self._single_token_headword("uunda1")
        result = self.engine.analyze(surface, item_id="TECHNICAL_PB2015_AMBIGUOUS_CROSSWALK")
        rows = [
            *self._entry_relation_rows(result, "uunda1"),
            *self._entry_relation_rows(result, "uunda2"),
        ]
        self.assertTrue(rows)
        for row in rows:
            self.assertEqual(row["documented_memberships"], [])
            candidates = row["ambiguous_crosswalk_candidates"]
            self.assertTrue(candidates)
            candidate = next(
                item for item in candidates if item["relation_set_id"] == "PB15-V2-UUNDA"
            )
            self.assertEqual(candidate["relation_role"], "BASIC")
            self.assertEqual(candidate["source_form_pdlma_raw"], "-uunda")
            self.assertEqual(set(candidate["candidate_entry_ids"]), {"uunda1", "uunda2"})
            self.assertEqual(candidate["status"], "AMBIGUOUS_STRICT_CROSSWALK_NOT_ASSIGNED")
            self.assertFalse(candidate["relation_assignment_assertion"])

        source_rows = [
            row
            for row in self.engine.relation_index.by_set["PB15-V2-UUNDA"]
            if row["dictionaria_match_status"] == STATUS_MULTIPLE
        ]
        self.assertEqual(len(source_rows), 1)

    def test_structural_candidate_route_cannot_assert_explicit_relation(self):
        payload = {
            "token_index": 0,
            "entries": [
                {
                    "entry_id": "ruku",
                    "entry_link_route": ROUTE_STRUCTURAL,
                    "entry_link_strength": "COMPATIBILITY_CANDIDATE_ONLY",
                    "documented_headword_raw": self.engine.morph1.records["ruku"].headword_raw,
                }
            ],
        }
        synthetic_result = {"valency_compatibility_observations": [payload]}
        eligible = self.engine._eligible_identified_entries(synthetic_result)
        self.assertEqual(dict(eligible), {})

    def test_unknown_surface_does_not_gain_relation_data(self):
        result = self.engine.analyze(
            "ZZZ_SYNTHETIC_PB2015_NONFORM_41021",
            item_id="TECHNICAL_PB2015_NEGATIVE",
        )
        self.assertEqual(result["explicit_valency_relation_informative_token_indexes"], [])
        self.assertEqual(
            result["explicit_valency_relation_observations"][0]["status"],
            "NO_ELIGIBLE_IDENTIFIED_VERB_ENTRY",
        )
        self.assertEqual(result["verb_morphological_hypothesis_informative_token_indexes"], [])
        self.assertEqual(result["causative_group_coordinate_informative_token_indexes"], [])
        self.assertFalse(result["automatic_pb2015_group_assignment_enabled"])
        self.assertFalse(result["surface_valency_relation_inference_enabled"])
        self.assertFalse(result["explicit_valency_relation_generation_enabled"])
        self.assertFalse(result["explicit_valency_relation_correction_enabled"])


if __name__ == "__main__":
    unittest.main()
