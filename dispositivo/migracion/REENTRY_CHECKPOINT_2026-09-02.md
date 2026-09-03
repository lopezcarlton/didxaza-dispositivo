# REENTRY_CHECKPOINT_2026-09-02

**Proyecto:** Voces de las Nubes  
**Fecha:** 2026-09-02  
**Estado:** `HISTORICAL_CHAT_MIGRATION_SUFFICIENT / REENTRY_READY / MANIFEST_CONSOLIDATED / REPLAY_TECHNICALLY_REPRODUCED / NON_CANONICAL`

## 1. Función

Este checkpoint registra que la recuperación histórica desde chats del dispositivo ha llegado a un punto suficiente para continuar el proyecto desde GitHub sin seguir recorriendo conversaciones por defecto.

No reemplaza el Sistema de Conocimiento canónico ni convierte el estado técnico recuperado en autoridad lingüística o pedagógica.

```text
HISTORICAL_CHAT_MIGRATION_SUFFICIENT != ALL_HISTORICAL_PAYLOADS_RECOVERED
REPOSITORY_REENTRY_READY != RUNTIME_COMPLETE
TECHNICAL_REPLAY != LINGUISTIC_VALIDATION
```

## 2. Estado técnico materializado

Consultar como fuentes técnicas vigentes:

- `dispositivo/migracion/MIGRATION_MANIFEST_v1.md`
- `dispositivo/migracion/CURRENT_EXECUTABLE_STATE_v1.md`
- `dispositivo/migracion/REENTRY_CHECKPOINT_2026-09-02.md`

`dispositivo/ESTADO_ACTUAL_2026-08-31.md` se conserva únicamente como snapshot histórico previo a la migración y no prevalece sobre los tres documentos anteriores.

A este corte:

- runtime v0.2.15.3: subconjunto exacto materializado; replay histórico aislado reproducido con `TECHNICAL_REPRODUCIBILITY_PASS` y outputs deterministas exactos;
- segunda pasada limpia: checkout sin mutación previa, 17/17 módulos recursivos exactos, hashes semánticos completos coincidentes y 38/38 pruebas aprobadas;
- `CLEAN_REPLAY_VERIFICATION_v0_2_15_3.json` recuperado con identidad exacta como referencia histórica de esos hashes semánticos;
- Analyzer v0.35: subconjunto parcial no licenciante reproducible;
- Generator v0.5: fuente histórica + adaptador al layout migrado;
- Tutor v0.33: fuente presente, dependencias incompletas;
- NC001/core: artefactos principales migrados con genealogía;
- COR001: exclusivamente `ANALYSIS_TARGET_ONLY`.

## 3. BIB065 / Bueno Holle

La lectura intensiva de Bueno Holle 2019 está cerrada para esta pasada.

Estado:

`STUDIED_IN_DEPTH / HIGH_VALUE_DISCOURSE_SOURCE / NOT_NORMATIVE / PARTIALLY_EXECUTABLE`

Artefactos disponibles en el repositorio:

- `dispositivo/migracion/fuentes/BIB065_BUENO_HOLLE_INGESTION_MATRIX_v0_36_1.md`
- `dispositivo/migracion/fuentes/BIB065_BUENO_HOLLE_INGESTION_MATRIX_v0_36_1.csv`
- `dispositivo/migracion/fuentes/BH2019_READING_STATE_CLOSED_v0_36_1.md`
- `dispositivo/migracion/fuentes/BH2019_SOURCE_PROVENANCE_v0_36_1.json`
- `dispositivo/pedagogia/PEDAGOGICAL_DISCUSSION_FREEZE_POST_BIB065_v0_36_2.md`

La matriz CSV conserva identidad exacta verificada en GitHub y su estado ya está integrado en `MIGRATION_MANIFEST_v1.md`.

## 4. Guardrails recuperados

Quedan materializados para reentrada:

- `dispositivo/hardening/ANALYSIS_CAPABILITY_GUARDRAILS_v0_35.md`
- `dispositivo/development_corpus/DevelopmentCorpusProtocol_v0_35.md`

Protecciones centrales:

- la frase aislada sigue siendo una unidad válida de análisis;
- el contexto puede enriquecer, nunca bloquear el análisis local;
- `UNRESOLVED != INCORRECT`;
- frecuencia no equivale a gramaticalidad;
- ninguna fuente individual se convierte en gramática global;
- audio, transcripción y análisis permanecen en capas separadas;
- las propiedades discursivas/prosódicas pueden conservarse sin volverse campos obligatorios.

## 5. Pedagogía

El documento `dispositivo/pedagogia/PEDAGOGICAL_DISCUSSION_FREEZE_POST_BIB065_v0_36_2.md` es un insumo de discusión no normativo.

Debe conservarse explícitamente:

```text
COR002_BEGINNER_SCOPE = STRONG_WORKING_IDEA / DISCUSS
PEDAGOGICAL_ARTIFACT != STYLE_AUTHORITY
NC001_TECHNICAL_SCOPE != COR002_PEDAGOGICAL_SCOPE
```

No reescribe automáticamente COR002, P1–P5, Generator, Tutor o Analyzer.

El estado canónico de pedagogía sigue gobernado por `conocimiento/PEDAGOGIA.md` y las decisiones vigentes del Sistema de Conocimiento.

## 6. Pendientes que NO bloquean reentrada

No es necesario recuperar los 75 payloads históricos del runtime para seguir investigando.

Tampoco bloquean la reentrada:

- ZIPs históricos completos cuyo contenido textual relevante ya fue migrado;
- runners/reports COR001 históricos que sólo sirven a genealogía;
- artefactos explícitamente `ARCHIVE_ONLY` o `SUPERSEDED`;
- futuras reejecuciones manuales del replay v0.2.15.3, que ya obtuvo `PASS` técnico el 2026-09-02.

La evidencia del cierre está en `ISOLATED_REPLAY_VERIFICATION_v0_2_15_3_2026-09-02.md`. Un `PASS` no concede autoridad lingüística a COR001.

## 7. Cierre documental de reentrada

La reentrada desde GitHub está consolidada:

- `INICIAR_AQUI_CHAT_NUEVO.md` existe en la raíz y define el orden de lectura;
- `README.md` enlaza explícitamente ese entrypoint;
- se verificaron las rutas principales usadas por el entrypoint;
- las rutas BIB065 del estado v37.1 apuntan al layout real del repositorio;
- cierre, provenance, matriz Markdown/CSV y guardrails post-BIB065 están materializados;
- `MIGRATION_MANIFEST_v1.md` incorpora los artefactos que estaban temporalmente registrados en el addendum;
- el addendum deja de formar parte del estado operativo de reentrada.

No queda mantenimiento documental que obligue a volver a chats históricos.

## 8. Ruta de investigación activa

1. continuar literatura lingüística con la siguiente fuente pertinente;
2. iniciar/desarrollar corpus oral independiente de Juchitán, audio-first;
3. mantener COR002 como piloto pedagógico revisable orientado a principiantes;
4. contrastar literatura, hablantes, corpus oral y conocimiento existente;
5. promover conocimiento al dispositivo sólo según evidencia y autoridad explícitas;
6. no reabrir por defecto la cola caso por caso de COR001.
