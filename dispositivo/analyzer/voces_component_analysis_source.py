#!/usr/bin/env python3
"""Strict loader for component analyses already adjudicated in Voces.

This module is a technical derivative of pinned Voces knowledge. It does not
attempt segmentation, substring discovery, fuzzy matching, or orthographic
normalization. A row is retrievable only when the observed token equals the
registered surface under Unicode NFC.

The registry records analyses that Voces has already promoted from independent
documentary evidence. Loading such a row does not grant correction, generation,
orthographic authority, or rule-discovery authority.
"""

from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
import unicodedata


HERE = Path(__file__).resolve().parent
DEFAULT_REGISTRY_PATH = (
    HERE.parent / "sources" / "VOCES_CONTEXTUALLY_SUPPORTED_COMPONENT_ANALYSES_v0_1.csv"
)

EXPECTED_VOCES_COMMIT = "f3af4a4e490b2d211c24f764b29d8ec29b5b61dc"
MATCH_POLICY = "NFC_RAW_TOKEN_ONLY"
SUPPORTED_ANALYSIS_STATUS = "CONTEXTUALLY_SUPPORTED_COMPONENT_ANALYSIS"
SUPPORTED_LICENSE_STATUS = "NON_LICENSING"

REQUIRED_FIELDS = (
    "surface_raw",
    "components_raw",
    "component_glosses",
    "component_functions",
    "analysis_status",
    "boundary_status",
    "hall_id",
    "voces_commit",
    "source_ids",
    "epistemic_role",
    "license_status",
)


def nfc_surface(text: str) -> str:
    """Comparison form for registered surface lookup; NFC only."""
    return unicodedata.normalize("NFC", str(text or ""))


def _split_pipe(raw: str) -> tuple[str, ...]:
    return tuple(part.strip() for part in str(raw or "").split("|"))


@dataclass(frozen=True)
class ComponentAnalysisRecord:
    surface_raw: str
    components_raw: tuple[str, ...]
    component_glosses: tuple[str, ...]
    component_functions: tuple[str, ...]
    analysis_status: str
    boundary_status: str
    hall_id: str
    voces_commit: str
    source_ids: tuple[str, ...]
    epistemic_role: str
    license_status: str

    @property
    def surface_nfc(self) -> str:
        return nfc_surface(self.surface_raw)

    def as_payload(self) -> dict[str, object]:
        return {
            "surface_registered_raw": self.surface_raw,
            "components_raw": list(self.components_raw),
            "component_count": len(self.components_raw),
            "component_glosses": list(self.component_glosses),
            "component_functions": list(self.component_functions),
            "analysis_status": self.analysis_status,
            "boundary_status": self.boundary_status,
            "hall_id": self.hall_id,
            "voces_commit": self.voces_commit,
            "source_ids": list(self.source_ids),
            "epistemic_role": self.epistemic_role,
            "license_status": self.license_status,
            "surface_match_policy": MATCH_POLICY,
            "substring_segmentation_assertion": False,
            "morphological_compound_assertion": False,
            "orthographic_boundary_preference_assertion": False,
            "correction_assertion": False,
            "generation_license_assertion": False,
            "orthographic_authority_assertion": False,
            "rule_discovery_assertion": False,
        }


class VocesComponentAnalysisSource:
    """Read-only exact-surface index of pinned Voces component analyses."""

    def __init__(self, registry_path: str | Path = DEFAULT_REGISTRY_PATH):
        self.registry_path = Path(registry_path)
        self.records: list[ComponentAnalysisRecord] = []
        self._by_surface_nfc: dict[str, list[ComponentAnalysisRecord]] = defaultdict(list)
        self._load()

    def _load(self) -> None:
        if not self.registry_path.is_file():
            raise FileNotFoundError(self.registry_path)

        with self.registry_path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            missing = [field for field in REQUIRED_FIELDS if field not in (reader.fieldnames or ())]
            if missing:
                raise ValueError(f"component registry missing required fields: {missing}")

            for row_number, row in enumerate(reader, start=2):
                surface = str(row.get("surface_raw", "") or "")
                components = _split_pipe(row.get("components_raw", "") or "")
                glosses = _split_pipe(row.get("component_glosses", "") or "")
                functions = _split_pipe(row.get("component_functions", "") or "")
                source_ids = tuple(
                    source for source in _split_pipe(row.get("source_ids", "") or "") if source
                )
                analysis_status = str(row.get("analysis_status", "") or "").strip()
                license_status = str(row.get("license_status", "") or "").strip()
                hall_id = str(row.get("hall_id", "") or "").strip()
                voces_commit = str(row.get("voces_commit", "") or "").strip()

                if not surface:
                    raise ValueError(f"row {row_number}: empty surface_raw")
                if len(components) < 2 or any(not component for component in components):
                    raise ValueError(f"row {row_number}: at least two non-empty components required")
                if len(glosses) != len(components):
                    raise ValueError(f"row {row_number}: component_glosses count mismatch")
                if len(functions) != len(components):
                    raise ValueError(f"row {row_number}: component_functions count mismatch")
                if analysis_status != SUPPORTED_ANALYSIS_STATUS:
                    raise ValueError(
                        f"row {row_number}: unsupported analysis_status {analysis_status!r}"
                    )
                if license_status != SUPPORTED_LICENSE_STATUS:
                    raise ValueError(
                        f"row {row_number}: registry must remain NON_LICENSING"
                    )
                if not hall_id.startswith("HALL-"):
                    raise ValueError(f"row {row_number}: invalid hall_id {hall_id!r}")
                if voces_commit != EXPECTED_VOCES_COMMIT:
                    raise ValueError(
                        f"row {row_number}: Voces commit {voces_commit!r} does not match pin "
                        f"{EXPECTED_VOCES_COMMIT}"
                    )
                if not source_ids:
                    raise ValueError(f"row {row_number}: at least one source_id required")

                record = ComponentAnalysisRecord(
                    surface_raw=surface,
                    components_raw=components,
                    component_glosses=glosses,
                    component_functions=functions,
                    analysis_status=analysis_status,
                    boundary_status=str(row.get("boundary_status", "") or "").strip(),
                    hall_id=hall_id,
                    voces_commit=voces_commit,
                    source_ids=source_ids,
                    epistemic_role=str(row.get("epistemic_role", "") or "").strip(),
                    license_status=license_status,
                )
                self.records.append(record)
                self._by_surface_nfc[record.surface_nfc].append(record)

    def lookup(self, observed_token_raw: str) -> tuple[ComponentAnalysisRecord, ...]:
        """Return only NFC-exact registered surface matches."""
        return tuple(self._by_surface_nfc.get(nfc_surface(observed_token_raw), ()))

    @property
    def stats(self) -> dict[str, object]:
        return {
            "registry_path": str(self.registry_path),
            "record_count": len(self.records),
            "indexed_surface_count": len(self._by_surface_nfc),
            "voces_commit": EXPECTED_VOCES_COMMIT,
            "surface_match_policy": MATCH_POLICY,
            "casefold": False,
            "apostrophe_unification": False,
            "tone_stripping": False,
            "diacritic_stripping": False,
            "substring_search": False,
            "near_match": False,
            "edit_distance": False,
            "pdlma_to_ap": False,
        }
