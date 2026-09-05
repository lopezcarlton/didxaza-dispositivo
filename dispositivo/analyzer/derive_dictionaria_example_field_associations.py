#!/usr/bin/env python3
"""Inspect and derive documentary verb-form associations from pinned Dictionaria.

This script is intentionally source-first. It verifies one pinned upstream raw
SQLite snapshot and prints compact diagnostics needed to determine which
relations are actually populated before materializing any technical derivative.
No missing source relation is reconstructed by inference.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path
import sqlite3
import tempfile
from urllib.request import urlopen

DICTIONARIA_COMMIT = "76c22cf30c23d8f4bc5c83c11013a8cb24fe0f85"
RAW_SQLITE_GIT_BLOB_SHA1 = "4722551b56bb219c1cad354d1bfa9077d657aada"
RAW_SQLITE_SIZE = 9433088
RAW_SQLITE_URL = (
    "https://raw.githubusercontent.com/dictionaria/didxazageneral/"
    f"{DICTIONARIA_COMMIT}/raw/jzd.dictionaria.sqlite"
)

TAM_FIELD_IDS = {
    "HAB": "HABITUAL",
    "POT": "POTENTIAL",
    "CMP": "COMPLETIVE",
    "PRG": "PROGRESSIVE",
    "PRF": "PERFECT",
    "FUT": "FUTURE",
    "CTF": "COUNTERFACTUAL",
    "AND": "ANDATIVE",
}

FIELDS = [
    "example_id",
    "sense_id",
    "field_id",
    "tam_label",
    "dictionaria_commit",
    "raw_sqlite_git_blob_sha1",
]


def git_blob_sha1(payload: bytes) -> str:
    header = f"blob {len(payload)}\0".encode("ascii")
    return hashlib.sha1(header + payload).hexdigest()


def inspect_source(db: sqlite3.Connection) -> None:
    print("sense_field_example_schema=")
    for row in db.execute("PRAGMA table_info(sense_field_example)"):
        print(tuple(row))
    total = db.execute("SELECT COUNT(*) FROM sense_field_example").fetchone()[0]
    print(f"sense_field_example_rows={total}")

    for table in ("example", "sense_example", "textvalue"):
        print(f"{table}_schema=")
        for row in db.execute(f'PRAGMA table_info("{table}")'):
            print(tuple(row))
        count = db.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
        print(f"{table}_rows={count}")

    # The technical README documents example.text_id as the shared identity for
    # multiple transcriptions/translations in textvalue. Measure what this exact
    # snapshot actually contains before relying on it.
    paired_sql = """
        SELECT e.example_id,
               MAX(CASE WHEN tv.language_id='jz_ap' THEN tv.content END) AS ap,
               MAX(CASE WHEN tv.language_id='jz_pdlma' THEN tv.content END) AS pdlma,
               MAX(CASE WHEN tv.language_id='jz_pdlma_sur' THEN tv.content END) AS pdlma_sur
        FROM example e
        JOIN textvalue tv ON tv.text_id=e.text_id
        GROUP BY e.example_id
    """
    aggregates = list(db.execute(paired_sql))
    has_ap = [row for row in aggregates if row[1]]
    has_pdlma = [row for row in aggregates if row[2]]
    paired = [row for row in aggregates if row[1] and row[2]]
    paired_sur = [row for row in aggregates if row[1] and row[3]]
    print(f"examples_aggregated={len(aggregates)}")
    print(f"examples_with_jz_ap={len(has_ap)}")
    print(f"examples_with_jz_pdlma={len(has_pdlma)}")
    print(f"examples_with_ap_and_pdlma={len(paired)}")
    print(f"examples_with_ap_and_pdlma_sur={len(paired_sur)}")

    print("sample_ap_pdlma_pairs=")
    for example_id, ap, pdlma, pdlma_sur in paired[:12]:
        sense_ids = [
            str(row[0])
            for row in db.execute(
                "SELECT sense_id FROM sense_example WHERE example_id=? ORDER BY sense_id",
                (example_id,),
            )
        ]
        print(
            f"example_id={example_id!r} sense_ids={sense_ids!r} "
            f"AP={ap!r} PDLMA={pdlma!r} PDLMA_SUR={pdlma_sur!r}"
        )


def derive_empty_field_associations(sqlite_path: Path, output_path: Path) -> int:
    """Materialize only genuine sense_field_example TAM rows; currently diagnostic."""
    payload = sqlite_path.read_bytes()
    if len(payload) != RAW_SQLITE_SIZE:
        raise RuntimeError(
            f"Unexpected raw SQLite size: {len(payload)} != {RAW_SQLITE_SIZE}"
        )
    actual_blob = git_blob_sha1(payload)
    if actual_blob != RAW_SQLITE_GIT_BLOB_SHA1:
        raise RuntimeError(
            f"Unexpected raw SQLite Git blob: {actual_blob} != {RAW_SQLITE_GIT_BLOB_SHA1}"
        )

    placeholders = ",".join("?" for _ in TAM_FIELD_IDS)
    sql = (
        "SELECT DISTINCT example_id, sense_id, field_id "
        "FROM sense_field_example "
        f"WHERE field_id IN ({placeholders}) "
        "ORDER BY example_id, sense_id, field_id"
    )
    with sqlite3.connect(str(sqlite_path)) as db:
        inspect_source(db)
        rows = list(db.execute(sql, tuple(TAM_FIELD_IDS)))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for example_id, sense_id, field_id in rows:
            writer.writerow(
                {
                    "example_id": str(example_id),
                    "sense_id": str(sense_id),
                    "field_id": str(field_id),
                    "tam_label": TAM_FIELD_IDS[str(field_id)],
                    "dictionaria_commit": DICTIONARIA_COMMIT,
                    "raw_sqlite_git_blob_sha1": RAW_SQLITE_GIT_BLOB_SHA1,
                }
            )
    return len(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default=(
            Path(__file__).resolve().parent.parent
            / "sources"
            / "DICTIONARIA_EXAMPLE_FIELD_ASSOCIATIONS_v0_1.csv"
        ),
        type=Path,
    )
    parser.add_argument(
        "--sqlite",
        type=Path,
        help="Use an already-downloaded pinned SQLite instead of downloading it.",
    )
    args = parser.parse_args()

    if args.sqlite is not None:
        count = derive_empty_field_associations(args.sqlite, args.output)
    else:
        with tempfile.TemporaryDirectory() as tmp:
            sqlite_path = Path(tmp) / "jzd.dictionaria.sqlite"
            with urlopen(RAW_SQLITE_URL, timeout=120) as response:
                sqlite_path.write_bytes(response.read())
            count = derive_empty_field_associations(sqlite_path, args.output)

    print(f"derived_sense_field_example_tam_rows={count}")
    print(f"output={args.output}")
    print(f"dictionaria_commit={DICTIONARIA_COMMIT}")
    print(f"raw_sqlite_git_blob_sha1={RAW_SQLITE_GIT_BLOB_SHA1}")


if __name__ == "__main__":
    main()
