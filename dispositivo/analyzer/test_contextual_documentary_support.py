#!/usr/bin/env python3
"""Regressions for Analyzer v0.35.15 contextual documentary support.

Positive fixtures are discovered only from the already-versioned Dictionaria
examples supporting existing v0.35.13 hypotheses. No COR001 or
NEW_WRITTEN_ANALYSIS_TARGET material is used as benchmark, regression fixture,
or rule source.
"""

from __future__ import annotations

import unittest

from analyzer_v0_35_10_documentary_verb_form_candidates import (
    strict_documentary_key,
    tokenize_documentary_surface,
)
from analyzer_v0_35_15_contextual_documentary_support import (
    STATUS_NO_CONTEXT,
    STATUS_NO_SUPPORT,
    STATUS_SUPPORT,
    ContextualDocumentarySupportViewAnalyzer,
)
from analyzer_v0_35_migrated_adapter import build_migrated_analyzer


class ContextualDocumentarySupportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Independent test wrapper until v0.35.15 becomes the migrated outer adapter.
        cls.engine = ContextualDocumentarySupportViewAnalyzer(build_migrated_analyzer())
        # v0.35.15(test) -> v0.35.14 -> v0.35.13 -> v0.35.12 -> v0.35.11 -> v0.35.10.
        cls.v02 = cls.engine.base.base.base.base.base

    @classmethod
    def tearDownClass(cls):
        cls.engine.close()

    def _discover_context_supported_fixture(self):
        seen = set()
        for rows in self.v02._example_token_index.values():
            if not rows:
                continue
            token = rows[0]["token_surface_in_example"]
            if token in seen:
                continue
            seen.add(token)
            base_result = self.engine.base.analyze(
                token, item_id="TECHNICAL_CONTEXT_FIXTURE_DISCOVERY"
            )
            views = base_result.get("verb_morphological_hypothesis_views", ())
            if not views or not views[0].get("hypotheses"):
                continue
            query_key = strict_documentary_key(token)
            for hypothesis in views[0]["hypotheses"]:
                for example_id in hypothesis.get("supporting_example_ids", ()):
                    example = self.engine._example_by_id.get(str(example_id))
                    if not example:
                        continue
                    for context_token in tokenize_documentary_surface(
                        str(example.get("Primary_Text", "") or "")
                    ):
                        if strict_documentary_key(context_token) == query_key:
                            continue
                        return token, hypothesis, str(example_id), context_token, base_result
        self.fail("No existing hypothesis with a non-query context token in its supporting example")

    def test_context_overlap_adds_support_observation_not_resolution(self):
        token, hypothesis, example_id, context_token, base_result = (
            self._discover_context_supported_fixture()
        )
        result = self.engine.analyze(
            token,
            item_id="TECHNICAL_CONTEXT_DOCUMENTARY_SUPPORT",
            context_segments=[{"surface": context_token}],
        )
        self.assertEqual(result["current_adapter_version"], "0.35.15")
        self.assertEqual(result["contextual_documentary_support_informative_token_indexes"], [0])
        view = result["contextual_documentary_support_views"][0]
        self.assertEqual(view["status"], STATUS_SUPPORT)
        supported = [
            row for row in view["hypothesis_support"]
            if row["hypothesis_identity"]["entry_id_candidate"]
            == hypothesis["entry_id_candidate"]
            and row["hypothesis_identity"]["tam_candidate"]
            == hypothesis["tam_candidate"]
        ]
        self.assertTrue(supported)
        row = supported[0]
        self.assertTrue(row["contextual_support_available"])
        self.assertIn(strict_documentary_key(context_token), row["matched_context_keys"])
        example_ids = {
            item["example_id"] for item in row["supporting_documentary_examples"]
        }
        self.assertIn(example_id, example_ids)
        self.assertFalse(row["hypothesis_resolved_by_context"])
        self.assertFalse(row["hypothesis_rank_changed_by_context"])
        self.assertFalse(row["lexical_identity_assertion"])
        self.assertFalse(row["tam_assertion"])
        self.assertFalse(row["root_segmentation_assertion"])
        self.assertFalse(row["verb_class_assertion"])
        self.assertFalse(row["pdlma_to_ap_assertion"])
        self.assertEqual(result["analysis_status"], base_result["analysis_status"])
        self.assertEqual(
            result["effective_evidence_token_count"],
            base_result["effective_evidence_token_count"],
        )
        self.assertFalse(result["contextual_documentary_support_changes_exact_evidence_metrics"])
        self.assertFalse(result["contextual_documentary_support_changes_analysis_status"])
        self.assertFalse(result["contextual_documentary_support_resolution_enabled"])
        self.assertFalse(result["contextual_documentary_support_ranking_enabled"])
        self.assertFalse(result["context_channel"]["used_for_local_analysis"])
        self.assertTrue(result["context_channel"]["used_for_nonresolving_documentary_support"])

    def test_no_context_preserves_reserved_local_analysis_behavior(self):
        token, _, _, _, _ = self._discover_context_supported_fixture()
        result = self.engine.analyze(token, item_id="TECHNICAL_CONTEXT_NONE")
        view = result["contextual_documentary_support_views"][0]
        self.assertEqual(view["status"], STATUS_NO_CONTEXT)
        self.assertEqual(result["contextual_documentary_support_informative_token_indexes"], [])
        self.assertFalse(result["context_channel"]["context_supplied"])
        self.assertFalse(result["context_channel"]["used_for_local_analysis"])
        self.assertFalse(result["context_channel"]["used_for_nonresolving_documentary_support"])

    def test_unrelated_context_does_not_create_support_or_hypothesis(self):
        token, _, _, _, base_result = self._discover_context_supported_fixture()
        result = self.engine.analyze(
            token,
            item_id="TECHNICAL_CONTEXT_NEGATIVE",
            context_segments=[{"surface": "ZZZ_SYNTHETIC_CONTEXT_NONOVERLAP_73129"}],
        )
        view = result["contextual_documentary_support_views"][0]
        self.assertEqual(view["status"], STATUS_NO_SUPPORT)
        self.assertEqual(view["supported_hypothesis_count"], 0)
        self.assertEqual(result["contextual_documentary_support_informative_token_indexes"], [])
        self.assertEqual(
            result["verb_morphological_hypothesis_views"],
            base_result["verb_morphological_hypothesis_views"],
        )
        self.assertEqual(result["analysis_status"], base_result["analysis_status"])

    def test_query_token_repetition_alone_is_not_contextual_support(self):
        token, _, _, _, _ = self._discover_context_supported_fixture()
        result = self.engine.analyze(
            token,
            item_id="TECHNICAL_CONTEXT_TAUTOLOGY_BLOCK",
            context_segments=[{"surface": token}],
        )
        view = result["contextual_documentary_support_views"][0]
        self.assertEqual(view["status"], STATUS_NO_SUPPORT)
        self.assertEqual(view["supported_hypothesis_count"], 0)
        self.assertTrue(
            result["fallback_policy"][
                "contextual_documentary_support_excludes_query_token_repetition"
            ]
        )

    def test_unrecognized_context_fields_are_ignored_not_interpreted(self):
        token, _, _, context_token, _ = self._discover_context_supported_fixture()
        result = self.engine.analyze(
            token,
            item_id="TECHNICAL_CONTEXT_FIELD_POLICY",
            context_segments=[{"spanish": context_token}],
        )
        self.assertEqual(result["contextual_documentary_support_context_segments_consumed"], 0)
        self.assertEqual(result["contextual_documentary_support_context_segments_ignored"], 1)
        self.assertEqual(result["contextual_documentary_support_informative_token_indexes"], [])
        self.assertFalse(result["context_channel"]["used_for_local_analysis"])
        self.assertFalse(result["contextual_documentary_support_generation_enabled"])
        self.assertFalse(result["contextual_documentary_support_correction_enabled"])


if __name__ == "__main__":
    unittest.main()
