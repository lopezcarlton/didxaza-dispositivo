# ANALYZER — Alcance multiescala requerido

**Proyecto:** Voces de las Nubes  
**Fecha:** 2026-08-31  
**Estado:** requisito funcional del dispositivo / no regla lingüística canónica

## Propósito

Registrar una condición de alcance que deberá conservarse durante la migración y recuperación del `ANALYZER_ENGINE`.

## Alcance

El Analyzer debe poder recibir y analizar material en distintas escalas, sin convertir una sola de ellas en unidad obligatoria universal.

Como mínimo debe admitir:

1. **palabra o forma aislada**;
2. **frase o enunciado aislado**;
3. **microescena** — secuencia breve de varios turnos;
4. **conversación o escena completa**;
5. **discurso de varios turnos o segmentos continuos** cuando exista contexto suficiente.

Estas escalas pueden requerir capacidades distintas. Un análisis de palabra aislada no puede depender de información conversacional inexistente; una conversación completa, en cambio, puede aportar antecedentes, correferencia, continuidad discursiva, inferencias y organización informativa que enriquecen el análisis.

## Regla de contexto

> **El contexto enriquece el análisis cuando existe; no se convierte en prerrequisito universal.**

Por tanto:

- una palabra aislada sigue siendo un objeto legítimo de análisis;
- una frase aislada sigue siendo un objeto legítimo de análisis;
- una microescena puede analizar relaciones entre turnos;
- una conversación completa puede activar análisis discursivo más rico;
- la ausencia de contexto debe producir límites explícitos o abstención cuando corresponda, no la falsa conclusión de que la unidad es inválida.

`UNRESOLVED` o `NO_ENCONTRADO` no equivalen automáticamente a error lingüístico.

## Relación con COR002

COR002 utiliza la conversación completa como unidad primaria de diseño, pero puede contener o derivar también microescenas, frases sueltas y otras unidades pedagógicas.

La elección de una unidad pedagógica de COR002 no limita el alcance del Analyzer.

```text
COR002_PRIMARY_DESIGN_UNIT != ANALYZER_ONLY_INPUT_UNIT
```

## Relación con la migración

Cuando se recuperen runtimes, schemas, benchmarks o vertical slices anteriores, esta capacidad multiescala deberá utilizarse como criterio para evaluar qué artefactos siguen representando correctamente la arquitectura vigente.

No se reconstruirá un Analyzer limitado artificialmente a conversación completa ni uno que requiera contexto discursivo para todo análisis.
