# generator_v0_initial — archivo histórico

**Estado de este subárbol:** `ARCHIVE_ONLY / SUPERSEDED / NOT_ACTIVE_TEST_SUITE / NON_KNOWLEDGE_AUTHORITY`

Este directorio conserva el scaffold inicial de Generator_v0 y sus pruebas tal como fueron recuperados durante la migración. `MIGRATION_MANIFEST_v1.md` clasifica el subárbol completo como `ARCHIVE_ONLY / SUPERSEDED`.

Su contenido no define el Generator ejecutable actual y sus archivos `test_*.py` no forman parte de la suite técnica activa del repositorio.

## Limitaciones históricas verificadas

### `test_runtime_reuse.py`

El archivo preservado contiene rutas absolutas al entorno histórico:

```text
/mnt/data/didxaza_v0_2_15_3_surface_semantics_resolution_integrity_CLOSED_PASS(1).zip
/mnt/data/BASE_CORRECTOR_DIDXAZA_SURFACE_SEMANTICS_v2_20(1).sqlite
```

Por ello no es una prueba portable del checkout actual. No modificar esas rutas dentro del artefacto archivado sólo para hacerlo pasar.

### `test_generator_v0.py`

La prueba instancia directamente `LicensedGeneratorV0()` y depende del layout histórico de inputs. Ese layout recuperado no contiene todas las dependencias esperadas por el entrypoint original, incluido el `ParadigmTable_v1.csv` en la ruta histórica esperada.

Esto no contradice el estado actual del Generator: el subconjunto migrado reproducible se instancia mediante `dispositivo/generator/generator_v0_5_migrated_adapter.py` y se comprueba desde `dispositivo/migracion/test_migrated_state.py`.

## Regla

```text
ARCHIVED_TEST_NAME != ACTIVE_TEST
HISTORICAL_PASS_TEXT != CURRENT_CI_PASS
ARCHIVED_LAYOUT != CURRENT_EXECUTABLE_LAYOUT
ARCHIVED_ARTIFACT != KNOWLEDGE_AUTHORITY
```

Si en el futuro se necesita reactivar una propiedad comprobada por estas pruebas, crear una prueba o adaptador nuevo fuera de este subárbol y conectarlo a las rutas actuales de manera explícita. Mantener los archivos archivados sin reescritura para preservar genealogía.
