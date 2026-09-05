#!/usr/bin/env python3
"""Analyzer v0.35.10 — documentary candidates for non-headword verb forms.

This wrapper extends VerbAnalysisBridge v0.1 without changing exact-evidence
metrics or promoting a token to a resolved morphological analysis.

For a token that lacks an already documented exact verb-headword analysis (and
has not been resolved by the separately licensed person-fusion rule), it may
surface a *research candidate* when all of the following are true:

1. the token is exactly attested in a Dictionaria AP Primary_Text example under
   a strict documentary key (NFC + case + apostrophe typography only);
2. the pinned upstream `sense_field_example` relation associates that example
   through a TAM field with exactly one verb entry in the 2,385-record inventory;
3. the TAM field is explicit: HAB/POT/CMP/PRG/PRF/FUT/CTF/AND.

The granular example↔sense-field relation is loaded from the static technical
registry derived by `derive_dictionaria_example_field_associations.py`.  The
public CLDF ExampleTable itself does not retain this granular field association.

The candidate exposes the compatible verb entry, class, analytical root/citation
and PDLMA paradigm coordinates for the TAM labels associated with the example.
It does NOT assert that the observed token is necessarily the verb in that
sentence, does NOT assert the TAM of the observed token, does NOT map PDLMA to
Alfabeto Popular, and does NOT license correction or generation.

This implements the recovery-coordinate use allowed by Voces HALL-0073,
HALL-0074 and HALL-0076 while preserving HALL-0076's explicit prohibition on
blind PDLMA -> Alfabeto Popular rewriting.
"""

from __future__ import annotations

from collections import defaultdict
import csv
from pathlib import Path
import re
import unicodedata
from typing import Any

ADAPTER_VERSION = "0.35.10"
BRIDGE_VERSION = "0.2"

CANDIDATE_STATUS = "DOCUMENTARY_VERB_FORM_CONTEXTUAL_CANDIDATE"

VOCES_KNOWLEDGE_COMMIT = "5a5a76eca11966b7df79edb76cf51ab94507bda1"
DICTIONARIA_SOURCE_ID = "SRC-DICTIONARIA-DIDXAZA-SPANISH-ENGLISH-DICTIONARY"
DICTIONARIA_COMMIT = "76c22cf30c23d8f4bc5c83c11013a8cb24fe0f85"
RAW_SQLITE_GIT_BLOB_SHA1 = "4722551b56bb219c1cad354d1bfa9077d657aada"
PBK_SOURCE_ID = "SRC-PEREZ-BAEZ-KAUFMAN-2016-VERB-CLASSES"
HALL_IDS = ("HALL-0073", "HALL-0074", "HALL-0076")

HERE = Path(__file__).resolve().parent
DEFAULT_ASSOCIATION_REGISTRY_PATH = (
    HERE.parent / "sources" / "DICTIONARIA_EXAMPLE_FIELD_ASSOCIATIONS_v0_1.csv"
)

APOSTROPHE_EQUIVALENTS = ("'", "’", "ʼ", "ꞌ")
TAM_FIELD_ID_MAP = {
    "HAB": "HABITUAL",
    "POT": "POTENTIAL",
    "CMP": "COMPLETIVE",
    "PRG": "PROGRESSIVE",
    "PRF": "PERFECT",
    "FUT": "FUTURE",
    "CTF": "COUNTERFACTUAL",
    "AND": "ANDATIVE",
}


def strict_documentary_key(text: str) -> str:
    """Comparison key for AP documentary evidence; never an output rewrite."""
    value = unicodedata.normalize("NFC", str(text or "")).casefold()
    for apostrophe in APOSTROPHE_EQUIVALENTS[1:]:
        value = value.replace(apostrophe, "'")
    return re.sub(r"\s+", " ", value.strip())


def tokenize_documentary_surface(text: str) -> tuple[str, ...]:
    """Strip only outer punctuation while retaining linguistic marks."""
    out: list[str] = []
    for match in re.finditer(r"\S+", str(text or "")):
        raw = match.group(0)
        left = 0
        right = len(raw)
        while left < right and not (
            raw[left].isalnum()
            or raw[left] in APOSTROPHE_EQUIVALENTS
            or unicodedata.category(raw[left]).startswith(("L", "M"))
        ):
            left += 1
        while right > left and not (
            raw[right - 1].isalnum()
            or raw[right - 1] in APOSTROPHE_EQUIVALENTS
            or unicodedata.category(raw[right - 1]).startswith(("L", "M"))
        ):
            right -= 1
        if left < right:
            out.append(raw[left:right])
    return tuple(out)


def _sense_ids(raw: str) -> tuple[str, ...]:
    return tuple(dict.fromkeys(x for x in re.split(r"[;\s]+", str(raw or "")) if x))


def _root_analysis_raw(record: Any) -> str:
    raw = str(getattr(record, "pdlma_raw", "") or "").strip()
    return raw[1:] if raw.startswith("-") else raw


def load_association_registry(path: str | Path) -> list[dict[str, str]]:
    path = Path(path)
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    required = {
        "example_id", "sense_id", "field_id", "tam_label",
        "dictionaria_commit", "raw_sqlite_git_blob_sha1",
    }
    if rows and not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0]))
        raise ValueError(f"Association registry missing columns: {', '.join(missing)}")
    for row in rows:
        if row["dictionaria_commit"] != DICTIONARIA_COMMIT:
            raise ValueError("Association registry Dictionaria commit mismatch")
        if row["raw_sqlite_git_blob_sha1"] != RAW_SQLITE_GIT_BLOB_SHA1:
            raise ValueError("Association registry raw SQLite blob mismatch")
        expected_tam = TAM_FIELD_ID_MAP.get(row["field_id"])
        if expected_tam is None or row["tam_label"] != expected_tam:
            raise ValueError(
                f"Invalid TAM association row: {row.get('field_id')} -> {row.get('tam_label')}"
            )
    return rows


class DocumentaryVerbFormCandidateAnalyzer:
    """Add non-licensing documentary verb-form research candidates."""

    def __init__(
        self,
        base_analyzer: Any,
        association_registry_path: str | Path | None = None,
    ):
        self.base = base_analyzer
        for name in (
            "retrieval", "bound", "morph2", "morph1", "db", "verb_meta",
            "person_exact", "runtime_root", "sqlite_path", "verb_inventory_path",
            "biyubi_source",
        ):
            if hasattr(base_analyzer, name):
                setattr(self, name, getattr(base_analyzer, name))

        self.association_registry_path = Path(
            association_registry_path or DEFAULT_ASSOCIATION_REGISTRY_PATH
        )
        self._association_registry_rows = load_association_registry(
            self.association_registry_path
        )
        self._association_rows_by_example: dict[str, list[dict[str, str]]] = defaultdict(list)
        for row in self._association_registry_rows:
            self._association_rows_by_example[row["example_id"]].append(row)

        self._sense_to_verb_entry: dict[str, str] = {}
        for entry_id, rows in self.retrieval.senses.items():
            if entry_id not in self.morph1.records:
                continue
            for row in rows:
                sense_id = str(row.get("ID", "") or "").strip()
                if sense_id:
                    self._sense_to_verb_entry[sense_id] = entry_id

        self._example_token_index: dict[str, list[dict[str, Any]]] = defaultdict(list)
        self._indexed_example_ids: set[str] = set()
        self._used_association_row_count = 0

        for example in self.retrieval.examples:
            example_id = str(example.get("ID", "") or "").strip()
            if not example_id:
                continue
            registry_rows = self._association_rows_by_example.get(example_id, ())
            if not registry_rows:
                continue

            exported_sense_ids = set(_sense_ids(example.get("Sense_IDs", "") or ""))
            by_entry: dict[str, list[dict[str, str]]] = defaultdict(list)
            for registry_row in registry_rows:
                sense_id = registry_row["sense_id"]
                # Integrity join: the granular raw relation must agree with the
                # sense link preserved in the exported ExampleTable.
                if sense_id not in exported_sense_ids:
                    continue
                entry_id = self._sense_to_verb_entry.get(sense_id)
                if entry_id is None:
                    continue
                by_entry[entry_id].append(registry_row)

            # v0.2 is deliberately conservative: examples whose explicit TAM
            # associations point to more than one verb entry are not indexed.
            if len(by_entry) != 1:
                continue
            linked_entry_id, entry_rows = next(iter(by_entry.items()))
            tam_labels = tuple(
                dict.fromkeys(row["tam_label"] for row in entry_rows)
            )
            if not tam_labels:
                continue

            primary_text = str(example.get("Primary_Text", "") or "").strip()
            tokens = tokenize_documentary_surface(primary_text)
            if not tokens:
                continue

            association = {
                "example_id": example_id,
                "primary_text_raw": primary_text,
                "sense_ids": sorted({row["sense_id"] for row in entry_rows}),
                "linked_verb_entry_id": linked_entry_id,
                "association_field_ids": sorted({row["field_id"] for row in entry_rows}),
                "tam_candidates_from_example_association": list(tam_labels),
                "attribution_raw": example.get("Attribution", "") or "",
                "source_id": DICTIONARIA_SOURCE_ID,
                "dictionaria_commit": DICTIONARIA_COMMIT,
                "raw_sqlite_git_blob_sha1": RAW_SQLITE_GIT_BLOB_SHA1,
                "token_role_within_example_assertion": False,
            }
            self._indexed_example_ids.add(example_id)
            self._used_association_row_count += len(entry_rows)
            for token in dict.fromkeys(tokens):
                key = strict_documentary_key(token)
                if key:
                    row = dict(association)
                    row["token_surface_in_example"] = token
                    self._example_token_index[key].append(row)

    @property
    def biyubi_source_status(self) -> str:
        return self.base.biyubi_source_status

    def close(self) -> None:
        self.base.close()

    @property
    def documentary_candidate_index_stats(self) -> dict[str, int | str | bool]:
        return {
            "association_registry_present": self.association_registry_path.exists(),
            "association_registry_path": str(self.association_registry_path),
            "association_registry_rows": len(self._association_registry_rows),
            "used_association_rows": self._used_association_row_count,
            "verb_sense_links": len(self._sense_to_verb_entry),
            "tam_tagged_examples": len(self._indexed_example_ids),
            "indexed_token_keys": len(self._example_token_index),
        }

    def _candidate_payload(self, raw_token: str, token_index: int) -> dict[str, Any] | None:
        key = strict_documentary_key(raw_token)
        associations = list(self._example_token_index.get(key, ()))
        if not associations:
            return None

        by_entry: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for association in associations:
            by_entry[association["linked_verb_entry_id"]].append(association)

        compatible_entries: list[dict[str, Any]] = []
        for entry_id, rows in sorted(by_entry.items()):
            record = self.morph1.records.get(entry_id)
            if record is None:
                continue
            tam_candidates = sorted(
                {
                    tam
                    for row in rows
                    for tam in row["tam_candidates_from_example_association"]
                }
            )
            pdlma_coordinates = {
                tam: list(record.tam_forms.get(tam, ()))
                for tam in tam_candidates
                if record.tam_forms.get(tam)
            }
            example_ids = sorted(
                {row["example_id"] for row in rows if row.get("example_id")}
            )
            compatible_entries.append(
                {
                    "entry_id": entry_id,
                    "documented_headword_raw": record.headword_raw,
                    "definition_es": record.definition_es,
                    "verb_class": record.verb_class,
                    "class_status": record.class_status,
                    "irregular": record.irregular,
                    "pdlma_citation_raw": record.pdlma_raw,
                    "root_analysis_raw": _root_analysis_raw(record),
                    "tam_candidates": tam_candidates,
                    "compatible_documented_pdlma_coordinates": pdlma_coordinates,
                    "supporting_example_ids": example_ids,
                    "supporting_example_count": len(example_ids),
                    "supporting_associations": rows,
                    "association_strength": (
                        "MULTIPLE_EXACT_EXAMPLE_ASSOCIATIONS"
                        if len(example_ids) > 1
                        else "SINGLE_EXACT_EXAMPLE_ASSOCIATION"
                    ),
                    "provenance": {
                        "documentary_source": DICTIONARIA_SOURCE_ID,
                        "dictionaria_commit": DICTIONARIA_COMMIT,
                        "raw_sqlite_git_blob_sha1": RAW_SQLITE_GIT_BLOB_SHA1,
                        "verb_class_system_authority": PBK_SOURCE_ID,
                        "voces_hall_ids": list(HALL_IDS),
                        "voces_knowledge_commit": VOCES_KNOWLEDGE_COMMIT,
                    },
                    "observed_token_is_verb_assertion": False,
                    "tam_of_observed_surface_assertion": False,
                    "root_segmentation_of_observed_token_assertion": False,
                    "pdlma_to_ap_assertion": False,
                    "semantic_equivalence_assertion": False,
                    "correction_assertion": False,
                    "orthographic_authority_assertion": False,
                    "generation_license_assertion": False,
                    "rule_discovery_assertion": False,
                }
            )

        if not compatible_entries:
            return None
        return {
            "token_index": token_index,
            "token_raw": raw_token,
            "documentary_key": key,
            "candidate_status": CANDIDATE_STATUS,
            "underlying_exact_documentary_token_attestation": True,
            "compatible_verb_entry_count": len(compatible_entries),
            "compatible_verb_entries": compatible_entries,
            "candidate_adds_exact_surface_evidence": False,
            "candidate_promotes_analysis_status": False,
            "candidate_resolves_token": False,
            "interpretation": (
                "EXACT_TOKEN_ATTESTED_INSIDE_TAM_FIELD_ASSOCIATED_EXAMPLE_"
                "COMPATIBLE_VERB_ENTRY_IDENTIFIED_TOKEN_ROLE_WITHIN_EXAMPLE_NOT_PROVEN"
            ),
        }

    def analyze(
        self,
        surface: str,
        *,
        item_id: str | None = None,
        spanish_supplied: str | None = None,
        context_segments: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        result = self.base.analyze(
            surface,
            item_id=item_id,
            spanish_supplied=spanish_supplied,
            context_segments=context_segments,
        )
        tokens = [match.group(0) for match in re.finditer(r"\S+", surface or "")]
        already_analyzed = set(result.get("documented_exact_verb_token_indexes", ()))
        already_analyzed.update(
            result.get("documented_person_fusion_analyzed_token_indexes", ())
        )

        candidates: list[dict[str, Any]] = []
        for token_index, token in enumerate(tokens):
            if token_index in already_analyzed:
                continue
            candidate = self._candidate_payload(token, token_index)
            if candidate is not None:
                candidates.append(candidate)

        candidate_indexes = [row["token_index"] for row in candidates]
        unresolved_before = list(
            result.get("unresolved_token_indexes_after_documented_morphology", ())
        )
        result.update(
            {
                "current_adapter_version": ADAPTER_VERSION,
                "verb_analysis_bridge_version": BRIDGE_VERSION,
                "documentary_verb_form_candidate_layer_enabled": True,
                "documentary_verb_form_candidate_search_scope": (
                    "TOKENS_WITHOUT_V01_EXACT_VERB_HEADWORD_OR_PROMOTED_PERSON_FUSION_ANALYSIS"
                ),
                "documentary_verb_form_candidates": candidates,
                "documentary_verb_form_candidate_token_indexes": candidate_indexes,
                "unresolved_token_indexes_after_documentary_verb_form_candidates": unresolved_before,
                "documentary_verb_form_candidates_change_exact_evidence_metrics": False,
                "documentary_verb_form_candidates_change_analysis_status": False,
                "documentary_verb_form_candidates_generation_enabled": False,
                "documentary_verb_form_candidates_correction_enabled": False,
            }
        )
        result.setdefault("fallback_policy", {}).update(
            {
                "documentary_verb_form_candidate_requires_no_existing_exact_verb_headword_analysis": True,
                "documentary_verb_form_candidate_requires_exact_ap_example_token": True,
                "documentary_verb_form_candidate_requires_unique_linked_verb_entry_per_example": True,
                "documentary_verb_form_candidate_requires_explicit_tam_field_association": True,
                "documentary_verb_form_candidate_token_role_is_not_asserted": True,
                "documentary_verb_form_candidate_pdlma_is_recovery_coordinate_only": True,
                "documentary_verb_form_candidate_pdlma_to_ap": False,
                "documentary_verb_form_candidate_promotes_analysis_status": False,
                "documentary_verb_form_candidate_generation": False,
                "documentary_verb_form_candidate_correction": False,
            }
        )
        result.setdefault("limitations", []).extend(
            [
                "DOCUMENTARY_VERB_FORM_CANDIDATE_DOES_NOT_PROVE_TOKEN_ROLE_WITHIN_EXAMPLE",
                "DOCUMENTARY_VERB_FORM_CANDIDATE_DOES_NOT_PROVE_TAM_OF_OBSERVED_SURFACE",
                "DOCUMENTARY_VERB_FORM_CANDIDATE_DOES_NOT_SEGMENT_OBSERVED_TOKEN",
                "PDLMA_COORDINATES_ARE_ANALYTICAL_RECOVERY_COORDINATES_NOT_AP_SURFACE_FORMS",
            ]
        )
        return result
