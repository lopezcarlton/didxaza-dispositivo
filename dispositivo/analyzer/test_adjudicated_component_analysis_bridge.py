#!/usr/bin/env python3
"""Technical tests for v0.35.16 adjudicated component-analysis bridge.

These tests intentionally do not query any form from a NEW_WRITTEN_ANALYSIS_TARGET.
The bridge is exercised with a temporary synthetic registry whose strings have no
linguistic status. The production registry is checked only for loadability and
policy metadata, never by looking up its registered surface.
"""

from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from analyzer_v0_35_16_adjudicated_component_analysis_bridge import (  # noqa: E402
    ADAPTER_VERSION,
    BRIDGE_VERSION,
    AdjudicatedComponentAnalysisBridgeAnalyzer,
    STATUS_NONE,
    STATUS_SUPPORTED,
)
from voces_component_analysis_source import (  # noqa: E402
    DEFAULT_REGISTRY_PATH,
    EXPECTED_VOCES_COMMIT,
    MATCH_POLICY,
    VocesComponentAnalysisSource,
)


HEADER = [
    "surface_raw",
    "components_raw",
    "component_glosses",
    "component_functions",
    "analysis_status",
    "boundary_status",
    "hall_id",
    "voces_commit",
    "source_ids",
    "epistemic_role",
    "license_status",
]


class FakeBaseAnalyzer:
    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []
        self.closed = False

    def analyze(
        self,
        surface: str,
        *,
        item_id: str | None = None,
        spanish_supplied: str | None = None,
        context_segments: list[dict[str, object]] | None = None,
    ) -> dict[str, object]:
        self.calls.append(
            {
                "surface": surface,
                "item_id": item_id,
                "spanish_supplied": spanish_supplied,
                "context_segments": context_segments,
            }
        )
        return {
            "surface_original": surface,
            "token_count": len(surface.split()),
            "analysis_status": "ABSTAIN_NO_COMPONENT_EVIDENCE",
            "matched_token_count": 0,
            "effective_evidence_token_count": 0,
            "fallback_policy": {},
            "limitations": [],
            "generation_license_assertion": False,
            "correction_assertion": False,
            "orthographic_authority_assertion": False,
            "rule_discovery_assertion": False,
        }

    def close(self) -> None:
        self.closed = True


def write_registry(path: Path, *, surface: str = "fixturealpha", commit: str = EXPECTED_VOCES_COMMIT) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADER)
        writer.writeheader()
        writer.writerow(
            {
                "surface_raw": surface,
                "components_raw": "fixture|alpha",
                "component_glosses": "technical-one|technical-two",
                "component_functions": "TEST_COMPONENT_A|TEST_COMPONENT_B",
                "analysis_status": "CONTEXTUALLY_SUPPORTED_COMPONENT_ANALYSIS",
                "boundary_status": "TECHNICAL_TEST_BOUNDARY_STATUS",
                "hall_id": "HALL-TECHNICAL-FIXTURE",
                "voces_commit": commit,
                "source_ids": "SRC-TECHNICAL-TEST-ONLY",
                "epistemic_role": "TECHNICAL_FIXTURE_ONLY",
                "license_status": "NON_LICENSING",
            }
        )


class AdjudicatedComponentAnalysisBridgeTests(unittest.TestCase):
    def _source(self, *, surface: str = "fixturealpha") -> tuple[tempfile.TemporaryDirectory[str], VocesComponentAnalysisSource]:
        tmp = tempfile.TemporaryDirectory()
        path = Path(tmp.name) / "registry.csv"
        write_registry(path, surface=surface)
        return tmp, VocesComponentAnalysisSource(path)

    def test_exact_registered_surface_exposes_analysis_without_rewriting_upstream(self) -> None:
        tmp, source = self._source()
        self.addCleanup(tmp.cleanup)
        base = FakeBaseAnalyzer()
        engine = AdjudicatedComponentAnalysisBridgeAnalyzer(base, component_source=source)

        context = [{"surface": "neighbor technical context"}]
        result = engine.analyze(
            "fixturealpha",
            item_id="TECHNICAL_COMPONENT_BRIDGE_FIXTURE",
            context_segments=context,
        )

        self.assertEqual(result["current_adapter_version"], ADAPTER_VERSION)
        self.assertEqual(ADAPTER_VERSION, "0.35.16")
        self.assertEqual(result["adjudicated_component_analysis_bridge_version"], BRIDGE_VERSION)
        self.assertEqual(result["adjudicated_component_analysis_informative_token_indexes"], [0])
        view = result["adjudicated_component_analysis_views"][0]
        self.assertEqual(view["status"], STATUS_SUPPORTED)
        self.assertEqual(view["analysis_count"], 1)
        self.assertEqual(view["analyses"][0]["components_raw"], ["fixture", "alpha"])
        self.assertEqual(view["analyses"][0]["hall_id"], "HALL-TECHNICAL-FIXTURE")
        self.assertEqual(view["surface_match_policy"], MATCH_POLICY)

        # The bridge exposes canonical metadata but does not resolve or inflate local evidence.
        self.assertEqual(result["analysis_status"], "ABSTAIN_NO_COMPONENT_EVIDENCE")
        self.assertEqual(result["matched_token_count"], 0)
        self.assertEqual(result["effective_evidence_token_count"], 0)
        self.assertFalse(result["adjudicated_component_analysis_changes_exact_evidence_metrics"])
        self.assertFalse(result["adjudicated_component_analysis_changes_analysis_status"])
        self.assertFalse(view["analysis_discovered_from_substring"])
        self.assertFalse(view["analysis_created_from_runtime_context"])
        self.assertFalse(view["analysis_resolved_by_runtime_context"])
        self.assertFalse(view["morphological_compound_assertion"])
        self.assertFalse(view["orthographic_boundary_preference_assertion"])
        self.assertFalse(view["correction_assertion"])
        self.assertFalse(view["generation_license_assertion"])
        self.assertFalse(view["orthographic_authority_assertion"])
        self.assertFalse(view["rule_discovery_assertion"])
        self.assertIs(base.calls[0]["context_segments"], context)

    def test_substring_overlap_cannot_create_component_analysis(self) -> None:
        tmp, source = self._source()
        self.addCleanup(tmp.cleanup)
        engine = AdjudicatedComponentAnalysisBridgeAnalyzer(FakeBaseAnalyzer(), component_source=source)
        result = engine.analyze("prefixfixturealpha")
        view = result["adjudicated_component_analysis_views"][0]
        self.assertEqual(view["status"], STATUS_NONE)
        self.assertEqual(view["analysis_count"], 0)
        self.assertFalse(result["fallback_policy"]["component_analysis_substring_discovery"])

    def test_runtime_context_cannot_supply_missing_registered_surface(self) -> None:
        tmp, source = self._source()
        self.addCleanup(tmp.cleanup)
        engine = AdjudicatedComponentAnalysisBridgeAnalyzer(FakeBaseAnalyzer(), component_source=source)
        result = engine.analyze(
            "otherfixture",
            context_segments=[{"surface": "fixturealpha appears only in context"}],
        )
        view = result["adjudicated_component_analysis_views"][0]
        self.assertEqual(view["status"], STATUS_NONE)
        self.assertFalse(result["fallback_policy"]["component_analysis_runtime_context_can_create"])
        self.assertFalse(result["fallback_policy"]["component_analysis_runtime_context_can_resolve"])

    def test_lookup_is_nfc_only_not_casefold_or_apostrophe_normalization(self) -> None:
        # Synthetic e + combining acute is NFC-equivalent to precomposed é.
        tmp, source = self._source(surface="fixturee\u0301")
        self.addCleanup(tmp.cleanup)
        self.assertEqual(len(source.lookup("fixtureé")), 1)
        self.assertEqual(len(source.lookup("FIXTUREÉ")), 0)
        self.assertFalse(source.stats["casefold"])
        self.assertFalse(source.stats["apostrophe_unification"])
        self.assertFalse(source.stats["tone_stripping"])
        self.assertFalse(source.stats["diacritic_stripping"])
        self.assertFalse(source.stats["substring_search"])

    def test_registry_rejects_wrong_voces_pin(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_name:
            path = Path(tmp_name) / "registry.csv"
            write_registry(path, commit="0" * 40)
            with self.assertRaisesRegex(ValueError, "does not match pin"):
                VocesComponentAnalysisSource(path)

    def test_production_registry_loads_without_using_registered_surface_as_fixture(self) -> None:
        source = VocesComponentAnalysisSource(DEFAULT_REGISTRY_PATH)
        stats = source.stats
        self.assertGreaterEqual(stats["record_count"], 1)
        self.assertEqual(stats["voces_commit"], EXPECTED_VOCES_COMMIT)
        self.assertEqual(stats["surface_match_policy"], MATCH_POLICY)
        self.assertFalse(stats["substring_search"])
        self.assertFalse(stats["near_match"])
        self.assertFalse(stats["edit_distance"])
        self.assertFalse(stats["pdlma_to_ap"])


if __name__ == "__main__":
    unittest.main()
