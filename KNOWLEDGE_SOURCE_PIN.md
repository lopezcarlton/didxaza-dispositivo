# Knowledge source pin

**Estado:** `CURRENT_CANONICAL_KNOWLEDGE_PIN / DERIVED_SYSTEM`
**Actualizado:** 2026-09-04

```text
KNOWLEDGE_SOURCE_REPOSITORY = lopezcarlton/vocesdelasnubes
KNOWLEDGE_SOURCE_COMMIT = 5a5a76eca11966b7df79edb76cf51ab94507bda1
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
- checkpoint `SEMANTIC_BACKFILL_CHECKPOINT_2026-09-04` con estado `SYSTEMATIC_BACKFILL_PASS_COMPLETE_TO_AVAILABLE_SOURCES / NORMA_2016_BLOCKED_BY_ACCESS`.

Reglas de precedencia relevantes:

```text
VOCES_AT_PIN = CANONICAL_KNOWLEDGE
DEVICE_DERIVED_FORMULATION_MUST_NOT_OVERRIDE_PINNED_VOCES = true
HALL_0186_EXACT_SURFACE_ATTESTATION != MORPHOLOGICAL_SEGMENTATION
HALL_0187_PDLMA_INFLECTION != AUTOMATIC_AP_SURFACE_EQUIVALENCE
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
