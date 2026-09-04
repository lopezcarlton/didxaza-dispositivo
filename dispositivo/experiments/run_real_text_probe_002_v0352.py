#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ANALYZER_DIR = HERE.parent / "analyzer"
RUNTIME_DIR = HERE.parent / "runtime" / "v0_2_15_3"
sys.path.insert(0, str(ANALYZER_DIR))
sys.path.insert(0, str(RUNTIME_DIR))

from analyzer_v0_35_migrated_adapter import build_migrated_analyzer  # noqa: E402

INPUT = HERE / "REAL_TEXT_PROBE_002.txt"


def main() -> None:
    lines = [line for line in INPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    analyzer = build_migrated_analyzer()
    try:
        rows = []
        unique_unresolved = set()
        for line_no, text in enumerate(lines, 1):
            result = analyzer.analyze(text, item_id=f"REAL_TEXT_PROBE_002_L{line_no:02d}")
            tokens = text.split()
            unresolved_indexes = result.get("unresolved_token_indexes_after_exact_fallback", [])
            fallback = []
            for row in result.get("supplemental_exact_existing_layer_evidence", []):
                fallback.append({
                    "token_index": row["token_index"],
                    "token_raw": row["token_raw"],
                    "lookup_key": row.get("punctuation_light_lookup_key", row.get("segmental_lookup_key")),
                    "lookup_normalization": row.get("lookup_normalization"),
                    "fallback_status": row["fallback_status"],
                    "evidence_counts": row["evidence_counts"],
                    "source_ids": row["source_ids"],
                })
            unresolved_tokens = [tokens[i] for i in unresolved_indexes]
            unique_unresolved.update(unresolved_tokens)
            rows.append({
                "line_no": line_no,
                "surface_original": text,
                "analysis_status": result.get("analysis_status"),
                "primary_analysis_status": result.get("primary_analysis_status"),
                "adapter_version": result.get("current_adapter_version"),
                "token_count": result.get("token_count"),
                "primary_matched_token_count": result.get("matched_token_count"),
                "effective_evidence_token_count": result.get("effective_evidence_token_count"),
                "effective_evidence_coverage_ratio": result.get("effective_evidence_coverage_ratio"),
                "fallback_attested_token_indexes": result.get("supplemental_exact_attested_token_indexes"),
                "unresolved_token_indexes": unresolved_indexes,
                "unresolved_tokens": unresolved_tokens,
                "fallback": fallback,
                "surface_preserved": result.get("surface_original") == text,
            })

        print(json.dumps({
            "probe_id": "REAL_TEXT_PROBE_002_AFTER_V0_35_2",
            "status": "EXPERIMENTAL_NON_AUTHORITATIVE_REAL_TEXT_ANALYSIS",
            "input_normalization": "NONE",
            "line_count": len(lines),
            "cor001_used": False,
            "benchmark_use": False,
            "rule_discovery_from_probe": False,
            "lines": rows,
            "aggregate": {
                "unique_unresolved_tokens_exact_as_input": sorted(unique_unresolved),
                "unique_unresolved_token_count": len(unique_unresolved),
                "all_surfaces_preserved": all(row["surface_preserved"] for row in rows),
            },
        }, ensure_ascii=False, indent=2, sort_keys=True))
    finally:
        analyzer.close()


if __name__ == "__main__":
    main()
