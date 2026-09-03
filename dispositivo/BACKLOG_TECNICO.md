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

**Estado:** `IN_PROGRESS / SOURCE_IDENTITIES_AND_V2_20_PROVENANCE_MAPPED / DISTRIBUTION_ARCHITECTURE_PENDING`  
**Prioridad:** Antes de declarar una licencia global o ampliar redistribución externa

La ausencia de `LICENSE` no debe resolverse escogiendo una licencia genérica mientras el árbol contenga artefactos derivados o relacionados con fuentes de terceros cuyos términos son distintos o todavía requieren adjudicación.

### Ejecutado y verificado

- inventario inicial de derechos/provenance materializado;
- auditor read-only de SQLite creado y ejecutado en CI;
- SQLite v2.20 mapeada parcialmente a nivel tabla → source ID → número de filas sin modificar el binario histórico;
- Dictionaria (`BIB054_DICTIONARIA`) verificada como fuente de varias tablas de runtime;
- NOTICE concreto de Dictionaria materializado, preservando requisito técnico de mantener attribution codes/columns por registro;
- Bueno Holle 2019 verificado como fuente `CC BY 4.0` conforme a publisher/provenance local;
- Pickett Vocabulary separado en dos IDs históricas: `BIB003_PICKETT_VOCABULARIO` y `BIB055_PICKETT_VOCABULARIO`, sin fusionarlas por inferencia;
- `BIB004_GRAMATICA_POPULAR` identificado como *Gramática popular del zapoteco del Istmo*, segunda edición electrónica 2001; aviso `D.R.` observado y ninguna licencia abierta verificada;
- `BIB059_PBK2016` triangulado como Pérez Báez & Kaufman 2016, *Verb Classes in Juchitán Zapotec*, DOI `10.1353/anl.2016.0030`; aviso `All rights reserved` observado;
- hueco histórico de `source_profile` verificado para BIB003/BIB055/BIB059;
- `SOURCE_PROFILE_SUPPLEMENT_v1.json` creado como capa derivada no destructiva; la SQLite exacta no se modificó;
- `THIRD_PARTY_ATTRIBUTION_v1.md` creado;
- checkpoint actual de auditoría: `governance/RIGHTS_PROVENANCE_AUDIT_v2.md`;
- inventario actual: `governance/RIGHTS_PROVENANCE_INVENTORY_v2.json`.

### Residual pendiente

- resolver genealogía exacta `BIB003` ↔ `BIB055` para notices/packaging sin colapsar IDs prematuramente;
- definir tratamiento distribuible de `PICKETT_LEXICON_BACKFILL_v0_1.csv` y datos derivados de Pickett;
- definir tratamiento de alineamientos/ejemplos derivados de `BIB004_GRAMATICA_POPULAR`;
- definir tratamiento de las expresiones/registros derivados de `BIB059_PBK2016`, distinguiendo hechos lingüísticos abstractos de expresión fuente;
- auditar SQLite v2.19 por separado;
- auditar outputs de replay por contenido/provenance, sin convertir COR001 en benchmark ni autoridad;
- inventariar alcance de código/documentación originales del proyecto frente a material migrado o source-derived;
- decidir arquitectura final: licencia(s) por subárbol/archivo, NOTICE, exclusiones de paquete distribuible o estrategia mixta;
- sólo entonces decidir si tiene sentido algún `LICENSE` en raíz y cuál sería su alcance exacto.

```text
PUBLIC_ACCESS != OPEN_LICENSE
TECHNICAL_REPRODUCIBILITY != REDISTRIBUTION_PERMISSION
SOURCE_LICENSE != WHOLE_REPOSITORY_LICENSE
THIRD_PARTY_NOTICE != BLANKET_LICENSE
```

No asumir que la presencia histórica de un archivo concede permiso para relicenciarlo. Tampoco eliminar o transformar artefactos sólo para simplificar la elección de licencia sin evaluar antes su función de provenance/reproducibilidad.

Esta tarea es de gobernanza técnica y documental; no adjudica por sí misma derechos jurídicos sobre los materiales existentes.

## Regla

```text
TECHNICAL_BACKLOG != KNOWLEDGE_BACKLOG
IMPLEMENTATION_TASK != PEDAGOGICAL_DECISION
VOCES = AUTHORITY_FOR_KNOWLEDGE
DIDXAZA_DISPOSITIVO = DERIVED_TECHNICAL_SYSTEM
```
