# DEVICE_REPOSITORY_SEPARATION_PLAN_v1

**Estado:** `PHYSICAL_SPLIT_COMPLETE / REPLAY_PASS / INTEGRITY_HARDENED / PERMISSION_HARDENING_PENDING`  
**Versión interna:** 1.6  
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
TREE_IDENTITY_AT_INITIAL_IMPORT = PASS
```

La igualdad del SHA del subárbol Git demuestra que el snapshot inicial importado en `6d205ff` fue idéntico al árbol `dispositivo/` de origen.

Ese SHA no debe compararse contra el `HEAD` actual como si el subárbol tuviera que permanecer congelado. Después de la importación existen cambios técnicos y documentales legítimos, cada uno trazado por Git. La genealogía del snapshot original permanece intacta.

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

La verificación de la separación se documenta en la raíz de este repositorio:

`SEPARATION_VERIFICATION_2026-09-03.md`

El replay histórico continúa verificando:

```text
DEVICE_REPO_REPLAY = PASS
DEVICE_REPO_TECHNICAL_TESTS = PASS
HISTORICAL_RUNTIME_TEST_COUNT = 38
BAD_CLOSURE_HASHES = 0
BAD_DATA_HASHES = 0
SEMANTIC_HASHES_MATCH = true
DETERMINISTIC_SUMMARY_METRICS_MATCH = true
COR001 = ANALYSIS_TARGET_ONLY
```

Workflow permanente:

`.github/workflows/replay-v0-2-15-3.yml`

Desde el endurecimiento post-separación el workflow se ejecuta en:

```text
workflow_dispatch
push -> main
pull_request -> main
```

Además:

- `.gitattributes` protege con `-text` los nueve artefactos byte-críticos identificados;
- `RELEASE_MANIFEST_ANCHOR_v0_2_15_3.json` ancla la identidad del manifiesto v0.2.15.3;
- el workflow verifica su SHA-256 `5e3f7ff7035e8fdd6358ddae8432e37e52518cc9b50067dccfb7411c741f2304` y Git blob `e9cbb2062385e913d5acb59427aa6c1b53b54b14`;
- `dispositivo/migracion/test_migrated_state.py` forma parte de CI y pasa 8/8 verificaciones en el checkpoint post-separación;
- el conteo de 39 payloads presentes funciona como piso monotónico: nuevas recuperaciones exactas no vuelven obsoleta la prueba, pero una regresión por debajo de ese checkpoint falla.

El merge del Bloque 2 de endurecimiento quedó en `e6d501c839269b878c0ae99a82aed69071e108af`; su ejecución automática por `push` en `main` concluyó `success` (Run ID `33805988652`).

## Estado de Voces después del corte

`vocesdelasnubes/main` ya no contiene:

- el árbol activo `dispositivo/`;
- el workflow técnico del replay.

Su reentrada general apunta al repositorio técnico separado sólo cuando el trabajo sea explícitamente técnico. El conocimiento y las fuentes siguen siendo reconstruibles sin ejecutar el dispositivo.

## Estructura actual del repositorio técnico

El subdirectorio `dispositivo/` se mantiene por ahora dentro de este repositorio para preservar rutas históricas y evitar mezclar la separación física con un refactor de paths.

```text
didxaza-dispositivo/
├── README.md
├── REENTRY_TECNICO.md
├── KNOWLEDGE_SOURCE_PIN.md
├── MIGRATION_ORIGIN.md
├── RELEASE_MANIFEST_ANCHOR_v0_2_15_3.json
├── SEPARATION_VERIFICATION_2026-09-03.md
├── dispositivo/            # rutas técnicas heredadas + desarrollo post-split
└── .github/workflows/      # replay automático + manual
```

Un refactor futuro de esa estructura es una tarea técnica independiente y no debe cambiar autoridad ni procedencia.

## Único frente de separación todavía pendiente: permisos

La separación física de contenidos y el endurecimiento de integridad están completos. Queda endurecer permisos/rulesets para reflejar plenamente:

```text
vocesdelasnubes:
  knowledge curators = write
  device developers = read only by default

didxaza-dispositivo:
  approved device developers = write
```

`CODEOWNERS` por sí solo no constituye una barrera de escritura. El `CODEOWNERS` de Voces existe; este repositorio técnico todavía no tiene uno propio. La consulta del endpoint clásico de branch protection sigue devolviendo `403` para la integración disponible, y la consulta de rulesets de `didxaza-dispositivo` devolvió `[]` durante la revisión del 2026-09-03.

La configuración efectiva de branch protection/rulesets debe hacerse en GitHub con permisos suficientes antes de incorporar desarrolladores externos.

## Criterio de éxito

```text
DEVICE_REPO_REPLAY = PASS
DEVICE_REPO_TECHNICAL_TESTS = PASS
BYTE_EXACT_CRITICAL_FILES_PROTECTED = true
REPLAY_CI_ON_PUSH_AND_PR = true
MIGRATED_STATE_TEST_IN_CI = true
RELEASE_MANIFEST_ANCHORED = true
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
