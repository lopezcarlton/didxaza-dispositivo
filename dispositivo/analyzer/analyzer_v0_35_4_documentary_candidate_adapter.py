#!/usr/bin/env python3
"""Current Analyzer wrapper exposing non-exact documentary/morphology candidates.

REAL_TEXT_PROBE_002 showed that several tokens left unresolved by exact
retrieval are not necessarily lexical knowledge gaps: some differ from
attested surfaces by a controlled orthographic operation, while others carry
person/possession shapes already recognized provisionally by the runtime.

This wrapper exposes those candidates WITHOUT changing exact evidence coverage,
analysis status, or unresolved indexes. Candidate != evidence != correction.

The candidate layer is deliberately agnostic about how many exact-evidence
layers precede it. When the Voces promoted-documentary layer is present it uses
that layer's unresolved indexes; otherwise it falls back to the older Biyubi
boundary for backwards-compatible tests.
"""

from __future__ import annotations

import re
from dataclasses import asdict
from typing import Any

from analyzer_v0_35_7_voces_documentary_exact_adapter import (
    VocesDocumentaryExactFallbackAnalyzer,
)
from documentary_candidate_layer_v0_1 import DocumentaryCandidateIndex

ADAPTER_VERSION = "0.35.4"
STATUS_RELATED = "RELATED_DOCUMENTARY_OR_GRAPHICAL_CANDIDATE_NON_EXACT"
STATUS_NONE = "NO_CONSTRAINED_CANDIDATE"


class DocumentaryCandidateAnalyzer:
    """Add candidate-only observation after all exact evidence layers."""

    def __init__(self, base_analyzer: VocesDocumentaryExactFallbackAnalyzer):
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

        self.documentary_candidates = DocumentaryCandidateIndex(
            self.db,
            biyubi_source=self.biyubi_source,
        )

    @property
    def biyubi_source_status(self) -> str:
        return self.base.biyubi_source_status

    def close(self) -> None:
        self.base.close()

    def _candidate_for_token(self, raw_token: str, token_index: int) -> dict[str, Any]:
        orthographic = self.documentary_candidates.lookup(raw_token)
        person = [asdict(x) for x in self.morph1.person_candidates(raw_token)]
        possession_obj = self.morph2.possession_candidate(raw_token)
        possession = asdict(possession_obj) if possession_obj is not None else None

        has_candidate = bool(orthographic["candidate_count"] or person or possession)
        return {
            "token_index": token_index,
            "token_raw": raw_token,
            "candidate_status": STATUS_RELATED if has_candidate else STATUS_NONE,
            "orthographic_documentary_candidates": orthographic,
            "graphical_person_candidates": person,
            "graphical_possession_candidate": possession,
            "candidate_interpretation": (
                "REVIEW_RELATION_ONLY_NOT_EXACT_ANALYSIS"
                if has_candidate
                else "NO_CONSTRAINED_CANDIDATE_FOUND_TOKEN_REMAINS_UNRESOLVED"
            ),
            "exact_surface_match_assertion": False,
            "semantic_equivalence_assertion": False,
            "correction_assertion": False,
            "orthographic_authority_assertion": False,
            "generation_license_assertion": False,
            "rule_discovery_assertion": False,
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
        exact_unresolved = list(
            result.get(
                "unresolved_token_indexes_after_voces_documentary_exact",
                result.get("unresolved_token_indexes_after_biyubi", []),
            )
        )

        rows = [
            self._candidate_for_token(tokens[index], index)
            for index in exact_unresolved
        ]
        candidate_indexes = sorted(
            row["token_index"] for row in rows if row["candidate_status"] == STATUS_RELATED
        )

        # Critical invariant: candidates do not change exact evidence state.
        result.update(
            {
                "current_adapter_version": ADAPTER_VERSION,
                "documentary_candidate_layer_enabled": True,
                "provisional_unresolved_token_candidates": rows,
                "candidate_only_token_indexes": candidate_indexes,
                "still_exactly_unresolved_token_indexes": exact_unresolved,
                "exact_evidence_state_unchanged_by_candidates": True,
            }
        )
        result.setdefault("fallback_policy", {}).update(
            {
                "candidate_layer_runs_after_exact_layers": True,
                "candidate_layer_uses_latest_exact_unresolved_boundary": True,
                "candidate_layer_does_not_promote_analysis_status": True,
                "candidate_layer_does_not_increase_effective_evidence_coverage": True,
                "candidate_layer_generic_edit_distance": False,
                "candidate_layer_near_match_ranking": False,
                "candidate_layer_rule_discovery": False,
            }
        )
        result.setdefault("limitations", []).extend(
            [
                "ORTHOGRAPHIC_VARIANT_CANDIDATE_IS_NOT_EXACT_SURFACE_EVIDENCE",
                "GRAPHICAL_PERSON_OR_POSSESSION_CANDIDATE_REQUIRES_LEMMA_OR_PARADIGM_ANCHOR",
                "CANDIDATE_LAYER_MAY_PRIORITIZE_RESEARCH_BUT_CANNOT_LICENSE_CORRECTION",
            ]
        )
        return result
