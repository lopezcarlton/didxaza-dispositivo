#!/usr/bin/env python3
"""Current migrated Analyzer wrapper with exact existing-layer fallback.

This module does not rewrite the historical v0.35 orchestrator. It wraps that
engine and, only for tokens not covered by the primary Analyzer, consults
existing exact/segmental evidence already materialized in the runtime SQLite.

The fallback is evidence retrieval only. It does not promote an attestation to
full lexical, morphological, syntactic, orthographic, correction, generation,
or research authority.
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from typing import Any

ADAPTER_VERSION = "0.35.1"
FALLBACK_STATUS_ATTESTED = "ATTESTED_OUTSIDE_PRIMARY_LEXICON"
FALLBACK_STATUS_UNRESOLVED = "UNRESOLVED_NO_EXACT_EXISTING_LAYER_EVIDENCE"
MAX_EVIDENCE_ROWS_PER_LAYER = 20


class ExactExistingLayerFallbackAnalyzer:
    """Wrap the migrated v0.35 Analyzer with a non-licensing exact fallback."""

    def __init__(self, base_analyzer: Any):
        self.base = base_analyzer

        # Preserve the public attributes used by migrated-state checks and
        # existing callers.
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

        # The historical analyzer constructor has already made the runtime
        # importable. Reuse its exact segmental comparison function rather than
        # creating a competing normalization rule here.
        from didxaza_runtime_v0_2_1_retrieval import segmental_index

        self._segmental_index = segmental_index
        self._pickett_by_segmental_key = self._build_pickett_index()

    def close(self) -> None:
        self.base.close()

    def _build_pickett_index(self) -> dict[str, list[dict[str, Any]]]:
        by_key: dict[str, list[dict[str, Any]]] = defaultdict(list)
        rows = self.db.execute(
            "select record_id,headword_raw_2007,surface_2013_reconciled,"
            "primary_surface_2013_reconciled,variants_json,source_id,"
            "source_edition_extracted,reconciliation_status "
            "from pickett_lexical_record_v0211"
        )
        for row in rows:
            values = [row[1], row[2], row[3]]
            try:
                variants = json.loads(row[4] or "[]")
                if isinstance(variants, list):
                    values.extend(variants)
            except Exception:
                pass

            record = {
                "record_id": row[0],
                "headword_raw_2007": row[1],
                "surface_2013_reconciled": row[2],
                "primary_surface_2013_reconciled": row[3],
                "source_id": row[5],
                "source_edition_extracted": row[6],
                "reconciliation_status": row[7],
            }
            seen_keys: set[str] = set()
            for value in values:
                key = self._segmental_index(str(value or ""))
                if not key or key in seen_keys:
                    continue
                seen_keys.add(key)
                by_key[key].append(record)
        return dict(by_key)

    def _query_rows(self, sql: str, params: tuple[Any, ...]) -> list[tuple[Any, ...]]:
        return list(self.db.execute(sql, params))

    def _fallback_for_token(self, raw_token: str, token_index: int) -> dict[str, Any]:
        key = self._segmental_index(raw_token)

        surface_rows = self._query_rows(
            "select source_kind,source_id,entry_id,example_id "
            "from surface_attestation_v029 where surface_key=? "
            "order by source_kind,entry_id,example_id",
            (key,),
        )
        cross_rows = self._query_rows(
            "select surface_key,pickett_record_ids_json,dictionaria_refs_json,source_ids_json "
            "from cross_source_exact_surface_v0212 where surface_key=?",
            (key,),
        )
        documentary_rows = self._query_rows(
            "select alignment_id,analysis_type,analysis_value,source_id,source_location,status "
            "from documentary_alignment_v0210 where surface_key=? order by alignment_id",
            (key,),
        )
        pickett_rows = self._pickett_by_segmental_key.get(key, [])

        evidence_counts = {
            "surface_attestation_v029": len(surface_rows),
            "cross_source_exact_surface_v0212": len(cross_rows),
            "documentary_alignment_v0210": len(documentary_rows),
            "pickett_lexical_record_v0211": len(pickett_rows),
        }
        evidence_present = any(evidence_counts.values())

        evidence = {
            "surface_attestation_v029": [
                {
                    "source_kind": row[0],
                    "source_id": row[1],
                    "entry_id": row[2],
                    "example_id": row[3],
                }
                for row in surface_rows[:MAX_EVIDENCE_ROWS_PER_LAYER]
            ],
            "cross_source_exact_surface_v0212": [
                {
                    "surface_key": row[0],
                    "pickett_record_ids_json": row[1],
                    "dictionaria_refs_json": row[2],
                    "source_ids_json": row[3],
                }
                for row in cross_rows[:MAX_EVIDENCE_ROWS_PER_LAYER]
            ],
            "documentary_alignment_v0210": [
                {
                    "alignment_id": row[0],
                    "analysis_type": row[1],
                    "analysis_value": row[2],
                    "source_id": row[3],
                    "source_location": row[4],
                    "status": row[5],
                }
                for row in documentary_rows[:MAX_EVIDENCE_ROWS_PER_LAYER]
            ],
            "pickett_lexical_record_v0211": pickett_rows[:MAX_EVIDENCE_ROWS_PER_LAYER],
        }
        source_ids = sorted(
            {
                str(item.get("source_id"))
                for rows in evidence.values()
                for item in rows
                if item.get("source_id")
            }
        )

        return {
            "token_index": token_index,
            "token_raw": raw_token,
            "segmental_lookup_key": key,
            "fallback_status": (
                FALLBACK_STATUS_ATTESTED if evidence_present else FALLBACK_STATUS_UNRESOLVED
            ),
            "evidence_basis": "EXACT_SEGMENTAL_EXISTING_LAYER_LOOKUP",
            "evidence_counts": evidence_counts,
            "source_ids": source_ids,
            "evidence": evidence,
            "evidence_rows_capped_per_layer": MAX_EVIDENCE_ROWS_PER_LAYER,
            "interpretation": (
                "ATTESTATION_ONLY_NOT_FULL_LEXICAL_OR_MORPHOLOGICAL_ANALYSIS"
                if evidence_present
                else "NO_EXACT_EXISTING_LAYER_EVIDENCE_FOUND_NOT_AN_INCORRECTNESS_CLAIM"
            ),
            "generation_license_assertion": False,
            "correction_assertion": False,
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
        primary_status = result["analysis_status"]
        primary_matched = set(result.get("matched_token_indexes", []))
        tokens = [match.group(0) for match in re.finditer(r"\S+", surface or "")]

        fallback = [
            self._fallback_for_token(token, index)
            for index, token in enumerate(tokens)
            if index not in primary_matched
        ]
        fallback_attested = {
            item["token_index"]
            for item in fallback
            if item["fallback_status"] == FALLBACK_STATUS_ATTESTED
        }
        unresolved = {
            item["token_index"]
            for item in fallback
            if item["fallback_status"] == FALLBACK_STATUS_UNRESOLVED
        }
        effective = sorted(primary_matched | fallback_attested)

        # Preserve the historical primary status separately. If the historical
        # Analyzer abstained but exact existing-layer evidence is present, the
        # current adapter may report partial non-licensing evidence while
        # recording that this promotion came only from the fallback layer.
        if primary_status == "ABSTAIN_NO_COMPONENT_EVIDENCE" and fallback_attested:
            result["analysis_status"] = "PARTIAL_ANALYSIS_NON_LICENSING"
            result["analysis_status_promotion_basis"] = (
                "EXACT_EXISTING_LAYER_ATTESTATION_ONLY"
            )
        else:
            result["analysis_status_promotion_basis"] = None

        result.update(
            {
                "primary_analysis_status": primary_status,
                "current_adapter_version": ADAPTER_VERSION,
                "exact_existing_layer_fallback_enabled": True,
                "supplemental_exact_existing_layer_evidence": fallback,
                "supplemental_exact_attested_token_indexes": sorted(fallback_attested),
                "unresolved_token_indexes_after_exact_fallback": sorted(unresolved),
                "effective_evidence_token_indexes": effective,
                "effective_evidence_token_count": len(effective),
                "effective_evidence_coverage_ratio": (
                    len(effective) / len(tokens) if tokens else 0.0
                ),
                "fallback_policy": {
                    "primary_match_fields_preserved": True,
                    "matched_token_count_not_inflated_by_fallback": True,
                    "exact_segmental_attestation_not_full_analysis": True,
                    "unresolved_not_incorrect": True,
                    "cor001_benchmark_allowed": False,
                },
            }
        )
        result.setdefault("limitations", []).extend(
            [
                "EXACT_FALLBACK_ATTESTATION_IS_NOT_FULL_LEXICAL_OR_MORPHOLOGICAL_ANALYSIS",
                "EXACT_FALLBACK_DOES_NOT_AUTHORIZE_ORTHOGRAPHIC_CORRECTION",
                "UNRESOLVED_AFTER_EXACT_FALLBACK_IS_NOT_INCORRECT",
            ]
        )
        return result
