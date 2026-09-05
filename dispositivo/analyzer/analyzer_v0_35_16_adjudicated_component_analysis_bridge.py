#!/usr/bin/env python3
"""Analyzer v0.35.16 — adjudicated component-analysis bridge v0.1.

This outer wrapper exposes component analyses that have already been adjudicated
in pinned Voces knowledge. It deliberately does *not* discover components from
substrings and it does not turn runtime context into a segmentation rule.

The only productive route in v0.1 is:

    OBSERVED_TOKEN
      + NFC_EXACT_REGISTERED_SURFACE
      + VOCES_ADJUDICATED_COMPONENT_ANALYSIS
      -> CONTEXTUALLY_SUPPORTED_COMPONENT_ANALYSIS_VIEW

"Contextually supported" describes the provenance of the canonical Voces
adjudication. It does not mean that neighboring text supplied at runtime may
create or resolve a component analysis.

Crucially:

    STRING_CONTAINS_KNOWN_FORM != COMPONENT_ANALYSIS
    REGISTERED_COMPONENT_ANALYSIS != MORPHOLOGICAL_COMPOUND_DIAGNOSIS
    DOCUMENTED_BOUNDARY_VARIATION != ORTHOGRAPHIC_PREFERENCE
    COMPONENT_ANALYSIS_VIEW != EXACT_SURFACE_EVIDENCE
    COMPONENT_ANALYSIS_VIEW != CORRECTION_OR_GENERATION_LICENSE

The wrapper preserves all upstream exact-evidence metrics and `analysis_status`.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from analyzer_v0_35_10_documentary_verb_form_candidates import tokenize_documentary_surface
from voces_component_analysis_source import (
    DEFAULT_REGISTRY_PATH,
    EXPECTED_VOCES_COMMIT,
    MATCH_POLICY,
    VocesComponentAnalysisSource,
)


ADAPTER_VERSION = "0.35.16"
BRIDGE_VERSION = "0.1"
STATUS_SUPPORTED = "CONTEXTUALLY_SUPPORTED_COMPONENT_ANALYSIS"
STATUS_NONE = "NO_ADJUDICATED_COMPONENT_ANALYSIS"


class AdjudicatedComponentAnalysisBridgeAnalyzer:
    """Expose read-only Voces-adjudicated component analyses by NFC-exact surface."""

    def __init__(
        self,
        base_analyzer: Any,
        registry_path: str | Path = DEFAULT_REGISTRY_PATH,
        *,
        component_source: VocesComponentAnalysisSource | None = None,
    ):
        self.base = base_analyzer
        self.component_source = component_source or VocesComponentAnalysisSource(registry_path)

    def __getattr__(self, name: str) -> Any:
        return getattr(self.base, name)

    def close(self) -> None:
        self.base.close()

    @property
    def component_analysis_registry_stats(self) -> dict[str, object]:
        return self.component_source.stats

    def _token_view(self, token_index: int, token_raw: str) -> dict[str, Any]:
        records = self.component_source.lookup(token_raw)
        analyses = [record.as_payload() for record in records]
        return {
            "token_index": token_index,
            "token_raw": token_raw,
            "status": STATUS_SUPPORTED if analyses else STATUS_NONE,
            "analysis_count": len(analyses),
            "analyses": analyses,
            "surface_match_policy": MATCH_POLICY,
            "voces_knowledge_commit": EXPECTED_VOCES_COMMIT,
            "analysis_is_registry_adjudicated": bool(analyses),
            "analysis_discovered_from_substring": False,
            "analysis_created_from_runtime_context": False,
            "analysis_resolved_by_runtime_context": False,
            "morphological_compound_assertion": False,
            "orthographic_boundary_preference_assertion": False,
            "changes_exact_evidence": False,
            "changes_analysis_status": False,
            "correction_assertion": False,
            "generation_license_assertion": False,
            "orthographic_authority_assertion": False,
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

        token_count = int(result.get("token_count", 0) or 0)
        token_surfaces = list(tokenize_documentary_surface(surface))
        views = [
            self._token_view(
                token_index,
                token_surfaces[token_index] if token_index < len(token_surfaces) else "",
            )
            for token_index in range(token_count)
        ]
        informative = [
            view["token_index"] for view in views if view["status"] == STATUS_SUPPORTED
        ]

        result.update(
            {
                "current_adapter_version": ADAPTER_VERSION,
                "adjudicated_component_analysis_bridge_enabled": True,
                "adjudicated_component_analysis_bridge_version": BRIDGE_VERSION,
                "adjudicated_component_analysis_views": views,
                "adjudicated_component_analysis_informative_token_indexes": informative,
                "adjudicated_component_analysis_registry_stats": self.component_source.stats,
                "adjudicated_component_analysis_changes_exact_evidence_metrics": False,
                "adjudicated_component_analysis_changes_analysis_status": False,
                "adjudicated_component_analysis_discovery_enabled": False,
                "adjudicated_component_analysis_runtime_context_resolution_enabled": False,
                "adjudicated_component_analysis_generation_enabled": False,
                "adjudicated_component_analysis_correction_enabled": False,
            }
        )
        result.setdefault("fallback_policy", {}).update(
            {
                "component_analysis_requires_voces_adjudicated_registry_row": True,
                "component_analysis_surface_match_policy": MATCH_POLICY,
                "component_analysis_nfc_only": True,
                "component_analysis_casefold": False,
                "component_analysis_apostrophe_unification": False,
                "component_analysis_tone_stripping": False,
                "component_analysis_diacritic_stripping": False,
                "component_analysis_substring_discovery": False,
                "component_analysis_near_match": False,
                "component_analysis_edit_distance": False,
                "component_analysis_pdlma_to_ap": False,
                "component_analysis_runtime_context_can_create": False,
                "component_analysis_runtime_context_can_resolve": False,
                "component_analysis_implies_morphological_compound": False,
                "component_analysis_implies_orthographic_boundary_preference": False,
                "component_analysis_rewrites_local_evidence": False,
                "component_analysis_changes_analysis_status": False,
                "component_analysis_generation": False,
                "component_analysis_correction": False,
            }
        )
        result.setdefault("limitations", []).extend(
            [
                "COMPONENT_ANALYSIS_V0_1_ONLY_EXPOSES_VOCES_ADJUDICATED_MAPPINGS",
                "COMPONENT_ANALYSIS_V0_1_DOES_NOT_DISCOVER_SPLITS_FROM_SUBSTRINGS",
                "RUNTIME_CONTEXT_DOES_NOT_CREATE_OR_RESOLVE_COMPONENT_ANALYSES_V0_1",
                "COMPONENT_ANALYSIS_DOES_NOT_ASSERT_MORPHOLOGICAL_COMPOUND_STATUS",
                "COMPONENT_ANALYSIS_DOES_NOT_SELECT_ORTHOGRAPHIC_BOUNDARY",
                "COMPONENT_ANALYSIS_DOES_NOT_REWRITE_RAW_LOCAL_EVIDENCE_OR_ANALYSIS_STATUS",
            ]
        )
        return result
