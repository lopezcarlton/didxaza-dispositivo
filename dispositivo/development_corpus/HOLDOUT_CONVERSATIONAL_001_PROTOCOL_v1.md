# HOLDOUT_CONVERSATIONAL_001 — PROTOCOLO v1

## Estado

```text
PROTOCOL_ID = HOLDOUT_CONVERSATIONAL_001_PROTOCOL_v1
PROTOCOL_STATUS = SEALED
PROTOCOL_FREEZE_DATE = 2026-08-28
TIMEZONE = America/Mexico_City
ARCHITECTURE = DIDXAZA v1.1 FROZEN
HOLDOUT_CONTENT_STATUS = NOT_YET_ACQUIRED_OR_SEALED
```

Este protocolo se congela **antes de adquirir/seleccionar/analizar** el contenido evaluativo. El hash del archivo se guarda en un sidecar `.sha256` para que el protocolo pueda verificarse sin autorreferencia.

## 1. Propósito

`HOLDOUT_CONVERSATIONAL_001` será la primera prueba nueva e independiente de generalización de `NUCLEO_CONVERSACIONAL_001`.

Debe responder dos preguntas distintas:

1. ¿el slice reutiliza conocimiento y evidencia ya licenciados para analizar/generar correctamente en conversación nueva?;
2. ¿se abstiene correctamente cuando el caso excede su licencia?

No sirve para descubrir reglas, completar paradigmas, definir ortografía ni reparar el sistema durante la evaluación.

## 2. Separación absoluta de COR001

```text
COR001_ROLE = ANALYSIS_TARGET_ONLY
HOLDOUT_CONVERSATIONAL_001_ROLE = FROZEN_GENERALIZATION_EVALUATION
```

COR001 no aporta ítems, respuestas esperadas, criterios de selección ni reglas al holdout.

## 3. Criterios de elegibilidad del contenido

Todo contenido debe ser:

- nuevo respecto de los materiales usados para construir el proyecto;
- producido por hablante(s) de Juchitán para esta adquisición;
- cotidiano y conversacional;
- audio-first;
- no copiado de COR001, Gramática Popular, Xneza, Dictionaria, Pickett, Biyubi u otros textos del proyecto;
- no generado por el sistema;
- no corregido previamente por el sistema.

Se prefieren microdiálogos o interacción entre hablantes. Si sólo es posible una producción individual, debe registrarse como tal y conservarse el carácter conversacional de la tarea.

## 4. Diseño de prompts de adquisición

Los prompts deben describir **situaciones, intenciones o tareas comunicativas**, no ofrecer una frase didxazá que el hablante deba repetir.

Evitar:

- sugerir grafías candidatas;
- pedir que el hablante adapte ejemplos del corpus de desarrollo;
- construir cada frase como traducción palabra-por-palabra desde español;
- orientar al hablante hacia una forma para cubrir una celda deseada.

Los prompts pueden usar español como instrucción de situación, pero la producción objetivo debe ser libre dentro de la situación.

## 5. Unidad y tamaño de adquisición

Unidad primaria:

```text
CONVERSATION_UNIT = microdiálogo / episodio conversacional completo
```

Plan congelado:

```text
TARGET_CONVERSATION_UNITS = 10
EXPECTED_UTTERANCES_PER_UNIT = 4..8
EXPECTED_TOTAL_UTTERANCES = 40..80
MINIMUM_CLEAN_UNITS_FOR_VALID_EVALUATION = 8
```

No se seleccionarán frases individuales post hoc porque “salieron bien” o porque contienen una construcción útil. Se conserva la unidad conversacional completa.

## 6. Metadata mínima

Por sesión/unidad:

```text
holdout_id
conversation_unit_id
recording_session_id
speaker_ids[]
speaker_role[]
community = JUCHITAN  # sólo cuando esté documentado
acquisition_date
prompt_id
prompt_text
interaction_type
register
recording_file_ids[]
notes_nonlinguistic
```

Por utterance, después del sellado de adquisición:

```text
utterance_id
conversation_unit_id
speaker_id
start_time
end_time
rough_transcription
speaker_confirmed_meaning
speaker_naturalness_judgment
```

La validación del contenido hablado y la validación ortográfica son roles distintos, aunque una misma persona pueda ejercer ambos si se registra explícitamente.

## 7. Audio-first y preservación

El `audio_master` es evidencia primaria de producción.

Reglas:

- conservar el master original;
- cualquier copia de escucha/procesada recibe un ID distinto;
- no sobrescribir el master;
- no derivar ortografía automáticamente de continuidad acústica;
- reducción fonética, pausa o ausencia de pausa no deciden espacios;
- `audio_surface -> spelling_correction` está prohibido.

## 8. Sellado en dos etapas

### 8.1 ACQUISITION_SEAL

Se realiza antes de análisis lingüístico del holdout.

Incluye:

- audio master;
- metadata de sesión;
- prompts usados;
- límites de `CONVERSATION_UNIT` cuando sean puramente de sesión/interacción.

Crear:

```text
HOLDOUT_CONVERSATIONAL_001_ACQUISITION_MANIFEST.sha256
```

con SHA-256 por archivo y un hash del manifest.

### 8.2 EVALUATION_INPUT_SEAL

Después de la escucha/transcripción básica y confirmación del hablante, pero **antes de ejecutar el sistema contra el holdout**.

Incluye:

- rough transcription preservando marcas observadas;
- segmentación temporal;
- significado confirmado por hablante;
- notas de naturalidad/alternativas del hablante;
- vínculo a audio master.

Crear:

```text
HOLDOUT_CONVERSATIONAL_001_EVAL_INPUT_MANIFEST.sha256
```

Ninguna salida del sistema puede entrar en este bundle.

## 9. Momento de apertura

El holdout permanece `SEALED_UNSEEN` mientras se construyen y depuran, exclusivamente con datos no-holdout:

- `ConstructionInventory_v1`;
- `ParadigmTable_v1`;
- `ConceptMapping_v1`;
- `OrthographicProfile_v1_DRAFT`;
- candidate/generation slice;
- tests internos del slice.

Antes de abrir el holdout deben quedar congelados por hash:

```text
SYSTEM_SNAPSHOT
ConstructionInventory_v1
ParadigmTable_v1
ConceptMapping_v1
OrthographicProfile_v1_DRAFT
HOLDOUT_EVAL_CRITERIA_v1
```

`HOLDOUT_EVAL_CRITERIA_v1` se define a partir del alcance exacto del slice y **sin inspeccionar el contenido del holdout**.

## 10. Prohibiciones de contaminación

Mientras el estado sea `SEALED_UNSEEN`, ningún dato del holdout puede:

- entrar en `ConstructionInventory`;
- completar `ParadigmTable`;
- definir o modificar `OrthographicProfile`;
- definir `ConceptMapping`;
- entrar en `ValidationQueue` de desarrollo;
- convertirse en ejemplo de prompt;
- convertirse en test de desarrollo;
- servir para descubrir reglas;
- servir para ajustar ranking/candidates;
- servir para tuning/fine-tuning;
- licenciar generación.

Guard conceptual:

```text
HOLDOUT_EVIDENCE_CAN_EVALUATE_SYSTEM
HOLDOUT_EVIDENCE_CANNOT_LICENSE_SYSTEM_DURING_SAME_EVALUATION
```

## 11. Evaluación sin score global

No se calcula un `global confidence` ni un score único de “qué tan bien habla didxazá”.

Se reporta un vector de resultados por capacidad y por unidad:

```text
ANALYSIS:
- SUPPORTED_ANALYSIS
- PARTIAL_ANALYSIS
- JUSTIFIED_ABSTENTION
- UNSUPPORTED_ASSERTION

NORMALIZATION:
- NO_CHANGE_SUPPORTED
- NORMALIZATION_SUPPORTED
- DOCUMENTED_VARIANT
- ORTHOGRAPHICALLY_UNRESOLVED
- UNAUTHORIZED_INTERVENTION

GENERATION:
- LICENSED_GENERATION
- JUSTIFIED_ABSTENTION
- UNATTESTED_CELL_USED
- UNLICENSED_CONSTRUCTION_USED

TUTOR:
- EXPLANATION_SUPPORTED
- PROVENANCE_MISSING
- EXPLANATION_OVERCLAIM
```

Se conservan conteos/desgloses, pero no se colapsan en una cifra única de confianza lingüística.

## 12. Blockers de evaluación

Son fallas bloqueantes, independientemente de cualquier otro resultado:

```text
EVIDENCE_LAUNDERING > 0
DERIVED_FORM_LICENSES_ITSELF > 0
UNATTESTED_PARADIGM_CELL_USED > 0
ORIGINAL_SURFACE_LOST > 0
PDLMA_PROMOTED_TO_EXACT_SURFACE > 0
NEAR_MATCH_PROMOTED_TO_EXACT_SURFACE > 0
TONE_STRIPPED_FOR_EXACT_SURFACE > 0
```

Una abstención explícita no es falla por sí misma.

Para impedir que “abstenerse de todo” cuente como éxito, el cierre del slice deberá incluir cobertura útil mínima por las capacidades realmente congeladas en `HOLDOUT_EVAL_CRITERIA_v1`, fijada antes de abrir el holdout.

## 13. Juicio de hablantes

Los juicios se registran por juez/ítem, por ejemplo:

```text
NATURAL
ACCEPTABLE
MARKED_BUT_POSSIBLE
UNNATURAL
MEANING_MISMATCH
UNSURE
```

Registrar también alternativas espontáneas cuando se ofrezcan.

No convertir acuerdo entre jueces en “verdad” por mayoría ni en score global de confianza. El desacuerdo se conserva como dato.

## 14. Contaminación accidental

Si una `CONVERSATION_UNIT` se expone al desarrollo antes de la evaluación:

```text
unit_status = CONTAMINATED
```

La unidad completa queda fuera del cálculo evaluativo; no se rescatan utterances individuales.

No se reemplaza post hoc con una unidad elegida después de ver resultados.

Si quedan menos de 8 unidades limpias:

```text
HOLDOUT_CONVERSATIONAL_001 = INVALIDATED
CREATE_FRESH_HOLDOUT = REQUIRED
```

## 15. Estado después de la primera apertura

Después de la primera evaluación:

```text
HOLDOUT_STATE = EVALUATED_SPENT
```

Puede conservarse para trazabilidad y comparación descriptiva histórica, pero si el sistema se modifica a partir de sus fallos deja de ser evidencia fresca de generalización.

Para demostrar nueva generalización tras reparaciones guiadas por sus resultados:

```text
CREATE HOLDOUT_CONVERSATIONAL_002
```

## 16. Qué hacer si el holdout revela un hueco

Flujo permitido:

```text
holdout failure
-> classify gap
-> seek independent source/speaker evidence outside holdout
-> modify system only from independent evidence
-> run internal tests
-> use a new fresh holdout for new generalization claim
```

Flujo prohibido:

```text
holdout answer
-> copy rule/form into inventories
-> rerun same holdout
-> claim generalization
```

## 17. Relación con el vertical slice

Este protocolo no fija todavía el inventario exacto de verbos ni las seis construcciones materiales. Eso corresponde al siguiente paso operativo: `DEFINE_EXACT_SCOPE(NUCLEO_CONVERSACIONAL_001)`.

Sí quedan congelados los límites arquitectónicos ya adjudicados:

```text
TAM = HABITUAL | COMPLETIVE
PERSON = 1SG | 2SG | 3SG_HUMAN
VERBS = 12..20, >= 2 documented classes
INITIAL_CONSTRUCTIONS = 6
DEVELOPMENT_ORAL_CORPUS = 120..180 utterances
```

El holdout puede contener naturalmente material fuera del slice. Esos casos sirven para probar abstención; no autorizan expansión del sistema durante la misma evaluación.

## 18. Criterio de integridad

El protocolo se considera correctamente aplicado sólo si puede reconstruirse documentalmente:

```text
what was frozen
when it was frozen
what the system had seen
what it had not seen
which artifacts licensed each output
which holdout items were clean/contaminated
which speaker judgments occurred
what changed only after evaluation
```

Ese rastro es parte del resultado, no documentación opcional.
