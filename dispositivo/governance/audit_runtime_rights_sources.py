#!/usr/bin/env python3
"""Read-only provenance metadata audit for the current runtime SQLite.

This tool is intentionally narrow. It inventories table/column structure, row
counts, and source/provenance/attribution/origin/license metadata. It does not
emit lexical surfaces, glosses, examples, definitions, raw text, original
content, or other content fields.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DB = (
    ROOT
    / "dispositivo"
    / "runtime"
    / "v0_2_15_3"
    / "BASE_CORRECTOR_DIDXAZA_SURFACE_SEMANTICS_v2_20.sqlite"
)

# Match these as whole identifier tokens, never as arbitrary substrings.
# This is important because `origin` must not match content fields such as
# `didxaza_original`.
METADATA_TOKENS = {"source", "provenance", "attribution", "origin", "license"}
CONTENT_TOKENS = {
    "text",
    "raw",
    "surface",
    "gloss",
    "definition",
    "example",
    "sentence",
    "translation",
    "comment",
    "note",
    "payload",
    "original",
}
MAX_DISTINCT_SAMPLE = 40
MAX_VALUE_LENGTH = 240


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def quote_identifier(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def identifier_tokens(column_name: str) -> set[str]:
    return {
        token
        for token in re.split(r"[^a-z0-9]+", column_name.lower())
        if token
    }


def metadata_candidate(column_name: str) -> bool:
    tokens = identifier_tokens(column_name)
    return bool(tokens & METADATA_TOKENS) and not bool(tokens & CONTENT_TOKENS)


def normalize_value(value: Any) -> Any:
    if value is None or isinstance(value, (int, float)):
        return value
    text = str(value)
    if len(text) > MAX_VALUE_LENGTH:
        return text[:MAX_VALUE_LENGTH] + "…[truncated]"
    return text


def audit_database(path: Path) -> dict[str, Any]:
    path = path.resolve()
    if not path.is_file():
        raise FileNotFoundError(path)

    connection = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    try:
        integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
        table_names = [
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master "
                "WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
            )
        ]

        tables: list[dict[str, Any]] = []
        candidate_columns_total = 0
        selected_content_columns: list[str] = []
        for table_name in table_names:
            qtable = quote_identifier(table_name)
            row_count = int(connection.execute(f"SELECT COUNT(*) FROM {qtable}").fetchone()[0])
            columns = [
                {
                    "cid": row[0],
                    "name": row[1],
                    "type": row[2],
                    "notnull": bool(row[3]),
                    "pk": bool(row[5]),
                }
                for row in connection.execute(f"PRAGMA table_info({qtable})")
            ]

            provenance_columns: list[dict[str, Any]] = []
            for column in columns:
                name = str(column["name"])
                if not metadata_candidate(name):
                    continue
                tokens = identifier_tokens(name)
                if tokens & CONTENT_TOKENS:
                    selected_content_columns.append(f"{table_name}.{name}")
                    continue
                candidate_columns_total += 1
                qcol = quote_identifier(name)
                distinct_count = int(
                    connection.execute(
                        f"SELECT COUNT(DISTINCT {qcol}) FROM {qtable} WHERE {qcol} IS NOT NULL"
                    ).fetchone()[0]
                )
                rows = connection.execute(
                    f"SELECT DISTINCT {qcol} FROM {qtable} "
                    f"WHERE {qcol} IS NOT NULL ORDER BY CAST({qcol} AS TEXT) LIMIT ?",
                    (MAX_DISTINCT_SAMPLE,),
                ).fetchall()
                sample_is_complete = distinct_count <= MAX_DISTINCT_SAMPLE

                value_counts = None
                if sample_is_complete:
                    grouped_rows = connection.execute(
                        f"SELECT {qcol}, COUNT(*) FROM {qtable} "
                        f"WHERE {qcol} IS NOT NULL GROUP BY {qcol} "
                        f"ORDER BY CAST({qcol} AS TEXT)"
                    ).fetchall()
                    value_counts = [
                        {"value": normalize_value(value), "row_count": int(count)}
                        for value, count in grouped_rows
                    ]

                provenance_columns.append(
                    {
                        "name": name,
                        "declared_type": column["type"],
                        "distinct_non_null_count": distinct_count,
                        "sample_is_complete": sample_is_complete,
                        "sample_values": [normalize_value(row[0]) for row in rows],
                        "value_counts_if_complete": value_counts,
                    }
                )

            tables.append(
                {
                    "table": table_name,
                    "row_count": row_count,
                    "columns": [column["name"] for column in columns],
                    "provenance_metadata_columns": provenance_columns,
                }
            )

        if selected_content_columns:
            raise AssertionError(
                "Content-bearing columns reached provenance selection: "
                + ", ".join(selected_content_columns)
            )

        return {
            "status": "READ_ONLY_PROVENANCE_METADATA_AUDIT",
            "non_legal_determination": True,
            "content_fields_emitted": False,
            "selection_mode": "WHOLE_IDENTIFIER_TOKEN_MATCH",
            "database_path_from_repo_root": str(path.relative_to(ROOT)),
            "database_sha256": sha256(path),
            "sqlite_integrity_check": integrity,
            "table_count": len(table_names),
            "provenance_metadata_column_count": candidate_columns_total,
            "metadata_tokens": sorted(METADATA_TOKENS),
            "excluded_content_tokens": sorted(CONTENT_TOKENS),
            "value_count_policy": (
                "EXACT_COUNTS_EMITTED_ONLY_WHEN_DISTINCT_NON_NULL_COUNT_LE_40"
            ),
            "tables": tables,
        }
    finally:
        connection.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = audit_database(args.db)
    rendered = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
