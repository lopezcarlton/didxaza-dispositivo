# PEDAGOGICAL_DISCUSSION_FREEZE_POST_BIB065_v0_36_2

## Estado del documento

```text
STATUS = FROZEN_DISCUSSION_INPUT_NOT_POLICY
AUTHORITY = NON_NORMATIVE
AUTOMATIC_GENERATOR_EFFECT = NONE
AUTOMATIC_COR002_EFFECT = NONE
AUTOMATIC_P1_P5_EFFECT = NONE
AUTOMATIC_STYLE_RULE_EFFECT = NONE
SOURCE_MOMENT = POST_BIB065_BUENO_HOLLE_2019_INTENSIVE_READING
PURPOSE = RESUME_FUTURE_PEDAGOGICAL_DISCUSSION_WITHOUT_LOSS
```

Este documento **congela ideas para discusión**. No establece una nueva metodología pedagógica, no reescribe COR002, no modifica P1–P5, no licencia construcciones del Generator y no convierte observaciones de Bueno Holle en reglas de estilo.

Su función es conservar, después de terminar la lectura intensiva de BIB065, qué preguntas e implicaciones pedagógicas se volvieron visibles y cómo se relacionan con lo que el repositorio ya había construido.

---

# 1. Dos ideas marco que deben quedar visibles al retomar la discusión

## 1.1 COR002 como material básico para principiantes

**Hipótesis de trabajo fuerte para discutir, no decisión cerrada en este documento:**

> COR002 debería mantenerse como material **básico para principiantes** y no intentar cargar desde ahora toda la complejidad discursiva, prosódica y pragmática que el proyecto vaya descubriendo.

La lectura de Bueno Holle hace todavía más evidente que una lengua conversacional completa contiene niveles de organización que pueden exceder ampliamente lo que conviene enseñar o ejercitar en un corpus inicial. Que el dispositivo llegue a modelar esos fenómenos no obliga a que COR002 los incorpore todos.

Consecuencia para la futura discusión: habrá que distinguir al menos entre:

```text
WHAT_THE_DEVICE_CAN_MODEL
WHAT_A_BEGINNER_NEEDS_NOW
WHAT_BELONGS_TO_LATER_PEDAGOGICAL_LEVELS
```

No se decide aquí dónde cae cada fenómeno.

## 1.2 Ningún material pedagógico generado se convierte automáticamente en regla de estilo

**Meta-principio de protección para la discusión pedagógica:**

> Una versión de COR002, una secuencia, una conversación, una taxonomía de dificultad, un formato de audio o una actividad pedagógica es un artefacto histórico de una metodología en evolución; su existencia no la convierte automáticamente en norma para futuras generaciones.

Esto aplica también a decisiones que funcionaron bien en un momento determinado. Deben poder revisarse a la luz de:

- nuevo conocimiento lingüístico;
- evidencia de hablantes;
- corpus oral independiente;
- experiencia real de aprendizaje;
- cambios en la arquitectura del Tutor/Generator;
- nuevos objetivos de nivel o modalidad.

Por tanto:

```text
PEDAGOGICAL_ARTIFACT != STYLE_AUTHORITY
PAST_CORPUS_OUTPUT != PEDAGOGICAL_GOLD_STANDARD
CURRENT_TEMPLATE != PERMANENT_TEMPLATE
```

Este principio no implica desechar lo anterior: exige **compararlo y discernirlo**, no heredarlo automáticamente.

---

# 2. Contraste con el repositorio actual

La revisión posterior a BIB065 no parte de cero. Varias protecciones ya existen y deben conservarse.

## 2.1 Ya estaba protegido

### `PEDAGOGICAL_BACKLOG_BH2019_PARTIAL_v0_35.md`

Ya establecía que sus consecuencias eran `PROVISIONAL_BACKLOG_NOT_AUTOMATICALLY_EXECUTABLE` y difería explícitamente:

- cualquier reescritura automática de P1–P5;
- reglas productivas nuevas de foco/tópico;
- corrección automática `=be`/cero;
- un significado global de `nga`;
- estado discursivo obligatorio;
- anotación prosódica obligatoria.

**Conclusión:** la lectura completa de BIB065 no invalida ese firewall; lo refuerza y amplía.

### `hardening/ANALYSIS_CAPABILITY_GUARDRAILS_v0_35.md`

Ya protege que:

- la frase aislada siga siendo una unidad válida;
- el contexto sólo enriquezca análisis cuando existe;
- `UNRESOLVED != INCORRECT`;
- frecuencia no equivalga a gramaticalidad;
- una sola fuente o género no se convierta en gramática global.

**Conclusión pedagógica:** ninguna propuesta futura basada en discurso debe transformar el contexto en prerrequisito del material básico ni del Analyzer.

### `development_corpus/DevelopmentCorpusProtocol_v0_35.md`

Ya permite conservar de manera no destructiva:

```text
continuous_audio -> turn -> optional intonation_unit -> later annotations
```

y distingue métodos de adquisición como conversación espontánea, estímulos no lingüísticos, traducción y juicios.

**Conclusión pedagógica:** podemos adquirir evidencia rica ahora sin decidir todavía qué parte terminará enseñándose en COR002.

## 2.2 Distinción que debe quedar explícita: NC001 no es COR002

`NUCLEO_CONVERSACIONAL_001_SCOPE_v1.md` es un **vertical slice técnico** para demostrar capacidades trazables del dispositivo. Sus seis construcciones y su scope congelado no constituyen una secuencia didáctica para principiantes y no deben convertirse por inercia en el syllabus de COR002.

```text
NC001_TECHNICAL_SCOPE != COR002_PEDAGOGICAL_SCOPE
GENERATION_LICENSE != TEACHING_PRIORITY
ANALYZER_CAPABILITY != BEGINNER_REQUIREMENT
```

Ésta es una protección importante para la próxima revisión pedagógica.

---

# 3. Backlog completo de implicaciones pedagógicas post-BIB065

Los puntos siguientes son **candidatos de discusión**, no instrucciones. Se reorganizan temáticamente para poder contrastarlos más adelante con el repositorio pedagógico anterior.

## A. Alcance y progresión de COR002

### A1. Mantener visible la posibilidad de que COR002 sea deliberadamente básico

No intentar que COR002 represente todo lo que Analyzer/Tutor puedan llegar a comprender. Evaluar qué complejidad discursiva es realmente útil para un principiante.

**Estado:** `STRONG_WORKING_IDEA / DISCUSS`.

### A2. Separar capacidad lingüística del dispositivo y contenido pedagógico

Una regla o fenómeno bien documentado puede ser importante para Analyzer/Tutor y no pertenecer todavía a COR002.

**Estado:** `REPOSITORY_COMPATIBLE / DISCUSS_APPLICATION`.

### A3. Revisar P1–P5, no sustituirlos automáticamente

Comprobar si la escala pragmática actual representa suficientemente operaciones como introducción, mantenimiento, cambio, reintroducción, contraste y seguimiento de múltiples referentes. La lectura no autoriza todavía otra escala.

**Estado:** `DEFERRED_COMPARISON`.

### A4. Separar dificultad gramatical de carga discursiva/referencial

Una escena con morfología sencilla puede ser difícil porque exige seguir varios referentes o un cambio de foco. Evaluar si esa carga merece una dimensión propia o sólo una propiedad auxiliar.

**Estado:** `DISCUSS`.

### A5. No medir dificultad principalmente por longitud o número de turnos

Comparar escenas cortas discursivamente densas con escenas más largas pero lineales.

**Estado:** `DISCUSS`.

### A6. No sobrecargar principiantes con toda la taxonomía lingüística

Que el proyecto distinga tópico, foco, accesibilidad, IU, etc. no implica presentar esas etiquetas al estudiante inicial.

**Estado:** `STRONG_CAUTION`.

---

## B. Unidad pedagógica y coherencia conversacional

### B1. Evitar pensar una conversación sólo como una lista de oraciones independientes

Explorar hasta qué punto una microescena básica necesita conservar continuidad mínima entre turnos: quién está activo, qué se preguntó y qué información ya se estableció.

**Cautela:** esto no convierte contexto en requisito para analizar frases aisladas.

### B2. Diseñar arcos de información además de arcos temáticos

Comparar una descripción tipo “hablan del mercado” con otra tipo:

```text
introduce X -> pregunta sobre X -> respuesta -> aparece Y -> contraste -> cierre
```

Evaluar si esto mejora naturalidad sin elevar demasiado la dificultad del principiante.

### B3. Hacer que las preguntas condicionen de verdad las respuestas

Una pregunta no sólo determina el contenido semántico de una respuesta; también establece qué se presupone y qué se solicita. Explorar esto en pares básicos antes de convertirlo en una regla generativa.

### B4. Permitir reformulación y repetición funcional

La lectura de las estructuras quiásticas muestra que repetir contenido no siempre es redundancia. No eliminar mecánicamente reformulaciones naturales sólo por “repetir información”.

**Estado:** `LATER_CONVERSATIONAL_DESIGN_CANDIDATE`.

### B5. Incorporar progresivamente habla continua

El objetivo a largo plazo no tiene por qué permanecer en `una frase = un audio`, aunque el corpus inicial pueda usar unidades pequeñas por razones pedagógicas.

**Estado:** `LONG_TERM_DISCUSSION`.

---

## C. Introducción y seguimiento de referentes

### C1. Introducir participantes de forma lingüísticamente natural

Comparar escenas donde una persona nueva simplemente aparece como pronombre con escenas que primero la establecen discursivamente.

### C2. Enseñar mantenimiento de referentes, no sólo equivalencias pronominales

Evitar reducir formas como `=be`, pronombres independientes o cero a una tabla simple “él/ella”. Considerar más adelante actividades donde el estudiante entienda a quién se refiere cada forma.

### C3. Incluir algunas escenas con más de un referente de tercera persona

No convertir esto en requisito de COR002. Evaluar cuáles son apropiadas para principiantes y en qué momento.

### C4. Explorar cambios A → B → A

Crear más adelante escenas o materiales de prueba donde cambie el referente principal y después se retome uno anterior.

### C5. Incluir reintroducción después de distancia discursiva

Comparar la expresión de un referente inmediatamente activo con uno que regresa después de varios turnos.

### C6. Explorar fronteras de episodio

Situaciones donde llega alguien, cambia la actividad o aparece un problema pueden ser útiles para estudiar reintroducción, pero no necesariamente deben entrar en el nivel más básico.

### C7. Evitar repetición automática de nombres/NP completas

Investigar si parte de la artificialidad del corpus generado viene de reidentificar referentes ya activos.

### C8. Evitar también una eliminación automática de referencias

La omisión no debe convertirse en la “solución” mecánica al problema anterior. Referentes competidores y cambios discursivos pueden requerir explicitud.

### C9. Correferencia multicláusula como contenido posterior

Las restricciones de formas explícitas/cero en reflexivas y subordinadas parecen más apropiadas para niveles posteriores salvo que emerjan naturalmente en material básico.

---

## D. Estructura informativa: foco, tópico y orden

### D1. Distinguir eventualmente foco de predicado, foco de oración y foco de argumento

No se decide que el principiante deba aprender estas etiquetas. Sí conviene conservar la posibilidad de construir materiales donde cambie la pregunta contextual y se compare cómo cambia la expresión.

### D2. Crear pares mínimos pragmáticos

Mismo evento, distinto contexto previo. Por ejemplo, conceptualmente:

- ¿qué hizo Pedro?;
- ¿quién compró pescado?;
- ¿qué compró Pedro?

El objetivo sería observar diferencias de empaquetamiento, no calcar estas preguntas al didxazá sin evidencia.

### D3. Introducir gradualmente la posición preverbal como recurso construccional

No enseñarla como “orden libre” ni como una regla general de foco.

### D4. Mantener explícito: `preverbal != foco`

Interrogación, negación, topicalización y otras construcciones pueden ocupar posición preverbal. Cualquier pedagogía futura debe evitar una regla falsa por simplificación excesiva.

### D5. Distinguir tópico y foco cuando el nivel lo justifique

“De quién estamos hablando” y “qué se está afirmando/contrastando” no son lo mismo. Decidir después cómo enseñar esa diferencia sin metalenguaje innecesario.

### D6. `nga` sólo por construcciones documentadas

No convertirlo en equivalente de “es”, “énfasis” o “foco”. Contrastes con/sin `nga` quedan como candidato posterior tras validación contemporánea.

### D7. No importar el modelo de énfasis prosódico del español

Evitar asumir que una palabra focal se obtiene simplemente pidiendo al hablante que “la acentúe más”.

---

## E. Audio, prosodia y segmentación

### E1. Preservar las unidades de entonación cuando existan

No hace falta que todo material pedagógico esté anotado en IU; la evidencia original sí puede conservar esa capa para usos posteriores.

### E2. Mantener abiertas tres escalas pedagógicas de audio

Candidato de diseño:

```text
forma aislada -> discriminación fonológica
unidad de entonación -> escucha/prosodia natural
turno o microescena -> interacción/pragmática
```

No se decide aquí que todo curso deba usar las tres.

### E3. No depender sólo de pronunciaciones aisladas o cuidadas

El habla continua puede reducir o modificar la realización superficial. Evaluar exposición gradual a ambas formas.

### E4. Contrastar una misma forma en distintas posiciones prosódicas

Posible material futuro para tono, glotalización, laringización y percepción auditiva.

### E5. No equiparar pausa con frontera gramatical

Evitar que el formato de audio enseñe accidentalmente una segmentación falsa.

### E6. Conservar audio natural además de cualquier versión pedagógica ralentizada

Si se producen versiones didácticas, no sustituir con ellas el registro natural.

---

## F. Cómo adquirir material que pueda informar la pedagogía

### F1. Usar conversación espontánea/naturalística como fuente de modelos

No sustituye el material pedagógico elaborado; sirve para observar fenómenos que una traducción desde español puede no provocar.

### F2. Complementar con elicitación no lingüística

Imágenes, videos, juegos o situaciones pueden permitir observar contrastes sin entregar primero una oración española.

### F3. Mantener traducción elicitada como categoría legítima pero etiquetada

No hay que prohibirla. Debe distinguirse de habla espontánea y no usarse por sí sola como prueba de naturalidad conversacional.

### F4. Conservar provenance del método

`SPONTANEOUS`, `NONLINGUISTIC_ELICITATION`, `TRANSLATION_ELICITATION`, `SPEAKER_JUDGMENT`, etc. pueden alimentar decisiones distintas en el futuro.

### F5. No usar frecuencia bruta como posibilidad lingüística

Una forma rara puede ser legítima; una forma frecuente en un género no necesariamente es prioritaria para principiantes.

### F6. No usar posibilidad elicitada como naturalidad conversacional

Necesitamos mantener separadas esas dimensiones al seleccionar ejemplos pedagógicos.

---

## G. Español, traducción y diseño del Generator pedagógico

### G1. Revisar si el español debe seguir siendo el punto de partida interno

Una misma traducción española puede corresponder a diferentes empaquetamientos en didxazá. Explorar una representación previa más cercana a:

```text
situación + intención + participantes + información compartida + objetivo del turno
```

sin convertir todos esos campos en requisitos obligatorios.

### G2. Mantener la traducción española como ayuda pedagógica, no necesariamente como representación central

El formato español → didxazá puede seguir siendo útil para principiantes; lo que queda abierto es si debe gobernar internamente la generación.

### G3. Revisar en el futuro el formato español → didxazá de las actividades

No se propone eliminarlo. Se propone compararlo con comprensión situacional, selección por contexto, escucha-respuesta y otras modalidades.

### G4. Contexto opcional, nunca candado

El Generator/Tutor pueden beneficiarse de contexto cuando existe, pero ninguna revisión pedagógica debe trasladar al Analyzer la obligación de recibir conversación completa.

---

## H. Actividades pedagógicas candidatas para niveles futuros

Estas son ideas de diseño, no elementos aprobados de COR002:

### H1. Elegir entre dos formas según el contexto

Escuchar o leer un contexto breve y seleccionar cuál continuación encaja mejor.

### H2. Identificar referentes

Con varios participantes: “¿a quién se refiere esta forma aquí?”.

### H3. Contrastes de foco

Mismo evento con preguntas/contextos distintos.

### H4. Seguir cambios de tópico o referente principal

Actividades de comprensión más que necesariamente de producción.

### H5. Comparar forma aislada vs. habla continua

Actividad auditiva para niveles donde resulte útil.

### H6. Explicaciones del Tutor centradas en “por qué aquí”

El Tutor podría explicar más adelante por qué una forma resulta adecuada en un contexto, sin convertir esa explicación en corrección automática.

---

# 4. Qué cambia respecto de la lista provisional de 48 puntos

La lista original post-Bueno-Holle se conserva como evidencia del proceso de reflexión, pero esta segunda pasada introduce cuatro correcciones de alcance importantes:

1. **Ya no se formula que “cada conversación necesita” obligatoriamente un estado discursivo.** Se reformula como una capacidad y una dimensión de diseño que puede mejorar determinadas conversaciones.
2. **Ya no se formula que “cada turno necesita” campos explícitos de nuevo/presupuesto/foco.** Es una representación candidata, no un schema obligatorio.
3. **Las complejidades discursivas detectadas no se asignan automáticamente a COR002.** Muchas pueden pertenecer a corpus de investigación, Tutor o niveles pedagógicos posteriores.
4. **La pedagogía previa no se convierte en baseline normativo.** Debe ser objeto de comparación junto con estas nuevas ideas.

Estas correcciones responden directamente al riesgo detectado durante la lectura: que una mayor especificidad lingüística se convierta en un nuevo conjunto de candados.

---

# 5. Preguntas concretas para la futura revisión pedagógica

Cuando se retome este frente, la discusión debería empezar por estas preguntas y no por implementar la lista anterior:

1. ¿Cuál es exactamente el objetivo de un principiante al terminar COR002?
2. ¿Qué parte de la complejidad discursiva de BIB065 es necesaria para ese objetivo y qué parte pertenece a niveles posteriores?
3. ¿Qué problemas reales observados en las muestras de COR002 intenta resolver cada cambio propuesto?
4. ¿Qué componentes actuales de P1–P5 siguen funcionando y cuáles no describen bien la dificultad observada?
5. ¿Qué situaciones actuales favorecen didxazá natural y cuáles siguen demasiado ancladas en interacciones que normalmente ocurrirían en español?
6. ¿Qué papel debe conservar el español en generación, estudio y audio para principiantes?
7. ¿Qué unidad es mejor para cada objetivo: frase, IU, turno o microescena?
8. ¿Qué fenómenos deben enseñarse explícitamente y cuáles basta con que estén presentes de forma natural en el material?
9. ¿Qué corpus oral contemporáneo necesitamos antes de tomar decisiones sobre `=be/∅`, `nga`, `la`, foco, tópico y orden?
10. ¿Cómo evitamos que una versión exitosa de COR002 se convierta después en una camisa de fuerza para COR003 u otros niveles?

---

# 6. Regla de uso de este documento

Al retomar pedagogía:

```text
READ_THIS_DOCUMENT
-> COMPARE_WITH_EXISTING_COR002_MATERIALS
-> COMPARE_WITH_P1_P5_AND_SITUATION_BANK
-> COMPARE_WITH_REAL_LEARNER_EXPERIENCE
-> COMPARE_WITH_INDEPENDENT_JUCHITAN_ORAL_CORPUS
-> DISCUSS
-> ADJUDICATE_EXPLICITLY
-> ONLY_THEN_CHANGE_PEDAGOGICAL_POLICY_OR_GENERATOR
```

No está permitido interpretar este archivo como:

```text
STYLE_GUIDE
COR002_SPECIFICATION
P1_P5_REPLACEMENT
GENERATION_LICENSE
LINGUISTIC_NORM
```

---

# 7. Relación con documentos anteriores

Para planificación pedagógica futura, este documento **sucede como punto de reanudación de la discusión** a:

- `PEDAGOGICAL_BACKLOG_BH2019_PARTIAL_v0_35.md`

pero **no lo invalida ni lo borra**. El archivo v0.35 conserva el estado parcial de la lectura y debe permanecer como provenance histórica.

La matriz:

- `BIB065_BUENO_HOLLE_INGESTION_MATRIX_v0_36_1.*`

sigue siendo el registro epistemológico de los hallazgos lingüísticos. Este documento sólo registra sus **posibles consecuencias pedagógicas** y las preguntas que deben adjudicarse después.

---

# 8. Estado final

```text
PEDAGOGICAL_DISCUSSION = FROZEN_FOR_LATER_COMPARATIVE_REVIEW
COR002 = UNCHANGED_BY_THIS_DOCUMENT
P1_P5 = UNCHANGED_BY_THIS_DOCUMENT
SITUATION_BANK = UNCHANGED_BY_THIS_DOCUMENT
GENERATOR = UNCHANGED_BY_THIS_DOCUMENT
TUTOR = UNCHANGED_BY_THIS_DOCUMENT
ANALYZER = UNCHANGED_BY_THIS_DOCUMENT
```

La conclusión principal de esta pasada no es una nueva metodología, sino una protección metodológica:

> **el proyecto puede aprender cada vez más sobre cómo funciona el didxazá sin obligar a que cada nuevo conocimiento se convierta inmediatamente en contenido para principiantes, regla de generación o estilo pedagógico permanente.**
