#!/usr/bin/env python3
"""Analyzer v0.35.11 — lexical valency compatibility bridge v0.1.

This wrapper does not infer valency from surface morphology. It consumes only
verb entry IDs already exposed by the current Analyzer chain and interprets only
lexical analysis codes whose meanings have been explicitly adjudicated in Voces
HALL-0192:

- ``:caus`` -> documented causative lexical code;
- ``:i``    -> documented intransitive lexical code;
- ``:t``    -> documented transitive lexical code.

The broader Juchitán valency architecture is sourced from Pérez Báez 2015 as
adjudicated in HALL-0188..HALL-0191. No entry is assigned to V1/V2/V3/C1/C2/C3/C4
without an explicit source relation. No numeric valence is inferred from
transitivity. Undefined analysis modifiers (including ``vers`` in this pass) are
left uninterpreted.

Three existing entry-link routes can be enriched:

1. exact documented verb-headword records from VerbAnalysisBridge v0.1;
2. source-licensed documented person-fusion analyses that preserve a lemma ID;
3. non-headword structural candidates from VerbAnalysisBridge v0.2.

Only routes 1 and 2 link the observed token to an identified lexical entry.
Route 3 remains compatibility-only because v0.2 explicitly does not assert that
the observed token is the compatible verb entry.

This layer never changes exact-evidence metrics, analysis status, correction,
generation, orthographic authority or rule-discovery authority.
"""

from __future__ import annotations

from collections import defaultdict
import re
from typing import Any, Iterable

ADAPTER_VERSION = "0.35.11"
BRIDGE_VERSION = "0.1"

VOCES_KNOWLEDGE_COMMIT = "59653cc283d2fceea968031e1b554192ff7b3a27"
DICTIONARIA_SOURCE_ID = "SRC-DICTIONARIA-DIDXAZA-SPANISH-ENGLISH-DICTIONARY"
DICTIONARIA_CODE_LEGEND_SOURCE_ID = (
    "SRC-DICTIONARIA-DIIDXAZA-LEXICOBOTANICAL-GRAMMATICAL-CODES"
)
PB2015_SOURCE_ID = "SRC-PEREZ-BAEZ-2015-VALENCE-CHANGING-JUCHITAN"
VALENCY_HALL_IDS = ("HALL-0188", "HALL-0189", "HALL-0190", "HALL-0191", "HALL-0192")
TECHNICAL_DERIVATIVE = "DIC_VERB_2385_v0_1.csv"

STATUS_DOCUMENTED = "DOCUMENTED_LEXICAL_VALENCY_CODE"
STATUS_NONE = "NO_ADJUDICATED_VALENCY_CODE_IN_RECORD"
GROUP_STATUS = "UNASSIGNED_REQUIRES_EXPLICIT_SOURCE_RELATION"
NUMERIC_VALENCE_STATUS = "NOT_INFERRED_FROM_TRANSITIVITY_CODE"

ROUTE_EXACT = "DOCUMENTED_EXACT_VERB_HEADWORD_ENTRY_LINK"
ROUTE_PERSON = "SOURCE_DOCUMENTED_PERSON_FUSION_LEMMA_ENTRY_LINK"
ROUTE_STRUCTURAL = "NONHEADWORD_STRUCTURAL_VERB_ENTRY_CANDIDATE_ONLY"


def _has_literal_causative_code(raw: str) -> bool:
    """Recognize only the literal lexical marker `caus` as a complete code atom."""
    return bool(re.search(r"(?i)(?:^|[^a-z])caus(?:$|[^a-z])", str(raw or "")))


def _documented_transitivity_labels(raw: str) -> tuple[str, ...]:
    """Recover only terminal/segment `:i` and `:t` labels adjudicated in HALL-0192."""
    labels: list[str] = []
    for match in re.finditer(r"(?i):([it])(?=$|[\s,#;])", str(raw or "")):
        label = "INTRANSITIVE" if match.group(1).lower() == "i" else "TRANSITIVE"
        if label not in labels:
            labels.append(label)
    return tuple(labels)


def parse_adjudicated_lexical_valency_codes(raw: str) -> dict[str, Any]:
    raw = str(raw or "")
    causative = _has_literal_causative_code(raw)
    transitivity = _documented_transitivity_labels(raw)
    documented = causative or bool(transitivity)
    return {
        "analysis_codes_raw": raw,
        "lexical_valency_code_status": STATUS_DOCUMENTED if documented else STATUS_NONE,
        "documented_causative_lexical_code": causative,
        "documented_transitivity_labels": list(transitivity),
        "documented_transitivity_code_count": len(transitivity),
        "transitivity_conflict_preserved": len(transitivity) > 1,
        "numeric_valence": None,
        "numeric_valence_status": NUMERIC_VALENCE_STATUS,
        "pb2015_valency_group": None,
        "pb2015_valency_group_status": GROUP_STATUS,
        "vers_marker_interpreted": False,
        "undefined_modifiers_interpreted": False,
    }


def _route_strength(route: str) -> str:
    if route == ROUTE_EXACT:
        return "DOCUMENTED_LEXICAL_ENTRY_LINK"
    if route == ROUTE_PERSON:
        return "SOURCE_DOCUMENTED_MORPHOLOGICAL_LEMMA_LINK"
    return "COMPATIBILITY_CANDIDATE_ONLY"


class ValencyCompatibilityBridgeAnalyzer:
    """Attach adjudicated lexical valency codes to already-linked verb entries."""

    def __init__(self, base_analyzer: Any):
        self.base = base_analyzer
        for name in (
            "retrieval", "bound", "morph2", "morph1", "db", "verb_meta",
            "person_exact", "runtime_root", "sqlite_path", "verb_inventory_path",
            "biyubi_source",
        ):
            if hasattr(base_analyzer, name):
                setattr(self, name, getattr(base_analyzer, name))

        self._inventory_stats = self._measure_inventory()

    @property
    def biyubi_source_status(self) -> str:
        return self.base.biyubi_source_status

    def close(self) -> None:
        self.base.close()

    def _measure_inventory(self) -> dict[str, int]:
        causative = 0
        intransitive = 0
        transitive = 0
        with_any = 0
        conflicts = 0
        for record in self.morph1.records.values():
            parsed = parse_adjudicated_lexical_valency_codes(record.analysis_codes_raw)
            if parsed["documented_causative_lexical_code"]:
                causative += 1
            labels = set(parsed["documented_transitivity_labels"])
            if "INTRANSITIVE" in labels:
                intransitive += 1
            if "TRANSITIVE" in labels:
                transitive += 1
            if parsed["lexical_valency_code_status"] == STATUS_DOCUMENTED:
                with_any += 1
            if parsed["transitivity_conflict_preserved"]:
                conflicts += 1
        return {
            "verb_inventory_rows": len(self.morph1.records),
            "entries_with_adjudicated_valency_code": with_any,
            "entries_with_literal_causative_code": causative,
            "entries_with_intransitive_code": intransitive,
            "entries_with_transitive_code": transitive,
            "entries_with_both_i_and_t_codes": conflicts,
        }

    @property
    def valency_compatibility_index_stats(self) -> dict[str, int | str | bool]:
        return {
            **self._inventory_stats,
            "group_assignment_enabled": False,
            "numeric_valence_inference_enabled": False,
            "surface_valency_inference_enabled": False,
        }

    def _entry_payload(
        self,
        entry_id: str,
        *,
        route: str,
        token_index: int,
        token_raw: str | None,
    ) -> dict[str, Any] | None:
        record = self.morph1.records.get(entry_id)
        if record is None:
            return None
        parsed = parse_adjudicated_lexical_valency_codes(record.analysis_codes_raw)
        return {
            "token_index": token_index,
            "token_raw": token_raw,
            "entry_id": entry_id,
            "entry_link_route": route,
            "entry_link_strength": _route_strength(route),
            "documented_headword_raw": record.headword_raw,
            "definition_es": record.definition_es,
            "verb_class": record.verb_class,
            "pdlma_citation_raw": record.pdlma_raw,
            "lexical_valency": parsed,
            "lexical_property_applies_to_documented_entry": True,
            "lexical_property_asserted_for_observed_token": route in (ROUTE_EXACT, ROUTE_PERSON),
            "observed_token_exact_surface_evidence_from_this_layer": False,
            "basic_to_derived_relation_assertion": False,
            "pb2015_group_assignment_assertion": False,
            "numeric_valence_assertion": False,
            "surface_prefix_valency_inference_assertion": False,
            "pdlma_to_ap_assertion": False,
            "correction_assertion": False,
            "orthographic_authority_assertion": False,
            "generation_license_assertion": False,
            "rule_discovery_assertion": False,
            "provenance": {
                "lexical_record_source": DICTIONARIA_SOURCE_ID,
                "grammatical_code_legend_source": DICTIONARIA_CODE_LEGEND_SOURCE_ID,
                "valency_architecture_source": PB2015_SOURCE_ID,
                "technical_derivative": TECHNICAL_DERIVATIVE,
                "voces_hall_ids": list(VALENCY_HALL_IDS),
                "voces_knowledge_commit": VOCES_KNOWLEDGE_COMMIT,
            },
        }

    @staticmethod
    def _append_unique(
        rows_by_token: dict[int, list[dict[str, Any]]],
        seen: set[tuple[int, str, str]],
        payload: dict[str, Any] | None,
    ) -> None:
        if payload is None:
            return
        key = (payload["token_index"], payload["entry_id"], payload["entry_link_route"])
        if key in seen:
            return
        seen.add(key)
        rows_by_token[payload["token_index"]].append(payload)

    def _collect_entry_links(self, result: dict[str, Any]) -> dict[int, list[dict[str, Any]]]:
        rows_by_token: dict[int, list[dict[str, Any]]] = defaultdict(list)
        seen: set[tuple[int, str, str]] = set()

        for observation in result.get("documented_exact_verb_analyses", ()):
            token_index = int(observation["token_index"])
            token_raw = observation.get("token_raw")
            for record in observation.get("documented_records", ()):
                self._append_unique(
                    rows_by_token,
                    seen,
                    self._entry_payload(
                        str(record.get("entry_id", "")),
                        route=ROUTE_EXACT,
                        token_index=token_index,
                        token_raw=token_raw,
                    ),
                )

        for analysis in result.get("documented_person_fusion_analyses", ()):
            entry_id = str(analysis.get("documented_lemma_entry_id", "") or "")
            if not entry_id:
                continue
            self._append_unique(
                rows_by_token,
                seen,
                self._entry_payload(
                    entry_id,
                    route=ROUTE_PERSON,
                    token_index=int(analysis["token_index"]),
                    token_raw=analysis.get("token_raw"),
                ),
            )

        for candidate in result.get("documentary_verb_form_candidates", ()):
            token_index = int(candidate["token_index"])
            token_raw = candidate.get("token_raw")
            for entry in candidate.get("compatible_verb_entries", ()):
                self._append_unique(
                    rows_by_token,
                    seen,
                    self._entry_payload(
                        str(entry.get("entry_id", "")),
                        route=ROUTE_STRUCTURAL,
                        token_index=token_index,
                        token_raw=token_raw,
                    ),
                )

        return rows_by_token

    @staticmethod
    def _token_status(entries: Iterable[dict[str, Any]]) -> str:
        entries = list(entries)
        if not entries:
            return "NO_LINKED_VERB_ENTRY"
        documented_entries = {
            row["entry_id"]
            for row in entries
            if row["entry_link_route"] in (ROUTE_EXACT, ROUTE_PERSON)
        }
        candidate_entries = {
            row["entry_id"]
            for row in entries
            if row["entry_link_route"] == ROUTE_STRUCTURAL
        }
        any_code = any(
            row["lexical_valency"]["lexical_valency_code_status"] == STATUS_DOCUMENTED
            for row in entries
        )
        if len(documented_entries) == 1 and any_code:
            return "DOCUMENTED_ENTRY_WITH_LEXICAL_VALENCY_CODE"
        if len(documented_entries) > 1:
            return "MULTIPLE_DOCUMENTED_ENTRIES_VALENCY_AMBIGUOUS"
        if documented_entries and not any_code:
            return "DOCUMENTED_ENTRY_WITHOUT_ADJUDICATED_VALENCY_CODE"
        if candidate_entries and any_code:
            return "STRUCTURAL_ENTRY_CANDIDATE_WITH_LEXICAL_VALENCY_COMPATIBILITY"
        if candidate_entries:
            return "STRUCTURAL_ENTRY_CANDIDATE_WITHOUT_ADJUDICATED_VALENCY_CODE"
        return "NO_ADJUDICATED_VALENCY_CODE"

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
        rows_by_token = self._collect_entry_links(result)

        observations: list[dict[str, Any]] = []
        for token_index in range(token_count):
            entries = rows_by_token.get(token_index, [])
            observations.append(
                {
                    "token_index": token_index,
                    "entry_count": len(entries),
                    "status": self._token_status(entries),
                    "entries": entries,
                    "pb2015_valency_group": None,
                    "pb2015_valency_group_status": GROUP_STATUS,
                    "numeric_valence": None,
                    "numeric_valence_status": NUMERIC_VALENCE_STATUS,
                }
            )

        informative = [
            row
            for row in observations
            if row["status"] not in ("NO_LINKED_VERB_ENTRY", "NO_ADJUDICATED_VALENCY_CODE")
        ]
        result.update(
            {
                "current_adapter_version": ADAPTER_VERSION,
                "valency_compatibility_bridge_enabled": True,
                "valency_compatibility_bridge_version": BRIDGE_VERSION,
                "valency_compatibility_observations": observations,
                "valency_compatibility_informative_token_indexes": [
                    row["token_index"] for row in informative
                ],
                "valency_compatibility_changes_exact_evidence_metrics": False,
                "valency_compatibility_changes_analysis_status": False,
                "valency_group_assignment_enabled": False,
                "numeric_valence_inference_enabled": False,
                "surface_valency_inference_enabled": False,
                "valency_generation_enabled": False,
                "valency_correction_enabled": False,
            }
        )
        result.setdefault("fallback_policy", {}).update(
            {
                "valency_requires_preexisting_verb_entry_link": True,
                "valency_literal_adjudicated_codes_only": ["caus", "i", "t"],
                "valency_undefined_analysis_modifiers_interpreted": False,
                "valency_vers_interpreted": False,
                "valency_group_assignment_from_surface": False,
                "valency_numeric_inference_from_transitivity": False,
                "valency_basic_derived_relation_inference": False,
                "valency_pdlma_to_ap": False,
                "valency_generation": False,
                "valency_correction": False,
            }
        )
        result.setdefault("limitations", []).extend(
            [
                "VALENCY_V0_1_INTERPRETS_ONLY_HALL_0192_LITERAL_LEXICAL_CODES_CAUS_I_T",
                "VALENCY_V0_1_DOES_NOT_ASSIGN_PB2015_V1_V2_V3_C1_C2_C3_C4_GROUPS",
                "VALENCY_V0_1_DOES_NOT_INFER_NUMERIC_VALENCE_FROM_TRANSITIVITY",
                "VALENCY_V0_1_DOES_NOT_RECONSTRUCT_BASIC_TO_DERIVED_RELATIONS",
                "VALENCY_V0_1_STRUCTURAL_NONHEADWORD_ROUTE_IS_COMPATIBILITY_ONLY",
                "VALENCY_V0_1_UNDEFINED_MODIFIERS_INCLUDING_VERS_REMAIN_UNINTERPRETED",
            ]
        )
        return result
