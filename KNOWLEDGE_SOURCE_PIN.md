# Knowledge source pin

**Estado:** `CURRENT_CANONICAL_KNOWLEDGE_PIN / DERIVED_SYSTEM`
**Actualizado:** 2026-09-05

```text
KNOWLEDGE_SOURCE_REPOSITORY = lopezcarlton/vocesdelasnubes
KNOWLEDGE_SOURCE_COMMIT = f17c5363caada6f8beb18fa99c39e37cd72c6f09
KNOWLEDGE_SOURCE_REF = main
```

Este pin identifica el estado canónico exacto de Voces de las Nubes que debe consumirse para nuevo trabajo técnico reproducible. Una rama móvil puede consultarse para descubrimiento, pero toda ejecución o modificación que dependa de conocimiento debe registrar el commit resuelto.

## Pin histórico de separación

```text
INITIAL_SPLIT_KNOWLEDGE_SOURCE_COMMIT = 22e3c088a97150453f28d03b31613ff9d9491d9a
INITIAL_SPLIT_DATE = 2026-09-03
```

## Alcance canónico actual

El pin incorpora el systematic semantic backfill completado hasta las fuentes prioritarias actualmente accesibles y las adjudicaciones posteriores ya promovidas:

- PBK2016 (`HALL-0073`–`HALL-0076`);
- Gramática Popular P0 estructural (`HALL-0077`–`HALL-0140`);
- PVM 2009/2010 + corrigendum (`HALL-0141`–`HALL-0150`);
- Xneza 2015 (`HALL-0151`–`HALL-0158`);
- Bueno Holle 2019 (`HALL-0159`–`HALL-0167`, además de hallazgos previos relacionados);
- Vocabulario Pickett 2007 P1 lexicográfico (`HALL-0168`–`HALL-0178`);
- Cardona 2020 + Cardona–Vicente 2025 P1 variación/escritura (`HALL-0179`–`HALL-0183`);
- cierre dirigido del Alfabeto Popular de 1956 hasta `HALL-0185`;
- recuperación independiente posterior a un hueco de análisis: atestación documental conservadora de `binnilaanu` en Xneza/Teria (`HALL-0186`) y separación AP/PDLMA + evidencia `ndani`/`gundani` en Dictionaria (`HALL-0187`);
- adjudicación directa de Pérez Báez 2015 sobre cambio morfológico de valencia: separación TAM/derivación (`HALL-0188`), grupos vocálicos V1–V3 (`HALL-0189`), grupos consonánticos C1–C4 (`HALL-0190`) y variación/productividad/equipolencia (`HALL-0191`);
- semántica explícita de códigos gramaticales Dictionaria para causativo, intransitivo y transitivo (`HALL-0192`);
- relaciones concretas fuente-explícitas de Pérez Báez 2015 entre miembros de díadas/tríadas y equipolentes (`HALL-0193`), con derivado selectivo de 65 miembros / 26 conjuntos y auditoría que confirma que el snapshot fijado de Dictionaria no contiene campos de relación poblados;
- checkpoint `SEMANTIC_BACKFILL_CHECKPOINT_2026-09-04` con estado `SYSTEMATIC_BACKFILL_PASS_COMPLETE_TO_AVAILABLE_SOURCES / NORMA_2016_BLOCKED_BY_ACCESS`.

Reglas de precedencia relevantes:

```text
VOCES_AT_PIN = CANONICAL_KNOWLEDGE
DEVICE_DERIVED_FORMULATION_MUST_NOT_OVERRIDE_PINNED_VOCES = true
HALL_0186_EXACT_SURFACE_ATTESTATION != MORPHOLOGICAL_SEGMENTATION
HALL_0187_PDLMA_INFLECTION != AUTOMATIC_AP_SURFACE_EQUIVALENCE
HALL_0188_TAM_MARKER != VALENCY_DERIVATION
HALL_0189_ROOT_SHAPE != AUTOMATIC_V1_V2_V3_ASSIGNMENT
HALL_0190_PREFIX_RESEMBLANCE != AUTOMATIC_C1_C2_C3_C4_ASSIGNMENT
HALL_0191_DOCUMENTED_DERIVATIONAL_PATTERN != PRODUCTIVE_RULE
HALL_0192_LITERAL_DEFINED_CODE = LEXICAL_DOCUMENTARY_PROPERTY_ONLY
HALL_0192_CAUSATIVE_CODE != BASIC_CAUSATIVE_RELATION
HALL_0192_TRANSITIVITY_CODE != AUTOMATIC_NUMERIC_VALENCE
HALL_0193_SOURCE_TABLE_MEMBERSHIP = EXPLICIT_VALENCY_RELATION
HALL_0193_V1_MORE_ACTIVE != AUTOMATIC_CAUSATIVE
HALL_0193_PDLMA_MEMBER != AP_SURFACE
HALL_0193_SELECTED_REGISTRY != EXHAUSTIVE_SOURCE_TRANSCRIPTION
STRICT_PDLMA_CROSSWALK_NO_MATCH != LINGUISTIC_ABSENCE
STRICT_PDLMA_CROSSWALK_MULTIPLE_MATCH != AUTOMATIC_DISAMBIGUATION
STRICT_PDLMA_ENTRY_LINK != OBSERVED_SURFACE_PDLMA_TO_AP_INFERENCE
vers = UNADJUDICATED
VALENCY_COMPATIBILITY != CORRECTION_OR_GENERATION_LICENSE
EXPLICIT_VALENCY_RELATION != GENERATION_LICENSE
```

Contradicciones abiertas que el dispositivo no debe resolver unilateralmente:

- `HALL-0150`: GP2001 vs PVM2010 sobre `b/d/g` intervocálicas;
- `HALL-0172`: Pickett 2007 vs Xneza 2015 sobre reglas españolas de acento ortográfico.

Estado de la Norma 2016:

```text
NORMA_2016_IDENTITY = RESOLVED
NORMA_2016_FULL_TEXT = NOT_ACCESSED
SECONDARY_QUOTATIONS != FULL_NORM
```

No se modifica aquí runtime histórico, SQLite, JLC ni otros artefactos byte-exactos.

```text
COR001 = ANALYSIS_TARGET_ONLY
NEW_WRITTEN_ANALYSIS_TARGET = ANALYSIS_TARGET_ONLY
UNRESOLVED != INCORRECT
```
