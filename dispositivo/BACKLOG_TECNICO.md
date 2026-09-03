# BACKLOG TÉCNICO DEL DISPOSITIVO

**Estado:** `DERIVED_SYSTEM_BACKLOG / NON_CANONICAL`

Este backlog conserva tareas de implementación que no constituyen deuda estructural del Sistema de Conocimiento de Voces de las Nubes.

No modifica `02_BACKLOG.md` ni crea decisiones pedagógicas.

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

**Estado:** Pendiente por acción de infraestructura  
**Prioridad:** Antes de incorporar desarrolladores externos

Ejecutar `migracion/DEVICE_REPOSITORY_SEPARATION_PLAN_v1.md`.

La tarea incluye:

- crear el repositorio técnico separado;
- migrar el árbol activo del dispositivo preservando genealogía e identidades relevantes;
- registrar `KNOWLEDGE_SOURCE_COMMIT`;
- reproducir replay y 38/38 pruebas en el repositorio destino;
- configurar permisos para que desarrolladores técnicos tengan lectura —no escritura por defecto— sobre `vocesdelasnubes`;
- activar protección/ruleset de `main` y revisión de ownership adecuada para el Sistema de Conocimiento;
- sólo después retirar el dispositivo activo del repositorio canónico.

`.github/CODEOWNERS` ya documenta ownership, pero **no debe considerarse una garantía de permisos por sí solo**. La integración usada durante la limpieza no tuvo acceso para inspeccionar/modificar la protección de rama (`403`), por lo que esa parte requiere configuración de GitHub fuera de esta automatización.

**No bloquea:** captura de Irma como fuente cruda ni trabajo humano de documentación.

**Sí bloquea:** considerar completada la garantía física de que futuros desarrolladores del dispositivo no pueden escribir en el Sistema de Conocimiento.

## Regla

```text
TECHNICAL_BACKLOG != KNOWLEDGE_BACKLOG
IMPLEMENTATION_TASK != PEDAGOGICAL_DECISION
```
