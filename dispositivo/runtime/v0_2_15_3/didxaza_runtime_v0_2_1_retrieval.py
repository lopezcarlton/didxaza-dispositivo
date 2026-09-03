#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Didxazá runtime v0.2.1 — Retrieval.

Builds on v0.2.0 Foundation. Adds retrieval capabilities only:
- exact lexical retrieval over surface spans
- overlapping multiword span retrieval
- separate Headword vs PDLMA indexing
- source alternative grouping without destroying raw source variants
- Spanish co-occurrence heuristic with exact/prefix evidence separated
- source coverage metadata

Explicitly NOT implemented:
- morphology
- grammatical BOUND adjudication
- dialect resolution
- orthographic suggestions
- automatic correction
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from pathlib import Path
from collections import defaultdict
from typing import Any, Mapping, Optional, Sequence
import csv
import json
import re
import unicodedata

from didxaza_runtime_v0_2_0_foundation import (
    AUTO_CORRECT_ENABLED,
    ORTHOGRAPHIC_SUGGESTIONS_ENABLED,
    ContextProfile,
    InputSchemaError,
    InputValidator,
    NormalizedView,
    Span,
    build_run_manifest,
    make_normalized_view,
    normalize_apostrophes,
    strip_tone_marks,
)

RUNTIME_VERSION = "0.2.1"
RUNTIME_STAGE = "RETRIEVAL"
MORPHOLOGY_STATUS = "NOT_IMPLEMENTED"
BOUND_ANALYSIS_STATUS = "NOT_IMPLEMENTED"
DIALECT_RESOLUTION_STATUS = "NOT_IMPLEMENTED"

SPANISH_STOP = {
    "el","la","los","las","un","una","unos","unas","de","del","a","al","y","o","que","qué",
    "es","esta","está","este","esto","esa","ese","en","con","por","para","me","te","se","lo","le",
    "mi","mis","tu","tus","su","sus","yo","tú","él","ella","nos","muy","ya"
}

ANALYTIC_DECORATION = re.compile(r"[~=#*+.:()<>/&!]")


@dataclass(frozen=True)
class SourceCoverageProfile:
    source_id: str
    communities: tuple[str, ...]
    coverage_note: str
    representativeness: str


DICTIONARIA_COVERAGE = SourceCoverageProfile(
    source_id="BIB054_DICTIONARIA",
    communities=("LA_VENTOSA", "JUCHITAN", "SANTA_MARIA_XADANI"),
    coverage_note="Dictionaria represents La Ventosa, Juchitán and Santa María Xadani; documentation reports greater weight from La Ventosa.",
    representativeness="MULTI_COMMUNITY_UNEQUAL_COVERAGE",
)


@dataclass(frozen=True)
class LexicalEntry:
    entry_id: str
    raw_headword: str
    orthographic_index: Optional[str]
    pdlma_raw: str
    pdlma_index: Optional[str]
    part_of_speech: str
    attribution: str
    orthographic_index_status: str


@dataclass(frozen=True)
class SpanishRetrievalEvidence:
    exact_terms: tuple[str, ...]
    prefix_derived_terms: tuple[str, ...]

    @property
    def exact_score(self) -> int:
        return len(self.exact_terms)

    @property
    def prefix_score(self) -> int:
        return len(self.prefix_derived_terms)


@dataclass(frozen=True)
class SpanLexicalMatch:
    start: int
    end: int
    raw_span: str
    normalized_span: str
    entry_ids: tuple[str, ...]
    match_type: str = "EXACT_SEGMENTAL_SPAN_ATTESTATION"


@dataclass(frozen=True)
class RawAlternativeAttestation:
    raw_source_surface: str
    example_ids: tuple[str, ...]
    attributions: tuple[str, ...]


@dataclass(frozen=True)
class AlternativeGroup:
    segmental_index: str
    attestations: tuple[RawAlternativeAttestation, ...]
    retrieval_basis: str = "EXACT_ES_TRANSLATION_MATCH"


def spanish_norm(s: str) -> str:
    x = unicodedata.normalize("NFD", (s or "").lower())
    # This is Spanish-only retrieval normalization, not Didxazá orthographic normalization.
    x = "".join(c for c in x if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-zñ]+", " ", x).strip()


def spanish_terms(s: str) -> tuple[set[str], dict[str, str]]:
    """Return exact content terms and prefix->source mapping.

    Prefixes are explicitly derivative heuristics. They never count as a second
    independent exact match for the same source token.
    """
    exact = {
        t for t in spanish_norm(s).split()
        if len(t) >= 3 and t not in SPANISH_STOP
    }
    prefixes = {t[:5]: t for t in exact if len(t) >= 6}
    return exact, prefixes


def es_cooccurrence_overlap(sentence_es: str, glosses: Sequence[str]) -> SpanishRetrievalEvidence:
    sent_exact, sent_prefix = spanish_terms(sentence_es)
    gloss_exact: set[str] = set()
    gloss_prefix: dict[str, str] = {}
    for gloss in glosses:
        e, p = spanish_terms(gloss)
        gloss_exact |= e
        gloss_prefix.update(p)

    exact_overlap = sent_exact & gloss_exact

    # Prefix overlap only counts when it is not merely the shadow of an exact
    # overlap of the same source word on both sides.
    prefix_overlap: set[str] = set()
    for pref in set(sent_prefix) & set(gloss_prefix):
        sent_word = sent_prefix[pref]
        gloss_word = gloss_prefix[pref]
        if sent_word == gloss_word and sent_word in exact_overlap:
            continue
        prefix_overlap.add(pref)

    return SpanishRetrievalEvidence(
        exact_terms=tuple(sorted(exact_overlap)),
        prefix_derived_terms=tuple(sorted(prefix_overlap)),
    )


def segmental_index(s: str) -> str:
    s = normalize_apostrophes(strip_tone_marks(s or "")).lower().strip()
    return re.sub(r"\s+", " ", s)


def punctuation_light_index(s: str) -> str:
    """Comparison-only phrase index; punctuation is ignored non-destructively."""
    s = segmental_index(s)
    return re.sub(r"[^\wñ' ]+", " ", s, flags=re.UNICODE).strip()


def orthographic_headword_index(raw_headword: str) -> tuple[Optional[str], str]:
    """Index only surface-like Headwords.

    Decorated/analytic headwords are retained in the entry model but are not
    silently converted into orthographic surfaces.
    """
    seg = segmental_index(raw_headword)
    if not seg:
        return None, "EMPTY_HEADWORD"
    if ANALYTIC_DECORATION.search(seg):
        return None, "ANALYTIC_DECORATION_BLOCKED_FROM_ORTHOGRAPHIC_INDEX"
    # Documentary Headwords may contain Latin letters beyond the AP inventory
    # (e.g. diaeresis in the source). Retrieval preserves these documentary
    # surfaces; it does not treat them as project-approved orthography.
    for ch in seg:
        if ch in {" ", "'"}:
            continue
        if unicodedata.category(ch) not in {"Ll", "Lu"}:
            return None, "NON_SURFACE_SYMBOLS_BLOCKED"
    return seg, "INDEXED"


def pdlma_analysis_index(pdlma: str) -> Optional[str]:
    """Preserve PDLMA as an analytical representation, never as orthography."""
    raw = (pdlma or "").strip()
    if not raw:
        return None
    return normalize_apostrophes(raw).lower()


class DictionariaLoader:
    ENTRY_REQUIRED = ("ID", "Headword", "Part_Of_Speech", "Attribution")
    SENSE_REQUIRED = ("ID", "Entry_ID")
    EXAMPLE_REQUIRED = ("ID", "Primary_Text", "Attribution")

    @staticmethod
    def _read_csv(path: str | Path, required: Sequence[str]) -> list[dict[str, str]]:
        path = Path(path)
        if not path.exists():
            raise InputSchemaError(f"Dictionaria file does not exist: {path}")
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                raise InputSchemaError(f"CSV has no header: {path}")
            missing = [c for c in required if c not in reader.fieldnames]
            if missing:
                raise InputSchemaError(
                    f"Missing required columns in {path.name}: {', '.join(missing)}"
                )
            return list(reader)

    @classmethod
    def load(cls, entries_csv: str | Path, senses_csv: str | Path, examples_csv: str | Path):
        return (
            cls._read_csv(entries_csv, cls.ENTRY_REQUIRED),
            cls._read_csv(senses_csv, cls.SENSE_REQUIRED),
            cls._read_csv(examples_csv, cls.EXAMPLE_REQUIRED),
        )


class RetrievalEngine:
    def __init__(self, entries_rows, senses_rows, examples_rows):
        self.entries: dict[str, LexicalEntry] = {}
        self.senses: dict[str, list[dict[str, str]]] = defaultdict(list)
        self.examples = list(examples_rows)
        self.by_orthographic_span: dict[str, list[str]] = defaultdict(list)
        self.by_pdlma_analysis: dict[str, list[str]] = defaultdict(list)
        self.examples_by_exact_es: dict[str, list[dict[str, str]]] = defaultdict(list)
        self.max_headword_tokens = 1

        for r in entries_rows:
            entry_id = r.get("ID", "")
            raw_headword = r.get("Headword", "")
            orth_idx, status = orthographic_headword_index(raw_headword)
            pdlma_raw = r.get("PDLMA", "") or ""
            pdlma_idx = pdlma_analysis_index(pdlma_raw)
            entry = LexicalEntry(
                entry_id=entry_id,
                raw_headword=raw_headword,
                orthographic_index=orth_idx,
                pdlma_raw=pdlma_raw,
                pdlma_index=pdlma_idx,
                part_of_speech=r.get("Part_Of_Speech", "") or "",
                attribution=r.get("Attribution", "") or "",
                orthographic_index_status=status,
            )
            self.entries[entry_id] = entry
            if orth_idx:
                self.by_orthographic_span[orth_idx].append(entry_id)
                self.max_headword_tokens = max(self.max_headword_tokens, len(orth_idx.split()))
            if pdlma_idx:
                self.by_pdlma_analysis[pdlma_idx].append(entry_id)

        for r in senses_rows:
            eid = r.get("Entry_ID", "")
            if eid in self.entries:
                self.senses[eid].append(r)

        for ex in self.examples:
            es = ex.get("alt_translation1", "") or ex.get("Translated_Text", "") or ""
            if es:
                self.examples_by_exact_es[spanish_norm(es)].append(ex)

    def glosses(self, entry_id: str) -> list[str]:
        return [
            s.get("alt_translation1", "") or s.get("Description", "") or ""
            for s in self.senses.get(entry_id, [])
        ]

    def span_matches(self, raw_text: str) -> tuple[SpanLexicalMatch, ...]:
        """Return all exact attested surface spans, including overlaps."""
        token_matches = list(re.finditer(r"\S+", raw_text or ""))
        found: list[SpanLexicalMatch] = []
        for i in range(len(token_matches)):
            for j in range(i, min(len(token_matches), i + self.max_headword_tokens)):
                start, end = token_matches[i].start(), token_matches[j].end()
                raw_span = raw_text[start:end]
                idx = punctuation_light_index(raw_span)
                ids = self.by_orthographic_span.get(idx, [])
                if ids:
                    found.append(SpanLexicalMatch(
                        start=start,
                        end=end,
                        raw_span=raw_span,
                        normalized_span=idx,
                        entry_ids=tuple(ids),
                    ))
        return tuple(found)

    def lexical_evidence_for_match(self, match: SpanLexicalMatch, sentence_es: str) -> dict[str, Any]:
        entries = []
        for eid in match.entry_ids:
            e = self.entries[eid]
            overlap = es_cooccurrence_overlap(sentence_es, self.glosses(eid))
            entries.append({
                "entry_id": eid,
                "raw_headword": e.raw_headword,
                "orthographic_index": e.orthographic_index,
                "pdlma_raw": e.pdlma_raw,
                "attribution": e.attribution,
                "part_of_speech": e.part_of_speech,
                "es_cooccurrence": asdict(overlap),
                "retrieval_interpretation": "SEGMENTAL_ATTESTATION_ONLY",
            })
        return {
            "span": {"start": match.start, "end": match.end, "raw": match.raw_span},
            "normalized_span": match.normalized_span,
            "match_type": match.match_type,
            "entries": entries,
        }

    def source_sentence_alternative_groups(self, sentence_es: str, original: str) -> tuple[AlternativeGroup, ...]:
        """Exact Spanish-translation retrieval only; grouped without raw-data loss."""
        by_segmental: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
        original_cmp = punctuation_light_index(original)
        for ex in self.examples_by_exact_es.get(spanish_norm(sentence_es), []):
            raw = (ex.get("Primary_Text", "") or "").strip()
            if not raw:
                continue
            seg = segmental_index(raw)
            if punctuation_light_index(raw) == original_cmp:
                continue
            raw_bucket = by_segmental[seg].setdefault(raw, {
                "example_ids": [],
                "attributions": [],
            })
            exid = ex.get("ID", "")
            if exid and exid not in raw_bucket["example_ids"]:
                raw_bucket["example_ids"].append(exid)
            att = ex.get("Attribution", "")
            if att and att not in raw_bucket["attributions"]:
                raw_bucket["attributions"].append(att)

        groups = []
        for seg in sorted(by_segmental):
            attestations = []
            for raw, meta in by_segmental[seg].items():
                attestations.append(RawAlternativeAttestation(
                    raw_source_surface=raw,
                    example_ids=tuple(meta["example_ids"]),
                    attributions=tuple(meta["attributions"]),
                ))
            groups.append(AlternativeGroup(
                segmental_index=seg,
                attestations=tuple(attestations),
            ))
        return tuple(groups)

    def analyze_row(self, row: Mapping[str, str], context: Optional[ContextProfile] = None) -> dict[str, Any]:
        original = row.get("Didxazá_original", "") or ""
        sentence_es = row.get("Español", "") or ""
        context = context or ContextProfile()
        matches = self.span_matches(original)
        span_evidence = [self.lexical_evidence_for_match(m, sentence_es) for m in matches]
        alternatives = self.source_sentence_alternative_groups(sentence_es, original)

        return {
            "ID": row.get("ID", ""),
            "Bloque": row.get("Bloque", ""),
            "Español": sentence_es,
            "didxaza_original": original,
            "didxaza_normalizado": original,
            "action": "NO_CHANGE",
            "runtime_version": RUNTIME_VERSION,
            "runtime_stage": RUNTIME_STAGE,
            "auto_correct_enabled": False,
            "orthographic_suggestions_enabled": False,
            "morphology_status": MORPHOLOGY_STATUS,
            "bound_analysis_status": BOUND_ANALYSIS_STATUS,
            "dialect_resolution_status": DIALECT_RESOLUTION_STATUS,
            "context_profile_json": json.dumps(asdict(context), ensure_ascii=False),
            "source_coverage_json": json.dumps(asdict(DICTIONARIA_COVERAGE), ensure_ascii=False),
            "lexical_span_match_count": len(matches),
            "lexical_span_evidence_json": json.dumps(span_evidence, ensure_ascii=False),
            "source_sentence_alternative_group_count": len(alternatives),
            "source_sentence_alternative_groups_json": json.dumps(
                [asdict(g) for g in alternatives], ensure_ascii=False
            ),
        }



OUTPUT_FIELDS = (
    "ID","Bloque","Español","didxaza_original","didxaza_normalizado","action",
    "runtime_version","runtime_stage","auto_correct_enabled","orthographic_suggestions_enabled",
    "morphology_status","bound_analysis_status","dialect_resolution_status",
    "context_profile_json","source_coverage_json","lexical_span_match_count",
    "lexical_span_evidence_json","source_sentence_alternative_group_count",
    "source_sentence_alternative_groups_json",
)


def run_retrieval(
    *,
    input_csv: str | Path,
    entries_csv: str | Path,
    senses_csv: str | Path,
    examples_csv: str | Path,
    output_csv: str | Path,
    manifest_json: str | Path,
    database_version: str = "2.4-retrieval",
) -> dict[str, Any]:
    """Execute v0.2.1 retrieval with reproducibility metadata.

    This runner remains NO_CHANGE-only and never enables suggestions/corrections.
    """
    rows, _ = InputValidator.validate_csv(input_csv)
    entries, senses, examples = DictionariaLoader.load(entries_csv, senses_csv, examples_csv)
    engine = RetrievalEngine(entries, senses, examples)
    out = [engine.analyze_row(row) for row in rows]

    output_csv = Path(output_csv)
    with output_csv.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(out)

    manifest = build_run_manifest(
        input_path=input_csv,
        source_paths={
            "dictionaria_entries": entries_csv,
            "dictionaria_senses": senses_csv,
            "dictionaria_examples": examples_csv,
        },
        source_versions={"Dictionaria": "input-provided"},
        database_version=database_version,
        config_version=RUNTIME_VERSION,
        heuristic_versions={"ES_COOCCURRENCE_PREFIX5": "0.2.1"},
        rule_registry_version="NOT_USED_BY_RETRIEVAL_V0_2_1",
    )
    # build_run_manifest records Foundation runtime version; override with the actual runner version.
    manifest_dict = asdict(manifest)
    manifest_dict["runtime_version"] = RUNTIME_VERSION
    manifest_dict["runtime_stage"] = RUNTIME_STAGE
    Path(manifest_json).write_text(
        json.dumps(manifest_dict, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    return {
        "rows": len(out),
        "actions": {"NO_CHANGE": len(out)},
        "span_matches": sum(int(r["lexical_span_match_count"]) for r in out),
        "alternative_groups": sum(int(r["source_sentence_alternative_group_count"]) for r in out),
        "runtime_version": RUNTIME_VERSION,
        "auto_correct_enabled": False,
        "orthographic_suggestions_enabled": False,
    }


def main() -> None:
    import argparse
    ap = argparse.ArgumentParser(description="Didxazá v0.2.1 retrieval-only runtime")
    ap.add_argument("--input", required=True)
    ap.add_argument("--entries", required=True)
    ap.add_argument("--senses", required=True)
    ap.add_argument("--examples", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--manifest", required=True)
    args = ap.parse_args()
    summary = run_retrieval(
        input_csv=args.input,
        entries_csv=args.entries,
        senses_csv=args.senses,
        examples_csv=args.examples,
        output_csv=args.output,
        manifest_json=args.manifest,
    )
    print(json.dumps(summary, ensure_ascii=False))

def retrieval_status() -> dict[str, Any]:
    return {
        "runtime_version": RUNTIME_VERSION,
        "stage": RUNTIME_STAGE,
        "auto_correct_enabled": False,
        "orthographic_suggestions_enabled": False,
        "morphology_status": MORPHOLOGY_STATUS,
        "bound_analysis_status": BOUND_ANALYSIS_STATUS,
        "dialect_resolution_status": DIALECT_RESOLUTION_STATUS,
        "multiword_surface_retrieval": "IMPLEMENTED",
        "overlapping_span_retrieval": "IMPLEMENTED",
        "headword_pdlma_separation": "IMPLEMENTED",
        "alternative_grouping": "IMPLEMENTED",
        "es_cooccurrence_double_count_fix": "IMPLEMENTED",
    }


if __name__ == "__main__":
    main()
