# CURRENT_EXECUTABLE_STATE_v1 — Estado materializado del dispositivo

**Repositorio:** `lopezcarlton/didxaza-dispositivo`  
**Autoridad de conocimiento:** `lopezcarlton/vocesdelasnubes`  
**Fecha:** 2026-09-03  
**Estado:** `CURRENT_TECHNICAL_CHECKPOINT / NON_CANONICAL / REVISABLE / POST_SPLIT`

## 1. Función

Este documento distingue entre:

- artefactos presentes;
- componentes que pueden instanciarse o ejecutarse con esos artefactos;
- snapshots históricos más avanzados cuyas dependencias todavía no están materializadas;
- protecciones técnicas vigentes del repositorio;
- preguntas de investigación que permanecen abiertas.

No reemplaza los estados históricos ni concede autoridad lingüística o pedagógica al código.

```text
MIGRATED != RUNNABLE
RUNNABLE_SUBSET != COMPLETE_COMPONENT
HISTORICAL_READINESS != CURRENT_CAPABILITY
TECHNICAL_CHECK != RESEARCH_CLOSURE
VOCES = AUTHORITY_FOR_KNOWLEDGE
DIDXAZA_DISPOSITIVO = DERIVED_TECHNICAL_SYSTEM
UNRESOLVED != INCORRECT
```

### 1.1 Estado post-separación del repositorio

La separación física respecto de `lopezcarlton/vocesdelasnubes` se completó el 2026-09-03. El snapshot inicial exacto se conserva en:

```text
SOURCE_COMMIT = 22e3c088a97150453f28d03b31613ff9d9491d9a
SOURCE_DEVICE_TREE_SHA = d92c38ec45be4e2e3176b1cfe7c288321c887d3b
INITIAL_IMPORT_COMMIT = 6d205ffe0a0fe660229cd7a958fe43c9a5b51508
IMPORTED_DEVICE_TREE_SHA = d92c38ec45be4e2e3176b1cfe7c288321c887d3b
```

El SHA de árbol `d92c38ec...` identifica el snapshot **en `6d205ff`**, no el `HEAD` actual. Los cambios post-importación están trazados por Git y no alteran retroactivamente ese snapshot.

El endurecimiento P0/P1 verificado hasta `e6d501c839269b878c0ae99a82aed69071e108af` añade:

```text
BYTE_EXACT_GITATTRIBUTES = active for 9 identified files
REPLAY_CI = push(main) + pull_request(main) + workflow_dispatch
RELEASE_MANIFEST_ANCHOR = present
RELEASE_MANIFEST_SHA256 = 5e3f7ff7035e8fdd6358ddae8432e37e52518cc9b50067dccfb7411c741f2304
RELEASE_MANIFEST_GIT_BLOB = e9cbb2062385e913d5acb59427aa6c1b53b54b14
MIGRATED_STATE_TESTS = 8/8 PASS
HISTORICAL_RUNTIME_TESTS = 38/38 PASS
LAST_VERIFIED_MAIN_PUSH_RUN = 33805988652 / success
PERMISSION_HARDENING = pending
```

La prueba migratoria usa 39 payloads presentes como piso monotónico contra regresión: puede subir al recuperar payloads exactos adicionales sin requerir reescribir un checkpoint rígido.

La protección de branch/rulesets sigue siendo un frente de infraestructura independiente. Ver `../../SEPARATION_VERIFICATION_2026-09-03.md` y `DEVICE_REPOSITORY_SEPARATION_PLAN_v1.md`.

## 2. Runtime v0.2.15.3

El manifiesto original enumera 75 payloads. En este checkpoint hay 39 payloads exactos presentes:

- los 39 coinciden con la identidad esperada del release o con la identidad exacta documentada para el artefacto reutilizado;
- los tres CSV de Dictionaria y la SQLite v2.20 están incluidos;
- siete módulos exactos forman el cierre importable de la prueba unitaria final;
- `test_surface_semantics_v0_2_15_3.py` está presente sin transformación;
- la SQLite v2.19, tres pruebas v0.2.15.2 y cuatro resultados de replay almacenados completan la cadena histórica de 38 pruebas;
- se restauraron además los módulos exactos v0.2.10, v0.2.11, v0.2.12 y v0.2.14, el input histórico COR001, el registry exacto de persona/posesión y `PICKETT_LEXICON_BACKFILL_v0_1.csv`;
- `CLEAN_REPLAY_VERIFICATION_v0_2_15_3.json` está ahora materializado con identidad exacta del release y conserva los hashes semánticos históricos de referencia;
- 36 payloads del release todavía no están migrados.

La SQLite exacta está en:

`runtime/v0_2_15_3/BASE_CORRECTOR_DIDXAZA_SURFACE_SEMANTICS_v2_20.sqlite`

Verificación:

```text
SHA256 = 2379773426baf4e3eace87c61ec17f7a1e1b9164421e56cf736d35eb64a5ebed
SQLITE_INTEGRITY_CHECK = ok
FOREIGN_KEY_VIOLATIONS = 0
canonical_state_v17 = 22 rows
verb_lexeme_class_v023 = present
person_possession_exact_v0214 = present
```

La fuente exacta de `DB_INTEGRITY_v0_2_15_3.json` se recuperó del ZIP canónico. La copia previa con salto de línea final permanece en la genealogía Git y fue sustituida por la identidad exacta:

```text
DB_INTEGRITY SHA256 = fa2b88c95b8d567b4165b49636f67cdf8c00fa1a036cf8c162d03a6bceb193bb
STATUS = EXACT_RELEASE_IDENTITY_VERIFIED
```

### 2.1 Slice unitario de semántica de superficie

Estado: `REPRODUCIBLE_SURFACE_SEMANTICS_UNIT_SLICE / NON_LICENSING / NON_AUTHORITATIVE`.

La prueba exacta `test_surface_semantics_v0_2_15_3.py` ejecuta 10 casos desde el árbol migrado y pasa. Su cierre de imports incluye los módulos exactos v0.2.6, v0.2.7, v0.2.7.1, v0.2.9, v0.2.13, v0.2.15.2 y el wrapper v0.2.15.3, además de módulos anteriores ya presentes.

El wrapper declara y las pruebas preservan:

```text
AUTO_CORRECT_ENABLED = false
ORTHOGRAPHIC_SUGGESTIONS_ENABLED = false
EDIT_EXECUTION_ENABLED = false
USER_VISIBLE_SUGGESTIONS_ENABLED = false
ANALYSIS_ONLY_SURFACE_PROMOTION = false
```

Esto reproduce el slice unitario de integridad de semántica de superficie. La cadena histórica de 38 pruebas también es ejecutable conforme a la sección siguiente. Los módulos v0.2.10, v0.2.11, v0.2.12 y v0.2.14 y todas las dependencias directas identificadas para el replay histórico están materializados. El replay histórico de COR001 fue además regenerado en un checkout aislado de GitHub Actions: runner `exit 0`, dependencias directas exactas y outputs deterministas `SUMMARY`/`METRICS` byte-idénticos al release. Esto verifica reproducibilidad técnica del runner, no los 26 criterios lingüísticos ni autoridad sobre COR001.

Estado del replay end-to-end:

`ISOLATED_REPLAY_REPRODUCED / TECHNICAL_REPRODUCIBILITY_PASS / NON_AUTHORITATIVE / COR001_ANALYSIS_TARGET_ONLY`.

Una segunda pasada ejecutada sobre un checkout sin mutación previa confirmó además: 17/17 módulos en la clausura recursiva de imports con SHA histórico exacto, 8/8 dependencias de datos exactas, hashes semánticos `details/metrics/summary` idénticos al clean replay histórico, `SUMMARY`/`METRICS` byte-idénticos y 38/38 pruebas `unittest` aprobadas. La diferencia byte a byte de `DETAILED` sigue limitada a IDs efímeros.

Evidencia histórica: `ISOLATED_REPLAY_VERIFICATION_v0_2_15_3_2026-09-02.md`.

### 2.2 Cadena histórica de 38 pruebas

Estado: `REPRODUCIBLE_STORED_ARTIFACT_TEST_CLOSURE / NON_AUTHORITATIVE`.

La cadena exacta ejecuta y supera:

```text
5  pruebas adversariales de integridad
12 pruebas sobre resultados de replay almacenados
11 pruebas de schema e integridad de la SQLite v2.19
10 pruebas de semántica de superficie v0.2.15.3
38 pruebas en total
```

La SQLite v2.19 y los cuatro resultados v0.2.15.2 usados por esas pruebas conservan la identidad exacta del release. El CSV de resumen mantiene sus bytes y terminadores de línea históricos; no fue normalizado durante la migración.

Las 12 pruebas de replay leen métricas, manifiesto, detalle y resumen ya almacenados. No ejecutan `run_cor001_replay_v0_2_15_2.py` ni `run_cor001_replay_v0_2_15_3.py`. Por ello demuestran consistencia del cierre histórico recuperado, no regeneración end-to-end ni validez lingüística de las salidas sobre COR001.

### 2.3 Recuperación adicional del runner histórico

Presentes y verificados contra la identidad histórica esperada:

```text
didxaza_runtime_v0_2_10_documentary_alignment.py
DOCUMENTARY_ALIGNMENT_REGISTRY_v0_2_15_2.csv
didxaza_runtime_v0_2_11_pickett_backfill.py
didxaza_runtime_v0_2_12_pickett_cross_source.py
didxaza_runtime_v0_2_14_person_possession.py
COR001_REPLAY_INPUT_v0_2_15_2.csv
PERSON_POSSESSION_EXACT_REGISTRY_v0_2_15_2.csv
PICKETT_LEXICON_BACKFILL_v0_1.csv
```

`PICKETT_LEXICON_BACKFILL_v0_1.csv` quedó materializado en `main` mediante subida directa del archivo fuente. La identidad se verificó byte a byte mediante SHA-256 y Git blob:

```text
SIZE = 940709 bytes
DATA_ROWS = 2534
SHA256 = 56e2372566cec9d7758b7e45b8de4e320a92eb2ee5c51b2a5e444e8165875723
GIT_BLOB = 98b4e87282b996e837356f41ead2f859d53face1
BOM_UTF8 = present
CRLF_LINES = 2535
STATUS = EXACT_BYTE_IDENTITY_VERIFIED
```

Con esto no queda ninguna dependencia directa conocida faltante para el replay histórico y la regeneración aislada ya fue ejecutada con `PASS` técnico. Durante esa verificación se restauró la representación byte-exacta histórica de `PERSON_POSSESSION_EXACT_REGISTRY_v0_2_15_2.csv` (`UTF-8 BOM + CRLF + final newline`, SHA-256 `3f1e955a285c2ce9c66d3953def6b41fd993d6b8dd81567c5f95a28281d20bdb`), corrigiendo sólo una normalización de transporte. La presencia del input y el éxito técnico no cambian el rol de COR001: `ANALYSIS_TARGET_ONLY`.

## 3. Analyzer v0.35

Estado: `REPRODUCIBLE_NON_LICENSING_PARTIAL_ANALYZER`.

Presentes:

- orquestador v0.35;
- `DIC_VERB_2385_v0_1.csv` exacto;
- módulos runtime v0.2.1, v0.2.3, v0.2.4 y v0.2.5;
- SQLite v2.20 exacta con las tablas críticas verificadas;
- `DICTIONARIA_entries_v0_2_15_2.csv`: 9,012 filas;
- `DICTIONARIA_senses_v0_2_15_2.csv`: 9,046 filas;
- `DICTIONARIA_examples_v0_2_15_2.csv`: 9,686 filas.

El adaptador ejecutable es:

`analyzer/analyzer_v0_35_migrated_adapter.py`

Pruebas de humo:

```text
"Quí rasé'" -> PARTIAL_ANALYSIS_NON_LICENSING
forma deliberadamente inexistente -> ABSTAIN_NO_COMPONENT_EVIDENCE
generation_license_assertion = false
correction_assertion = false
orthographic_authority_assertion = false
rule_discovery_assertion = false
```

“Reproducible” describe la carga y el comportamiento del Analyzer parcial v0.35, no una cobertura completa del Didxazá ni autoridad sobre nuevas reglas.

## 4. Generator_v0.5

`generator_v0_5.py` se preserva como la implementación histórica más reciente localizada. Su entrada por defecto no es ejecutable en el árbol migrado porque combina rutas de dos layouts distintos y espera `NovelRecombinationAttempt_v0_1.json`, que no está presente.

Para no alterar silenciosamente el artefacto histórico se añadió:

`generator/generator_v0_5_migrated_adapter.py`

El adaptador usa exclusivamente `generator/inputs/` y permite instanciar el subconjunto realmente materializado:

```text
PARADIGM_CELLS = 72
CONSTRUCTIONS = 6
GENERATION_LICENSES = 6
ACTIVE_LICENSE_CONSTRUCTIONS = C01, C02
BLOCKED_BY_MIGRATED_INPUTS = C03, C04, C05, C06
```

`GENERATION_READINESS_MATRIX_v14.csv` se conserva como el snapshot más reciente localizado, pero sus capacidades C03/C05 no son reproducibles con los archivos actualmente migrados. No se rebajó ni se reescribió la matriz: queda clasificada como:

`MIGRATED_SNAPSHOT_NOT_REPRODUCIBLE_WITH_CURRENT_FILES`.

## 5. Tutor_v0.33

Estado: `SOURCE_PRESENT / DEPENDENCIES_INCOMPLETE / NOT_INSTANTIABLE_YET`.

Faltan `TutorCaseLicenseBindings_v0_33.jsonl` y las licencias C03/C05 enumeradas en el manifiesto. La presencia del renderer no equivale a un Tutor ejecutable.

## 6. COR001 y terminología histórica

`core/JUCHITAN_LINGUISTIC_CORE_v0_27.md` conserva una referencia a “benchmarks COR001”. Esa formulación no representa la política vigente y no se usa como contrato de ejecución.

El rol actual es:

```text
COR001 = ANALYSIS_TARGET_ONLY
COR001 != GOLD_STANDARD
COR001 != BENCHMARK
COR001 != REGRESSION_AUTHORITY
COR001 != RULE_DISCOVERY_SOURCE
```

La frase histórica no se reescribió dentro del core experimental para no alterar silenciosamente el artefacto migrado.

## 7. Interpretación

Este checkpoint no decide si C03, C05, la escala P, las capas BIB065 u otra hipótesis deben mantenerse o cambiar. Tampoco interpreta un `PASS` técnico como validación lingüística. Sólo evita atribuir al repositorio capacidades que sus archivos actuales no pueden reproducir.

Las líneas de investigación, COR002, el trabajo con hablantes y la incorporación de nueva evidencia continúan abiertas conforme a `lopezcarlton/vocesdelasnubes/conocimiento/principios/PRIN-INVESTIGACION-ABIERTA.md`.

Los hallazgos P2/P3 de la auditoría técnica externa del 2026-09-03 no se adoptan por esta sincronización documental; deben verificarse por separado contra el repositorio antes de cualquier corrección adicional.
