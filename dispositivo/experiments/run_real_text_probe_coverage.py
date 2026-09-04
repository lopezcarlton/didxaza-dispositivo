#!/usr/bin/env python3
from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ANALYZER_DIR = HERE.parent / "analyzer"
RUNTIME_DIR = HERE.parent / "runtime" / "v0_2_15_3"
sys.path.insert(0, str(ANALYZER_DIR))
sys.path.insert(0, str(RUNTIME_DIR))

from analyzer_v0_35_migrated_adapter import build_migrated_analyzer  # noqa: E402
from didxaza_runtime_v0_2_1_retrieval import segmental_index  # noqa: E402

INPUT = HERE / "REAL_TEXT_PROBE_001.txt"
DB = RUNTIME_DIR / "BASE_CORRECTOR_DIDXAZA_SURFACE_SEMANTICS_v2_20.sqlite"


def qident(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def main() -> None:
    lines = [line for line in INPUT.read_text(encoding="utf-8").splitlines() if line.strip()]
    analyzer = build_migrated_analyzer()
    conn = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    try:
        out = []
        for line_no, line in enumerate(lines, 1):
            result = analyzer.analyze(line, item_id=f"REAL_TEXT_PROBE_001_L{line_no:02d}")
            tokens = line.split()
            matched = set(result.get("matched_token_indexes", []))
            for idx, token in enumerate(tokens):
                if idx in matched:
                    continue
                key = segmental_index(token)
                evidence = {
                    "surface_attestation_v029": [],
                    "cross_source_exact_surface_v0212": [],
                    "documentary_alignment_v0210": [],
                    "pickett_lexical_record_v0211": [],
                }

                for row in conn.execute(
                    "select source_kind,source_id,entry_id,example_id from surface_attestation_v029 where surface_key=? order by source_kind,entry_id,example_id limit 50",
                    (key,),
                ):
                    evidence["surface_attestation_v029"].append({
                        "source_kind": row[0], "source_id": row[1], "entry_id": row[2], "example_id": row[3]
                    })

                for row in conn.execute(
                    "select surface_key,pickett_record_ids_json,dictionaria_refs_json,source_ids_json from cross_source_exact_surface_v0212 where surface_key=?",
                    (key,),
                ):
                    evidence["cross_source_exact_surface_v0212"].append({
                        "surface_key": row[0],
                        "pickett_record_ids_json": row[1],
                        "dictionaria_refs_json": row[2],
                        "source_ids_json": row[3],
                    })

                for row in conn.execute(
                    "select alignment_id,analysis_type,analysis_value,source_id,source_location,status from documentary_alignment_v0210 where surface_key=? order by alignment_id",
                    (key,),
                ):
                    evidence["documentary_alignment_v0210"].append({
                        "alignment_id": row[0], "analysis_type": row[1], "analysis_value": row[2],
                        "source_id": row[3], "source_location": row[4], "status": row[5]
                    })

                for row in conn.execute(
                    "select record_id,headword_raw_2007,surface_2013_reconciled,primary_surface_2013_reconciled,variants_json,source_id,source_edition_extracted,reconciliation_status from pickett_lexical_record_v0211"
                ):
                    candidate_values = [row[1], row[2], row[3]]
                    try:
                        candidate_values.extend(json.loads(row[4] or "[]"))
                    except Exception:
                        pass
                    if any(segmental_index(str(v or "")) == key for v in candidate_values):
                        evidence["pickett_lexical_record_v0211"].append({
                            "record_id": row[0],
                            "headword_raw_2007": row[1],
                            "surface_2013_reconciled": row[2],
                            "primary_surface_2013_reconciled": row[3],
                            "source_id": row[5],
                            "source_edition_extracted": row[6],
                            "reconciliation_status": row[7],
                        })

                out.append({
                    "line": line_no,
                    "token_index": idx,
                    "token_exact": token,
                    "segmental_lookup_key": key,
                    "evidence": evidence,
                    "evidence_counts": {name: len(rows) for name, rows in evidence.items()},
                })

        payload = {
            "probe_id": "REAL_TEXT_PROBE_001_COVERAGE_DIAGNOSTIC",
            "mode": "READ_ONLY_EXISTING_LAYER_COVERAGE_FOR_UNMATCHED_TOKENS",
            "cor001_used": False,
            "rule_discovery": False,
            "items": out,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    finally:
        conn.close()
        analyzer.close()


if __name__ == "__main__":
    main()
