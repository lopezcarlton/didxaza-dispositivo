#!/usr/bin/env python3
"""Analyzer v0.35.14 — source-documented causative group coordinates.

This wrapper consumes only source-explicit PB2015 relation memberships already
exposed by v0.35.12 and makes the adjudicated C1-C4 group resources from Voces
visible as analytical coordinates.

It does not detect a causative prefix by looking at the observed surface. It does
not segment the observed token, project PDLMA notation to Alfabeto Popular, or
assign a PB2015 group from phonological/orthographic resemblance.

A coordinate is emitted only when an earlier layer has already identified a
Dictionaria verb entry and v0.35.12 has attached a source-explicit membership in
one of the consonantal PB2015 groups C1-C4.

Voces authority:
- HALL-0188: valency-changing morphology is distinct from TAM and analytical
  morphemes are not project surface spellings;
- HALL-0190: C1=-g-, C2=-u-, C3=-u-g-, C4=larger concatenations including
  -u(-g)-zi- / -zu-;
- HALL-0191: documented patterns are not universally productive rules.

Therefore:

    SOURCE_GROUP_COORDINATE != VISIBLE_PREFIX_SEGMENTATION
    DOCUMENTED_CAUSATIVE_RESOURCE != TOKEN_LEVEL_CAUSATIVE_PARSE
    PDLMA_ANALYTICAL_MORPHEME != PROJECT_SURFACE_SPELLING
    DOCUMENTED_PATTERN != PRODUCTIVE_GENERATION_RULE
"""

from __future__ import annotations

from typing import Any

ADAPTER_VERSION = "0.35.14"
VIEW_VERSION = "0.1"

VOCES_KNOWLEDGE_COMMIT = "f17c5363caada6f8beb18fa99c39e37cd72c6f09"
PB2015_SOURCE_ID = "SRC-PEREZ-BAEZ-2015-VALENCE-CHANGING-JUCHITAN"
HALL_IDS = ("HALL-0188", "HALL-0190", "HALL-0191")

STATUS_AVAILABLE = "SOURCE_EXPLICIT_CONSONANT_CAUSATIVE_GROUP_COORDINATE_AVAILABLE"
STATUS_NONE = "NO_SOURCE_EXPLICIT_CONSONANT_CAUSATIVE_GROUP_COORDINATE"

# Analytical/source notation only. These strings must never be treated as an
# orthographic rewrite recipe for observed project surface forms.
CAUSATIVE_GROUP_RESOURCES: dict[str, dict[str, Any]] = {
    "C1": {
        "resource_id": "PB2015_C1_CAUSATIVE_RESOURCE_G",
        "analytical_resource_raw": "-g-",
        "resource_description": "CAUSATIVE_RESOURCE_G",
    },
    "C2": {
        "resource_id": "PB2015_C2_CAUSATIVE_RESOURCE_U",
        "analytical_resource_raw": "-u-",
        "resource_description": "CAUSATIVE_RESOURCE_U",
    },
    "C3": {
        "resource_id": "PB2015_C3_CAUSATIVE_RESOURCE_U_G",
        "analytical_resource_raw": "-u-g-",
        "resource_description": "CAUSATIVE_RESOURCE_U_G",
    },
    "C4": {
        "resource_id": "PB2015_C4_CAUSATIVE_RESOURCE_LARGER_CONCATENATIONS",
        "analytical_resource_raw": "-u(-g)-zi- / -zu-",
        "resource_description": "LARGER_CAUSATIVE_CONCATENATIONS_INCLUDING_U_G_ZI_ZU",
    },
}


def group_resource_payload(source_group: str) -> dict[str, Any] | None:
    base = CAUSATIVE_GROUP_RESOURCES.get(str(source_group or ""))
    if base is None:
        return None
    return {
        **base,
        "source_group": source_group,
        "source_id": PB2015_SOURCE_ID,
        "voces_hall_ids": list(HALL_IDS),
        "voces_knowledge_commit": VOCES_KNOWLEDGE_COMMIT,
        "epistemic_status": "SOURCE_DOCUMENTED_GROUP_LEVEL_ANALYTICAL_COORDINATE",
        "group_membership_must_be_source_explicit": True,
        "observed_surface_prefix_assertion": False,
        "observed_surface_segmentation_assertion": False,
        "observed_token_causative_analysis_assertion": False,
        "pdlma_to_ap_assertion": False,
        "productive_rule_assertion": False,
        "generation_license_assertion": False,
        "correction_assertion": False,
        "orthographic_authority_assertion": False,
        "rule_discovery_assertion": False,
    }


class CausativeGroupCoordinateViewAnalyzer:
    """Expose C1-C4 analytical resources for source-explicit memberships only."""

    def __init__(self, base_analyzer: Any):
        self.base = base_analyzer

    def __getattr__(self, name: str) -> Any:
        return getattr(self.base, name)

    def close(self) -> None:
        self.base.close()

    @staticmethod
    def _entry_coordinates(entry: dict[str, Any]) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        seen: set[tuple[str, str, str]] = set()
        for membership in entry.get("documented_memberships", ()):
            source_group = str(membership.get("source_group", ""))
            resource = group_resource_payload(source_group)
            if resource is None:
                continue
            current_member = membership.get("current_member") or {}
            relation_set_id = str(membership.get("relation_set_id", ""))
            role = str(current_member.get("relation_role", ""))
            key = (relation_set_id, source_group, role)
            if key in seen:
                continue
            seen.add(key)
            out.append(
                {
                    "entry_id": entry.get("entry_id"),
                    "entry_link_route": entry.get("entry_link_route"),
                    "documented_headword_raw": entry.get("documented_headword_raw"),
                    "relation_set_id": relation_set_id,
                    "source_group": source_group,
                    "source_explicit_relation_role": role,
                    "source_member_pdlma_raw": current_member.get("source_form_pdlma_raw"),
                    "entry_is_source_explicit_causative_member": role == "CAUSATIVE",
                    "entry_is_source_explicit_basic_member": role == "BASIC",
                    "group_causative_resource": resource,
                    "coordinate_scope": "SOURCE_GROUP_LEVEL_NOT_OBSERVED_SURFACE_SEGMENTATION",
                    "group_was_inferred_from_surface": False,
                    "resource_was_detected_from_visible_prefix": False,
                    "observed_surface_prefix_assertion": False,
                    "observed_surface_segmentation_assertion": False,
                    "observed_token_causative_analysis_assertion": False,
                    "pdlma_to_ap_assertion": False,
                    "generation_license_assertion": False,
                    "correction_assertion": False,
                }
            )
        return out

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

        observations: list[dict[str, Any]] = []
        informative: list[int] = []
        for observation in result.get("explicit_valency_relation_observations", ()):
            token_index = int(observation.get("token_index", 0))
            coordinates: list[dict[str, Any]] = []
            for entry in observation.get("entries", ()):
                coordinates.extend(self._entry_coordinates(entry))
            status = STATUS_AVAILABLE if coordinates else STATUS_NONE
            observations.append(
                {
                    "token_index": token_index,
                    "status": status,
                    "coordinate_count": len(coordinates),
                    "coordinates": coordinates,
                    "source_explicit_membership_required": True,
                    "surface_group_assignment_enabled": False,
                    "visible_prefix_detection_enabled": False,
                    "pdlma_to_ap_enabled": False,
                }
            )
            if coordinates:
                informative.append(token_index)

        result.update(
            {
                "current_adapter_version": ADAPTER_VERSION,
                "causative_group_coordinate_view_enabled": True,
                "causative_group_coordinate_view_version": VIEW_VERSION,
                "causative_group_coordinate_observations": observations,
                "causative_group_coordinate_informative_token_indexes": informative,
                "causative_group_coordinate_changes_exact_evidence_metrics": False,
                "causative_group_coordinate_changes_analysis_status": False,
                "causative_group_surface_assignment_enabled": False,
                "causative_visible_prefix_detection_enabled": False,
                "causative_group_generation_enabled": False,
                "causative_group_correction_enabled": False,
            }
        )
        result.setdefault("fallback_policy", {}).update(
            {
                "causative_group_coordinate_requires_source_explicit_membership": True,
                "causative_group_coordinate_c1_resource_analytical": "-g-",
                "causative_group_coordinate_c2_resource_analytical": "-u-",
                "causative_group_coordinate_c3_resource_analytical": "-u-g-",
                "causative_group_coordinate_c4_resource_analytical": "-u(-g)-zi- / -zu-",
                "causative_group_coordinate_visible_prefix_detection": False,
                "causative_group_coordinate_surface_segmentation": False,
                "causative_group_coordinate_pdlma_to_ap": False,
                "causative_group_coordinate_productive_generation": False,
            }
        )
        result.setdefault("limitations", []).extend(
            [
                "CAUSATIVE_GROUP_COORDINATE_ONLY_FOR_SOURCE_EXPLICIT_C1_C4_MEMBERSHIP",
                "CAUSATIVE_GROUP_RESOURCE_IS_GROUP_LEVEL_NOT_TOKEN_LEVEL_SEGMENTATION",
                "VISIBLE_U_G_ZI_ZU_RESEMBLANCE_DOES_NOT_ASSIGN_CAUSATIVE_GROUP",
                "PDLMA_CAUSATIVE_RESOURCE_IS_NOT_PROJECT_SURFACE_SPELLING",
                "DOCUMENTED_CAUSATIVE_PATTERN_IS_NOT_UNIVERSALLY_PRODUCTIVE",
            ]
        )
        return result
