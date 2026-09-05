#!/usr/bin/env python3
"""Exact documentary surface evidence derived from pinned Voces knowledge.

This loader consumes a small technical registry whose rows must already be
promoted in lopezcarlton/vocesdelasnubes. It does not discover rules or infer
surface forms from PDLMA, near matches, normalization beyond Unicode NFC, or
punctuation changes.
"""
from __future__ import annotations

import csv
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Any

SOURCE_REGISTRY_VERSION = "0.1"
STATUS_EXACT = "VOCES_DOCUMENTARY_EXACT_ATTESTATION"
STATUS_NO_EXACT = "NO_VOCES_DOCUMENTARY_EXACT_ATTESTATION"
REQUIRED_COLUMNS = {
    "surface_exact",
    "source_id",
    "source_location",
    "hall_id",
    "knowledge_commit",
    "evidence_type",
    "authority_scope",
}


def _nfc(value: str) -> str:
    return unicodedata.normalize("NFC", str(value or ""))


class VocesExactDocumentarySource:
    def __init__(self, registry_path: str | Path):
        self.registry_path = Path(registry_path)
        if not self.registry_path.is_file():
            raise FileNotFoundError(self.registry_path)

        by_surface: dict[str, list[dict[str, str]]] = defaultdict(list)
        with self.registry_path.open(encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
            if missing:
                raise ValueError(
                    f"Voces documentary registry missing columns: {sorted(missing)}"
                )
            for row_number, row in enumerate(reader, 2):
                surface = _nfc(row.get("surface_exact", ""))
                if not surface:
                    raise ValueError(f"Empty surface_exact at row {row_number}")
                if surface != row.get("surface_exact"):
                    raise ValueError(
                        f"surface_exact must be stored NFC-normalized at row {row_number}"
                    )
                record = {key: str(row.get(key, "")) for key in REQUIRED_COLUMNS}
                record["registry_row_number"] = str(row_number)
                by_surface[surface].append(record)
        self._by_surface = dict(by_surface)
        self.record_count = sum(len(rows) for rows in self._by_surface.values())

    def lookup(self, raw_surface: str) -> dict[str, Any]:
        query = _nfc(raw_surface)
        records = list(self._by_surface.get(query, []))
        return {
            "voces_documentary_status": STATUS_EXACT if records else STATUS_NO_EXACT,
            "query_surface_nfc": query,
            "exact_records": records,
            "exact_record_count": len(records),
            "registry_version": SOURCE_REGISTRY_VERSION,
            "match_policy": {
                "unicode_nfc_only": True,
                "casefold": False,
                "punctuation_stripping": False,
                "tone_stripping": False,
                "diacritic_stripping": False,
                "apostrophe_normalization": False,
                "near_match": False,
                "pdlma_to_surface": False,
            },
            "interpretation": (
                "DOCUMENTARY_SURFACE_ATTESTATION_ONLY_NOT_MORPHOLOGICAL_ANALYSIS"
                if records
                else "NO_EXACT_PROMOTED_DOCUMENTARY_SURFACE_ATTESTATION"
            ),
            "correction_assertion": False,
            "orthographic_authority_assertion": False,
            "generation_license_assertion": False,
            "rule_discovery_assertion": False,
        }
