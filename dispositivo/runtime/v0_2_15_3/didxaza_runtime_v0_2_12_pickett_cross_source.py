#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
from dataclasses import dataclass
from collections import defaultdict
from pathlib import Path
from typing import Iterable,Optional,Any
import re,uuid

from didxaza_runtime_v0_2_6_evidence_adjudication import EvidenceAtom
from didxaza_runtime_v0_2_9_surface_evidence_coverage import surface_key
from didxaza_runtime_v0_2_11_pickett_backfill import PickettLexicalRecord,PickettLexicalIndex

RUNTIME_VERSION="0.2.12"
RUNTIME_STAGE="PICKETT_INTERNAL_SURFACE_CROSS_SOURCE"
AUTO_CORRECT_ENABLED=False
ORTHOGRAPHIC_SUGGESTIONS_ENABLED=False
EDIT_EXECUTION_ENABLED=False
USER_VISIBLE_SUGGESTIONS_ENABLED=False

@dataclass(frozen=True)
class PickettInternalSurface:
    record_id:str
    parent_headword:str
    record_type:str
    source_surface_raw:str
    span_surface_raw:str
    span_key:str
    token_start:int
    token_end:int
    source_id:str="BIB003_PICKETT_VOCABULARIO"
    dialect_scope:tuple[str,...]=("JUCHITAN_HISTORICAL_SOURCE",)
    semantic_equivalence:bool=False
    lexical_equivalence:bool=False

@dataclass(frozen=True)
class CrossSourceExactSurface:
    surface_key:str
    pickett_record_ids:tuple[str,...]
    dictionaria_refs:tuple[str,...]
    source_ids:tuple[str,...]=("BIB003_PICKETT_VOCABULARIO","BIB054_DICTIONARIA")
    universal_scope:bool=False
    semantic_equivalence:bool=False

def _tokens(text:str):
    return tuple(x for x in re.split(r"\s+",(text or "").strip()) if x)

class PickettInternalSurfaceIndex:
    def __init__(self,pickett:PickettLexicalIndex,max_tokens:int=4):
        self.max_tokens=max_tokens
        self.by_key=defaultdict(list)
        self.multiword_records=0
        self.ngram_count=0
        for rec in pickett.records.values():
            # Each documented variant is processed independently. No ngram may cross variants.
            seen_sources=set()
            for src in rec.variants_2013_reconciled:
                if not src or src in seen_sources: continue
                seen_sources.add(src)
                toks=_tokens(src)
                if len(toks)<2: continue
                self.multiword_records+=1
                for n in range(1,min(max_tokens,len(toks))+1):
                    for i in range(len(toks)-n+1):
                        raw=" ".join(toks[i:i+n])
                        item=PickettInternalSurface(
                            record_id=rec.record_id,
                            parent_headword=rec.parent_headword_2013_reconciled,
                            record_type=rec.record_type,
                            source_surface_raw=src,
                            span_surface_raw=raw,
                            span_key=surface_key(raw),
                            token_start=i,token_end=i+n,
                        )
                        self.by_key[item.span_key].append(item)
                        self.ngram_count+=1

    def lookup_exact(self,text:str)->tuple[PickettInternalSurface,...]:
        return tuple(self.by_key.get(surface_key(text),()))

class CrossSourceSurfaceRegistry:
    def __init__(self,pickett_index:PickettLexicalIndex,pickett_internal:PickettInternalSurfaceIndex,
                 dictionaria_surface_index):
        p=defaultdict(set)
        for key,ids in pickett_index.by_exact_surface.items():
            p[key].update(ids)
        for key,items in pickett_internal.by_key.items():
            p[key].update(x.record_id for x in items)

        d=defaultdict(set)
        for key,atts in dictionaria_surface_index.by_key.items():
            for a in atts:
                ref=a.entry_id or a.example_id or a.source_location
                if ref:d[key].add(ref)

        self.by_key={}
        for key in p.keys() & d.keys():
            self.by_key[key]=CrossSourceExactSurface(
                surface_key=key,
                pickett_record_ids=tuple(sorted(p[key])),
                dictionaria_refs=tuple(sorted(d[key])),
            )

    def lookup_exact(self,text:str)->Optional[CrossSourceExactSurface]:
        return self.by_key.get(surface_key(text))

def pickett_internal_surface_atom(item:PickettInternalSurface,*,target_ref:str,start:int,end:int,observed_surface:str)->EvidenceAtom:
    if surface_key(observed_surface)!=item.span_key:
        raise ValueError("Observed surface does not match Pickett internal attestation")
    return EvidenceAtom(
        atom_id=str(uuid.uuid4()),target_ref=target_ref,target_start=start,target_end=end,
        claim_type="DOCUMENTED_SURFACE_ATTESTATION",
        value={"surface":observed_surface,"semantic_equivalence":False},
        provenance_type="SOURCE_DIRECT",
        source_ids=(item.source_id,),
        rule_ids=("PICKETT-INTERNAL-EXACT-SURFACE",),
        dialect_scope=item.dialect_scope,
        epistemic_status="DOCUMENTED",evidence_strength="STRONG",
        raw_payload={
            "record_id":item.record_id,
            "parent_headword":item.parent_headword,
            "record_type":item.record_type,
            "source_surface_raw":item.source_surface_raw,
            "token_start":item.token_start,
            "token_end":item.token_end,
            "semantic_equivalence":False,
            "lexical_equivalence":False,
        },
        surface_claim=True,
    )

def cross_source_atom(cross:CrossSourceExactSurface,*,target_ref:str,start:int,end:int,observed_surface:str)->EvidenceAtom:
    if surface_key(observed_surface)!=cross.surface_key:
        raise ValueError("Cross-source surface mismatch")
    return EvidenceAtom(
        atom_id=str(uuid.uuid4()),target_ref=target_ref,target_start=start,target_end=end,
        claim_type="CROSS_SOURCE_EXACT_SURFACE",
        value={"surface":observed_surface,"source_count":2},
        provenance_type="SOURCE_DIRECT",
        source_ids=cross.source_ids,
        rule_ids=("CROSS-SOURCE-EXACT-SURFACE",),
        dialect_scope=("JUCHITAN_HISTORICAL_SOURCE","UNKNOWN"),
        epistemic_status="DOCUMENTED",evidence_strength="STRONG",
        raw_payload={
            "pickett_record_ids":cross.pickett_record_ids,
            "dictionaria_refs":cross.dictionaria_refs,
            "universal_scope":False,
            "semantic_equivalence":False,
            "source_count_is_confidence_score":False,
        },
        surface_claim=False,
    )

def status()->dict[str,Any]:
    return {
        "runtime_version":RUNTIME_VERSION,
        "runtime_stage":RUNTIME_STAGE,
        "pickett_internal_surface_index":"IMPLEMENTED_EXACT_ONLY",
        "cross_source_exact_surface":"IMPLEMENTED_PROVENANCE_ONLY",
        "source_count_as_confidence":"PROHIBITED",
        "rule_based_surface_generation":"DISABLED",
        "pdlma_to_surface":"PROHIBITED",
        "auto_correct_enabled":False,
        "orthographic_suggestions_enabled":False,
        "edit_execution_enabled":False,
        "user_visible_suggestions_enabled":False,
    }
