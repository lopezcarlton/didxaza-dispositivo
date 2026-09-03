# MIGRATION_MANIFEST_v1 — Dispositivo lingüístico

**Proyecto:** Voces de las Nubes  
**Fecha de inicio:** 2026-08-31  
**Última actualización:** 2026-09-02 — consolidada la migración histórica y verificada la reproducibilidad técnica aislada del replay v0.2.15.3; COR001 permanece `ANALYSIS_TARGET_ONLY`.

**Estado:** `ACTIVE_INVENTORY / HISTORICAL_CHAT_MIGRATION_SUFFICIENT / REENTRY_READY / NO_BLOCKING`  
**Alcance:** recuperación selectiva del estado técnico y documental del dispositivo

## 1. Principio

La migración preserva conocimiento, procedencia y capacidad reproducible. **No congela la investigación ni convierte la arquitectura recuperada en arquitectura definitiva.**

Se rige por `conocimiento/principios/PRIN-INVESTIGACION-ABIERTA.md` y por `dispositivo/migracion/MIGRATION_AGENT_PROTOCOL_v1.md`.

```text
MIGRATED_ARTIFACT != IMMUTABLE_RULE
IMPLEMENTED_CAPABILITY != RESEARCH_AUTHORITY
MIGRATION_STATUS != PEDAGOGICAL_PRIORITY
MIGRATION_INCOMPLETE != RESEARCH_BLOCKED
CHAT != MIGRATION_ARTIFACT
```

COR001, COR002, corpus oral, trabajo con hablantes, investigación pedagógica, lectura bibliográfica y nuevas hipótesis pueden continuar durante la migración salvo dependencia técnica concreta.

COR001 mantiene exclusivamente:

```text
COR001 = ANALYSIS_TARGET_ONLY
COR001 != GOLD_STANDARD
COR001 != BENCHMARK
COR001 != REGRESSION_AUTHORITY
COR001 != RULE_DISCOVERY_SOURCE
```

## 2. Estados

- `MIGRATED`: ya existe en el repositorio.
- `RECOVERABLE_SOURCE_LOCATED`: fuente externa concreta localizada.
- `REFERENCED_BY_LOCATED_ARTIFACT`: existencia documentada, archivo aún no recuperado.
- `EXTERNAL_KNOWN_NOT_MIGRATED`: estado conocido, fuente exacta aún no localizada.
- `NOT_LOCATED_IN_CURRENT_PASS`: no apareció en esta búsqueda; no equivale a perdido.
- `SUPERSEDED`: antecedente que no representa el estado vigente.
- `ARCHIVE_ONLY`: trazabilidad histórica, no pieza activa.
- `SOURCE_COMPLETE_READY_TO_MIGRATE`: fuente completa disponible y lista para copia exacta.
- `SOURCE_PARTIAL_DO_NOT_MIGRATE`: sólo existe contenido parcial o truncado.
- `BINARY_TRANSFER_PENDING`: artefacto identificado cuya transferencia íntegra no es posible todavía con la herramienta disponible.
- `FAILED_INCOMPLETE_TRANSFER`: intento de transporte incompleto o no verificable.

Ningún estado concede autoridad lingüística o pedagógica.

## 3. Migrado

| Artefacto | Función / estado recuperado |
|---|---|
| `INICIAR_AQUI_CHAT_NUEVO.md` | entrypoint único de reentrada desde GitHub; navegación, no autoridad lingüística |
| `dispositivo/README.md` | arquitectura y frontera del dispositivo |
| `dispositivo/ESTADO_ACTUAL_2026-08-31.md` | snapshot técnico previo a la migración |
| `dispositivo/ANALYZER_SCOPE_MULTIESCALA_2026-08-31.md` | alcance palabra → discurso |
| `dispositivo/PROVENANCE_LABEL_CROSSWALK_v0_1.md` | equivalencias de procedencia |
| `dispositivo/migracion/MIGRATION_AGENT_PROTOCOL_v1.md` | protocolo de migración directa |
| `dispositivo/migracion/CURRENT_EXECUTABLE_STATE_v1.md` | checkpoint de presencia/ejecutabilidad/reproducibilidad |
| `dispositivo/migracion/REENTRY_CHECKPOINT_2026-09-02.md` | cierre de reentrada; `NON_CANONICAL` |
| `dispositivo/migracion/ISOLATED_REPLAY_VERIFICATION_v0_2_15_3_2026-09-02.md` | evidencia del replay aislado; `TECHNICAL_REPRODUCIBILITY_PASS / NON_LINGUISTIC_AUTHORITY` |
| `dispositivo/migracion/test_migrated_state.py` | verificaciones del estado migrado |
| `dispositivo/pedagogia/PEDAGOGICAL_DISCUSSION_FREEZE_POST_BIB065_v0_36_2.md` | discusión pedagógica no normativa |
| `dispositivo/hardening/ANALYSIS_CAPABILITY_GUARDRAILS_v0_35.md` | `MIGRATED / EXACT_TEXT_IDENTITY_VERIFIED / P1`; frase aislada y contexto opcional protegidos |
| `dispositivo/development_corpus/DevelopmentCorpusProtocol_v0_35.md` | `MIGRATED / EXACT_TEXT_IDENTITY_VERIFIED / P1`; adquisición no destructiva y provenance de método |
| `dispositivo/development_corpus/HOLDOUT_CONVERSATIONAL_001_PROTOCOL_v1.md` | protocolo sellado previo a adquisición; COR001 separado como `ANALYSIS_TARGET_ONLY` |
| `dispositivo/development_corpus/DEV_CORPUS_AUDIO_FIRST_PROTOCOL_v1.md` | protocolo P1 audio-first y separación estricta del holdout |
| `dispositivo/development_corpus/HOLDOUT_GENERALIZATION_REQUIREMENTS_v0_1.md` | requisitos mínimos P1 para evaluación fresca de generalización |
| `dispositivo/core/NUCLEO_CONVERSACIONAL_001_SCOPE_v1.md` | scope exacto del vertical slice NC001 |
| `dispositivo/core/JUCHITAN_LINGUISTIC_CORE_v0_27.md` | fuente completa; `EXPERIMENTAL_CORE`, baseline verificable actual |
| `dispositivo/migracion/fuentes/CURRENT_STATE_NC001_v1.md` | checkpoint pre-Generator; `ARCHIVE_ONLY` |
| `dispositivo/migracion/fuentes/CURRENT_STATE_NC001_v2_POST_GENERATOR_V0.md` | estado post Generator_v0 |
| `dispositivo/migracion/fuentes/CURRENT_STATE_NC001_v3_POST_ROUNDTRIP_BRIDGE.md` | bridge round-trip; `ARCHIVE_ONLY` |
| `dispositivo/migracion/fuentes/CURRENT_STATE_NC001_v4_POST_ROUNDTRIP_STABILIZATION.md` | estabilización round-trip v0.2; `ARCHIVE_ONLY` |
| `dispositivo/migracion/fuentes/CURRENT_STATE_NC001_v34_POST_C02_DEFAULT_QUI_MIGRATION.md` | transición C02 a `quí`; `qué` variante secundaria |
| `dispositivo/migracion/fuentes/CURRENT_STATE_NC001_v35_POST_EVIDENCE_GAP_PRIORITIZER.md` | priorizador de huecos; COR001 analysis-only |
| `dispositivo/migracion/fuentes/CURRENT_STATE_NC001_v36_POST_KNOWLEDGE_INGESTION_GUARDRAILS.md` | guardrails y ruta literatura+audio |
| `dispositivo/migracion/fuentes/CURRENT_STATE_NC001_v37_1_POST_BIB065_REPAIR.md` | ruta activa más reciente localizada; rutas reparadas al layout de GitHub |
| `dispositivo/migracion/fuentes/ROUNDTRIP_CONTRACT_v0_2.md` | contrato histórico `STRUCTURAL_COMPATIBILITY_ONLY_NON_LICENSING` |
| `dispositivo/migracion/fuentes/SINTESIS_ADVERSARIAL_ARQUITECTURA_DIDXAZA_v1_1_CORREGIDA.md` | adjudicación arquitectónica histórica; `ARCHIVE_ONLY` |
| `dispositivo/migracion/fuentes/BENCHMARK_ISOLATION_PROTOCOL_v1.md` | `ARCHIVE_ONLY / SUPERSEDED_BY_CURRENT_COR001_POLICY` |
| `dispositivo/migracion/fuentes/MVP_REUSE_MAP_v1.md` | mapa de reutilización/cuarentena del vertical slice |
| `dispositivo/migracion/fuentes/mvp_vertical_slice_v0_2/` | payloads textuales exactos; `ARCHIVE_ONLY / NON_AUTHORITY` |
| `dispositivo/migracion/fuentes/mvp_audio_review_v0_1/` | payloads textuales exactos; `ARCHIVE_ONLY / NON_AUTHORITY` |
| `dispositivo/migracion/fuentes/generator_v0_initial/` | scaffold histórico Generator_v0; `ARCHIVE_ONLY / SUPERSEDED` |
| `dispositivo/migracion/fuentes/BIB065_BUENO_HOLLE_INGESTION_MATRIX_v0_36_1.md` | matriz bibliográfica reparada; P1 no normativa |
| `dispositivo/migracion/fuentes/BIB065_BUENO_HOLLE_INGESTION_MATRIX_v0_36_1.csv` | `MIGRATED / EXACT_BYTE_IDENTITY_VERIFIED / P1`; SHA-256 `acffea79fe7d228a0b28f740094e5a15fd4ec0ba6d36b257cc3aaef918a83c54` |
| `dispositivo/migracion/fuentes/BH2019_READING_STATE_CLOSED_v0_36_1.md` | `MIGRATED / EXACT_TEXT_IDENTITY_VERIFIED / P1`; lectura intensiva cerrada |
| `dispositivo/migracion/fuentes/BH2019_SOURCE_PROVENANCE_v0_36_1.json` | `MIGRATED / EXACT_TEXT_IDENTITY_VERIFIED / P1` |
| `dispositivo/migracion/fuentes/PEDAGOGICAL_BACKLOG_BH2019_PARTIAL_v0_35.md` | `MIGRATED / ARCHIVE_ONLY / SUPERSEDED_FOR_CURRENT_PLANNING` |
| `dispositivo/generator/inputs/ConstructionInventory_v1.jsonl` | seis construcciones NC001 |
| `dispositivo/generator/inputs/ParadigmTable_v1.csv` | 72 celdas TAM/persona con procedencia |
| `dispositivo/validation/ValidationQueue_v0.jsonl` | cola de validación/desarrollo audio-first |
| `dispositivo/analyzer/non_licensing_analyzer_orchestrator_v0_35.py` | Analyzer parcial no licenciante |
| `dispositivo/analyzer/analyzer_v0_35_migrated_adapter.py` | adaptador reproducible del Analyzer v0.35 |
| `dispositivo/analyzer/DIC_VERB_2385_v0_1.csv` | inventario exacto de 2,385 verbos |
| `dispositivo/analyzer/reports/COR001_ANALYSIS_TARGET_PASS_REPORT_v0_24.md` | reporte histórico; `ANALYSIS_TARGET_ONLY / NON_AUTHORITY` |
| `dispositivo/runtime/v0_2_15_3/BASE_CORRECTOR_DIDXAZA_SURFACE_SEMANTICS_v2_20.sqlite` | SQLite v2.20 exacta, integridad verificada |
| `dispositivo/runtime/v0_2_15_3/DICTIONARIA_entries_v0_2_15_2.csv` | 9,012 entradas exactas |
| `dispositivo/runtime/v0_2_15_3/DICTIONARIA_senses_v0_2_15_2.csv` | 9,046 sentidos exactos |
| `dispositivo/runtime/v0_2_15_3/DICTIONARIA_examples_v0_2_15_2.csv` | 9,686 ejemplos exactos |
| `dispositivo/runtime/v0_2_15_3/run_cor001_replay_v0_2_15_3.py` | runner exacto del replay histórico; sólo reproducibilidad técnica |
| `dispositivo/runtime/v0_2_15_3/CLEAN_REPLAY_VERIFICATION_v0_2_15_3.json` | verificación limpia histórica exacta; SHA-256 `0446768fa8ec1d6e76937688c62e8aa667e7503d211070988944c44253b36644`; referencia de hashes semánticos y 38/38 pruebas |
| `dispositivo/runtime/v0_2_15_3/didxaza_runtime_v0_2_10_documentary_alignment.py` | dependencia exacta del replay |
| `dispositivo/runtime/v0_2_15_3/DOCUMENTARY_ALIGNMENT_REGISTRY_v0_2_15_2.csv` | registry exacto |
| `dispositivo/runtime/v0_2_15_3/didxaza_runtime_v0_2_11_pickett_backfill.py` | dependencia exacta del replay |
| `dispositivo/runtime/v0_2_15_3/didxaza_runtime_v0_2_12_pickett_cross_source.py` | dependencia exacta del replay |
| `dispositivo/runtime/v0_2_15_3/didxaza_runtime_v0_2_14_person_possession.py` | dependencia exacta del replay |
| `dispositivo/runtime/v0_2_15_3/COR001_REPLAY_INPUT_v0_2_15_2.csv` | input histórico exacto; `ANALYSIS_TARGET_ONLY` |
| `dispositivo/runtime/v0_2_15_3/PERSON_POSSESSION_EXACT_REGISTRY_v0_2_15_2.csv` | registry exacto GP persona/posesión |
| `dispositivo/runtime/v0_2_15_3/PICKETT_LEXICON_BACKFILL_v0_1.csv` | 2,534 registros; identidad byte a byte verificada |
| `dispositivo/generator/generator_v0_5.py` | implementación Generator más reciente localizada |
| `dispositivo/generator/generator_v0_5_migrated_adapter.py` | adaptador al layout migrado |
| `dispositivo/generator/GENERATION_READINESS_MATRIX_v14.csv` | snapshot readiness más reciente localizado |
| `dispositivo/tutor/tutor_v0_33.py` | Tutor renderer conservador; dependencias incompletas |
| `dispositivo/generator/inputs/GenerationLicense_v0_33_c02_default_qui.jsonl` | licencias activas v0.33 |
| `dispositivo/generator/inputs/GenerationEvidenceAtoms_v0_33_c02_default_qui.jsonl` | átomos de evidencia v0.33 |
| `dispositivo/generator/inputs/AuthorizedSlotFillers_v0_33.jsonl` | fillers autorizados por slot |
| `dispositivo/generator/inputs/IntegrationBlockers_v0_1.jsonl` | bloqueadores C03–C06 |
| `dispositivo/generator/inputs/OrthographicResolutions_v0_9.jsonl` | resoluciones ortográficas por celda |
| `dispositivo/generator/inputs/AdoptionRecords_v1.jsonl` | guardas/adopciones NC001 |
| `dispositivo/generator/inputs/ConceptMapping_v1.jsonl` | HABITUAL/COMPLETIVE, sin proyección automática a superficie |
| `dispositivo/generator/inputs/OrthographicProfile_v1_DRAFT.json` | vector ortográfico conservador, no norma global |

## 4. Runtime v0.2.15.3 — estado de recuperación

Fuente histórica:

```text
didxaza_v0_2_15_3_surface_semantics_resolution_integrity_CLOSED_PASS(1).zip
ZIP SHA256 = 6e5c3e8ee9bb5dbd04666537dc423724eb4bc402440e670e5be81cfa54b5d7e5
```

`RELEASE_FILE_MANIFEST_v0_2_15_3.json` enumera 75 payloads. En este checkpoint hay **39/75 payloads exactos recuperados** y 36 ausentes.

SQLite:

```text
BASE_CORRECTOR_DIDXAZA_SURFACE_SEMANTICS_v2_20.sqlite
SHA256 = 2379773426baf4e3eace87c61ec17f7a1e1b9164421e56cf736d35eb64a5ebed
SQLITE_INTEGRITY_CHECK = ok
FOREIGN_KEY_VIOLATIONS = 0
canonical_state_v17 = 22 rows
verb_lexeme_class_v023 = present
person_possession_exact_v0214 = present
```

El slice final de semántica de superficie y la cadena histórica de 38 pruebas permanecen reproducibles desde artefactos almacenados. El replay histórico v0.2.15.3 fue regenerado en un checkout aislado de GitHub Actions y obtuvo `TECHNICAL_REPRODUCIBILITY_PASS`: todas las dependencias directas verificadas coincidieron con el release y los outputs deterministas `SUMMARY` y `METRICS` reprodujeron exactamente sus SHA-256 históricos. Ver `ISOLATED_REPLAY_VERIFICATION_v0_2_15_3_2026-09-02.md`. Esto no concede autoridad lingüística a COR001.

La segunda pasada fortaleció esa conclusión sobre un checkout sin mutación previa: verificó la clausura recursiva de 17 módulos, 8 dependencias de datos, los tres hashes semánticos históricos, los outputs deterministas y 38/38 pruebas. El primer cierre se conserva como genealogía de la reparación de transporte; la segunda pasada es la comprobación limpia del estado final materializado.

`PICKETT_LEXICON_BACKFILL_v0_1.csv` conserva identidad exacta:

```text
SIZE = 940709 bytes
DATA_ROWS = 2534
COLUMNS = 23
SHA256 = 56e2372566cec9d7758b7e45b8de4e320a92eb2ee5c51b2a5e444e8165875723
GIT_BLOB = 98b4e87282b996e837356f41ead2f859d53face1
STATUS = MIGRATED / EXACT_BYTE_IDENTITY_VERIFIED
```

No queda ninguna dependencia directa conocida faltante para el replay histórico y la regeneración aislada ya fue ejecutada con `PASS` técnico. Durante la verificación se restauró la representación byte-exacta histórica de `PERSON_POSSESSION_EXACT_REGISTRY_v0_2_15_2.csv` (`UTF-8 BOM + CRLF + final newline`, SHA-256 `3f1e955a285c2ce9c66d3953def6b41fd993d6b8dd81567c5f95a28281d20bdb`), corrigiendo sólo una normalización de transporte. COR001 permanece `ANALYSIS_TARGET_ONLY`.

## 5. Analyzer, Generator y Tutor

### Analyzer v0.35

```text
STATUS = MIGRATED / REPRODUCIBLE_NON_LICENSING_PARTIAL_ANALYZER
```

Puede abstenerse y no concede licencia de generación, corrección, autoridad ortográfica ni descubrimiento de reglas.

### Generator v0.5

Genealogía localizada:

```text
generator_v0.py -> generator_v0_1.py -> generator_v0_2.py -> generator_v0_3.py -> generator_v0_4.py -> generator_v0_5.py
```

El adaptador migrado materializa:

```text
PARADIGM_CELLS = 72
CONSTRUCTIONS = 6
GENERATION_LICENSES = 6
ACTIVE_LICENSE_CONSTRUCTIONS = C01, C02
BLOCKED_BY_MIGRATED_INPUTS = C03, C04, C05, C06
```

`GENERATION_READINESS_MATRIX_v14.csv` permanece `MIGRATED_SNAPSHOT_NOT_REPRODUCIBLE_WITH_CURRENT_FILES` para capacidades históricas cuyas dependencias exactas faltan.

### Tutor v0.33

```text
STATUS = SOURCE_PRESENT / DEPENDENCIES_INCOMPLETE / NOT_INSTANTIABLE_YET
```

Dependencias todavía no localizadas como fuentes completas:

```text
TutorCaseLicenseBindings_v0_33.jsonl
GenerationLicense_C03_v0_12.jsonl
GenerationLicense_C05_v0_11.jsonl
GenerationLicense_C05_Inherent_v0_14.jsonl
GenerationLicense_C05_XHX_v0_15.jsonl
GenerationLicense_C05_Morphophonology_v0_16.jsonl
GenerationLicense_C05_Morphophonology_v0_17.jsonl
GenerationLicense_C05_Morphophonology_v0_18.jsonl
GenerationLicense_C05_Morphophonology_v0_19.jsonl
```

## 6. Genealogías recuperadas

### JUCHITAN_LINGUISTIC_CORE

```text
v0.1 -> ... -> v0.23 -> ... -> v0.27
                              \\-> v0.28 [QUARANTINED / NOT_CURRENT_BASELINE]
```

`v0.27` permanece la referencia verificable migrada. `JUCHITAN_LINGUISTIC_CORE_v0_28.md` fue localizado como rama posterior con:

```text
SHA256 = 6766d25f38ecd39a01a1a0e0463776e85c518325f6653603b70583562910a12a
RELATION_TO_v0_27 = v0.27 body preserved + COR001 post-grammar patch
STATUS = SOURCE_COMPLETE_READY_TO_MIGRATE / ARCHIVE_ONLY / QUARANTINED_NOT_CURRENT_BASELINE
```

No es requisito para reproducir ni continuar el estado vigente.

### NC001

```text
v1 -> v2 -> v3 -> v4 -> ... -> v34 -> v35 -> v36 -> v37.1
```

v37.1 permanece el estado más reciente localizado.

### Runtime

```text
v0.2.0 foundation
-> v0.2.1 retrieval
-> v0.2.2 context/provenance
-> v0.2.3 morphology I
-> v0.2.4 BOUND
-> v0.2.5 morphology II
-> v0.2.6 evidence adjudication
-> v0.2.7 decision simulation
-> v0.2.7.1 integration fixes
-> v0.2.9 surface evidence/coverage
-> v0.2.10 documentary alignment
-> v0.2.11 Pickett backfill
-> v0.2.12 Pickett cross-source
-> v0.2.13 resolution vectors
-> v0.2.14 person/possession
-> v0.2.15 evidence qualification
-> v0.2.15.2 evidence integrity
-> v0.2.15.3 surface semantics/resolution integrity
```

## 7. Artefactos localizados y pendientes

| Artefacto | Estado actual | SHA-256 / evidencia |
|---|---|---|
| `COR001AnalysisObservations_v0_24.jsonl` | `REFERENCED_BY_LOCATED_ARTIFACT / NOT_LOCATED_IN_CURRENT_PASS` | referenciado por reporte v0.24 migrado |
| `COR001AnalysisObservationSummary_v0_24.json` | `REFERENCED_BY_LOCATED_ARTIFACT / NOT_LOCATED_IN_CURRENT_PASS` | idem |
| `COR001AnalysisHarnessCalibration_v0_24.json` | `REFERENCED_BY_LOCATED_ARTIFACT / NOT_LOCATED_IN_CURRENT_PASS` | idem |
| `run_cor001_analysis_target_pass_v0_24.py` | `REFERENCED_BY_LOCATED_ARTIFACT / NOT_LOCATED_IN_CURRENT_PASS` | idem |
| `JUCHITAN_LINGUISTIC_CORE_v0_28.md` | `SOURCE_COMPLETE_READY_TO_MIGRATE / ARCHIVE_ONLY / QUARANTINED_NOT_CURRENT_BASELINE` | `6766d25f38ecd39a01a1a0e0463776e85c518325f6653603b70583562910a12a` |
| `verify_cor001_blind_fixture_v1.py` | `REFERENCED_BY_LOCATED_ARTIFACT / NOT_LOCATED_IN_CURRENT_PASS / HISTORICAL` | referenciado por protocolo archivado |
| `HOLDOUT_CONVERSATIONAL_001_PROTOCOL_v1.sha256` | `REFERENCED_BY_LOCATED_ARTIFACT / NOT_LOCATED_IN_CURRENT_PASS` | sidecar requerido por el protocolo; fuente exacta no localizada |
| `PAQUETE_MIGRACION_DIDXAZA_GENERATOR_V0_INTEGRATED_v1(1).zip` | `BINARY_TRANSFER_PENDING / ARCHIVE_ONLY` | `270dff08371f6b35bbb817d5440db85811ab87f11b2c7a96a9cf8f485ed76b9a` |
| `MVP_LINGUISTICO_001_VERTICAL_SLICE_v0_1.zip` | `SOURCE_COMPLETE_READY_TO_MIGRATE / BINARY_TRANSFER_PENDING / ARCHIVE_ONLY` | `f4819f...60c948` |
| `MVP_LINGUISTICO_001_VERTICAL_SLICE_v0_2.zip` | `BINARY_TRANSFER_PENDING / TEXTUAL_PAYLOADS_MIGRATED / ARCHIVE_ONLY` | `e6524d...6185e2` |
| `MVP_LINGUISTICO_001_AUDIO_REVIEW_v0_1.zip` | `BINARY_TRANSFER_PENDING / TEXTUAL_PAYLOADS_MIGRATED / ARCHIVE_ONLY` | `52b648aa2739b36cb78e5efcef0b037de8a0681c47bbc76d04bc8731b9e6272b` |

### 7.1 Paquetes completos del trabajo ortográfico/corrector localizados

| Paquete | Contenido principal | Estado | SHA-256 |
|---|---|---|---|
| `picket extracción.zip` | fase documental Pickett: validación, abreviaciones, ortografía, grafemas, morfología, automatización y cobertura COR001 | `SOURCE_COMPLETE_READY_TO_MIGRATE / BINARY_TRANSFER_PENDING / NON_CANONICAL_CORRECTOR_RESEARCH_SOURCE` | `46fb0865c96ace4ffa29742b2a78c284a85b0f52f66eb3fb2f60320c77dc8a0b` |
| `diagnóstico fuentes pickett.zip` | diagnóstico de fuentes/glifos, mapeo, validación y prototipo | `SOURCE_COMPLETE_READY_TO_MIGRATE / BINARY_TRANSFER_PENDING / EXTRACTION_REPRODUCIBILITY_SOURCE` | `dee278ca50d3ba415ee745684cb0e0ea655ec882fac4e6d19f78db9862b27bc4` |
| `cierre de fase 4.zip` | extractor final y léxico estructurado Pickett | `SOURCE_COMPLETE_READY_TO_MIGRATE / BINARY_TRANSFER_PENDING / NON_CANONICAL_CORRECTOR_RESEARCH_SOURCE` | `205bab2db28f9fbc9639fabde959b6d0c6164772d1fd026a5adc500d871320ec` |
| `fase 5.zip` | auditoría histórica de COR001 contra Pickett | `SOURCE_COMPLETE_READY_TO_MIGRATE / BINARY_TRANSFER_PENDING / COR001_ANALYSIS_TARGET_ONLY / NON_AUTHORITY` | `293b66233d3febe2f5e715356b3d859a7e5c9ed15e031ab766e3ad32545353a1` |

`cierre de fase 4.zip` documenta un léxico de investigación de 6,431 registros. **No es identidad ni sustituto** de `PICKETT_LEXICON_BACKFILL_v0_1.csv` (2,534 registros, schema y procedencia diferentes).

`fase 5.zip` sólo puede conservarse bajo `ANALYSIS_TARGET_ONLY / NON_AUTHORITY`; no puede usarse como benchmark, regresión, gold ni fuente de reglas.

## 8. Reuse map / cuarentenas

Permanecen fuera de licencias de generación:

```text
SequenceMatcher / near-match
normalización destructiva de diacríticos
clean_paradigm_surface() -> surface
COR001 como licencia
confidence legado
handlers particulares COR001
owner review / PROBABLE_TRANSCRIPTION_CORRECTION como licencia
```

Los artefactos históricos que trataban COR001 como benchmark/regression no se promueven al estado técnico activo. `COR001 = ANALYSIS_TARGET_ONLY` prevalece.

`BENCHMARK_ISOLATION_PROTOCOL_v1.md` se preserva exclusivamente en `migracion/fuentes/` y su semántica histórica queda superseded por la política vigente.

## 9. Commits de migración relevantes

```text
554ce87239d9aa7b4a7f04be1f9378ece7afde47  migrate Juchitán linguistic core v0.27
7ab707cf33461438e832454685cbd5355f75b586  migrate exact DIC_VERB inventory
505f7125321c75238e90135e91667ae5544fa870  migrate exact SQLite v2.20
f533bf667b0a7aca94426fb24016000761502e10  migrate exact Dictionaria analyzer inputs
9d631d3db742afc6affbd1fb14179eb174c578da  make migrated Analyzer v0.35 reproducible
1349a0be610d4020a698795925a8a70702a22f2d  migrate exact runtime surface semantics slice
bdd2d9857bbaa647f239748aff3cf2af1e5bc567  migrate exact runtime v0.2.15.3 replay runner
a4539d9eeab6ce197e5682afc1c0f2cd547ddcdd  migrate BIB065 ingestion matrix v0.36.1
b9612c85debe59f115c54972c1b9adc78c7988db  migrate exact Pickett lexicon backfill v0.1
b67bb0708ea47deb2f7d767a43acace79a66834d  archive historical benchmark isolation protocol v1
6053b2c8b48c6a3f1b95bb86fcdfe759c48cd291  remove superseded benchmark protocol from active hardening
a00df054d9c0e6b2150a47fbc15227eb788ecacf  migrate sealed conversational holdout protocol v1
395912cd694e04c4df345adf1b01597cba70356d  migrate audio-first development corpus protocol v1
deb1e45057a4b1a96d52c8b007bdbd0a80df435f  migrate holdout generalization requirements v0.1
750b9bafbdcdff158b47e72763c2484731e66122  migrate analysis capability guardrails v0.35
185baf3ab8a18cdd890f2454192782baa15bff4a  migrate development corpus protocol v0.35
18977e2c0f359c89c4b1af99082e91fa2850e21a  migrate BH2019 closed reading state v0.36.1
432529a099b0ce6cca58a8a5af2127ab8ff69a40  migrate BH2019 source provenance v0.36.1
b7c2655fed6bc5a24aadfd3513958bac228247c2  migrate historical BH2019 pedagogical backlog
c063fb591e5034070ad703b077bb63b174477414  migrate exact BIB065 matrix CSV v0.36.1
7b8ca1f2cfbdac163638f7a197ac169498c0b7b8  add GitHub reentry entrypoint
7f5eaf327016eb0a3904d551037fb4ba691fee19  repair BIB065 state paths for GitHub layout
153fbeb99a265ebb6521e9f3b3a234dcb5ef3b10  link reentry entrypoint from README
```

La historia completa permanece en Git; esta lista resalta cierres relevantes para el estado materializado.

## 10. Orden de recuperación restante

### P0 — reproducibilidad técnica, no bloqueo de investigación

1. recuperar `TutorCaseLicenseBindings_v0_33.jsonl` y las licencias C03/C05 exactas sólo si aparecen como fuentes completas y si siguen siendo útiles para reproducir el Tutor histórico.

El replay histórico v0.2.15.3 ya no es un pendiente: su reproducibilidad técnica aislada fue verificada el 2026-09-02. Futuras ejecuciones son manuales y no constituyen una suite de regresión COR001.

### P1 — límites y genealogía

- sidecar `HOLDOUT_CONVERSATIONAL_001_PROTOCOL_v1.sha256` si aparece como fuente exacta;
- paquetes corrector/Pickett de §7.1 cuando exista canal de transferencia binaria exacta;
- soportes v0.24 de COR001 si aparecen como fuentes completas.

### P2/P3

Sólo artefactos ejecutables útiles o historia necesaria para genealogía. `JUCHITAN_LINGUISTIC_CORE_v0_28.md` permanece `ARCHIVE_ONLY / QUARANTINED_NOT_CURRENT_BASELINE` y no es requisito para reproducir el estado actual.

## 11. Cierre de la migración histórica entre chats

Con la consolidación de este manifiesto:

- `ANALYSIS_CAPABILITY_GUARDRAILS_v0_35.md`, `DevelopmentCorpusProtocol_v0_35.md`, el cierre/provenance BIB065, la matriz CSV exacta y el backlog parcial BH2019 ya no son pendientes;
- el backlog parcial BH2019 se conserva únicamente como histórico superseded;
- `INICIAR_AQUI_CHAT_NUEVO.md` es el punto de reentrada desde GitHub;
- las rutas BIB065 del estado v37.1 apuntan al layout real del repositorio;
- no hace falta volver por defecto a chats históricos;
- el runtime sigue con 39/75 payloads exactos materializados;
- el replay end-to-end v0.2.15.3 fue regenerado aisladamente y obtuvo `TECHNICAL_REPRODUCIBILITY_PASS`; `SUMMARY` y `METRICS` coinciden byte por byte con el release;
- Tutor v0.33 sigue no instanciable por dependencias históricas faltantes;
- ninguna de estas limitaciones bloquea literatura, corpus oral, COR002, trabajo con hablantes o investigación pedagógica.

```text
HISTORICAL_CHAT_MIGRATION_SUFFICIENT = true
REENTRY_READY = true
ALL_HISTORICAL_PAYLOADS_RECOVERED = false
RUNTIME_COMPLETE = false
RESEARCH_BLOCKED = false
```

## 12. Próxima acción

No queda un replay P0 pendiente. La recuperación del Tutor v0.33 sólo debe continuar si aparecen sus dependencias exactas y sigue siendo útil para genealogía; no bloquea investigación.

Desde el punto de vista de migración entre chats y reproducibilidad técnica del replay histórico, el repositorio está suficientemente cerrado para reentrada. La ruta sustantiva vuelve a literatura lingüística, corpus oral independiente de Juchitán y discusión pedagógica abierta de COR002.

COR001 permanece `ANALYSIS_TARGET_ONLY`: el `PASS` técnico no lo convierte en benchmark, gold, regresión ni fuente de reglas.
