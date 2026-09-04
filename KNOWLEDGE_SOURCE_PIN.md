# Knowledge source pin

**Estado:** `CURRENT_CANONICAL_KNOWLEDGE_PIN / DERIVED_SYSTEM`
**Actualizado:** 2026-09-04

```text
KNOWLEDGE_SOURCE_REPOSITORY = lopezcarlton/vocesdelasnubes
KNOWLEDGE_SOURCE_COMMIT = 212cfddda4005d3417e72776ce396c2388748444
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
- backfill dirigido de Gramática Popular:
  - sistema verbal/aspectual (`HALL-0077`–`HALL-0089`);
  - persona (`HALL-0090`–`HALL-0096`);
  - posesión (`HALL-0097`–`HALL-0101`);
  - causatividad/valencia (`HALL-0102`–`HALL-0105`);
  - imperativos/movimiento (`HALL-0106`–`HALL-0109`);
  - negación/partículas/preguntas (`HALL-0110`–`HALL-0114`);
  - combinación de oraciones (`HALL-0115`–`HALL-0121`);
  - Apéndice técnico de fonética/prosodia (`HALL-0122`–`HALL-0124`);
- `conocimiento/TEORIA.md` v1.7;
- checkpoint de backfill actualizado con P0-A Gramática Popular `IN_PROGRESS`.

Reglas de precedencia relevantes para el dispositivo:

```text
VOCES_HALL_DECISION_VIEW_AT_PIN = CANONICAL_KNOWLEDGE
JUCHITAN_LINGUISTIC_CORE_v0_27 = DERIVED_HISTORICAL_COMPILATION
DEVICE_DERIVED_FORMULATION_MUST_NOT_OVERRIDE_PINNED_VOCES = true
```

Consecuencias técnicas del lote:

- la Gramática Popular afirma que Juego 1C no tiene prefijo para el potencial (`HALL-0081`), sin autorizar generación ciega por analogía;
- la interpretación de `u` en Juego 2 como vocal temática causativa permanece hipótesis de la fuente (`HALL-0082`);
- el perfecto no debe representarse como perfecto genérico de resultado presente (`HALL-0078`);
- potencial, completivo, progresivo y estativo no deben mapearse mecánicamente a tiempos españoles (`HALL-0077`, `HALL-0084`–`HALL-0088`);
- tercera persona sin marca segmental puede ser válida si el referente es recuperable (`HALL-0092`): `UNMARKED != ERROR`;
- persona y posesión contienen fusiones/alternancias: no aplicar stripping ciego de afijos (`HALL-0093`, `HALL-0094`, `HALL-0098`–`HALL-0101`);
- causatividad es sensible a lema/paradigma y no se genera universalmente con `si-` (`HALL-0102`–`HALL-0105`);
- imperativo singular/plural y verbos de movimiento requieren patrones específicos (`HALL-0106`–`HALL-0109`);
- negación e interrogación deben resolverse por construcción, no por sustitución lineal (`HALL-0110`–`HALL-0114`);
- secuencias complejas deben distinguir coordinación, complemento, pregunta indirecta, subordinada adverbial y relativa; español `que` no es una plantilla universal (`HALL-0115`–`HALL-0121`);
- fuerte/débil no equivale sólo a sordo/sonoro y las realizaciones fonéticas contextuales no deben convertirse en cambios ortográficos (`HALL-0122`, `HALL-0123`);
- la neutralización prosódica en frases/compuestos no autoriza borrar marcas de la forma ortográfica de cita (`HALL-0124`).

No se modifica aquí el runtime histórico, la SQLite, el JLC ni otros artefactos byte-exactos. El conocimiento canónico se sincroniza por pin y cualquier cambio ejecutable posterior debe consumir este commit o uno más reciente y conservar provenance hacia las entidades canónicas pertinentes.
