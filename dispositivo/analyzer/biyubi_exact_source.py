#!/usr/bin/env python3
"""Controlled Biyubi source loader and exact orthographic-token lookup.

The raw Biyubi workbook is a controlled external source and is intentionally not
stored in this public repository. This module reads the exact registered
snapshot when mounted, preserves tones/diacritics/apostrophes, and distinguishes
a complete entry match from an exact token attestation inside a longer entry.

It is evidence retrieval only: Biyubi does not grant orthographic, correction,
generation, or research authority.
"""

from __future__ import annotations

import hashlib
import re
import unicodedata
import zipfile
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

SOURCE_ID = "SRC-BIYUBI-DICCIONARIO-DIDXAZA-ESPANOL"
EXPECTED_SNAPSHOT_SHA256 = "53a01c4661e465930289ff042a2def58627ab8fc26d0b812feb65b47714e3b75"
EXPECTED_NONEMPTY_ROWS = 23601
SOURCE_ENV_VAR = "DIDXAZA_BIYUBI_XLSX"
MAX_EVIDENCE_ROWS = 20

STATUS_EXACT_ENTRY = "BIYUBI_EXACT_ENTRY"
STATUS_EXACT_TOKEN = "BIYUBI_EXACT_TOKEN_ATTESTATION"
STATUS_NO_EXACT = "BIYUBI_NO_EXACT_EVIDENCE"

_OUTER_PUNCTUATION = ".,;:!?¿¡\"“”«»()[]{}…"
_MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
_REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
_PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def exact_token_key(value: str) -> str:
    """Build exact comparison key without stripping linguistic marks.

    Only external sentence punctuation and case are ignored. Apostrophes are
    deliberately excluded from punctuation stripping because they are
    linguistically meaningful in the source forms.
    """

    text = unicodedata.normalize("NFC", str(value or "").strip())
    text = text.strip(_OUTER_PUNCTUATION).strip()
    return text.casefold()


def tokenize_entry(value: str) -> list[str]:
    return [key for part in str(value or "").split() if (key := exact_token_key(part))]


def _cell_column(cell_ref: str) -> str:
    match = re.match(r"[A-Z]+", cell_ref or "")
    return match.group(0) if match else ""


def _read_shared_strings(archive: zipfile.ZipFile) -> list[str]:
    try:
        root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
    except KeyError:
        return []
    strings: list[str] = []
    ns = f"{{{_MAIN_NS}}}"
    for si in root.findall(f"{ns}si"):
        parts = [node.text or "" for node in si.iter(f"{ns}t")]
        strings.append("".join(parts))
    return strings


def _first_worksheet_path(archive: zipfile.ZipFile) -> str:
    ns = {"m": _MAIN_NS, "r": _REL_NS, "p": _PKG_REL_NS}
    workbook = ET.fromstring(archive.read("xl/workbook.xml"))
    sheet = workbook.find("m:sheets/m:sheet", ns)
    if sheet is None:
        raise ValueError("Biyubi workbook contains no worksheet")
    rel_id = sheet.attrib[f"{{{_REL_NS}}}id"]

    rels = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
    target = None
    for rel in rels.findall("p:Relationship", ns):
        if rel.attrib.get("Id") == rel_id:
            target = rel.attrib.get("Target")
            break
    if not target:
        raise ValueError("Unable to resolve first worksheet relationship")
    target = target.lstrip("/")
    if not target.startswith("xl/"):
        target = "xl/" + target
    return target


def _read_cell_text(cell: ET.Element, shared: list[str]) -> str:
    ns = f"{{{_MAIN_NS}}}"
    cell_type = cell.attrib.get("t")
    if cell_type == "inlineStr":
        inline = cell.find(f"{ns}is")
        if inline is None:
            return ""
        return "".join(node.text or "" for node in inline.iter(f"{ns}t"))

    value = cell.find(f"{ns}v")
    if value is None:
        return ""
    raw = value.text or ""
    if cell_type == "s":
        return shared[int(raw)]
    return raw


def read_biyubi_rows(path: Path) -> list[dict[str, Any]]:
    """Read nonempty A/B rows from the first worksheet using stdlib only."""

    rows: list[dict[str, Any]] = []
    ns = f"{{{_MAIN_NS}}}"
    with zipfile.ZipFile(path) as archive:
        shared = _read_shared_strings(archive)
        sheet_path = _first_worksheet_path(archive)
        root = ET.fromstring(archive.read(sheet_path))
        for row in root.findall(f".//{ns}sheetData/{ns}row"):
            values: dict[str, str] = {}
            for cell in row.findall(f"{ns}c"):
                column = _cell_column(cell.attrib.get("r", ""))
                if column in {"A", "B"}:
                    values[column] = _read_cell_text(cell, shared)
            didxaza = values.get("A", "")
            spanish = values.get("B", "")
            if didxaza or spanish:
                rows.append(
                    {
                        "source_row": int(row.attrib.get("r", "0") or 0),
                        "didxaza_raw": didxaza,
                        "spanish_gloss": spanish,
                    }
                )
    return rows


class BiyubiControlledSource:
    """Exact evidence index over one controlled Biyubi workbook snapshot."""

    def __init__(self, path: str | Path, *, enforce_registered_snapshot: bool = True):
        self.path = Path(path)
        if not self.path.is_file():
            raise FileNotFoundError(self.path)
        self.snapshot_sha256 = sha256_file(self.path)
        if enforce_registered_snapshot and self.snapshot_sha256 != EXPECTED_SNAPSHOT_SHA256:
            raise ValueError(
                "Biyubi snapshot hash mismatch: "
                f"{self.snapshot_sha256} != {EXPECTED_SNAPSHOT_SHA256}"
            )

        rows = read_biyubi_rows(self.path)
        if enforce_registered_snapshot and len(rows) != EXPECTED_NONEMPTY_ROWS:
            raise ValueError(
                f"Biyubi nonempty row count mismatch: {len(rows)} != {EXPECTED_NONEMPTY_ROWS}"
            )
        self.rows = rows
        self._build_indexes()

    @classmethod
    def from_rows(
        cls,
        rows: Iterable[tuple[int, str, str] | dict[str, Any]],
        *,
        snapshot_sha256: str = "SYNTHETIC_TEST_SOURCE",
    ) -> "BiyubiControlledSource":
        obj = cls.__new__(cls)
        obj.path = None
        obj.snapshot_sha256 = snapshot_sha256
        normalized = []
        for item in rows:
            if isinstance(item, dict):
                normalized.append(
                    {
                        "source_row": int(item["source_row"]),
                        "didxaza_raw": str(item.get("didxaza_raw", "")),
                        "spanish_gloss": str(item.get("spanish_gloss", "")),
                    }
                )
            else:
                row_no, didxaza, spanish = item
                normalized.append(
                    {
                        "source_row": int(row_no),
                        "didxaza_raw": str(didxaza),
                        "spanish_gloss": str(spanish),
                    }
                )
        obj.rows = normalized
        obj._build_indexes()
        return obj

    def _build_indexes(self) -> None:
        self._entry_index: dict[str, list[dict[str, Any]]] = defaultdict(list)
        self._token_index: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for record in self.rows:
            raw = record["didxaza_raw"]
            entry_key = exact_token_key(raw)
            if entry_key:
                self._entry_index[entry_key].append(record)
            seen: set[str] = set()
            for token_key in tokenize_entry(raw):
                if token_key and token_key not in seen:
                    self._token_index[token_key].append(record)
                    seen.add(token_key)

    def lookup(self, raw_token: str) -> dict[str, Any]:
        key = exact_token_key(raw_token)
        entry_rows = list(self._entry_index.get(key, []))
        token_rows = list(self._token_index.get(key, []))
        if entry_rows:
            status = STATUS_EXACT_ENTRY
        elif token_rows:
            status = STATUS_EXACT_TOKEN
        else:
            status = STATUS_NO_EXACT

        def compact(record: dict[str, Any]) -> dict[str, Any]:
            return {
                "source_row": record["source_row"],
                "didxaza_raw": record["didxaza_raw"],
                "spanish_gloss": record["spanish_gloss"],
            }

        return {
            "source_id": SOURCE_ID,
            "source_snapshot_sha256": self.snapshot_sha256,
            "query_token_raw": raw_token,
            "exact_token_key": key,
            "biyubi_status": status,
            "exact_entry_count": len(entry_rows),
            "exact_token_attestation_count": len(token_rows),
            "exact_entry_evidence": [compact(x) for x in entry_rows[:MAX_EVIDENCE_ROWS]],
            "exact_token_attestation_evidence": [
                compact(x) for x in token_rows[:MAX_EVIDENCE_ROWS]
            ],
            "evidence_rows_capped": MAX_EVIDENCE_ROWS,
            "match_contract": {
                "unicode_normalization": "NFC_ONLY",
                "case_sensitive": False,
                "outer_sentence_punctuation_ignored": True,
                "tones_and_diacritics_preserved": True,
                "apostrophe_codepoints_preserved": True,
                "near_match": False,
                "strip_tone": False,
                "pdlma_to_surface": False,
            },
            "interpretation": (
                "SECONDARY_SURFACE_EVIDENCE_ONLY_NOT_ORTHOGRAPHIC_AUTHORITY"
                if status != STATUS_NO_EXACT
                else "NO_EXACT_BIYUBI_EVIDENCE_NOT_AN_INCORRECTNESS_CLAIM"
            ),
            "generation_license_assertion": False,
            "correction_assertion": False,
            "orthographic_authority_assertion": False,
            "rule_discovery_assertion": False,
        }
