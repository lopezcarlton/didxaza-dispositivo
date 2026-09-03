# SÍNTESIS ADVERSARIAL FINAL — ARQUITECTURA DIDXAZÁ v1.1

## Alcance

Síntesis de las propuestas de Kimi, DeepSeek y Claude, contrastadas contra el estado canónico del proyecto.

Cada propuesta se adjudica como:

`ACCEPT / MODIFY / REJECT / DEFER / EXPERIMENT`

Estado de partida:

- `CANONICAL_PREDECESSOR = v0.2.15.3`
- `COR001_ROLE = ANALYSIS_TARGET_ONLY`
- `COR001_AS_REFERENCE = PROHIBITED`
- `COR001_FOR_RULE_DISCOVERY = PROHIBITED`
- `COR001_FOR_TRAINING = PROHIBITED`
- `COR001_FOR_GOLD_EVALUATION = PROHIBITED`
- `GENERALIZATION = NEW_FROZEN_HOLDOUT_REQUIRED`

Invariantes existentes que se conservan:

- `AUTO_CORRECT = OFF`
- `VISIBLE_SUGGESTIONS = OFF`
- `EDIT_EXECUTION = OFF`
- `PDLMA_TO_SURFACE = PROHIBITED`
- `NEAR_MATCH_TO_SURFACE = PROHIBITED`
- `TONE_STRIPPING_FOR_EXACT_SURFACE = PROHIBITED`
- `GLOBAL_NUMERIC_CONFIDENCE = PROHIBITED`
- `SOURCE_COUNT_AS_CONFIDENCE = PROHIBITED`

### Corrección de rol de COR001

COR001 no funciona como benchmark, gold standard, referencia normativa ni suite de regresión.

Su único papel en esta arquitectura es:

`ANALYSIS_TARGET_ONLY`

Esto significa que COR001 puede pasarse al dispositivo para observar:

- qué reconoce;
- qué analiza;
- dónde se abstiene;
- qué contradicciones detecta;
- qué huecos del sistema quedan expuestos.

Pero sus respuestas o formas **no se usan para decidir qué es correcto** ni para ajustar el sistema.

Flujo correcto:

`COR001 item → system analysis → observe capability/gap`

Flujo prohibido:

`COR001 item → expected answer → tune system to match`

Si COR001 revela un hueco, ese hueco debe resolverse con evidencia independiente: Gramática Popular, Xneza, Dictionaria, Pickett, otras fuentes documentales o nueva evidencia de hablantes.

---

## 1. Convergencias fuertes

Las tres IAs convergen en:

1. ANALYZER como núcleo epistémico.
2. NORMALIZER sin duplicar la gramática.
3. `AnalysisBundle` como agregador de referencias.
4. `NormalizationCandidate`.
5. política ortográfica explícita.
6. alineación terminológica entre fuentes.
7. inventario ejecutable de construcciones.
8. registro material de valencia.
9. GENERATOR: estructura antes de superficie.
10. TUTOR reutilizando el análisis.
11. Biyubi útil pero no normativo.
12. distinguir original didxazá de traducciones.
13. mayor prioridad para producción oral.
14. feedback humano selectivo.
15. nuevo holdout para generalización.
16. no fine-tuning indiscriminado.

---

## 2. Adjudicación

### ANALYZER como núcleo
**ACCEPT**

No se reconstruye. Reutiliza Retrieval, Context/Provenance, Morphology I, BOUND, Morphology II, Evidence Adjudication, Surface Evidence, ResolutionVector, Person/Possession y EvidenceQualification.

### NORMALIZER como orquestador
**ACCEPT WITH MODIFICATION**

Flujo:

`candidate generation → ANALYZER → evidence/adjudication → policy → accept/suggest/abstain`

No es precondición para grabar habla, pero sí sigue siendo necesario para convertir transcripciones y otros textos en representación ortográfica consistente.

Separación obligatoria:

- `TEXT_ANALYSIS_RUNTIME: audio optional`
- `CORPUS_ACQUISITION_PIPELINE: audio may be primary evidence`

### CORRECTOR
**MODIFY**

Se conserva como capacidad de producto, pero técnicamente puede ser una proyección sin estado sobre:

`AnalysisBundle + NormalizationCandidates + OrthographicProfile`

Estados mínimos:

- `DOCUMENTED_IN_SOURCE`
- `ACCEPTED_BY_ACTIVE_PROFILE`
- `DOCUMENTED_VARIANT`
- `STYLE_PREFERENCE`
- `ORTHOGRAPHICALLY_UNRESOLVED`
- `ERROR_CONFIRMED`

### TUTOR
**MODIFY / ACCEPT**

Se conserva como capacidad de producto y se implementa como renderer del análisis.

Niveles:

- `LEVEL_1`: respuesta breve
- `LEVEL_2`: análisis morfológico/gramatical
- `LEVEL_3`: explicación completa + provenance

### GENERATOR
**ACCEPT WITH STRONG CONSTRAINTS**

Primera implementación: `LICENSED_RECOMBINATION`.

`ATTESTED_CONSTRUCTION × TYPED_SLOTS × ATTESTED_PARADIGM_CELLS × AUTHORIZED_LEXICAL_FILLERS → generated structure → orthographic realization`

Si falta una celda requerida: `ABSTAIN`.

No inferir paradigmas faltantes por analogía.

### GENERADOR DE CORPUS
**ACCEPT AS SEPARATE PIPELINE**

GENERATOR responde si puede producir una forma/estructura.
CORPUS GENERATOR decide si esa forma sirve para un objetivo pedagógico.

### AnalysisBundle
**ACCEPT**

Sólo referencias. Prohibido `bundle_confidence`.

### NormalizationCandidate
**ACCEPT**

Debe estar anclado al target y conservar la superficie original.

### OrthographicProfile
**MODIFY**

No es ranking de autoridades. Se identifica por su `policy_vector`:

- tone policy
- glottal policy
- vowel length policy
- clitic spacing policy
- compound surface policy
- variant policy

La legitimidad/adopción se registra aparte en `AdoptionRecord` por regla.

### TAMMapping
**MODIFY**

Crear schema general `ConceptMapping`, pero implementar primero sólo `dimension = TAM`.

### ConstructionRegistry
**ACCEPT**

Usar inicialmente `ConstructionInventory`.

Cada construcción debe incluir función, slots tipados, restricciones, TAM/persona autorizados, registro, ejemplos y provenance.

### ValenciaRegistry
**ACCEPT**

No crear nueva ontología; materializar relaciones concretas por lexema.

### Orchestrator
**EXPERIMENT**

Sólo routing, control de flujo y condición de terminación. Sin reglas lingüísticas.

### Segmenter / Tokenizer / Lemmatizer nuevos
**REJECT AS NEW SUBSYSTEMS**

Extender Retrieval/BOUND/Morphology si hace falta.

### Active learning
**ACCEPT AS EXPERIMENTAL SUPPORT**

Crear `ValidationQueue` para agrupar casos no resueltos por fenómeno y pedir validaciones de alto apalancamiento.

---

## 3. Invariante nueva crítica: evidencia vs derivados

Se incorpora un guard contra *evidence laundering*:

`EVIDENCE_ORIGIN = SOURCE_ATTESTATION | SPEAKER_ATTESTATION | PROJECT_NORMALIZED | PROJECT_GENERATED`

Reglas:

- `PROJECT_NORMALIZED` nunca se convierte en `SOURCE_ATTESTATION`
- `PROJECT_GENERATED` nunca se convierte en `SOURCE_ATTESTATION`

Test bloqueante:

`NO_DERIVED_FORM_CAN_LICENSE_ITSELF`

---

## 4. Biyubi: Operation Inventory

**EXPERIMENT**

Crear `ORTHOGRAPHIC_OPERATION_CANDIDATE_INVENTORY`.

Pipeline:

`align same lexeme/sense → compare exact surfaces → extract minimal difference → classify candidate operation → cross-source adjudication`

Operaciones candidatas:

- tono/diacríticos
- saltillo
- longitud vocálica
- frontera
- adjunción de clítico
- representación de reducción fonológica

Una diferencia superficial nunca se convierte directamente en regla.

---

## 5. Corrección factual a Claude

Claude propuso rediseñar el índice a spans antes de Biyubi.

**REJECT**

Retrieval v0.2.1 ya recupera multiword Headwords y usa spans. El pendiente correcto sigue siendo montar/reutilizar Biyubi + Dictionaria + Pickett en el mismo entorno y ejecutar el cross-source exacto.

---

## 6. Estrategia de adquisición oral

**ACCEPT**

Para nuevo corpus:

`speaker production → audio master → rough transcription → listening confirmation → linguistic analysis → orthographic realization → adjudication`

El hablante valida:

- qué se dijo
- significado
- naturalidad
- alternativas

La ortografía se valida mediante perfil documentado y/o escritor competente.

La misma persona puede ejercer ambos roles, pero deben registrarse por separado.

---

## 7. Textos traducidos

**MODIFY CLAUDE**

No usar `TRANSLATED_TEXT => no structural evidence`.

Sí pueden aportar evidencia estructural secundaria, además de léxico y ortografía. No pueden por sí solos licenciar naturalidad espontánea ni productividad general.

---

## 8. Holdout nuevo

**ACCEPT — PRIORIDAD ALTA**

Crear `HOLDOUT_CONVERSATIONAL_001` después de congelar el protocolo.

Debe ser nuevo, de Juchitán, cotidiano, y no entrar en ConstructionInventory, ParadigmTable, OrthographicProfile ni tuning.

Se sella por hash antes de análisis.

COR001 queda sólo como **objeto de análisis**. Puede volver a pasarse por el sistema para observar cambios de capacidad, pero nunca como referencia contra la cual se juzgue o ajuste el sistema.

---

## 9. Arquitectura v1 definitiva

### Vista de producto

Se conservan todas las capacidades:

- NORMALIZER
- ANALYZER
- CORRECTOR
- TUTOR
- GENERATOR
- CORPUS_GENERATOR

### Vista de implementación

`ANALYZER CORE → AnalysisBundle → Candidate Engine/NORMALIZER → Orthographic Policy → normalized output`

En paralelo desde AnalysisBundle:

- CORRECTOR projection
- TUTOR projection

Después:

`ConstructionInventory × AttestedParadigmCells × AuthorizedSlotFillers → LICENSED GENERATOR → CORPUS GENERATOR`

Transversal:

- `ValidationQueue`
- `ConceptMapping`
- guard de `EvidenceOrigin`

Pipeline separado:

`CORPUS ACQUISITION: audio-first → speaker confirmation → analysis → orthographic realization → adjudicated corpus`

---

## 10. Vertical slice definitivo

Nombre: `NUCLEO_CONVERSACIONAL_001`

Objetivo: demostrar el ciclo completo:

`oral evidence → analysis → orthographic realization → licensed generation → tutor explanation → speaker judgment`

sin inventar paradigmas ni blanquear datos derivados.

### Alcance

**Verbos:** 12–20 verbos de alta frecuencia, al menos 2 clases, con buena evidencia Dictionaria/Pickett.

**TAM:** sólo HABITUAL y COMPLETIVE.

**Persona:** 1SG, 2SG, 3SG_HUMAN.

**Construcciones iniciales:**
1. afirmación verbal simple
2. negación
3. pregunta polar
4. pregunta de contenido
5. posesión básica
6. deseo/querer + complemento

**Corpus oral de desarrollo:** 120–180 utterances, preferentemente microdiálogos y habla entre hablantes cuando sea posible.

**Holdout:** `HOLDOUT_CONVERSATIONAL_001`, separado desde el inicio.

---

## 11. Artefactos del slice

- `ConstructionInventory_v1` — 6 construcciones.
- `ParadigmTable_v1` — sólo celdas atestiguadas; `UNATTESTED` es valor válido.
- `ConceptMapping_v1` — sólo TAM para las categorías usadas.
- `OrthographicProfile_v1_DRAFT` — sólo decisiones necesarias para el slice, con `AdoptionRecord`.
- `NormalizationCandidate_v1`.
- `Generator_v0` — recombinación licenciada.
- `Tutor_v0`.
- `ValidationQueue_v0`.

---

## 12. Tests bloqueantes

### T1 — No evidence laundering
Una forma `PROJECT_GENERATED` o `PROJECT_NORMALIZED` no puede licenciarse como evidencia fuente.

### T2 — No inferred paradigm cell
Toda celda usada por GENERATOR debe tener `evidence_id`.

### T3 — Original preservation
Toda normalización conserva `observed_surface`.

### T4 — Abstention
Si falta construcción/celda/política: `ABSTAIN(reason)`.

### T5 — Round-trip structural
`generated structure → surface → ANALYZER` recupera rasgos compatibles.

### T6 — Speaker naturalness judgment
Comparaciones A/B, registrando acuerdo entre jueces, sin score único de naturalidad.

### T7 — COR001 observational analysis

COR001 puede ejecutarse como objeto de análisis para observar qué capacidades emergen o qué huecos persisten.

No hay respuestas esperadas, umbral de aprobación ni ajuste del sistema contra COR001.

Salida:

`observed_analysis_behavior + abstentions + unresolved phenomena + capability notes`

---

## 13. Qué NO hacer durante el slice

Congelar:

- nuevos schemas generales
- nuevos módulos de propósito general
- fine-tuning
- TTS
- nuevo retrieval
- nuevo BOUND
- generación causativa automática
- generación libre masiva
- normalización masiva de Biyubi

Bibliografía nueva sólo si desbloquea directamente un fenómeno del slice.

---

## 14. Papel de Biyubi durante el slice

No se ingiere como norma.

Usos:
1. recuperar ejemplos con los verbos elegidos
2. localizar superficies candidatas de paradigma
3. localizar construcciones candidatas
4. experimentar con `ORTHOGRAPHIC_OPERATION_CANDIDATE_INVENTORY`

Todo se contrasta.

El cross-source masivo queda como pendiente técnico separado.

---

## 15. Papel de la reunión con Irma Pineda

Puede desbloquear:

- `OrthographicProfile_v1_DRAFT`
- `AdoptionRecords`
- política de variantes
- preguntas ortográficas abiertas
- textos modelo
- especialistas
- criterios de naturalidad

No pedirle corrección manual masiva.

---

## 16. Decisiones finales

### ACCEPT
- Analyzer core
- AnalysisBundle
- NormalizationCandidate
- ConstructionInventory
- ValenciaRegistry
- audio-first acquisition
- selective speaker feedback
- new sealed holdout
- licensed recombination generator
- evidence/derived separation
- Generator != CorpusGenerator

### MODIFY
- CORRECTOR → capacidad de producto / proyección de política sin estado
- TUTOR → capacidad de producto / renderer sin estado
- OrthographicProfile → policy vector + AdoptionRecord
- TAMMapping → ConceptMapping, TAM primero
- translated texts → evidencia estructural secundaria
- NORMALIZER → no requisito para grabar habla, sí para consistencia textual

### REJECT
- nuevos Segmenter/Tokenizer/Lemmatizer
- global confidence interval
- plantilla SVO
- escritura del hablante como gold ortográfico
- BIB086–088 como norma automática
- BIB085 como fuente globalmente superior por ser original
- rediseño de spans antes de Biyubi
- inferencia abierta de paradigmas

### DEFER
- gramática computacional completa
- generación estadística general
- resolución dialectal amplia
- norma contemporánea completa más allá de políticas documentadas

### EXPERIMENT
- Orchestrator ligero
- ValidationQueue
- OrthographicOperationCandidateInventory
- ranking estadístico sólo dentro de candidatos cerrados

---

## 17. Ruta inmediata

1. Freeze architecture v1.
2. Sellar protocolo de `HOLDOUT_CONVERSATIONAL_001`.
3. Definir alcance exacto de `NUCLEO_CONVERSACIONAL_001`.
4. Seleccionar 12–20 verbos.
5. Construir 6 entradas de `ConstructionInventory`.
6. Materializar celdas atestiguadas de `ParadigmTable`.
7. Crear `ConceptMapping(TAM)`.
8. Crear `OrthographicProfile_v1_DRAFT` sólo para fenómenos requeridos.
9. Iniciar corpus oral audio-first.
10. Implementar candidate/generation slice.
11. Ejecutar juicios de hablantes.
12. Ejecutar COR001 únicamente como análisis observacional, sin usarlo como referencia ni criterio de aprobación.
13. Expandir sólo si el slice cierra.

---

## 18. Criterio de éxito

El slice no triunfa porque “corrige muchas palabras”.

Triunfa si demuestra en un dominio pequeño:

`KNOW → ANALYZE → NORMALIZE WHEN AUTHORIZED → ABSTAIN WHEN NOT AUTHORIZED → GENERATE ONLY LICENSED FORMS → EXPLAIN → RECEIVE SPEAKER JUDGMENT → LEARN AS EVIDENCE WITHOUT LAUNDERING IT`

Ese ciclo es la unidad mínima de capacidad lingüística que debe escalarse después.


---

## 19. Corrección v1.1 respecto de v1.0

Se elimina cualquier uso de COR001 como:

- benchmark;
- suite de regresión;
- gold standard;
- referencia normativa;
- fuente de respuestas esperadas.

COR001 queda exclusivamente como `ANALYSIS_TARGET_ONLY`.

La evaluación objetiva de generalización corresponde exclusivamente a un holdout nuevo e independiente.
