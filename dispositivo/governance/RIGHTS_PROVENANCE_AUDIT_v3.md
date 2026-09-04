# RIGHTS_PROVENANCE_AUDIT_v3 — DT-004 checkpoint

**Estado:** `PARTIAL_RIGHTS_AUDIT / V2_19_AND_REPLAY_RESIDUALS_MAPPED / DISTRIBUTION_ARCHITECTURE_PENDING / NON_LEGAL_DETERMINATION`  
**Fecha:** 2026-09-03  
**Reemplaza para planificación actual:** `RIGHTS_PROVENANCE_AUDIT_v2.md`  
**Licencia global:** `BLOCKED_PENDING_RIGHTS_AND_DISTRIBUTION_ARCHITECTURE`

## 1. Qué cambió desde v2

La fase anterior dejó mapeada la SQLite v2.20, materializó el NOTICE de terceros y resolvió de forma no destructiva el hueco histórico de `source_profile`.

Esta pasada cierra dos residuales técnicos adicionales:

1. auditoría de provenance a nivel tabla de `BASE_CORRECTOR_DIDXAZA_EVIDENCE_INTEGRITY_v2_19.sqlite`;
2. auditoría estructural/de derechos de seis artefactos COR001/replay almacenados, sin emitir valores lingüísticos ni usar COR001 como benchmark, regresión o fuente de reglas.

El estado actual de COR001 sigue siendo:

```text
COR001 = ANALYSIS_TARGET_ONLY
COR001 != GOLD_STANDARD
COR001 != BENCHMARK
COR001 != REGRESSION_AUTHORITY
COR001 != RULE_DISCOVERY_SOURCE
```

## 2. SQLite v2.19

Artefacto auditado:

```text
BASE_CORRECTOR_DIDXAZA_EVIDENCE_INTEGRITY_v2_19.sqlite
SHA256 = c0433ff9a97fa8d4fb3d1ae5efc859b4ef2eacff1da92396fc5e8c22ff0215f4
integrity_check = ok
tables = 83
provenance_metadata_columns = 48
```

La auditoría read-only confirma que las tablas source-bearing compartidas con v2.20 tienen **las mismas firmas de provenance y los mismos conteos** para los campos auditados.

Entre ellas:

```text
BIB054_DICTIONARIA
  verb_lexeme_class_v023    = 2,385
  bound_entry_v024          = 6,600
  causative_inventory_v025  =   869
  derivation_inventory_v025 = 1,064
  surface_attestation_v029  =84,188

BIB003_PICKETT_VOCABULARIO
  pickett_lexical_record_v0211 = 2,534

BIB003 + BIB054
  cross_source_exact_surface_v0212 = 1,118

BIB004_GRAMATICA_POPULAR
  documentary_alignment_v0210 = 131
  person_possession_exact_v0214 = 100

BIB055_PICKETT_VOCABULARIO
  documentary_alignment_v0210 = 16

BIB059_PBK2016
  morphology_rule_registry_v023 = 11
```

Respecto de v2.19, v2.20 añade únicamente dos tablas:

```text
canonical_state_v17 = 22 filas
surface_semantics_integrity_v0153 = 7 filas
```

Además `schema_migration_log` pasa de 17 a 18 filas. No apareció una nueva familia externa source-bearing en v2.19 que altere el mapa de derechos ya identificado para las tablas compartidas.

Mapa materializado:

`SQLITE_V2_19_RIGHTS_SOURCE_MAP_v1.json`.

**Conclusión técnica de derechos:** la SQLite v2.19 hereda para sus tablas source-bearing compartidas los mismos límites de distribución que ya fueron identificados para Dictionaria, Pickett, Gramática Popular y PBK2016. Esto no convierte ambos binarios en equivalentes ni decide copyright a nivel de campo; evita repetir una falsa incertidumbre sobre sus familias de fuentes.

## 3. Auditoría de artefactos COR001/replay

La auditoría vigente usa clasificación Unicode normalizada (`NFKD`) de nombres de campos y no emite valores de contenido.

Evidencia de CI:

```text
workflow = rights-provenance-audit
run_id   = 33819805688
head_sha = 54a52eb5154645f1d14132bb6f67e9a98c2cc9cd
status   = success
content_values_emitted = false
```

Se auditaron seis artefactos y no faltó ninguno.

### 3.1 Artefactos con texto directo COR001

`COR001_REPLAY_INPUT_v0_2_15_2.csv`

```text
rows = 107
schema includes Español + Didxazá_original
rights/license metadata fields in artifact = none detected
```

`COR001_REPLAY_SUMMARY_v0_2_15_2.csv`

```text
rows = 107
schema includes Español + Didxazá_original
also contains derived action/review/validation fields
rights/license metadata fields in artifact = none detected
```

`COR001_REPLAY_DETAILED_v0_2_15_2.jsonl`

```text
rows = 107
schema contains spanish + didxaza_original + derived analysis/decision fields
source_coverage_metadata contains BIB054_DICTIONARIA as a mapping key
```

Estos tres son **content-bearing**. Su mera presencia en un release histórico no concede una licencia de redistribución abierta.

### 3.2 Artefactos técnicos/agregados sin campos directos de texto del corpus detectados

`COR001_REPLAY_METRICS_v0_2_15_2.json` contiene métricas agregadas, conteos y versión del runtime. El auditor no detectó campos directos `Español`/`Didxazá_original` o equivalentes de texto del corpus.

`RUN_MANIFEST_COR001_v0_2_15_2.json` contiene hashes, entorno, flags y políticas técnicas; no contiene campos directos de texto del corpus.

`CLEAN_REPLAY_VERIFICATION_v0_2_15_3.json` contiene estado técnico y hashes semánticos; no contiene campos directos de texto del corpus.

Esto reduce su riesgo relativo de redistribución respecto de los outputs text-bearing, pero **no los declara automáticamente open-source**: todavía hay que resolver el alcance autoral/licenciable del código y metadatos producidos por el proyecto.

Mapa materializado:

`REPLAY_ARTIFACT_RIGHTS_MAP_v1.json`.

## 4. Qué dice Voces sobre audio y participación

La autoridad de conocimiento actual, `lopezcarlton/vocesdelasnubes/conocimiento/AUDIO.md`, documenta que:

- las personas hablantes participan como productoras del contenido oral y validadoras de naturalidad dentro del alcance de cada sesión;
- el proyecto conserva el registro primario y puede generar varios derivados;
- el flujo completo de publicación y distribución de todos los derivados todavía no está documentado de forma definitiva.

El documento no fija por sí mismo una licencia o cesión de redistribución para COR001.

Por tanto:

```text
NO_RIGHTS_METADATA_IN_REPLAY_ARTIFACT != NO_PERMISSION_EXISTS
SPEAKER_PARTICIPATION_DOCUMENTED != OPEN_REDISTRIBUTION_LICENSE
COR001_TEXT_BEARING_DISTRIBUTION = HOLD_PENDING_EXPLICIT_RIGHTS_PROVENANCE
```

La acción correcta no es editar los CSV/JSONL históricos para insertar una licencia retrospectiva. Debe existir un registro autoritativo de derechos/provenance en Voces de las Nubes y, después, una política de packaging en el repositorio técnico que lo consuma.

## 5. Estado de DT-004 después de esta pasada

```text
INITIAL_RIGHTS_INVENTORY = DONE
V2_20_TABLE_LEVEL_SOURCE_MAP = DONE
V2_19_TABLE_LEVEL_SOURCE_MAP = DONE
DICTIONARIA_NOTICE = MATERIALIZED
BIB004_IDENTITY_AND_RIGHTS_NOTICE = VERIFIED
BIB059_IDENTITY_AND_RIGHTS_NOTICE = VERIFIED
SOURCE_PROFILE_NON_DESTRUCTIVE_SUPPLEMENT = MATERIALIZED
STORED_REPLAY_RIGHTS_SCHEMA_MAP = DONE
COR001_TEXT_BEARING_ARTIFACTS = IDENTIFIED
COR001_AUTHORITATIVE_RIGHTS_PROVENANCE = OPEN
PICKETT_BIB003_BIB055_GENEALOGY = OPEN
PROJECT_AUTHORED_SCOPE_INVENTORY = OPEN
DISTRIBUTION_ARCHITECTURE = OPEN
BLANKET_LICENSE = BLOCKED
```

## 6. Siguiente prioridad

El cuello de botella ya no es descubrir fuentes dentro del runtime. Quedan tres frentes con valor real:

1. materializar en Voces de las Nubes un estado autoritativo de rights/provenance para COR001 y futuros registros humanos, sin inferir consentimiento retroactivamente;
2. separar qué código/documentación de `didxaza-dispositivo` es originalmente licenciable por el proyecto frente a archivos source-derived/históricos;
3. diseñar la arquitectura de distribución final: qué puede entrar en un paquete abierto, qué requiere NOTICE/atribución, qué debe excluirse o distribuirse por separado y qué licencias concretas aplican a cada scope.

Hasta entonces no añadir `LICENSE` global.
