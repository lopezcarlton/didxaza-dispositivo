#!/usr/bin/env python3
"""Analyzer v0.35.10 — documentary candidates for non-headword verb forms.

This wrapper extends VerbAnalysisBridge v0.1 without changing any exact-evidence
metric or promoting an unresolved token to a resolved morphological analysis.

For tokens that remain unresolved after the documented morphology layer, it may
surface a *research candidate* when all of the following are true:

1. the token is exactly attested in a Dictionaria AP Primary_Text example under
   a strict documentary key (NFC + case + apostrophe typography only);
2. the example is associated with exactly one Dictionaria sense that maps to a
   verb entry present in the 2,385-record inventory (or multiple senses that all
   map to the same verb entry);
3. the example carries at least one explicit grammatical-feature association
   among Habitual/Potential/Completive/Progressive/Perfect/Future/
   Counterfactual/Andative.

The candidate exposes the compatible verb entry, class, analytical root/citation
and the PDLMA paradigm fields for the TAM labels associated with the example.
It does NOT assert that the observed token is necessarily the verb in that
sentence, does NOT map PDLMA to AP, and does NOT license correction/generation.

This implements the recovery-coordinate use allowed by Voces HALL-0073,
HALL-0074 and HALL-0076 while preserving HALL-0076's explicit prohibition on
blind PDLMA -> Alfabeto Popular rewriting.
"""

from __future__ import annotations

from collections import defaultdict
import re
import unicodedata
from typing import Any

ADAPTER_VERSION = "0.35.10"
BRIDGE_VERSION = "0.2"

CANDIDATE_STATUS = "DOCUMENTARY_VERB_FORM_CONTEXTUAL_CANDIDATE"

VOCES_KNOWLEDGE_COMMIT = "5a5a76eca11966b7df79edb76cf51ab94507bda1"
DICTIONARIA_SOURCE_ID = "SRC-DICTIONARIA-DIDXAZA-SPANISH-ENGLISH-DICTIONARY"
PBK_SOURCE_ID = "SRC-PEREZ-BAEZ-KAUFMAN-2016-VERB-CLASSES"
HALL_IDS = ("HALL-0073", "HALL-0074", "HALL-0076")

APOSTROPHE_EQUIVALENTS = ("'", "’", "ʼ", "ꞌ")
TAM_FEATURE_MAP = {
    "Habitual": "HABITUAL",
    "Potential": "POTENTIAL",
    "Completive": "COMPLETIVE",
    "Progressive": "PROGRESSIVE",
    "Perfect": "PERFECT",
    "Future": "FUTURE",
    "Counterfactual": "COUNTERFACTUAL",
    "Andative": "ANDATIVE",
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


def _features(raw: str) -> tuple[str, ...]:
    return tuple(dict.fromkeys(x.strip() for x in str(raw or "").split(";") if x.strip()))


def _root_analysis_raw(record: Any) -> str:
    raw = str(getattr(record, "pdlma_raw", "") or "").strip()
    return raw[1:] if raw.startswith("-") else raw


class DocumentaryVerbFormCandidateAnalyzer:
    """Add non-licensing documentary verb-form research candidates."""

    def __init__(self, base_analyzer: Any):
        self.base = base_analyzer
        for name in (
            "retrieval", "bound", "morph2", "morph1", "db", "verb_meta",
            "person_exact", "runtime_root", "sqlite_path", "verb_inventory_path",
            "biyubi_source",
        ):
            if hasattr(base_analyzer, name):
                setattr(self, name, getattr(base_analyzer, name))

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
        for example in self.retrieval.examples:
            sense_ids = _sense_ids(example.get("Sense_IDs", "") or "")
            linked_entries = sorted(
                {
                    self._sense_to_verb_entry[sense_id]
                    for sense_id in sense_ids
                    if sense_id in self._sense_to_verb_entry
                }
            )
            if len(linked_entries) != 1:
                continue

            features = _features(example.get("Associated_Grammatical_Features", "") or "")
            tam_labels = tuple(
                dict.fromkeys(TAM_FEATURE_MAP[f] for f in features if f in TAM_FEATURE_MAP)
            )
            if not tam_labels:
                continue

            primary_text = str(example.get("Primary_Text", "") or "").strip()
            tokens = tokenize_documentary_surface(primary_text)
            if not tokens:
                continue

            example_id = str(example.get("ID", "") or "").strip()
            association = {
                "example_id": example_id or None,
                "primary_text_raw": primary_text,
                "sense_ids": list(sense_ids),
                "linked_verb_entry_id": linked_entries[0],
                "associated_grammatical_features": list(features),
                "tam_candidates_from_example_association": list(tam_labels),
                "attribution_raw": example.get("Attribution", "") or "",
                "source_id": DICTIONARIA_SOURCE_ID,
                "token_role_within_example_assertion": False,
            }
            if example_id:
                self._indexed_example_ids.add(example_id)
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
    def documentary_candidate_index_stats(self) -> dict[str, int]:
        return {
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
            "compatible_verb_entry_count": len(compatible_entries),
            "compatible_verb_entries": compatible_entries,
            "candidate_is_exact_surface_evidence": False,
            "candidate_promotes_analysis_status": False,
            "candidate_resolves_unresolved_token": False,
            "interpretation": (
                "EXACT_TOKEN_ATTESTED_INSIDE_TAM_TAGGED_EXAMPLE_ASSOCIATED_WITH_VERB_ENTRY_"
                "TOKEN_ROLE_WITHIN_EXAMPLE_NOT_PROVEN"
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
        unresolved = list(result.get("unresolved_token_indexes_after_documented_morphology", ()))
        candidates: list[dict[str, Any]] = []
        for token_index in unresolved:
            if token_index >= len(tokens):
                continue
            candidate = self._candidate_payload(tokens[token_index], token_index)
            if candidate is not None:
                candidates.append(candidate)

        candidate_indexes = [row["token_index"] for row in candidates]
        result.update(
            {
                "current_adapter_version": ADAPTER_VERSION,
                "verb_analysis_bridge_version": BRIDGE_VERSION,
                "documentary_verb_form_candidate_layer_enabled": True,
                "documentary_verb_form_candidates": candidates,
                "documentary_verb_form_candidate_token_indexes": candidate_indexes,
                "unresolved_token_indexes_after_documentary_verb_form_candidates": unresolved,
                "documentary_verb_form_candidates_change_exact_evidence_metrics": False,
                "documentary_verb_form_candidates_change_analysis_status": False,
                "documentary_verb_form_candidates_generation_enabled": False,
                "documentary_verb_form_candidates_correction_enabled": False,
            }
        )
        result.setdefault("fallback_policy", {}).update(
            {
                "documentary_verb_form_candidates_run_only_on_unresolved_tokens": True,
                "documentary_verb_form_candidate_requires_exact_ap_example_token": True,
                "documentary_verb_form_candidate_requires_unique_linked_verb_entry": True,
                "documentary_verb_form_candidate_requires_explicit_tam_feature": True,
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
