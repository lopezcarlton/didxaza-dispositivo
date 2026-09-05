#!/usr/bin/env python3

from __future__ import annotations

import unittest

from run_new_written_analysis_target import analyze_target_text


class NewWrittenAnalysisTargetRunnerTests(unittest.TestCase):
    def test_neutral_smoke_probe_is_quarantined_and_reproducible(self) -> None:
        payload = analyze_target_text(
            "xubá’\n\n",
            input_kind="test_fixture",
            item_prefix="NEUTRAL_SMOKE",
        )

        self.assertEqual(payload["schema_version"], "1.1")
        self.assertEqual(payload["target_role"], "NEW_WRITTEN_ANALYSIS_TARGET")
        self.assertEqual(payload["analyzed_nonempty_line_count"], 1)
        self.assertTrue(payload["target_internal_context_enabled"])
        self.assertEqual(payload["target_internal_context_radius_nonempty_lines"], 1)
        self.assertTrue(payload["target_internal_context_excludes_current_line"])
        self.assertFalse(payload["target_internal_context_is_authority"])
        self.assertFalse(payload["target_internal_context_can_create_rules"])
        self.assertFalse(payload["target_internal_context_can_promote_knowledge"])
        self.assertFalse(payload["target_internal_context_can_resolve_hypothesis_by_itself"])
        self.assertFalse(payload["benchmark_use"])
        self.assertFalse(payload["gold_use"])
        self.assertFalse(payload["regression_source_use"])
        self.assertFalse(payload["rule_discovery"])
        self.assertFalse(payload["correction_authority"])
        self.assertFalse(payload["generation_license"])
        self.assertFalse(payload["orthographic_authority"])
        self.assertFalse(payload["knowledge_promotion_from_target"])

        row = payload["results"][0]
        self.assertEqual(row["source_line_number"], 1)
        self.assertEqual(row["original_surface"], "xubá’")
        self.assertEqual(row["context_source_line_numbers"], [])
        self.assertEqual(row["context_segment_count"], 0)
        self.assertEqual(row["analysis"]["item_id"], "NEUTRAL_SMOKE_L001")
        self.assertFalse(row["analysis"]["context_channel"]["context_supplied"])
        self.assertFalse(row["analysis"]["correction_assertion"])
        self.assertFalse(row["analysis"]["generation_license_assertion"])
        self.assertFalse(row["analysis"]["orthographic_authority_assertion"])
        self.assertFalse(row["analysis"]["rule_discovery_assertion"])

    def test_neighboring_nonempty_lines_are_passed_as_nonresolving_context(self) -> None:
        payload = analyze_target_text(
            "xubá’\n\nbeeu\nni\n",
            input_kind="test_fixture",
            item_prefix="NEUTRAL_CONTEXT_TRANSPORT",
            context_radius=1,
        )

        rows = payload["results"]
        self.assertEqual(len(rows), 3)
        self.assertEqual([row["source_line_number"] for row in rows], [1, 3, 4])
        self.assertEqual(rows[0]["context_source_line_numbers"], [3])
        self.assertEqual(rows[1]["context_source_line_numbers"], [1, 4])
        self.assertEqual(rows[2]["context_source_line_numbers"], [3])
        self.assertEqual([row["context_segment_count"] for row in rows], [1, 2, 1])

        for row in rows:
            channel = row["analysis"]["context_channel"]
            self.assertTrue(channel["context_supplied"])
            self.assertEqual(channel["context_segment_count"], row["context_segment_count"])
            self.assertFalse(channel["used_for_local_analysis"])
            self.assertFalse(row["analysis"]["contextual_documentary_support_changes_analysis_status"])
            self.assertFalse(row["analysis"]["contextual_documentary_support_changes_exact_evidence_metrics"])
            self.assertFalse(row["analysis"]["correction_assertion"])
            self.assertFalse(row["analysis"]["generation_license_assertion"])

    def test_context_radius_zero_preserves_line_isolation(self) -> None:
        payload = analyze_target_text(
            "xubá’\nbeeu\n",
            input_kind="test_fixture",
            item_prefix="NEUTRAL_CONTEXT_OFF",
            context_radius=0,
        )
        self.assertFalse(payload["target_internal_context_enabled"])
        for row in payload["results"]:
            self.assertEqual(row["context_source_line_numbers"], [])
            self.assertEqual(row["context_segment_count"], 0)
            self.assertFalse(row["analysis"]["context_channel"]["context_supplied"])

    def test_negative_context_radius_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "context_radius must be >= 0"):
            analyze_target_text(
                "xubá’\n",
                input_kind="test_fixture",
                context_radius=-1,
            )


if __name__ == "__main__":
    unittest.main()
