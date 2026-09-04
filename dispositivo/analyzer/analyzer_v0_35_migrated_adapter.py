#!/usr/bin/env python3
"""Current execution adapter for the migrated Analyzer.

The historical v0.35 orchestrator remains unchanged. This module supplies
explicit paths to its verified runtime, SQLite and verb inventory dependencies
and wraps it with the current v0.35.2 punctuation-light exact fallback.

Neither primary analysis nor fallback attestation grants generation,
correction, orthographic or research authority.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from analyzer_v0_35_2_punctuation_light_fallback_adapter import (
    ADAPTER_VERSION,
    PunctuationLightExactFallbackAnalyzer,
)
from non_licensing_analyzer_orchestrator_v0_35 import (
    NonLicensingAnalyzerOrchestrator,
)


HERE = Path(__file__).resolve().parent
RUNTIME_ROOT = HERE.parent / "runtime" / "v0_2_15_3"
SQLITE_PATH = RUNTIME_ROOT / "BASE_CORRECTOR_DIDXAZA_SURFACE_SEMANTICS_v2_20.sqlite"
VERB_INVENTORY_PATH = HERE / "DIC_VERB_2385_v0_1.csv"


def build_migrated_analyzer() -> PunctuationLightExactFallbackAnalyzer:
    """Instantiate the current migrated Analyzer over exact repository artifacts."""

    historical = NonLicensingAnalyzerOrchestrator(
        runtime_root=RUNTIME_ROOT,
        sqlite_path=SQLITE_PATH,
        verb_inventory_path=VERB_INVENTORY_PATH,
    )
    return PunctuationLightExactFallbackAnalyzer(historical)


def migrated_execution_state() -> dict[str, Any]:
    """Describe the materialized, non-licensing Analyzer capability."""

    engine = build_migrated_analyzer()
    try:
        return {
            "status": "REPRODUCIBLE_NON_LICENSING_PARTIAL_ANALYZER",
            "historical_implementation": "non_licensing_analyzer_orchestrator_v0_35.py",
            "current_adapter": "analyzer_v0_35_2_punctuation_light_fallback_adapter.py",
            "current_adapter_version": ADAPTER_VERSION,
            "exact_existing_layer_fallback_enabled": True,
            "punctuation_light_fallback_lookup_enabled": True,
            "fallback_layers": [
                "surface_attestation_v029",
                "pickett_lexical_record_v0211",
                "cross_source_exact_surface_v0212",
                "documentary_alignment_v0210",
            ],
            "runtime_profile": "runtime/v0_2_15_3",
            "dictionaria_entries": len(engine.retrieval.entries),
            "dictionaria_senses": sum(len(rows) for rows in engine.retrieval.senses.values()),
            "dictionaria_examples": len(engine.retrieval.examples),
            "verb_inventory_rows": len(engine.morph1.records),
            "verb_metadata_rows": len(engine.verb_meta),
            "person_possession_exact_rows": len(engine.person_exact),
            "generation_license_assertion": False,
            "correction_assertion": False,
            "orthographic_authority_assertion": False,
            "rule_discovery_assertion": False,
            "cor001_benchmark_allowed": False,
            "research_authority_assertion": False,
        }
    finally:
        engine.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--surface")
    parser.add_argument("--item-id", default="AD_HOC_NON_LICENSING_ANALYSIS")
    args = parser.parse_args()

    if args.surface is None:
        payload = migrated_execution_state()
    else:
        engine = build_migrated_analyzer()
        try:
            payload = engine.analyze(args.surface, item_id=args.item_id)
        finally:
            engine.close()
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
