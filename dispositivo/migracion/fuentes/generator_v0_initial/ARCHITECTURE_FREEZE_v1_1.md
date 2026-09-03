# ARCHITECTURE FREEZE — DIDXAZÁ v1.1

## Estado

```text
FREEZE_ID = DIDXAZA_ARCH_V1_1_FREEZE_2026-08-28
FREEZE_STATUS = SEALED
LOCAL_DATE = 2026-08-28
TIMEZONE = America/Mexico_City
CANONICAL_PREDECESSOR = v0.2.15.3
IMPLEMENTATION_PHASE = NUCLEO_CONVERSACIONAL_001
```

Este documento **no crea una arquitectura nueva**. Registra y congela la arquitectura ya adjudicada en `SINTESIS_ADVERSARIAL_ARQUITECTURA_DIDXAZA_v1_1_CORREGIDA.md` para impedir deriva durante el vertical slice.

## Documento arquitectónico gobernante congelado

```text
01_CANONICO/SINTESIS_ADVERSARIAL_ARQUITECTURA_DIDXAZA_v1_1_CORREGIDA.md
SHA256 = 2c4e7ea01261dfa6917674acdafa1b398470f7296b9ea183f345b4b1010123ea
```

Predecesor runtime:

```text
v0.2.15.3 — Surface Semantics & Resolution Integrity — CLOSED_PASS
DB = BASE_CORRECTOR_DIDXAZA_SURFACE_SEMANTICS_v2_20.sqlite
CANONICAL_STATE = canonical_state_v17
```

El paquete migratorio no contiene el runtime ejecutable ni la base SQLite; por tanto este freeze no modifica código runtime. Toda implementación posterior debe partir de los activos de v0.2.15.3 y comprobar primero qué schemas/APIs/capas ya existen.

## Invariantes congelados

```text
REUSE_BEFORE_REEXTRACT = REQUIRED
EXISTING_SCHEMA -> GAP_ANALYSIS -> EXTEND/MIGRATE = REQUIRED
PARALLEL_ARCHITECTURE = PROHIBITED

AUTO_CORRECT = OFF
VISIBLE_SUGGESTIONS = OFF
EDIT_EXECUTION = OFF
PDLMA_TO_SURFACE = PROHIBITED
NEAR_MATCH_TO_SURFACE = PROHIBITED
TONE_STRIPPING_FOR_EXACT_SURFACE = PROHIBITED
GLOBAL_NUMERIC_CONFIDENCE = PROHIBITED
SOURCE_COUNT_AS_CONFIDENCE = PROHIBITED

EVIDENCE_ORIGIN = SOURCE_ATTESTATION | SPEAKER_ATTESTATION | PROJECT_NORMALIZED | PROJECT_GENERATED
NO_DERIVED_FORM_CAN_LICENSE_ITSELF = BLOCKING_INVARIANT
```

## COR001 — rol definitivo congelado

```text
COR001_ROLE = ANALYSIS_TARGET_ONLY
COR001_AS_REFERENCE = PROHIBITED
COR001_AS_BENCHMARK = PROHIBITED
COR001_AS_GOLD_STANDARD = PROHIBITED
COR001_AS_REGRESSION_SUITE = PROHIBITED
COR001_FOR_RULE_DISCOVERY = PROHIBITED
COR001_FOR_TRAINING = PROHIBITED
COR001_FOR_EXPECTED_ANSWERS = PROHIBITED
```

Flujo permitido:

```text
COR001 item -> system analysis -> observe capabilities/gaps
```

Si COR001 revela un hueco, sólo puede resolverse con evidencia independiente.

## Arquitectura v1.1 congelada

Capacidades de producto conservadas:

- NORMALIZER
- ANALYZER
- CORRECTOR
- TUTOR
- GENERATOR
- CORPUS_GENERATOR

Vista de implementación congelada:

```text
ANALYZER CORE
  -> AnalysisBundle
  -> Candidate Engine / NORMALIZER
  -> Orthographic Policy
  -> normalized output

AnalysisBundle
  -> CORRECTOR projection
  -> TUTOR projection

ConstructionInventory
  x AttestedParadigmCells
  x AuthorizedSlotFillers
  -> LICENSED GENERATOR
  -> CORPUS GENERATOR
```

Transversal:

- `ValidationQueue`
- `ConceptMapping` (TAM primero)
- guard de `EvidenceOrigin`

Pipeline separado:

```text
CORPUS ACQUISITION
  audio-first
  -> speaker confirmation
  -> analysis
  -> orthographic realization
  -> adjudicated corpus
```

## Reutilización obligatoria

No reconstruir:

1. Foundation
2. Retrieval
3. Context & Provenance
4. Morphology I
5. BOUND
6. Morphology II
7. Evidence Adjudication
8. Decision Simulation
9. Surface Evidence & Coverage
10. Documentary Alignment
11. Pickett Lexical Backfill
12. Pickett Internal Surface & Cross-Source
13. Resolution Vectors
14. Person/Possession Alignment
15. Evidence Qualification
16. Evidence Integrity Repair
17. Surface Semantics & Resolution Integrity

Considerar antes de crear un candidate engine nuevo:

```text
MVP_LINGUISTICO_001 / REVIEW_CANDIDATE
= IMPLEMENTED_NON_CANONICAL antecedent
```

Regla:

```text
existing object/API/schema?
    YES -> reuse or migrate minimally
    NO  -> document gap -> extend only if slice requires it
```

## Objetos autorizados para el slice

La arquitectura permite materializar, sólo en la medida necesaria para `NUCLEO_CONVERSACIONAL_001`:

- `AnalysisBundle` como wrapper de referencias, nunca merger de verdad;
- `NormalizationCandidate` anclado a target/coordenadas y preservando `observed_surface`;
- `ConstructionInventory_v1`;
- `ParadigmTable_v1`, sólo celdas atestiguadas;
- `ConceptMapping_v1`, empezando exclusivamente por `dimension = TAM`;
- `OrthographicProfile_v1_DRAFT` como policy layer que referencia provenance existente;
- `AdoptionRecord` por regla;
- `ValidationQueue_v0`;
- `Generator_v0` de recombinación licenciada;
- `Tutor_v0` como renderer del análisis.

## Tests bloqueantes congelados

1. `NO_DERIVED_FORM_CAN_LICENSE_ITSELF`.
2. Toda celda usada por GENERATOR tiene `evidence_id`.
3. Toda normalización conserva `observed_surface` y target/coordenadas originales.
4. Si falta construcción, celda o política: `ABSTAIN(reason)`.
5. Round-trip estructural de generación a análisis recupera rasgos compatibles.
6. Juicios de hablantes se registran de forma categórica/por juez; no crean score global de naturalidad.
7. COR001 sólo produce observaciones, abstenciones, fenómenos no resueltos y notas de capacidad.

## Qué queda congelado fuera del slice

No abrir durante `NUCLEO_CONVERSACIONAL_001`:

- schemas generales nuevos no exigidos por el slice;
- módulos generales nuevos;
- nuevo Retrieval;
- nuevo BOUND;
- fine-tuning;
- TTS;
- causativos generativos automáticos;
- inferencia abierta de paradigmas;
- generación libre masiva;
- normalización destructiva masiva de Biyubi;
- resolución dialectal amplia;
- norma ortográfica global definitiva.

## Resolución de inconsistencias históricas

Algunos documentos de inventario/auditoría anteriores a la adjudicación v1.1 aún contienen formulaciones como:

```text
COR001 = DEVELOPMENT_REGRESSION_ONLY
```

o campos genéricos `confidence` en propuestas de data model.

Esas formulaciones **no gobiernan** el estado congelado. La síntesis v1.1 posterior establece:

```text
COR001 = ANALYSIS_TARGET_ONLY
GLOBAL_NUMERIC_CONFIDENCE = PROHIBITED
```

Dentro del JLC v0.27, las reglas `JLC-SP2-*` tienen precedencia sobre formulaciones anteriores incompatibles, según la propia regla de precedencia del core.

## Regla de cambio después del freeze

Durante el slice sólo se admite cambio arquitectónico si aparece un blocker real que haga imposible implementar el alcance congelado sin violar un invariante.

Todo cambio debe registrarse antes de implementarse como:

```text
ARCHITECTURE_CHANGE_RECORD
- change_id
- blocker
- affected frozen decision
- existing-runtime gap evidence
- minimal proposed change
- migration impact
- tests affected
- decision
```

Una mejora conveniente, una nueva idea o evidencia adicional no basta para descongelar arquitectura.

## Siguiente paso autorizado

```text
DESIGN_AND_SEAL_PROTOCOL(HOLDOUT_CONVERSATIONAL_001)
```

Después de sellar ese protocolo:

```text
DEFINE_EXACT_SCOPE(NUCLEO_CONVERSACIONAL_001)
```
