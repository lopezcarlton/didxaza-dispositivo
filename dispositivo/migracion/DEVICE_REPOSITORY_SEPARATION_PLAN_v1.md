# DEVICE_REPOSITORY_SEPARATION_PLAN_v1

**Estado:** `RECOVERY_INDEX_COMPLETE / WAITING_FOR_DEVICE_REPOSITORY`  
**Versión interna:** 1.4  
**Fecha:** 2026-09-03

## Objetivo

Separar físicamente el dispositivo del repositorio canónico de Voces de las Nubes sin perder genealogía, reproducibilidad ni acceso a las fuentes que lo alimentaron.

La separación implementa `DEC-AUTORIDAD-SISTEMA-CONOCIMIENTO`; no crea una nueva autoridad.

## Regla simple

Sólo existen dos dominios de autoridad:

```text
VOCES DE LAS NUBES = conocimiento + fuentes + decisiones
DISPOSITIVO = implementación derivada
```

No se crea un tercer sistema de acervo.

Las gramáticas, vocabularios, corpus, diccionarios, normas y bibliografía se identifican desde `conocimiento/fuentes/` mediante `SRC-*`. El payload puede vivir en el repositorio o en una ubicación externa/restringida según derechos y acceso.

El dispositivo conserva sus representaciones técnicas y los fixtures exactos necesarios para reproducibilidad.

```text
SOURCE_USED_BY_DEVICE != DEVICE_OWNED_KNOWLEDGE
SRC_RECORD = CANONICAL_SOURCE_IDENTITY
EXECUTABLE_DERIVATIVE = DEVICE
```

La decisión `DEC-AUTORIDAD-SISTEMA-CONOCIMIENTO` v1.1 añade además la obligación de reconstruibilidad: el conocimiento canónico de Voces debe poder justificarse sin ejecutar ni depender epistemológicamente del dispositivo.

## Baseline que debe preservarse

```text
repository = lopezcarlton/vocesdelasnubes
branch = checkpoint/pre-irma-post-migration-2026-09-02
commit = e1f9f4ef2852b9e0453ef757a291816e1faa10e2
```

Antes del corte, el nuevo repositorio técnico debe reproducir el cierre ya demostrado para runtime v0.2.15.3:

- dependencias históricas exactas necesarias;
- replay `exit 0`;
- hashes semánticos coincidentes;
- `SUMMARY` y `METRICS` deterministas exactos;
- 38/38 pruebas históricas;
- `COR001 = ANALYSIS_TARGET_ONLY`.

## Fase 0 — realizada

- frontera constitucional formalizada;
- `DEC-AUTORIDAD-SISTEMA-CONOCIMIENTO` vigente;
- reentrada general y técnica separadas;
- backlog técnico separado;
- provenance canónica hacia `dispositivo/` eliminada;
- `KNOWLEDGE_CONSUMPTION_CONTRACT_v1.md` activo;
- raíz del repositorio simplificada y sistemas derivados clasificados.

## Fase 1 — identidad y trazabilidad de fuentes críticas — realizada 2026-09-03

La revisión del core y del runtime muestra que las fuentes externas centrales materializadas o citadas por el dispositivo ya pueden resolverse desde Voces sin ejecutar el runtime.

Registros canónicos principales:

- `SRC-ALFABETO-POPULAR-1956` — `BIB015`, antecedente histórico ortográfico;
- `SRC-PICKETT-VILLALOBOS-MARLETT-2009-ZAPOTECO-ISTMO-JUCHITAN` — `BIB016`, ilustración fonética en español con audio;
- `SRC-PICKETT-BLACK-MARCIAL-2001-GRAMATICA-POPULAR` — Gramática Popular / `BIB004`;
- `SRC-PICKETT-2007-VOCABULARIO-ZAPOTECO-ISTMO` — Vocabulario / `BIB003`;
- `SRC-DICTIONARIA-DIDXAZA-SPANISH-ENGLISH-DICTIONARY` — `BIB054`, fuente de los inventarios Dictionaria y `DIC_VERB_2385`;
- `SRC-CATA-ETAL-2016-NORMA-ESCRITURA` — `BIB058`, identidad resuelta; manuscrito todavía por conseguir;
- `SRC-PEREZ-BAEZ-KAUFMAN-2016-VERB-CLASSES` — `BIB059`, clases verbales usadas por la capa PBK;
- `SRC-PEREZ-BAEZ-2015-VALENCE-CHANGING-JUCHITAN` — `BIB060`, cambio de valencia/causatividad;
- `SRC-PICKETT-VILLALOBOS-MARLETT-2010-PHONETICS` — `BIB061`, publicación JIPA;
- `SRC-CARDONA-2020-DIALECTOLOGIA-ZAPOTECO-ISTMO` — `BIB063`;
- `SRC-CARDONA-VICENTE-2025-VARIACION-ESCRITURA` — `BIB064`;
- `SRC-BUENO-HOLLE-2019` — `BIB065`, monografía, ubicación pública, DOI, licencia y hash de la copia de trabajo;
- `SRC-PEREZ-BAEZ-CATA-BUENO-HOLLE-2015-XNEZA` — `BIB017`, ortografía/palabra gráfica.

Comprobaciones de las capas técnicas recuperadas:

- `BOUND` cita `BIB004_GRAMATICA_POPULAR` y `BIB054_DICTIONARIA`;
- Morphology I cita `BIB059_PBK2016`, correspondiente al trabajo de Pérez Báez y Kaufman sobre clasificación verbal;
- Morphology II cita Dictionaria, PBK2016 y Pérez Báez 2015;
- `PERSON_POSSESSION_EXACT_REGISTRY` vuelve a `BIB004_GRAMATICA_POPULAR` con secciones/cuadros exactos;
- el backfill Pickett permanece derivado técnico del Vocabulario;
- `JUCHITAN_LINGUISTIC_CORE_v0_27` permanece compilación experimental y no fuente.

La hoja bibliográfica maestra fue reconciliada el 2026-09-03. La serie quedó continua hasta `BIB091`, sin huecos ni duplicados. `BL-026` quedó cerrado. Esto sustituye el uso provisional del snapshot BIB001–BIB084 como respaldo de asignaciones.

En el caso de Bueno Holle, las matrices técnicas históricas pueden usarse como coordenadas de recuperación, no como resumen autoritativo de lo que dice la fuente. Toda adjudicación debe volver al pasaje original.

No es requisito reingerir de golpe todo el contenido de estas obras. La lectura/adjudicación se hará incrementalmente cuando una pregunta de investigación lo requiera.

## Fase 1.5 — índice de recuperación pre-split — realizada 2026-09-03

Se creó:

`informes/KNOWLEDGE_RECOVERY_INDEX_PRE_SPLIT_2026-09-03.md`

El índice es deliberadamente **no normativo**. No adjudica, no promueve afirmaciones del dispositivo, no modifica `TEORIA.md` y no reabre `BL-016`.

Su función es preservar un mapa de recuperación de los principales artefactos técnicos que contienen formulaciones lingüísticas, pedagógicas u ortográficas que todavía pueden requerir relectura futura contra sus fuentes originales.

Cobertura principal:

- `JUCHITAN_LINGUISTIC_CORE_v0_27.md` completo;
- `BIB065_BUENO_HOLLE_INGESTION_MATRIX_v0_36_1.md`, 28 filas;
- `PEDAGOGICAL_DISCUSSION_FREEZE_POST_BIB065_v0_36_2.md`;
- `SINTESIS_ADVERSARIAL_ARQUITECTURA_DIDXAZA_v1_1_CORREGIDA.md`;
- `NUCLEO_CONVERSACIONAL_001_SCOPE_v1.md`;
- `PEDAGOGICAL_BACKLOG_BH2019_PARTIAL_v0_35.md`;
- `PERSON_POSSESSION_EXACT_REGISTRY_v0_2_15_2.csv`;
- `DOCUMENTARY_ALIGNMENT_REGISTRY_v0_2_15_2.csv`;
- `AdoptionRecords_v1.jsonl`, añadido durante la revisión porque conserva decisiones ortográficas técnicas históricas que no deben confundirse con `DEC` canónicas;
- datasets grandes Pickett/Dictionaria inventariados sólo de forma agregada y enlazados a sus `SRC`.

Regla de uso:

```text
RECOVERY_INDEX_AS_COORDINATES = allowed
RECOVERY_INDEX_AS_CLAIM_SUMMARY = not_authoritative
SOURCE_PASSAGE_MUST_BE_READ_BEFORE_ADJUDICATION = true
```

Para la matriz BIB065 se preservan literalmente sus `epistemic_status` y `promotion_status` como **etiquetas declaradas por el artefacto**. Para JLC y otros artefactos que no se auto-clasifican, las etiquetas del índice están marcadas como **asignadas por el inventario**, por lo que no deben confundirse con una clasificación de la fuente original.

Esta fase **no es una compuerta de adjudicación masiva**. Una formulación que vive sólo en el dispositivo y que Voces nunca ha adoptado se revisará contra su fuente original cuando una pregunta activa del proyecto la necesite. La separación física no exige convertirla previamente en HALL/TEO/DEC.

## Fase 2 — crear el repositorio técnico separado — bloqueada por infraestructura

Crear un repositorio técnico separado bajo el control de Emiliano y mover el árbol activo de `dispositivo/`, preservando en la medida posible historia y referencias al repo/commit de origen.

Debe contener como mínimo:

- Analyzer / Corrector / Tutor / Generator;
- runtime y bases ejecutables;
- tests;
- migración y estado técnico;
- `REENTRY_TECNICO.md`;
- `BACKLOG_TECNICO.md`;
- `KNOWLEDGE_CONSUMPTION_CONTRACT_v1.md`;
- workflow manual del replay histórico;
- prompts técnicos históricos.

**Bloqueo actual:** las herramientas disponibles en esta sesión permiten escribir dentro de repositorios existentes pero no crear un repositorio GitHub nuevo. No existe aún un repositorio técnico destino bajo `lopezcarlton`.

No utilizar `lopezcarlton/ELDP` como destino.

## Fase 3 — vincular el estado de Voces

Toda versión reproducible del dispositivo debe registrar:

```text
KNOWLEDGE_SOURCE_REPOSITORY = lopezcarlton/vocesdelasnubes
KNOWLEDGE_SOURCE_COMMIT = <commit exacto>
```

Cuando una compilación dependa de fuentes concretas, puede registrar además sus `SRC-*` correspondientes.

## Fase 4 — verificar antes del corte

En el repositorio técnico separado:

1. verificar artefactos críticos;
2. ejecutar replay histórico;
3. ejecutar 38 pruebas;
4. comprobar reentry técnico;
5. comprobar `KNOWLEDGE_SOURCE_COMMIT`;
6. comprobar que las fuentes documentales críticas pueden resolverse desde Voces sin depender del repo técnico;
7. comprobar que ninguna instrucción técnica conceda autoridad de escritura sobre Voces;
8. comprobar que el índice de recuperación pre-split permanezca accesible desde Voces como mapa histórico no normativo.

**No retirar el dispositivo activo de Voces hasta que esta fase pase.**

## Fase 5 — retirar la copia activa de Voces y aplicar permisos

Después de la verificación:

- retirar de `main` la copia activa de `dispositivo/` o dejar únicamente una referencia mínima;
- conservar la historia previa en Git y el baseline congelado;
- configurar el repositorio de Voces para que desarrolladores del dispositivo sean read-only por defecto;
- configurar el repositorio técnico con permisos propios de desarrollo.

`CODEOWNERS` documenta ownership, pero la frontera física sólo queda completa con permisos/rulesets adecuados.

## Criterio de éxito

```text
DEVICE_REPO_REPLAY = PASS
DEVICE_REPO_TECHNICAL_TESTS = PASS
KNOWLEDGE_SOURCE_COMMIT = EXPLICIT
CRITICAL_SOURCE_IDENTITY_UNRESOLVED = 0
RECOVERY_INDEX_AVAILABLE_FROM_VOCES = true
MASS_ADJUDICATION_REQUIRED_BEFORE_SPLIT = false
DEVICE_DEVELOPER_CANONICAL_WRITE_BY_DEFAULT = false
VOCES_REENTRY_DOES_NOT_REQUIRE_DEVICE_REPO = true
VOCES_CAN_RESOLVE_SHARED_SOURCES_WITHOUT_DEVICE_REPO = true
```

## Lo que este plan no autoriza

- no cambia P1–P5;
- no convierte una tabla técnica en fuente canónica;
- no publica materiales con derechos no verificados;
- no convierte el runtime histórico en arquitectura futura;
- no borra genealogía para simplificar el repositorio;
- no corta el dispositivo antes de verificar replay y pruebas;
- no obliga a adjudicar antes del split conocimiento potencial que Voces todavía no sostiene.
