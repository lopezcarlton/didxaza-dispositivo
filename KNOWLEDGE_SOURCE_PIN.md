# Knowledge source pin

**Estado:** `CURRENT_CANONICAL_KNOWLEDGE_PIN / DERIVED_SYSTEM`
**Actualizado:** 2026-09-04

```text
KNOWLEDGE_SOURCE_REPOSITORY = lopezcarlton/vocesdelasnubes
KNOWLEDGE_SOURCE_COMMIT = d6eb3861a7e6816f8c9181034f8d52b212cddb9c
KNOWLEDGE_SOURCE_REF = main
```

Este pin identifica el estado canónico exacto de Voces de las Nubes que debe consumirse para nuevo trabajo técnico reproducible. Una rama móvil puede consultarse para descubrimiento, pero toda ejecución o modificación que dependa de conocimiento debe registrar el commit resuelto.

## Pin histórico de separación

```text
INITIAL_SPLIT_KNOWLEDGE_SOURCE_COMMIT = 22e3c088a97150453f28d03b31613ff9d9491d9a
INITIAL_SPLIT_DATE = 2026-09-03
```

La identidad inicial permanece preservada en Git y en `SEPARATION_VERIFICATION_2026-09-03.md`.

## Alcance canónico actual

El pin incorpora:

- PBK2016 (`HALL-0073`–`HALL-0076`);
- backfill P0 estructural de Gramática Popular (`HALL-0077`–`HALL-0140`);
- PVM 2009/2010 + corrigendum (`HALL-0141`–`HALL-0150`);
- Xneza 2015 (`HALL-0151`–`HALL-0158`);
- checkpoint `SEMANTIC_BACKFILL_CHECKPOINT_2026-09-04` con siguiente P0 = Bueno Holle 2019.

Reglas de precedencia:

```text
VOCES_AT_PIN = CANONICAL_KNOWLEDGE
JUCHITAN_LINGUISTIC_CORE_v0_27 = DERIVED_HISTORICAL_COMPILATION
DEVICE_DERIVED_FORMULATION_MUST_NOT_OVERRIDE_PINNED_VOCES = true
```

Consecuencias nuevas especialmente relevantes:

```text
PHONEME != ALLOPHONE != ORTHOGRAPHIC_GRAPHEME
THREE_PHONEMIC_TONES != FIVE_ROOT_MELODIES
ALLOPHONE != SPELLING_CORRECTION
PHONOLOGICAL_WORD != GRAMMATICAL_WORD != ORTHOGRAPHIC_WORD_BY_DEFAULT
TOKEN_BOUNDARY != PHONOLOGICAL_BOUNDARY_BY_DEFAULT
CLITIC_HOSTING != AUTOMATIC_SPACING_POLICY
PROSODIC_WEAKENING != COMPOUND_PROOF
SPANISH_STRESS_ORTHOGRAPHY_AS_TEMPLATE = unsafe
```

`HALL-0150` conserva una discrepancia bibliográfica abierta entre GP2001 y PVM2010 respecto de la realización intervocálica de `b/d/g`; el dispositivo no debe resolverla unilateralmente.

No se modifica aquí runtime histórico, SQLite, JLC ni otros artefactos byte-exactos. Cualquier cambio ejecutable posterior debe consumir este pin o uno más reciente y conservar provenance hacia las entidades canónicas pertinentes.

```text
COR001 = ANALYSIS_TARGET_ONLY
UNRESOLVED != INCORRECT
```
