# DISPOSITIVO LINGÜÍSTICO — CAPA EXPERIMENTAL DERIVADA

**Repositorio:** `lopezcarlton/didxaza-dispositivo`  
**Sistema de conocimiento autoritativo:** `lopezcarlton/vocesdelasnubes`  
**Estado:** `DERIVED_SYSTEM / NON_CANONICAL / EXPERIMENTAL / PHYSICALLY_SEPARATED`  
**Fecha de creación:** 2026-08-31  
**Frontera de autoridad sincronizada:** 2026-09-03

## Reentrada técnica

Para trabajo explícitamente técnico sobre Analyzer, Corrector, Tutor, Generator, runtime, tests, schemas o migración, iniciar en:

`../REENTRY_TECNICO.md`

La reentrada general de Voces de las Nubes vive en el repositorio autoritativo:

`lopezcarlton/vocesdelasnubes/INICIAR_AQUI_CHAT_NUEVO.md`

Este repositorio técnico no contiene `conocimiento/` ni sustituye esa reentrada.

## Propósito

Esta carpeta conserva el trabajo técnico desarrollado para convertir conocimiento aprobado del proyecto en capacidades operativas de:

- análisis;
- revisión y normalización;
- explicación pedagógica;
- producción controlada de estímulos y materiales.

También preserva genealogía, hipótesis ejecutables, estados históricos y capacidad reproducible de investigación técnica.

## Regla fundamental de autoridad

**`didxaza-dispositivo` no es una segunda fuente de verdad lingüística, pedagógica, metodológica ni comunitaria.**

El Sistema de Conocimiento permanece exclusivamente en `lopezcarlton/vocesdelasnubes`. Las reglas vigentes de autoridad se consultan allí, especialmente:

- `00_ARQUITECTURA_DEL_CONOCIMIENTO.md`;
- `01_JERARQUIA_DE_VERDAD.md`;
- `03_REGLAS_DE_ACTUALIZACIÓN.md`;
- `conocimiento/decisiones/DEC-AUTORIDAD-SISTEMA-CONOCIMIENTO.md`.

El contrato técnico local es `KNOWLEDGE_CONSUMPTION_CONTRACT_v1.md`.

```text
DEVICE_MAY_READ = true
DEVICE_MAY_ANALYZE = true
DEVICE_MAY_PROPOSE = true
DEVICE_MAY_CHALLENGE = true

DEVICE_MAY_ADOPT_KNOWLEDGE = false
DEVICE_MAY_PROMOTE_CANDIDATE = false
DEVICE_MAY_WRITE_KNOWLEDGE = false
```

Una persona o agente trabajando como desarrollador del dispositivo tampoco adquiere autoridad sobre el Sistema de Conocimiento por tener capacidad técnica para analizarlo.

Los futuros desarrolladores del dispositivo no deben tener por defecto permisos de escritura sobre `vocesdelasnubes`. La separación física ya está hecha; el endurecimiento adicional mediante branch protection/rulesets sigue pendiente como configuración de GitHub. El `CODEOWNERS` de Voces documenta ownership, pero no sustituye una barrera de permisos. Este repositorio técnico todavía no declara un `CODEOWNERS` propio.

## Flujo correcto de descubrimientos

El dispositivo puede localizar un problema real. Eso no obliga a ignorarlo; obliga a devolverlo por la vía correcta.

```text
DISPOSITIVO_DETECTA_X
-> identifica la fuente original o evidencia pertinente
-> devuelve candidato / contradicción / requisito
-> Voces de las Nubes registra la entidad correspondiente
-> adjudica con autoridad pertinente
-> adopta mediante DEC cuando corresponda
-> actualiza las vistas canónicas
-> el dispositivo consume después el nuevo estado aprobado
```

Nunca:

```text
DISPOSITIVO_DETECTA_X
-> EDITA_DIRECTAMENTE_PEDAGOGIA_TEORIA_CORPUS_METODOLOGIA
```

Un resultado técnico puede ser evidencia válida sobre **el comportamiento del dispositivo**. No se convierte por ello en evidencia lingüística, pedagógica o comunitaria.

## Investigación abierta

El principio de investigación abierta se consulta en:

`lopezcarlton/vocesdelasnubes/conocimiento/principios/PRIN-INVESTIGACION-ABIERTA.md`

La función del dispositivo es ampliar la capacidad de investigar, no cerrar la investigación. Una representación implementada puede ser provisional, quedar superseded, ser útil sólo para una prueba o necesitar revisión posterior.

```text
IMPLEMENTED_CAPABILITY != RESEARCH_AUTHORITY
MIGRATED_ARTIFACT != IMMUTABLE_RULE
CURRENT_RUNTIME != FINAL_ARCHITECTURE
UNRESOLVED != INCORRECT
```

La reproducibilidad exige saber qué se utilizó en una prueba concreta; no exige mantenerlo indefinidamente cuando nueva evidencia justifique cambiarlo.

## Relación con los cuatro componentes

La arquitectura de trabajo distingue cuatro funciones que comparten un núcleo lingüístico:

### ANALYZER

Intenta reconocer estructura, morfología, persona, aspecto, referencia, procedencia y otras capas documentadas sin convertir automáticamente un análisis plausible en verdad.

Su alcance requerido es multiescala: palabra o forma aislada, frase/enunciado, microescena, conversación completa y discurso continuo cuando exista. El contexto enriquece el análisis, pero no se convierte en requisito universal.

Referencia: `ANALYZER_SCOPE_MULTIESCALA_2026-08-31.md`.

### CORRECTOR

Busca distinguir entre:

- forma documentada;
- variante;
- error suficientemente respaldado;
- normalización posible;
- caso no resuelto.

Debe conservar siempre la forma original y abstenerse cuando la evidencia no sea suficiente.

### TUTOR

Transforma conocimiento aprobado y análisis trazable en explicaciones por capas. Debe distinguir con claridad qué parte proviene de una fuente, qué parte es análisis y qué parte permanece incierta.

### GENERATOR

Ayuda a explorar borradores, situaciones, escenas, estímulos y restricciones. No puede convertir una propuesta generada en Didxazá validado ni definir por sí mismo política pedagógica.

Cualquier requisito futuro de generación debe derivarse de un estado aprobado del Sistema de Conocimiento y quedar identificado por versión/commit.

## Núcleo compartido

Los cuatro componentes deben consumir un núcleo lingüístico común para evitar que cada uno mantenga reglas propias incompatibles.

El núcleo experimental localizado está preservado en `core/JUCHITAN_LINGUISTIC_CORE_v0_27.md`. Es un artefacto técnico migrado, no una fuente canónica de Voces.

La incorporación de esta carpeta no implica que todos los artefactos históricos hayan sido migrados ni que todo lo migrado sea ejecutable. `ESTADO_ACTUAL_2026-08-31.md` conserva un snapshot histórico; el inventario acumulado está en `migracion/MIGRATION_MANIFEST_v1.md` y el estado materializado más reciente en `migracion/CURRENT_EXECUTABLE_STATE_v1.md`.

## COR001

```text
COR001 = ANALYSIS_TARGET_ONLY
COR001 != GOLD_STANDARD
COR001 != BENCHMARK_AUTHORITY
COR001 != REGRESSION_AUTHORITY
COR001 != RULE_DISCOVERY_SOURCE
```

El replay COR001 se conserva para reproducibilidad técnica del runtime histórico. Un `PASS` técnico no valida lingüísticamente sus salidas.

## Discusión pedagógica surgida durante trabajo técnico

La subcarpeta `pedagogia/` conserva documentos de discusión producidos durante trabajo técnico cuando puedan formular preguntas útiles para el proyecto.

Estos documentos son **candidatos o genealogía**, no política pedagógica, y no pueden utilizarse como procedencia autoritativa de una entidad de Voces.

Actualmente contiene:

- `pedagogia/PEDAGOGICAL_DISCUSSION_FREEZE_POST_BIB065_v0_36_2.md` — `FROZEN_DISCUSSION_INPUT_NOT_POLICY`.

Cuando un documento de este tipo sugiera una consecuencia válida, debe volver a la fuente original y al procedimiento de actualización de Voces de las Nubes.

```text
ANALYZER_CAPABILITY != BEGINNER_REQUIREMENT
GENERATION_LICENSE != TEACHING_PRIORITY
PEDAGOGICAL_DISCUSSION != AUTOMATIC_POLICY
```

## Backlog técnico

Las tareas propias de implementación viven en `BACKLOG_TECNICO.md`.

El backlog estructural canónico vive fuera de este repositorio:

`lopezcarlton/vocesdelasnubes/02_BACKLOG.md`

```text
TECHNICAL_BACKLOG != KNOWLEDGE_BACKLOG
IMPLEMENTATION_TASK != PEDAGOGICAL_DECISION
```

## Procedencia y migración

La migración puede conservar etiquetas históricas diferentes para métodos de obtención de evidencia. No se reescriben silenciosamente.

Referencia: `PROVENANCE_LABEL_CROSSWALK_v0_1.md`.

La recuperación técnica se organiza en:

`migracion/MIGRATION_MANIFEST_v1.md`

La migración es una línea de preservación paralela. Su incompletitud no bloquea automáticamente corpus oral, trabajo con hablantes, lectura bibliográfica ni nueva investigación segura en Voces.

## Separación física completada

La separación física se ejecutó y verificó el 2026-09-03. El snapshot inicial exacto está preservado por Git:

```text
SOURCE_REPOSITORY = lopezcarlton/vocesdelasnubes
SOURCE_COMMIT = 22e3c088a97150453f28d03b31613ff9d9491d9a
SOURCE_DEVICE_TREE_SHA = d92c38ec45be4e2e3176b1cfe7c288321c887d3b
INITIAL_IMPORT_COMMIT = 6d205ffe0a0fe660229cd7a958fe43c9a5b51508
IMPORTED_DEVICE_TREE_SHA = d92c38ec45be4e2e3176b1cfe7c288321c887d3b
```

Ese SHA de árbol describe el **snapshot de importación en `6d205ff`**, no el `HEAD` actual: después del corte existen cambios técnicos legítimos y trazables en este repositorio.

Ver:

- `../SEPARATION_VERIFICATION_2026-09-03.md`;
- `migracion/DEVICE_REPOSITORY_SEPARATION_PLAN_v1.md`;
- `KNOWLEDGE_CONSUMPTION_CONTRACT_v1.md`.

## Protección de reproducibilidad vigente

Desde el endurecimiento posterior a la auditoría externa del 2026-09-03:

- `.gitattributes` fija `-text` para los nueve artefactos byte-críticos identificados;
- `.github/workflows/replay-v0-2-15-3.yml` corre en `push` a `main`, `pull_request` hacia `main` y `workflow_dispatch`;
- `../RELEASE_MANIFEST_ANCHOR_v0_2_15_3.json` ancla la identidad SHA-256 y Git blob del manifiesto del release;
- `migracion/test_migrated_state.py` forma parte de CI y pasa 8/8 verificaciones en el checkpoint post-separación;
- el replay histórico mantiene 38/38 pruebas y COR001 permanece `ANALYSIS_TARGET_ONLY`.

La protección de rama/rulesets continúa pendiente y es independiente de estas barreras de integridad.

## Regla de publicación

Los archivos de esta carpeta son documentación técnica de trabajo. No deben citarse como norma del Didxazá, decisión pedagógica vigente ni consenso comunitario.
