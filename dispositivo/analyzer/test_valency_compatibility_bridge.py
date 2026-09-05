#!/usr/bin/env python3
"""Independent regressions for ValencyCompatibilityBridge v0.1.

No NEW_WRITTEN_ANALYSIS_TARGET or COR001 material is used as a benchmark,
regression fixture or rule source. Positive integration fixtures are discovered
from the already-versioned 2,385-record Dictionaria verb derivative.
"""

from __future__ import annotations

import json
import unittest

from analyzer_v0_35_11_valency_compatibility_bridge import (
    GROUP_STATUS,
    NUMERIC_VALENCE_STATUS,
    ROUTE_EXACT,
    ROUTE_PERSON,
    ROUTE_STRUCTURAL,
    STATUS_DOCUMENTED,
    STATUS_NONE,
    parse_adjudicated_lexical_valency_codes,
)
from analyzer_v0_35_9_verb_analysis_bridge import _split_documented_headword_variants
from analyzer_v0_35_migrated_adapter import build_migrated_analyzer, migrated_execution_state


class ValencyCompatibilityBridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = build_migrated_analyzer()

    @classmethod
    def tearDownClass(cls):
        cls.engine.close()

    def test_literal_code_parser_is_narrow_and_non_generative(self):
        caus = parse_adjudicated_lexical_valency_codes("vB:caus")
        self.assertEqual(caus["lexical_valency_code_status"], STATUS_DOCUMENTED)
        self.assertTrue(caus["documented_causative_lexical_code"])
        self.assertEqual(caus["documented_transitivity_labels"], [])
        self.assertIsNone(caus["numeric_valence"])
        self.assertEqual(caus["numeric_valence_status"], NUMERIC_VALENCE_STATUS)
        self.assertIsNone(caus["pb2015_valency_group"])
        self.assertEqual(caus["pb2015_valency_group_status"], GROUP_STATUS)

        intr = parse_adjudicated_lexical_valency_codes("vC:i")
        self.assertEqual(intr["documented_transitivity_labels"], ["INTRANSITIVE"])
        self.assertFalse(intr["documented_causative_lexical_code"])

        trans = parse_adjudicated_lexical_valency_codes("vD(k>l):t")
        self.assertEqual(trans["documented_transitivity_labels"], ["TRANSITIVE"])

        vers = parse_adjudicated_lexical_valency_codes("vA:i vers")
        self.assertEqual(vers["documented_transitivity_labels"], ["INTRANSITIVE"])
        self.assertFalse(vers["vers_marker_interpreted"])
        self.assertFalse(vers["undefined_modifiers_interpreted"])

        unknown = parse_adjudicated_lexical_valency_codes("vCirr:a")
        self.assertEqual(unknown["lexical_valency_code_status"], STATUS_NONE)

        causal = parse_adjudicated_lexical_valency_codes("vA:causal")
        self.assertFalse(causal["documented_causative_lexical_code"])
        self.assertEqual(causal["lexical_valency_code_status"], STATUS_NONE)

    def test_execution_state_exposes_measured_inventory_and_hard_limits(self):
        state = migrated_execution_state()
        self.assertEqual(state["current_adapter_version"], "0.35.12")
        self.assertEqual(state["verb_analysis_bridge_version"], "0.2")
        self.assertTrue(state["valency_compatibility_bridge_enabled"])
        self.assertEqual(state["valency_compatibility_bridge_version"], "0.1")
        self.assertTrue(state["explicit_valency_relation_bridge_enabled"])

        stats = state["valency_compatibility_index_stats"]
        print("VALENCY_INDEX_STATS=" + json.dumps(stats, sort_keys=True))
        self.assertEqual(stats["verb_inventory_rows"], 2385)
        self.assertGreater(stats["entries_with_adjudicated_valency_code"], 0)
        self.assertGreater(stats["entries_with_literal_causative_code"], 0)
        self.assertGreater(stats["entries_with_intransitive_code"], 0)
        self.assertGreater(stats["entries_with_transitive_code"], 0)
        self.assertFalse(stats["group_assignment_enabled"])
        self.assertFalse(stats["numeric_valence_inference_enabled"])
        self.assertFalse(stats["surface_valency_inference_enabled"])

        policy = state["valency_compatibility_policy"]
        self.assertEqual(policy["literal_adjudicated_codes_only"], ["caus", "i", "t"])
        self.assertTrue(policy["requires_preexisting_verb_entry_link"])
        self.assertTrue(policy["structural_route_is_compatibility_only"])
        self.assertFalse(policy["pb2015_group_assignment"])
        self.assertFalse(policy["numeric_valence_inference_from_transitivity"])
        self.assertFalse(policy["basic_derived_relation_inference"])
        self.assertFalse(policy["vers_interpretation"])
        self.assertFalse(policy["surface_prefix_inference"])
        self.assertFalse(policy["pdlma_to_ap"])
        self.assertFalse(policy["generation_license"])
        self.assertFalse(policy["correction_authority"])

    def _find_exact_single_token_record_with(self, predicate):
        for entry_id, record in self.engine.morph1.records.items():
            parsed = parse_adjudicated_lexical_valency_codes(record.analysis_codes_raw)
            if not predicate(parsed):
                continue
            variants = _split_documented_headword_variants(record.headword_raw)
            for variant in variants:
                if variant and not any(ch.isspace() for ch in variant):
                    return entry_id, variant, record, parsed
        self.fail("No suitable exact single-token verb record found")

    def test_exact_causative_entry_surfaces_lexical_valency_without_group_inference(self):
        entry_id, surface, record, _ = self._find_exact_single_token_record_with(
            lambda parsed: parsed["documented_causative_lexical_code"]
        )
        result = self.engine.analyze(surface, item_id="TECHNICAL_VALENCY_EXACT_CAUSATIVE")
        observation = result["valency_compatibility_observations"][0]
        matching = [row for row in observation["entries"] if row["entry_id"] == entry_id]
        self.assertTrue(matching)
        row = matching[0]
        self.assertEqual(row["entry_link_route"], ROUTE_EXACT)
        self.assertTrue(row["lexical_valency"]["documented_causative_lexical_code"])
        self.assertTrue(row["lexical_property_asserted_for_observed_token"])
        self.assertIsNone(row["lexical_valency"]["pb2015_valency_group"])
        self.assertFalse(row["basic_to_derived_relation_assertion"])
        self.assertFalse(row["numeric_valence_assertion"])
        self.assertFalse(row["surface_prefix_valency_inference_assertion"])
        self.assertFalse(row["generation_license_assertion"])
        self.assertFalse(row["correction_assertion"])
        self.assertEqual(row["documented_headword_raw"], record.headword_raw)

    def test_exact_transitivity_code_does_not_become_numeric_valence(self):
        entry_id, surface, _, _ = self._find_exact_single_token_record_with(
            lambda parsed: bool(parsed["documented_transitivity_labels"])
        )
        result = self.engine.analyze(surface, item_id="TECHNICAL_VALENCY_EXACT_TRANSITIVITY")
        rows = [
            row
            for row in result["valency_compatibility_observations"][0]["entries"]
            if row["entry_id"] == entry_id and row["entry_link_route"] == ROUTE_EXACT
        ]
        self.assertTrue(rows)
        row = rows[0]
        self.assertTrue(row["lexical_valency"]["documented_transitivity_labels"])
        self.assertIsNone(row["lexical_valency"]["numeric_valence"])
        self.assertEqual(
            row["lexical_valency"]["numeric_valence_status"], NUMERIC_VALENCE_STATUS
        )

    def test_person_route_preserves_lemma_link_semantics_without_extra_inference(self):
        entry_id, _, _, _ = self._find_exact_single_token_record_with(
            lambda parsed: parsed["lexical_valency_code_status"] == STATUS_DOCUMENTED
        )
        payload = self.engine._entry_payload(
            entry_id,
            route=ROUTE_PERSON,
            token_index=0,
            token_raw="SYNTHETIC_PERSON_ROUTE_ONLY",
        )
        self.assertIsNotNone(payload)
        self.assertEqual(payload["entry_link_route"], ROUTE_PERSON)
        self.assertTrue(payload["lexical_property_asserted_for_observed_token"])
        self.assertFalse(payload["basic_to_derived_relation_assertion"])
        self.assertFalse(payload["pb2015_group_assignment_assertion"])
        self.assertFalse(payload["generation_license_assertion"])

    def test_structural_nonheadword_route_is_compatibility_only(self):
        chosen_surface = None
        chosen_entry = None
        # Current chain: v0.35.12 -> v0.35.11 -> v0.35.10 -> v0.35.9.
        # The example index belongs to v0.35.10; _lookup_token belongs to v0.35.9.
        v02 = self.engine.base.base
        v01 = v02.base
        for rows in v02._example_token_index.values():
            if not rows:
                continue
            token = rows[0]["token_surface_in_example"]
            if v01._lookup_token(token, 0)["verb_category_documented"]:
                continue
            entry_ids = {row["linked_verb_entry_id"] for row in rows}
            for entry_id in entry_ids:
                record = self.engine.morph1.records.get(entry_id)
                if record is None:
                    continue
                parsed = parse_adjudicated_lexical_valency_codes(record.analysis_codes_raw)
                if parsed["lexical_valency_code_status"] != STATUS_DOCUMENTED:
                    continue
                chosen_surface = token
                chosen_entry = entry_id
                break
            if chosen_surface is not None:
                break

        self.assertIsNotNone(
            chosen_surface,
            "No independent non-headword structural candidate with valency code found",
        )
        result = self.engine.analyze(
            chosen_surface, item_id="TECHNICAL_VALENCY_STRUCTURAL_CANDIDATE"
        )
        rows = [
            row
            for obs in result["valency_compatibility_observations"]
            for row in obs["entries"]
            if row["entry_id"] == chosen_entry and row["entry_link_route"] == ROUTE_STRUCTURAL
        ]
        self.assertTrue(rows)
        row = rows[0]
        self.assertFalse(row["lexical_property_asserted_for_observed_token"])
        self.assertTrue(row["lexical_property_applies_to_documented_entry"])
        self.assertFalse(row["basic_to_derived_relation_assertion"])
        self.assertFalse(row["pb2015_group_assignment_assertion"])
        self.assertFalse(row["numeric_valence_assertion"])
        self.assertFalse(row["generation_license_assertion"])
        self.assertFalse(result["valency_compatibility_changes_exact_evidence_metrics"])
        self.assertFalse(result["valency_compatibility_changes_analysis_status"])
        self.assertEqual(result["explicit_valency_relation_informative_token_indexes"], [])

    def test_unknown_surface_receives_no_valency_entry_link(self):
        result = self.engine.analyze(
            "ZZZ_SYNTHETIC_VALENCY_NONFORM_91277",
            item_id="TECHNICAL_VALENCY_NEGATIVE",
        )
        self.assertEqual(result["valency_compatibility_informative_token_indexes"], [])
        self.assertEqual(
            result["valency_compatibility_observations"][0]["status"],
            "NO_LINKED_VERB_ENTRY",
        )
        self.assertEqual(result["explicit_valency_relation_informative_token_indexes"], [])
        self.assertFalse(result["valency_generation_enabled"])
        self.assertFalse(result["valency_correction_enabled"])


if __name__ == "__main__":
    unittest.main()
