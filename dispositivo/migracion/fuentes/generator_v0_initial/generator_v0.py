#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
INPUTS = HERE.parent / "inputs_nc001"
LICENSES = HERE / "GenerationLicense_v0.jsonl"
BLOCKERS = HERE / "IntegrationBlockers_v0.jsonl"


@dataclass(frozen=True)
class GenerationRequest:
    construction_id: str
    candidate_id: str
    tam: str
    person: str
    slots: dict[str, str]
    target_scope: str = "JUCHITAN"


@dataclass(frozen=True)
class GenerationResult:
    status: str
    surface: str
    reason: str
    construction_id: str
    license_id: str | None
    cell_id: str | None
    evidence_ids: tuple[str, ...]
    source_refs: tuple[str, ...]
    origin: str | None
    novelty: str | None
    analysis_features: dict[str, Any]


class LicensedGeneratorV0:
    """Exact-license generator for NC001.

    It emits a surface only when the request matches a materialized license whose
    whole assembled surface is independently source-attested. Missing or
    conflicting licenses cause explicit abstention.
    """

    def __init__(self, *, inputs_dir: Path = INPUTS, licenses_path: Path = LICENSES, blockers_path: Path = BLOCKERS):
        self.inputs_dir = Path(inputs_dir)
        self.cells = self._load_cells(self.inputs_dir / "ParadigmTable_v1.csv")
        self.constructions = self._load_jsonl_index(self.inputs_dir / "ConstructionInventory_v1.jsonl", "construction_id")
        self.licenses = self._load_jsonl(licenses_path)
        self.blockers = self._load_jsonl_index(blockers_path, "construction_id")
        self._validate_materialized_licenses()

    @staticmethod
    def _load_jsonl(path: Path) -> list[dict[str, Any]]:
        with path.open(encoding="utf-8") as f:
            return [json.loads(line) for line in f if line.strip()]

    @classmethod
    def _load_jsonl_index(cls, path: Path, key: str) -> dict[str, dict[str, Any]]:
        return {row[key]: row for row in cls._load_jsonl(path)}

    @staticmethod
    def _load_cells(path: Path) -> dict[str, dict[str, str]]:
        with path.open(encoding="utf-8-sig", newline="") as f:
            return {row["cell_id"]: row for row in csv.DictReader(f)}

    def _assemble(self, lic: dict[str, Any]) -> str:
        parts: list[str] = []
        for item in lic["assembly"]:
            if item["kind"] == "literal":
                parts.append(item["value"])
            elif item["kind"] == "cell":
                cell = self.cells[item["cell_id"]]
                parts.append(cell["surface_observed"])
            else:
                raise ValueError(f"Unsupported assembly item: {item['kind']}")
        return " ".join(parts)

    def _validate_materialized_licenses(self) -> None:
        seen: set[str] = set()
        for lic in self.licenses:
            lid = lic["license_id"]
            if lid in seen:
                raise ValueError(f"Duplicate license_id: {lid}")
            seen.add(lid)
            if lic["origin"] not in {"SOURCE_ATTESTATION", "SPEAKER_ATTESTATION"}:
                raise ValueError(f"Non-licensing origin in {lid}")
            if not lic.get("whole_surface_attested"):
                raise ValueError(f"v0 requires whole_surface_attested in {lid}")
            if lic.get("may_license_new_combinations"):
                raise ValueError(f"v0 cannot license novel combinations: {lid}")
            cell = self.cells.get(lic["cell_id"])
            if not cell:
                raise ValueError(f"Unknown cell in {lid}")
            if cell["status"] != "ATTESTED" or not cell["evidence_id"]:
                raise ValueError(f"Unattested cell in {lid}")
            if cell["evidence_id"] != lic["cell_evidence_id"]:
                raise ValueError(f"Evidence mismatch in {lid}")
            if cell["dialect_scope"] != "JUCHITAN_EXPLICIT":
                raise ValueError(f"Target scope not explicit in {lid}")
            if cell["orthography_status"] != "SOURCE_EXACT_RENDERING":
                raise ValueError(f"Orthographic realization not exact in {lid}")
            assembled = self._assemble(lic)
            if assembled != lic["attested_whole_surface"]:
                raise ValueError(f"Assembled surface differs from attested whole in {lid}: {assembled!r}")
            c = self.constructions.get(lic["construction_id"])
            if not c:
                raise ValueError(f"Unknown construction in {lid}")
            if c.get("generator", "").startswith("DISABLED"):
                raise ValueError(f"Disabled construction licensed in {lid}")

    @staticmethod
    def _signature_matches(req: GenerationRequest, lic: dict[str, Any]) -> bool:
        return (
            req.construction_id == lic["construction_id"]
            and req.candidate_id == lic["candidate_id"]
            and req.tam == lic["tam"]
            and req.person == lic["person"]
            and req.target_scope == lic["target_scope"]
            and req.slots == lic["request_slots"]
        )

    def generate(self, req: GenerationRequest) -> GenerationResult:
        if req.construction_id not in self.constructions:
            return self._abstain(req, "UNKNOWN_CONSTRUCTION")
        if req.target_scope != "JUCHITAN":
            return self._abstain(req, "TARGET_SCOPE_UNLICENSED")
        if req.tam not in {"HABITUAL", "COMPLETIVE"}:
            return self._abstain(req, "TAM_OUT_OF_SCOPE")
        if req.person not in {"1SG", "2SG", "3SG_HUMAN"}:
            return self._abstain(req, "PERSON_OUT_OF_SCOPE")
        blocker = self.blockers.get(req.construction_id)
        if blocker:
            return self._abstain(req, blocker["reason"])
        matches = [lic for lic in self.licenses if self._signature_matches(req, lic)]
        if not matches:
            # Distinguish missing direct cell from missing combination license.
            candidate_cells = [c for c in self.cells.values() if c["candidate_id"] == req.candidate_id and c["tam"] == req.tam and c["person"] == req.person]
            if not candidate_cells or candidate_cells[0]["status"] != "ATTESTED":
                return self._abstain(req, "MISSING_CELL")
            return self._abstain(req, "NO_EXACT_GENERATION_LICENSE")
        if len(matches) != 1:
            return self._abstain(req, "CONFLICTING_GENERATION_LICENSES")
        lic = matches[0]
        surface = self._assemble(lic)
        features = {
            "construction_id": lic["construction_id"],
            "candidate_id": lic["candidate_id"],
            "tam": lic["tam"],
            "person": lic["person"],
            "slots": dict(lic["request_slots"]),
            "target_scope": lic["target_scope"],
        }
        return GenerationResult(
            status="LICENSED_GENERATION",
            surface=surface,
            reason="EXACT_SOURCE_ATTESTED_ASSEMBLY",
            construction_id=req.construction_id,
            license_id=lic["license_id"],
            cell_id=lic["cell_id"],
            evidence_ids=(lic["cell_evidence_id"],),
            source_refs=tuple(lic["source_refs"]),
            origin=lic["origin"],
            novelty=lic["novelty"],
            analysis_features=features,
        )

    def analyze_licensed_surface(self, surface: str) -> tuple[dict[str, Any], ...]:
        """Exact license-index round trip; not a replacement for the analyzer core."""
        out = []
        for lic in self.licenses:
            if self._assemble(lic) == surface:
                out.append({
                    "license_id": lic["license_id"],
                    "construction_id": lic["construction_id"],
                    "candidate_id": lic["candidate_id"],
                    "tam": lic["tam"],
                    "person": lic["person"],
                    "slots": dict(lic["request_slots"]),
                    "target_scope": lic["target_scope"],
                    "evidence_id": lic["cell_evidence_id"],
                })
        return tuple(out)

    @staticmethod
    def _abstain(req: GenerationRequest, reason: str) -> GenerationResult:
        return GenerationResult(
            status="ABSTAIN",
            surface="",
            reason=reason,
            construction_id=req.construction_id,
            license_id=None,
            cell_id=None,
            evidence_ids=(),
            source_refs=(),
            origin=None,
            novelty=None,
            analysis_features={
                "construction_id": req.construction_id,
                "candidate_id": req.candidate_id,
                "tam": req.tam,
                "person": req.person,
                "slots": dict(req.slots),
                "target_scope": req.target_scope,
            },
        )


def main() -> None:
    eng = LicensedGeneratorV0()
    probes = [
        GenerationRequest("C01", "NC001-V01", "COMPLETIVE", "1SG", {"TEMPORAL_CONTEXT": "ALREADY"}),
        GenerationRequest("C02", "NC001-V01", "HABITUAL", "3SG_HUMAN", {"NEG_PATTERN": "QUE_PRED_GUIRA_DXI"}),
        GenerationRequest("C03", "NC001-V01", "COMPLETIVE", "2SG", {"PRAGMATIC_FUNCTION": "INFORMATION_QUESTION"}),
        GenerationRequest("C06", "NC001-V05", "HABITUAL", "1SG", {}),
    ]
    print(json.dumps([asdict(eng.generate(x)) for x in probes], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
