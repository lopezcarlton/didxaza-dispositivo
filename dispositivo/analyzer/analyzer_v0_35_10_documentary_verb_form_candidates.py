#!/usr/bin/env python3
"""Analyzer v0.35.10 — documentary candidates for non-headword verb forms.

This wrapper extends VerbAnalysisBridge v0.1 without changing exact-evidence
metrics or promoting a token to a resolved morphological analysis.

The pinned Dictionaria snapshot does *not* contain populated example↔TAM links
(`sense_field_example` has zero rows) and its examples contain AP text but no
parallel PDLMA transcription.  Therefore v0.2 does not manufacture either kind
of missing association.

Instead, it uses only relations that are actually present and independently
anchored:

1. an AP token occurs exactly in a Dictionaria Primary_Text example;
2. that example is associated through Sense_IDs with exactly one verb entry in
   the 2,385-record verb inventory;
3. one documented PDLMA TAM variant of that *same verb entry* becomes literally
   identical to the AP token after removing ASCII hyphen U+002D only.

The third operation is deliberately a comparison operation, not an orthographic
rewrite.  No `7`→apostrophe mapping, tone/diacritic stripping, `!` removal, dot
removal, vowel change, segment substitution, edit distance or general
PDLMA→Alfabeto Popular conversion is permitted.

A successful match is therefore exposed only as a research candidate connecting
observed AP token → candidate TAM → analytical root → compatible verb entry →
verb class. It does NOT assert token identity, TAM, root segmentation, spelling,
semantic equivalence, correction or generation.

This uses the recovery-coordinate role allowed by Voces HALL-0073/HALL-0074 and
HALL-0076 while preserving HALL-0076's explicit prohibition on blind
PDLMA→Alfabeto Popular rewriting.
"""

from __future__ import annotations

from collections import defaultdict
import re
import unicodedata
from typing import Any

ADAPTER_VERSION = "0.35.10"
BRIDGE_VERSION = "0.2"

CANDIDATE_STATUS = "DOCUMENTARY_VERB_FORM_STRUCTURAL_CANDIDATE"
COMPARISON_OPERATION = "PDLMA_REMOVE_ASCII_MORPHEME_HYPHEN_ONLY"

VOCES_KNOWLEDGE_COMMIT = "5a5a76eca11966b7df79edb76cf51ab94507bda1"
DICTIONARIA_SOURCE_ID = "SRC-DICTIONARIA-DIDXAZA-SPANISH-ENGLISH-DICTIONARY"
DICTIONARIA_COMMIT = "76c22cf30c23d8f4bc5c83c11013a8cb24fe0f85"
PBK_SOURCE_ID = "SRC-PEREZ-BAEZ-KAUFMAN-2016-VERB-CLASSES"
HALL_IDS = ("HALL-0073", "HALL-0074", "HALL-0076")

APOSTROPHE_EQUIVALENTS = ("'", "’", "ʼ", "ꞌ")


def strict_documentary_key(text: str) -> str:
    """Comparison key for AP documentary evidence; never an output rewrite."""
    value = unicodedata.normalize("NFC", str(text or "")).casefold()
    for apostrophe in APOSTROPHE_EQUIVALENTS[1:]:
        value = value.replace(apostrophe, "'")
    return re.sub(r"\s+", " ", value.strip())


def pdlma_hyphen_collapse_candidate_key(text: str) -> str:
    """Remove only literal ASCII hyphens, then apply the documentary key.

    This intentionally leaves PDLMA symbols such as `.`, `=`, `!`, `7`, `*`,
    parentheses and spaces untouched.  It is a candidate-comparison coordinate,
    never a PDLMA→AP conversion function.
    """
    return strict_documentary_key(str(text or "").replace("-", ""))


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


class DocumentaryVerbFormCandidateAnalyzer:
    """Add non-licensing documentary verb-form structural candidates."""

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
        self._linked_single_verb_example_count = 0
        self._matched_structural_example_count = 0
        self._candidate_relation_count = 0

        for example in self.retrieval.examples:
            sense_ids = _sense_ids(example.get("Sense_IDs", "") or "")
            linked_entries = sorted(
                {
                    self._sense_to_verb_entry[sense_id]
                    for sense_id in sense_ids
                    if sense_id in self._sense_to_verb_entry
                }
            )
            # One example linked to multiple verb entries is too ambiguous for
            # this first bridge; preserve abstention instead of choosing.
            if len(linked_entries) != 1:
                continue
            entry_id = linked_entries[0]
            record = self.morph1.records[entry_id]
            self._linked_single_verb_example_count += 1

            pdlma_candidates_by_key: dict[str, list[dict[str, str]]] = defaultdict(list)
            for tam, variants in record.tam_forms.items():
                for variant in variants:
                    variant_raw = str(variant or "").strip()
                    if not variant_raw:
                        continue
                    candidate_key = pdlma_hyphen_collapse_candidate_key(variant_raw)
                    if not candidate_key:
                        continue
                    pdlma_candidates_by_key[candidate_key].append(
                        {
                            "tam": str(tam),
                            "pdlma_variant_raw": variant_raw,
                            "comparison_operation": COMPARISON_OPERATION,
                        }
                    )

            if not pdlma_candidates_by_key:
                continue

            primary_text = str(example.get("Primary_Text", "") or "").strip()
            tokens = tokenize_documentary_surface(primary_text)
            if not tokens:
                continue

            example_matched = False
            for token in dict.fromkeys(tokens):
                token_key = strict_documentary_key(token)
                structural_matches = pdlma_candidates_by_key.get(token_key, ())
                if not structural_matches:
                    continue
                example_matched = True
                for structural_match in structural_matches:
                    association = {
                        "example_id": str(example.get("ID", "") or "") or None,
                        "primary_text_raw": primary_text,
                        "sense_ids": list(sense_ids),
                        "linked_verb_entry_id": entry_id,
                        "token_surface_in_example": token,
                        "tam_candidate": structural_match["tam"],
                        "pdlma_variant_raw": structural_match["pdlma_variant_raw"],
                        "comparison_operation": COMPARISON_OPERATION,
                        "attribution_raw": example.get("Attribution", "") or "",
                        "source_id": DICTIONARIA_SOURCE_ID,
                        "dictionaria_commit": DICTIONARIA_COMMIT,
                        "token_role_within_example_assertion": False,
                        "pdlma_to_ap_assertion": False,
                    }
                    self._example_token_index[token_key].append(association)
                    self._candidate_relation_count += 1
            if example_matched:
                self._matched_structural_example_count += 1

    @property
    def biyubi_source_status(self) -> str:
        return self.base.biyubi_source_status

    def close(self) -> None:
        self.base.close()

    @property
    def documentary_candidate_index_stats(self) -> dict[str, int | str | bool]:
        return {
            "verb_sense_links": len(self._sense_to_verb_entry),
            "single_verb_linked_examples": self._linked_single_verb_example_count,
            "examples_with_literal_hyphen_collapse_match": self._matched_structural_example_count,
            "candidate_relations": self._candidate_relation_count,
            "indexed_token_keys": len(self._example_token_index),
            "comparison_operation": COMPARISON_OPERATION,
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
            tam_candidates = sorted({row["tam_candidate"] for row in rows})
            pdlma_coordinates: dict[str, list[str]] = defaultdict(list)
            for row in rows:
                variant = row["pdlma_variant_raw"]
                if variant not in pdlma_coordinates[row["tam_candidate"]]:
                    pdlma_coordinates[row["tam_candidate"]].append(variant)
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
                    "matching_documented_pdlma_variants": dict(pdlma_coordinates),
                    "supporting_example_ids": example_ids,
                    "supporting_example_count": len(example_ids),
                    "supporting_associations": rows,
                    "association_strength": (
                        "MULTIPLE_DOCUMENTARY_EXAMPLES_PLUS_LITERAL_PDLMA_BOUNDARY_COLLAPSE"
                        if len(example_ids) > 1
                        else "SINGLE_DOCUMENTARY_EXAMPLE_PLUS_LITERAL_PDLMA_BOUNDARY_COLLAPSE"
                    ),
                    "comparison_policy": {
                        "operation": COMPARISON_OPERATION,
                        "ascii_hyphen_removed": True,
                        "tone_stripping": False,
                        "diacritic_stripping": False,
                        "glottal_7_to_apostrophe": False,
                        "bang_removal": False,
                        "dot_removal": False,
                        "equals_removal": False,
                        "asterisk_removal": False,
                        "segment_substitution": False,
                        "vowel_change": False,
                        "near_match": False,
                        "edit_distance": False,
                    },
                    "provenance": {
                        "documentary_source": DICTIONARIA_SOURCE_ID,
                        "dictionaria_commit": DICTIONARIA_COMMIT,
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
                "AP_TOKEN_OCCURS_IN_EXAMPLE_LINKED_TO_VERB_ENTRY_AND_LITERAL_PDLMA_TAM_"
                "VARIANT_MATCHES_AFTER_ASCII_HYPHEN_REMOVAL_ONLY_CANDIDATE_NOT_ANALYSIS"
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
                "documentary_verb_form_candidate_requires_literal_pdlma_tam_match_after_ascii_hyphen_removal_only": True,
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
                "ASCII_HYPHEN_COLLAPSE_IS_COMPARISON_ONLY_NOT_PDLMA_TO_AP_CONVERSION",
                "PDLMA_COORDINATES_ARE_ANALYTICAL_RECOVERY_COORDINATES_NOT_AP_SURFACE_FORMS",
            ]
        )
        return result
