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
from didxaza_runtime_v0_2_1_retrieval import punctuation_light_index  # noqa: E402

INPUT = HERE / "REAL_TEXT_PROBE_002.txt"


def compact_line(result: dict, line_no: int, text: str) -> dict:
    tokens = text.split()
    fallback = result.get("supplemental_exact_existing_layer_evidence", [])
    fallback_by_index = {row["token_index"]: row for row in fallback}
    unresolved_indexes = result.get("unresolved_token_indexes_after_exact_fallback", [])

    lexical = []
    for ev in result.get("lexical_span_evidence", []):
        lexical.append({
            "span": ev.get("span"),
            "normalized_span": ev.get("normalized_span"),
            "entry_ids": [e.get("entry_id") for e in ev.get("entries", [])],
            "headwords": [e.get("raw_headword") for e in ev.get("entries", [])],
        })

    morphology = []
    for row in result.get("morphology_i_documented_surface_analyses", []):
        morphology.append({
            "span": row.get("span"),
            "entry_id": row.get("entry_id"),
            "tam": row.get("tam"),
            "recognition_basis": row.get("recognition_basis"),
            "contextual_resolution_status": row.get("contextual_resolution_status"),
        })

    fallback_compact = []
    for row in fallback:
        fallback_compact.append({
            "token_index": row["token_index"],
            "token_raw": row["token_raw"],
            "segmental_lookup_key": row["segmental_lookup_key"],
            "fallback_status": row["fallback_status"],
            "evidence_counts": row["evidence_counts"],
            "source_ids": row["source_ids"],
        })

    punctuation_diagnostic = []
    analyzer = compact_line.analyzer
    for idx in unresolved_indexes:
        raw = tokens[idx]
        light = punctuation_light_index(raw)
        current = fallback_by_index.get(idx, {})
        current_key = current.get("segmental_lookup_key")
        if light and light != current_key:
            alt = analyzer._fallback_for_token(light, idx)  # diagnostic only; current Analyzer is not mutated
            punctuation_diagnostic.append({
                "token_index": idx,
                "token_raw": raw,
                "current_segmental_lookup_key": current_key,
                "punctuation_light_lookup_key": light,
                "punctuation_light_status": alt["fallback_status"],
                "punctuation_light_evidence_counts": alt["evidence_counts"],
                "punctuation_light_source_ids": alt["source_ids"],
            })

    return {
        "line_no": line_no,
        "surface_original": text,
        "analysis_status": result.get("analysis_status"),
        "primary_analysis_status": result.get("primary_analysis_status"),
        "token_count": result.get("token_count"),
        "primary_matched_token_count": result.get("matched_token_count"),
        "effective_evidence_token_count": result.get("effective_evidence_token_count"),
        "effective_evidence_coverage_ratio": result.get("effective_evidence_coverage_ratio"),
        "primary_matched_token_indexes": result.get("matched_token_indexes"),
        "fallback_attested_token_indexes": result.get("supplemental_exact_attested_token_indexes"),
        "unresolved_token_indexes": unresolved_indexes,
        "unresolved_tokens": [tokens[i] for i in unresolved_indexes],
        "lexical_evidence": lexical,
        "morphology_i": morphology,
        "fallback": fallback_compact,
        "punctuation_diagnostic_for_unresolved": punctuation_diagnostic,
    }


def main() -> None:
    lines = [line for line in INPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    analyzer = build_migrated_analyzer()
    compact_line.analyzer = analyzer
    try:
        rows = []
        unique_unresolved = set()
        punctuation_recoverable = set()
        for line_no, text in enumerate(lines, 1):
            result = analyzer.analyze(text, item_id=f"REAL_TEXT_PROBE_002_L{line_no:02d}")
            row = compact_line(result, line_no, text)
            rows.append(row)
            unique_unresolved.update(row["unresolved_tokens"])
            for diag in row["punctuation_diagnostic_for_unresolved"]:
                if diag["punctuation_light_status"] == "ATTESTED_OUTSIDE_PRIMARY_LEXICON":
                    punctuation_recoverable.add(diag["token_raw"])

        payload = {
            "probe_id": "REAL_TEXT_PROBE_002",
            "status": "EXPERIMENTAL_NON_AUTHORITATIVE_REAL_TEXT_ANALYSIS",
            "input_normalization": "NONE",
            "line_count": len(lines),
            "cor001_used": False,
            "benchmark_use": False,
            "rule_discovery_from_probe": False,
            "analyzer_adapter": "0.35.1",
            "lines": rows,
            "aggregate": {
                "unique_unresolved_tokens_exact_as_input": sorted(unique_unresolved),
                "unique_unresolved_token_count": len(unique_unresolved),
                "punctuation_light_recoverable_tokens": sorted(punctuation_recoverable),
            },
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    finally:
        analyzer.close()


if __name__ == "__main__":
    main()
