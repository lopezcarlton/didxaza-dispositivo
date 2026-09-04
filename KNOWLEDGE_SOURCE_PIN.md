# Knowledge source pin

**Estado:** `CURRENT_CANONICAL_KNOWLEDGE_PIN / DERIVED_SYSTEM`
**Actualizado:** 2026-09-04

```text
KNOWLEDGE_SOURCE_REPOSITORY = lopezcarlton/vocesdelasnubes
KNOWLEDGE_SOURCE_COMMIT = 478ef8177598ab565e5acd6c9f245b4ae83a093d
KNOWLEDGE_SOURCE_REF = main
```

Este pin identifica el estado canónico exacto de Voces de las Nubes que debe consumirse para nuevo trabajo técnico reproducible. Una rama móvil puede consultarse para descubrimiento, pero toda ejecución o modificación que dependa de conocimiento debe registrar el commit resuelto.

## Pin histórico de separación

```text
INITIAL_SPLIT_KNOWLEDGE_SOURCE_COMMIT = 22e3c088a97150453f28d03b31613ff9d9491d9a
INITIAL_SPLIT_DATE = 2026-09-03
```

## Alcance canónico actual

El pin incorpora:

- PBK2016 (`HALL-0073`–`HALL-0076`);
- Gramática Popular P0 estructural (`HALL-0077`–`HALL-0140`);
- PVM 2009/2010 + corrigendum (`HALL-0141`–`HALL-0150`);
- Xneza 2015 (`HALL-0151`–`HALL-0158`);
- Bueno Holle 2019 (`HALL-0159`–`HALL-0167`, además de `HALL-0007`, `HALL-0067`, `HALL-0068` ya existentes);
- checkpoint de semantic backfill con siguiente frente = P1 Vocabulario Pickett.

Reglas de precedencia relevantes:

```text
VOCES_AT_PIN = CANONICAL_KNOWLEDGE
DEVICE_DERIVED_FORMULATION_MUST_NOT_OVERRIDE_PINNED_VOCES = true
```

Consecuencias recientes:

```text
REFERENCE_FORM_SELECTION = DISCOURSE_SENSITIVE
OVERT_3RD != ZERO_3RD_FREE_VARIATION
FOCUS != GENERIC_EMPHASIS
TOPIC != FOCUS
nga != GENERIC_EMPHASIS_PARTICLE_BY_DEFAULT
la != SIMPLE_COMMA
IU != ORTHOGRAPHIC_SENTENCE_BY_DEFAULT
CORPUS_TENDENCY != CATEGORICAL_GENERATION_RULE
```

`HALL-0150` conserva la discrepancia bibliográfica abierta GP2001/PVM2010 sobre `b/d/g` intervocálicas. El dispositivo no debe resolverla unilateralmente.

No se modifica aquí runtime histórico, SQLite, JLC ni otros artefactos byte-exactos.

```text
COR001 = ANALYSIS_TARGET_ONLY
UNRESOLVED != INCORRECT
```
