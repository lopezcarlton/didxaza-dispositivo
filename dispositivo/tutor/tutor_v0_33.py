#!/usr/bin/env python3
from __future__ import annotations
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

HERE=Path(__file__).resolve().parent
BINDINGS=HERE/'TutorCaseLicenseBindings_v0_33.jsonl'
LICENSE_FILES=(
    HERE/'GenerationLicense_v0_33_c02_default_qui.jsonl',
    HERE/'GenerationLicense_C03_v0_12.jsonl',
    HERE/'GenerationLicense_C05_v0_11.jsonl',
    HERE/'GenerationLicense_C05_Inherent_v0_14.jsonl',
    HERE/'GenerationLicense_C05_XHX_v0_15.jsonl',
    HERE/'GenerationLicense_C05_Morphophonology_v0_16.jsonl',
    HERE/'GenerationLicense_C05_Morphophonology_v0_17.jsonl',
    HERE/'GenerationLicense_C05_Morphophonology_v0_18.jsonl',
    HERE/'GenerationLicense_C05_Morphophonology_v0_19.jsonl',
)

CONSTRUCTION_LABELS={
 'C01':'afirmación verbal simple',
 'C02':'negación verbal básica',
 'C03':'pregunta polar de información',
 'C05':'posesión básica',
}
PERSON_LABELS={'1SG':'primera persona singular','2SG':'segunda persona singular','3SG_HUMAN':'tercera persona singular humana'}
TAM_LABELS={'HABITUAL':'habitual','COMPLETIVE':'completivo'}
STRATEGY_LABELS={'XTI_LINKER':'posesión con xti\' / realización posesiva documentada','INHERENTLY_POSSESSED':'sustantivo inherentemente poseído','XH_X_PREFIX':'posesión con xh-/x- o superficie posesiva correspondiente'}

@dataclass(frozen=True)
class TutorOutput:
    status:str
    reason:str
    surface:str
    construction_id:str|None=None
    construction_label_es:str|None=None
    explanation_es:str|None=None
    analysis_points:tuple[str,...]=()
    license_id:str|None=None
    evidence_refs:tuple[str,...]=()
    trace_ids:tuple[str,...]=()
    tutor_contract_version:str='0.1'
    semantics:str='RENDER_ANALYSIS_AND_LICENSE_EVIDENCE_ONLY_NON_LICENSING'
    generation_license_assertion:bool=False

class TutorV0:
    """Minimal NC001 tutor renderer.

    It consumes an already-produced structural analysis and an exact current
    generation-license binding. It does not analyze, normalize, correct or
    generate surfaces. It never upgrades ANALYZED to licensed status.
    """
    def __init__(self, bindings_path:Path=BINDINGS, license_files=LICENSE_FILES):
        self.bindings={}
        for line in Path(bindings_path).read_text(encoding='utf8').splitlines():
            if line.strip():
                row=json.loads(line); self.bindings[row['surface']]=row
        self.licenses={}
        for p in license_files:
            if not Path(p).exists(): continue
            for line in Path(p).read_text(encoding='utf8').splitlines():
                if line.strip():
                    row=json.loads(line); self.licenses[row['license_id']]=row
        missing={b['license_id'] for b in self.bindings.values()}-set(self.licenses)
        if missing: raise ValueError('TUTOR_BINDING_LICENSE_MISSING:'+','.join(sorted(missing)))

    def render(self, analysis:dict[str,Any])->dict[str,Any]:
        surface=str(analysis.get('surface') or '')
        if analysis.get('analysis_status')!='ANALYZED':
            return asdict(TutorOutput('ABSTAIN','ANALYSIS_NOT_AVAILABLE',surface))
        if analysis.get('generation_license_assertion') is not False:
            return asdict(TutorOutput('ABSTAIN','ANALYZER_MUST_BE_NON_LICENSING',surface))
        if analysis.get('target_scope')!='JUCHITAN':
            return asdict(TutorOutput('ABSTAIN','TARGET_SCOPE_NOT_JUCHITAN',surface))
        binding=self.bindings.get(surface)
        if not binding:
            return asdict(TutorOutput('ABSTAIN','NO_EXACT_TUTOR_LICENSE_BINDING',surface))
        cid=analysis.get('construction_id')
        if cid!=binding['construction_id']:
            return asdict(TutorOutput('ABSTAIN','CONSTRUCTION_BINDING_MISMATCH',surface))
        lic=self.licenses[binding['license_id']]
        if lic.get('construction_id')!=cid or lic.get('novelty')!='LICENSED_NOVEL_RECOMBINATION':
            return asdict(TutorOutput('ABSTAIN','LICENSE_NOT_ACTIVE_NOVEL_BINDING',surface))
        if lic.get('target_scope')!='JUCHITAN' or lic.get('whole_surface_evidence_id') is not None:
            return asdict(TutorOutput('ABSTAIN','LICENSE_PROVENANCE_CONTRACT_MISMATCH',surface))
        refs=tuple(lic.get('source_refs') or ())
        if not refs:
            return asdict(TutorOutput('ABSTAIN','MISSING_TUTOR_EVIDENCE_REFS',surface))
        points=[]
        label=CONSTRUCTION_LABELS.get(cid,cid)
        if cid in {'C01','C02','C03'}:
            tam=analysis.get('tam'); person=analysis.get('person')
            if tam: points.append(f"El predicado está en {TAM_LABELS.get(tam,tam)}.")
            if person: points.append(f"La persona gramatical es {PERSON_LABELS.get(person,person)}.")
            slots=analysis.get('recognized_slots') or {}
            if cid=='C01' and slots.get('TEMPORAL_CONTEXT')=='ALREADY':
                points.append("Ma' aporta el contexto temporal equivalente a ‘ya’ en esta construcción licenciada.")
            if cid=='C02' and slots.get('NEG_PATTERN'):
                points.append("quí realiza el patrón negativo habitual autorizado para C02 dentro de NC001; qué se conserva como variante documentada secundaria.")
            if cid=='C03':
                points.append("La partícula final lá marca aquí una pregunta de información con respuesta sí/no.")
        elif cid=='C05':
            strategy=analysis.get('strategy')
            points.append(f"La estrategia posesiva es {STRATEGY_LABELS.get(strategy,strategy)}.")
            slots=analysis.get('recognized_slots') or {}
            if slots.get('BASE_NOUN') and slots.get('POSSESSED_STEM'):
                points.append(f"La base documentada {slots['BASE_NOUN']} aparece en esta licencia como la superficie poseída {slots['POSSESSED_STEM']}.")
            elif slots.get('POSSESSED_NOUN'):
                points.append(f"El elemento poseído es {slots['POSSESSED_NOUN']}.")
            if slots.get('POSSESSOR'):
                points.append(f"El poseedor es {slots['POSSESSOR']}.")
            if analysis.get('transform_license_id'):
                points.append(f"La alternancia morfofonológica está limitada por la licencia exacta {analysis['transform_license_id']}; no es una regla libre para otros sustantivos.")
        else:
            return asdict(TutorOutput('ABSTAIN','CONSTRUCTION_NOT_TUTOR_MATERIALIZED',surface))
        points.append("El análisis reconoce la estructura, pero no licencia por sí solo la generación; la licencia se verifica por separado.")
        trace=[]
        for k in ('construction_evidence_ids','paradigm_cell_evidence_ids','slot_filler_evidence_ids','runtime_record_ids'):
            v=analysis.get(k) or ()
            trace.extend(str(x) for x in v)
        if analysis.get('orthographic_resolution_id'): trace.append(str(analysis['orthographic_resolution_id']))
        if analysis.get('transform_license_id'): trace.append(str(analysis['transform_license_id']))
        explanation=f"«{surface}» se analiza dentro de NC001 como {label}. " + ' '.join(points[:-1])
        return asdict(TutorOutput('EXPLAINED','TRACEABLE_LICENSED_ANALYSIS_RENDERED',surface,cid,label,explanation,tuple(points),lic['license_id'],refs,tuple(dict.fromkeys(trace))))
