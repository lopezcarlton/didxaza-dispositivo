#!/usr/bin/env python3
"""Analyzer v0.35.12 — source-explicit PB2015 valency relation bridge v0.1.

This layer consumes only the crosswalk derived from Voces HALL-0193. It never
reconstructs a basic↔derived relation from visible morphology. A relation is
attached to an observed token only when an earlier Analyzer layer has already
identified a lexical entry through a documented exact-headword route or a
source-documented person-fusion lemma route.

Crosswalk resolution is deliberately strict:
- UNIQUE_STRICT may link the PB2015 member to one Dictionaria entry;
- MULTIPLE_STRICT is preserved as ambiguity and is never assigned to one entry;
- NO_STRICT is absence of a strict crosswalk, not negative linguistic evidence.

PDLMA forms remain analytical/source forms. This layer does not project them to
Alfabeto Popular, infer a surface causative, create new members, license
correction/generation, or change exact-evidence metrics or analysis status.
"""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

from analyzer_v0_35_11_valency_compatibility_bridge import ROUTE_EXACT, ROUTE_PERSON

ADAPTER_VERSION = "0.35.12"
BRIDGE_VERSION = "0.1"

HERE = Path(__file__).resolve().parent
DEFAULT_CROSSWALK_PATH = (
    HERE.parent / "sources" / "VOCES_PB2015_EXPLICIT_VALENCY_RELATIONS_v0_1.csv"
)

VOCES_KNOWLEDGE_COMMIT = "f17c5363caada6f8beb18fa99c39e37cd72c6f09"
PB2015_SOURCE_ID = "SRC-PEREZ-BAEZ-2015-VALENCE-CHANGING-JUCHITAN"
HALL_ID = "HALL-0193"
TECHNICAL_DERIVATIVE = "VOCES_PB2015_EXPLICIT_VALENCY_RELATIONS_v0_1.csv"

STATUS_UNIQUE = "UNIQUE_STRICT"
STATUS_NONE = "NO_STRICT"
STATUS_MULTIPLE = "MULTIPLE_STRICT"
COMPARISON_POLICY = "RAW_PDLMA_EQUALITY_NO_NORMALIZATION"

ELIGIBLE_ENTRY_LINK_ROUTES = (ROUTE_EXACT, ROUTE_PERSON)


class ExplicitValencyRelationIndex:
    """Read-only index over source-explicit PB2015 relation sets."""

    REQUIRED_FIELDS = (
        "relation_set_id",
        "source_id",
        "source_location",
        "hall_id",
        "voces_commit",
        "source_group",
        "relation_role",
        "source_form_pdlma_raw",
        "dictionaria_match_status",
        "dictionaria_entry_ids",
        "dictionaria_headwords_ap",
        "comparison_policy",
        "ap_surface_assertion",
        "generation_license_assertion",
        "correction_assertion",
    )

    def __init__(self, path: str | Path = DEFAULT_CROSSWALK_PATH):
        self.path = Path(path)
        self.rows: list[dict[str, Any]] = []
        self.by_set: dict[str, list[dict[str, Any]]] = defaultdict(list)
        self.unique_by_entry: dict[str, list[dict[str, Any]]] = defaultdict(list)
        self.ambiguous_by_entry: dict[str, list[dict[str, Any]]] = defaultdict(list)
        self._load()

    @staticmethod
    def _split_pipe(raw: str) -> list[str]:
        return [part for part in str(raw or "").split("|") if part]

    def _load(self) -> None:
        with self.path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if tuple(reader.fieldnames or ()) != self.REQUIRED_FIELDS:
                raise ValueError(
                    f"Unexpected PB2015 relation crosswalk schema: {reader.fieldnames!r}"
                )
            raw_rows = list(reader)

        for raw in raw_rows:
            if raw["source_id"] != PB2015_SOURCE_ID:
                raise ValueError("Unexpected source_id in PB2015 relation crosswalk")
            if raw["hall_id"] != HALL_ID:
                raise ValueError("Unexpected HALL id in PB2015 relation crosswalk")
            if raw["voces_commit"] != VOCES_KNOWLEDGE_COMMIT:
                raise ValueError("Unexpected Voces commit in PB2015 relation crosswalk")
            if raw["comparison_policy"] != COMPARISON_POLICY:
                raise ValueError("Unexpected comparison policy in PB2015 relation crosswalk")
            if any(
                raw[name].strip().lower() != "false"
                for name in (
                    "ap_surface_assertion",
                    "generation_license_assertion",
                    "correction_assertion",
                )
            ):
                raise ValueError("Licensing/AP assertion unexpectedly enabled in crosswalk")
            status = raw["dictionaria_match_status"]
            if status not in (STATUS_UNIQUE, STATUS_NONE, STATUS_MULTIPLE):
                raise ValueError(f"Unknown crosswalk resolution status: {status}")

            row = dict(raw)
            row["resolved_entry_ids"] = self._split_pipe(raw["dictionaria_entry_ids"])
            row["resolved_headwords_ap"] = self._split_pipe(raw["dictionaria_headwords_ap"])
            if status == STATUS_UNIQUE and len(row["resolved_entry_ids"]) != 1:
                raise ValueError("UNIQUE_STRICT row must contain exactly one entry id")
            if status == STATUS_NONE and row["resolved_entry_ids"]:
                raise ValueError("NO_STRICT row must not contain entry ids")
            if status == STATUS_MULTIPLE and len(row["resolved_entry_ids"]) < 2:
                raise ValueError("MULTIPLE_STRICT row must contain multiple entry ids")

            self.rows.append(row)
            self.by_set[row["relation_set_id"]].append(row)
            if status == STATUS_UNIQUE:
                self.unique_by_entry[row["resolved_entry_ids"][0]].append(row)
            elif status == STATUS_MULTIPLE:
                for entry_id in row["resolved_entry_ids"]:
                    self.ambiguous_by_entry[entry_id].append(row)

    def _member_payload(self, row: dict[str, Any]) -> dict[str, Any]:
        return {
            "relation_role": row["relation_role"],
            "source_form_pdlma_raw": row["source_form_pdlma_raw"],
            "dictionaria_match_status": row["dictionaria_match_status"],
            "resolved_entry_ids": list(row["resolved_entry_ids"]),
            "resolved_headwords_ap": list(row["resolved_headwords_ap"]),
            "pdlma_form_is_project_surface_assertion": False,
        }

    def set_payload(self, relation_set_id: str) -> dict[str, Any]:
        rows = self.by_set[relation_set_id]
        counts = Counter(row["dictionaria_match_status"] for row in rows)
        return {
            "relation_set_id": relation_set_id,
            "source_group": rows[0]["source_group"],
            "source_location": rows[0]["source_location"],
            "member_count": len(rows),
            "resolution_counts": {
                STATUS_UNIQUE: counts[STATUS_UNIQUE],
                STATUS_NONE: counts[STATUS_NONE],
                STATUS_MULTIPLE: counts[STATUS_MULTIPLE],
            },
            "fully_uniquely_resolved": all(
                row["dictionaria_match_status"] == STATUS_UNIQUE for row in rows
            ),
            "members": [self._member_payload(row) for row in rows],
            "source_id": PB2015_SOURCE_ID,
            "hall_id": HALL_ID,
            "voces_commit": VOCES_KNOWLEDGE_COMMIT,
            "technical_derivative": TECHNICAL_DERIVATIVE,
            "relation_is_source_explicit": True,
            "relation_is_surface_morphology_inference": False,
            "pdlma_to_ap_assertion": False,
            "generation_license_assertion": False,
            "correction_assertion": False,
        }

    def unique_memberships_for_entry(self, entry_id: str) -> list[dict[str, Any]]:
        memberships = []
        for row in self.unique_by_entry.get(entry_id, ()): 
            payload = self.set_payload(row["relation_set_id"])
            payload["current_member"] = self._member_payload(row)
            payload["current_entry_id"] = entry_id
            payload["current_member_identity_status"] = (
                "SOURCE_MEMBER_UNIQUELY_RESOLVED_TO_THIS_ENTRY"
            )
            memberships.append(payload)
        return memberships

    def ambiguous_candidates_for_entry(self, entry_id: str) -> list[dict[str, Any]]:
        candidates = []
        for row in self.ambiguous_by_entry.get(entry_id, ()):
            candidates.append(
                {
                    "relation_set_id": row["relation_set_id"],
                    "source_group": row["source_group"],
                    "relation_role": row["relation_role"],
                    "source_form_pdlma_raw": row["source_form_pdlma_raw"],
                    "candidate_entry_ids": list(row["resolved_entry_ids"]),
                    "candidate_headwords_ap": list(row["resolved_headwords_ap"]),
                    "status": "AMBIGUOUS_STRICT_CROSSWALK_NOT_ASSIGNED",
                    "source_id": PB2015_SOURCE_ID,
                    "hall_id": HALL_ID,
                    "voces_commit": VOCES_KNOWLEDGE_COMMIT,
                    "relation_assignment_assertion": False,
                    "pdlma_to_ap_assertion": False,
                }
            )
        return candidates

    @property
    def stats(self) -> dict[str, Any]:
        resolution = Counter(row["dictionaria_match_status"] for row in self.rows)
        fully_unique = [
            set_id
            for set_id, rows in self.by_set.items()
            if all(row["dictionaria_match_status"] == STATUS_UNIQUE for row in rows)
        ]
        return {
            "selected_relation_members": len(self.rows),
            "selected_relation_sets": len(self.by_set),
            "members_with_unique_strict_match": resolution[STATUS_UNIQUE],
            "members_with_zero_strict_match": resolution[STATUS_NONE],
            "members_with_multiple_strict_matches": resolution[STATUS_MULTIPLE],
            "fully_unique_strict_relation_sets": len(fully_unique),
            "fully_unique_strict_relation_set_ids": sorted(fully_unique),
            "entries_with_unique_source_membership": len(self.unique_by_entry),
            "entries_exposed_to_ambiguous_source_member": len(self.ambiguous_by_entry),
            "comparison_policy": COMPARISON_POLICY,
            "pdlma_to_ap": False,
            "automatic_group_assignment": False,
            "surface_relation_inference": False,
        }


class ExplicitValencyRelationBridgeAnalyzer:
    """Expose source-explicit relation sets for already identified lexical entries."""

    def __init__(
        self,
        base_analyzer: Any,
        crosswalk_path: str | Path = DEFAULT_CROSSWALK_PATH,
    ):
        self.base = base_analyzer
        self.relation_index = ExplicitValencyRelationIndex(crosswalk_path)

    def __getattr__(self, name: str) -> Any:
        # Preserve access to stable capabilities of the immediately preceding
        # Analyzer layer without copying its private implementation state.
        return getattr(self.base, name)

    def close(self) -> None:
        self.base.close()

    @property
    def explicit_valency_relation_index_stats(self) -> dict[str, Any]:
        return self.relation_index.stats

    def _eligible_identified_entries(
        self, result: dict[str, Any]
    ) -> dict[int, list[dict[str, Any]]]:
        by_token: dict[int, list[dict[str, Any]]] = defaultdict(list)
        seen: set[tuple[int, str, str]] = set()
        for observation in result.get("valency_compatibility_observations", ()):
            token_index = int(observation["token_index"])
            for entry in observation.get("entries", ()):
                route = str(entry.get("entry_link_route", ""))
                entry_id = str(entry.get("entry_id", ""))
                if route not in ELIGIBLE_ENTRY_LINK_ROUTES or not entry_id:
                    continue
                key = (token_index, entry_id, route)
                if key in seen:
                    continue
                seen.add(key)
                by_token[token_index].append(
                    {
                        "entry_id": entry_id,
                        "entry_link_route": route,
                        "entry_link_strength": entry.get("entry_link_strength"),
                        "documented_headword_raw": entry.get("documented_headword_raw"),
                    }
                )
        return by_token

    def _entry_relation_payload(self, entry: dict[str, Any]) -> dict[str, Any]:
        entry_id = entry["entry_id"]
        memberships = self.relation_index.unique_memberships_for_entry(entry_id)
        ambiguous = self.relation_index.ambiguous_candidates_for_entry(entry_id)
        if memberships:
            status = "SOURCE_EXPLICIT_RELATION_MEMBERSHIP_DOCUMENTED"
        elif ambiguous:
            status = "AMBIGUOUS_SOURCE_MEMBER_CROSSWALK_NOT_ASSIGNED"
        else:
            status = "NO_SOURCE_EXPLICIT_RELATION_MEMBERSHIP_AT_STRICT_LEVEL"
        return {
            **entry,
            "status": status,
            "documented_membership_count": len(memberships),
            "documented_memberships": memberships,
            "ambiguous_crosswalk_candidate_count": len(ambiguous),
            "ambiguous_crosswalk_candidates": ambiguous,
            "entry_identity_required_before_relation_assertion": True,
            "relation_asserted_from_surface_morphology": False,
            "pdlma_to_ap_assertion": False,
            "generation_license_assertion": False,
            "correction_assertion": False,
            "orthographic_authority_assertion": False,
            "rule_discovery_assertion": False,
        }

    @staticmethod
    def _token_status(entries: Iterable[dict[str, Any]]) -> str:
        entries = list(entries)
        if not entries:
            return "NO_ELIGIBLE_IDENTIFIED_VERB_ENTRY"
        if any(row["documented_memberships"] for row in entries):
            if len(entries) > 1:
                return "MULTIPLE_IDENTIFIED_ENTRIES_WITH_SOURCE_EXPLICIT_RELATION_DATA"
            return "IDENTIFIED_ENTRY_WITH_SOURCE_EXPLICIT_RELATION_DATA"
        if any(row["ambiguous_crosswalk_candidates"] for row in entries):
            return "IDENTIFIED_ENTRY_WITH_AMBIGUOUS_SOURCE_CROSSWALK_ONLY"
        return "IDENTIFIED_ENTRY_WITHOUT_SOURCE_EXPLICIT_RELATION_AT_STRICT_LEVEL"

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
        identified = self._eligible_identified_entries(result)
        observations = []
        informative = []
        for token_index in range(token_count):
            entries = [
                self._entry_relation_payload(entry)
                for entry in identified.get(token_index, ())
            ]
            observation = {
                "token_index": token_index,
                "identified_entry_count": len(entries),
                "status": self._token_status(entries),
                "entries": entries,
            }
            observations.append(observation)
            if any(
                entry["documented_memberships"] or entry["ambiguous_crosswalk_candidates"]
                for entry in entries
            ):
                informative.append(token_index)

        result.update(
            {
                "current_adapter_version": ADAPTER_VERSION,
                "explicit_valency_relation_bridge_enabled": True,
                "explicit_valency_relation_bridge_version": BRIDGE_VERSION,
                "explicit_valency_relation_observations": observations,
                "explicit_valency_relation_informative_token_indexes": informative,
                "explicit_pb2015_group_retrieval_enabled": True,
                "automatic_pb2015_group_assignment_enabled": False,
                "surface_valency_relation_inference_enabled": False,
                "explicit_valency_relation_changes_exact_evidence_metrics": False,
                "explicit_valency_relation_changes_analysis_status": False,
                "explicit_valency_relation_generation_enabled": False,
                "explicit_valency_relation_correction_enabled": False,
            }
        )
        result.setdefault("fallback_policy", {}).update(
            {
                "explicit_valency_relation_requires_identified_entry": True,
                "explicit_valency_relation_eligible_routes": list(
                    ELIGIBLE_ENTRY_LINK_ROUTES
                ),
                "explicit_valency_relation_structural_candidate_route_eligible": False,
                "explicit_valency_relation_raw_pdlma_crosswalk_only": True,
                "explicit_valency_relation_no_strict_is_negative_evidence": False,
                "explicit_valency_relation_multiple_strict_auto_disambiguation": False,
                "explicit_valency_relation_surface_morphology_inference": False,
                "explicit_valency_relation_pdlma_to_ap": False,
                "explicit_valency_relation_generation": False,
                "explicit_valency_relation_correction": False,
            }
        )
        result.setdefault("limitations", []).extend(
            [
                "PB2015_RELATION_V0_1_CONSUMES_ONLY_HALL_0193_SOURCE_EXPLICIT_SELECTED_RELATIONS",
                "PB2015_RELATION_V0_1_REQUIRES_PREEXISTING_DOCUMENTED_ENTRY_IDENTITY",
                "PB2015_RELATION_V0_1_NO_STRICT_CROSSWALK_IS_NOT_NEGATIVE_EVIDENCE",
                "PB2015_RELATION_V0_1_MULTIPLE_STRICT_CROSSWALK_IS_NOT_AUTO_DISAMBIGUATED",
                "PB2015_RELATION_V0_1_PDLMA_FORMS_ARE_NOT_PROJECT_ORTHOGRAPHIC_SURFACES",
                "PB2015_RELATION_V0_1_DOES_NOT_INFER_RELATIONS_FROM_VISIBLE_PREFIXES",
                "PB2015_RELATION_V0_1_DOES_NOT_LICENSE_GENERATION_OR_CORRECTION",
            ]
        )
        return result
