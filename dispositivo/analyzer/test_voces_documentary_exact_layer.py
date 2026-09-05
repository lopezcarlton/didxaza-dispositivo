#!/usr/bin/env python3
from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

from analyzer_v0_35_2_punctuation_light_fallback_adapter import (
    PunctuationLightExactFallbackAnalyzer,
)
from analyzer_v0_35_3_biyubi_exact_fallback_adapter import BiyubiExactFallbackAnalyzer
from analyzer_v0_35_7_voces_documentary_exact_adapter import (
    VocesDocumentaryExactFallbackAnalyzer,
)
from analyzer_v0_35_migrated_adapter import (
    RUNTIME_ROOT,
    SQLITE_PATH,
    VERB_INVENTORY_PATH,
    migrated_execution_state,
)
from non_licensing_analyzer_orchestrator_v0_35 import NonLicensingAnalyzerOrchestrator
from voces_exact_documentary_source import (
    STATUS_EXACT,
    STATUS_NO_EXACT,
    VocesExactDocumentarySource,
)


FIELDS = [
    "surface_exact",
    "source_id",
    "source_location",
    "hall_id",
    "knowledge_commit",
    "evidence_type",
    "authority_scope",
]


class VocesDocumentaryExactLayerTest(unittest.TestCase):
    def _registry(self, root: Path) -> Path:
        path = root / "synthetic_voces_documentary.csv"
        with path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerow(
                {
                    "surface_exact": "SYNTHVOCES",
                    "source_id": "SYNTHETIC_TEST_SOURCE",
                    "source_location": "synthetic fixture",
                    "hall_id": "SYNTHETIC_TEST_HALL",
                    "knowledge_commit": "0" * 40,
                    "evidence_type": "EXACT_DOCUMENTARY_SURFACE_ATTESTATION",
                    "authority_scope": "TEST_ONLY_NON_LICENSING",
                }
            )
        return path

    def test_source_is_strict_exact_not_casefold(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source = VocesExactDocumentarySource(self._registry(Path(tmp)))
            self.assertEqual(source.lookup("SYNTHVOCES")["voces_documentary_status"], STATUS_EXACT)
            self.assertEqual(source.lookup("synthvoces")["voces_documentary_status"], STATUS_NO_EXACT)
            self.assertFalse(source.lookup("SYNTHVOCES")["correction_assertion"])

    def test_layer_resolves_only_documentary_attestation_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            historical = NonLicensingAnalyzerOrchestrator(
                runtime_root=RUNTIME_ROOT,
                sqlite_path=SQLITE_PATH,
                verb_inventory_path=VERB_INVENTORY_PATH,
            )
            existing = PunctuationLightExactFallbackAnalyzer(historical)
            biyubi = BiyubiExactFallbackAnalyzer(existing, None)
            analyzer = VocesDocumentaryExactFallbackAnalyzer(
                biyubi,
                registry_path=self._registry(Path(tmp)),
            )
            try:
                result = analyzer.analyze("SYNTHVOCES", item_id="SYNTHETIC_TEST")
            finally:
                analyzer.close()

            self.assertEqual(result["voces_documentary_exact_attested_token_indexes"], [0])
            self.assertEqual(result["unresolved_token_indexes_after_voces_documentary_exact"], [])
            self.assertEqual(
                result["analysis_status_promotion_basis"],
                "VOCES_PROMOTED_DOCUMENTARY_EXACT_SURFACE_ATTESTATION_ONLY",
            )
            self.assertTrue(result["fallback_policy"]["voces_documentary_attestation_not_morphological_analysis"])

    def test_current_builder_keeps_documentary_layer_under_latest_wrapper(self) -> None:
        state = migrated_execution_state()
        self.assertEqual(state["current_adapter_version"], "0.35.15")
        self.assertTrue(state["voces_documentary_exact_layer_enabled"])
        self.assertTrue(state["documented_person_fusion_analysis_enabled"])
        self.assertTrue(state["verb_analysis_bridge_enabled"])
        self.assertTrue(state["documentary_verb_form_candidate_layer_enabled"])
        self.assertTrue(state["valency_compatibility_bridge_enabled"])
        self.assertTrue(state["explicit_valency_relation_bridge_enabled"])
        self.assertTrue(state["verb_morphological_hypothesis_view_enabled"])
        self.assertTrue(state["causative_group_coordinate_view_enabled"])
        self.assertTrue(state["contextual_documentary_support_view_enabled"])
        self.assertFalse(state["generation_license_assertion"])
        self.assertFalse(state["correction_assertion"])


if __name__ == "__main__":
    unittest.main()
