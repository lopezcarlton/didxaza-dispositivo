# KNOWLEDGE_CONSUMPTION_CONTRACT_v1

**Estado:** `ACTIVE_TECHNICAL_CONTRACT / DERIVED_SYSTEM / NON_CANONICAL`

## Propósito

Definir cómo el dispositivo consume conocimiento aprobado de Voces de las Nubes sin crear una segunda fuente de verdad ni obtener capacidad de escritura sobre el Sistema de Conocimiento.

## Autoridad

Este contrato implementa técnicamente:

- `00_ARQUITECTURA_DEL_CONOCIMIENTO.md` §3.5;
- `01_JERARQUIA_DE_VERDAD.md` v1.1;
- `03_REGLAS_DE_ACTUALIZACIÓN.md` v1.2;
- `conocimiento/decisiones/DEC-AUTORIDAD-SISTEMA-CONOCIMIENTO.md`.

No puede ampliar ni modificar esas reglas.

## Identidad del conocimiento consumido

Toda ejecución o desarrollo reproducible que dependa de Voces de las Nubes debe poder declarar:

```text
KNOWLEDGE_SOURCE_REPOSITORY = lopezcarlton/vocesdelasnubes
KNOWLEDGE_SOURCE_COMMIT = <commit exacto>
KNOWLEDGE_SOURCE_REF = <opcional: branch/tag descriptivo>
```

El commit es la identidad autoritativa del estado consumido. Una rama móvil como `main` puede servir para descubrimiento, pero una prueba reproducible debe registrar el commit resuelto.

## Dirección Voces → dispositivo

El dispositivo puede leer conocimiento aprobado necesario para:

- análisis lingüístico trazable;
- representación de hipótesis explícitamente identificadas;
- restricciones de corrección suficientemente autorizadas;
- explicaciones pedagógicas derivadas de conocimiento aprobado;
- requisitos para producción de borradores;
- criterios de abstención;
- procedencia y alcance de evidencia.

La copia o representación técnica de una decisión debe conservar un enlace a su entidad y commit de origen cuando sea materialmente relevante.

```text
CANONICAL_KNOWLEDGE -> TECHNICAL_REPRESENTATION
TECHNICAL_REPRESENTATION != NEW_CANONICAL_KNOWLEDGE
```

## Dirección dispositivo → Voces

El dispositivo puede emitir únicamente candidatos sin autoridad de adopción:

```text
CANDIDATE_FINDING
CANDIDATE_CONTRADICTION
CANDIDATE_REQUIREMENT
CANDIDATE_PEDAGOGICAL_IMPLICATION
CANDIDATE_LINGUISTIC_QUESTION
TECHNICAL_BEHAVIOR_EVIDENCE
```

Cada candidato debe incluir, cuando corresponda:

- artefacto y versión que lo produjo;
- `KNOWLEDGE_SOURCE_COMMIT` usado;
- entrada original analizada;
- evidencia o fuente original que motivó la observación, si existe;
- separación explícita entre resultado técnico e interpretación;
- dominio de autoridad requerido para adjudicarlo.

## Prohibiciones

El dispositivo y sus desarrolladores no pueden, en calidad de desarrolladores del sistema derivado:

- editar directamente `conocimiento/`;
- convertir un candidato en `HALL`, `DEC`, `PRIN`, `VAL` o `TEO` vigente;
- modificar una vista canónica por el resultado de una prueba;
- usar un artefacto técnico como sustituto de una fuente bibliográfica u oral original;
- resolver desacuerdos entre hablantes por frecuencia del runtime;
- convertir COR001 en fuente de reglas, gold, benchmark o regresión.

## Descubrimientos bibliográficos durante desarrollo técnico

Si una lectura realizada durante trabajo del dispositivo produce un hallazgo potencial:

```text
LECTURA_EN_CONTEXTO_TECNICO
-> LOCALIZAR_FUENTE_ORIGINAL
-> REGISTRAR_CANDIDATO
-> VOCES REVISA LA FUENTE
-> HALL / TEO / SUP / DEC, SEGÚN CORRESPONDA
-> NUEVO KNOWLEDGE_SOURCE_COMMIT
-> DISPOSITIVO ACTUALIZA REPRESENTACIÓN
```

El caso BIB065 es la motivación histórica principal de esta regla, no una excepción a ella.

## Acceso

La arquitectura objetivo es:

```text
Voces de las Nubes repository:
  device developers = read only by default

Device repository:
  device developers = write according to technical governance
```

Mientras ambas capas permanezcan en un solo repositorio, esta separación es una regla de autoridad documentada pero no una garantía física completa. La separación física se rige por `migracion/DEVICE_REPOSITORY_SEPARATION_PLAN_v1.md`.
