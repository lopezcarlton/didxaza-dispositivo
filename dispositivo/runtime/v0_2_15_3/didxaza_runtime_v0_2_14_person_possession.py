from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from collections import defaultdict
from typing import Iterable,Mapping,Any
import csv,uuid

from didxaza_runtime_v0_2_6_evidence_adjudication import EvidenceAtom
from didxaza_runtime_v0_2_9_surface_evidence_coverage import surface_key

RUNTIME_VERSION="0.2.14"
RUNTIME_STAGE="PERSON_POSSESSION_DOCUMENTARY_ALIGNMENT"
AUTO_CORRECT_ENABLED=False
ORTHOGRAPHIC_SUGGESTIONS_ENABLED=False
EDIT_EXECUTION_ENABLED=False
USER_VISIBLE_SUGGESTIONS_ENABLED=False

@dataclass(frozen=True)
class ExactPersonPossessionRecord:
    record_id:str
    surface_raw:str
    category:str
    analysis:str
    source_id:str
    source_location:str
    dialect_scope:tuple[str,...]

class PersonPossessionExactIndex:
    def __init__(self,rows:Iterable[Mapping[str,str]]):
        self.records={}
        self.by_key=defaultdict(list)
        for r in rows:
            rec=ExactPersonPossessionRecord(
                r["record_id"],r["surface_raw"],r["category"],r["analysis"],
                r["source_id"],r["source_location"],(r["dialect_scope"],)
            )
            self.records[rec.record_id]=rec
            self.by_key[surface_key(rec.surface_raw)].append(rec)
    @classmethod
    def from_csv(cls,path):
        with Path(path).open(encoding="utf-8-sig",newline="") as f:
            return cls(csv.DictReader(f))
    def lookup_exact(self,text):
        return tuple(self.by_key.get(surface_key(text),()))

def documentary_atom(rec:ExactPersonPossessionRecord,*,target_ref,start,end,observed_surface):
    if surface_key(observed_surface)!=surface_key(rec.surface_raw):
        raise ValueError("not exact")
    ctype="DOCUMENTED_PERSON_FORM" if rec.category.startswith("PERSON") else "DOCUMENTED_POSSESSION_FORM"
    return EvidenceAtom(
        atom_id=str(uuid.uuid4()),target_ref=target_ref,target_start=start,target_end=end,
        claim_type=ctype,value={"surface":observed_surface,"analysis":rec.analysis},
        provenance_type="SOURCE_DIRECT",source_ids=(rec.source_id,),
        rule_ids=(rec.record_id,),dialect_scope=rec.dialect_scope,
        epistemic_status="DOCUMENTED",evidence_strength="DIRECT",
        raw_payload={"source_location":rec.source_location,"category":rec.category},
        surface_claim=True
    )

def qualify_candidate(claim,index:PersonPossessionExactIndex,observed_surface:str):
    ct=claim.claim_type if hasattr(claim,"claim_type") else claim.get("claim_type")
    if ct not in {"PERSON_SUFFIX_CANDIDATE","POSSESSION_PREFIX_CANDIDATE"}:
        return "NOT_APPLICABLE"
    if index.lookup_exact(observed_surface):
        return "DOCUMENTED_EXACT"
    return "HYPOTHESIS_ONLY"

def status()->dict[str,Any]:
    return {
        "runtime_version":RUNTIME_VERSION,
        "runtime_stage":RUNTIME_STAGE,
        "candidate_shape_is_evidence":False,
        "inverse_person_generation":"PROHIBITED",
        "productive_possession_generation":"PROHIBITED",
        "base_reconstruction":"PROHIBITED",
        "pdlma_to_surface":"PROHIBITED",
        "auto_correct_enabled":False,
        "orthographic_suggestions_enabled":False,
        "edit_execution_enabled":False,
        "user_visible_suggestions_enabled":False,
    }
