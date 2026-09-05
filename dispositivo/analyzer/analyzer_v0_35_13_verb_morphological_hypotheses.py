#!/usr/bin/env python3
"""Analyzer v0.35.13 — verb morphological hypothesis view v0.1.

This wrapper creates no new morphological relation. It turns the analytical
coordinates already emitted by VerbAnalysisBridge v0.2 (v0.35.10) into an
explicit per-token hypothesis view:

    observed AP documentary token
      -> compatible Dictionaria verb entry candidate
      -> TAM candidate(s)
      -> analytical root candidate
      -> documented verb-class candidate
      -> documented PDLMA coordinate(s)

The underlying v0.35.10 relation is already constrained by an AP token in a
Dictionaria example, a unique verb-entry link for that example, and a matching
PDLMA TAM form under its narrow ASCII-hyphen-collapse candidate operation.
This layer does not strengthen that relation into a fact.

In particular:
- candidate TAM != asserted TAM of the observed token;
- analytical root != asserted surface segmentation;
- documented class of a compatible entry != asserted class of the token;
- PDLMA analytical coordinates != project orthographic surface;
- no candidate changes exact evidence or analysis status;
- no correction, generation, orthographic authority or rule-discovery license.

PBK2016 / HALL-0073 and HALL-0074 motivate exposing TAM/root/class coordinates;
HALL-0076 blocks blind projection from the analytical notation to AP surface.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any

ADAPTER_VERSION = "0.35.13"
VIEW_VERSION = "0.1"

VOCES_KNOWLEDGE_COMMIT = "f17c5363caada6f8beb18fa99c39e37cd72c6f09"
PBK_SOURCE_ID = "SRC-PEREZ-BAEZ-KAUFMAN-2016-VERB-CLASSES"
DICTIONARIA_SOURCE_ID = "SRC-DICTIONARIA-DIDXAZA-SPANISH-ENGLISH-DICTIONARY"
HALL_IDS = ("HALL-0073", "HALL-0074", "HALL-0076")

STATUS_UNIQUE = "UNIQUE_DOCUMENTARY_MORPHOLOGICAL_HYPOTHESIS"
STATUS_MULTIPLE = "MULTIPLE_DOCUMENTARY_MORPHOLOGICAL_HYPOTHESES"
STATUS_NONE = "NO_DOCUMENTARY_MORPHOLOGICAL_HYPOTHESIS"


def _hypothesis_key(entry: dict[str, Any], tam: str) -> tuple[str, str, str]:
    return (
        str(entry.get("entry_id", "")),
        str(tam or ""),
        str(entry.get("root_analysis_raw", "")),
    )


def _candidate_hypotheses(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    """Expand one v0.35.10 candidate into explicit non-licensing hypotheses."""
    out: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()
    for entry in candidate.get("compatible_verb_entries", ()):
        for tam in entry.get("tam_candidates", ()):
            key = _hypothesis_key(entry, str(tam))
            if key in seen:
                continue
            seen.add(key)
            pdlma_variants = list(
                (entry.get("matching_documented_pdlma_variants") or {}).get(str(tam), ())
            )
            out.append(
                {
                    "entry_id_candidate": entry.get("entry_id"),
                    "documented_headword_raw": entry.get("documented_headword_raw"),
                    "definition_es": entry.get("definition_es"),
                    "tam_candidate": str(tam),
                    "root_candidate_analytical_raw": entry.get("root_analysis_raw"),
                    "verb_class_candidate": entry.get("verb_class"),
                    "verb_class_record_status": entry.get("class_status"),
                    "irregular_record": entry.get("irregular"),
                    "pdlma_citation_raw": entry.get("pdlma_citation_raw"),
                    "matching_documented_pdlma_variants_raw": pdlma_variants,
                    "supporting_example_ids": list(entry.get("supporting_example_ids", ())),
                    "supporting_example_count": int(entry.get("supporting_example_count", 0) or 0),
                    "supporting_ap_token_raw_nfc_exact": bool(
                        entry.get("query_matches_supporting_ap_token_raw_nfc_exact")
                    ),
                    "association_strength": entry.get("association_strength"),
                    "epistemic_status": "DOCUMENTARY_STRUCTURAL_HYPOTHESIS_ONLY",
                    "observed_token_is_verb_assertion": False,
                    "tam_of_observed_token_assertion": False,
                    "root_segmentation_of_observed_token_assertion": False,
                    "verb_class_of_observed_token_assertion": False,
                    "pdlma_to_ap_assertion": False,
                    "semantic_equivalence_assertion": False,
                    "correction_assertion": False,
                    "generation_license_assertion": False,
                    "orthographic_authority_assertion": False,
                    "rule_discovery_assertion": False,
                    "provenance": {
                        "documentary_source": DICTIONARIA_SOURCE_ID,
                        "verb_class_system_authority": PBK_SOURCE_ID,
                        "voces_hall_ids": list(HALL_IDS),
                        "voces_knowledge_commit": VOCES_KNOWLEDGE_COMMIT,
                        "upstream_candidate_status": candidate.get("candidate_status"),
                        "upstream_candidate_key_policy": candidate.get("candidate_key_policy"),
                    },
                }
            )
    return out


class VerbMorphologicalHypothesisViewAnalyzer:
    """Expose v0.35.10 TAM/root/class coordinates as explicit hypotheses."""

    def __init__(self, base_analyzer: Any):
        self.base = base_analyzer

    def __getattr__(self, name: str) -> Any:
        return getattr(self.base, name)

    def close(self) -> None:
        self.base.close()

    @staticmethod
    def _token_view(
        token_index: int,
        candidates: list[dict[str, Any]],
    ) -> dict[str, Any]:
        hypotheses: list[dict[str, Any]] = []
        seen: set[tuple[str, str, str]] = set()
        raw_exact_documentary_support = False
        for candidate in candidates:
            raw_exact_documentary_support = raw_exact_documentary_support or bool(
                candidate.get("raw_nfc_exact_documentary_token_attestation")
            )
            for hypothesis in _candidate_hypotheses(candidate):
                key = (
                    str(hypothesis.get("entry_id_candidate", "")),
                    str(hypothesis.get("tam_candidate", "")),
                    str(hypothesis.get("root_candidate_analytical_raw", "")),
                )
                if key in seen:
                    continue
                seen.add(key)
                hypotheses.append(hypothesis)

        if not hypotheses:
            status = STATUS_NONE
        elif len(hypotheses) == 1:
            status = STATUS_UNIQUE
        else:
            status = STATUS_MULTIPLE

        entry_ids = sorted(
            {
                str(row["entry_id_candidate"])
                for row in hypotheses
                if row.get("entry_id_candidate")
            }
        )
        tam_candidates = sorted({row["tam_candidate"] for row in hypotheses})
        roots = sorted(
            {
                str(row["root_candidate_analytical_raw"])
                for row in hypotheses
                if row.get("root_candidate_analytical_raw")
            }
        )
        classes = sorted(
            {
                str(row["verb_class_candidate"])
                for row in hypotheses
                if row.get("verb_class_candidate")
            }
        )
        return {
            "token_index": token_index,
            "status": status,
            "hypothesis_count": len(hypotheses),
            "hypotheses": hypotheses,
            "compatible_entry_ids": entry_ids,
            "tam_candidates": tam_candidates,
            "root_candidates_analytical_raw": roots,
            "verb_class_candidates": classes,
            "raw_exact_documentary_example_token_support": raw_exact_documentary_support,
            "candidate_view_only": True,
            "candidate_is_fact": False,
            "candidate_resolves_token": False,
            "candidate_changes_exact_evidence": False,
            "candidate_changes_analysis_status": False,
            "surface_prefix_segmentation_assertion": False,
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
        token_count = int(result.get("token_count", 0) or 0)
        by_token: dict[int, list[dict[str, Any]]] = defaultdict(list)
        for candidate in result.get("documentary_verb_form_candidates", ()):
            by_token[int(candidate["token_index"])].append(candidate)

        views = [
            self._token_view(token_index, by_token.get(token_index, []))
            for token_index in range(token_count)
        ]
        informative = [row["token_index"] for row in views if row["hypothesis_count"]]

        result.update(
            {
                "current_adapter_version": ADAPTER_VERSION,
                "verb_morphological_hypothesis_view_enabled": True,
                "verb_morphological_hypothesis_view_version": VIEW_VERSION,
                "verb_morphological_hypothesis_views": views,
                "verb_morphological_hypothesis_informative_token_indexes": informative,
                "verb_morphological_hypothesis_changes_exact_evidence_metrics": False,
                "verb_morphological_hypothesis_changes_analysis_status": False,
                "verb_morphological_hypothesis_generation_enabled": False,
                "verb_morphological_hypothesis_correction_enabled": False,
            }
        )
        result.setdefault("fallback_policy", {}).update(
            {
                "verb_morphological_hypothesis_upstream_v03510_only": True,
                "verb_morphological_hypothesis_tam_is_assertion": False,
                "verb_morphological_hypothesis_root_is_surface_segmentation": False,
                "verb_morphological_hypothesis_class_is_token_assignment": False,
                "verb_morphological_hypothesis_visible_prefix_segmentation": False,
                "verb_morphological_hypothesis_pdlma_to_ap": False,
                "verb_morphological_hypothesis_generation": False,
                "verb_morphological_hypothesis_correction": False,
            }
        )
        result.setdefault("limitations", []).extend(
            [
                "VERB_MORPH_HYPOTHESIS_V0_1_REEXPRESSES_ONLY_V03510_DOCUMENTARY_COORDINATES",
                "TAM_CANDIDATE_IS_NOT_ASSERTED_TAM_OF_OBSERVED_TOKEN",
                "ROOT_CANDIDATE_IS_NOT_ASSERTED_SURFACE_SEGMENTATION",
                "VERB_CLASS_CANDIDATE_IS_NOT_ASSERTED_CLASS_OF_OBSERVED_TOKEN",
                "PDLMA_ANALYTICAL_COORDINATE_IS_NOT_PROJECT_ORTHOGRAPHIC_SURFACE",
                "VERB_MORPH_HYPOTHESIS_DOES_NOT_SEGMENT_VISIBLE_PREFIXES",
            ]
        )
        return result
