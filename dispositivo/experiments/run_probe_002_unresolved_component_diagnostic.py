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


def main() -> None:
    lines = [line for line in INPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    analyzer = build_migrated_analyzer()
    try:
        occurrences = []
        for line_no, text in enumerate(lines, 1):
            current = analyzer.analyze(text, item_id=f"PROBE002_COMPONENT_SCAN_L{line_no:02d}")
            tokens = text.split()
            for token_index in current.get("unresolved_token_indexes_after_exact_fallback", []):
                raw = tokens[token_index]
                comparison_surface = punctuation_light_index(raw)
                single = analyzer.base.analyze(
                    comparison_surface,
                    item_id=f"PROBE002_COMPONENT_SCAN_L{line_no:02d}_T{token_index:02d}",
                )
                component_counts = {
                    "lexical_span_evidence": len(single.get("lexical_span_evidence", [])),
                    "morphology_i_documented_surface_analyses": len(single.get("morphology_i_documented_surface_analyses", [])),
                    "whole_surface_bound_analyses": len(single.get("whole_surface_bound_analyses", [])),
                    "whole_surface_derivation_analyses": len(single.get("whole_surface_derivation_analyses", [])),
                    "whole_surface_causative_analyses": len(single.get("whole_surface_causative_analyses", [])),
                    "whole_surface_exact_person_possession": 1 if single.get("whole_surface_exact_person_possession") else 0,
                }
                evidence_present = any(component_counts.values())
                occurrences.append({
                    "line_no": line_no,
                    "token_index": token_index,
                    "token_raw": raw,
                    "comparison_surface": comparison_surface,
                    "single_token_historical_analysis_status": single.get("analysis_status"),
                    "component_counts": component_counts,
                    "existing_component_evidence_present": evidence_present,
                    "component_evidence": {
                        "morphology_i_documented_surface_analyses": single.get("morphology_i_documented_surface_analyses", []),
                        "whole_surface_bound_analyses": single.get("whole_surface_bound_analyses", []),
                        "whole_surface_derivation_analyses": single.get("whole_surface_derivation_analyses", []),
                        "whole_surface_causative_analyses": single.get("whole_surface_causative_analyses", []),
                        "whole_surface_exact_person_possession": single.get("whole_surface_exact_person_possession"),
                    },
                    "provisional_possession_prefix_candidate": single.get("provisional_possession_prefix_candidate"),
                    "interpretation": (
                        "EXISTING_COMPONENT_EVIDENCE_NOT_APPLIED_TOKENWISE_IN_MULTI_TOKEN_INPUT"
                        if evidence_present
                        else "NO_EXISTING_COMPONENT_EVIDENCE_FOUND_IN_V0_35_SINGLE_TOKEN_CHANNEL"
                    ),
                })

        dedup = {}
        for row in occurrences:
            key = row["comparison_surface"]
            bucket = dedup.setdefault(key, {
                "comparison_surface": key,
                "raw_forms": set(),
                "occurrence_count": 0,
                "existing_component_evidence_present": False,
                "component_counts_max": {},
            })
            bucket["raw_forms"].add(row["token_raw"])
            bucket["occurrence_count"] += 1
            bucket["existing_component_evidence_present"] = (
                bucket["existing_component_evidence_present"] or row["existing_component_evidence_present"]
            )
            for name, count in row["component_counts"].items():
                bucket["component_counts_max"][name] = max(
                    bucket["component_counts_max"].get(name, 0), count
                )

        unique = []
        for key in sorted(dedup):
            row = dedup[key]
            row["raw_forms"] = sorted(row["raw_forms"])
            unique.append(row)

        payload = {
            "probe_id": "REAL_TEXT_PROBE_002_UNRESOLVED_COMPONENT_DIAGNOSTIC",
            "mode": "READ_ONLY_EXISTING_COMPONENT_SINGLE_TOKEN_DIAGNOSTIC",
            "cor001_used": False,
            "benchmark_use": False,
            "rule_discovery": False,
            "occurrences": occurrences,
            "unique_surfaces": unique,
            "aggregate": {
                "unresolved_occurrence_count": len(occurrences),
                "unique_comparison_surface_count": len(unique),
                "unique_surfaces_with_existing_component_evidence": [
                    row["comparison_surface"] for row in unique
                    if row["existing_component_evidence_present"]
                ],
            },
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    finally:
        analyzer.close()


if __name__ == "__main__":
    main()
