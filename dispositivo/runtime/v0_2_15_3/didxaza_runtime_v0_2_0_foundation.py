#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Didxazá runtime v0.2.0 — Foundation.

Infrastructure only:
- data contracts
- input validation
- conservative Unicode comparison views
- original offset mapping
- reproducible run manifests

NO lexical retrieval changes.
NO morphology.
NO BOUND analysis.
NO orthographic suggestions.
NO automatic correction.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional, Sequence, Mapping, Any
import csv
import hashlib
import json
import unicodedata
import uuid
from datetime import datetime, timezone


RUNTIME_VERSION = "0.2.0"
RUNTIME_STAGE = "FOUNDATION"
AUTO_CORRECT_ENABLED = False
ORTHOGRAPHIC_SUGGESTIONS_ENABLED = False

APOSTROPHE_EQUIVALENTS = ("'", "’", "ʼ", "ꞌ")
TONE_COMBINING_MARKS = frozenset({"\u0300", "\u0301"})


class FoundationError(Exception):
    """Base class for structural Foundation failures."""


class InputSchemaError(FoundationError):
    pass


@dataclass(frozen=True)
class ContextProfile:
    speaker_id: Optional[str] = None
    community: str = "UNKNOWN"
    dialect_core: str = "UNKNOWN"
    dialect_membership: str = "UNKNOWN"
    membership_strength: str = "UNKNOWN"
    transition_status: str = "UNKNOWN"
    corpus_id: Optional[str] = None
    editorial_profile: Optional[str] = None
    production_context: Optional[str] = None
    age_group: Optional[str] = None
    literacy_language: Optional[str] = None


@dataclass(frozen=True)
class Span:
    start: int
    end: int
    text: str

    def __post_init__(self):
        if self.start < 0 or self.end < self.start:
            raise ValueError("Invalid span offsets")


@dataclass(frozen=True)
class OffsetRef:
    normalized_index: int
    original_start: int
    original_end: int


@dataclass(frozen=True)
class NormalizedView:
    raw_text: str
    nfc_text: str
    comparison_text: str
    segmental_view: str
    apostrophe_normalized_view: str
    original_offset_map: tuple[OffsetRef, ...]


@dataclass(frozen=True)
class EngineeringHeuristic:
    heuristic_id: str
    version: str
    purpose: str
    algorithm: str
    parameters: Mapping[str, Any] = field(default_factory=dict)
    known_limitations: tuple[str, ...] = ()
    test_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class LinguisticRule:
    rule_id: str
    phenomenon: str
    rule_kind: str
    source_id: str
    source_location: str
    input_conditions: Mapping[str, Any]
    context_requirements: Mapping[str, Any]
    dialect_scope: tuple[str, ...]
    analysis_operation: str
    possible_surface_operation: Optional[str]
    blocking_conditions: tuple[str, ...]
    status: str = "CURRENT"
    supersedes: tuple[str, ...] = ()


@dataclass(frozen=True)
class UnresolvedSpan:
    start_original: int
    end_original: int
    text: str
    reason_codes: tuple[str, ...]
    candidate_analysis_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class AnalysisResult:
    analyses: tuple[Mapping[str, Any], ...] = ()
    evidence_claims: tuple[Mapping[str, Any], ...] = ()
    unresolved_spans: tuple[UnresolvedSpan, ...] = ()
    module_warnings: tuple[str, ...] = ()


@dataclass(frozen=True)
class CandidateEdit:
    start_original: int
    end_original: int
    original: str
    replacement: str
    operation_type: str
    rule_ids: tuple[str, ...]
    evidence_claim_ids: tuple[str, ...]
    dialect_scope: tuple[str, ...]
    decision_status: str = "DISABLED_IN_V0_2_0"


@dataclass(frozen=True)
class RunManifest:
    run_id: str
    timestamp_utc: str
    runtime_version: str
    runtime_stage: str
    database_version: Optional[str]
    source_versions: Mapping[str, str]
    source_checksums: Mapping[str, str]
    input_checksum: Optional[str]
    config_version: str
    heuristic_versions: Mapping[str, str]
    rule_registry_version: str
    auto_correct_enabled: bool
    orthographic_suggestions_enabled: bool


def normalize_apostrophes(text: str) -> str:
    out = text or ""
    for c in APOSTROPHE_EQUIVALENTS[1:]:
        out = out.replace(c, "'")
    return out


def strip_tone_marks(text: str) -> str:
    """Remove only explicitly authorized tone marks; preserve all other marks."""
    decomposed = unicodedata.normalize("NFD", text or "")
    kept = "".join(ch for ch in decomposed if ch not in TONE_COMBINING_MARKS)
    return unicodedata.normalize("NFC", kept)


def _clusters_with_offsets(text: str):
    """Yield conservative base+combining clusters with original codepoint offsets."""
    if not text:
        return
    start = 0
    current = text[0]
    for i, ch in enumerate(text[1:], start=1):
        if unicodedata.combining(ch):
            current += ch
        else:
            yield start, i, current
            start = i
            current = ch
    yield start, len(text), current


def make_normalized_view(raw_text: str) -> NormalizedView:
    raw_text = raw_text or ""
    nfc_parts = []
    offset_refs = []
    norm_index = 0

    for start, end, cluster in _clusters_with_offsets(raw_text) or ():
        normalized_cluster = unicodedata.normalize("NFC", cluster)
        nfc_parts.append(normalized_cluster)
        for _ in normalized_cluster:
            offset_refs.append(OffsetRef(norm_index, start, end))
            norm_index += 1

    nfc_text = "".join(nfc_parts)
    apostrophe_view = normalize_apostrophes(nfc_text)
    segmental = strip_tone_marks(apostrophe_view).lower()

    return NormalizedView(
        raw_text=raw_text,
        nfc_text=nfc_text,
        comparison_text=apostrophe_view.lower(),
        segmental_view=segmental,
        apostrophe_normalized_view=apostrophe_view,
        original_offset_map=tuple(offset_refs),
    )



def normalized_span_to_original(view: NormalizedView, start: int, end: int) -> tuple[int, int]:
    """Map a half-open span in nfc_text back to raw_text codepoint offsets.

    The mapping is conservative: if a normalized codepoint represents a base +
    combining cluster in the original, the returned span covers the full cluster.
    """
    if start < 0 or end < start or end > len(view.nfc_text):
        raise ValueError("Invalid normalized span")
    if start == end:
        if start == len(view.nfc_text):
            return len(view.raw_text), len(view.raw_text)
        ref = view.original_offset_map[start]
        return ref.original_start, ref.original_start
    refs = view.original_offset_map[start:end]
    return min(r.original_start for r in refs), max(r.original_end for r in refs)

def candidate_whitespace_spans(raw_text: str, max_tokens: int = 4) -> tuple[Span, ...]:
    """Infrastructure-only span lattice over whitespace-delimited units.

    It intentionally returns overlapping spans. It does NOT claim that any span
    is a grammatical or orthographic word.
    """
    import re
    matches = list(re.finditer(r"\S+", raw_text or ""))
    spans = []
    for i in range(len(matches)):
        for j in range(i, min(len(matches), i + max_tokens)):
            start, end = matches[i].start(), matches[j].end()
            spans.append(Span(start, end, raw_text[start:end]))
    return tuple(spans)


class InputValidator:
    REQUIRED_COLUMNS = ("ID", "Bloque", "Español", "Didxazá_original")

    @classmethod
    def validate_csv(cls, path: str | Path) -> tuple[list[dict[str, str]], tuple[str, ...]]:
        path = Path(path)
        if not path.exists():
            raise InputSchemaError(f"Input file does not exist: {path}")
        try:
            with path.open("r", encoding="utf-8-sig", newline="") as f:
                reader = csv.DictReader(f)
                if reader.fieldnames is None:
                    raise InputSchemaError("CSV has no header")
                missing = [c for c in cls.REQUIRED_COLUMNS if c not in reader.fieldnames]
                if missing:
                    raise InputSchemaError(
                        "Missing required columns: " + ", ".join(missing)
                    )
                rows = list(reader)
                return rows, tuple(reader.fieldnames)
        except UnicodeDecodeError as e:
            raise InputSchemaError(f"Input is not valid UTF-8: {e}") from e


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def build_run_manifest(
    *,
    input_path: Optional[str | Path] = None,
    source_paths: Optional[Mapping[str, str | Path]] = None,
    source_versions: Optional[Mapping[str, str]] = None,
    database_version: Optional[str] = None,
    config_version: str = "0.2.0",
    heuristic_versions: Optional[Mapping[str, str]] = None,
    rule_registry_version: str = "NOT_IMPLEMENTED",
) -> RunManifest:
    source_paths = source_paths or {}
    checksums = {name: sha256_file(path) for name, path in source_paths.items()}
    return RunManifest(
        run_id=str(uuid.uuid4()),
        timestamp_utc=datetime.now(timezone.utc).isoformat(),
        runtime_version=RUNTIME_VERSION,
        runtime_stage=RUNTIME_STAGE,
        database_version=database_version,
        source_versions=dict(source_versions or {}),
        source_checksums=checksums,
        input_checksum=sha256_file(input_path) if input_path is not None else None,
        config_version=config_version,
        heuristic_versions=dict(heuristic_versions or {}),
        rule_registry_version=rule_registry_version,
        auto_correct_enabled=AUTO_CORRECT_ENABLED,
        orthographic_suggestions_enabled=ORTHOGRAPHIC_SUGGESTIONS_ENABLED,
    )


def write_manifest(manifest: RunManifest, path: str | Path) -> None:
    Path(path).write_text(
        json.dumps(asdict(manifest), ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def foundation_status() -> dict[str, Any]:
    return {
        "runtime_version": RUNTIME_VERSION,
        "stage": RUNTIME_STAGE,
        "auto_correct_enabled": AUTO_CORRECT_ENABLED,
        "orthographic_suggestions_enabled": ORTHOGRAPHIC_SUGGESTIONS_ENABLED,
        "morphology_status": "NOT_IMPLEMENTED",
        "bound_status": "NOT_IMPLEMENTED",
        "retrieval_v0_2_status": "NOT_IMPLEMENTED",
    }


def run_foundation(
    input_path: str | Path,
    output_path: str | Path,
    manifest_path: str | Path,
    *,
    context: Optional[ContextProfile] = None,
) -> dict[str, Any]:
    """Run Foundation infrastructure only.

    Produces structural views and candidate whitespace spans. It never performs
    lexical retrieval, morphology, BOUND adjudication, suggestions, or edits.
    A manifest is emitted for every successful run.
    """
    context = context or ContextProfile()
    rows, _ = InputValidator.validate_csv(input_path)
    output_path = Path(output_path)
    manifest_path = Path(manifest_path)

    with output_path.open("w", encoding="utf-8") as f:
        for row in rows:
            raw = row["Didxazá_original"]
            view = make_normalized_view(raw)
            spans = candidate_whitespace_spans(raw)
            record = {
                "ID": row["ID"],
                "Bloque": row["Bloque"],
                "Español": row["Español"],
                "didxaza_original": raw,
                "normalized_view": {
                    "nfc_text": view.nfc_text,
                    "comparison_text": view.comparison_text,
                    "segmental_view": view.segmental_view,
                    "apostrophe_normalized_view": view.apostrophe_normalized_view,
                },
                "candidate_spans": [asdict(x) for x in spans],
                "context_profile": asdict(context),
                "action": "NO_CHANGE",
                "auto_correct_enabled": False,
                "orthographic_suggestions_enabled": False,
                "morphology_status": "NOT_IMPLEMENTED",
                "bound_status": "NOT_IMPLEMENTED",
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    manifest = build_run_manifest(
        input_path=input_path,
        source_paths={},
        source_versions={},
        database_version="2.3-foundation",
        config_version="0.2.0",
        rule_registry_version="FOUNDATION_SCHEMA_ONLY",
    )
    write_manifest(manifest, manifest_path)
    return {
        "rows": len(rows),
        "output_path": str(output_path),
        "manifest_path": str(manifest_path),
        "auto_correct_enabled": False,
        "orthographic_suggestions_enabled": False,
    }
