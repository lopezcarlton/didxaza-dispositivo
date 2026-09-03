# P3_AUDIT_DISPOSITION_2026-09-03

**Estado:** `VERIFIED_DISPOSITION / NON_CANONICAL / TECHNICAL_ONLY`  
**Repositorio:** `lopezcarlton/didxaza-dispositivo`  
**Fecha:** 2026-09-03

## Propósito

Registrar la disposición de los hallazgos P3 recuperados de la auditoría técnica externa, verificándolos contra el repositorio actual antes de adoptar cambios.

Este documento no modifica autoridad lingüística, pedagógica, metodológica ni comunitaria. COR001 permanece `ANALYSIS_TARGET_ONLY`.

## P3-01 — rutas absolutas en `test_runtime_reuse.py`

**Verificación:** `CONFIRMED`.

El archivo archivado:

`migracion/fuentes/generator_v0_initial/test_runtime_reuse.py`

contiene rutas absolutas `/mnt/data/...` para el ZIP histórico y la SQLite. Por ello no es portable como prueba de un checkout actual.

**Disposición:** `ARCHIVE_LIMITATION_QUARANTINED / NO_IN_PLACE_REWRITE`.

El subárbol `generator_v0_initial/` está clasificado por `MIGRATION_MANIFEST_v1.md` como `ARCHIVE_ONLY / SUPERSEDED`. Se añadió `generator_v0_initial/README.md` para hacer explícito que estos `test_*.py` no pertenecen a la suite activa.

No se reescribió el archivo histórico. Si la propiedad necesita cobertura actual, debe implementarse una prueba nueva fuera del archivo histórico.

## P3-02 — script `test_adjudication_v0_2.py` con 0 unittest cases

**Verificación:** `CONFIRMED`.

El archivo:

`migracion/fuentes/mvp_vertical_slice_v0_2/test_adjudication_v0_2.py`

ejecuta asserts a nivel de módulo y, al completarlos, imprime `PASS: adjudication invariants preserved`. No define `unittest.TestCase` ni métodos de prueba unittest.

**Disposición:** `ARCHIVE_TEST_SEMANTICS_CLARIFIED / NO_IN_PLACE_REWRITE`.

`MIGRATION_MANIFEST_v1.md` clasifica `mvp_vertical_slice_v0_2/` como `ARCHIVE_ONLY / NON_AUTHORITY`. Su README fue ampliado para impedir que el texto `PASS` sea interpretado como CI actual, conteo unittest mayor que cero o validación lingüística.

## P3-03 — `test_generator_v0.py` depende del layout histórico incompleto

**Verificación:** `CONFIRMED`.

`test_generator_v0.py` instancia directamente `LicensedGeneratorV0()` y hereda el layout histórico del scaffold archivado. Ese layout no contiene todas las dependencias que el entrypoint original espera en sus rutas históricas.

**Disposición:** `ARCHIVE_LIMITATION_QUARANTINED / CURRENT_ADAPTER_TESTED_SEPARATELY`.

No se reparó el test archivado. El estado ejecutable actual del Generator se representa mediante `generator/generator_v0_5_migrated_adapter.py` y su subconjunto reproducible se prueba desde `migracion/test_migrated_state.py`.

## P3-04 — ausencia de `.gitignore`

**Verificación contra HEAD actual:** `RESOLVED_BEFORE_P3_BLOCK`.

`.gitignore` ya fue añadido durante P2 con alcance conservador. Excluye artefactos locales/cachés/entornos, sin ignorar globalmente CSV, JSON/JSONL, SQLite, ZIP, Markdown u otros formatos de estado histórico/técnico.

## P3-05 — GitHub Actions por tag móvil

**Verificación:** `CONFIRMED`.

El workflow vigente usaba:

```text
actions/checkout@v4
actions/upload-artifact@v4
```

Los tags `v4` se verificaron el 2026-09-03 contra GitHub y resolvían respectivamente a:

```text
actions/checkout = 11d5960a326750d5838078e36cf38b85af677262
actions/upload-artifact = ea165f8d65b6e75b540449e92b4886f43607fa02
```

**Disposición:** `REPAIRED_BY_EXACT_SHA_PIN`.

El workflow actual fija esas identidades exactas y conserva comentarios `# v4` sólo como referencia humana. La funcionalidad no se amplió por este cambio.

## P3-06 — nombre histórico `verificador de ortografía` y diagnóstico truncado

**Fuente recuperada:** `PARTIAL_SOURCE_ONLY`.

La porción disponible de la auditoría dice únicamente que existe un “Nombre de archivo con espacio y carácter no ASCII (`verificador de ortografía`), sin …”. El resto del diagnóstico y su remediación propuesta no están disponibles en la fuente recuperada.

No es válido reconstruir lo omitido por inferencia.

**Hecho verificable relacionado:** el archivo existe con ese nombre histórico y fue puesto previamente en cuarentena mediante `prompts/historicos/README.md`, sin renombrarlo ni modificar su blob.

**Disposición:** `PARTIALLY_ADDRESSED / FULL_FINDING_NOT_RECOVERED / DO_NOT_CLAIM_CLOSED`.

Si aparece la auditoría completa, P3-06 debe reevaluarse desde su texto real.

## Resumen

```text
P3-01 = CONFIRMED / ARCHIVE_QUARANTINED
P3-02 = CONFIRMED / ARCHIVE_TEST_SEMANTICS_CLARIFIED
P3-03 = CONFIRMED / ARCHIVE_QUARANTINED
P3-04 = RESOLVED_BEFORE_P3_BLOCK
P3-05 = CONFIRMED / EXACT_SHA_PIN_APPLIED
P3-06 = PARTIAL_SOURCE_ONLY / NOT_CLOSED
```

Ninguna disposición P3 convierte un artefacto histórico en autoridad actual ni sustituye la fuente canónica de conocimiento `lopezcarlton/vocesdelasnubes`.
