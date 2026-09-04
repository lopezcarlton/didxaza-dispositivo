# VOCES_KNOWLEDGE_PATCH_2026-09-04_v1

**Estado:** `ACTIVE_DERIVED_KNOWLEDGE_PATCH / NON_CANONICAL / VOCES_AUTHORITY`  
**Fecha:** 2026-09-04

```text
KNOWLEDGE_SOURCE_REPOSITORY = lopezcarlton/vocesdelasnubes
KNOWLEDGE_SOURCE_COMMIT = e66630195471f1d4d142c018e067dade55a35a41
```

## Propósito

Materializar en el repositorio técnico un conjunto de hechos que ya fueron promovidos o corregidos en Voces de las Nubes después de detectar huecos de migración semántica durante la lectura del Alfabeto Popular de 1956.

Este archivo **no crea conocimiento**. Es una representación técnica derivada de `HALL` canónicos y debe leerse junto con `KNOWLEDGE_CONSUMPTION_CONTRACT_v1.md`.

## DKP-001 — segunda persona singular `tú/usted`

**Fuente canónica:** `HALL-0066`.

```text
GRAMMATICAL_TU_USTED_OPPOSITION = false
SECOND_PERSON_SINGULAR = one_grammatical_person
LIi_CAN_TRANSLATE_AS = tú | usted
PRAGMATIC_TREATMENT = separate_layer
```

Efectos:

- ANALYZER no debe crear dos valores gramaticales distintos por la diferencia española `tú/usted`.
- TUTOR puede explicar que el español exige una elección de traducción que el pronombre didxazá no codifica de la misma manera.
- GENERATOR debe resolver cortesía/trato en la capa pragmática, no mediante una falsa oposición pronominal.

El core v0.27 ya contiene las formas 2SG `-lu'/-u'`, pero no hacía explícita esta ausencia de oposición `tú/usted`.

## DKP-002 — inventario tonal

**Fuente canónica:** `HALL-0067`.

```text
PHONEMIC_TONE_COUNT = 3
LOW = L
HIGH = H
RISING = LH
```

El `JLC-TONE-001` de v0.27 reconoce que el tono es contrastivo, pero queda incompleto si no declara el inventario. Este patch fija para el baseline juchiteco el análisis contemporáneo de tres tonos fonémicos.

No confundir:

```text
PHONEMIC_TONES != SURFACE_TONAL_MELODIES
PHONEMIC_TONES != FLOATING_TONE_CONFIGURATIONS
```

La descripción histórica de cuatro tipos en 1956 no se usa como inventario fonémico actual.

## DKP-003 — regla contextual `xh/x`

**Fuente canónica:** `HALL-0068`; antecedente `HALL-0048`.

```text
XH_VALUE_CAN_SURFACE_AS_X_BEFORE_CONSONANT = true
GLOBAL_X_TO_XH_REWRITE = forbidden
```

El core v0.27 ya contiene `JLC-POS-003` (`xh-` ante vocal / `x-` ante consonante) y alternancias relacionadas. Este patch aclara que la regla no es sólo un residuo histórico: está documentada en fuentes posteriores y debe conservarse como conocimiento vigente de análisis.

## DKP-004 — `r` débil y `r` fuerte

**Fuente canónica:** `HALL-0069`; antecedente `HALL-0052`.

```text
R_WEAK_TAP = default_general_pattern
R_STRONG_TRILL_NATIVE = exceptional_small_lexical_set
R_STRONG_TRILL_SPANISH_LOANS = expected_possibility
```

La `r` fuerte no debe modelarse como alternativa productiva equiprobable de la `r` débil. Las excepciones nativas requieren inventario léxico documentado. La ortografía superficial `r` puede ser ambigua, por lo que no debe inferirse automáticamente la pronunciación fuerte desde la grafía.

## DKP-005 — variación `tobi/tubi`

**Fuentes canónicas:** `HALL-0070`, `HALL-0071`.

```text
TOBI = reported_Juchitan_variant_for_ONE
TUBI = reported_El_Espinal_variant_for_ONE
TOBI_TUBI_SEMANTIC_EQUIVALENCE_IN_SPEAKER_REPORT = true
AUTO_CORRECT_ONE_VARIANT_TO_THE_OTHER = forbidden
```

Esta evidencia refuerza que las diferencias locales deben conservar provenance de comunidad. No resuelve por analogía la distribución exacta de `qui/qué`.

## DKP-006 — autoridad histórica del Alfabeto Popular

**Fuente canónica:** `HALL-0072`.

```text
ALFABETO_POPULAR_1956 = foundational_orthographic_reference
ALFABETO_POPULAR_1956 = high_historical_authority
ALFABETO_POPULAR_1956 != sole_complete_2026_norm
ALFABETO_POPULAR_1956 != NORMA_2016
```

Al consumir reglas ortográficas históricas, el dispositivo debe comprobar continuidad con conocimiento posterior formalizado en Voces. No debe tratar el Alfabeto Popular como simple curiosidad histórica, pero tampoco convertir su versión de 1956 en regla contemporánea automática sin adjudicación.

## Regla de transición

Este patch es **documentalmente activo** pero no afirma que todos los engines o registries ejecutables ya lo consuman. Cualquier wiring al runtime debe:

1. preservar estos IDs de fuente canónica;
2. registrar el `KNOWLEDGE_SOURCE_COMMIT`;
3. añadir pruebas técnicas que no usen COR001 como gold, benchmark, regresión o fuente de reglas;
4. conservar `UNRESOLVED != INCORRECT`.
