#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Callable

HERE = Path(__file__).resolve().parent
INPUTS = HERE.parent / "inputs_nc001"
LICENSES = HERE / "GenerationLicense_v0_33_c02_default_qui.jsonl"
BLOCKERS = HERE / "IntegrationBlockers_v0_1.jsonl"
EVIDENCE = HERE / "GenerationEvidenceAtoms_v0_33_c02_default_qui.jsonl"
SLOT_FILLERS = HERE / "AuthorizedSlotFillers_v0_33.jsonl"
ADOPTIONS = INPUTS / "AdoptionRecords_v1.jsonl"

ALLOWED_MATERIAL_ORIGINS = {"SOURCE_ATTESTATION", "SPEAKER_ATTESTATION"}
FORBIDDEN_LICENSE_ORIGINS = {"PROJECT_GENERATED", "PROJECT_NORMALIZED"}
ADOPTED_ORTH_STATUS = {"ADOPTED_HARD_GUARD", "ADOPTED_CONSERVATIVE_GUARD"}
NOVEL_CELL_BLOCKER_MARKERS = (
    "GENERATION_PENDING_VALENCY",
    "TARGET_SURFACE_GENERATION_BLOCKED_DIALECT_CELL_LOCALITY",
)
ORTH_RESOLUTIONS = HERE / "OrthographicResolutions_v0_9.jsonl"
ROUNDTRIP_CONTRACT_VERSION = "0.2"
ROUNDTRIP_ANALYSIS_SEMANTICS = "STRUCTURAL_COMPATIBILITY_ONLY_NON_LICENSING"


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
    surface_origin: str | None = None
    construction_evidence_ids: tuple[str, ...] = ()
    paradigm_cell_evidence_ids: tuple[str, ...] = ()
    slot_filler_evidence_ids: tuple[str, ...] = ()
    orthographic_policy_ids: tuple[str, ...] = ()
    whole_surface_evidence_id: str | None = None


class LicensedGeneratorV02:
    """Generator_v0.2 round-trip contract stabilization.

    Zero-novelty generation remains materialized-input based. Novel generation
    additionally requires independently reusable slot evidence, explicit
    orthographic project-policy IDs, and a canonical ANALYZER round-trip.
    """

    def __init__(self, *, inputs_dir: Path = INPUTS, licenses_path: Path = LICENSES,
                 blockers_path: Path = BLOCKERS, evidence_path: Path = EVIDENCE,
                 slot_fillers_path: Path = SLOT_FILLERS, adoptions_path: Path = ADOPTIONS,
                 orth_resolutions_path: Path = ORTH_RESOLUTIONS, canonical_analyzer: Callable[[str], dict[str, Any]] | None = None):
        self.inputs_dir = Path(inputs_dir)
        self.cells = self._load_cells(self.inputs_dir / "ParadigmTable_v1.csv")
        self.constructions = self._load_jsonl_index(self.inputs_dir / "ConstructionInventory_v1.jsonl", "construction_id")
        self.licenses = self._load_jsonl(licenses_path)
        self.blockers = self._load_jsonl_index(blockers_path, "construction_id")
        self.evidence = self._load_jsonl_index(evidence_path, "atom_id")
        self.slot_fillers = self._load_jsonl_index(slot_fillers_path, "slot_filler_license_id")
        self.adoptions = self._load_jsonl_index(adoptions_path, "adoption_id")
        self.orth_resolutions = self._load_jsonl_index(orth_resolutions_path, "cell_id") if Path(orth_resolutions_path).exists() else {}
        self.canonical_analyzer = canonical_analyzer
        self._validate_materialized_licenses()
        self._validate_slot_fillers()

    @staticmethod
    def _load_jsonl(path: Path) -> list[dict[str, Any]]:
        with Path(path).open(encoding="utf-8") as f:
            return [json.loads(line) for line in f if line.strip()]

    @classmethod
    def _load_jsonl_index(cls, path: Path, key: str) -> dict[str, dict[str, Any]]:
        return {row[key]: row for row in cls._load_jsonl(path)}

    @staticmethod
    def _load_cells(path: Path) -> dict[str, dict[str, str]]:
        with Path(path).open(encoding="utf-8-sig", newline="") as f:
            return {row["cell_id"]: row for row in csv.DictReader(f)}

    def _evidence_atom(self, eid: str, role: str, *, independent: bool = False) -> dict[str, Any]:
        atom = self.evidence.get(eid)
        if not atom:
            raise ValueError(f"Missing material evidence atom: {eid}")
        payload = atom.get("raw_payload") or {}
        if payload.get("evidence_role") != role:
            raise ValueError(f"Evidence role mismatch: {eid} expected={role}")
        origin = payload.get("evidence_origin")
        if origin in FORBIDDEN_LICENSE_ORIGINS or origin not in ALLOWED_MATERIAL_ORIGINS:
            raise ValueError(f"Derived evidence cannot license generation: {eid}:{origin}")
        if independent and payload.get("reuse_scope") != "INDEPENDENT_SUBSTITUTION_LICENSE":
            raise ValueError(f"Evidence is not independently reusable: {eid}")
        return atom

    def _orthographic_policy_gate(self, policy_ids: list[str] | tuple[str, ...], surface: str, *, novel: bool) -> tuple[bool, str]:
        if novel and not policy_ids:
            return False, "ORTHOGRAPHIC_POLICY_IDS_REQUIRED_FOR_NOVELTY"
        for pid in policy_ids:
            rec = self.adoptions.get(pid)
            if not rec:
                return False, f"UNKNOWN_ORTHOGRAPHIC_POLICY:{pid}"
            if rec.get("status") not in ADOPTED_ORTH_STATUS:
                return False, f"ORTHOGRAPHIC_POLICY_NOT_ADOPTED_FOR_GATE:{pid}"
        required = {"AR-NC001-ORTH-007"} if novel else set()
        if any(ch in surface for ch in ("'", "’", "ʼ", "ꞌ")):
            required.add("AR-NC001-ORTH-004")
        # Explicit accented/diacritic characters require preservation policy.
        if any(ord(ch) > 127 for ch in surface):
            required.add("AR-NC001-ORTH-003")
        missing = required.difference(policy_ids)
        if missing:
            return False, "MISSING_REQUIRED_ORTHOGRAPHIC_POLICY:" + ",".join(sorted(missing))
        return True, "ORTHOGRAPHIC_PROJECT_SLICE_GATE_PASS"

    def _cell_generation_surface(self, cell: dict[str, str]) -> str:
        res = self.orth_resolutions.get(cell["cell_id"])
        if not res:
            return cell["surface_observed"]
        status = res.get("status")
        if status == "BLOCKED_PENDING_REVIEW":
            raise ValueError(f"ORTHOGRAPHIC_OUTPUT_BLOCKED_PENDING_REVIEW:{cell['cell_id']}")
        if status != "ADOPTED_CELL_SPECIFIC":
            raise ValueError(f"UNKNOWN_ORTHOGRAPHIC_RESOLUTION_STATUS:{cell['cell_id']}:{status}")
        if res.get("raw_attested_surface") != cell.get("surface_observed"):
            raise ValueError(f"ORTHOGRAPHIC_RESOLUTION_RAW_SURFACE_MISMATCH:{cell['cell_id']}")
        if res.get("target_scope") != "JUCHITAN" or not res.get("canonical_generation_surface"):
            raise ValueError(f"ORTHOGRAPHIC_RESOLUTION_INCOMPLETE:{cell['cell_id']}")
        return str(res["canonical_generation_surface"])

    def _assemble(self, lic: dict[str, Any]) -> str:
        parts: list[str] = []
        for item in lic["assembly"]:
            if item["kind"] == "literal":
                parts.append(item["value"])
            elif item["kind"] == "cell":
                cell = self.cells[item["cell_id"]]
                parts.append(self._cell_generation_surface(cell))
            elif item["kind"] == "slot_filler":
                sf = self.slot_fillers[item["slot_filler_license_id"]]
                parts.append(sf["surface"])
            else:
                raise ValueError(f"Unsupported assembly item: {item['kind']}")
        return " ".join(parts)

    def _validate_slot_fillers(self) -> None:
        for sfid, sf in self.slot_fillers.items():
            if sf.get("target_scope") != "JUCHITAN":
                raise ValueError(f"Slot filler not Juchitán-scoped: {sfid}")
            if not sf.get("may_license_generation"):
                raise ValueError(f"Slot filler cannot license generation: {sfid}")
            construction = self.constructions.get(sf.get("construction_id"))
            if not construction:
                raise ValueError(f"Unknown construction for slot filler: {sfid}")
            if not set(sf.get("tam_scope", [])).issubset(set(construction.get("tam_scope", []))):
                raise ValueError(f"Slot filler TAM scope exceeds construction scope: {sfid}")
            for eid in sf.get("evidence_ids", []):
                self._evidence_atom(eid, "SLOT_FILLER_EVIDENCE", independent=True)
            for eid in sf.get("construction_evidence_ids", []):
                self._evidence_atom(eid, "CONSTRUCTION_EVIDENCE", independent=True)
            ok, reason = self._orthographic_policy_gate(sf.get("orthographic_policy_ids", []), sf["surface"], novel=True)
            if not ok:
                raise ValueError(f"Slot filler orthographic gate failed {sfid}: {reason}")

    def _validate_materialized_licenses(self) -> None:
        seen: set[str] = set()
        for lic in self.licenses:
            lid = lic["license_id"]
            if lid in seen:
                raise ValueError(f"Duplicate license_id: {lid}")
            seen.add(lid)
            if lic.get("license_contract_version") != "0.1":
                raise ValueError(f"License not hardened to v0.1: {lid}")
            if lic["origin"] not in ALLOWED_MATERIAL_ORIGINS:
                raise ValueError(f"Non-licensing origin in {lid}")
            for field in ("construction_evidence_ids", "paradigm_cell_evidence_ids", "slot_filler_evidence_ids", "orthographic_policy_ids"):
                if not lic.get(field):
                    raise ValueError(f"Missing explicit provenance field {field} in {lid}")
            for eid in lic["construction_evidence_ids"]:
                self._evidence_atom(eid, "CONSTRUCTION_EVIDENCE")
            for eid in lic["slot_filler_evidence_ids"]:
                self._evidence_atom(eid, "SLOT_FILLER_EVIDENCE")
            whole_id = lic.get("whole_surface_evidence_id")
            if whole_id and (whole_id in lic["construction_evidence_ids"] or whole_id in lic["slot_filler_evidence_ids"]):
                raise ValueError(f"Whole-surface evidence laundering across roles in {lid}")
            cell = self.cells.get(lic["cell_id"])
            if not cell:
                raise ValueError(f"Unknown cell in {lid}")
            if cell["status"] != "ATTESTED" or not cell["evidence_id"]:
                raise ValueError(f"Unattested cell in {lid}")
            if cell["evidence_id"] not in lic["paradigm_cell_evidence_ids"]:
                raise ValueError(f"Paradigm evidence mismatch in {lid}")
            if cell["dialect_scope"] not in {"JUCHITAN_EXPLICIT", "JUCHITAN_FIELDWORK_CORPUS_EXPLICIT"}:
                raise ValueError(f"Target scope not explicit in {lid}")
            res = self.orth_resolutions.get(cell["cell_id"])
            if res and lic.get("novelty") == "LICENSED_NOVEL_RECOMBINATION":
                if res.get("status") == "BLOCKED_PENDING_REVIEW":
                    raise ValueError(f"Novel license cell has unresolved orthographic output in {lid}:{cell['cell_id']}")
                if res.get("status") == "ADOPTED_CELL_SPECIFIC":
                    if lic.get("orthographic_resolution_id") != res.get("resolution_id"):
                        raise ValueError(f"Orthographic resolution not explicitly licensed in {lid}")
                    aid = res.get("adoption_id")
                    if not aid or aid not in lic.get("orthographic_policy_ids", []):
                        raise ValueError(f"Orthographic resolution adoption missing in {lid}")
            elif lic.get("orthographic_resolution_id"):
                raise ValueError(f"License declares unknown orthographic resolution in {lid}")
            if lic.get("novelty") == "LICENSED_NOVEL_RECOMBINATION":
                effect = cell.get("license_effect", "")
                blockers = [m for m in NOVEL_CELL_BLOCKER_MARKERS if m in effect]
                if blockers:
                    raise ValueError(f"Novel license cell has unresolved generation blocker in {lid}: {','.join(blockers)}")
            c = self.constructions.get(lic["construction_id"])
            if not c or c.get("generator", "").startswith("DISABLED"):
                raise ValueError(f"Unknown/disabled construction in {lid}")
            assembled = self._assemble(lic)
            novel = lic.get("novelty") == "LICENSED_NOVEL_RECOMBINATION"
            ok, reason = self._orthographic_policy_gate(lic["orthographic_policy_ids"], assembled, novel=novel)
            if not ok:
                raise ValueError(f"Orthographic gate failed {lid}: {reason}")
            if novel:
                if lic.get("whole_surface_attested") or whole_id is not None:
                    raise ValueError(f"Novel license cannot rely on whole-surface attestation: {lid}")
                if not lic.get("may_license_new_combinations"):
                    raise ValueError(f"Novel license must explicitly allow recombination: {lid}")
                if lic.get("surface_origin") != "PROJECT_GENERATED":
                    raise ValueError(f"Novel surface must be PROJECT_GENERATED: {lid}")
                if lic.get("license_evidence_origin", lic.get("origin")) not in ALLOWED_MATERIAL_ORIGINS:
                    raise ValueError(f"Novel license evidence origin must remain material: {lid}")
                for eid in lic["construction_evidence_ids"]:
                    self._evidence_atom(eid, "CONSTRUCTION_EVIDENCE", independent=True)
                for eid in lic["slot_filler_evidence_ids"]:
                    self._evidence_atom(eid, "SLOT_FILLER_EVIDENCE", independent=True)
            else:
                if lic.get("surface_origin", lic.get("origin")) not in ALLOWED_MATERIAL_ORIGINS:
                    raise ValueError(f"Zero-novelty surface origin must be material: {lid}")
                if not lic.get("whole_surface_attested") or not whole_id:
                    raise ValueError(f"Zero-novelty license requires material whole-surface evidence: {lid}")
                whole = self._evidence_atom(whole_id, "WHOLE_SURFACE_EVIDENCE")
                observed = (whole.get("raw_payload") or {}).get("observed_surface")
                if assembled != lic.get("attested_whole_surface") or assembled != observed:
                    raise ValueError(f"Whole surface evidence mismatch in {lid}")
                if lic.get("may_license_new_combinations"):
                    raise ValueError(f"Zero-novelty license cannot license new combinations: {lid}")

    @staticmethod
    def _signature_matches(req: GenerationRequest, lic: dict[str, Any]) -> bool:
        return (
            req.construction_id == lic["construction_id"] and req.candidate_id == lic["candidate_id"]
            and req.tam == lic["tam"] and req.person == lic["person"]
            and req.target_scope == lic["target_scope"] and req.slots == lic["request_slots"]
        )

    def _construction_predicate_valence_scope(self, evidence_ids: list[str] | tuple[str, ...]) -> list[str]:
        out: list[str] = []
        for eid in evidence_ids:
            atom = self._evidence_atom(eid, "CONSTRUCTION_EVIDENCE", independent=True)
            for value in (atom.get("raw_payload") or {}).get("predicate_valence_scope", []):
                if value not in out:
                    out.append(value)
        return out

    def _analysis_expected(self, req: GenerationRequest, lic: dict[str, Any]) -> dict[str, Any]:
        return {
            "construction_id":lic["construction_id"],"candidate_id":lic["candidate_id"],"cell_id":lic["cell_id"],
            "tam":lic["tam"],"person":lic["person"],"slots":dict(lic["request_slots"]),"target_scope":lic["target_scope"],
            "predicate_valence_scope":self._construction_predicate_valence_scope(lic.get("construction_evidence_ids", [])),
        }

    def _roundtrip_novel(self, surface: str, expected: dict[str, Any]) -> tuple[bool, str, dict[str, Any]]:
        if self.canonical_analyzer is None:
            return False, "CANONICAL_ANALYZER_ROUNDTRIP_UNAVAILABLE", {}
        observed = self.canonical_analyzer(surface)
        if observed.get("analysis_status") != "ANALYZED":
            return False, "CANONICAL_ANALYZER_ROUNDTRIP_NOT_ANALYZED", observed
        if observed.get("roundtrip_contract_version") != ROUNDTRIP_CONTRACT_VERSION:
            return False, "CANONICAL_ANALYZER_ROUNDTRIP_CONTRACT_MISMATCH", observed
        if observed.get("analysis_semantics") != ROUNDTRIP_ANALYSIS_SEMANTICS:
            return False, "CANONICAL_ANALYZER_ROUNDTRIP_SEMANTICS_MISMATCH", observed
        if observed.get("generation_license_assertion") is not False:
            return False, "CANONICAL_ANALYZER_MUST_BE_NON_LICENSING", observed
        keys = ("construction_id", "candidate_id", "cell_id", "tam", "person", "target_scope")
        if not all(observed.get(k) == expected.get(k) for k in keys):
            return False, "CANONICAL_ANALYZER_ROUNDTRIP_INCOMPATIBLE", observed
        if observed.get("recognized_slots") != expected.get("slots"):
            return False, "CANONICAL_ANALYZER_ROUNDTRIP_SLOT_MISMATCH", observed
        required_valence = expected.get("predicate_valence_scope") or []
        if required_valence:
            if observed.get("lexeme_metadata_source") != "verb_lexeme_class_v023":
                return False, "CANONICAL_ANALYZER_ROUNDTRIP_VALENCE_METADATA_UNAVAILABLE", observed
            if observed.get("lexeme_valence_subtype") not in required_valence:
                return False, "CANONICAL_ANALYZER_ROUNDTRIP_VALENCE_INCOMPATIBLE", observed
        return True, "CANONICAL_ANALYZER_ROUNDTRIP_COMPATIBLE", observed

    def generate(self, req: GenerationRequest) -> GenerationResult:
        if req.construction_id not in self.constructions: return self._abstain(req, "UNKNOWN_CONSTRUCTION")
        if req.target_scope != "JUCHITAN": return self._abstain(req, "TARGET_SCOPE_UNLICENSED")
        if req.tam not in {"HABITUAL", "COMPLETIVE"}: return self._abstain(req, "TAM_OUT_OF_SCOPE")
        if req.person not in {"1SG", "2SG", "3SG_HUMAN"}: return self._abstain(req, "PERSON_OUT_OF_SCOPE")
        construction = self.constructions[req.construction_id]
        if req.tam not in construction.get("tam_scope", []): return self._abstain(req, "CONSTRUCTION_TAM_NOT_LICENSED")
        if req.person not in construction.get("person_scope", []): return self._abstain(req, "CONSTRUCTION_PERSON_NOT_LICENSED")
        blocker = self.blockers.get(req.construction_id)
        if blocker: return self._abstain(req, blocker["reason"])
        matches = [lic for lic in self.licenses if self._signature_matches(req, lic)]
        if not matches:
            candidate_cells = [c for c in self.cells.values() if c["candidate_id"] == req.candidate_id and c["tam"] == req.tam and c["person"] == req.person]
            if not candidate_cells or candidate_cells[0]["status"] != "ATTESTED": return self._abstain(req, "MISSING_CELL")
            res = self.orth_resolutions.get(candidate_cells[0]["cell_id"])
            if res and res.get("status") == "BLOCKED_PENDING_REVIEW":
                return self._abstain(req, "ORTHOGRAPHIC_OUTPUT_BLOCKED_PENDING_REVIEW")
            return self._abstain(req, "NO_EXACT_GENERATION_LICENSE")
        if len(matches) != 1: return self._abstain(req, "CONFLICTING_GENERATION_LICENSES")
        lic = matches[0]
        surface = self._assemble(lic)
        features = self._analysis_expected(req, lic)
        if lic.get("novelty") == "LICENSED_NOVEL_RECOMBINATION":
            ok, reason, _observed = self._roundtrip_novel(surface, features)
            if not ok:
                return self._abstain(req, reason)
        all_evidence = tuple(dict.fromkeys(lic["construction_evidence_ids"] + lic["paradigm_cell_evidence_ids"] + lic["slot_filler_evidence_ids"] + ([lic["whole_surface_evidence_id"]] if lic.get("whole_surface_evidence_id") else [])))
        return GenerationResult(
            status="LICENSED_GENERATION", surface=surface,
            reason=("LICENSED_NOVEL_RECOMBINATION" if lic.get("novelty")=="LICENSED_NOVEL_RECOMBINATION" else "EXACT_SOURCE_ATTESTED_ASSEMBLY"),
            construction_id=req.construction_id, license_id=lic["license_id"], cell_id=lic["cell_id"],
            evidence_ids=all_evidence, source_refs=tuple(lic.get("source_refs", [])), origin=lic["origin"], novelty=lic["novelty"],
            analysis_features=features, surface_origin=lic.get("surface_origin", lic.get("origin")), construction_evidence_ids=tuple(lic["construction_evidence_ids"]),
            paradigm_cell_evidence_ids=tuple(lic["paradigm_cell_evidence_ids"]), slot_filler_evidence_ids=tuple(lic["slot_filler_evidence_ids"]),
            orthographic_policy_ids=tuple(lic["orthographic_policy_ids"]), whole_surface_evidence_id=lic.get("whole_surface_evidence_id"),
        )

    def evaluate_novel_candidate(self, attempt: dict[str, Any]) -> GenerationResult:
        """Evaluate a non-active novelty probe without silently promoting it to a license."""
        req = GenerationRequest(attempt["construction_id"], attempt["candidate_id"], attempt["tam"], attempt["person"], attempt["request_slots"], attempt.get("target_scope", "JUCHITAN"))
        construction = self.constructions.get(req.construction_id)
        if not construction: return self._abstain(req, "UNKNOWN_CONSTRUCTION")
        if req.tam not in construction.get("tam_scope", []): return self._abstain(req, "CONSTRUCTION_TAM_NOT_LICENSED")
        if req.person not in construction.get("person_scope", []): return self._abstain(req, "CONSTRUCTION_PERSON_NOT_LICENSED")
        if req.construction_id in self.blockers: return self._abstain(req, self.blockers[req.construction_id]["reason"])
        cell_id = f"{req.candidate_id}-{req.tam}-{req.person}"
        cell = self.cells.get(cell_id)
        if not cell or cell["status"] != "ATTESTED": return self._abstain(req, "MISSING_CELL")
        if cell["evidence_id"] not in attempt.get("paradigm_cell_evidence_ids", []): return self._abstain(req, "PARADIGM_EVIDENCE_NOT_EXPLICIT")
        parts=[]; slot_eids=[]; construction_eids=[]
        for sfid in attempt.get("slot_filler_license_ids", []):
            sf=self.slot_fillers.get(sfid)
            if not sf or sf["construction_id"] != req.construction_id: return self._abstain(req, "SLOT_FILLER_LICENSE_MISSING_OR_WRONG_CONSTRUCTION")
            parts.append(sf["surface"]); slot_eids += sf["evidence_ids"]; construction_eids += sf.get("construction_evidence_ids",[])
        try:
            parts.append(self._cell_generation_surface(cell))
        except ValueError as exc:
            if str(exc).startswith("ORTHOGRAPHIC_OUTPUT_BLOCKED_PENDING_REVIEW"):
                return self._abstain(req, "ORTHOGRAPHIC_OUTPUT_BLOCKED_PENDING_REVIEW")
            raise
        surface=" ".join(parts)
        if surface != attempt.get("proposed_surface"): return self._abstain(req, "NOVEL_ASSEMBLY_SURFACE_MISMATCH")
        if attempt.get("whole_surface_evidence_id") is not None: return self._abstain(req, "NOVELTY_MUST_NOT_REQUIRE_WHOLE_SURFACE_EVIDENCE")
        for eid in attempt.get("construction_evidence_ids", []): self._evidence_atom(eid, "CONSTRUCTION_EVIDENCE", independent=True)
        for eid in attempt.get("slot_filler_evidence_ids", []): self._evidence_atom(eid, "SLOT_FILLER_EVIDENCE", independent=True)
        ok, reason=self._orthographic_policy_gate(attempt.get("orthographic_policy_ids",[]), surface, novel=True)
        if not ok: return self._abstain(req, reason)
        expected={
            "construction_id":req.construction_id,"candidate_id":req.candidate_id,"cell_id":cell_id,"tam":req.tam,"person":req.person,
            "slots":dict(req.slots),"target_scope":req.target_scope,
            "predicate_valence_scope":self._construction_predicate_valence_scope(attempt.get("construction_evidence_ids", [])),
        }
        rt_ok, rt_reason, _ = self._roundtrip_novel(surface, expected)
        if not rt_ok:
            return self._abstain(req, "NO_LICENSED_NOVEL_RECOMBINATION_YET")
        return GenerationResult(
            status="NOVEL_CANDIDATE_READY_FOR_LICENSE",surface=surface,reason="ALL_HARDENING_GATES_PASS_PENDING_PERSISTED_LICENSE",
            construction_id=req.construction_id,license_id=None,cell_id=cell_id,
            evidence_ids=tuple(dict.fromkeys(construction_eids+[cell['evidence_id']]+slot_eids)),source_refs=(),origin="SOURCE_ATTESTATION",novelty="LICENSED_NOVEL_RECOMBINATION_CANDIDATE",
            analysis_features=expected,surface_origin="PROJECT_GENERATED",construction_evidence_ids=tuple(attempt.get("construction_evidence_ids",[])),paradigm_cell_evidence_ids=tuple(attempt.get("paradigm_cell_evidence_ids",[])),slot_filler_evidence_ids=tuple(attempt.get("slot_filler_evidence_ids",[])),orthographic_policy_ids=tuple(attempt.get("orthographic_policy_ids",[])),whole_surface_evidence_id=None,
        )

    @staticmethod
    def _abstain(req: GenerationRequest, reason: str) -> GenerationResult:
        return GenerationResult(status="ABSTAIN",surface="",reason=reason,construction_id=req.construction_id,license_id=None,cell_id=None,evidence_ids=(),source_refs=(),origin=None,novelty=None,analysis_features={"construction_id":req.construction_id,"candidate_id":req.candidate_id,"tam":req.tam,"person":req.person,"slots":dict(req.slots),"target_scope":req.target_scope})


def main() -> None:
    eng = LicensedGeneratorV02()
    probes = [
        GenerationRequest("C01", "NC001-V01", "COMPLETIVE", "1SG", {"TEMPORAL_CONTEXT": "ALREADY"}),
        GenerationRequest("C02", "NC001-V01", "HABITUAL", "3SG_HUMAN", {"NEG_PATTERN": "QUE_PRED_GUIRA_DXI"}),
        GenerationRequest("C03", "NC001-V01", "COMPLETIVE", "2SG", {"QUESTION_PATTERN": "UNMATERIALIZED_POLAR_PATTERN", "PRAGMATIC_FUNCTION": "POLAR_INFORMATION_QUESTION"}),
        GenerationRequest("C06", "NC001-V05", "HABITUAL", "1SG", {}),
    ]
    attempt=json.loads((HERE / "NovelRecombinationAttempt_v0_1.json").read_text(encoding="utf-8"))
    payload={"probes":[asdict(eng.generate(x)) for x in probes],"novel_attempt":asdict(eng.evaluate_novel_candidate(attempt))}
    print(json.dumps(payload,ensure_ascii=False,indent=2))


if __name__ == "__main__": main()
