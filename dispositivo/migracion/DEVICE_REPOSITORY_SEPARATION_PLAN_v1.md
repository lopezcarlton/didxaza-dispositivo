# DEVICE_REPOSITORY_SEPARATION_PLAN_v1

**Estado:** `PHYSICAL_SPLIT_COMPLETE / REPLAY_PASS / PERMISSION_HARDENING_PENDING`  
**Versión interna:** 1.5  
**Fecha:** 2026-09-03

## Resultado

La separación física del dispositivo respecto de `lopezcarlton/vocesdelasnubes` quedó ejecutada el 2026-09-03.

```text
KNOWLEDGE_REPOSITORY = lopezcarlton/vocesdelasnubes
DEVICE_REPOSITORY = lopezcarlton/didxaza-dispositivo
```

La separación implementa `DEC-AUTORIDAD-SISTEMA-CONOCIMIENTO`; no crea una autoridad nueva.

## Snapshot de origen e importación

```text
SOURCE_REPOSITORY = lopezcarlton/vocesdelasnubes
SOURCE_COMMIT = 22e3c088a97150453f28d03b31613ff9d9491d9a
SOURCE_DEVICE_TREE_SHA = d92c38ec45be4e2e3176b1cfe7c288321c887d3b
INITIAL_IMPORT_COMMIT = 6d205ffe0a0fe660229cd7a958fe43c9a5b51508
IMPORTED_DEVICE_TREE_SHA = d92c38ec45be4e2e3176b1cfe7c288321c887d3b
TREE_IDENTITY = PASS
```

La igualdad del SHA del subárbol Git demuestra que el snapshot inicial importado fue idéntico al árbol `dispositivo/` de origen.

El historial anterior a la separación sigue disponible en Git de Voces y el snapshot exacto permanece identificable por los commits anteriores. La retirada de `dispositivo/` de `vocesdelasnubes/main` no borró genealogía.

## Fuentes y autoridad

Las fuentes canónicas se identifican desde `lopezcarlton/vocesdelasnubes/conocimiento/fuentes/` mediante `SRC-*`.

```text
SOURCE_USED_BY_DEVICE != DEVICE_OWNED_KNOWLEDGE
SRC_RECORD = CANONICAL_SOURCE_IDENTITY
EXECUTABLE_DERIVATIVE = DEVICE
```

Toda ejecución o desarrollo reproducible debe registrar:

```text
KNOWLEDGE_SOURCE_REPOSITORY = lopezcarlton/vocesdelasnubes
KNOWLEDGE_SOURCE_COMMIT = <commit exacto>
```

El pin inicial de la separación está en `KNOWLEDGE_SOURCE_PIN.md`.

## Índice de recuperación pre-split

Antes del corte se creó en Voces:

`informes/KNOWLEDGE_RECOVERY_INDEX_PRE_SPLIT_2026-09-03.md`

Es un índice no autoritativo. Conserva coordenadas y temas de material histórico del dispositivo sin promoverlo a conocimiento.

```text
RECOVERY_INDEX_AS_COORDINATES = allowed
RECOVERY_INDEX_AS_CLAIM_SUMMARY = not_authoritative
SOURCE_PASSAGE_MUST_BE_READ_BEFORE_ADJUDICATION = true
MASS_ADJUDICATION_REQUIRED_BEFORE_SPLIT = false
```

## Verificación técnica

La verificación completa se documenta en la raíz de este repositorio:

`SEPARATION_VERIFICATION_2026-09-03.md`

Resultado:

```text
DEVICE_REPO_REPLAY = PASS
DEVICE_REPO_TECHNICAL_TESTS = PASS
TEST_COUNT = 38
BAD_CLOSURE_HASHES = 0
BAD_DATA_HASHES = 0
SEMANTIC_HASHES_MATCH = true
DETERMINISTIC_SUMMARY_METRICS_MATCH = true
COR001 = ANALYSIS_TARGET_ONLY
```

Workflow permanente:

`.github/workflows/replay-v0-2-15-3.yml`

El workflow quedó en `workflow_dispatch` manual únicamente.

## Estado de Voces después del corte

`vocesdelasnubes/main` ya no contiene:

- el árbol activo `dispositivo/`;
- el workflow técnico del replay.

Su reentrada general apunta al repositorio técnico separado sólo cuando el trabajo sea explícitamente técnico. El conocimiento y las fuentes siguen siendo reconstruibles sin ejecutar el dispositivo.

## Estructura inicial del repositorio técnico

El subdirectorio `dispositivo/` se mantiene por ahora dentro de este repositorio para preservar rutas históricas y evitar mezclar la separación física con un refactor de paths.

```text
didxaza-dispositivo/
├── README.md
├── REENTRY_TECNICO.md
├── KNOWLEDGE_SOURCE_PIN.md
├── MIGRATION_ORIGIN.md
├── SEPARATION_VERIFICATION_2026-09-03.md
├── dispositivo/            # snapshot/rutas técnicas heredadas
└── .github/workflows/      # replay manual histórico
```

Un refactor futuro de esa estructura es una tarea técnica independiente y no debe cambiar autoridad ni procedencia.

## Único frente de separación todavía pendiente: permisos

La separación física de contenidos está completa. Queda endurecer permisos/rulesets para reflejar plenamente:

```text
vocesdelasnubes:
  knowledge curators = write
  device developers = read only by default

didxaza-dispositivo:
  approved device developers = write
```

`CODEOWNERS` por sí solo no constituye una barrera de escritura. La configuración de branch protection/rulesets debe hacerse en GitHub cuando esté disponible.

## Criterio de éxito

```text
DEVICE_REPO_REPLAY = PASS
DEVICE_REPO_TECHNICAL_TESTS = PASS
KNOWLEDGE_SOURCE_COMMIT = EXPLICIT
CRITICAL_SOURCE_IDENTITY_UNRESOLVED = 0
RECOVERY_INDEX_AVAILABLE_FROM_VOCES = true
MASS_ADJUDICATION_REQUIRED_BEFORE_SPLIT = false
VOCES_REENTRY_DOES_NOT_REQUIRE_DEVICE_REPO = true
VOCES_CAN_RESOLVE_SHARED_SOURCES_WITHOUT_DEVICE_REPO = true
PHYSICAL_DEVICE_COPY_RETIRED_FROM_VOCES_MAIN = true
PERMISSION_HARDENING = pending
```

## Lo que esta separación no cambia

- no cambia P1–P5;
- no reabre BL-016;
- no convierte JLC, registries o matrices técnicas en fuentes canónicas;
- no convierte COR001 en benchmark/gold/regresión;
- no obliga a adjudicar conocimiento potencial antes de necesitarlo;
- no congela la investigación lingüística, pedagógica ni ortográfica de Voces.
