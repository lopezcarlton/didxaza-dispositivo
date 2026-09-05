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

        self.assertEqual(payload["target_role"], "NEW_WRITTEN_ANALYSIS_TARGET")
        self.assertEqual(payload["analyzed_nonempty_line_count"], 1)
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
        self.assertEqual(row["analysis"]["item_id"], "NEUTRAL_SMOKE_L001")
        self.assertFalse(row["analysis"]["correction_assertion"])
        self.assertFalse(row["analysis"]["generation_license_assertion"])
        self.assertFalse(row["analysis"]["orthographic_authority_assertion"])
        self.assertFalse(row["analysis"]["rule_discovery_assertion"])


if __name__ == "__main__":
    unittest.main()
