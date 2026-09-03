# MIGRATION_AGENT_PROTOCOL_v1 — Migración directa desde chats del dispositivo

**Proyecto:** Voces de las Nubes  
**Fecha:** 2026-08-31  
**Estado:** ACTIVE_PROTOCOL / NON_BLOCKING  
**Ámbito:** chats históricos o activos donde se desarrollaron Analyzer, Corrector, Tutor, Generator, núcleo lingüístico, runtimes, bases, schemas, pruebas y documentación relacionada

---

## 1. Objetivo

Este protocolo permite recuperar el estado del dispositivo directamente desde los chats donde fue desarrollado, **sin convertir previamente cada conversación completa en un documento Markdown de migración**.

La unidad de migración no es el chat.

La unidad de migración es un **artefacto identificable o un estado técnico/documental recuperable con trazabilidad**.

Ejemplos:

- un archivo Markdown existente;
- un script completo;
- un schema;
- un conjunto de tests;
- una tabla o inventario;
- una especificación versionada;
- un reporte de estado;
- una decisión de arquitectura explícita;
- un archivo generado dentro del chat;
- una referencia verificable a un ZIP, SQLite u otro binario que no pueda transferirse todavía.

```text
CHAT != MIGRATION_ARTIFACT
CONVERSATION_HISTORY != SOURCE_OF_TRUTH_BY_ITSELF
RECOVERABLE_ARTIFACT > RETROSPECTIVE_SUMMARY
```

---

## 2. Principio de investigación abierta

Antes de migrar, leer:

1. `conocimiento/principios/PRIN-INVESTIGACION-ABIERTA.md`;
2. `dispositivo/README.md`;
3. `dispositivo/migracion/MIGRATION_MANIFEST_v1.md`;
4. `dispositivo/migracion/CURRENT_EXECUTABLE_STATE_v1.md`;
5. `dispositivo/migracion/REENTRY_CHECKPOINT_2026-09-02.md`;
6. `dispositivo/ESTADO_ACTUAL_2026-08-31.md` únicamente como snapshot histórico previo a la migración.

La migración preserva estado; **no congela la investigación**.

```text
MIGRATED_ARTIFACT != IMMUTABLE_RULE
IMPLEMENTED_CAPABILITY != RESEARCH_AUTHORITY
HISTORICAL_STATE != CURRENT_POLICY
MIGRATION_INCOMPLETE != RESEARCH_BLOCKED
```

No convertir por inercia en regla canónica:

- una implementación;
- una hipótesis;
- una salida del Analyzer;
- una propuesta del Generator;
- un benchmark;
- una convención de schema;
- una decisión que luego fue revisada;
- un artefacto recuperado sólo porque sea la versión más reciente disponible.

---

## 3. Modo de trabajo dentro del chat histórico

Al recibir la instrucción de ejecutar este protocolo:

### Paso 1 — Leer el estado actual del repositorio

Consultar los documentos vigentes listados arriba y cualquier archivo específico mencionado por el manifiesto como relacionado con este chat. `ESTADO_ACTUAL_2026-08-31.md` aporta genealogía histórica, pero no prevalece sobre `CURRENT_EXECUTABLE_STATE_v1.md` ni `REENTRY_CHECKPOINT_2026-09-02.md`.

No asumir que el estado recordado por la conversación sigue vigente.

### Paso 2 — Inventariar únicamente lo realmente accesible en este chat

Revisar:

- archivos adjuntos actuales o históricos accesibles;
- archivos generados dentro del chat;
- bloques de código completos;
- documentos versionados completos;
- nombres de ZIPs, SQLite, scripts, schemas o paquetes mencionados;
- reportes de pruebas;
- hashes, versiones y dependencias cuando estén registrados;
- decisiones explícitas que expliquen el estado de un artefacto.

No inventar contenido de archivos que sólo se mencionan por nombre.

No reconstruir un archivo completo desde recuerdos parciales si existe la posibilidad de localizar su fuente exacta.

### Paso 3 — Clasificar cada candidato

Usar los estados del manifiesto:

- `MIGRATED`;
- `RECOVERABLE_SOURCE_LOCATED`;
- `REFERENCED_BY_LOCATED_ARTIFACT`;
- `EXTERNAL_KNOWN_NOT_MIGRATED`;
- `NOT_LOCATED_IN_CURRENT_PASS`;
- `SUPERSEDED`;
- `ARCHIVE_ONLY`.

Puede añadirse, cuando sea necesario:

- `SOURCE_COMPLETE_READY_TO_MIGRATE` — fuente completa disponible en el chat y lista para copia exacta;
- `SOURCE_PARTIAL_DO_NOT_MIGRATE` — sólo existe contenido parcial o truncado;
- `BINARY_TRANSFER_PENDING` — el artefacto existe pero la herramienta disponible no permite transferirlo de forma íntegra.

### Paso 4 — Migrar directamente cuando la fuente sea completa

Si el chat contiene el artefacto completo y su identidad/versionado es suficientemente claro:

1. conservar nombre y versión originales cuando sea posible;
2. copiar el contenido íntegro, sin reescribirlo para “mejorarlo”;
3. colocarlo en una ruta coherente dentro de `dispositivo/`;
4. añadir un encabezado externo sólo si es imprescindible para dejar claro su estado, y preferentemente mediante un archivo acompañante en vez de alterar el artefacto original;
5. hacer un commit atómico y descriptivo;
6. actualizar `MIGRATION_MANIFEST_v1.md` inmediatamente después.

Nunca migrar una versión truncada como si fuera completa.

### Paso 5 — Si no puede migrarse el archivo, migrar su identidad

Para ZIP, SQLite, audio, binarios o archivos inaccesibles para escritura directa, registrar en el manifiesto, si la evidencia existe:

- nombre exacto;
- versión;
- hash conocido y su estatus (`canonical`, `observed_historical`, `unverified`, etc.);
- función;
- dependencias;
- dónde fue visto;
- qué contiene según evidencia verificable;
- qué falta para transferirlo.

No sustituir el binario por una reconstrucción textual ficticia.

### Paso 6 — Resolver genealogía cuando existan varias versiones

Si aparecen versiones sucesivas:

1. no asumir que la más nueva es automáticamente la correcta;
2. identificar qué cambió;
3. buscar reportes de estabilización, decisiones, tests o migraciones que indiquen qué versión representaba el estado activo;
4. conservar versiones antiguas sólo cuando expliquen una transición relevante;
5. marcar versiones superadas como `SUPERSEDED` o `ARCHIVE_ONLY`.

Especial cuidado con casos donde:

```text
CONCEPT -> IMPLEMENTATION -> REFACTOR -> RULE_DISAPPEARS -> FIELD_REMAINS
```

La presencia de un campo o nombre histórico no demuestra que su semántica original siguiera activa.

### Paso 7 — No usar COR001 como gold standard

COR001 puede ser objeto de análisis del dispositivo, nunca fuente automática de reglas, benchmark lingüístico, gold standard ni licencia de generación.

Los reportes sobre COR001 se conservan como evidencia del comportamiento del dispositivo.

### Paso 8 — Cerrar cada pasada

Al terminar una pasada en un chat histórico, producir sólo un resumen breve con:

- artefactos migrados;
- artefactos localizados pero pendientes;
- artefactos parciales que deliberadamente no se migraron;
- dependencias nuevas descubiertas;
- commits realizados;
- siguiente artefacto recomendado.

No generar una narración exhaustiva de todo el chat salvo que sea necesaria para entender una genealogía concreta.

---

## 4. Estructura de destino sugerida

La estructura puede evolucionar. Inicialmente:

```text
dispositivo/
  core/
  analyzer/
    reports/
    tests/
  corrector/
  tutor/
  generator/
  schemas/
  validation/
  development_corpus/
  hardening/
  pedagogia/
  migracion/
    fuentes/
    reports/
```

No crear carpetas vacías por anticipado.

La ubicación física no concede autoridad.

---

## 5. Qué NO hacer

- No resumir todo el chat antes de empezar.
- No transformar cada conversación en un Markdown monolítico.
- No reconstruir código desde descripciones si el código original puede localizarse.
- No “limpiar” silenciosamente un artefacto histórico mientras se migra.
- No fusionar versiones distintas sin dejar genealogía.
- No declarar perdido algo después de una sola búsqueda fallida.
- No bloquear investigación lingüística o pedagógica hasta completar la migración.
- No promover resultados del dispositivo al Sistema de Conocimiento sin el proceso normal de evidencia y revisión.
- No asumir que una regla implementada debe seguir implementándose.
- No asumir que una hipótesis no implementada carece de valor investigativo.

---

## 6. Prioridad de recuperación

Dentro de cada chat, priorizar:

### P0 — Estado irreemplazable

- núcleos lingüísticos versionados;
- especificaciones de vertical slices;
- runtimes identificables;
- DB/schema con versión;
- Generator/Analyzer/Corrector/Tutor en su último estado reproducible;
- inventarios y ValidationQueue;
- documentos de estado que expliquen qué estaba realmente implementado.

### P1 — Límites y reproducibilidad

- guardrails;
- schemas;
- tests;
- reports;
- readiness matrices;
- protocolos de corpus de desarrollo;
- perfiles ortográficos;
- AdoptionRecords;
- documentación de procedencia.

### P2 — Herramientas auxiliares

- scripts secundarios;
- adaptadores;
- tooling;
- bases derivadas reproducibles.

### P3 — Historia

- auditorías antiguas;
- paquetes intermedios;
- respuestas de brainstorming;
- versiones superadas sin dependencias actuales.

---

## 7. Regla de autonomía del chat migrador

El chat que ejecuta este protocolo puede tomar decisiones **de preservación**, no decisiones nuevas sobre la investigación.

Puede decidir:

- que una fuente está completa;
- que una versión está claramente identificada;
- dónde archivarla provisionalmente;
- que algo está truncado y no debe migrarse;
- que dos artefactos tienen una relación documental demostrable;
- que una versión está explícitamente marcada como superseded.

No puede decidir por sí solo:

- cambiar una regla lingüística vigente;
- cerrar una hipótesis pedagógica;
- declarar definitiva una arquitectura;
- convertir una capacidad en requisito de aprendizaje;
- adoptar una nueva norma ortográfica;
- redefinir G/P;
- cerrar una contradicción lingüística sin evidencia.

Cuando encuentre una cuestión de investigación real, debe registrarla como pendiente o evidencia, no resolverla por conveniencia de migración.

---

## 8. Actualización obligatoria del manifiesto

Cada chat migrador debe leer la última versión de `MIGRATION_MANIFEST_v1.md` antes de escribir y actualizarla al terminar.

El manifiesto funciona como **memoria compartida entre chats**.

Así, diferentes conversaciones históricas pueden contribuir a la misma migración sin depender unas de otras ni repetir trabajo.

Si dos chats contienen versiones distintas del mismo artefacto, no sobrescribir una con otra: registrar ambas y resolver genealogía.

---

## 9. Resultado esperado

La migración estará suficientemente avanzada cuando el repositorio permita responder sin reconstrucción conversacional a estas preguntas:

- ¿cuál era el estado reproducible más reciente de cada componente?;
- ¿qué evidencia consumía?;
- ¿qué podía hacer y qué no podía hacer?;
- ¿qué estaba validado, provisional, en cuarentena o superseded?;
- ¿qué dependencias faltan?;
- ¿qué resultados siguen siendo investigables?;
- ¿qué artefactos históricos explican la genealogía del estado actual?;

No es necesario recuperar cada mensaje ni cada versión intermedia para alcanzar ese punto.
