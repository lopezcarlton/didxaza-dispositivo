# BIB065 — Bueno Holle 2019: matriz de ingestión normalizada v0.36.1

**Estado:** cierre bibliográfico reparado. Esta versión supersede la matriz v0.36 para planificación actual, sin borrar el histórico.

## Contrato canónico
- `epistemic_status` usa únicamente el vocabulario de guardrails v0.35: `SOURCE_ASSERTED_CONSTRAINT`, `SOURCE_REPORTED_TENDENCY`, `SOURCE_ATTESTED_PATTERN`, `SOURCE_HYPOTHESIS`, `PROJECT_DERIVATION`, `SPEAKER_ATTESTATION`.
- La granularidad previa se conserva en `epistemic_detail`; no se pierde información.
- `promotion_status` distingue registro/adjudicación/validación/bloqueo; ya no significa ambiguamente «implementar runtime».
- `empirical_scope` separa el alcance real de la evidencia de la mera referencia bibliográfica.
- La ausencia de contexto nunca bloquea el análisis local.
- Ninguna tendencia de corpus se convierte automáticamente en corrección o regla generativa.

## Conteo por estatuto epistemológico
- `PROJECT_DERIVATION`: **2**
- `SOURCE_ASSERTED_CONSTRAINT`: **1**
- `SOURCE_ATTESTED_PATTERN`: **9**
- `SOURCE_HYPOTHESIS`: **7**
- `SOURCE_REPORTED_TENDENCY`: **9**

## Conteo por promoción
- `BACKLOG_ONLY`: **1**
- `BLOCKED_FROM_EXECUTION`: **1**
- `READY_FOR_ADJUDICATION`: **3**
- `REQUIRES_ORAL_VALIDATION`: **10**
- `SAFE_TO_RECORD_NOW`: **13**

## Matriz
| ID | Dominio | Hallazgo | Estatuto | Detalle | Alcance empírico | Promoción |
|---|---|---|---|---|---|---|
| `BH2019-METH-01` | metodología | El análisis de estructura informativa se apoya en una combinación de habla espontánea, elicitación y juicios de hablantes; los métodos responden preguntas distintas. | `SOURCE_ATTESTED_PATTERN` | `documented_method` | fieldwork_methodology; spontaneous_speech; elicitation; speaker_judgments | `SAFE_TO_RECORD_NOW` |
| `BH2019-METH-02` | metodología | El habla espontánea puede revelar palabras y estructuras que no emergen al traducir desde una lengua de contacto. | `SOURCE_HYPOTHESIS` | `author_methodological_claim` | fieldwork_methodology; spontaneous_speech; elicitation; speaker_judgments | `SAFE_TO_RECORD_NOW` |
| `BH2019-METH-03` | metodología | La elicitación con estímulos no lingüísticos sirve para provocar construcciones raras sin imponer una oración de traducción. | `SOURCE_ATTESTED_PATTERN` | `documented_method` | fieldwork_methodology; spontaneous_speech; elicitation; speaker_judgments | `SAFE_TO_RECORD_NOW` |
| `BH2019-PROS-01` | prosodia | La unidad de entonación es una unidad útil de análisis del habla; sus fronteras se identifican mediante múltiples pistas, no por pausa sola. | `SOURCE_ATTESTED_PATTERN` | `analytic_frame` | naturally_occurring_discourse; elicited_phonology_background | `SAFE_TO_RECORD_NOW` |
| `BH2019-PROS-02` | prosodia | La realización superficial de tono, duración, glotalización/laringización y estrés puede variar según posición prosódica y habla continua. | `SOURCE_REPORTED_TENDENCY` | `documented_generalization` | naturally_occurring_discourse; elicited_phonology_background | `SAFE_TO_RECORD_NOW` |
| `BH2019-SYN-01` | sintaxis | El orden más común es verbo–sujeto–objeto, pero ZAI no es rígidamente verbo-inicial. | `SOURCE_REPORTED_TENDENCY` | `documented_generalization` | mixed_documented_examples; corpus_examples; prior_grammar | `SAFE_TO_RECORD_NOW` |
| `BH2019-SYN-02` | estructura informativa | La posición preverbal es un locus privilegiado para varias funciones discursivas, no una etiqueta unívoca de foco. | `SOURCE_REPORTED_TENDENCY` | `documented_generalization` | mixed_documented_examples; corpus_examples; prior_grammar | `SAFE_TO_RECORD_NOW` |
| `BH2019-REF-01` | referencia | La elección de forma nominal se correlaciona con accesibilidad: referentes menos accesibles tienden a expresiones más plenas; los más accesibles, a formas más reducidas. | `SOURCE_HYPOTHESIS` | `documented_tendency` | Pear_Story_narratives; seven_bilingual_adults; Juchitan | `REQUIRES_ORAL_VALIDATION` |
| `BH2019-REF-02` | referencia | Los referentes nuevos del corpus analizado se introducen con NPs léxicas; la distribución favorece O y S y evita A. | `SOURCE_REPORTED_TENDENCY` | `corpus_tendency` | Pear_Story_narratives; seven_bilingual_adults; Juchitan | `REQUIRES_ORAL_VALIDATION` |
| `BH2019-REF-03` | referencia | El rol S puede funcionar como zona de introducción o reintroducción, especialmente en fronteras de episodio. | `SOURCE_REPORTED_TENDENCY` | `corpus_tendency` | Pear_Story_narratives; seven_bilingual_adults; Juchitan | `REQUIRES_ORAL_VALIDATION` |
| `BH2019-REF-04` | referencia | Accesibilidad, topicalidad, foco y saliencia temática están relacionadas pero no son equivalentes. | `SOURCE_REPORTED_TENDENCY` | `author_conclusion` | Pear_Story_narratives; seven_bilingual_adults; Juchitan | `SAFE_TO_RECORD_NOW` |
| `BH2019-COREF-01` | correferencia | Las formas de tercera persona explícita y cero muestran restricciones locales de correferencia distintas en reflexivos y cláusulas dependientes/adverbiales. | `SOURCE_ASSERTED_CONSTRAINT` | `documented_constraint_pattern` | elicited_or_constructed_examples; Marlett_Pickett_examples; syntactic_judgments | `READY_FOR_ADJUDICATION` |
| `BH2019-COREF-02` | correferencia | En cláusula principal, la elección =be/∅ puede depender de la saliencia temática relativa de participantes de tercera persona. | `SOURCE_REPORTED_TENDENCY` | `discourse_tendency` | Pear_Story_narratives; spontaneous_conversation | `REQUIRES_ORAL_VALIDATION` |
| `BH2019-FOC-01` | foco | Foco de predicado y foco de oración son consistentemente verbo-iniciales en los datos analizados. | `SOURCE_REPORTED_TENDENCY` | `documented_generalization` | elicited_contexts; discourse_examples; spontaneous_conversation | `REQUIRES_ORAL_VALIDATION` |
| `BH2019-FOC-02` | foco | El foco de argumento puede ser preverbal o verbo-inicial; existe una fuerte preferencia por la posición preverbal. | `SOURCE_HYPOTHESIS` | `documented_tendency` | elicited_contexts; discourse_examples; spontaneous_conversation | `READY_FOR_ADJUDICATION` |
| `BH2019-FOC-03` | foco | No se encuentra evidencia de pitch accent directamente asociado al material focal; el orden de constituyentes cumple un papel mayor. | `SOURCE_ATTESTED_PATTERN` | `negative_result` | elicited_contexts; discourse_examples; spontaneous_conversation | `SAFE_TO_RECORD_NOW` |
| `BH2019-FOC-04` | foco | En ciertas construcciones de foco de argumento, nga se asocia con una lectura identificacional/exhaustiva. | `SOURCE_HYPOTHESIS` | `construction_specific_analysis` | elicited_contexts; discourse_examples; spontaneous_conversation | `REQUIRES_ORAL_VALIDATION` |
| `BH2019-TOP-01` | tópico | Las construcciones presentacionales, topic-comment, identificacionales, topicalizadas y desprendidas cumplen funciones distintas y pueden compartir rasgos superficiales. | `SOURCE_ATTESTED_PATTERN` | `construction_set` | narrative_and_conversation; discourse_examples | `SAFE_TO_RECORD_NOW` |
| `BH2019-TOP-02` | tópico | Un sujeto preverbal con retomación pronominal correferente puede corresponder a topicalización, no a foco de argumento. | `SOURCE_ATTESTED_PATTERN` | `construction_pattern` | narrative_and_conversation; discourse_examples | `READY_FOR_ADJUDICATION` |
| `BH2019-TOP-03` | tópico | Las construcciones desprendidas/la-marked pueden establecer marcos personales, temporales, espaciales o conceptuales y requieren referentes suficientemente accesibles. | `SOURCE_REPORTED_TENDENCY` | `documented_generalization` | narrative_and_conversation; discourse_examples | `REQUIRES_ORAL_VALIDATION` |
| `BH2019-LA-01` | partícula la | la es multifuncional: aparece en tópicos/promoción, scene-setting, cambios o fronteras tópicas, contraste y preguntas sí/no. | `SOURCE_ATTESTED_PATTERN` | `documented_distribution` | conversation; adverbial_and_conditional_examples; polar_questions | `SAFE_TO_RECORD_NOW` |
| `BH2019-LA-02` | partícula la | Bueno Holle propone que el la final de preguntas sí/no y el la discursivo son el mismo morfema. | `SOURCE_HYPOTHESIS` | `author_analysis_hypothesis` | conversation; adverbial_and_conditional_examples; polar_questions | `REQUIRES_ORAL_VALIDATION` |
| `BH2019-LA-03` | partícula la | Bueno Holle propone como función unificadora la negociación/organización del common ground y de la interacción. | `SOURCE_HYPOTHESIS` | `high_level_author_analysis` | conversation; adverbial_and_conditional_examples; polar_questions | `BLOCKED_FROM_EXECUTION` |
| `BH2019-CONV-01` | conversación | La secuencia predicate focus→argument focus puede formar una construcción quiástica en dos IUs, prolongar el turno y contribuir a su cierre. | `SOURCE_ATTESTED_PATTERN` | `conversational_pattern` | spontaneous_conversation; paired_intonation_units | `REQUIRES_ORAL_VALIDATION` |
| `BH2019-GEN-01` | generación | Una misma proposición puede requerir empaquetamientos distintos según common ground, presuposición, foco, tópico y estado referencial. | `PROJECT_DERIVATION` | `project_derivation_from_bh2019` | project_derivation_from_multiple_BH2019_findings | `SAFE_TO_RECORD_NOW` |
| `BH2019-PED-01` | pedagogía | La progresión debe enseñar operaciones discursivas (introducir, mantener, reintroducir, focalizar, topicalizar, contrastar) además de estructuras de frase. | `PROJECT_DERIVATION` | `pedagogical_derivation` | project_derivation_from_multiple_BH2019_findings | `BACKLOG_ONLY` |
| `BH2019-OPEN-01` | hueco | El uso del enclítico de objeto inanimado en funciones tópicas aparece como observación informal/inconsistente y el autor pide más investigación. | `SOURCE_HYPOTHESIS` | `explicit_open_question` | author_stated_limit_or_open_question | `REQUIRES_ORAL_VALIDATION` |
| `BH2019-OPEN-02` | hueco | La extensión de varios patrones a otros géneros, hablantes y contextos requiere más evidencia natural. | `SOURCE_ATTESTED_PATTERN` | `explicit_limitation` | author_stated_limit_or_open_question | `SAFE_TO_RECORD_NOW` |

## Bloqueos explícitos preservados
- No `PREVERBAL = FOCUS`.
- No `la = TOPIC_MARKER`.
- No `nga = EMPHASIS`.
- No `=be = referente principal` / `∅ = secundario`.
- No contexto obligatorio.
- No IU obligatoria.
- No frecuencia A/S/O convertida en gramaticalidad.
- No reestructuración de P1–P5 todavía.
