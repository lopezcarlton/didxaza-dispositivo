# Knowledge source pin

**Estado:** `CURRENT_CANONICAL_KNOWLEDGE_PIN / DERIVED_SYSTEM`
**Actualizado:** 2026-09-04

```text
KNOWLEDGE_SOURCE_REPOSITORY = lopezcarlton/vocesdelasnubes
KNOWLEDGE_SOURCE_COMMIT = 05567cec1bf3d6beb5ec373529674bee1212112a
KNOWLEDGE_SOURCE_REF = main
```

Este pin identifica el estado canónico exacto de Voces de las Nubes que debe consumirse para nuevo trabajo técnico reproducible. Una rama móvil puede consultarse para descubrimiento, pero toda ejecución o modificación que dependa de conocimiento debe registrar el commit resuelto.

## Pin histórico de la separación

El snapshot de conocimiento asociado a la separación física inicial permanece preservado como antecedente y no se reescribe retroactivamente:

```text
INITIAL_SPLIT_KNOWLEDGE_SOURCE_COMMIT = 22e3c088a97150453f28d03b31613ff9d9491d9a
INITIAL_SPLIT_DATE = 2026-09-03
```

La identidad técnica del snapshot inicial continúa documentada en `SEPARATION_VERIFICATION_2026-09-03.md` y en la historia Git.

## Alcance del pin actual

El commit actual incorpora, entre otros cambios canónicos posteriores a la separación:

- piloto PBK2016 de clases verbales (`HALL-0073`–`HALL-0076`);
- backfill dirigido de Gramática Popular §7.2–7.3 (`HALL-0077`–`HALL-0089`);
- `conocimiento/TEORIA.md` v1.4 con corrección del sistema aspectual.

Reglas de precedencia relevantes para el dispositivo:

```text
VOCES_HALL_DECISION_VIEW_AT_PIN = CANONICAL_KNOWLEDGE
JUCHITAN_LINGUISTIC_CORE_v0_27 = DERIVED_HISTORICAL_COMPILATION
DEVICE_DERIVED_FORMULATION_MUST_NOT_OVERRIDE_PINNED_VOCES = true
```

En particular:

- la Gramática Popular afirma que Juego 1C no tiene prefijo para el potencial (`HALL-0081`);
- esto corrige el grado de incertidumbre documental de `JLC-SP2-006`;
- **no** autoriza generación ciega por analogía: análisis/generación siguen requiriendo lema, clase y paradigma cuando la implementación lo necesite;
- la interpretación de `u` en Juego 2 como vocal temática causativa permanece como hipótesis de la fuente (`HALL-0082`);
- el perfecto no debe representarse como un perfecto genérico de resultado presente (`HALL-0078`);
- potencial, completivo, progresivo y estativo no deben mapearse mecánicamente a categorías temporales españolas (`HALL-0077`, `HALL-0084`–`HALL-0088`).

No se modifica aquí el runtime histórico ni sus artefactos byte-exactos. Cualquier cambio ejecutable posterior debe consumir este pin o uno más reciente y conservar provenance hacia las entidades canónicas pertinentes.
