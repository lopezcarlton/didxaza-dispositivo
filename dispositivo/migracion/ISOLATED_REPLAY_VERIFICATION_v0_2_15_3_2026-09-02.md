# ISOLATED_REPLAY_VERIFICATION_v0_2_15_3 — 2026-09-02

**Proyecto:** Voces de las Nubes  
**Estado:** `TECHNICAL_REPRODUCIBILITY_PASS / NON_CANONICAL / NON_LINGUISTIC_AUTHORITY`

## 1. Alcance

Esta verificación documenta dos ejecuciones complementarias del runner histórico `run_cor001_replay_v0_2_15_3.py`. La primera detectó y reparó una normalización de transporte antes del replay; la segunda ejecutó el estado final de `main` desde un checkout sin mutación previa. Se comparan identidades de release, clausura recursiva de imports, hashes semánticos, outputs deterministas y pruebas históricas.

No es una evaluación lingüística de COR001 y no modifica su rol:

```text
COR001 = ANALYSIS_TARGET_ONLY
COR001 != GOLD_STANDARD
COR001 != BENCHMARK
COR001 != REGRESSION_AUTHORITY
COR001 != RULE_DISCOVERY_SOURCE
```

## 2. Ejecución inicial de reparación y cierre

GitHub Actions:

```text
workflow = replay-v0-2-15-3-reproducibility
run_id = 33680809372
job_id = 100416640022
head_sha = feb0a994f877f22f680a849a5cdda605208348f6
runner = Ubuntu 24.04 / Python 3.12.3
result = SUCCESS
```

Criterio del replay:

```text
runner_exit_0
+ exact_direct_dependencies
+ exact_deterministic_outputs
```

Resultado:

```text
STATUS = PASS
DIRECT_DEPENDENCIES_OK = true
DETERMINISTIC_OUTPUTS_OK = true
```

Esta ejecución partió de un checkout limpio, pero **reparó el registry de persona/posesión dentro del worktree antes de lanzar el replay** y luego publicó esa reparación. Por ello se conserva como cierre de reparación, no como la demostración más fuerte de un replay inmutable del `main` final.

### 2.1 Segunda pasada limpia sobre el estado final

```text
workflow = second-pass-clean-replay-audit-v2
run_id = 33682539100
job_id = 100422262288
head_sha = 4edf9dcde8ad86025b319b6e3a78e3fb3a173a9c
runner = Ubuntu 24.04 / Python 3.12.3
checkout_mutated_before_replay = false
result = SUCCESS
```

La segunda pasada verificó:

```text
ENTRYPOINT_PATHS = 23/23
RECURSIVE_IMPORT_CLOSURE = 17/17 exactos
DATA_DEPENDENCIES = 8/8 exactas
REPLAY_EXIT_CODE = 0
SEMANTIC_HASHES_MATCH = true
DETERMINISTIC_OUTPUTS_MATCH = true
UNITTEST = 38/38 PASS
```

Esta segunda ejecución es la evidencia principal de reproducibilidad del estado final materializado.

## 3. Discrepancia de transporte detectada y reparada

La primera ejecución aislada encontró una única discrepancia entre una dependencia migrada y el hash del release:

```text
PERSON_POSSESSION_EXACT_REGISTRY_v0_2_15_2.csv
migrated SHA256 = 4eb026a6e6b713dec9eeee804a376d3e75884addbfb10096e3fc881adbc85ac7
release SHA256  = 3f1e955a285c2ce9c66d3953def6b41fd993d6b8dd81567c5f95a28281d20bdb
```

El diagnóstico exhaustivo de representación demostró que el contenido tabular era el mismo y que la diferencia provenía únicamente de terminadores de línea:

```text
migrated representation = UTF-8 BOM + LF + final newline
release representation  = UTF-8 BOM + CRLF + final newline
```

La variante `UTF-8 BOM + CRLF + final newline` reprodujo exactamente el SHA-256 histórico del release. No se alteró ninguna celda ni decisión lingüística.

La representación byte-exacta se restauró y se publicó en `main` mediante:

```text
commit = 44e8b04
message = restore exact person-possession registry bytes v0.2.15.2
verified SHA256 = 3f1e955a285c2ce9c66d3953def6b41fd993d6b8dd81567c5f95a28281d20bdb
```

## 4. Outputs reproducidos

Los outputs deterministas del replay coinciden byte por byte con el release histórico:

```text
COR001_REPLAY_METRICS_v0_2_15_3.json
SHA256 = d7184c94af1eff07b54c63ab3da5e83f81e037342265ba8e20a74dbf0dd0bd22
EXACT_MATCH = true

COR001_REPLAY_SUMMARY_v0_2_15_3.csv
SHA256 = ce4b799d9cb800eea9e220a3166fcf532246ac9e92f6ec000a36f7f9e0fb06b4
EXACT_MATCH = true
```

El `COR001_REPLAY_DETAILED_v0_2_15_3.jsonl` no coincide byte por byte porque contiene identificadores UUID efímeros generados en cada ejecución. Esa diferencia no se usa como criterio de fallo. El runner produjo los siguientes hashes semánticos en la ejecución de cierre:

```text
details = eb68bb9a4a3d21e59fa889c5d214f6a7d108c54df228741a2920bec14f5d3d46
metrics = 336db0939a8712b101766f28ebdd841936d8c539736820510c881cf1dbb47dec
summary = adf75622ec8062b74826535a39ab50ced989e3390bf5e88ad19738d56bb13fa5
```

Estos tres valores coinciden exactamente con `CLEAN_REPLAY_VERIFICATION_v0_2_15_3.json`, ahora recuperado con identidad byte-exacta del release:

```text
SHA256 = 0446768fa8ec1d6e76937688c62e8aa667e7503d211070988944c44253b36644
SEMANTIC_HASHES_MATCH = true
TESTS = 38/38 PASS
```

## 5. Conclusión técnica

El subconjunto materializado del runtime v0.2.15.3 es suficiente para regenerar el replay histórico aislado y reproducir exactamente sus outputs deterministas relevantes.

Esto permite cerrar el pendiente de **reproducibilidad técnica del replay v0.2.15.3**.

No demuestra:

- que COR001 sea lingüísticamente correcto;
- que COR001 pueda servir como benchmark o regresión;
- que las salidas del runtime constituyan reglas;
- que los 75 payloads del release estén migrados;
- que el runtime histórico deba convertirse en la arquitectura futura del proyecto.

El workflow debe conservarse únicamente como herramienta manual de reproducibilidad histórica, no como gate automático sobre cambios futuros.
