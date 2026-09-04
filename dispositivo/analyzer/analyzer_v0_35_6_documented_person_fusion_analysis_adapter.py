#!/usr/bin/env python3
"""Analyzer v0.35.6: promote source-backed 1SG fusion candidates only when
orthographic prosody is independently licensed.

Knowledge authority:
- VOCES HALL-0022 (commit c555732061cfb4bc29a8fa7f746b3bc4157c1fcb)
- BIB004 Gramática Popular, §3.6 and Cuadro 17

The rule is deliberately narrow:
1. an unresolved observed token ends in ``e'``;
2. v0.35.5 reverse-links it by exactly ``e' -> i`` to a documented habitual
   verb headword;
3. the documented headword is a single orthographic word, ends in plain ``i``,
   contains no written stress accent or glottal mark, and has at least two vowel
   nuclei;
4. under GP §3.6, Spanish stress-marking rules apply to diidxazá, so such an
   unaccented vowel-final polysyllabic headword is orthographically licensed as
   grave;
5. GP Cuadro 17 documents final ``i -> e'`` in 1SG for grave words.

This is ANALYSIS of an observed surface, not free paradigm generation. Exact
surface-evidence metrics remain unchanged and are reported separately.
"""

from __future__ import annotations

import re
import unicodedata
from typing import Any

from analyzer_v0_35_5_person_fusion_candidate_adapter import (
    PersonFusionCandidateAnalyzer,
    STATUS_PERSON_FUSION_CANDIDATE,
)

ADAPTER_VERSION = "0.35.6"
ANALYSIS_STATUS = "DOCUMENTED_1SG_PERSON_FUSION_ANALYSIS"
KNOWLEDGE_RULE_ID = "HALL-0022"
KNOWLEDGE_COMMIT = "c555732061cfb4bc29a8fa7f746b3bc4157c1fcb"
GP_RULE_ID = "JLC-PERS-002"
GP_SOURCE_ID = "BIB004_GRAMATICA_POPULAR"
GP_PERSON_SOURCE_LOCATION = "Cuadro 17"
GP_STRESS_SOURCE_LOCATION = "§3.6 El acento"

_APOSTROPHES = "'’ꞌʼ‘`"
_STRESS_ACCENTS = set("áéíóúÁÉÍÓÚ")
_VOWELS = set("aeiouáéíóúàèìòùäëïöüâêîôûAEIOUÁÉÍÓÚÀÈÌÒÙÄËÏÖÜÂÊÎÔÛ")


def _vowel_nucleus_count(text: str) -> int:
    """Conservative orthographic vowel-nucleus count.

    Consecutive vowel letters are treated as one nucleus here. This helper is
    used only as a blocker against monosyllables; it is not a general syllabifier.
    """

    count = 0
    in_vowel = False
    for ch in unicodedata.normalize("NFC", text or ""):
        is_vowel = ch in _VOWELS
        if is_vowel and not in_vowel:
            count += 1
        in_vowel = is_vowel
    return count


def _orthographically_licensed_grave_final_i(headword_raw: str) -> tuple[bool, dict[str, Any]]:
    raw = unicodedata.normalize("NFC", str(headword_raw or "").strip())
    blockers: list[str] = []

    if not raw or re.search(r"\s", raw):
        blockers.append("NOT_SINGLE_ORTHOGRAPHIC_WORD")
    if not raw.casefold().endswith("i"):
        blockers.append("HEADWORD_DOES_NOT_END_PLAIN_I")
    if any(ch in _STRESS_ACCENTS for ch in raw):
        blockers.append("WRITTEN_STRESS_ACCENT_PRESENT")
    if any(ch in _APOSTROPHES for ch in raw):
        blockers.append("GLOTTAL_MARK_PRESENT_PROSODIC_PATH_NOT_THIS_RULE")
    nuclei = _vowel_nucleus_count(raw)
    if nuclei < 2:
        blockers.append("MONOSYLLABLE_OR_UNDERDETERMINED_SYLLABLE_COUNT")

    licensed = not blockers
    return licensed, {
        "headword_raw": headword_raw,
        "orthographic_vowel_nucleus_count_minimum_estimate": nuclei,
        "written_stress_accent_present": any(ch in _STRESS_ACCENTS for ch in raw),
        "glottal_mark_present": any(ch in _APOSTROPHES for ch in raw),
        "ends_plain_i": raw.casefold().endswith("i"),
        "single_orthographic_word": bool(raw) and not bool(re.search(r"\s", raw)),
        "prosodic_license_status": (
            "GRAVE_LICENSED_BY_GP_SPANISH_STRESS_ORTHOGRAPHY"
            if licensed
            else "NOT_LICENSED_BY_THIS_NARROW_RULE"
        ),
        "blockers": blockers,
        "source_id": GP_SOURCE_ID,
        "source_location": GP_STRESS_SOURCE_LOCATION,
    }


class DocumentedPersonFusionAnalysisAnalyzer:
    """Promote only fully source-licensed v0.35.5 1SG candidates."""

    def __init__(self, base_analyzer: PersonFusionCandidateAnalyzer):
        self.base = base_analyzer
        self.biyubi_source = base_analyzer.biyubi_source

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

        exact_unresolved = set(result.get("still_exactly_unresolved_token_indexes", []))
        exact_effective = set(result.get("effective_evidence_after_biyubi_token_indexes", []))
        analyses: list[dict[str, Any]] = []
        analyzed_indexes: set[int] = set()

        for candidate in result.get("supplemental_documented_person_fusion_candidates", []):
            if candidate.get("candidate_status") != STATUS_PERSON_FUSION_CANDIDATE:
                continue
            token_index = int(candidate["token_index"])
            if token_index not in exact_unresolved:
                continue

            licensed, prosody = _orthographically_licensed_grave_final_i(
                candidate.get("documented_headword_raw", "")
            )
            if not licensed:
                continue

            analyses.append(
                {
                    "token_index": token_index,
                    "token_raw": candidate.get("token_raw"),
                    "analysis_status": ANALYSIS_STATUS,
                    "person": "1SG",
                    "documented_lemma_entry_id": candidate.get("documented_entry_id"),
                    "documented_lemma_surface": candidate.get("documented_headword_raw"),
                    "documented_definition_es": candidate.get("documented_definition_es"),
                    "observed_surface_relation": "FINAL_I_TO_E_GLOTTAL_1SG",
                    "person_fusion_rule": {
                        "rule_id": GP_RULE_ID,
                        "source_id": GP_SOURCE_ID,
                        "source_location": GP_PERSON_SOURCE_LOCATION,
                        "statement": "grave final i -> e' in 1SG",
                    },
                    "orthographic_prosody_license": prosody,
                    "knowledge_authority": {
                        "repository": "lopezcarlton/vocesdelasnubes",
                        "record_id": KNOWLEDGE_RULE_ID,
                        "commit": KNOWLEDGE_COMMIT,
                    },
                    "recognition_basis": (
                        "DOCUMENTED_LEMMA_PLUS_GP_1SG_FUSION_PLUS_GP_STRESS_ORTHOGRAPHY"
                    ),
                    "epistemic_status": "SOURCE_DOCUMENTED_RULE_APPLICATION_TO_OBSERVED_SURFACE",
                    "observed_surface_preserved": True,
                    "generated_surface": False,
                    "exact_surface_match_assertion": False,
                    "correction_assertion": False,
                    "orthographic_authority_assertion": False,
                    "generation_license_assertion": False,
                    "rule_discovery_assertion": False,
                }
            )
            analyzed_indexes.add(token_index)

        unresolved_after = sorted(exact_unresolved - analyzed_indexes)
        effective_analysis = sorted(exact_effective | analyzed_indexes)

        primary_status = result.get("analysis_status")
        if primary_status == "ABSTAIN_NO_COMPONENT_EVIDENCE" and analyses:
            result["analysis_status"] = "PARTIAL_ANALYSIS_NON_LICENSING"
            result["analysis_status_promotion_basis"] = (
                "DOCUMENTED_MORPHOLOGICAL_RULE_APPLICATION_TO_OBSERVED_SURFACE"
            )

        result.update(
            {
                "current_adapter_version": ADAPTER_VERSION,
                "documented_person_fusion_analysis_enabled": True,
                "documented_person_fusion_analyses": analyses,
                "documented_person_fusion_analyzed_token_indexes": sorted(analyzed_indexes),
                "still_exactly_unresolved_token_indexes": sorted(exact_unresolved),
                "unresolved_token_indexes_after_documented_morphology": unresolved_after,
                "effective_analysis_token_indexes_after_documented_morphology": effective_analysis,
                "effective_analysis_token_count_after_documented_morphology": len(effective_analysis),
                "effective_analysis_coverage_ratio_after_documented_morphology": (
                    len(effective_analysis) / result.get("token_count", 0)
                    if result.get("token_count", 0)
                    else 0.0
                ),
                "exact_evidence_metrics_preserved_separately": True,
            }
        )
        result.setdefault("fallback_policy", {}).update(
            {
                "documented_morphology_requires_documented_lemma": True,
                "documented_morphology_requires_explicit_source_rule": True,
                "documented_morphology_requires_independent_prosodic_license": True,
                "documented_morphology_does_not_become_exact_surface_evidence": True,
                "documented_morphology_does_not_license_generation": True,
                "documented_morphology_does_not_license_correction": True,
            }
        )
        result.setdefault("limitations", []).extend(
            [
                "DOCUMENTED_MORPHOLOGICAL_ANALYSIS_IS_SEPARATE_FROM_EXACT_SURFACE_ATTESTATION",
                "ONLY_GP_1SG_GRAVE_FINAL_I_TO_E_GLOTTAL_IS_PROMOTED_IN_V0_35_6",
                "NO_FREE_PARADIGM_GENERATION_FROM_DOCUMENTED_MORPHOLOGY",
            ]
        )
        return result
