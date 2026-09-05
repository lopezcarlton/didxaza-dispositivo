#!/usr/bin/env python3
"""Analyzer v0.35.9 — first vertical bridge into documented verb knowledge.

Purpose
-------
Expose, token by token, verb information that is *already associated with a
Dictionaria verb record* in DIC_VERB_2385_v0_1.csv / Morphology I:

- documented AP headword;
- PBK/Dictionaria verb class label and class status;
- lexical irregularity flag;
- analytical citation/root string as stored by Dictionaria;
- documented PDLMA paradigm fields and their availability;
- per-record attribution and knowledge provenance.

This layer does NOT infer a non-headword surface, segment a new word, convert a
PDLMA paradigm form to Alfabeto Popular, generate a paradigm, resolve homography,
change valency, correct spelling, or discover a rule.

The index deliberately does not reuse Morphology I ``surface_index`` because
that historical comparison removes tone marks. Here the comparison is stricter:
Unicode NFC + case-insensitive comparison only. A second, explicitly labelled
comparison may remove *sentence-edge punctuation only*; glottal/apostrophe
characters are never stripped or normalized.
"""

from __future__ import annotations

from collections import defaultdict
import re
import unicodedata
from typing import Any

ADAPTER_VERSION = "0.35.9"
BRIDGE_VERSION = "0.1"

STATUS_RAW = "DOCUMENTED_VERB_HEADWORD_EXACT_RAW"
STATUS_PUNCT = "DOCUMENTED_VERB_HEADWORD_PUNCTUATION_LIGHT"
STATUS_NONE = "NO_DOCUMENTED_VERB_HEADWORD_MATCH"

VOCES_KNOWLEDGE_COMMIT = "5a5a76eca11966b7df79edb76cf51ab94507bda1"
DICTIONARIA_SOURCE_ID = "SRC-DICTIONARIA-DIDXAZA-SPANISH-ENGLISH-DICTIONARY"
PBK_SOURCE_ID = "SRC-PEREZ-BAEZ-KAUFMAN-2016-VERB-CLASSES"
PBK_HALL_IDS = ("HALL-0073", "HALL-0074", "HALL-0075", "HALL-0076")
TECHNICAL_DERIVATIVE = "DIC_VERB_2385_v0_1.csv"

# Only ordinary sentence-edge punctuation. Apostrophes/glottal marks are absent
# on purpose and therefore remain linguistically contrastive in comparison.
_EDGE_PUNCT = ".,;:!?¿¡()[]{}\"“”«»"


def _nfc_casefold(value: str) -> str:
    return unicodedata.normalize("NFC", str(value or "")).casefold()


def _punctuation_light(value: str) -> str:
    return str(value or "").strip(_EDGE_PUNCT)


def _split_documented_headword_variants(raw: str) -> tuple[str, ...]:
    """Split only explicit top-level variants already present in the record."""
    raw = str(raw or "").strip()
    if not raw:
        return ()
    parts = [x.strip() for x in re.split(r"\s*;\s*|\s+~\s+", raw) if x.strip()]
    return tuple(dict.fromkeys(parts))


class VerbAnalysisBridgeAnalyzer:
    """Add exact documented verb-record enrichment after Analyzer v0.35.8."""

    def __init__(self, base_analyzer: Any):
        self.base = base_analyzer

        # Preserve public attributes expected by current callers/tests.
        for name in (
            "retrieval", "bound", "morph2", "morph1", "db", "verb_meta",
            "person_exact", "runtime_root", "sqlite_path", "verb_inventory_path",
            "biyubi_source",
        ):
            if hasattr(base_analyzer, name):
                setattr(self, name, getattr(base_analyzer, name))

        self._verb_headword_index: dict[str, list[tuple[str, str]]] = defaultdict(list)
        for entry_id, record in self.morph1.records.items():
            for variant in _split_documented_headword_variants(record.headword_raw):
                # MVP v0.1 is token-level only. Multiword headwords remain visible
                # in the underlying record but are not silently collapsed.
                if any(ch.isspace() for ch in variant):
                    continue
                key = _nfc_casefold(variant)
                if key:
                    self._verb_headword_index[key].append((entry_id, variant))

    @property
    def biyubi_source_status(self) -> str:
        return self.base.biyubi_source_status

    def close(self) -> None:
        self.base.close()

    def _record_payload(self, entry_id: str, matched_variant: str) -> dict[str, Any]:
        record = self.morph1.records[entry_id]
        paradigm = {
            tam: {
                "available": bool(variants),
                "variants_raw": list(variants),
                "channel": "PDLMA_ANALYTICAL_DOCUMENTARY_FIELD",
                "ap_surface_projection_assertion": False,
                "generation_license_assertion": False,
            }
            for tam, variants in record.tam_forms.items()
        }
        return {
            "entry_id": record.entry_id,
            "documented_headword_raw": record.headword_raw,
            "matched_headword_variant_raw": matched_variant,
            "headword_channel": "JZ_AP_DOCUMENTED_HEADWORD",
            "verb_class": record.verb_class,
            "class_status": record.class_status,
            "irregular": record.irregular,
            "analysis_codes_raw": record.analysis_codes_raw,
            "definition_es": record.definition_es,
            "pdlma_citation_raw": record.pdlma_raw,
            "pdlma_citation_interpretation": "ANALYTICAL_CITATION_ONLY_NOT_AP_SURFACE",
            "documented_paradigm": paradigm,
            "documented_tam_labels_available": [
                tam for tam, detail in paradigm.items() if detail["available"]
            ],
            "record_attribution_raw": record.attribution_entry,
            "provenance": {
                "documentary_record_source": DICTIONARIA_SOURCE_ID,
                "technical_derivative": TECHNICAL_DERIVATIVE,
                "verb_class_system_authority": PBK_SOURCE_ID,
                "verb_class_system_hall_ids": list(PBK_HALL_IDS),
                "voces_knowledge_commit": VOCES_KNOWLEDGE_COMMIT,
                "concrete_class_assignment_basis": "DICTIONARIA_RECORD_AS_EXPOSED_BY_TECHNICAL_DERIVATIVE",
            },
            "lexical_identity_from_context_assertion": False,
            "root_segmentation_of_observed_token_assertion": False,
            "pdlma_to_ap_assertion": False,
            "correction_assertion": False,
            "orthographic_authority_assertion": False,
            "generation_license_assertion": False,
            "rule_discovery_assertion": False,
        }

    def _lookup_token(self, raw_token: str, token_index: int) -> dict[str, Any]:
        raw_key = _nfc_casefold(raw_token)
        raw_matches = list(self._verb_headword_index.get(raw_key, []))

        comparison_surface = raw_token
        status = STATUS_NONE
        matches = raw_matches
        if raw_matches:
            status = STATUS_RAW
        else:
            light = _punctuation_light(raw_token)
            comparison_surface = light
            light_key = _nfc_casefold(light)
            if light != raw_token and light_key:
                matches = list(self._verb_headword_index.get(light_key, []))
                if matches:
                    status = STATUS_PUNCT

        payloads = [self._record_payload(entry_id, variant) for entry_id, variant in matches]
        return {
            "token_index": token_index,
            "token_raw": raw_token,
            "comparison_surface": comparison_surface,
            "verb_headword_status": status,
            "documented_record_count": len(payloads),
            "documented_records": payloads,
            "verb_category_documented": bool(payloads),
            "single_inventory_record": len(payloads) == 1,
            "ambiguity_preserved": len(payloads) > 1,
            "comparison_policy": {
                "unicode_nfc": True,
                "case_insensitive_only_for_sentence_capitalization": True,
                "sentence_edge_punctuation_light_secondary": True,
                "tone_stripping": False,
                "diacritic_stripping": False,
                "apostrophe_normalization": False,
                "glottal_mark_stripping": False,
                "near_match": False,
                "edit_distance": False,
                "pdlma_to_surface": False,
            },
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
        observations = [self._lookup_token(token, i) for i, token in enumerate(tokens)]
        matched = [row for row in observations if row["verb_category_documented"]]
        matched_indexes = [row["token_index"] for row in matched]

        result.update(
            {
                "current_adapter_version": ADAPTER_VERSION,
                "verb_analysis_bridge_version": BRIDGE_VERSION,
                "verb_analysis_bridge_enabled": True,
                "verb_headword_observations": observations,
                "documented_exact_verb_analyses": matched,
                "documented_exact_verb_token_indexes": matched_indexes,
                "documented_exact_verb_token_count": len(matched_indexes),
                "verb_analysis_bridge_changes_exact_evidence_metrics": False,
                "verb_analysis_bridge_generation_enabled": False,
                "verb_analysis_bridge_valency_enabled": False,
                "verb_analysis_bridge_nonheadword_tam_inference_enabled": False,
                "verb_analysis_bridge_context_resolution_enabled": False,
            }
        )
        result.setdefault("fallback_policy", {}).update(
            {
                "verb_bridge_documented_headword_only": True,
                "verb_bridge_preserves_homography": True,
                "verb_bridge_pdlma_fields_are_analytical_only": True,
                "verb_bridge_pdlma_to_ap": False,
                "verb_bridge_tone_stripping": False,
                "verb_bridge_near_match": False,
                "verb_bridge_generation": False,
                "verb_bridge_correction": False,
            }
        )
        result.setdefault("limitations", []).extend(
            [
                "VERB_BRIDGE_V0_1_RECOGNIZES_DOCUMENTED_SINGLE_TOKEN_HEADWORDS_ONLY",
                "VERB_BRIDGE_V0_1_DOES_NOT_INFER_NONHEADWORD_TAM_OR_ROOT",
                "VERB_BRIDGE_V0_1_DOES_NOT_APPLY_VALENCY_OR_CONTEXT_TO_RESOLVE_LEXICAL_IDENTITY",
                "PDLMA_PARADIGM_FIELDS_ARE_NOT_AP_SURFACE_FORMS_OR_GENERATION_LICENSES",
            ]
        )
        return result
