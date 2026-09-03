# SEPARATION VERIFICATION — 2026-09-03

**Estado:** `PASS / PHYSICAL_SPLIT_COMPLETE / DEVICE_SNAPSHOT_VERIFIED`

## Identidad de origen

```text
SOURCE_REPOSITORY = lopezcarlton/vocesdelasnubes
SOURCE_COMMIT = 22e3c088a97150453f28d03b31613ff9d9491d9a
SOURCE_DEVICE_TREE_SHA = d92c38ec45be4e2e3176b1cfe7c288321c887d3b
```

## Identidad de importación

```text
DESTINATION_REPOSITORY = lopezcarlton/didxaza-dispositivo
INITIAL_IMPORT_COMMIT = 6d205ffe0a0fe660229cd7a958fe43c9a5b51508
IMPORTED_DEVICE_TREE_SHA = d92c38ec45be4e2e3176b1cfe7c288321c887d3b
TREE_IDENTITY = PASS
```

La igualdad del SHA del subárbol Git demuestra identidad del árbol `dispositivo/` importado respecto del árbol de origen: mismos blobs, modos, nombres y estructura.

## Replay y pruebas

Workflow: `replay-v0-2-15-3-reproducibility`  
Run ID: `33799819789`  
Head SHA verificado: `da99157c70901b2a92afc5d5421a2ab89ea40923`  
Conclusión GitHub Actions: `success`

Resultado interno:

```text
status = PASS
cor001_policy = ANALYSIS_TARGET_ONLY
replay_exit_code = 0
bad_closure_hashes = {}
bad_data_hashes = {}
semantic_hashes_match = true
deterministic_outputs_match = true
unittest_count = 38
tests_38_pass = true
unittest_exit_code = 0
recursive_import_closure_count = 17
```

El detalle JSONL no fue byte-exacto y el workflow declara explícitamente `detailed_byte_exact_required = false`; los hashes semánticos sí coincidieron y SUMMARY/METRICS fueron deterministas exactos.

### Hashes deterministas

```text
COR001_REPLAY_METRICS_v0_2_15_3.json
= d7184c94af1eff07b54c63ab3da5e83f81e037342265ba8e20a74dbf0dd0bd22

COR001_REPLAY_SUMMARY_v0_2_15_3.csv
= ce4b799d9cb800eea9e220a3166fcf532246ac9e92f6ec000a36f7f9e0fb06b4
```

### Hashes semánticos

```text
details = eb68bb9a4a3d21e59fa889c5d214f6a7d108c54df228741a2920bec14f5d3d46
metrics = 336db0939a8712b101766f28ebdd841936d8c539736820510c881cf1dbb47dec
summary = adf75622ec8062b74826535a39ab50ced989e3390bf5e88ad19738d56bb13fa5
```

## Evidencia de Actions

```text
ARTIFACT_ID = 9910606165
ARTIFACT_ZIP_SHA256 = 57b4aaec79c2b997300cf188450a23e8784aab85ad1d7bf206950d842ee4d7a4
```

## Knowledge pin

El repositorio técnico declara explícitamente:

```text
KNOWLEDGE_SOURCE_REPOSITORY = lopezcarlton/vocesdelasnubes
KNOWLEDGE_SOURCE_COMMIT = 22e3c088a97150453f28d03b31613ff9d9491d9a
```

La rama móvil `main` de Voces puede consultarse para descubrimiento; una ejecución reproducible debe fijar el commit real consumido.

## Cierre físico en Voces

Las condiciones previas fueron satisfechas y la copia activa fue retirada.

```text
VOCES_SPLIT_COMMIT = 67aabe3ed34bc04165583f7cb45cc610f619ebc0
VOCES_INITIAL_POST_CLEANUP_COMMIT = 4ba3596e2a4096254a70a29c23bc3f007451640b
VOCES_FINAL_POST_SPLIT_COMMIT = eb081b7c40ade6e017bc6ea1ac714a15461b6070
PHYSICAL_DEVICE_COPY_RETIRED_FROM_VOCES_MAIN = true
VOCES_TECHNICAL_REPLAY_WORKFLOW_REMOVED = true
VOCES_TEMPORARY_SPLIT_WORKFLOWS_REMOVED = true
ARCHITECTURE_PHYSICAL_STATE_PATCH = 0.3.1
```

En el árbol raíz final de `vocesdelasnubes/main` no existe `dispositivo/`. Dentro de `.github/` sólo permanece `CODEOWNERS`; no hay workflows técnicos activos.

La historia Git de Voces y los commits previos preservan la genealogía. Retirar la copia activa no borró el dispositivo histórico.

## Estado residual

La separación física y la reproducibilidad están completas. Queda como configuración independiente el endurecimiento de permisos mediante branch protection/rulesets. Ambas ramas `main` continúan actualmente sin protección de rama; `CODEOWNERS` no sustituye esa barrera.
