#!/usr/bin/env python3
"""Analyzer v0.35.15 — contextual documentary support view v0.1.

This wrapper activates the previously reserved `context_segments` channel in a
strictly non-resolving way. It does not reinterpret the observed surface and it
does not create a new lexical or morphological candidate.

For a verb morphological hypothesis already exposed by v0.35.13, the layer may
report that one or more tokens supplied in an explicit context segment also occur
in the Dictionaria example(s) already supporting that hypothesis.

The relation is deliberately narrow:

    EXISTING_VERB_HYPOTHESIS
      + SUPPORTING_DICTIONARIA_EXAMPLE
      + CONTEXT_TOKEN_OVERLAP_IN_SAME_EXAMPLE
      -> CONTEXTUAL_DOCUMENTARY_SUPPORT_OBSERVATION

The overlap comparison uses the same candidate-only documentary key already
used by v0.35.10: NFC + casefold + apostrophe typography unification. It does
not strip tone or diacritics and does not perform edit-distance or PDLMA→AP
conversion. The query token itself is excluded from contextual overlap so that
mere repetition of the analyzed token is not counted as contextual support.

Crucially:

    CONTEXTUAL_SUPPORT != HYPOTHESIS_RESOLUTION
    CONTEXTUAL_SUPPORT != LEXICAL_IDENTITY
    CONTEXTUAL_SUPPORT != TAM_ASSERTION
    CONTEXTUAL_SUPPORT != ROOT_SEGMENTATION
    CONTEXTUAL_SUPPORT != CORRECTION_OR_GENERATION_LICENSE

Context can annotate an already-existing hypothesis; it never changes exact
evidence metrics or `analysis_status`.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from analyzer_v0_35_10_documentary_verb_form_candidates import (
    CANDIDATE_KEY_POLICY,
    strict_documentary_key,
    tokenize_documentary_surface,
)

ADAPTER_VERSION = "0.35.15"
VIEW_VERSION = "0.1"

DICTIONARIA_SOURCE_ID = "SRC-DICTIONARIA-DIDXAZA-SPANISH-ENGLISH-DICTIONARY"
DICTIONARIA_COMMIT = "76c22cf30c23d8f4bc5c83c11013a8cb24fe0f85"

STATUS_NO_CONTEXT = "NO_EXPLICIT_CONTEXT_SURFACE_SUPPLIED"
STATUS_NO_HYPOTHESIS = "NO_EXISTING_VERB_MORPHOLOGICAL_HYPOTHESIS"
STATUS_NO_SUPPORT = "NO_CONTEXT_TOKEN_OVERLAP_IN_SUPPORTING_DOCUMENTARY_EXAMPLES"
STATUS_SUPPORT = "CONTEXTUAL_DOCUMENTARY_SUPPORT_AVAILABLE"

# Explicit contract: only these fields are read as Didxazá/context surface.
# Other dict fields are preserved upstream but ignored by this layer.
CONTEXT_SURFACE_FIELDS = ("surface", "surface_original", "didxaza")


def _extract_context_surfaces(
    context_segments: list[dict[str, Any]] | None,
) -> tuple[list[dict[str, Any]], int]:
    extracted: list[dict[str, Any]] = []
    ignored = 0
    for index, segment in enumerate(context_segments or []):
        if not isinstance(segment, dict):
            ignored += 1
            continue
        found = False
        for field in CONTEXT_SURFACE_FIELDS:
            raw = segment.get(field)
            if not isinstance(raw, str) or not raw.strip():
                continue
            extracted.append(
                {
                    "context_segment_index": index,
                    "field": field,
                    "surface_raw": raw,
                    "token_surfaces": list(tokenize_documentary_surface(raw)),
                }
            )
            found = True
            break
        if not found:
            ignored += 1
    return extracted, ignored


def _hypothesis_identity(hypothesis: dict[str, Any]) -> tuple[str, str, str]:
    return (
        str(hypothesis.get("entry_id_candidate", "")),
        str(hypothesis.get("tam_candidate", "")),
        str(hypothesis.get("root_candidate_analytical_raw", "")),
    )


class ContextualDocumentarySupportViewAnalyzer:
    """Annotate existing v0.35.13 hypotheses with documentary context overlap."""

    def __init__(self, base_analyzer: Any):
        self.base = base_analyzer
        self._example_by_id: dict[str, dict[str, Any]] = {}
        for example in self.retrieval.examples:
            example_id = str(example.get("ID", "") or "").strip()
            if example_id:
                self._example_by_id[example_id] = example

    def __getattr__(self, name: str) -> Any:
        return getattr(self.base, name)

    def close(self) -> None:
        self.base.close()

    def _support_for_hypothesis(
        self,
        hypothesis: dict[str, Any],
        *,
        query_token_raw: str,
        context_segments: list[dict[str, Any]],
    ) -> dict[str, Any]:
        query_key = strict_documentary_key(query_token_raw)
        context_occurrences: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for segment in context_segments:
            for token_surface in segment.get("token_surfaces", ()):
                key = strict_documentary_key(token_surface)
                if not key or key == query_key:
                    continue
                context_occurrences[key].append(
                    {
                        "context_segment_index": segment["context_segment_index"],
                        "context_field": segment["field"],
                        "context_token_surface_raw": token_surface,
                    }
                )

        support_rows: list[dict[str, Any]] = []
        for example_id in hypothesis.get("supporting_example_ids", ()):
            example = self._example_by_id.get(str(example_id))
            if example is None:
                continue
            primary_text = str(example.get("Primary_Text", "") or "")
            example_tokens = list(tokenize_documentary_surface(primary_text))
            example_keys: dict[str, list[str]] = defaultdict(list)
            for token_surface in example_tokens:
                key = strict_documentary_key(token_surface)
                if key and key != query_key:
                    example_keys[key].append(token_surface)

            matched_keys = sorted(set(example_keys).intersection(context_occurrences))
            if not matched_keys:
                continue
            support_rows.append(
                {
                    "example_id": str(example_id),
                    "primary_text_raw": primary_text,
                    "matched_context_keys": matched_keys,
                    "matched_context_occurrences": {
                        key: list(context_occurrences[key]) for key in matched_keys
                    },
                    "matching_example_token_surfaces_raw": {
                        key: list(example_keys[key]) for key in matched_keys
                    },
                    "candidate_key_policy": CANDIDATE_KEY_POLICY,
                    "documentary_source": DICTIONARIA_SOURCE_ID,
                    "dictionaria_commit": DICTIONARIA_COMMIT,
                    "context_supports_hypothesis_candidate": True,
                    "context_resolves_hypothesis_assertion": False,
                    "semantic_equivalence_assertion": False,
                    "token_role_assertion": False,
                    "correction_assertion": False,
                    "generation_license_assertion": False,
                }
            )

        matched_context_keys = sorted(
            {
                key
                for row in support_rows
                for key in row.get("matched_context_keys", ())
            }
        )
        return {
            "hypothesis_identity": {
                "entry_id_candidate": hypothesis.get("entry_id_candidate"),
                "tam_candidate": hypothesis.get("tam_candidate"),
                "root_candidate_analytical_raw": hypothesis.get(
                    "root_candidate_analytical_raw"
                ),
            },
            "supporting_documentary_example_count": len(support_rows),
            "supporting_documentary_examples": support_rows,
            "matched_context_keys": matched_context_keys,
            "contextual_support_available": bool(support_rows),
            "hypothesis_resolved_by_context": False,
            "hypothesis_rank_changed_by_context": False,
            "lexical_identity_assertion": False,
            "tam_assertion": False,
            "root_segmentation_assertion": False,
            "verb_class_assertion": False,
            "pdlma_to_ap_assertion": False,
            "correction_assertion": False,
            "generation_license_assertion": False,
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

        extracted_context, ignored_segment_count = _extract_context_surfaces(context_segments)
        surface_tokens = list(tokenize_documentary_surface(surface))
        hypothesis_views = result.get("verb_morphological_hypothesis_views", ())

        token_views: list[dict[str, Any]] = []
        informative: list[int] = []
        for token_index in range(int(result.get("token_count", 0) or 0)):
            hypothesis_view = (
                hypothesis_views[token_index]
                if token_index < len(hypothesis_views)
                else {"hypotheses": []}
            )
            hypotheses = list(hypothesis_view.get("hypotheses", ()))
            query_token_raw = (
                surface_tokens[token_index] if token_index < len(surface_tokens) else ""
            )

            if not extracted_context:
                status = STATUS_NO_CONTEXT
                support = []
            elif not hypotheses:
                status = STATUS_NO_HYPOTHESIS
                support = []
            else:
                support = [
                    self._support_for_hypothesis(
                        hypothesis,
                        query_token_raw=query_token_raw,
                        context_segments=extracted_context,
                    )
                    for hypothesis in hypotheses
                ]
                status = STATUS_SUPPORT if any(
                    row["contextual_support_available"] for row in support
                ) else STATUS_NO_SUPPORT

            supported_count = sum(
                1 for row in support if row.get("contextual_support_available")
            )
            view = {
                "token_index": token_index,
                "token_raw": query_token_raw,
                "status": status,
                "existing_hypothesis_count": len(hypotheses),
                "supported_hypothesis_count": supported_count,
                "hypothesis_support": support,
                "context_can_create_hypothesis": False,
                "context_can_resolve_hypothesis": False,
                "context_can_rank_hypotheses": False,
                "context_changes_exact_evidence": False,
                "context_changes_analysis_status": False,
                "correction_assertion": False,
                "generation_license_assertion": False,
            }
            token_views.append(view)
            if supported_count:
                informative.append(token_index)

        result.update(
            {
                "current_adapter_version": ADAPTER_VERSION,
                "contextual_documentary_support_view_enabled": True,
                "contextual_documentary_support_view_version": VIEW_VERSION,
                "contextual_documentary_support_views": token_views,
                "contextual_documentary_support_informative_token_indexes": informative,
                "contextual_documentary_support_context_segments_consumed": len(
                    extracted_context
                ),
                "contextual_documentary_support_context_segments_ignored": ignored_segment_count,
                "contextual_documentary_support_changes_exact_evidence_metrics": False,
                "contextual_documentary_support_changes_analysis_status": False,
                "contextual_documentary_support_resolution_enabled": False,
                "contextual_documentary_support_ranking_enabled": False,
                "contextual_documentary_support_generation_enabled": False,
                "contextual_documentary_support_correction_enabled": False,
            }
        )

        context_channel = result.setdefault("context_channel", {})
        context_channel.update(
            {
                "context_supplied": bool(context_segments),
                "context_segment_count": len(context_segments or []),
                "used_for_local_analysis": False,
                "used_for_nonresolving_documentary_support": bool(extracted_context),
                "status": (
                    "CONTEXT_USED_FOR_NONRESOLVING_DOCUMENTARY_SUPPORT_v0_35_15"
                    if extracted_context
                    else (
                        "CONTEXT_SUPPLIED_BUT_NO_SUPPORTED_SURFACE_FIELD_v0_35_15"
                        if context_segments
                        else "NO_CONTEXT_SUPPLIED_LOCAL_ANALYSIS_PROCEEDS"
                    )
                ),
            }
        )
        result.setdefault("fallback_policy", {}).update(
            {
                "contextual_documentary_support_requires_existing_hypothesis": True,
                "contextual_documentary_support_requires_existing_supporting_example": True,
                "contextual_documentary_support_excludes_query_token_repetition": True,
                "contextual_documentary_support_candidate_key_policy": CANDIDATE_KEY_POLICY,
                "contextual_documentary_support_tone_stripping": False,
                "contextual_documentary_support_diacritic_stripping": False,
                "contextual_documentary_support_edit_distance": False,
                "contextual_documentary_support_pdlma_to_ap": False,
                "contextual_documentary_support_resolves_hypothesis": False,
                "contextual_documentary_support_ranks_hypotheses": False,
                "contextual_documentary_support_rewrites_local_evidence": False,
            }
        )
        result.setdefault("limitations", []).extend(
            [
                "CONTEXT_V0_1_ONLY_CORROBORATES_EXISTING_VERB_HYPOTHESES",
                "CONTEXT_TOKEN_OVERLAP_IN_SUPPORTING_EXAMPLE_DOES_NOT_RESOLVE_HYPOTHESIS",
                "CONTEXT_DOES_NOT_CREATE_LEXICAL_OR_MORPHOLOGICAL_CANDIDATES",
                "CONTEXT_DOES_NOT_REWRITE_RAW_LOCAL_EVIDENCE_OR_ANALYSIS_STATUS",
                "CONTEXT_QUERY_TOKEN_REPETITION_IS_EXCLUDED_FROM_SUPPORT",
            ]
        )
        return result
