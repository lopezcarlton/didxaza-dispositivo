# REENTRY TÉCNICO — DISPOSITIVO DIDXAZÁ

**Estado:** `TECHNICAL_REENTRY / NON_CANONICAL / DERIVED_SYSTEM`

## Propósito

Este archivo es el punto de entrada para trabajo explícitamente técnico sobre Analyzer, Corrector, Tutor, Generator, runtime, schemas, pruebas, migración y otras capacidades del dispositivo.

No es el punto de entrada general de Voces de las Nubes.

## Frontera de autoridad

Antes de trabajar, conservar:

```text
VOCES_DE_LAS_NUBES = AUTHORITY_FOR_KNOWLEDGE
DISPOSITIVO = DERIVED_SYSTEM

DEVICE_MAY_READ = true
DEVICE_MAY_ANALYZE = true
DEVICE_MAY_PROPOSE = true
DEVICE_MAY_CHALLENGE = true

DEVICE_MAY_ADOPT_KNOWLEDGE = false
DEVICE_MAY_PROMOTE_CANDIDATE = false
DEVICE_MAY_WRITE_KNOWLEDGE = false
```

Regla vigente: `conocimiento/decisiones/DEC-AUTORIDAD-SISTEMA-CONOCIMIENTO.md`.

## Reconstrucción técnica

Leer, en este orden:

1. `00_ARQUITECTURA_DEL_CONOCIMIENTO.md`
2. `01_JERARQUIA_DE_VERDAD.md`
3. `03_REGLAS_DE_ACTUALIZACIÓN.md`
4. `conocimiento/decisiones/DEC-AUTORIDAD-SISTEMA-CONOCIMIENTO.md`
5. `dispositivo/README.md`
6. `dispositivo/migracion/MIGRATION_AGENT_PROTOCOL_v1.md`
7. `dispositivo/migracion/MIGRATION_MANIFEST_v1.md`
8. `dispositivo/migracion/CURRENT_EXECUTABLE_STATE_v1.md`
9. `dispositivo/migracion/REENTRY_CHECKPOINT_2026-09-02.md`
10. los artefactos técnicos específicos que el trabajo actual requiera.

Para BIB065 y pedagogía, no tomar los artefactos técnicos como autoridad. Si el dispositivo detecta una consecuencia posible para Voces de las Nubes, registrarla como candidato y volver a la fuente original y al procedimiento de actualización del Sistema de Conocimiento.

## COR001

```text
COR001 = ANALYSIS_TARGET_ONLY
COR001 != GOLD_STANDARD
COR001 != BENCHMARK
COR001 != REGRESSION_AUTHORITY
COR001 != RULE_DISCOVERY_SOURCE
```

El replay histórico sirve exclusivamente para reproducibilidad técnica.

## Estado de separación física

A 2026-09-02 el dispositivo continúa materializado dentro del mismo repositorio por razones de genealogía y migración. La arquitectura vigente exige que esta coexistencia no se interprete como autoridad compartida.

La futura separación física en un repositorio técnico deberá preservar historia, hashes, replay y trazabilidad antes de retirar el dispositivo activo de este repositorio.
