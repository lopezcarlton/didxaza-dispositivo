#!/usr/bin/env python3
"""Current exact fallback adapter with punctuation-light token lookup.

REAL_TEXT_PROBE_002 demonstrated that otherwise exact existing-layer evidence
could be missed when sentence punctuation remained attached to a token (for
example a comma or final period). This wrapper preserves v0.35.1 behavior but
uses the same non-destructive punctuation-light comparison index already used
by the primary retrieval layer before exact fallback lookup.

No punctuation is written back to the input, no orthographic correction is
asserted, and unresolved remains distinct from incorrect.
"""

from __future__ import annotations

from typing import Any

from analyzer_v0_35_1_exact_fallback_adapter import (
    ExactExistingLayerFallbackAnalyzer,
)

ADAPTER_VERSION = "0.35.2"


class PunctuationLightExactFallbackAnalyzer(ExactExistingLayerFallbackAnalyzer):
    """Apply punctuation-light comparison only to exact fallback lookup keys."""

    def __init__(self, base_analyzer: Any):
        super().__init__(base_analyzer)
        from didxaza_runtime_v0_2_1_retrieval import punctuation_light_index

        self._punctuation_light_index = punctuation_light_index

    def _fallback_for_token(self, raw_token: str, token_index: int) -> dict[str, Any]:
        lookup_key = self._punctuation_light_index(raw_token)
        result = super()._fallback_for_token(lookup_key, token_index)

        # Restore the untouched source token while exposing the comparison key.
        result["token_raw"] = raw_token
        result["segmental_lookup_key"] = lookup_key
        result["punctuation_light_lookup_key"] = lookup_key
        result["lookup_normalization"] = "PUNCTUATION_LIGHT_INDEX"
        result["evidence_basis"] = (
            "EXACT_EXISTING_LAYER_LOOKUP_AFTER_NONDESTRUCTIVE_PUNCTUATION_LIGHT_INDEX"
        )
        return result

    def analyze(
        self,
        surface: str,
        *,
        item_id: str | None = None,
        spanish_supplied: str | None = None,
        context_segments: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        result = super().analyze(
            surface,
            item_id=item_id,
            spanish_supplied=spanish_supplied,
            context_segments=context_segments,
        )
        result["current_adapter_version"] = ADAPTER_VERSION
        result.setdefault("fallback_policy", {}).update(
            {
                "punctuation_light_lookup_enabled": True,
                "punctuation_is_comparison_only_not_input_rewrite": True,
            }
        )
        result.setdefault("limitations", []).append(
            "PUNCTUATION_LIGHT_FALLBACK_IS_COMPARISON_ONLY_NOT_ORTHOGRAPHIC_NORMALIZATION"
        )
        return result
