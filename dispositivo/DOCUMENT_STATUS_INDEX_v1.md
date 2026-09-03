# DOCUMENT_STATUS_INDEX_v1 — índice técnico de estado documental

**Estado del índice:** `ACTIVE_TECHNICAL_METADATA / NON_CANONICAL / NON_KNOWLEDGE_AUTHORITY`  
**Fecha:** 2026-09-03

## Propósito

Este índice resuelve una ambigüedad documental detectada durante la auditoría técnica sin reescribir artefactos heredados sólo para uniformar encabezados.

El índice distingue entre:

```text
EXPLICIT_STATUS = el propio artefacto declara Estado/Status
EXPLICIT_RESULT_ONLY = el artefacto declara un resultado, no un estado de ciclo de vida
STATUS_NOT_DECLARED = el artefacto no declara estado; no inferir ACTIVE, DEPRECATED, SEALED u otro
INDEX_CLASSIFICATION != KNOWLEDGE_AUTHORITY
```

La ausencia de un encabezado `Estado` o `Status` no autoriza a inventar uno retroactivamente.

## Documentos verificados en P2-06

| Documento | Declaración propia observada | Tratamiento del índice |
|---|---|---|
| `core/NUCLEO_CONVERSACIONAL_001_SCOPE_v1.md` | `## Estado`; `SCOPE_STATUS = FROZEN_FOR_MATERIAL_SELECTION`; `HOLDOUT_CONTENT = NOT_ACQUIRED_OR_EXPOSED`; `COR001_ROLE = ANALYSIS_TARGET_ONLY` | `EXPLICIT_STATUS` |
| `development_corpus/DEV_CORPUS_AUDIO_FIRST_PROTOCOL_v1.md` | `## Status`; `READY_FOR_EXTERNAL_ACQUISITION` | `EXPLICIT_STATUS` |
| `development_corpus/HOLDOUT_CONVERSATIONAL_001_PROTOCOL_v1.md` | `## Estado`; `PROTOCOL_STATUS = SEALED`; `HOLDOUT_CONTENT_STATUS = NOT_YET_ACQUIRED_OR_SEALED` | `EXPLICIT_STATUS` |
| `development_corpus/DevelopmentCorpusProtocol_v0_35.md` | no declara encabezado ni campo explícito de estado al inicio; declara que v0.35 extiende v0.22 aditivamente | `STATUS_NOT_DECLARED / DO_NOT_INFER` |
| `development_corpus/HOLDOUT_GENERALIZATION_REQUIREMENTS_v0_1.md` | no declara encabezado ni campo explícito de estado | `STATUS_NOT_DECLARED / DO_NOT_INFER` |
| `hardening/ANALYSIS_CAPABILITY_GUARDRAILS_v0_35.md` | no declara encabezado ni campo explícito de estado | `STATUS_NOT_DECLARED / DO_NOT_INFER` |
| `analyzer/reports/COR001_ANALYSIS_TARGET_PASS_REPORT_v0_24.md` | `## Result`; `PASS / ANALYSIS_TARGET_OBSERVATION_COMPLETED`; declara además que no es una evaluación de exactitud | `EXPLICIT_RESULT_ONLY / STATUS_NOT_DECLARED` |

## Regla de lectura

Para los documentos marcados `STATUS_NOT_DECLARED`, este índice no decide si deben estar activos, archivados, superados o adoptados. Esa decisión requiere evidencia adicional o una decisión técnica explícita posterior.

Para el reporte COR001, `PASS` describe la finalización de una observación del objeto de análisis. No convierte COR001 en benchmark, gold standard, regresión ni fuente de descubrimiento de reglas.

## Alcance

Este v1 cubre únicamente el conjunto documental verificado durante P2-06. No afirma ser un inventario exhaustivo de todos los documentos del repositorio. Puede ampliarse aditivamente cuando aparezcan nuevos casos de ambigüedad documental.
