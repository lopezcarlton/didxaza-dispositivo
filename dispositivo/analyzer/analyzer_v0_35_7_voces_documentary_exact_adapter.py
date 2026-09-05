#!/usr/bin/env python3
"""Analyzer v0.35.7: exact documentary surfaces already promoted in Voces.

This layer runs after existing exact layers and optional Biyubi, but before
candidate or rule-based morphology layers. It adds exact *documentary surface
attestation* only. It never converts that attestation into a lexical identity,
morphological segmentation, correction, generation license, orthographic
authority, or rule-discovery authority.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from analyzer_v0_35_3_biyubi_exact_fallback_adapter import BiyubiExactFallbackAnalyzer
from voces_exact_documentary_source import (
    STATUS_NO_EXACT,
    VocesExactDocumentarySource,
)

ADAPTER_VERSION = "0.35.7"
DEFAULT_REGISTRY_PATH = (
    Path(__file__).resolve().parent.parent
    / "sources"
    / "VOCES_EXACT_DOCUMENTARY_ATTESTATIONS_v0_1.csv"
)


class VocesDocumentaryExactFallbackAnalyzer:
    def __init__(
        self,
        base_analyzer: BiyubiExactFallbackAnalyzer,
        registry_path: str | Path = DEFAULT_REGISTRY_PATH,
    ):
        self.base = base_analyzer
        self.biyubi_source = base_analyzer.biyubi_source
        self.voces_documentary_source = VocesExactDocumentarySource(registry_path)

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

    @property
    def biyubi_source_status(self) -> str:
        return self.base.biyubi_source_status

    def close(self) -> None:
        self.base.close()

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
        before_unresolved = set(
            result.get("unresolved_token_indexes_after_biyubi", [])
        )
        before_effective = set(
            result.get("effective_evidence_after_biyubi_token_indexes", [])
        )

        rows: list[dict[str, Any]] = []
        attested: set[int] = set()
        for token_index in sorted(before_unresolved):
            evidence = self.voces_documentary_source.lookup(tokens[token_index])
            rows.append(
                {
                    "token_index": token_index,
                    "token_raw": tokens[token_index],
                    **evidence,
                }
            )
            if evidence["voces_documentary_status"] != STATUS_NO_EXACT:
                attested.add(token_index)

        unresolved_after = sorted(before_unresolved - attested)
        effective_after = sorted(before_effective | attested)

        if result.get("analysis_status") == "ABSTAIN_NO_COMPONENT_EVIDENCE" and attested:
            result["analysis_status"] = "PARTIAL_ANALYSIS_NON_LICENSING"
            result["analysis_status_promotion_basis"] = (
                "VOCES_PROMOTED_DOCUMENTARY_EXACT_SURFACE_ATTESTATION_ONLY"
            )

        result.update(
            {
                "current_adapter_version": ADAPTER_VERSION,
                "voces_documentary_exact_layer_enabled": True,
                "voces_documentary_registry_path": str(
                    self.voces_documentary_source.registry_path
                ),
                "voces_documentary_registry_record_count": (
                    self.voces_documentary_source.record_count
                ),
                "supplemental_voces_documentary_exact_evidence": rows,
                "voces_documentary_exact_attested_token_indexes": sorted(attested),
                "unresolved_token_indexes_before_voces_documentary_exact": sorted(
                    before_unresolved
                ),
                "unresolved_token_indexes_after_voces_documentary_exact": unresolved_after,
                "effective_evidence_after_voces_documentary_exact_token_indexes": effective_after,
                "effective_evidence_after_voces_documentary_exact_token_count": len(
                    effective_after
                ),
                "effective_evidence_after_voces_documentary_exact_coverage_ratio": (
                    len(effective_after) / len(tokens) if tokens else 0.0
                ),
            }
        )
        result.setdefault("fallback_policy", {}).update(
            {
                "voces_documentary_exact_requires_promoted_hall": True,
                "voces_documentary_exact_nfc_only": True,
                "voces_documentary_exact_casefold": False,
                "voces_documentary_exact_punctuation_stripping": False,
                "voces_documentary_exact_tone_stripping": False,
                "voces_documentary_exact_diacritic_stripping": False,
                "voces_documentary_exact_near_match": False,
                "voces_documentary_exact_pdlma_to_surface": False,
                "voces_documentary_attestation_not_morphological_analysis": True,
                "voces_documentary_attestation_not_orthographic_authority": True,
            }
        )
        result.setdefault("limitations", []).extend(
            [
                "VOCES_DOCUMENTARY_EXACT_ATTESTATION_IS_NOT_FULL_LEXICAL_OR_MORPHOLOGICAL_ANALYSIS",
                "VOCES_DOCUMENTARY_EXACT_ATTESTATION_DOES_NOT_LICENSE_CORRECTION_OR_GENERATION",
            ]
        )
        return result
