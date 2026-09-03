#!/usr/bin/env python3
"""Schema/provenance-only audit of stored COR001/replay artifacts.

This auditor is deliberately rights-oriented and non-linguistic. It records
file identity, structural schemas, record counts, and low-cardinality values
only for fields whose names explicitly denote provenance/rights metadata.
It never emits corpus sentences, didxazá surfaces, Spanish translations,
analysis outputs, corrections, metrics-by-item, or other content-bearing
values.

COR001 remains ANALYSIS_TARGET_ONLY. This tool must not be used to score,
validate, benchmark, regress, or discover linguistic rules from COR001.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "dispositivo" / "runtime" / "v0_2_15_3"

DEFAULT_ARTIFACTS = (
    "COR001_REPLAY_INPUT_v0_2_15_2.csv",
    "COR001_REPLAY_DETAILED_v0_2_15_2.jsonl",
    "COR001_REPLAY_METRICS_v0_2_15_2.json",
    "COR001_REPLAY_SUMMARY_v0_2_15_2.csv",
    "RUN_MANIFEST_COR001_v0_2_15_2.json",
    "CLEAN_REPLAY_VERIFICATION_v0_2_15_3.json",
)

METADATA_TOKENS = {
    "source",
    "sources",
    "provenance",
    "attribution",
    "origin",
    "license",
    "rights",
    "copyright",
    "author",
    "authors",
    "creator",
    "creators",
    "contributor",
    "contributors",
    "speaker",
    "speakers",
    "dataset",
    "corpus",
    "version",
    "sha256",
    "hash",
    "path",
    "file",
    "filename",
}

CONTENT_TOKENS = {
    "text",
    "raw",
    "surface",
    "didxaza",
    "spanish",
    "es",
    "translation",
    "gloss",
    "definition",
    "example",
    "sentence",
    "phrase",
    "utterance",
    "input",
    "output",
    "analysis",
    "detail",
    "expected",
    "observed",
    "suggestion",
    "correction",
    "original",
    "normalized",
    "value",
    "reason",
    "note",
    "comment",
}

MAX_DISTINCT_VALUES = 40
MAX_METADATA_VALUE_LENGTH = 240


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tokens(name: str) -> set[str]:
    return {token for token in re.split(r"[^a-z0-9]+", name.lower()) if token}


def safe_metadata_field(name: str) -> bool:
    field_tokens = tokens(name)
    return bool(field_tokens & METADATA_TOKENS) and not bool(field_tokens & CONTENT_TOKENS)


def content_bearing_field(name: str) -> bool:
    return bool(tokens(name) & CONTENT_TOKENS)


def normalize_metadata_value(value: Any) -> Any:
    if value is None or isinstance(value, (bool, int, float)):
        return value
    if isinstance(value, (list, tuple)):
        return [normalize_metadata_value(item) for item in value]
    if isinstance(value, dict):
        # Never emit arbitrary nested mappings as values. Only expose key names.
        return {"mapping_keys": sorted(str(key) for key in value.keys())}
    text = str(value)
    if len(text) > MAX_METADATA_VALUE_LENGTH:
        return text[:MAX_METADATA_VALUE_LENGTH] + "…[truncated]"
    return text


def file_base(path: Path, kind: str) -> dict[str, Any]:
    return {
        "file": str(path.relative_to(ROOT)),
        "format": kind,
        "byte_size": path.stat().st_size,
        "sha256": sha256(path),
    }


def finalize_scalar_counts(values: Iterable[Any]) -> dict[str, Any]:
    normalized = [json.dumps(normalize_metadata_value(v), ensure_ascii=False, sort_keys=True) for v in values if v is not None]
    counts = Counter(normalized)
    distinct = len(counts)
    result: dict[str, Any] = {
        "distinct_non_null_count": distinct,
        "counts_complete": distinct <= MAX_DISTINCT_VALUES,
    }
    if distinct <= MAX_DISTINCT_VALUES:
        result["value_counts"] = [
            {"value": json.loads(value), "row_count": count}
            for value, count in sorted(counts.items())
        ]
    return result


def audit_csv(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames or [])
        metadata_values: dict[str, list[Any]] = defaultdict(list)
        row_count = 0
        for row in reader:
            row_count += 1
            for field in fields:
                if safe_metadata_field(field):
                    metadata_values[field].append(row.get(field))

    result = file_base(path, "csv")
    result.update(
        {
            "record_count": row_count,
            "schema_fields": fields,
            "content_bearing_schema_fields": [f for f in fields if content_bearing_field(f)],
            "metadata_fields": {
                field: finalize_scalar_counts(values)
                for field, values in sorted(metadata_values.items())
            },
        }
    )
    return result


def audit_jsonl(path: Path) -> dict[str, Any]:
    fields: set[str] = set()
    metadata_values: dict[str, list[Any]] = defaultdict(list)
    row_count = 0
    non_object_rows = 0
    with path.open("r", encoding="utf-8-sig") as handle:
        for line in handle:
            if not line.strip():
                continue
            row_count += 1
            obj = json.loads(line)
            if not isinstance(obj, dict):
                non_object_rows += 1
                continue
            for key, value in obj.items():
                key = str(key)
                fields.add(key)
                if safe_metadata_field(key):
                    metadata_values[key].append(value)

    ordered_fields = sorted(fields)
    result = file_base(path, "jsonl")
    result.update(
        {
            "record_count": row_count,
            "non_object_record_count": non_object_rows,
            "schema_fields": ordered_fields,
            "content_bearing_schema_fields": [f for f in ordered_fields if content_bearing_field(f)],
            "metadata_fields": {
                field: finalize_scalar_counts(values)
                for field, values in sorted(metadata_values.items())
            },
        }
    )
    return result


def walk_json_schema(value: Any, path: tuple[str, ...], schema_paths: set[str], metadata: dict[str, list[Any]]) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            key = str(key)
            child_path = path + (key,)
            schema_paths.add(".".join(child_path))
            if safe_metadata_field(key) and not isinstance(child, (dict, list)):
                metadata[".".join(child_path)].append(child)
            walk_json_schema(child, child_path, schema_paths, metadata)
    elif isinstance(value, list):
        array_path = path + ("[]",)
        schema_paths.add(".".join(array_path))
        for child in value:
            walk_json_schema(child, array_path, schema_paths, metadata)


def audit_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    schema_paths: set[str] = set()
    metadata_values: dict[str, list[Any]] = defaultdict(list)
    walk_json_schema(value, (), schema_paths, metadata_values)
    ordered_paths = sorted(p for p in schema_paths if p)

    top_level_type = type(value).__name__
    top_level_count = len(value) if isinstance(value, (dict, list)) else 1
    result = file_base(path, "json")
    result.update(
        {
            "top_level_type": top_level_type,
            "top_level_item_count": top_level_count,
            "schema_paths": ordered_paths,
            "content_bearing_schema_paths": [
                p for p in ordered_paths if any(content_bearing_field(part) for part in p.split("."))
            ],
            "metadata_fields": {
                field: finalize_scalar_counts(values)
                for field, values in sorted(metadata_values.items())
            },
        }
    )
    return result


def audit_file(path: Path) -> dict[str, Any]:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return audit_csv(path)
    if suffix == ".jsonl":
        return audit_jsonl(path)
    if suffix == ".json":
        return audit_json(path)
    raise ValueError(f"Unsupported replay artifact format: {path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime", type=Path, default=RUNTIME)
    parser.add_argument("--artifact", action="append", dest="artifacts")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    runtime = args.runtime.resolve()
    names = tuple(args.artifacts or DEFAULT_ARTIFACTS)
    reports = []
    missing = []
    for name in names:
        path = runtime / name
        if not path.is_file():
            missing.append(name)
            continue
        reports.append(audit_file(path))

    result = {
        "status": "REPLAY_ARTIFACT_RIGHTS_SCHEMA_AUDIT",
        "non_legal_determination": True,
        "cor001_policy": "ANALYSIS_TARGET_ONLY",
        "benchmark_or_rule_discovery_use": False,
        "content_values_emitted": False,
        "metadata_value_policy": "VALUES_ONLY_FOR_EXPLICIT_RIGHTS_PROVENANCE_FIELDS_AND_ONLY_IF_LOW_CARDINALITY",
        "artifact_count": len(reports),
        "missing_artifacts": missing,
        "artifacts": reports,
    }

    rendered = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
