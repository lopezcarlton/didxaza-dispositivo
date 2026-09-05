#!/usr/bin/env python3
"""Regressions for Analyzer v0.35.14 causative group coordinates.

Fixtures come from the already-versioned PB2015 explicit relation crosswalk or
synthetic negative strings. No COR001 or NEW_WRITTEN_ANALYSIS_TARGET material is
used as benchmark, regression fixture, or rule source.
"""

from __future__ import annotations

import unittest

from analyzer_v0_35_14_causative_group_coordinates import (
    CAUSATIVE_GROUP_RESOURCES,
    STATUS_AVAILABLE,
    STATUS_NONE,
    CausativeGroupCoordinateViewAnalyzer,
    group_resource_payload,
)
from analyzer_v0_35_9_verb_analysis_bridge import _split_documented_headword_variants
from analyzer_v0_35_migrated_adapter import build_migrated_analyzer


class CausativeGroupCoordinateViewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # At this stage the migrated builder is v0.35.13; wrap it independently
        # before promoting v0.35.14 to the current outer adapter.
        cls.engine = CausativeGroupCoordinateViewAnalyzer(build_migrated_analyzer())

    @classmethod
    def tearDownClass(cls):
        cls.engine.close()

    def _single_token_headword(self, entry_id: str) -> str:
        record = self.engine.morph1.records[entry_id]
        for variant in _split_documented_headword_variants(record.headword_raw):
            if variant and not any(ch.isspace() for ch in variant):
                return variant
        self.fail(f"No single-token headword for {entry_id}")

    def test_group_resource_map_matches_adjudicated_c1_c4_coordinates(self):
        expected = {
            "C1": "-g-",
            "C2": "-u-",
            "C3": "-u-g-",
            "C4": "-u(-g)-zi- / -zu-",
        }
        self.assertEqual(set(CAUSATIVE_GROUP_RESOURCES), set(expected))
        for group, raw in expected.items():
            payload = group_resource_payload(group)
            self.assertIsNotNone(payload)
            self.assertEqual(payload["analytical_resource_raw"], raw)
            self.assertEqual(payload["source_group"], group)
            self.assertFalse(payload["observed_surface_prefix_assertion"])
            self.assertFalse(payload["observed_surface_segmentation_assertion"])
            self.assertFalse(payload["observed_token_causative_analysis_assertion"])
            self.assertFalse(payload["pdlma_to_ap_assertion"])
            self.assertFalse(payload["productive_rule_assertion"])
        self.assertIsNone(group_resource_payload("V2"))

    def test_chuku_preserves_c1_and_c2_group_coordinates_without_surface_parse(self):
        surface = self._single_token_headword("chuku")
        result = self.engine.analyze(surface, item_id="TECHNICAL_CAUSATIVE_GROUP_CHUKU")
        self.assertEqual(result["current_adapter_version"], "0.35.14")
        self.assertEqual(result["causative_group_coordinate_informative_token_indexes"], [0])
        observation = result["causative_group_coordinate_observations"][0]
        self.assertEqual(observation["status"], STATUS_AVAILABLE)
        by_group = {row["source_group"]: row for row in observation["coordinates"]}
        self.assertIn("C1", by_group)
        self.assertIn("C2", by_group)

        c1 = by_group["C1"]
        self.assertEqual(c1["source_explicit_relation_role"], "CAUSATIVE")
        self.assertTrue(c1["entry_is_source_explicit_causative_member"])
        self.assertEqual(c1["group_causative_resource"]["analytical_resource_raw"], "-g-")

        c2 = by_group["C2"]
        self.assertEqual(c2["source_explicit_relation_role"], "BASIC")
        self.assertTrue(c2["entry_is_source_explicit_basic_member"])
        self.assertEqual(c2["group_causative_resource"]["analytical_resource_raw"], "-u-")

        for row in observation["coordinates"]:
            self.assertFalse(row["group_was_inferred_from_surface"])
            self.assertFalse(row["resource_was_detected_from_visible_prefix"])
            self.assertFalse(row["observed_surface_prefix_assertion"])
            self.assertFalse(row["observed_surface_segmentation_assertion"])
            self.assertFalse(row["observed_token_causative_analysis_assertion"])
            self.assertFalse(row["pdlma_to_ap_assertion"])

        self.assertFalse(result["causative_group_coordinate_changes_exact_evidence_metrics"])
        self.assertFalse(result["causative_group_coordinate_changes_analysis_status"])

    def test_visible_prefix_resemblance_alone_never_creates_group_coordinate(self):
        result = self.engine.analyze(
            "ugziZZZ_SYNTHETIC_NONFORM_72819",
            item_id="TECHNICAL_CAUSATIVE_PREFIX_NEGATIVE",
        )
        observation = result["causative_group_coordinate_observations"][0]
        self.assertEqual(observation["status"], STATUS_NONE)
        self.assertEqual(observation["coordinates"], [])
        self.assertEqual(result["causative_group_coordinate_informative_token_indexes"], [])
        self.assertFalse(result["causative_visible_prefix_detection_enabled"])
        self.assertFalse(result["causative_group_surface_assignment_enabled"])

    def test_unknown_surface_preserves_non_authority(self):
        result = self.engine.analyze(
            "ZZZ_SYNTHETIC_CAUSATIVE_GROUP_NONFORM_91827",
            item_id="TECHNICAL_CAUSATIVE_GROUP_NEGATIVE",
        )
        self.assertEqual(result["causative_group_coordinate_informative_token_indexes"], [])
        self.assertFalse(result["causative_group_generation_enabled"])
        self.assertFalse(result["causative_group_correction_enabled"])
        self.assertFalse(result["generation_license_assertion"])
        self.assertFalse(result["correction_assertion"])
        self.assertFalse(result["orthographic_authority_assertion"])
        self.assertFalse(result["rule_discovery_assertion"])


if __name__ == "__main__":
    unittest.main()
