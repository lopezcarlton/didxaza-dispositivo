#!/usr/bin/env python3
"""Regressions for the v0.35.13 verb morphological hypothesis view.

Positive fixtures are discovered from the already-versioned v0.35.10
Dictionaria candidate index and must survive into the current Analyzer's
`documentary_verb_form_candidates` output. No COR001 or
NEW_WRITTEN_ANALYSIS_TARGET material is used as benchmark, regression fixture,
or rule source.
"""

from __future__ import annotations

import unittest

from analyzer_v0_35_13_verb_morphological_hypotheses import (
    STATUS_MULTIPLE,
    STATUS_NONE,
    STATUS_UNIQUE,
)
from analyzer_v0_35_migrated_adapter import build_migrated_analyzer


class VerbMorphologicalHypothesisViewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = build_migrated_analyzer()
        # v0.35.14 -> v0.35.13 -> v0.35.12 -> v0.35.11 -> v0.35.10.
        cls.v02 = cls.engine.base.base.base.base

    @classmethod
    def tearDownClass(cls):
        cls.engine.close()

    def _discover_unique_candidate(self):
        seen_tokens = set()
        for rows in self.v02._example_token_index.values():
            if not rows:
                continue
            token = rows[0]["token_surface_in_example"]
            if token in seen_tokens:
                continue
            seen_tokens.add(token)
            # Require the candidate to survive all layers through v0.35.13.
            # Earlier resolution is a valid reason for it not to appear here.
            current = self.engine.base.analyze(
                token, item_id="TECHNICAL_MORPH_HYPOTHESIS_FIXTURE_DISCOVERY"
            )
            candidates = current.get("documentary_verb_form_candidates", ())
            for payload in candidates:
                if int(payload.get("token_index", -1)) != 0:
                    continue
                if len(payload.get("compatible_verb_entries", ())) != 1:
                    continue
                entry = payload["compatible_verb_entries"][0]
                if len(entry.get("tam_candidates", ())) != 1:
                    continue
                if not payload.get("raw_nfc_exact_documentary_token_attestation"):
                    continue
                return token, entry
        self.fail("No surviving unique documentary TAM/root/class candidate found")

    def test_unique_documentary_candidate_becomes_explicit_hypothesis_not_fact(self):
        surface, upstream_entry = self._discover_unique_candidate()
        result = self.engine.analyze(
            surface, item_id="TECHNICAL_VERB_MORPH_HYPOTHESIS_UNIQUE"
        )
        self.assertEqual(result["current_adapter_version"], "0.35.14")
        self.assertEqual(result["verb_morphological_hypothesis_informative_token_indexes"], [0])
        view = result["verb_morphological_hypothesis_views"][0]
        self.assertEqual(view["status"], STATUS_UNIQUE)
        self.assertEqual(view["hypothesis_count"], 1)
        hypothesis = view["hypotheses"][0]
        self.assertEqual(hypothesis["entry_id_candidate"], upstream_entry["entry_id"])
        self.assertEqual(hypothesis["tam_candidate"], upstream_entry["tam_candidates"][0])
        self.assertEqual(
            hypothesis["root_candidate_analytical_raw"], upstream_entry["root_analysis_raw"]
        )
        self.assertEqual(hypothesis["verb_class_candidate"], upstream_entry["verb_class"])
        self.assertTrue(hypothesis["matching_documented_pdlma_variants_raw"])
        self.assertFalse(hypothesis["observed_token_is_verb_assertion"])
        self.assertFalse(hypothesis["tam_of_observed_token_assertion"])
        self.assertFalse(hypothesis["root_segmentation_of_observed_token_assertion"])
        self.assertFalse(hypothesis["verb_class_of_observed_token_assertion"])
        self.assertFalse(hypothesis["pdlma_to_ap_assertion"])
        self.assertFalse(view["candidate_is_fact"])
        self.assertFalse(view["candidate_resolves_token"])
        self.assertFalse(result["causative_group_coordinate_changes_analysis_status"])

    def test_multiple_coordinates_remain_multiple_hypotheses(self):
        candidate = {
            "candidate_status": "SYNTHETIC_TEST_UPSTREAM_CANDIDATE",
            "candidate_key_policy": "SYNTHETIC_TEST_POLICY",
            "raw_nfc_exact_documentary_token_attestation": True,
            "compatible_verb_entries": [
                {
                    "entry_id": "SYNTH_E1",
                    "documented_headword_raw": "SYNTH_HEADWORD",
                    "definition_es": "fixture",
                    "verb_class": "A",
                    "class_status": "DOCUMENTED",
                    "irregular": "NO",
                    "pdlma_citation_raw": "-synth",
                    "root_analysis_raw": "synth",
                    "tam_candidates": ["HABITUAL", "COMPLETIVE"],
                    "matching_documented_pdlma_variants": {
                        "HABITUAL": ["ri-synth"],
                        "COMPLETIVE": ["bi-synth"],
                    },
                    "supporting_example_ids": ["SYNTH_EXAMPLE"],
                    "supporting_example_count": 1,
                    "query_matches_supporting_ap_token_raw_nfc_exact": True,
                    "association_strength": "SYNTHETIC_TEST_ONLY",
                }
            ],
        }
        view = self.engine._token_view(0, [candidate])
        self.assertEqual(view["status"], STATUS_MULTIPLE)
        self.assertEqual(view["hypothesis_count"], 2)
        self.assertEqual(set(view["tam_candidates"]), {"HABITUAL", "COMPLETIVE"})
        self.assertTrue(all(not row["tam_of_observed_token_assertion"] for row in view["hypotheses"]))

    def test_unknown_surface_receives_no_hypothesis(self):
        result = self.engine.analyze(
            "ZZZ_SYNTHETIC_MORPH_HYPOTHESIS_NONFORM_88211",
            item_id="TECHNICAL_VERB_MORPH_HYPOTHESIS_NEGATIVE",
        )
        view = result["verb_morphological_hypothesis_views"][0]
        self.assertEqual(view["status"], STATUS_NONE)
        self.assertEqual(view["hypotheses"], [])
        self.assertEqual(result["verb_morphological_hypothesis_informative_token_indexes"], [])
        self.assertEqual(result["causative_group_coordinate_informative_token_indexes"], [])
        self.assertFalse(result["verb_morphological_hypothesis_changes_exact_evidence_metrics"])
        self.assertFalse(result["verb_morphological_hypothesis_changes_analysis_status"])
        self.assertFalse(result["verb_morphological_hypothesis_generation_enabled"])
        self.assertFalse(result["verb_morphological_hypothesis_correction_enabled"])

    def test_view_never_claims_visible_prefix_segmentation(self):
        surface, _ = self._discover_unique_candidate()
        result = self.engine.analyze(surface, item_id="TECHNICAL_NO_VISIBLE_PREFIX_SEGMENTATION")
        view = result["verb_morphological_hypothesis_views"][0]
        self.assertFalse(view["surface_prefix_segmentation_assertion"])
        self.assertFalse(result["fallback_policy"]["verb_morphological_hypothesis_visible_prefix_segmentation"])
        self.assertFalse(result["fallback_policy"]["verb_morphological_hypothesis_pdlma_to_ap"])
        self.assertFalse(result["fallback_policy"]["causative_group_coordinate_visible_prefix_detection"])


if __name__ == "__main__":
    unittest.main()
