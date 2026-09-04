#!/usr/bin/env python3
"""Current execution adapter for the migrated Analyzer.

The historical v0.35 orchestrator remains unchanged. This module supplies
explicit paths to its verified runtime, SQLite and verb inventory dependencies,
wraps it with the v0.35.2 punctuation-light exact fallback, and optionally adds
v0.35.3 exact evidence from the controlled Biyubi source snapshot.

Neither primary analysis nor any fallback attestation grants generation,
correction, orthographic or research authority.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from analyzer_v0_35_2_punctuation_light_fallback_adapter import (
    PunctuationLightExactFallbackAnalyzer,
)
from analyzer_v0_35_3_biyubi_exact_fallback_adapter import (
    ADAPTER_VERSION,
    BiyubiExactFallbackAnalyzer,
)
from biyubi_exact_source import (
    BiyubiControlledSource,
    EXPECTED_NONEMPTY_ROWS as BIYUBI_EXPECTED_DATA_ROWS,
    EXPECTED_SNAPSHOT_SHA256 as BIYUBI_EXPECTED_SHA256,
    SOURCE_ENV_VAR as BIYUBI_SOURCE_ENV_VAR,
    SOURCE_ID as BIYUBI_SOURCE_ID,
)
from non_licensing_analyzer_orchestrator_v0_35 import (
    NonLicensingAnalyzerOrchestrator,
)


HERE = Path(__file__).resolve().parent
RUNTIME_ROOT = HERE.parent / "runtime" / "v0_2_15_3"
SQLITE_PATH = RUNTIME_ROOT / "BASE_CORRECTOR_DIDXAZA_SURFACE_SEMANTICS_v2_20.sqlite"
VERB_INVENTORY_PATH = HERE / "DIC_VERB_2385_v0_1.csv"


def _resolved_biyubi_path(biyubi_path: str | Path | None = None) -> Path | None:
    """Resolve explicit Biyubi path first, then the controlled-mount env var."""

    if biyubi_path is not None:
        return Path(biyubi_path).expanduser()
    env_value = os.environ.get(BIYUBI_SOURCE_ENV_VAR)
    if env_value:
        return Path(env_value).expanduser()
    return None


def build_migrated_analyzer(
    biyubi_path: str | Path | None = None,
    *,
    require_biyubi: bool = False,
) -> BiyubiExactFallbackAnalyzer:
    """Instantiate the current Analyzer over exact repository/source artifacts.

    Biyubi is a controlled optional mount because its raw XLSX is intentionally
    not published in this repository. When supplied, the loader validates the
    registered SHA-256 and 23,601-row data count before the Analyzer may use it.
    """

    historical = NonLicensingAnalyzerOrchestrator(
        runtime_root=RUNTIME_ROOT,
        sqlite_path=SQLITE_PATH,
        verb_inventory_path=VERB_INVENTORY_PATH,
    )
    builtin = PunctuationLightExactFallbackAnalyzer(historical)

    source_path = _resolved_biyubi_path(biyubi_path)
    if source_path is None:
        if require_biyubi:
            builtin.close()
            raise FileNotFoundError(
                f"Biyubi controlled source is required; pass --biyubi-xlsx or set {BIYUBI_SOURCE_ENV_VAR}"
            )
        return BiyubiExactFallbackAnalyzer(builtin, None)

    try:
        biyubi_source = BiyubiControlledSource(source_path)
    except Exception:
        builtin.close()
        raise
    return BiyubiExactFallbackAnalyzer(builtin, biyubi_source)


def migrated_execution_state(
    biyubi_path: str | Path | None = None,
) -> dict[str, Any]:
    """Describe the materialized, non-licensing Analyzer capability."""

    engine = build_migrated_analyzer(biyubi_path=biyubi_path)
    try:
        return {
            "status": "REPRODUCIBLE_NON_LICENSING_PARTIAL_ANALYZER",
            "historical_implementation": "non_licensing_analyzer_orchestrator_v0_35.py",
            "current_adapter": "analyzer_v0_35_3_biyubi_exact_fallback_adapter.py",
            "current_adapter_version": ADAPTER_VERSION,
            "exact_existing_layer_fallback_enabled": True,
            "punctuation_light_fallback_lookup_enabled": True,
            "fallback_layers": [
                "surface_attestation_v029",
                "pickett_lexical_record_v0211",
                "cross_source_exact_surface_v0212",
                "documentary_alignment_v0210",
            ],
            "controlled_external_sources": [
                {
                    "source_id": BIYUBI_SOURCE_ID,
                    "source_role": [
                        "SURFACE_EVIDENCE_SECONDARY",
                        "CONTRAST_EVIDENCE",
                        "PARADIGM_CANDIDATE",
                    ],
                    "payload_in_public_repository": False,
                    "mount_env_var": BIYUBI_SOURCE_ENV_VAR,
                    "registered_snapshot_sha256": BIYUBI_EXPECTED_SHA256,
                    "registered_data_rows": BIYUBI_EXPECTED_DATA_ROWS,
                    "mount_status": engine.biyubi_source_status,
                    "mounted_snapshot_sha256": (
                        engine.biyubi_source.snapshot_sha256
                        if engine.biyubi_source is not None
                        else None
                    ),
                    "orthographic_authority": False,
                }
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
    parser.add_argument(
        "--biyubi-xlsx",
        help=f"Controlled Biyubi XLSX; alternatively set {BIYUBI_SOURCE_ENV_VAR}",
    )
    parser.add_argument(
        "--require-biyubi",
        action="store_true",
        help="Fail rather than run without the controlled Biyubi snapshot",
    )
    args = parser.parse_args()

    if args.surface is None:
        if args.require_biyubi and _resolved_biyubi_path(args.biyubi_xlsx) is None:
            raise FileNotFoundError(
                f"Biyubi controlled source is required; pass --biyubi-xlsx or set {BIYUBI_SOURCE_ENV_VAR}"
            )
        payload = migrated_execution_state(biyubi_path=args.biyubi_xlsx)
    else:
        engine = build_migrated_analyzer(
            biyubi_path=args.biyubi_xlsx,
            require_biyubi=args.require_biyubi,
        )
        try:
            payload = engine.analyze(args.surface, item_id=args.item_id)
        finally:
            engine.close()
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
