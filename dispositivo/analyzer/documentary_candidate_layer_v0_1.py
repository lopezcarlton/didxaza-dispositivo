#!/usr/bin/env python3
"""Constrained non-exact documentary candidate retrieval.

This module implements a small part of the candidate architecture already
specified for Biyubi/cross-source work:

    EXACT_SURFACE_MATCH != ORTHOGRAPHIC_VARIANT_CANDIDATE

It does NOT use edit distance, fuzzy ranking, tone stripping, PDLMA projection,
or generated morphology. It only looks for source surfaces reachable by one of
these explicitly enumerated candidate operations:

- final glottal/apostrophe presence vs absence;
- one adjacent identical-vowel length difference.

Apostrophe codepoints are canonicalized only to make candidate lookup possible;
that comparison operation is exposed in the result and never becomes a source
or normalized surface.
"""

from __future__ import annotations

import json
import re
import unicodedata
from collections import defaultdict
from typing import Any

MAX_CANDIDATES_PER_TOKEN = 20
STATUS_ORTHOGRAPHIC = "ORTHOGRAPHIC_VARIANT_CANDIDATE"
STATUS_NONE = "NO_CONSTRAINED_DOCUMENTARY_CANDIDATE"

_APOSTROPHES = "'’ꞌʼ‘`ʼ"
_OUTER_PUNCTUATION = ".,;:!?¿¡\"“”«»()[]{}…"
_VOWELS = set("aeiouáéíóúàèìòùäëïöüâêîôû")


def _strip_outer_punctuation(value: str) -> str:
    return str(value or "").strip().strip(_OUTER_PUNCTUATION).strip()


def candidate_relation_key(value: str) -> str:
    """Candidate-only key; preserves letters/diacritics and glottal presence."""

    text = unicodedata.normalize("NFC", _strip_outer_punctuation(value)).casefold()
    return "".join("'" if ch in _APOSTROPHES else ch for ch in text)


def _single_token(value: str) -> bool:
    text = _strip_outer_punctuation(value)
    return bool(text) and not re.search(r"\s", text)


def constrained_variant_keys(raw_token: str) -> dict[str, dict[str, Any]]:
    """Generate only explicitly licensed candidate search keys.

    Returned keys are not normalized outputs and never license correction.
    """

    key = candidate_relation_key(raw_token)
    out: dict[str, dict[str, Any]] = {}
    if not key:
        return out

    # Saltillo/glottal presence candidate.
    if key.endswith("'"):
        variant = key[:-1]
        if variant:
            out[variant] = {
                "operation": "FINAL_GLOTTAL_MARK_DELETION_CANDIDATE",
                "dimension": "SALTILLO",
            }
    else:
        out[key + "'"] = {
            "operation": "FINAL_GLOTTAL_MARK_INSERTION_CANDIDATE",
            "dimension": "SALTILLO",
        }

    # Exactly one adjacent identical-vowel difference. This is not generic
    # edit distance: no consonant substitution/deletion/insertion is allowed.
    chars = list(key)
    for i, ch in enumerate(chars):
        if ch not in _VOWELS:
            continue
        doubled = key[: i + 1] + ch + key[i + 1 :]
        if doubled != key:
            out.setdefault(
                doubled,
                {
                    "operation": "SINGLE_VOWEL_LENGTH_EXPANSION_CANDIDATE",
                    "dimension": "VOWEL_LENGTH",
                    "vowel": ch,
                    "position": i,
                },
            )
        if i + 1 < len(chars) and chars[i + 1] == ch:
            collapsed = key[:i] + key[i + 1 :]
            if collapsed != key:
                out.setdefault(
                    collapsed,
                    {
                        "operation": "SINGLE_VOWEL_LENGTH_COLLAPSE_CANDIDATE",
                        "dimension": "VOWEL_LENGTH",
                        "vowel": ch,
                        "position": i,
                    },
                )

    out.pop(key, None)
    return out


class DocumentaryCandidateIndex:
    """Candidate-only index over Pickett and optionally controlled Biyubi."""

    def __init__(self, db: Any, biyubi_source: Any | None = None):
        self.db = db
        self.biyubi_source = biyubi_source
        self._by_key: dict[str, list[dict[str, Any]]] = defaultdict(list)
        self._build_pickett_index()
        self._build_biyubi_index()

    def _add(self, surface_raw: str, record: dict[str, Any]) -> None:
        if not _single_token(surface_raw):
            return
        key = candidate_relation_key(surface_raw)
        if not key:
            return
        self._by_key[key].append({"source_surface_raw": surface_raw, **record})

    def _build_pickett_index(self) -> None:
        rows = self.db.execute(
            "select record_id,headword_raw_2007,surface_2013_reconciled,"
            "primary_surface_2013_reconciled,variants_json,source_id,gloss_es,"
            "source_edition_extracted,reconciliation_status "
            "from pickett_lexical_record_v0211"
        )
        for row in rows:
            values = [row[1], row[2], row[3]]
            try:
                variants = json.loads(row[4] or "[]")
                if isinstance(variants, list):
                    values.extend(str(v) for v in variants)
            except Exception:
                pass
            seen: set[str] = set()
            for value in values:
                raw = str(value or "").strip()
                if not raw or raw in seen:
                    continue
                seen.add(raw)
                self._add(
                    raw,
                    {
                        "source_layer": "PICKETT_LEXICAL_RECORD",
                        "source_id": row[5],
                        "source_locator": row[0],
                        "gloss_es": row[6],
                        "source_edition": row[7],
                        "reconciliation_status": row[8],
                    },
                )

    def _build_biyubi_index(self) -> None:
        if self.biyubi_source is None:
            return
        for record in self.biyubi_source.rows:
            entry = str(record.get("didxaza_raw", "") or "").strip()
            if not entry:
                continue
            common = {
                "source_id": "SRC-BIYUBI-DICCIONARIO-DIDXAZA-ESPANOL",
                "source_locator": f"BIYUBI:{record['source_row']}",
                "gloss_es": record.get("spanish_gloss", ""),
                "source_snapshot_sha256": self.biyubi_source.snapshot_sha256,
            }
            if _single_token(entry):
                self._add(entry, {"source_layer": "BIYUBI_FULL_ENTRY", **common})
            for raw_token in entry.split():
                token = _strip_outer_punctuation(raw_token)
                if token:
                    self._add(token, {"source_layer": "BIYUBI_TOKEN_ATTESTATION", **common})

    def lookup(self, raw_token: str) -> dict[str, Any]:
        variants = constrained_variant_keys(raw_token)
        candidates: list[dict[str, Any]] = []
        seen: set[tuple[str, str, str, str]] = set()

        for variant_key, operation in variants.items():
            for record in self._by_key.get(variant_key, []):
                dedupe = (
                    str(record.get("source_id", "")),
                    str(record.get("source_locator", "")),
                    str(record.get("source_surface_raw", "")),
                    operation["operation"],
                )
                if dedupe in seen:
                    continue
                seen.add(dedupe)
                candidates.append(
                    {
                        "candidate_status": STATUS_ORTHOGRAPHIC,
                        "query_token_raw": raw_token,
                        "query_candidate_key": candidate_relation_key(raw_token),
                        "source_candidate_key": variant_key,
                        "relation_operation": operation,
                        "candidate_comparison_basis": (
                            "NFC_CASEFOLD_OUTER_PUNCTUATION_LIGHT_"
                            "APOSTROPHE_CODEPOINT_CANONICALIZATION_CANDIDATE_ONLY"
                        ),
                        **record,
                        "exact_surface_match_assertion": False,
                        "semantic_equivalence_assertion": False,
                        "correction_assertion": False,
                        "orthographic_authority_assertion": False,
                        "generation_license_assertion": False,
                        "rule_discovery_assertion": False,
                    }
                )
                if len(candidates) >= MAX_CANDIDATES_PER_TOKEN:
                    break
            if len(candidates) >= MAX_CANDIDATES_PER_TOKEN:
                break

        return {
            "query_token_raw": raw_token,
            "candidate_status": STATUS_ORTHOGRAPHIC if candidates else STATUS_NONE,
            "candidate_count": len(candidates),
            "candidates": candidates,
            "candidate_rows_capped": MAX_CANDIDATES_PER_TOKEN,
            "policy": {
                "generic_edit_distance": False,
                "near_match_ranking": False,
                "tone_stripping": False,
                "pdlma_to_surface": False,
                "candidate_is_exact_evidence": False,
                "candidate_can_promote_coverage": False,
                "candidate_can_license_correction": False,
            },
        }
