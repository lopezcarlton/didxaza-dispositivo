# REENTRY TÉCNICO — DISPOSITIVO DIDXAZÁ

**Estado:** `TECHNICAL_REENTRY / NON_CANONICAL / DERIVED_SYSTEM / SEPARATE_REPOSITORY`
**Actualizado:** 2026-09-03

## Propósito

Este archivo es el punto de entrada heredado para trabajo técnico sobre Analyzer, Corrector, Tutor, Generator, runtime, schemas, pruebas, migración y otras capacidades del dispositivo.

El punto de entrada principal del repositorio separado es ahora `../REENTRY_TECNICO.md` en la raíz de `lopezcarlton/didxaza-dispositivo`.

No es un punto de entrada general de Voces de las Nubes.

## Frontera de autoridad

```text
VOCES_DE_LAS_NUBES = AUTHORITY_FOR_KNOWLEDGE
KNOWLEDGE_REPOSITORY = lopezcarlton/vocesdelasnubes
DEVICE_REPOSITORY = lopezcarlton/didxaza-dispositivo
DISPOSITIVO = DERIVED_SYSTEM

DEVICE_MAY_READ = true
DEVICE_MAY_ANALYZE = true
DEVICE_MAY_PROPOSE = true
DEVICE_MAY_CHALLENGE = true
DEVICE_MAY_ADOPT_KNOWLEDGE = false
DEVICE_MAY_PROMOTE_CANDIDATE = false
DEVICE_MAY_WRITE_KNOWLEDGE = false
```

Regla vigente en Voces: `conocimiento/decisiones/DEC-AUTORIDAD-SISTEMA-CONOCIMIENTO.md`.

Los paths `conocimiento/...`, `00_ARQUITECTURA...`, etc. que aparezcan en documentos técnicos históricos deben resolverse en `lopezcarlton/vocesdelasnubes`, no suponerse presentes localmente.

## Reconstrucción técnica

Leer, en este orden:

1. `../REENTRY_TECNICO.md`
2. `../KNOWLEDGE_SOURCE_PIN.md`
3. `../SEPARATION_VERIFICATION_2026-09-03.md`
4. `KNOWLEDGE_CONSUMPTION_CONTRACT_v1.md`
5. `BACKLOG_TECNICO.md`
6. `migracion/CURRENT_EXECUTABLE_STATE_v1.md`
7. `migracion/MIGRATION_MANIFEST_v1.md` cuando se necesite genealogía histórica
8. los artefactos técnicos específicos del trabajo actual.

Para BIB065 y pedagogía, no tomar matrices, JLC, freezes ni otros artefactos técnicos como autoridad. Si el dispositivo detecta una consecuencia posible para Voces, volver a la fuente original y al procedimiento de actualización del Sistema de Conocimiento.

## COR001

```text
COR001 = ANALYSIS_TARGET_ONLY
COR001 != GOLD_STANDARD
COR001 != BENCHMARK_AUTHORITY
COR001 != REGRESSION_AUTHORITY
COR001 != RULE_DISCOVERY_SOURCE
```

El replay histórico sirve exclusivamente para reproducibilidad técnica.

## Separación física

La separación física quedó completada el 2026-09-03. El snapshot de origen está identificado por:

```text
SOURCE_COMMIT = 22e3c088a97150453f28d03b31613ff9d9491d9a
INITIAL_IMPORT_COMMIT = 6d205ffe0a0fe660229cd7a958fe43c9a5b51508
DEVICE_TREE_SHA = d92c38ec45be4e2e3176b1cfe7c288321c887d3b
```

Ver `../SEPARATION_VERIFICATION_2026-09-03.md`.
