# NUCLEO_CONVERSACIONAL_001 — EXACT SCOPE v1

## Estado

```text
SCOPE_ID = NC001_EXACT_SCOPE_v1
SCOPE_STATUS = FROZEN_FOR_MATERIAL_SELECTION
ARCHITECTURE = DIDXAZA_ARCH_V1_1_FREEZE_2026-08-28
CANONICAL_PREDECESSOR = v0.2.15.3
TARGET_COMMUNITY = JUCHITAN
HOLDOUT_CONTENT = NOT_ACQUIRED_OR_EXPOSED
COR001_ROLE = ANALYSIS_TARGET_ONLY
```

Este documento **no amplía la arquitectura v1.1**. Materializa el alcance exacto del vertical slice autorizado por `SINTESIS_ADVERSARIAL_ARQUITECTURA_DIDXAZA_v1_1_CORREGIDA.md` y por `ARCHITECTURE_FREEZE_v1_1.md` para permitir selección material sin deriva.

## 1. Propósito demostrable

`NUCLEO_CONVERSACIONAL_001` debe demostrar un ciclo real y trazable:

```text
SOURCE_ATTESTATION / SPEAKER_ATTESTATION
-> ANALYZER
-> AnalysisBundle
-> candidate/orthographic policy when applicable
-> LICENSED_GENERATOR only when construction + cells + slot fillers are licensed
-> TUTOR explanation
-> speaker judgment
-> evidence recording without laundering
```

No se exige que las seis construcciones tengan generación habilitada si hacerlo requeriría una categoría fuera del scope. `ABSTAIN(reason)` es salida correcta y bloqueante cuando falta licencia.

## 2. Target lingüístico y documental

```text
COMMUNITY_SCOPE = JUCHITAN
REGISTER = contemporary everyday conversational use
PRIMARY_MODE = spoken interaction
ORTHOGRAPHIC_OUTPUT = policy-mediated, never inferred from PDLMA
SOURCE_PRIORITY_FOR_SELECTION = existing runtime assets first
```

`SOURCE_COVERAGE != DIALECT_SCOPE` sigue vigente. Una forma de Dictionaria sin anclaje suficiente a Juchitán puede aportar análisis o candidatura, pero no licencia por sí sola una superficie para el target del slice.

Pickett puede aportar evidencia histórica/documental juchiteca; no se convierte por ello en norma contemporánea automática.

## 3. Inventario verbal

```text
FINAL_VERB_COUNT = 12..20
REQUIRED_DOCUMENTED_CLASSES >= 2
TARGET_TAM = HABITUAL | COMPLETIVE
TARGET_PERSON = 1SG | 2SG | 3SG_HUMAN
```

La selección final debe priorizar verbos de alta utilidad conversacional con clase documentada y buena evidencia ya existente en Dictionaria/Pickett/runtime.

### 3.1 Semántica de “alta frecuencia” en esta fase

Los activos localizados no contienen un conteo corpus-frecuencial comparable que autorice afirmar frecuencia estadística. Por tanto, antes del corpus oral de desarrollo:

```text
HIGH_FREQUENCY = NOT_MEASURED
SELECTION_PROXY = HIGH_CONVERSATIONAL_UTILITY + DOCUMENTARY_COVERAGE
```

No se fabricará un ranking numérico de frecuencia. La frecuencia empírica podrá medirse después sobre corpus de desarrollo independiente.

### 3.2 Paradigmas

`ParadigmTable_v1` no completa paradigmas por analogía.

Para cada combinación:

```text
verb x TAM x person
```

sólo son válidos:

```text
ATTESTED(evidence_id)
UNATTESTED
```

`UNATTESTED` no es error ni invitación a reconstrucción.

## 4. Construcciones materiales autorizadas

`ConstructionInventory_v1` tendrá exactamente seis entradas de nivel slice.

### C01 — VERBAL_ASSERTION_SIMPLE

**Función:** afirmación declarativa positiva con un predicado verbal principal.

Incluye:
- un predicado verbal léxico;
- HABITUAL o COMPLETIVE;
- 1SG, 2SG o 3SG_HUMAN;
- participantes sólo cuando la valencia del verbo esté documentada.

Excluye:
- negación;
- interrogación;
- subordinación;
- imperativos;
- causativos generados por analogía;
- auxiliares/movimiento no licenciados;
- foco/tópico generado sin patrón documentado.

**Generator:** `ENABLED_IF_LICENSED`.

### C02 — VERBAL_NEGATION_BASIC

**Función:** negación declarativa básica de un evento.

Incluye sólo patrones negativos directamente documentados cuya realización verbal usada por el generador permanezca dentro de HABITUAL/COMPLETIVE.

Excluye de generación:
- prohibiciones/mandatos negativos;
- `todavía no`;
- negaciones que seleccionen POTENTIAL o IRREALIZED;
- negación de posibilidad/capacidad, existencia o participante cuando requiera otra construcción.

El ANALYZER puede reconocer material fuera de este subconjunto, pero el GENERATOR debe devolver `ABSTAIN(TAM_OR_CONSTRUCTION_OUT_OF_SCOPE)`.

**Generator:** `ENABLED_IF_LICENSED_WITHIN_H_C`.

### C03 — POLAR_QUESTION_BASIC

**Función:** pregunta genuina de información con respuesta sí/no.

Incluye:
- predicado verbal simple;
- HABITUAL o COMPLETIVE;
- 1SG, 2SG o 3SG_HUMAN;
- partícula/orden/realización interrogativa sólo cuando estén documentados.

Excluye:
- peticiones, ofertas, sugerencias o confirmaciones pragmáticas disfrazadas de pregunta;
- preguntas incrustadas;
- interrogación inferida sólo por `?` o entonación.

**Generator:** `ENABLED_IF_LICENSED`.

### C04 — CONTENT_QUESTION_BASIC

**Función:** pregunta genuina que solicita un contenido explícito.

Subdominios permitidos a nivel de representación:

```text
PERSON | THING | PLACE | QUANTITY | MANNER | CAUSE
```

Cada palabra/partícula interrogativa y cada patrón sintáctico debe estar licenciado individualmente; la pertenencia a un subdominio no autoriza sustitución libre entre interrogativos.

Excluye:
- preguntas indirectas;
- interrogativas retóricas;
- uso pragmático como petición/oferta;
- traducción palabra-por-palabra de interrogativos españoles.

**Generator:** `ENABLED_ONLY_FOR_AUTHORIZED_INTERROGATIVE_FILLERS`.

### C05 — BASIC_POSSESSION

**Función:** una relación posesiva simple con un poseído y un poseedor.

Estrategias reconocidas, sólo con clase nominal/evidencia documentada:

```text
XH_X_PREFIX
INHERENTLY_POSSESSED
XTI_LINKER
```

Incluye:
- un solo poseído;
- un solo poseedor;
- poseedor 1SG, 2SG o 3SG_HUMAN cuando la realización esté atestiguada.

Excluye:
- cadenas posesivas anidadas;
- relativas/demostrativos añadidos;
- inferencia de clase posesiva;
- generación de cambios morfofonológicos no atestiguados.

**Generator:** `ENABLED_IF_NOUN_CLASS_AND_SURFACE_LICENSED`.

### C06 — DESIRE_WANT_COMPLEMENT

**Función:** verbo equivalente a querer/desear con complemento oracional y sujeto correferente cuando así lo exige el patrón documentado.

El JLC documenta que el complemento de `querer` selecciona POTENTIAL. POTENTIAL está fuera del `TARGET_TAM` congelado de NC001.

Por tanto:

```text
ANALYZER = IN_SCOPE
TUTOR = IN_SCOPE
CONSTRUCTION_RECOGNITION = IN_SCOPE
FREE_GENERATION = DISABLED_IN_NC001_v1
GENERATOR_RESULT = ABSTAIN(DEPENDENT_POTENTIAL_OUT_OF_SCOPE)
```

No se añade POTENTIAL a `ConceptMapping_v1` para resolver esta tensión. Tampoco se calca el español `que`.

## 5. Matriz de capacidad por construcción

| Construction | Analyze | Tutor | Licensed generation | Corpus generation |
|---|---|---|---|---|
| C01 VERBAL_ASSERTION_SIMPLE | YES | YES | CONDITIONAL | CONDITIONAL |
| C02 VERBAL_NEGATION_BASIC | YES | YES | CONDITIONAL H/C ONLY | CONDITIONAL |
| C03 POLAR_QUESTION_BASIC | YES | YES | CONDITIONAL | CONDITIONAL |
| C04 CONTENT_QUESTION_BASIC | YES | YES | CONDITIONAL PER FILLER | CONDITIONAL |
| C05 BASIC_POSSESSION | YES | YES | CONDITIONAL PER NOUN CLASS | CONDITIONAL |
| C06 DESIRE_WANT_COMPLEMENT | YES | YES | NO — REQUIRED ABSTENTION | NO FREE RECOMBINATION |

`CONDITIONAL` significa: construcción + lexical slot + morphological cell + orthographic realization + target scope deben estar licenciados por evidencia admisible.

## 6. ConceptMapping_v1

En NC001 v1 sólo se materializa:

```text
dimension = TAM
canonical_concepts = HABITUAL | COMPLETIVE
```

Mapeos de otras categorías pueden ser referenciados desde activos existentes, pero no se crea una ontología nueva para persona, valencia, interrogación o posesión durante este slice.

## 7. OrthographicProfile_v1_DRAFT

Sólo puede contener decisiones requeridas por las formas realmente seleccionadas.

No es norma global. Cada decisión requiere `AdoptionRecord` y provenance existente.

No autoriza:
- strip-tone;
- strip-accent;
- PDLMA->surface;
- near-match->surface;
- normalización destructiva;
- reglas globales de clíticos/compuestos no adjudicadas.

Si una superficie necesaria sigue abierta: `ABSTAIN(ORTHOGRAPHIC_POLICY_UNRESOLVED)`.

## 8. Corpus oral de desarrollo

```text
SIZE = 120..180 utterances
MODE = audio-first
COMMUNITY = Juchitan
STATUS = DEVELOPMENT_EVIDENCE
```

Objetivo de cobertura, no cuota artificial:
- las seis construcciones deben aparecer cuando resulten naturales;
- las tres personas deben estar representadas;
- HABITUAL y COMPLETIVE deben estar representados;
- los verbos seleccionados deben obtener ejemplos naturales suficientes para analizar cobertura;
- no forzar una forma si el hablante la rechaza o reformula.

El corpus de desarrollo puede modificar inventarios sólo como `SPEAKER_ATTESTATION` debidamente registrada. Nunca se mezcla con el holdout.

## 9. Holdout

`HOLDOUT_CONVERSATIONAL_001` permanece completamente separado.

Este scope se definió sin inspeccionar contenido de holdout.

El holdout puede contener material fuera de NC001; esos casos prueban abstención y no autorizan expansión durante la evaluación.

## 10. Criterio de éxito del slice

NC001 no usa score global.

Debe demostrar documentalmente:
- análisis correcto de material dentro de alcance cuando hay evidencia;
- abstención específica cuando falta licencia;
- generación de al menos parte del slice mediante recombinación licenciada, sin paradigma inferido;
- tutoría trazable a análisis/evidencia;
- preservación de superficies originales;
- ausencia de evidence laundering;
- juicio de hablantes registrado por caso/juez, no agregado a confianza global.

## 11. Fuera de alcance

Además de lo ya congelado por arquitectura:
- PROGRESSIVE, PERFECT, POTENTIAL, IRREALIZED, FUTURE, STATIVE como paradigmas generativos del slice;
- plural como dimensión productiva;
- 3SG_ANIMAL / 3SG_THING;
- cortesía/honoríficos como sistema nuevo;
- coordinación/subordinación general fuera de C06 recognition;
- relativas;
- imperativos;
- causativos productivos;
- referencia discursiva de larga distancia;
- norma ortográfica global;
- resolución dialectal amplia.

## 12. Siguiente operación autorizada

```text
PREPARE_AND_EXECUTE_VERB_SELECTION(12..20)
-> MATERIALIZE_6_CONSTRUCTION_ENTRIES
```

Aplicar antes:

```text
REUSE_BEFORE_REEXTRACT
EXISTING_SCHEMA -> GAP_ANALYSIS -> EXTEND/MIGRATE
```
