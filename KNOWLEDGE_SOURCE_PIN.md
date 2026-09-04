# Knowledge source pin

**Estado:** `CURRENT_CANONICAL_KNOWLEDGE_PIN / DERIVED_SYSTEM`
**Actualizado:** 2026-09-04

```text
KNOWLEDGE_SOURCE_REPOSITORY = lopezcarlton/vocesdelasnubes
KNOWLEDGE_SOURCE_COMMIT = caced70ceaab9e86564daf1717f6295cfe65a788
KNOWLEDGE_SOURCE_REF = main
```

Este pin identifica el estado canónico exacto de Voces de las Nubes que debe consumirse para nuevo trabajo técnico reproducible. Una rama móvil puede consultarse para descubrimiento, pero toda ejecución o modificación que dependa de conocimiento debe registrar el commit resuelto.

## Pin histórico de separación

```text
INITIAL_SPLIT_KNOWLEDGE_SOURCE_COMMIT = 22e3c088a97150453f28d03b31613ff9d9491d9a
INITIAL_SPLIT_DATE = 2026-09-03
```

## Alcance canónico actual

El pin incorpora el systematic semantic backfill completado hasta las fuentes prioritarias actualmente accesibles:

- PBK2016 (`HALL-0073`–`HALL-0076`);
- Gramática Popular P0 estructural (`HALL-0077`–`HALL-0140`);
- PVM 2009/2010 + corrigendum (`HALL-0141`–`HALL-0150`);
- Xneza 2015 (`HALL-0151`–`HALL-0158`);
- Bueno Holle 2019 (`HALL-0159`–`HALL-0167`, además de hallazgos previos relacionados);
- Vocabulario Pickett 2007 P1 lexicográfico (`HALL-0168`–`HALL-0178`);
- Cardona 2020 + Cardona–Vicente 2025 P1 variación/escritura (`HALL-0179`–`HALL-0183`);
- checkpoint `SEMANTIC_BACKFILL_CHECKPOINT_2026-09-04` con estado `SYSTEMATIC_BACKFILL_PASS_COMPLETE_TO_AVAILABLE_SOURCES / NORMA_2016_BLOCKED_BY_ACCESS`.

Reglas de precedencia relevantes:

```text
VOCES_AT_PIN = CANONICAL_KNOWLEDGE
DEVICE_DERIVED_FORMULATION_MUST_NOT_OVERRIDE_PINNED_VOCES = true
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
UNRESOLVED != INCORRECT
```
