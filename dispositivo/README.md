# DISPOSITIVO LINGÜÍSTICO — CAPA EXPERIMENTAL DERIVADA

**Proyecto:** Voces de las Nubes  
**Estado:** `DERIVED_SYSTEM / NON_CANONICAL / EXPERIMENTAL`  
**Fecha de creación:** 2026-08-31  
**Frontera de autoridad actualizada:** 2026-09-02

## Reentrada técnica

Para trabajo explícitamente técnico sobre Analyzer, Corrector, Tutor, Generator, runtime, tests, schemas o migración, iniciar en:

`REENTRY_TECNICO.md`

El punto de entrada general de Voces de las Nubes permanece en `../INICIAR_AQUI_CHAT_NUEVO.md` y **no carga esta capa por defecto**.

## Propósito

Esta carpeta conserva el trabajo interno desarrollado para convertir conocimiento aprobado del proyecto en capacidades operativas de:

- análisis;
- revisión y normalización;
- explicación pedagógica;
- producción controlada de estímulos y materiales.

También preserva genealogía, hipótesis ejecutables, estados históricos y capacidad reproducible de investigación técnica.

## Regla fundamental de autoridad

**`dispositivo/` no es una segunda fuente de verdad lingüística, pedagógica, metodológica ni comunitaria.**

El Sistema de Conocimiento permanece en `conocimiento/` y en los documentos constitucionales del repositorio.

La decisión vigente es `conocimiento/decisiones/DEC-AUTORIDAD-SISTEMA-CONOCIMIENTO.md`.

```text
DEVICE_MAY_READ = true
DEVICE_MAY_ANALYZE = true
DEVICE_MAY_PROPOSE = true
DEVICE_MAY_CHALLENGE = true

DEVICE_MAY_ADOPT_KNOWLEDGE = false
DEVICE_MAY_PROMOTE_CANDIDATE = false
DEVICE_MAY_WRITE_KNOWLEDGE = false
```

La expresión **no puede escribir conocimiento** es más fuerte que “no puede modificar automáticamente”. Una persona o agente trabajando como desarrollador del dispositivo tampoco adquiere autoridad sobre `conocimiento/` por tener capacidad técnica para analizarlo.

Los futuros desarrolladores del dispositivo **no tendrán por defecto permisos de escritura sobre el Sistema de Conocimiento**. Mientras ambas capas sigan materializadas en este repositorio, `.github/CODEOWNERS` documenta ownership; la protección efectiva de ramas/rulesets debe configurarse en GitHub y no se presume activa únicamente por existir ese archivo.

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

El dispositivo se rige por `conocimiento/principios/PRIN-INVESTIGACION-ABIERTA.md`.

Su función es ampliar la capacidad de investigar, no cerrar la investigación. Una representación implementada puede ser provisional, quedar superseded, ser útil sólo para una prueba o necesitar revisión posterior.

```text
IMPLEMENTED_CAPABILITY != RESEARCH_AUTHORITY
MIGRATED_ARTIFACT != IMMUTABLE_RULE
CURRENT_RUNTIME != FINAL_ARCHITECTURE
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

El núcleo experimental localizado está preservado en `core/JUCHITAN_LINGUISTIC_CORE_v0_27.md`. Bases, runtimes, inventarios, pruebas y paquetes tienen grados distintos de transferencia y reproducibilidad.

La incorporación de esta carpeta **no implica que todos esos artefactos hayan sido migrados ni que todo lo migrado sea ejecutable**. `ESTADO_ACTUAL_2026-08-31.md` conserva un snapshot histórico; el inventario acumulado está en `migracion/MIGRATION_MANIFEST_v1.md` y el estado materializado más reciente en `migracion/CURRENT_EXECUTABLE_STATE_v1.md`.

## Discusión pedagógica surgida durante trabajo técnico

La subcarpeta `pedagogia/` conserva documentos de discusión producidos durante trabajo técnico cuando puedan formular preguntas útiles para el proyecto.

Estos documentos son **candidatos o genealogía**, no política pedagógica, y no pueden utilizarse como `provenance` autoritativa de una entidad de `conocimiento/`.

Actualmente contiene:

- `pedagogia/PEDAGOGICAL_DISCUSSION_FREEZE_POST_BIB065_v0_36_2.md` — `FROZEN_DISCUSSION_INPUT_NOT_POLICY`.

Cuando un documento de este tipo sugiera una consecuencia válida, debe volver a la fuente original y al procedimiento de actualización de Voces de las Nubes.

```text
ANALYZER_CAPABILITY != BEGINNER_REQUIREMENT
GENERATION_LICENSE != TEACHING_PRIORITY
PEDAGOGICAL_DISCUSSION != AUTOMATIC_POLICY
```

## Backlog técnico

Las tareas propias de implementación viven en `BACKLOG_TECNICO.md` y no en el backlog estructural canónico `../02_BACKLOG.md`.

```text
TECHNICAL_BACKLOG != KNOWLEDGE_BACKLOG
IMPLEMENTATION_TASK != PEDAGOGICAL_DECISION
```

## Procedencia y migración

La migración puede encontrar etiquetas históricas diferentes para métodos de obtención de evidencia. No se reescribirán silenciosamente.

Referencia: `PROVENANCE_LABEL_CROSSWALK_v0_1.md`.

La recuperación técnica se organiza en:

`migracion/MIGRATION_MANIFEST_v1.md`

La migración es una línea de preservación paralela. Su incompletitud no bloquea automáticamente corpus oral, trabajo con hablantes, lectura bibliográfica ni nueva investigación segura.

## Separación física futura

La coexistencia actual de `conocimiento/` y `dispositivo/` en el mismo repositorio se conserva temporalmente por genealogía y reproducibilidad. No representa el diseño final de permisos.

La separación física futura debe seguir `migracion/DEVICE_REPOSITORY_SEPARATION_PLAN_v1.md` y preservar el replay y las identidades exactas antes de retirar el dispositivo activo de Voces de las Nubes.

El contrato de consumo entre ambas capas se documenta en `KNOWLEDGE_CONSUMPTION_CONTRACT_v1.md`.

## Regla de publicación

Los archivos de esta carpeta son documentación técnica de trabajo. No deben citarse como norma del Didxazá, decisión pedagógica vigente ni consenso comunitario.
