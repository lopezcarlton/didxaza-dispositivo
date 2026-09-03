# BENCHMARK_ISOLATION_PROTOCOL v1

## Estado

`FROZEN_FOR_COR001_DEVELOPMENT_AND_REGRESSION`

COR001 **no** se considera benchmark ciego de generalización. El core v0.27 se construyó en parte durante trabajo previo con COR001, por lo que el enmascaramiento de respuestas explícitas no puede eliminar un posible **sesgo de selección de contenido**. Para generalización se requiere un holdout nuevo, creado después de congelar el conocimiento de producción que vaya a evaluarse.

## 1. Espacios obligatoriamente separados

### PRODUCTION_KNOWLEDGE
Puede contener reglas generales, léxico, paradigmas, construcciones, ortografía y provenance. Una observación nacida en un benchmark sólo puede entrar aquí si se reformula como regla general y obtiene validación independiente o evidencia generalizable suficiente.

### BENCHMARK_INPUT
Contiene superficie didxazá y metadatos permitidos. El español de referencia puede conservarse para scoring posterior, pero queda prohibido usarlo para descubrir lema, segmentación, persona, TAM, sintaxis o corrección.

### BENCHMARK_GOLD
Contiene adjudicaciones y respuestas esperadas. Nunca es consultable antes de congelar la salida.

### AUXILIARY_EVIDENCE
Audio, revisión de hablante, vertical slices y diagnósticos previos. Se abre sólo después de la salida text-only y sirve para una evaluación enriquecida separada.

## 2. Audio

Pipeline basal obligatorio:

`TEXT → TOKENIZER → ANALYZER → CORRECTOR/TUTOR`

Pipeline opcional:

`AUDIO → TRANSCRIPTION → TEXT → MISMO ANALYZER`

Pipeline de adjudicación:

`TEXT_ANALYSIS + OPTIONAL_AUDIO/HUMAN_EVIDENCE → REVIEW`

`NO_AUDIO` nunca debe implicar `NO_ANALYSIS`. El audio puede mejorar validación y desambiguación, pero no ser dependencia del corrector textual.

## 3. Estados mínimos de corrección

- `PRESERVE`
- `UNKNOWN`
- `NON_ACTIONABLE_NEIGHBOR`
- `REVIEW_CANDIDATE`
- `VALIDATED_CORRECTION`
- `AUTO_CORRECT_ALLOWED`

Semejanza gráfica nunca basta para subir de estado.

## 4. Definición formal de COMPLETE_INDEPENDENT_ANALYSIS

Una fila sólo puede contarse como `COMPLETE_INDEPENDENT_ANALYSIS` cuando se cumplen **todos** los criterios siguientes:

1. todos los spans relevantes para la proposición tienen soporte independiente en el core o análisis autorizado por una construcción general;
2. la morfología y sintaxis necesarias se resuelven sin consultar la referencia española;
3. persona y TAM/modalidad se resuelven cuando son aplicables, o se marcan explícitamente `N/A` cuando no lo son;
4. puede generarse una lectura literal o estructuralmente fiel desde el didxazá;
5. no queda un span sin resolver capaz de cambiar materialmente la proposición o una propuesta de corrección;
6. sólo después se compara con el español para puntuar equivalencia.

Con esta rúbrica, el baseline COR001 v1 tiene `0/107 COMPLETE_INDEPENDENT_ANALYSIS`.

## 5. Leakage: categorías distintas

No volver a usar una sola cifra de “filas afectadas” sin distinguir:

- `MASKED_DIRECT_OR_CASE_SPECIFIC`: conocimiento que existía en core-as-is y fue eliminado del fixture para evitar lookup de caso. En v1: **9 filas**.
- `LATENT_GENERALIZATION_RISK`: una regla derivada del benchmark que podría beneficiar otra fila si se reintrodujera; el riesgo no se realizó en la salida blind. En v1: **5 filas**.

Total de filas relacionadas con el problema: 14, pero **9 ≠ 5 epistemológicamente**.

## 6. Negative controls reproducibles

Antes de congelar una corrida BLIND-STRICT debe ejecutarse `verify_cor001_blind_fixture_v1.py`. Debe devolver cero ocurrencias en el cuerpo lingüístico para:

- `COR001`;
- IDs `FB-###`;
- respuestas conocidas: `sacani`, `riené`, `zeenda`, `chaahui'`;
- `qui` como lexema desnudo, mientras su identificación como negación no tenga fuente independiente dentro del fixture.

El resultado de la corrida se conserva como artefacto de cadena de custodia.

## 7. Aprendizaje legítimo desde datos de desarrollo

Una observación nacida en COR001 puede volver a `PRODUCTION_KNOWLEDGE` sólo si:

1. deja de estar formulada como respuesta a FB-###;
2. se demuestra su fuente independiente/generalizable;
3. se define alcance y límites;
4. conserva provenance;
5. se prueba en material que no participó en su formulación.

`BENCHMARK_DERIVED_OBSERVATION != GENERAL_RULE`.

## 8. Función permitida de COR001

- desarrollo: **SÍ**;
- regression suite: **SÍ**;
- benchmark ciego de generalización: **NO**.

El próximo test de generalización deberá hacerse con un holdout nuevo.
