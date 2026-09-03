#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
from pathlib import Path
from dataclasses import asdict
from collections import Counter
import csv,json,re,unicodedata,hashlib,uuid,platform,sys

from didxaza_runtime_v0_2_0_foundation import ContextProfile,candidate_whitespace_spans,normalize_apostrophes
from didxaza_runtime_v0_2_1_retrieval import DictionariaLoader,RetrievalEngine
from didxaza_runtime_v0_2_3_morphology_i import VerbInventoryLoader,MorphologyEngine
from didxaza_runtime_v0_2_4_bound import BoundInventory
from didxaza_runtime_v0_2_5_morphology_ii import MorphologyIIInventory
from didxaza_runtime_v0_2_6_evidence_adjudication import (
    EvidenceAtom,EvidenceGraph,atom_from_retrieval,atom_from_morph_analysis,
    atom_from_bound_analysis,atom_for_explicit_conflict,
)
from didxaza_runtime_v0_2_7_decision_simulation import UnresolvedSpan
from didxaza_runtime_v0_2_9_surface_evidence_coverage import SurfaceAttestationIndex,surface_attestation_atom,derivation_atom_conclusion_only
from didxaza_runtime_v0_2_10_documentary_alignment import DocumentaryAlignmentIndex,alignment_surface_atom,alignment_analysis_atom,phrase_ngram_surface_atom,full_phrase_semantic_atom
from didxaza_runtime_v0_2_11_pickett_backfill import PickettLexicalIndex,pickett_surface_atom,pickett_lexical_atom
from didxaza_runtime_v0_2_12_pickett_cross_source import PickettInternalSurfaceIndex,CrossSourceSurfaceRegistry,pickett_internal_surface_atom
from didxaza_runtime_v0_2_14_person_possession import PersonPossessionExactIndex,qualify_candidate
from didxaza_runtime_v0_2_15_2_evidence_integrity import EvidenceAdjudicatorV0152
from didxaza_runtime_v0_2_15_3_surface_semantics_resolution_integrity import (
    DecisionSimulatorV0153,resolve_claims_v0153,qualify_bundle_v0153,sanitize_analysis_atom_v0153
)

RUNTIME_VERSION='0.2.15.3'
RUNTIME_STAGE='SURFACE_SEMANTICS_RESOLUTION_REPLAY'
DIC_EVIDENCE_SCOPE=('UNKNOWN',)
DIC_SOURCE_COVERAGE=('LA_VENTOSA','JUCHITAN','SANTA_MARIA_XADANI')

AUTO_CORRECT_ENABLED=False
ORTHOGRAPHIC_SUGGESTIONS_ENABLED=False
EDIT_EXECUTION_ENABLED=False
USER_VISIBLE_SUGGESTIONS_ENABLED=False

def sha256(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()

def semantic_sha(obj):
    # Remove known ephemeral IDs before hashing semantic output.
    ephemeral={'atom_id','atom_ids','decision_id','edit_id','claim_id','claim_ids','run_id'}
    def clean(x):
        if isinstance(x,dict):return {k:clean(v) for k,v in sorted(x.items()) if k not in ephemeral}
        if isinstance(x,list):return [clean(v) for v in x]
        if isinstance(x,tuple):return [clean(v) for v in x]
        return x
    raw=json.dumps(clean(obj),ensure_ascii=False,sort_keys=True,default=str,separators=(',',':'))
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()

def trim_peripheral_punct(text,start,end):
    raw=text[start:end];left=0;right=len(raw)
    while left<right and not (raw[left].isalnum() or raw[left] in "'’ʼꞌ" or unicodedata.category(raw[left]).startswith(('L','M'))):left+=1
    while right>left and not (raw[right-1].isalnum() or raw[right-1] in "'’ʼꞌ" or unicodedata.category(raw[right-1]).startswith(('L','M'))):right-=1
    return start+left,start+right,raw[left:right]

def reconstruct_verb_records(entries,senses):
    by_sense={s['Entry_ID']:s for s in senses};out=[];class_re=re.compile(r'^v(A~B|A~C|A|B|C|D)')
    for e in entries:
        if e.get('Part_Of_Speech')!='v':continue
        s=by_sense.get(e['ID'],{});code=e.get('Additional_Information','') or '';m=class_re.match(code)
        row={'entry_id':e['ID'],'headword':e.get('Headword','') or '','pdlma':e.get('PDLMA','') or '',
             'attribution_entry':e.get('Attribution','') or '','analysis_codes_raw':code,'verb_class':m.group(1) if m else '',
             'irregular':'YES' if 'irr' in code else 'NO','definition_es':s.get('alt_translation1','') or s.get('Description','') or '',
             'habitual':s.get('Habitual','') or '','potential':s.get('Potential','') or '','completive':s.get('Completive','') or '',
             'progressive':s.get('Progressive','') or '','perfect':s.get('Perfect','') or '','future':s.get('Future','') or '',
             'counterfactual':s.get('Counterfactual','') or '','andative':s.get('Andative','') or ''}
        out.append(VerbInventoryLoader.from_row(row))
    return out

def _atom_span(atom,start,end):
    return EvidenceAtom(atom_id=atom.atom_id,target_ref=atom.target_ref,target_start=start,target_end=end,
        claim_type=atom.claim_type,value=atom.value,provenance_type=atom.provenance_type,source_ids=atom.source_ids,
        rule_ids=atom.rule_ids,dialect_scope=atom.dialect_scope,epistemic_status=atom.epistemic_status,
        validation_status=atom.validation_status,evidence_strength=atom.evidence_strength,conflict_status=atom.conflict_status,
        blockers=atom.blockers,notes=atom.notes,raw_payload=atom.raw_payload,surface_claim=atom.surface_claim)

def source_alternative_atom(target_ref,group):
    return EvidenceAtom(atom_id=str(uuid.uuid4()),target_ref=target_ref,target_start=None,target_end=None,
        claim_type='SOURCE_SENTENCE_ALTERNATIVE',value={'segmental_index':group.segmental_index,
        'raw_surfaces':[a.raw_source_surface for a in group.attestations],
        'example_ids':[i for a in group.attestations for i in a.example_ids]},provenance_type='LEXICAL_RETRIEVAL',
        source_ids=('BIB054_DICTIONARIA',),dialect_scope=DIC_EVIDENCE_SCOPE,epistemic_status='RETRIEVED_ONLY',
        evidence_strength='MODERATE',raw_payload={'attestations':[asdict(a) for a in group.attestations],
        'source_coverage':DIC_SOURCE_COVERAGE},surface_claim=False)

def provisional_person_atom(target_ref,start,end,candidate):
    return EvidenceAtom(atom_id=str(uuid.uuid4()),target_ref=target_ref,target_start=start,target_end=end,
        claim_type='PERSON_SUFFIX_CANDIDATE',value={'person':candidate.person,'suffix':candidate.matched_suffix},
        provenance_type='MORPHOLOGICAL_ANALYSIS',source_ids=(candidate.source_id,),rule_ids=(candidate.rule_id,),
        dialect_scope=('UNKNOWN',),epistemic_status='PROVISIONAL',evidence_strength='WEAK',
        blockers=(candidate.blocking_condition,),raw_payload={'observed_input':candidate.observed_input},surface_claim=False)

def provisional_possession_atom(target_ref,start,end,candidate):
    return EvidenceAtom(atom_id=str(uuid.uuid4()),target_ref=target_ref,target_start=start,target_end=end,
        claim_type='POSSESSION_PREFIX_CANDIDATE',value={'prefix_candidate':candidate.prefix_candidate},
        provenance_type='DERIVATIONAL_ANALYSIS',source_ids=('BIB004_GRAMATICA_POPULAR',),dialect_scope=('UNKNOWN',),
        epistemic_status='PROVISIONAL',evidence_strength='WEAK',blockers=(candidate.blocking_condition,),
        raw_payload={'observed_surface':candidate.observed_surface},surface_claim=False)

def run(input_csv,entries_csv,senses_csv,examples_csv,out_dir):
    out_dir=Path(out_dir);out_dir.mkdir(parents=True,exist_ok=True)
    entries,senses,examples=DictionariaLoader.load(entries_csv,senses_csv,examples_csv)
    retrieval=RetrievalEngine(entries,senses,examples)
    surface_index=SurfaceAttestationIndex(entries,examples,max_example_tokens=4)
    alignment_index=DocumentaryAlignmentIndex.from_csv(out_dir/'DOCUMENTARY_ALIGNMENT_REGISTRY_v0_2_15_2.csv',4)
    pickett_index=PickettLexicalIndex.from_csv(out_dir/'PICKETT_LEXICON_BACKFILL_v0_1.csv')
    pickett_internal=PickettInternalSurfaceIndex(pickett_index,4)
    cross_registry=CrossSourceSurfaceRegistry(pickett_index,pickett_internal,surface_index)
    pp_index=PersonPossessionExactIndex.from_csv(out_dir/'PERSON_POSSESSION_EXACT_REGISTRY_v0_2_15_2.csv')
    bound=BoundInventory(entries);morph2=MorphologyIIInventory(entries)
    verb_records=reconstruct_verb_records(entries,senses);morph1=MorphologyEngine(verb_records)
    assert len(verb_records)==2385
    with Path(input_csv).open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
    assert len(rows)==107

    detailed=[];summary=[];action_counts=Counter();qualification_totals=Counter();scope_counts=Counter()
    for row in rows:
        cid=f"COR001-{int(row['ID']):03d}";original=row['Didxazá_original'];sentence_es=row['Español']
        context=ContextProfile(community='UNKNOWN',dialect_core='UNKNOWN',dialect_membership='UNKNOWN',membership_strength='UNKNOWN',transition_status='UNKNOWN',corpus_id='COR001')
        atoms=[];target_spans={};retrieval_matches=retrieval.span_matches(original);lexical_details=[]
        for m in retrieval_matches:
            st,en,inner=trim_peripheral_punct(original,m.start,m.end)
            if not inner:continue
            tref=f'{cid}:SPAN:{st}:{en}';target_spans[tref]=(st,en,inner);lexical_details.append(retrieval.lexical_evidence_for_match(m,sentence_es))
            a=atom_from_retrieval(target_ref=tref,value={'raw_span':inner,'entry_ids':m.entry_ids},source_ids=('BIB054_DICTIONARIA',),dialect_scope=DIC_EVIDENCE_SCOPE,
                raw_payload={'match_type':m.match_type,'normalized_span':m.normalized_span,'source_coverage':DIC_SOURCE_COVERAGE})
            atoms.append(_atom_span(a,st,en))

        seen=set();max_tokens=min(max(retrieval.max_headword_tokens,4),8)
        for sp in candidate_whitespace_spans(original,max_tokens=max_tokens):
            st,en,inner=trim_peripheral_punct(original,sp.start,sp.end)
            if not inner or (st,en,inner) in seen:continue
            seen.add((st,en,inner));tref=f'{cid}:SPAN:{st}:{en}';target_spans[tref]=(st,en,inner)
            for att in surface_index.lookup_exact(inner):atoms.append(surface_attestation_atom(att,target_ref=tref,start=st,end=en,observed_surface=inner))
            for al in alignment_index.lookup_exact(inner):
                atoms.append(alignment_surface_atom(al,target_ref=tref,start=st,end=en,observed_surface=inner))
                atoms.append(alignment_analysis_atom(al,target_ref=tref,start=st,end=en))
                if al.analysis_type=='FREQUENT_PHRASE':atoms.append(full_phrase_semantic_atom(al,target_ref=tref,start=st,end=en,observed_surface=inner))
            for pn in alignment_index.lookup_phrase_ngram(inner):atoms.append(phrase_ngram_surface_atom(pn,target_ref=tref,start=st,end=en,observed_surface=inner))
            for pr in pickett_index.lookup_exact(inner):
                atoms.append(pickett_surface_atom(pr,target_ref=tref,start=st,end=en,observed_surface=inner));atoms.append(pickett_lexical_atom(pr,target_ref=tref,start=st,end=en,observed_surface=inner))
            for pi in pickett_internal.lookup_exact(inner):atoms.append(pickett_internal_surface_atom(pi,target_ref=tref,start=st,end=en,observed_surface=inner))
            for ma in morph1.analyze_surface(inner):atoms.append(_atom_span(atom_from_morph_analysis(ma,target_ref=tref,dialect_scope=DIC_EVIDENCE_SCOPE),st,en))
            for pc in morph1.person_candidates(inner):atoms.append(provisional_person_atom(tref,st,en,pc))
            for ba in bound.exact_surface_analyses(inner):atoms.append(_atom_span(atom_from_bound_analysis(ba,target_ref=tref,dialect_scope=DIC_EVIDENCE_SCOPE),st,en))
            ders=morph2.analyze_derivation_surface(inner)
            for da in ders:
                atoms.append(sanitize_analysis_atom_v0153(derivation_atom_conclusion_only(da,target_ref=tref,start=st,end=en,dialect_scope=DIC_EVIDENCE_SCOPE)))
                rawp=(da.pdlma_evidence_raw or '').lower()
                if 'na-' in rawp and any(t in {'ADJ_SIMILITIVE','ADJ_DEVERBAL'} for t in da.der_types):
                    atoms.append(_atom_span(atom_for_explicit_conflict(atom_id=str(uuid.uuid4()),target_ref=tref,claim_type='NA_ANALYSIS',value='STATIVE',source_id='BIB004_GRAMATICA_POPULAR',rule_id='GP-NA',dialect_scope=('JUCHITAN',),note='Known GP/PBK analytical conflict'),st,en))
                    atoms.append(_atom_span(atom_for_explicit_conflict(atom_id=str(uuid.uuid4()),target_ref=tref,claim_type='NA_ANALYSIS',value='PARTICIPIAL_IN_MANY_CASES',source_id='BIB059_PBK2016',rule_id='PBK-DER-002',dialect_scope=('JUCHITAN',),note='Known GP/PBK analytical conflict'),st,en))
            pc2=morph2.possession_candidate(inner)
            if pc2 is not None and not any('POSSESSED_NOUN' in d.der_types for d in ders):atoms.append(provisional_possession_atom(tref,st,en,pc2))

        alternatives=retrieval.source_sentence_alternative_groups(sentence_es,original);phrase_tref=f'{cid}:UTTERANCE'
        for group in alternatives:atoms.append(source_alternative_atom(phrase_tref,group))
        adjudicated=EvidenceAdjudicatorV0152(EvidenceGraph(atoms)).adjudicate()
        for a in adjudicated:
            scope_counts[tuple(a.claim.dialect_scope)]+=1

        simulator=DecisionSimulatorV0153();span_decisions=[];accepted=[];review=[]
        for tref,(st,en,inner) in sorted(target_spans.items(),key=lambda kv:(kv[1][0],kv[1][1])):
            claims=[a for a in adjudicated if a.claim.target_ref==tref]
            if not claims:continue
            d=simulator.simulate_target(claims,target_ref=tref,scope='SPAN',observed_text=inner,requested_dialect_scope=('UNKNOWN',),target_start=st,target_end=en)
            span_decisions.append(d)
            if d.action in {'RT-A-EXACT','RT-A-ACCEPT_AT_SCOPE'}:accepted.append((st,en,tref))
            if d.action=='RT-D-REVIEW':review.append((st,en,tref))

        tokens=[]
        for m in re.finditer(r'\S+',original):
            st,en,inner=trim_peripheral_punct(original,m.start(),m.end())
            if inner:tokens.append((st,en,inner))
        byid={a.claim.claim_id:a for a in adjudicated};vectors=[];orth_unresolved=[];analysis_open=[];qualifications=[]
        surface_reclassified_from_prior_unresolved=0
        for st,en,text in tokens:
            cids=tuple(a.claim.claim_id for a in adjudicated if a.claim.target_start is not None and a.claim.target_start<=st and en<=a.claim.target_end)
            covered_by_accepted=any(a<=st and en<=b for a,b,_ in accepted)
            covered_by_review=any(a<=st and en<=b for a,b,_ in review)
            if covered_by_review:prior_reasons=('REVIEW_REQUIRED',)
            elif cids:prior_reasons=('EVIDENCE_PRESENT_BUT_NOT_ACCEPTED',)
            else:prior_reasons=('NO_RETRIEVED_OR_ANALYTICAL_SUPPORT',)
            claims=[byid[cid_] for cid_ in cids if cid_ in byid]
            rv=resolve_claims_v0153(claims,target_ref=f'{cid}:TOKEN:{st}:{en}',requested_dialect_scope=('UNKNOWN',))
            rvd={'target_ref':rv.target_ref,'start_original':st,'end_original':en,'text':text,
                 'surface_status':rv.surface_status,'morphology_status':rv.morphology_status,'bound_status':rv.bound_status,
                 'semantic_status':rv.semantic_status,'dialect_status':rv.dialect_status,'intervention_status':rv.intervention_status,
                 'orthographic_unresolved':rv.orthographic_unresolved,'analysis_open':rv.analysis_open,'review_required':rv.review_required,
                 'supporting_claim_ids':list(rv.supporting_claim_ids),'open_claim_ids':list(rv.open_claim_ids),'reason_codes':list(rv.reason_codes),
                 'prior_unresolved_reason_codes':list(prior_reasons),'covered_by_accepted_span':covered_by_accepted}
            vectors.append(rvd)
            if rv.orthographic_unresolved:
                orth_unresolved.append({'target_ref':phrase_tref,'start_original':st,'end_original':en,'text':text,
                    'reason_codes':list(prior_reasons),'claim_ids':list(cids),'resolution_vector':rvd})
            elif not covered_by_accepted:
                surface_reclassified_from_prior_unresolved+=1
            if rv.analysis_open:analysis_open.append({'start_original':st,'end_original':en,'text':text,'resolution_vector':rvd})
            bundle=qualify_bundle_v0153(claims)
            qs=[asdict(q) for q in bundle['qualifications']]
            if bundle['analysis_positive']:cat='ANALYSIS_POSITIVE'
            elif bundle['retrieval_only']:cat='RETRIEVAL_ONLY'
            elif bundle['hypothesis_only']:cat='HYPOTHESIS_ONLY'
            else:cat='NONE'
            if rv.orthographic_unresolved:qualification_totals[cat]+=1
            pp_quals=[]
            for a in claims:
                if a.claim.claim_type in {'PERSON_SUFFIX_CANDIDATE','POSSESSION_PREFIX_CANDIDATE'}:
                    pp_quals.append({'claim_type':a.claim.claim_type,'qualification':qualify_candidate(a.claim,pp_index,text)})
            qualifications.append({'start_original':st,'end_original':en,'text':text,'category':cat,
                'surface_positive':bundle['surface_positive'],'analysis_positive':bundle['analysis_positive'],'retrieval_only':bundle['retrieval_only'],
                'hypothesis_only':bundle['hypothesis_only'],'claim_qualifications':qs,'person_possession_gate':pp_quals})

        accepted_final=len(accepted)+surface_reclassified_from_prior_unresolved
        has_review=any(v['review_required'] for v in vectors) or bool(review)
        if accepted_final>0 and orth_unresolved:
            phrase_action='RT-B-PARTIAL';phrase_reasons=('MIXED_SURFACE_RESOLVED_AND_ORTHOGRAPHIC_UNRESOLVED','UTTERANCE_NOT_VALIDATED')
        else:
            phrase_action='RT-E-PRESERVE';phrase_reasons=('NO_UTTERANCE_LEVEL_VALIDATION','PRESERVE_DOES_NOT_MEAN_CORRECT')
            if has_review:phrase_reasons+=('ANALYSIS_REVIEW_REMAINS_SEPARATE_FROM_SURFACE_STATUS',)
        action_counts[phrase_action]+=1

        cross_hits=[]
        for st,en,text in tokens:
            c=cross_registry.lookup_exact(text)
            if c:cross_hits.append({'start_original':st,'end_original':en,'text':text,'pickett_record_ids':list(c.pickett_record_ids),'dictionaria_refs':list(c.dictionaria_refs),'semantic_equivalence':False,'universal_scope':False})

        drow={'id':cid,'block':row['Bloque'],'spanish':sentence_es,'didxaza_original':original,'context':asdict(context),
              'retrieval':{'matches':lexical_details,'source_alternatives':[asdict(g) for g in alternatives]},
              'adjudicated_claims':[asdict(a) for a in adjudicated],'span_decisions':[asdict(d) for d in span_decisions],
              'resolution_vectors_v0_2_15_3':vectors,'orthographic_unresolved_spans':orth_unresolved,'analysis_open_spans':analysis_open,
              'evidence_qualification_v0_2_15_3':qualifications,'cross_source_exact_surface':cross_hits,
              'phrase_decision':{'action':phrase_action,'scope':'UTTERANCE','utterance_validation':False,'reason_codes':phrase_reasons,
              'simulation_only':True,'edit_execution_enabled':False,'user_visible_suggestions_enabled':False},
              'source_coverage_metadata':{'BIB054_DICTIONARIA':list(DIC_SOURCE_COVERAGE)},'dialect_scope_policy':'INDIVIDUAL_EVIDENCE_UNKNOWN_UNLESS_EXPLICIT_MAPPING','warnings':['COMMUNITY_UNKNOWN_NO_DIALECT_FALLBACK','DICTIONARIA_SOURCE_COVERAGE_NOT_USED_AS_DIALECT_SCOPE']}
        detailed.append(drow)
        summary.append({'ID':row['ID'],'Bloque':row['Bloque'],'Español':sentence_es,'Didxazá_original':original,'phrase_action':phrase_action,
                        'accepted_exact_spans':accepted_final,'orthographic_unresolved_tokens':len(orth_unresolved),'analysis_open_tokens':len(analysis_open),
                        'analysis_review_tokens':sum(1 for x in analysis_open if x['resolution_vector']['review_required']),
                        'candidate_edits':sum(len(d.candidate_edits) for d in span_decisions),'utterance_validation':False})

    assert len(summary)==107
    assert sum(int(x['candidate_edits']) for x in summary)==0
    assert not any(x['utterance_validation'] for x in summary)
    detail_path=out_dir/'COR001_REPLAY_DETAILED_v0_2_15_3.jsonl'
    with detail_path.open('w',encoding='utf-8') as f:
        for d in detailed:f.write(json.dumps(d,ensure_ascii=False,default=str)+'\n')
    summary_path=out_dir/'COR001_REPLAY_SUMMARY_v0_2_15_3.csv'
    with summary_path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(summary[0]));w.writeheader();w.writerows(summary)

    metrics={'runtime_version':RUNTIME_VERSION,'rows':107,'actions':dict(action_counts),
             'orthographic_unresolved_total':sum(x['orthographic_unresolved_tokens'] for x in summary),
             'analysis_open_total':sum(x['analysis_open_tokens'] for x in summary),
             'analysis_review_total':sum(x['analysis_review_tokens'] for x in summary),
             'analysis_vector_scope':'ALL_TOKENS_NOT_ONLY_ORTHOGRAPHIC_UNRESOLVED',
             'accepted_exact_spans_total':sum(x['accepted_exact_spans'] for x in summary),
             'qualification_totals':dict(qualification_totals),'candidate_edits_total':0,'utterance_validations_total':0,
             'dictionaria_named_scope_claims':sum(v for k,v in scope_counts.items() if k==DIC_SOURCE_COVERAGE),
             'claim_scope_counts':{'|'.join(k):v for k,v in scope_counts.items()},'verb_records_reconstructed':len(verb_records),
             'surface_index_headwords':surface_index.headword_count,'surface_index_examples':surface_index.example_count,
             'surface_index_example_ngrams':surface_index.example_ngram_count,'pickett_records':len(pickett_index.records),
             'pickett_internal_ngram_occurrences':pickett_internal.ngram_count,'cross_source_exact_unique_keys':len(cross_registry.by_key),
             'auto_correct_enabled':False,'visible_suggestions_enabled':False,'edit_execution_enabled':False}
    (out_dir/'COR001_REPLAY_METRICS_v0_2_15_3.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2,sort_keys=True),encoding='utf-8')

    manifest={'run_id':str(uuid.uuid4()),'runtime_version':RUNTIME_VERSION,'input_policy':'COR001_ORIGINAL_COLUMNS_ONLY',
              'excluded_inputs':['historical_candidates','manual_deltas','retrospective_classifications','exception_lists'],
              'source_scope_policy':'DICTIONARIA_SOURCE_COVERAGE_SEPARATE; HISTORICAL_SCOPE_ALIAS_CANONICALIZED_FOR_COMMUNITY_COMPATIBILITY',
              'checksums':{'cor001_input':sha256(input_csv),'dictionaria_entries':sha256(entries_csv),'dictionaria_senses':sha256(senses_csv),
                           'dictionaria_examples':sha256(examples_csv),'pickett_backfill':sha256(out_dir/'PICKETT_LEXICON_BACKFILL_v0_1.csv'),
                           'documentary_alignment_registry':sha256(out_dir/'DOCUMENTARY_ALIGNMENT_REGISTRY_v0_2_15_2.csv'),
                           'person_possession_registry':sha256(out_dir/'PERSON_POSSESSION_EXACT_REGISTRY_v0_2_15_2.csv'),
                           'db_predecessor':sha256(out_dir/'BASE_CORRECTOR_DIDXAZA_EVIDENCE_INTEGRITY_v2_19.sqlite'),
                           'repair_runtime_v0152':sha256(out_dir/'didxaza_runtime_v0_2_15_2_evidence_integrity.py'),
                           'surface_semantics_runtime_v0153':sha256(out_dir/'didxaza_runtime_v0_2_15_3_surface_semantics_resolution_integrity.py')},
              'environment':{'python':sys.version,'platform':platform.platform()},'semantic_hashes':{'details':semantic_sha(detailed),'summary':semantic_sha(summary),'metrics':semantic_sha(metrics)},
              'hard_flags':{'auto_correct':False,'visible_suggestions':False,'edit_execution':False}}
    (out_dir/'RUN_MANIFEST_COR001_v0_2_15_3.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2,sort_keys=True),encoding='utf-8')
    return metrics

if __name__=='__main__':
    here=Path(__file__).parent
    m=run(here/'COR001_REPLAY_INPUT_v0_2_15_2.csv',here/'DICTIONARIA_entries_v0_2_15_2.csv',here/'DICTIONARIA_senses_v0_2_15_2.csv',here/'DICTIONARIA_examples_v0_2_15_2.csv',here)
    print(json.dumps(m,ensure_ascii=False,indent=2,sort_keys=True))
