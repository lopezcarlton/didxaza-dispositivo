#!/usr/bin/env python3
from __future__ import annotations
import csv, json, os, re, sqlite3, sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

ORCHESTRATOR_VERSION='0.35'
STATUS_ANALYZED='PARTIAL_ANALYSIS_NON_LICENSING'
STATUS_ABSTAIN='ABSTAIN_NO_COMPONENT_EVIDENCE'

class OrchestratorError(RuntimeError): pass

def _open_ro(db_path: Path):
    return sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)

def _token_spans(text:str):
    return [(m.start(),m.end(),m.group(0)) for m in re.finditer(r'\S+', text or '')]

def _covered_token_indexes(text, matches):
    toks=_token_spans(text); covered=set()
    for m in matches:
        for i,(s,e,_) in enumerate(toks):
            if not (e <= m.start or s >= m.end): covered.add(i)
    return sorted(covered), len(toks)

class NonLicensingAnalyzerOrchestrator:
    def __init__(self, runtime_root:str|Path, sqlite_path:str|Path, verb_inventory_path:str|Path|None=None):
        self.runtime_root=Path(runtime_root); self.sqlite_path=Path(sqlite_path)
        if not self.runtime_root.exists(): raise OrchestratorError('RUNTIME_ROOT_MISSING')
        if not self.sqlite_path.exists(): raise OrchestratorError('SQLITE_MISSING')
        sys.path.insert(0,str(self.runtime_root))
        from didxaza_runtime_v0_2_1_retrieval import DictionariaLoader, RetrievalEngine
        from didxaza_runtime_v0_2_4_bound import BoundInventory
        from didxaza_runtime_v0_2_5_morphology_ii import MorphologyIIInventory
        from didxaza_runtime_v0_2_3_morphology_i import MorphologyEngine, VerbInventoryLoader
        entries,senses,examples=DictionariaLoader.load(
            self.runtime_root/'DICTIONARIA_entries_v0_2_15_2.csv',
            self.runtime_root/'DICTIONARIA_senses_v0_2_15_2.csv',
            self.runtime_root/'DICTIONARIA_examples_v0_2_15_2.csv')
        self.retrieval=RetrievalEngine(entries,senses,examples)
        self.bound=BoundInventory(entries)
        self.morph2=MorphologyIIInventory(entries)
        if verb_inventory_path is None:
            verb_inventory_path = Path(__file__).with_name('DIC_VERB_2385_v0_1.csv')
        self.verb_inventory_path=Path(verb_inventory_path)
        records=VerbInventoryLoader.load_csv(self.verb_inventory_path)
        self.morph1=MorphologyEngine(records)
        self.db=_open_ro(self.sqlite_path)
        self.verb_meta={r[0]: {'verb_class':r[1],'analysis_codes_raw':r[2]} for r in self.db.execute(
            'select entry_id,verb_class,analysis_codes_raw from verb_lexeme_class_v023')}
        self.person_exact={r[0]: {'record_id':r[1],'category':r[2],'analysis':r[3],'source_id':r[4],'dialect_scope':r[5]} for r in self.db.execute(
            'select surface_key,record_id,category,analysis,source_id,dialect_scope from person_possession_exact_v0214')}

    def close(self):
        try:self.db.close()
        except Exception:pass

    def _surface_key(self,s):
        # Query helper only. Does not authorize orthographic normalization.
        return re.sub(r'\s+',' ',(s or '').lower().strip())

    def analyze(self, surface:str, *, item_id:str|None=None, spanish_supplied:str|None=None, context_segments:list[dict[str,Any]]|None=None)->dict[str,Any]:
        surface=surface or ''
        matches=self.retrieval.span_matches(surface)
        lex=[]
        for m in matches:
            ev=self.retrieval.lexical_evidence_for_match(m, '')  # Didxazá-only primary channel.
            for e in ev['entries']:
                vm=self.verb_meta.get(e['entry_id'])
                if vm: e['canonical_verb_metadata_read_only']=vm
            lex.append(ev)
        bound_whole=[asdict(x) for x in self.bound.exact_surface_analyses(surface)]
        deriv_whole=[asdict(x) for x in self.morph2.analyze_derivation_surface(surface)]
        caus_whole=[asdict(x) for x in self.morph2.analyze_causative_surface(surface)]
        poss_candidate=self.morph2.possession_candidate(surface) if len(_token_spans(surface))==1 else None
        # Morphology I: documented orthographic HABITUAL headword recognition only.
        # PDLMA forms are NOT projected onto orthographic input.
        morph1_surface=[]
        morph_token_indexes=set()
        person_graph=[]
        seen_morph=set()
        for i,(ts,te,traw) in enumerate(_token_spans(surface)):
            exact_lex_entries=set()
            for ev in lex:
                sp=ev.get('span',{})
                if sp.get('start')==ts and sp.get('end')==te:
                    exact_lex_entries.update(e.get('entry_id') for e in ev.get('entries',[]) if e.get('entry_id'))
            for x in self.morph1.analyze_surface(traw):
                key=(i,x.entry_id,x.tam,x.recognition_basis)
                if key in seen_morph: continue
                seen_morph.add(key)
                d=asdict(x); d['span']={'start':ts,'end':te,'raw':traw}
                d['exact_lexical_entry_candidate_count']=len(exact_lex_entries)
                d['contextual_resolution_status']=(
                    'CANDIDATE_ONLY_HOMOGRAPHY_UNRESOLVED' if len(exact_lex_entries)>1
                    else 'DOCUMENTED_UNIQUE_SURFACE_MATCH_NOT_FULL_SENTENCE_RESOLUTION'
                )
                morph1_surface.append(d); morph_token_indexes.add(i)
                for pc in self.morph1.person_candidates(traw):
                    pd=asdict(pc); pd['span']={'start':ts,'end':te,'raw':traw}; pd['linked_morphology_i_entry_id']=x.entry_id; person_graph.append(pd)
        exact_person=self.person_exact.get(self._surface_key(surface))
        covered,total=_covered_token_indexes(surface,matches)
        covered=sorted(set(covered)|morph_token_indexes)
        evidence_present=bool(lex or morph1_surface or bound_whole or deriv_whole or caus_whole or exact_person)
        # Provisional graphical candidates alone never promote the analysis status.
        status=STATUS_ANALYZED if evidence_present else STATUS_ABSTAIN
        return {
            'item_id':item_id,
            'surface_original':surface,
            'analysis_status':status,
            'orchestrator_version':ORCHESTRATOR_VERSION,
            'analysis_scope':'NON_LICENSING_PARTIAL_COMPONENT_ANALYSIS',
            'local_analysis_guaranteed_when_context_absent':True,
            'context_channel':{
                'context_supplied': bool(context_segments),
                'context_segment_count': len(context_segments or []),
                'used_for_local_analysis': False,
                'status': 'OPTIONAL_CONTEXT_RESERVED_NO_LOCAL_EFFECT_v0_35' if context_segments else 'NO_CONTEXT_SUPPLIED_LOCAL_ANALYSIS_PROCEEDS',
            },
            'context_sensitive_claim_policy':'UNRESOLVED_CONTEXT_SENSITIVE_CLAIMS_MUST_NOT_BLOCK_LOCAL_ANALYSIS',
            'generation_license_assertion':False,
            'correction_assertion':False,
            'orthographic_authority_assertion':False,
            'rule_discovery_assertion':False,
            'spanish_supplied_preserved_but_not_used_for_primary_analysis':spanish_supplied,
            'lexical_span_match_count':len(matches),
            'lexical_span_evidence':lex,
            'morphology_i_documented_surface_analyses':morph1_surface,
            'morphology_i_inventory_row_count':len(self.morph1.records),
            'matched_token_indexes':covered,
            'token_count':total,
            'matched_token_count':len(covered),
            'whole_surface_bound_analyses':bound_whole,
            'whole_surface_derivation_analyses':deriv_whole,
            'whole_surface_causative_analyses':caus_whole,
            'whole_surface_exact_person_possession':exact_person,
            'provisional_graphical_person_candidates':person_graph,
            'provisional_possession_prefix_candidate':asdict(poss_candidate) if poss_candidate else None,
            'limitations':[
                'PARTIAL_LEXICAL_MATCH_IS_NOT_FULL_SENTENCE_ANALYSIS',
                'MORPHOLOGY_I_SURFACE_CHANNEL_IS_DOCUMENTED_HABITUAL_HEADWORD_ONLY',
                'NO_PDLMA_TO_SURFACE_INFERENCE',
                'NO_UNATTESTED_MORPHOLOGICAL_DECOMPOSITION',
                'NO_GENERATION_LICENSE_FROM_ANALYSIS',
                'NO_RULE_DISCOVERY_FROM_COR001',
                'CONTEXT_ABSENCE_NEVER_BLOCKS_LOCAL_ANALYSIS',
                'OPTIONAL_CONTEXT_MAY_NOT_REWRITE_RAW_LOCAL_EVIDENCE',
                'UNRESOLVED_CONTEXT_SENSITIVE_CLAIM_IS_NOT_ERROR',
            ],
        }

def run_manifest(manifest_path, output_path, runtime_root, sqlite_path, verb_inventory_path=None):
    orch=NonLicensingAnalyzerOrchestrator(runtime_root,sqlite_path,verb_inventory_path)
    rows=[]
    try:
        with open(manifest_path,encoding='utf-8') as f:
            for line in f:
                if not line.strip():continue
                r=json.loads(line)
                if r.get('corpus_id')=='COR001':
                    assert r.get('analysis_status')=='ANALYSIS_TARGET_ONLY'
                    assert not r.get('benchmark_allowed') and not r.get('gold_allowed') and not r.get('rule_discovery_allowed')
                rows.append(orch.analyze(r.get('didxaza_supplied_draft_transcription',''),item_id=r.get('item_id'),spanish_supplied=r.get('spanish_supplied')))
    finally: orch.close()
    with open(output_path,'w',encoding='utf-8') as f:
        for r in rows:f.write(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n')
    return rows

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser(); p.add_argument('--manifest',required=True);p.add_argument('--output',required=True);p.add_argument('--runtime-root',required=True);p.add_argument('--sqlite',required=True);p.add_argument('--verb-inventory')
    a=p.parse_args(); run_manifest(a.manifest,a.output,a.runtime_root,a.sqlite,a.verb_inventory)
