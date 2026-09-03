# REENTRY TÉCNICO — DIDXAZA DISPOSITIVO

**Estado:** `ACTIVE_TECHNICAL_REENTRY / DERIVED_SYSTEM / SEPARATE_REPOSITORY`
**Fecha:** 2026-09-03

## Frontera de autoridad

Este repositorio contiene implementación técnica. No contiene la autoridad lingüística, pedagógica, metodológica ni comunitaria de Voces de las Nubes.

```text
KNOWLEDGE_AUTHORITY_REPOSITORY = lopezcarlton/vocesdelasnubes
DEVICE_REPOSITORY = lopezcarlton/didxaza-dispositivo

DEVICE_MAY_READ = true
DEVICE_MAY_ANALYZE = true
DEVICE_MAY_PROPOSE = true
DEVICE_MAY_CHALLENGE = true
DEVICE_MAY_ADOPT_KNOWLEDGE = false
DEVICE_MAY_PROMOTE_CANDIDATE = false
DEVICE_MAY_WRITE_KNOWLEDGE = false
```

Para trabajo reproducible, leer `KNOWLEDGE_SOURCE_PIN.md` y conservar un `KNOWLEDGE_SOURCE_COMMIT` exacto.

## Estado inicial de la separación

El snapshot técnico inicial fue importado desde:

```text
SOURCE_REPOSITORY = lopezcarlton/vocesdelasnubes
SOURCE_COMMIT = 22e3c088a97150453f28d03b31613ff9d9491d9a
SOURCE_PATH = dispositivo/
IMPORTED_DEVICE_COMMIT = 6d205ffe0a0fe660229cd7a958fe43c9a5b51508
IMPORTED_DEVICE_TREE_SHA = d92c38ec45be4e2e3176b1cfe7c288321c887d3b
```

El subdirectorio `dispositivo/` se conserva en esta primera etapa para mantener rutas y reproducibilidad. No significa que el dispositivo siga perteneciendo al repositorio de conocimiento.

## Orden de lectura técnica

1. `KNOWLEDGE_SOURCE_PIN.md`
2. `SEPARATION_VERIFICATION_2026-09-03.md`
3. `dispositivo/KNOWLEDGE_CONSUMPTION_CONTRACT_v1.md`
4. `dispositivo/BACKLOG_TECNICO.md`
5. `dispositivo/migracion/CURRENT_EXECUTABLE_STATE_v1.md`
6. `dispositivo/migracion/MIGRATION_MANIFEST_v1.md` sólo cuando la genealogía histórica sea necesaria
7. los artefactos técnicos específicos del trabajo actual.

Los documentos importados dentro de `dispositivo/` son el snapshot exacto del antiguo monorepo y pueden contener rutas relativas históricas como `conocimiento/...`. Cuando aparezcan, deben resolverse en `lopezcarlton/vocesdelasnubes` y no interpretarse como archivos locales faltantes.

## COR001

```text
COR001 = ANALYSIS_TARGET_ONLY
COR001 != GOLD_STANDARD
COR001 != BENCHMARK_AUTHORITY
COR001 != RULE_DISCOVERY_SOURCE
```

El replay COR001 existe únicamente para reproducibilidad técnica del runtime histórico.

## Descubrimientos del dispositivo

```text
TECHNICAL_RESULT
-> IDENTIFY_ORIGINAL_SOURCE_OR_EVIDENCE
-> RETURN_CANDIDATE_TO_VOCES
-> HUMAN/KNOWLEDGE_SYSTEM_ADJUDICATION
-> NEW_CANONICAL_KNOWLEDGE_COMMIT_IF_ADOPTED
-> DEVICE_CONSUMES_PINNED_STATE
```

Nunca usar un JLC, registry, SQLite, output de Analyzer/Generator o matriz técnica como sustituto de la fuente original.
