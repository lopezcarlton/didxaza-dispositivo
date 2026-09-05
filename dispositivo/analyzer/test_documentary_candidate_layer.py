#!/usr/bin/env python3
"""Technical regressions for Analyzer documentary candidate observations.

These tests do not assert that a candidate spelling is correct or equivalent.
They assert only that already-specified candidate channels are visible while
remaining strictly separate from exact evidence and correction authority. Later
Analyzer wrappers may add documented morphology without changing this layer.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNTIME = HERE.parent / "runtime" / "v0_2_15_3"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(RUNTIME))

from analyzer_v0_35_migrated_adapter import build_migrated_analyzer  # noqa: E402
from biyubi_exact_source import BiyubiControlledSource  # noqa: E402
from documentary_candidate_layer_v0_1 import (  # noqa: E402
    DocumentaryCandidateIndex,
    STATUS_ORTHOGRAPHIC,
)


class _EmptyPickettDB:
    def execute(self, sql, params=()):
        return []


class DocumentaryCandidateIndexTests(unittest.TestCase):
    def test_vowel_length_candidate_is_not_exact_evidence(self):
        biyubi = BiyubiControlledSource.from_rows(
            [(10, "Binebiaaya'", "Conocí, reconocí")]
        )
        index = DocumentaryCandidateIndex(_EmptyPickettDB(), biyubi_source=biyubi)
        result = index.lookup("binebiaya'")
        self.assertEqual(result["candidate_status"], STATUS_ORTHOGRAPHIC)
        rows = [row for row in result["candidates"] if row["source_surface_raw"] == "Binebiaaya'"]
        self.assertTrue(rows)
        self.assertIn("SINGLE_VOWEL_LENGTH_EXPANSION_CANDIDATE", {row["relation_operation"]["operation"] for row in rows})
        self.assertTrue(all(not row["exact_surface_match_assertion"] for row in rows))
        self.assertTrue(all(not row["correction_assertion"] for row in rows))
        self.assertFalse(result["policy"]["generic_edit_distance"])
        self.assertFalse(result["policy"]["near_match_ranking"])
        self.assertFalse(result["policy"]["tone_stripping"])

    def test_final_glottal_candidate_is_separate_from_exact(self):
        biyubi = BiyubiControlledSource.from_rows(
            [(20, "Guendaranaxhii'", "Amor, querer, cariño, pasión")]
        )
        index = DocumentaryCandidateIndex(_EmptyPickettDB(), biyubi_source=biyubi)
        result = index.lookup("guendaranaxhii")
        rows = [row for row in result["candidates"] if row["source_surface_raw"] == "Guendaranaxhii'"]
        self.assertTrue(rows)
        self.assertIn("FINAL_GLOTTAL_MARK_INSERTION_CANDIDATE", {row["relation_operation"]["operation"] for row in rows})
        self.assertTrue(all(not row["semantic_equivalence_assertion"] for row in rows))
        self.assertFalse(result["policy"]["candidate_is_exact_evidence"])
        self.assertFalse(result["policy"]["candidate_can_promote_coverage"])

    def test_unlicensed_consonant_difference_is_not_a_candidate(self):
        biyubi = BiyubiControlledSource.from_rows([(30, "xquendascarulu'", "tu belleza")])
        index = DocumentaryCandidateIndex(_EmptyPickettDB(), biyubi_source=biyubi)
        result = index.lookup("xquendasicarulu'")
        self.assertEqual(result["candidate_count"], 0)


class CurrentAnalyzerCandidateLayerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = build_migrated_analyzer()

    @classmethod
    def tearDownClass(cls):
        cls.engine.close()

    def _candidate_row(self, surface: str):
        result = self.engine.analyze(surface, item_id="TECHNICAL_CANDIDATE_REGRESSION")
        self.assertEqual(result["current_adapter_version"], "0.35.10")
        self.assertTrue(result["documentary_candidate_layer_enabled"])
        self.assertEqual(len(result["provisional_unresolved_token_candidates"]), 1)
        return result, result["provisional_unresolved_token_candidates"][0]

    def test_pickett_ruunda_candidate_does_not_change_exact_state(self):
        result, row = self._candidate_row("ruunda")
        candidates = row["orthographic_documentary_candidates"]["candidates"]
        pickett = [x for x in candidates if x.get("source_surface_raw") in {"ruunda’", "ruunda'", "ruundaꞌ"}]
        self.assertTrue(pickett)
        self.assertIn("FINAL_GLOTTAL_MARK_INSERTION_CANDIDATE", {x["relation_operation"]["operation"] for x in pickett})
        self.assertEqual(result["effective_evidence_after_biyubi_token_count"], 0)
        self.assertEqual(result["unresolved_token_indexes_after_biyubi"], [0])
        self.assertEqual(result["still_exactly_unresolved_token_indexes"], [0])
        self.assertTrue(result["exact_evidence_state_unchanged_by_candidates"])
        self.assertEqual(result["analysis_status"], "ABSTAIN_NO_COMPONENT_EVIDENCE")

    def test_rucuidxiilu_exposes_existing_graphical_2sg_candidate_only(self):
        result, row = self._candidate_row("rucuidxiilu'")
        persons = row["graphical_person_candidates"]
        self.assertIn("2SG", {x["person"] for x in persons})
        self.assertIn("lu'", {x["matched_suffix"] for x in persons})
        self.assertTrue(all(x["status"] == "PROVISIONAL" for x in persons))
        self.assertEqual(result["still_exactly_unresolved_token_indexes"], [0])
        self.assertEqual(result["effective_evidence_after_biyubi_token_count"], 0)
        self.assertEqual(result["unresolved_token_indexes_after_documented_morphology"], [0])

    def test_binebiaya_exposes_existing_graphical_1sg_candidates_only(self):
        result, row = self._candidate_row("binebiaya'")
        persons = row["graphical_person_candidates"]
        self.assertIn("1SG", {x["person"] for x in persons})
        self.assertIn("ya'", {x["matched_suffix"] for x in persons})
        self.assertEqual(result["still_exactly_unresolved_token_indexes"], [0])
        self.assertEqual(result["unresolved_token_indexes_after_documented_morphology"], [0])
        self.assertFalse(row["exact_surface_match_assertion"])
        self.assertFalse(row["correction_assertion"])

    def test_possession_candidate_visible_inside_multiword_input(self):
        result = self.engine.analyze("Ne lii xquendasicarulu'", item_id="TECHNICAL_POSSESSION_VISIBILITY")
        rows = {row["token_index"]: row for row in result["provisional_unresolved_token_candidates"]}
        target_index = 2
        self.assertIn(target_index, rows)
        target = rows[target_index]
        self.assertIsNotNone(target["graphical_possession_candidate"])
        self.assertEqual(target["graphical_possession_candidate"]["prefix_candidate"], "x-")
        self.assertIn("2SG", {x["person"] for x in target["graphical_person_candidates"]})
        self.assertIn(target_index, result["still_exactly_unresolved_token_indexes"])
        self.assertIn(target_index, result["unresolved_token_indexes_after_documented_morphology"])

    def test_quidxu_remains_exactly_unresolved_despite_graphical_suffix_candidate(self):
        result, row = self._candidate_row("quidxu'")
        self.assertIn("2SG", {x["person"] for x in row["graphical_person_candidates"]})
        self.assertEqual(row["orthographic_documentary_candidates"]["candidate_count"], 0)
        self.assertEqual(result["still_exactly_unresolved_token_indexes"], [0])
        self.assertEqual(result["unresolved_token_indexes_after_documented_morphology"], [0])
        self.assertEqual(result["effective_evidence_after_biyubi_token_count"], 0)
        self.assertTrue(result["fallback_policy"]["candidate_layer_does_not_increase_effective_evidence_coverage"])
        self.assertFalse(result["correction_assertion"])
        self.assertFalse(result["orthographic_authority_assertion"])
        self.assertFalse(result["rule_discovery_assertion"])


if __name__ == "__main__":
    unittest.main()
