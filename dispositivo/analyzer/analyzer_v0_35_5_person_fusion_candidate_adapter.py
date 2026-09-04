#!/usr/bin/env python3
"""Analyzer v0.35.5: source-backed person-fusion candidates.

REAL_TEXT_PROBE_002 exposed ``Rinite'`` after all exact evidence layers.  The
verb inventory documents ``riniti`` 'perderse, extraviarse', while Gramática
Popular Cuadro 17 documents a 1SG fusion pattern for grave words ending in
``i``: final ``i`` surfaces as ``e'`` (e.g. ``bihui`` -> ``xpihue'``).

This wrapper links an unresolved observed surface ending in ``e'`` to an exact
DOCUMENTED VERB HEADWORD obtainable by the single reverse comparison
``e'`` -> ``i``.  It emits a morphology CANDIDATE only.  The runtime does not
currently encode the prosodic subclass (grave/aguda) needed to promote the
candidate to a fully resolved person analysis, so exact evidence, unresolved
indexes, analysis status, correction authority, and generation authority are
all preserved unchanged.

No generic edit distance, tone stripping, suffix guessing, or PDLMA projection
is performed here.
"""

from __future__ import annotations

import re
import unicodedata
from collections import defaultdict
from typing import Any

from analyzer_v0_35_4_documentary_candidate_adapter import (
    DocumentaryCandidateAnalyzer,
)

ADAPTER_VERSION = "0.35.5"
STATUS_PERSON_FUSION_CANDIDATE = "DOCUMENTED_LEXEME_PLUS_GP_1SG_FUSION_CANDIDATE"
RULE_ID = "JLC-PERS-002"
SOURCE_ID = "BIB004_GRAMATICA_POPULAR"
SOURCE_LOCATION = "Cuadro 17"

_APOSTROPHES = "'’ꞌʼ‘`"
_OUTER_PUNCTUATION = ".,;:!?¿¡\"“”«»()[]{}…"


def _candidate_key(value: str) -> str:
    """Candidate-only comparison key preserving tone/diacritics."""

    text = str(value or "").strip().strip(_OUTER_PUNCTUATION).strip()
    text = unicodedata.normalize("NFC", text).casefold()
    return "".join("'" if ch in _APOSTROPHES else ch for ch in text)


class PersonFusionCandidateAnalyzer:
    """Add a conservative 1SG i->e' reverse-link candidate after v0.35.4."""

    def __init__(self, base_analyzer: DocumentaryCandidateAnalyzer):
        self.base = base_analyzer
        self.biyubi_source = base_analyzer.biyubi_source

        # Preserve current public attributes.
        self.retrieval = base_analyzer.retrieval
        self.bound = base_analyzer.bound
        self.morph2 = base_analyzer.morph2
        self.morph1 = base_analyzer.morph1
        self.db = base_analyzer.db
        self.verb_meta = base_analyzer.verb_meta
        self.person_exact = base_analyzer.person_exact
        self.runtime_root = base_analyzer.runtime_root
        self.sqlite_path = base_analyzer.sqlite_path
        self.verb_inventory_path = base_analyzer.verb_inventory_path

        self._habitual_verb_headword_index: dict[str, list[Any]] = defaultdict(list)
        for record in self.morph1.records.values():
            # The headword channel is licensed only when Morphology I itself has
            # a documented habitual form for the lexeme.
            if not record.tam_forms.get("HABITUAL"):
                continue
            key = _candidate_key(record.headword_raw)
            if key:
                self._habitual_verb_headword_index[key].append(record)

    @property
    def biyubi_source_status(self) -> str:
        return self.base.biyubi_source_status

    def close(self) -> None:
        self.base.close()

    def _person_fusion_candidates(self, raw_token: str, token_index: int) -> list[dict[str, Any]]:
        observed_key = _candidate_key(raw_token)
        if not observed_key.endswith("e'"):
            return []

        reconstructed_key = observed_key[:-2] + "i"
        records = self._habitual_verb_headword_index.get(reconstructed_key, [])
        out: list[dict[str, Any]] = []
        for record in records:
            out.append(
                {
                    "token_index": token_index,
                    "token_raw": raw_token,
                    "candidate_status": STATUS_PERSON_FUSION_CANDIDATE,
                    "person_candidate": "1SG",
                    "observed_candidate_key": observed_key,
                    "reconstructed_habitual_headword_key": reconstructed_key,
                    "documented_entry_id": record.entry_id,
                    "documented_headword_raw": record.headword_raw,
                    "documented_definition_es": record.definition_es,
                    "documented_habitual_pdlma_forms": list(record.tam_forms.get("HABITUAL", ())),
                    "documented_verb_class": record.verb_class,
                    "comparison_operation": "FINAL_E_GLOTTAL_TO_I_REVERSE_CANDIDATE",
                    "rule_id": RULE_ID,
                    "rule_source_id": SOURCE_ID,
                    "rule_source_location": SOURCE_LOCATION,
                    "rule_statement": (
                        "GP Cuadro 17 documents final i -> e' in 1SG for grave words; "
                        "candidate requires a documented lexical base and prosodic-class confirmation."
                    ),
                    "lexical_base_match": "EXACT_RAW_HEADWORD_CANDIDATE_KEY",
                    "prosodic_class_status": "NOT_ENCODED_REQUIRES_CONFIRMATION",
                    "candidate_only": True,
                    "exact_surface_match_assertion": False,
                    "full_person_resolution_assertion": False,
                    "semantic_equivalence_assertion": False,
                    "correction_assertion": False,
                    "orthographic_authority_assertion": False,
                    "generation_license_assertion": False,
                    "rule_discovery_assertion": False,
                }
            )
        return out

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
        exact_unresolved = list(result.get("still_exactly_unresolved_token_indexes", []))

        rows: list[dict[str, Any]] = []
        candidate_indexes: set[int] = set()
        for token_index in exact_unresolved:
            token_rows = self._person_fusion_candidates(tokens[token_index], token_index)
            rows.extend(token_rows)
            if token_rows:
                candidate_indexes.add(token_index)

        # Strict invariant: candidate relations do not alter any exact state.
        result.update(
            {
                "current_adapter_version": ADAPTER_VERSION,
                "documented_person_fusion_candidate_layer_enabled": True,
                "supplemental_documented_person_fusion_candidates": rows,
                "documented_person_fusion_candidate_token_indexes": sorted(candidate_indexes),
                "still_exactly_unresolved_token_indexes": exact_unresolved,
                "exact_evidence_state_unchanged_by_person_fusion_candidates": True,
            }
        )
        result.setdefault("fallback_policy", {}).update(
            {
                "person_fusion_candidate_layer_runs_after_all_exact_layers": True,
                "person_fusion_candidate_requires_documented_habitual_headword": True,
                "person_fusion_candidate_requires_prosodic_confirmation_for_resolution": True,
                "person_fusion_candidate_does_not_promote_analysis_status": True,
                "person_fusion_candidate_does_not_increase_effective_evidence_coverage": True,
                "person_fusion_candidate_generic_edit_distance": False,
                "person_fusion_candidate_tone_stripping": False,
                "person_fusion_candidate_pdlma_to_surface": False,
            }
        )
        result.setdefault("limitations", []).extend(
            [
                "GP_1SG_I_TO_E_GLOTTAL_RELATION_IS_CANDIDATE_UNTIL_PROSODIC_CLASS_IS_CONFIRMED",
                "PERSON_FUSION_CANDIDATE_DOES_NOT_LICENSE_CORRECTION_OR_GENERATION",
            ]
        )
        return result
