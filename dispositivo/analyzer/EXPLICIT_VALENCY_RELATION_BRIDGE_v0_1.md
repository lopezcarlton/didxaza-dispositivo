# ExplicitValencyRelationBridge v0.1

Estado: `DERIVED_NON_LICENSING_ANALYZER_LAYER`

## Autoridad consumida

```text
VOCES_COMMIT = f17c5363caada6f8beb18fa99c39e37cd72c6f09
SOURCE = SRC-PEREZ-BAEZ-2015-VALENCE-CHANGING-JUCHITAN
HALL = HALL-0193
TECHNICAL_CROSSWALK = dispositivo/sources/VOCES_PB2015_EXPLICIT_VALENCY_RELATIONS_v0_1.csv
```

La capa no descubre relaciones morfológicas. Recupera únicamente conjuntos y papeles ya documentados por Pérez Báez 2015 y promovidos en Voces.

## Requisito de identidad

Una relación puede atribuirse a una entrada sólo cuando una capa anterior ya identificó el verbo mediante:

- `DOCUMENTED_EXACT_VERB_HEADWORD_ENTRY_LINK`; o
- `SOURCE_DOCUMENTED_PERSON_FUSION_LEMMA_ENTRY_LINK`.

Un `NONHEADWORD_STRUCTURAL_VERB_ENTRY_CANDIDATE_ONLY` no basta para afirmar pertenencia a un conjunto de valencia.

## Crosswalk

La resolución entre miembro PB2015 y Dictionaria usa igualdad PDLMA cruda, sin normalización:

```text
UNIQUE_STRICT   -> puede enlazar ese miembro fuente con una entrada
NO_STRICT       -> sin enlace estricto; NO es evidencia negativa
MULTIPLE_STRICT -> ambigüedad conservada; no se elige una entrada
```

Estado v0.1:

```text
65 miembros fuente
26 conjuntos
26 UNIQUE_STRICT
38 NO_STRICT
1 MULTIPLE_STRICT
6 conjuntos completamente resueltos de manera única
```

El caso `PB15-V2-UUNDA / -uunda` conserva dos candidatos (`uunda1`, `uunda2`) y no asigna la relación a ninguno.

## Límites

```text
SOURCE_EXPLICIT_RELATION != SURFACE_MORPHOLOGY_INFERENCE
PDLMA_FORM != PROJECT_ORTHOGRAPHIC_SURFACE
NO_STRICT != NEGATIVE_EVIDENCE
MULTIPLE_STRICT != AUTO_DISAMBIGUATION
RELATION_RETRIEVAL != GENERATION_LICENSE
RELATION_RETRIEVAL != CORRECTION_LICENSE
RELATION_RETRIEVAL != ORTHOGRAPHIC_AUTHORITY
RELATION_RETRIEVAL != RULE_DISCOVERY
```

La capa no cambia `matched_token_count`, cobertura exacta, `analysis_status` ni las decisiones de las capas anteriores.
