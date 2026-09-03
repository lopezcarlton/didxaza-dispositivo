# PROVENANCE LABEL CROSSWALK v0.1

**Proyecto:** Voces de las Nubes  
**Estado:** regla técnica de migración / no jerarquía de verdad  
**Fecha:** 2026-08-31

## Propósito

Evitar que diferencias históricas de nomenclatura produzcan falsas contradicciones durante la migración del dispositivo.

Los documentos y artefactos desarrollados en momentos distintos utilizan nombres ligeramente diferentes para métodos de obtención de evidencia. No es necesario reescribir los archivos históricos ni elegir manualmente un nombre cada vez.

La migración conservará dos campos cuando sea necesario:

```text
provenance_raw        = etiqueta original del artefacto
provenance_canonical  = categoría normalizada para interoperabilidad
```

La etiqueta original nunca se pierde.

## Categorías canónicas actuales

Las categorías canónicas siguen la terminología adoptada actualmente por `METODOLOGIA.md` y `CORPUS.md`:

| Etiqueta histórica o alternativa | Etiqueta canónica | Nota |
|---|---|---|
| `SPONTANEOUS` | `SPONTANEOUS` | Habla espontánea o naturalista. |
| `NONLINGUISTIC_ELICITATION` | `ELICITED_NONLINGUISTIC` | Variante nominal usada en artefactos del dispositivo. |
| `ELICITED_NONLINGUISTIC` | `ELICITED_NONLINGUISTIC` | Forma canónica actual. |
| `SPEAKER_JUDGMENT` | `SPEAKER_JUDGMENT` | Juicio explícito de hablante. |
| `TRANSLATION_ELICITATION` | `TRANSLATION_REFORMULATION` | Se mapea a la categoría amplia actual; el valor original se conserva para no perder la distinción histórica. |
| `TRANSLATION_REFORMULATION` | `TRANSLATION_REFORMULATION` | Traducción o reformulación a partir de una propuesta. |
| `DOCUMENTARY` | `DOCUMENTARY` | Evidencia documental. |

## Regla de no colapso

El mapeo canónico facilita búsquedas y comparación, pero no autoriza a afirmar que dos procedimientos fueron metodológicamente idénticos.

Por ejemplo, `TRANSLATION_ELICITATION` y `TRANSLATION_REFORMULATION` pueden compartir una categoría canónica amplia y seguir conservando diferencias relevantes en `provenance_raw`, notas de sesión o metadatos adicionales.

## Etiquetas no reconocidas

Cuando aparezca durante la migración una etiqueta que no pueda mapearse con seguridad:

```text
provenance_raw = <valor original>
provenance_canonical = UNMAPPED
```

No se inventará una equivalencia para completar el esquema.

## Relación con autoridad

Estas etiquetas describen **cómo se obtuvo un dato**. No constituyen por sí mismas una jerarquía automática de verdad, naturalidad o corrección.

La autoridad de una evidencia depende de la pregunta que se intenta resolver y de las reglas vigentes del Sistema de Conocimiento.
