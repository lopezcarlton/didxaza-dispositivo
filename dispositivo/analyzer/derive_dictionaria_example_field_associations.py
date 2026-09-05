#!/usr/bin/env python3
"""Derive the missing Dictionaria example↔sense-field associations.

The public CLDF examples table keeps Primary_Text and Sense_IDs but the granular
`sense_field_example` relation from the upstream raw database is not materialized
in the exported ExampleTable. VerbAnalysisBridge v0.2 needs only the subset of
that relation whose field_id is an explicitly named TAM field.

This script downloads one pinned upstream raw SQLite snapshot, verifies its Git
blob identity, inspects the exact source schema for auditability, reads only
`sense_field_example`, and writes a compact CSV. The result is a technical
derivative, not a new linguistic authority.
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
    """Print only compact schema/value diagnostics needed to map field_id."""
    print("sense_field_example_schema=")
    for row in db.execute("PRAGMA table_info(sense_field_example)"):
        print(tuple(row))

    total = db.execute("SELECT COUNT(*) FROM sense_field_example").fetchone()[0]
    print(f"sense_field_example_rows={total}")
    print("sense_field_example_distinct_field_ids=")
    for field_id, count in db.execute(
        "SELECT field_id, COUNT(*) FROM sense_field_example "
        "GROUP BY field_id ORDER BY COUNT(*) DESC, field_id LIMIT 100"
    ):
        print(f"{field_id!r}\t{count}")

    print("tables_containing_field=")
    tables = [
        row[0]
        for row in db.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND lower(name) LIKE '%field%' ORDER BY name"
        )
    ]
    for table in tables:
        print(table)
        columns = list(db.execute(f'PRAGMA table_info("{table}")'))
        print("  columns=", [row[1] for row in columns])
        try:
            samples = list(db.execute(f'SELECT * FROM "{table}" LIMIT 5'))
        except sqlite3.DatabaseError as exc:
            print("  sample_error=", repr(exc))
        else:
            for sample in samples:
                print("  sample=", tuple(sample))


def derive(sqlite_path: Path, output_path: Path) -> int:
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
        count = derive(args.sqlite, args.output)
    else:
        with tempfile.TemporaryDirectory() as tmp:
            sqlite_path = Path(tmp) / "jzd.dictionaria.sqlite"
            with urlopen(RAW_SQLITE_URL, timeout=120) as response:
                sqlite_path.write_bytes(response.read())
            count = derive(sqlite_path, args.output)

    print(f"derived_rows={count}")
    print(f"output={args.output}")
    print(f"dictionaria_commit={DICTIONARIA_COMMIT}")
    print(f"raw_sqlite_git_blob_sha1={RAW_SQLITE_GIT_BLOB_SHA1}")


if __name__ == "__main__":
    main()
