# BACKLOG TÉCNICO DEL DISPOSITIVO

**Estado:** `DERIVED_SYSTEM_BACKLOG / NON_CANONICAL / POST_SPLIT`
**Actualizado:** 2026-09-03

Este backlog conserva tareas de implementación que no constituyen deuda estructural del Sistema de Conocimiento de Voces de las Nubes.

El backlog estructural canónico vive en `lopezcarlton/vocesdelasnubes/02_BACKLOG.md`. Este archivo no lo modifica ni crea decisiones pedagógicas.

## DT-001 — Evaluar futura producción asistida de borradores

**Origen:** antiguo BL-017 de `02_BACKLOG.md`.

Evaluar herramientas de producción de borradores únicamente cuando existan suficientes escenas de referencia y requisitos aprobados por Voces de las Nubes.

Criterios técnicos posibles:

- aceptación de borradores tras revisión humana;
- artificialidad;
- errores;
- cobertura;
- utilidad real;
- abstención;
- trazabilidad de restricciones.

La herramienta no define por sí misma los criterios pedagógicos de aceptación.

## DT-002 — Representar capas analíticas finas relevantes

**Origen:** componente técnico del antiguo BL-022 de `02_BACKLOG.md`.

Cuando Voces de las Nubes haya adjudicado qué distinciones lingüísticas deben conservarse, evaluar su representación técnica sin convertirlas automáticamente en escalas curriculares.

Candidatos históricos incluyen referencia, tópico/foco, estado informativo, relaciones pregunta-respuesta, organización prosódica y alternancias de realización explícita/clítica/omisión.

La selección final debe consumir una versión aprobada del conocimiento, no el artefacto técnico BIB065 como autoridad.

## DT-003 — Separar físicamente el repositorio técnico y hacer efectiva la frontera de permisos

**Estado:** `PHYSICAL_SPLIT_EXECUTED / REPRODUCIBILITY_PROTECTED / LOCAL_GOVERNANCE_PRESENT / PERMISSION_HARDENING_PENDING`  
**Prioridad residual:** Antes de incorporar desarrolladores externos

Plan: `migracion/DEVICE_REPOSITORY_SEPARATION_PLAN_v1.md`.

### Ejecutado y verificado

- repositorio técnico separado creado: `lopezcarlton/didxaza-dispositivo`;
- árbol técnico inicial importado preservando genealogía e identidad del snapshot;
- `KNOWLEDGE_SOURCE_COMMIT` registrado;
- replay reproducido en el repositorio destino;
- cadena histórica de 38/38 pruebas reproducida;
- copia activa de `dispositivo/` retirada de `lopezcarlton/vocesdelasnubes/main`;
- workflow técnico retirado de Voces;
- `.gitattributes` añadido para proteger los nueve artefactos byte-críticos identificados;
- replay configurado para `push`, `pull_request` y `workflow_dispatch`;
- `test_migrated_state.py` reparado e incorporado a CI, con 9/9 verificaciones en el checkpoint post-separación;
- `RELEASE_MANIFEST_ANCHOR_v0_2_15_3.json` creado y verificado contra SHA-256 y Git blob del manifiesto;
- `.gitignore` conservador añadido sin excluir formatos de datos/documentos usados por artefactos del repositorio;
- `.github/CODEOWNERS` añadido con ownership general `@lopezcarlton`;
- `CONTRIBUTING.md` añadido con frontera de conocimiento, preservación histórica y disciplina de PR/CI;
- `dispositivo/prompts/historicos/README.md` añadido para poner los dos prompts recuperados en cuarentena explícita sin modificar sus blobs.

La evidencia de separación está en `../SEPARATION_VERIFICATION_2026-09-03.md`.

### Residual pendiente

Queda hacer efectiva la frontera de permisos mediante configuración de GitHub:

- branch protection y/o rulesets apropiados sobre `main`;
- permisos de escritura sobre `vocesdelasnubes` restringidos para futuros desarrolladores técnicos;
- hacer exigible la revisión/ownership antes de incorporar colaboradores externos.

La consulta del endpoint clásico de branch protection sigue bloqueada para esta integración (`403`). En `didxaza-dispositivo` la consulta de rulesets devolvió una lista vacía durante la revisión del 2026-09-03. El repositorio técnico ya tiene `CODEOWNERS`, pero ese archivo sólo enruta ownership/revisión: no constituye por sí solo una barrera de escritura ni una aprobación obligatoria.

**No bloquea:** investigación, captura de fuentes, trabajo humano de documentación ni desarrollo técnico que respete la frontera de autoridad.

**Sí bloquea:** considerar completada la garantía de permisos para incorporar desarrolladores externos con separación efectiva de escritura entre ambos repositorios.

## DT-004 — Auditar derechos de materiales y definir estrategia de licenciamiento

**Estado:** `OPEN / RIGHTS_AUDIT_REQUIRED_BEFORE_BLANKET_LICENSE`  
**Prioridad:** Antes de declarar una licencia global o ampliar redistribución externa

La auditoría técnica detectó que el repositorio no tiene `LICENSE`. No debe resolverse escogiendo una licencia genérica mientras el árbol contenga artefactos derivados o relacionados con fuentes de terceros cuyos términos no estén inventariados.

Trabajo pendiente:

- inventariar artefactos propios y de terceros con provenance suficiente;
- identificar licencias, permisos, restricciones o estados no resueltos cuando existan;
- separar código original del proyecto de corpus, diccionarios, bases derivadas, documentación u otros materiales con derechos potencialmente distintos;
- decidir si procede una licencia global, licencias por subárbol/archivo o una combinación;
- documentar explícitamente cualquier material cuyo derecho de redistribución o relicenciamiento permanezca sin resolver.

No asumir que la presencia histórica de un archivo concede permiso para relicenciarlo. Tampoco eliminar o transformar artefactos sólo para simplificar la elección de licencia sin evaluar antes su función de provenance/reproducibilidad.

Esta tarea es de gobernanza técnica y documental; no adjudica por sí misma derechos jurídicos sobre los materiales existentes.

## Regla

```text
TECHNICAL_BACKLOG != KNOWLEDGE_BACKLOG
IMPLEMENTATION_TASK != PEDAGOGICAL_DECISION
VOCES = AUTHORITY_FOR_KNOWLEDGE
DIDXAZA_DISPOSITIVO = DERIVED_TECHNICAL_SYSTEM
```
