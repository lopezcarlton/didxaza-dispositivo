#!/usr/bin/env python3
"""Current Analyzer wrapper with optional exact Biyubi secondary-source evidence.

Biyubi is a registered secondary, non-normative source. Its controlled XLSX
payload is not stored in the public repository. When the exact registered
snapshot is mounted, this wrapper queries Biyubi only for tokens that remain
unresolved after the v0.35.2 primary + existing-layer analysis.

Biyubi attestation is evidence only. It does not license correction,
orthographic authority, generation, or rule discovery.
"""

from __future__ import annotations

import re
from typing import Any

from analyzer_v0_35_2_punctuation_light_fallback_adapter import (
    PunctuationLightExactFallbackAnalyzer,
)
from biyubi_exact_source import (
    BiyubiControlledSource,
    SOURCE_ID,
    STATUS_NO_EXACT,
)

ADAPTER_VERSION = "0.35.3"


class BiyubiExactFallbackAnalyzer:
    """Add a controlled Biyubi exact-evidence layer after v0.35.2."""

    def __init__(
        self,
        base_analyzer: PunctuationLightExactFallbackAnalyzer,
        biyubi_source: BiyubiControlledSource | None = None,
    ):
        self.base = base_analyzer
        self.biyubi_source = biyubi_source

        # Preserve public attributes expected by current callers/tests.
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
        return (
            "MOUNTED_REGISTERED_SNAPSHOT"
            if self.biyubi_source is not None
            else "NOT_MOUNTED"
        )

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
            result.get("unresolved_token_indexes_after_exact_fallback", [])
        )
        before_effective = set(result.get("effective_evidence_token_indexes", []))

        biyubi_rows: list[dict[str, Any]] = []
        biyubi_attested: set[int] = set()

        if self.biyubi_source is not None:
            for token_index in sorted(before_unresolved):
                evidence = self.biyubi_source.lookup(tokens[token_index])
                row = {"token_index": token_index, **evidence}
                biyubi_rows.append(row)
                if evidence["biyubi_status"] != STATUS_NO_EXACT:
                    biyubi_attested.add(token_index)

        unresolved_after = sorted(before_unresolved - biyubi_attested)
        effective_after = sorted(before_effective | biyubi_attested)

        if (
            result.get("analysis_status") == "ABSTAIN_NO_COMPONENT_EVIDENCE"
            and biyubi_attested
        ):
            result["analysis_status"] = "PARTIAL_ANALYSIS_NON_LICENSING"
            result["analysis_status_promotion_basis"] = (
                "BIYUBI_EXACT_SECONDARY_ATTESTATION_ONLY"
            )

        result.update(
            {
                "current_adapter_version": ADAPTER_VERSION,
                "biyubi_source_registered": True,
                "biyubi_source_id": SOURCE_ID,
                "biyubi_source_status": self.biyubi_source_status,
                "biyubi_source_snapshot_sha256": (
                    self.biyubi_source.snapshot_sha256
                    if self.biyubi_source is not None
                    else None
                ),
                "supplemental_biyubi_exact_evidence": biyubi_rows,
                "biyubi_exact_attested_token_indexes": sorted(biyubi_attested),
                "unresolved_token_indexes_before_biyubi": sorted(before_unresolved),
                "unresolved_token_indexes_after_biyubi": unresolved_after,
                "effective_evidence_after_biyubi_token_indexes": effective_after,
                "effective_evidence_after_biyubi_token_count": len(effective_after),
                "effective_evidence_after_biyubi_coverage_ratio": (
                    len(effective_after) / len(tokens) if tokens else 0.0
                ),
            }
        )
        result.setdefault("fallback_policy", {}).update(
            {
                "biyubi_registered_secondary_source": True,
                "biyubi_payload_optional_controlled_mount": True,
                "biyubi_exact_only": True,
                "biyubi_preserves_tones_diacritics_apostrophes": True,
                "biyubi_near_match": False,
                "biyubi_strip_tone": False,
                "biyubi_pdlma_to_surface": False,
                "biyubi_attestation_not_orthographic_authority": True,
                "biyubi_absence_not_incorrect": True,
            }
        )
        result.setdefault("limitations", []).extend(
            [
                "BIYUBI_IS_SECONDARY_SURFACE_EVIDENCE_NOT_ORTHOGRAPHIC_AUTHORITY",
                "BIYUBI_EXACT_ATTESTATION_IS_NOT_FULL_LEXICAL_OR_MORPHOLOGICAL_ANALYSIS",
                "BIYUBI_PAYLOAD_MUST_BE_MOUNTED_AS_REGISTERED_CONTROLLED_SNAPSHOT",
            ]
        )
        return result
