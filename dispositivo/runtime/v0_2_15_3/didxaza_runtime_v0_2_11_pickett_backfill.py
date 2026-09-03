#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
from dataclasses import dataclass
from collections import defaultdict
from pathlib import Path
from typing import Iterable,Mapping,Optional,Any
import csv,json,uuid

from didxaza_runtime_v0_2_6_evidence_adjudication import EvidenceAtom
from didxaza_runtime_v0_2_9_surface_evidence_coverage import surface_key

RUNTIME_VERSION="0.2.11"
RUNTIME_STAGE="PICKETT_LEXICAL_BACKFILL"
AUTO_CORRECT_ENABLED=False
ORTHOGRAPHIC_SUGGESTIONS_ENABLED=False
EDIT_EXECUTION_ENABLED=False
USER_VISIBLE_SUGGESTIONS_ENABLED=False

@dataclass(frozen=True)
class PickettLexicalRecord:
    record_id:str
    headword_raw_2007:str
    surface_2013_reconciled:str
    primary_surface_2013_reconciled:str
    variants_2013_reconciled:tuple[str,...]
    record_type:str
    parent_headword_2013_reconciled:str
    grammatical_label_raw:str
    tone_annotation_raw:str
    gloss_es:str
    printed_page:int
    pdf_page_2007:int
    source_id:str
    source_edition_extracted:str
    target_edition:str
    reconciliation_status:str
    dialect_scope:tuple[str,...]
    extraction_status:str

class PickettLexicalIndex:
    def __init__(self,rows:Iterable[Mapping[str,str]]):
        self.records={}
        self.by_exact_surface=defaultdict(list)
        self.primary_count=0
        self.subentry_count=0
        for r in rows:
            variants=tuple(json.loads(r["variants_2013_reconciled_json"]))
            rec=PickettLexicalRecord(
                record_id=r["record_id"],
                headword_raw_2007=r["headword_raw_2007"],
                surface_2013_reconciled=r["surface_2013_reconciled"],
                primary_surface_2013_reconciled=r["primary_surface_2013_reconciled"],
                variants_2013_reconciled=variants,
                record_type=r["record_type"],
                parent_headword_2013_reconciled=r["parent_headword_2013_reconciled"],
                grammatical_label_raw=r["grammatical_label_raw"],
                tone_annotation_raw=r["tone_annotation_raw"],
                gloss_es=r["gloss_es"],
                printed_page=int(r["printed_page"]),
                pdf_page_2007=int(r["pdf_page_2007"]),
                source_id=r["source_id"],
                source_edition_extracted=r["source_edition_extracted"],
                target_edition=r["target_edition"],
                reconciliation_status=r["reconciliation_status"],
                dialect_scope=(r["dialect_scope"],),
                extraction_status=r["extraction_status"],
            )
            self.records[rec.record_id]=rec
            if rec.record_type=="ENTRY":self.primary_count+=1
            elif rec.record_type=="SUBENTRY":self.subentry_count+=1

            surfaces=set(variants)
            surfaces.add(rec.surface_2013_reconciled)
            surfaces.add(rec.primary_surface_2013_reconciled)
            for s in surfaces:
                if s.strip():
                    self.by_exact_surface[surface_key(s)].append(rec.record_id)

    @classmethod
    def from_csv(cls,path:str|Path):
        with Path(path).open(encoding="utf-8-sig",newline="") as f:
            return cls(csv.DictReader(f))

    def lookup_exact(self,text:str)->tuple[PickettLexicalRecord,...]:
        return tuple(self.records[x] for x in self.by_exact_surface.get(surface_key(text),()))

def pickett_surface_atom(rec:PickettLexicalRecord,*,target_ref:str,start:int,end:int,observed_surface:str)->EvidenceAtom:
    # Must correspond to one of the surfaces actually indexed for this record.
    candidates=set(rec.variants_2013_reconciled)|{
        rec.surface_2013_reconciled,rec.primary_surface_2013_reconciled
    }
    if surface_key(observed_surface) not in {surface_key(x) for x in candidates if x}:
        raise ValueError("Observed surface is not an exact Pickett surface")
    return EvidenceAtom(
        atom_id=str(uuid.uuid4()),target_ref=target_ref,target_start=start,target_end=end,
        claim_type="DOCUMENTED_SURFACE_ATTESTATION",
        value={"surface":observed_surface,"semantic_equivalence":False},
        provenance_type="SOURCE_DIRECT",
        source_ids=(rec.source_id,),
        rule_ids=("PICKETT-EXACT-LEXICAL-SURFACE",),
        dialect_scope=rec.dialect_scope,
        epistemic_status="DOCUMENTED",evidence_strength="STRONG",
        raw_payload={
            "record_id":rec.record_id,
            "headword_raw_2007":rec.headword_raw_2007,
            "surface_2013_reconciled":rec.surface_2013_reconciled,
            "record_type":rec.record_type,
            "parent_headword":rec.parent_headword_2013_reconciled,
            "gloss_es":rec.gloss_es,
            "tone_annotation_raw":rec.tone_annotation_raw,
            "grammatical_label_raw":rec.grammatical_label_raw,
            "printed_page":rec.printed_page,
            "reconciliation_status":rec.reconciliation_status,
            "semantic_equivalence":False,
        },
        surface_claim=True
    )

def pickett_lexical_atom(rec:PickettLexicalRecord,*,target_ref:str,start:int,end:int,observed_surface:str)->EvidenceAtom:
    return EvidenceAtom(
        atom_id=str(uuid.uuid4()),target_ref=target_ref,target_start=start,target_end=end,
        claim_type="PICKETT_LEXICAL_RECORD",
        value={"record_id":rec.record_id,"gloss_es":rec.gloss_es},
        provenance_type="LEXICAL_RETRIEVAL",
        source_ids=(rec.source_id,),
        rule_ids=("PICKETT-LEXICAL-BACKFILL",),
        dialect_scope=rec.dialect_scope,
        epistemic_status="RETRIEVED_ONLY",
        evidence_strength="MODERATE",
        raw_payload={
            "observed_surface":observed_surface,
            "record_type":rec.record_type,
            "source_page":rec.printed_page,
            "semantic_equivalence_to_target":False,
        },
        surface_claim=False
    )

def status()->dict[str,Any]:
    return {
        "runtime_version":RUNTIME_VERSION,
        "runtime_stage":RUNTIME_STAGE,
        "pickett_lexical_backfill":"IMPLEMENTED",
        "pickett_2013_raw_byte_extraction":"NO",
        "pickett_2013_reconciliation":"DOCUMENTED_RULES_ONLY",
        "rule_based_surface_generation":"DISABLED",
        "pdlma_to_surface":"PROHIBITED",
        "auto_correct_enabled":False,
        "orthographic_suggestions_enabled":False,
        "edit_execution_enabled":False,
        "user_visible_suggestions_enabled":False,
    }
