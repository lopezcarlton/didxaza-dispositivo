# JUCHITAN_LINGUISTIC_CORE — v0.27

## Alcance
Núcleo lingüístico compartido para didxazá de Juchitán.

Consumidores:
- ANALYZER_ENGINE
- CORRECTOR_ENGINE
- TUTOR_ENGINE
- GENERATOR_ENGINE

Fuente primaria inicial:
- Pickett, Velma B.; Black, Cheryl; Marcial Cerqueda, Vicente. *Gramática popular del zapoteco del Istmo*, 2a ed. electrónica, 2001.
- La propia obra declara que registra el habla de Juchitán.

## Reglas iniciales generales

### JLC-OVERVIEW-001 — orden básico verbal
Dominio: sintaxis
Regla:
- El orden básico descrito es Verbo – Sujeto – Complemento directo – Complemento indirecto.
Uso:
- No proyectar SVO español como patrón por defecto.

### JLC-MORPH-001 — verbo con prefijo aspectual
Dominio: morfología verbal
Regla:
- Los verbos incorporan un prefijo aspectual con la raíz.
- La persona del sujeto se analiza por separado del prefijo aspectual.

### JLC-NOUN-001 — sustantivos sin género/número flexivo español
Dominio: nominal
Regla:
- Los sustantivos no reproducen necesariamente las oposiciones de género y número del español.

### JLC-PRON-001 — clasificación pronominal por referente
Dominio: pronombres
Regla:
- La tercera persona distingue persona / animal / cosa.
- No corresponde a masculino/femenino español.

### JLC-PRON-002 — pronombres dependientes
Dominio: pronombres / morfología
Regla:
- Una misma serie dependiente puede funcionar como sujeto, objeto o poseedor según el contexto.

### JLC-PHON-001 — tres tipos de vocal
Dominio: fonología / ortografía
Regla:
- Vocal sencilla: V
- Vocal cortada: V'
- Vocal quebrada: VV
- La vocal quebrada aparece en sílaba tónica.

### JLC-TONE-001 — tono contrastivo
Dominio: fonología / morfología
Regla:
- El tono puede distinguir palabras y formas gramaticales.
- No eliminar diacríticos antes del análisis.

### JLC-STRESS-001 — acento léxico
Dominio: fonología / ortografía
Regla:
- Acento y tono son dimensiones distintas y ambas pueden ser lingüísticamente relevantes.

---

## Capítulo 4 — Sustantivos y posesión

### JLC-POS-001 — tres estrategias principales de posesión
Dominio: morfología nominal / posesión
Regla:
1. `xh-/x- + sustantivo + poseedor`.
2. `sustantivo siempre poseído + poseedor`, sin `xh-/x-`.
3. `sustantivo + xti' + poseedor`.
Fuente: Gramática Popular, §§4.2–4.2.3.
Ejemplos:
- `xhamígube` — su amigo.
- `ñeebe` — su pie.
- `tou' xtibe` — su guajolote.
Uso:
- ANALYZER: identificar primero la clase posesiva.
- CORRECTOR: no exigir un único patrón.
- TUTOR: explicar la estrategia seleccionada.
- GENERATOR: elegirla según clase nominal y contexto.

### JLC-POS-002 — sustantivos siempre poseídos
Dominio: morfología nominal
Regla:
Partes del cuerpo, miembros de la familia y otros sustantivos pertenecen a una clase que no acepta `xh-/x-`; aparece el sustantivo con el poseedor.
Ejemplos:
- `ñeebe` — su pie.
- `bixhozebe` — su padre.
- `lidxi Juana` — la casa de Juana.
Fuente: Gramática Popular, §4.2.2.
Uso:
- No buscar un posesivo independiente inexistente.
- Permitir que la persona dependiente forme parte de la superficie nominal.
- COR001 FB-019 `jñaa`: compatible con esta clase.

### JLC-POS-003 — prefijo posesivo `xh-/x-`
Dominio: morfofonología
Regla:
Una clase de sustantivos forma posesión con `xh-` ante vocal y `x-` ante consonante; puede haber cambios en el sonido inicial.
Fuente: Gramática Popular, §4.2.1.

### JLC-POS-004 — fortalecimiento tras `x-`
Dominio: morfofonología
Regla:
- `b → p`: `bere` → `xpérebe`.
- `d → t`: `doo` → `xtoobe`.
- `g → c/qu`: `gueta` → `xquétabe`.
Fuente: Gramática Popular, Cuadro 7.
Uso:
- Reconstrucción morfológica de base y forma poseída.
- No tratar las formas fortalecidas como errores.

### JLC-POS-005 — otros cambios ante `x-`
Dominio: morfofonología
Regla:
- `x + ch → xh`: `chin` → `xhinbe`.
- `x + dx → xh`: `dxiiña'` → `xhiiñabe`.
- `x + z → s`: `zidi` → `sídibe`.
- `x + s → s`: `saa` → `saabe`.
- `x + r → xt`: `rii` → `xtiibe`.
Fuente: Gramática Popular, Cuadro 8.
Uso:
- Transformaciones condicionadas; nunca sustituciones globales.

### JLC-POS-006 — pérdida de `bi-` en ciertas prendas poseídas
Dominio: morfofonología / léxico
Regla:
- `bidaani'` → `xtaanibe`.
- `bizuudi'` → `suudibe`.
Fuente: Gramática Popular, Cuadro 9.
Uso:
- Requiere clase léxica explícita; no generalizar.

### JLC-POS-007 — posesión con `xti'`
Dominio: sintaxis nominal
Regla:
La mayoría de los sustantivos pueden aparecer con `xti'` + pronombre dependiente o frase nominal.
Ejemplos:
- `tou' xtibe` — su guajolote.
- `tou' xti' Ana` — el guajolote de Ana.
- `bi'cu' xti' bixhoze'` — el perro de mi papá.
- `bere xti' jñaa Ana` — la gallina de la mamá de Ana.
Fuente: Gramática Popular, §4.2.3.
Uso:
- Permitir cadenas posesivas anidadas.

### JLC-DERIV-001 — formación de abstractos con `guenda/enda`
Dominio: derivación / composición
Regla:
Sustantivos abstractos pueden formarse con `guenda` (opcionalmente `enda`) antepuesto a un verbo con prefijo habitual.
Ejemplos:
- `ro` → `guendaró` — comida.
- `re'` → `guendaré'` — desayuno / el tomar.
- `roxhi` → `guendaroxhi` — cena.
- `ribana'` → `guendaribana'` — nostalgia.
- `rati` → `guendarati` — el morir.
Fuente: Gramática Popular, §4.3.
Uso:
- ANALYZER: segmentar morfología interna sin exigir espacios.
- CORRECTOR: no separar automáticamente `guenda` de la base.
- TUTOR: explicar el significado composicional.
- GENERATOR: reconocer el patrón; generar sólo con base documentada.

## Estado
EXPERIMENTAL_CORE
No activa autocorrección automática.


---

## Capítulo 5 — Pronombres y persona dependiente

### JLC-PRON-003 — inventario de pronombres dependientes
Dominio: persona / morfología
Regla:
- 1SG: `a'`, con realizaciones/fusiones `-a'` y `-ya'`.
- 2SG: `lu'`, con alternancia `-u'`.
- 3SG persona: `be`.
- 3SG animal: `me`.
- 3SG cosa: `ni`.
- 1PL exclusivo: `du`.
- 1PL inclusivo: `nu`.
- 2PL: `tu`.
- 3PL personas: `cabe`.
- 3PL animales: `came`.
- 3PL cosas: `cani`.
Fuente: Gramática Popular, §5.1.2, Cuadros 13–18.
Uso:
- ANALYZER: identificar persona y clase semántica sin exigir pronombre independiente.
- CORRECTOR: no marcar automáticamente una forma ligada como desconocida.
- TUTOR: explicar qué información de persona está incorporada.
- GENERATOR: seleccionar persona dependiente acorde con referente y contexto.

### JLC-PRON-004 — alojamiento de pronombres dependientes
Dominio: morfosintaxis
Regla:
Los pronombres dependientes pueden alojarse en:
- verbo;
- sustantivo;
- modificador;
- base `laa`;
- plural `ca`;
- `xti'`.
Ejemplos documentados: `Cayuundabe`, `xpí'cube`, `laabe`, `Rócabe`, `xtibe`.
Fuente: Gramática Popular, §5.1.2.
Uso:
- No imponer espacios entre el anfitrión y la persona dependiente.
- El motor debe distinguir palabra ortográfica de estructura morfológica interna.

### JLC-PRON-005 — tercera persona cero
Dominio: morfosintaxis / discurso
Regla:
`be`, `me` o `ni` pueden omitirse cuando el referente de tercera persona se recupera por contexto.
Ejemplos: `íquebe ~ ique`; `Biábabe rarí' ~ Biaba rarí'`.
Fuente: Gramática Popular.
Uso:
- ANALYZER: permitir análisis 3SG sin morfema superficial.
- GENERATOR: no insertar pronombre obligatoriamente si el contexto permite cero.
- TUTOR: explicar que ausencia de marca no equivale a ausencia de sujeto.

### JLC-PRON-006 — tercera persona clasifica referente
Dominio: semántica / pronombres
Regla:
- `be` = tercera persona humana/persona.
- `me` = animal.
- `ni` = cosa/no-persona según la clasificación documentada.
La distinción no corresponde a masculino/femenino.
Uso:
- GENERATOR: resolver clase semántica antes de escoger 3SG.
- CORRECTOR: no sustituir `be/me/ni` por analogía española.

### JLC-PRON-007 — inclusivo vs exclusivo
Dominio: persona / pragmática
Regla:
- `nu` = 1PL inclusivo: hablante + interlocutor(es).
- `du` = 1PL exclusivo: hablante + otros, excluyendo al interlocutor.
Fuente: Gramática Popular, inventario de pronombres dependientes.
Uso:
- TUTOR: enseñar explícitamente la diferencia que el español `nosotros` no codifica.
- GENERATOR: preguntar/inferir si el interlocutor está incluido antes de producir 1PL.

### JLC-PERS-001 — 2SG `-lu' ~ -u'`
Dominio: persona / morfofonología
Regla:
La segunda persona singular tiene dos realizaciones documentadas: `-lu'` y `-u'`. La forma `-u'` puede modificar la raíz.
Ejemplos:
- `ene` → `rie'nu'` / `riénelu'` — entiendes.
- `ique` → `i'cu'` / `iquelu'` — tu cabeza.
- `apa` → `napu'` / `nápalu'` — tienes.
Fuente: Gramática Popular, Cuadro 15.
Uso:
- No reconstruir una raíz por terminación `u'` sin lema/paradigma compatible.
- GENERATOR: elegir forma sólo con clase/paradigma documentado.

### JLC-PERS-002 — 1SG `-a' ~ -ya'` y fusiones
Dominio: persona / morfofonología
Regla:
La primera persona singular se realiza mediante `-a'` o `-ya'` con fusiones vocálicas condicionadas por la raíz y la prosodia.
Ejemplos:
- `ree` → `riree'` — salgo.
- `ro` → `raua'` — como.
- `apa` → `napa'` — tengo.
- `ene` → `riene'` — entiendo.
- `bihui` → `xpihue'` — mi puerco.
Fuente: Gramática Popular, Cuadros 16–17.
Uso:
- ANALYZER: buscar superficie flexionada antes de `NO_ENCONTRADO`.
- CORRECTOR: no añadir saltillo/acento de forma ciega.
- TUTOR: enseñar la fusión como morfología, no irregularidad arbitraria.
- GENERATOR: generar sólo con lema y patrón confirmados.

### JLC-PERS-003 — persona no equivale a una cadena fija
Dominio: arquitectura
Regla:
Una misma función de persona puede realizarse como sufijo, fusión vocálica, cambio prosódico o cero según la construcción.
Uso:
- Prohibir reglas ingenuas del tipo `1SG => añadir '`.
- Consultar negación, aspecto, clase verbal, posesión y contexto antes de resolver superficie.

### JLC-PERS-004 — COR001 `riené`
Dominio: benchmark / tono-persona
Regla experimental:
COR001 y su audio documentan `qui riené` para “No entiendo”; la prominencia final debe conservarse como rasgo relevante de primera persona en este caso.
Estado:
- SPEAKER_PRODUCED + OWNER_CONFIRMED + AUDIO_SUPPORTED.
- Requiere alineación formal con la notación de GP antes de generalizar.
Uso:
- Caso de prueba obligatorio para no eliminar marcas prosódico-ortográficas antes del análisis.


---

## Capítulo 6 — Adjetivos y estados

### JLC-ADJ-001 — adjetivo atributivo y predicativo
Dominio: sintaxis / adjetivos
Regla:
- Una propiedad puede aparecer modificando a un sustantivo o funcionando como predicado.
- El motor no debe asumir que toda traducción española con “ser/estar + adjetivo” requiere una cópula independiente en didxazá.
Fuente: Gramática Popular, capítulo de adjetivos.
Uso:
- ANALYZER: distinguir modificación nominal de predicación.
- CORRECTOR: no insertar automáticamente `nga` por analogía con “es”.
- TUTOR: explicar cuándo una cualidad se predica directamente.
- GENERATOR: seleccionar construcción adjetival documentada, no calcar `ser/estar`.

### JLC-ADJ-002 — posición del adjetivo
Dominio: sintaxis nominal
Regla:
- La posición del adjetivo respecto del sustantivo sigue patrones propios del didxazá y no debe inferirse desde el español.
Uso:
- ANALYZER/GENERATOR: consultar construcción documentada antes de ordenar N/ADJ.

### JLC-STATE-001 — estado vs acción
Dominio: aspecto / semántica
Regla:
- El sistema distingue predicados que describen una acción/proceso de aquellos que describen un estado.
- Una forma estativa presenta una condición como vigente, no como evento en desarrollo.
Uso:
- TUTOR: contrastar “abrirse” vs “estar abierto”.
- GENERATOR: no usar progresivo cuando la intención es estado.
- ANALYZER: separar ESTADO de PROCESO aun cuando el español use `estar` en ambos.

### JLC-STATE-002 — estativo no equivale mecánicamente a `estar`
Dominio: semántica / traducción
Regla:
- El valor estativo puede traducirse al español con `ser`, `estar`, `tener`, o una construcción adjetival según el predicado.
Uso:
- Prohibir regla `ESTATIVO => estar + adjetivo`.
- Priorizar equivalencia semántica y ejemplos paralelos.

### JLC-ADJ-003 — intensidad y modificación
Dominio: semántica / adverbial
Regla:
- Grado e intensidad de propiedades pueden expresarse mediante partículas o construcciones propias.
Uso:
- TUTOR/GENERATOR: no trasladar automáticamente `muy`, `más`, `tan` como si fueran operadores universales.

### JLC-ADJ-004 — propiedades lexicalizadas
Dominio: léxico / semántica
Regla:
- Algunas nociones que el español expresa mediante adjetivos pueden corresponder en didxazá a verbos, formas estativas o lexemas de otra clase.
Uso:
- ANALYZER: clasificar por función en contexto, no por etiqueta de traducción española.
- GENERATOR: partir de construcción didxazá documentada.

### JLC-STATE-003 — relevancia para COR001
Dominio: benchmark
Regla:
- Frases españolas con `ser/estar + cualidad` deben revisarse para determinar si el didxazá usa `nga`, predicación directa, forma estativa u otra construcción.
Casos de interés:
- FB-050 “La casa es grande.”
- FB-057 “Las flores son hermosas.”
Uso:
- No cerrar ortografía/sintaxis únicamente por correspondencia palabra a palabra.


---

## Capítulo 7 — Verbos: arquitectura general y aspectos

### JLC-VERB-001 — estructura verbal general
Dominio: morfología verbal
Regla:
Antes de clasificar una forma verbal como no encontrada, el analizador debe intentar reconocer:

ASPECTO + (CAUSATIVO) + RAÍZ + (OTROS ELEMENTOS) + PERSONA

La superficie depende de juego verbal, aspecto, forma fonológica de la raíz, causatividad, persona, auxiliares de movimiento y alternancias léxicas.
Fuente: Gramática Popular, cap. 7; MORF-VERB GP v0.1.

### JLC-VERB-002 — inventario funcional de aspectos
- Habitual: acción repetida/acostumbrada.
- Completivo: acción terminada.
- Progresivo: acción en curso.
- Perfecto: valor aspectual propio, no simple pasado.
- Potencial: acción no realizada seleccionada por múltiples construcciones.
- Irrealizado: acción contraria a los hechos/no realizada en contextos específicos.
- Estativo: estado.
- Futuro: contexto futuro.

La inicial gráfica sola no identifica de manera única el aspecto.

### JLC-VERB-003 — juegos de prefijos aspectuales

Juego 1A:
H ri- | C bi- | PR ca-/cay- | P gui- | I ni-/ñ- | PF hua-/huay- | F za-/zi-

Juego 1B:
H ri-/r- | C gu-/gü- | PR ca-/cay- | P gui-/gu- | I ni-/ñ- | PF hua-/huay- | F za-/z-

Juego 1C:
H ri- | C gu- | PR ca- | P Ø | I ni- | PF hua- | F za-

Juego 2:
H ru- | C bi- | PR cu- | P gu- | I nu- | PF hua- | F zu-

Regla de arquitectura:
- GENERATOR: no generar aspecto sin clase verbal.
- ANALYZER: potencial de Juego 1C puede no tener prefijo visible.
- CORRECTOR: una inicial r-/b-/g-/c-/z- no basta para diagnosticar aspecto.

### JLC-VERB-004 — habitual no equivale a presente
El habitual expresa acción repetida/acostumbrada y puede interpretarse en presente o pasado según contexto; la Gramática indica que no se usa en contexto futuro.

### JLC-VERB-005 — completivo no equivale a pasado
El completivo presenta una acción como terminada. Aunque suele traducirse con pasado español, es una categoría aspectual.

### JLC-VERB-006 — progresivo y tiempo contextual
El progresivo presenta una acción en curso; el contexto puede situarla en presente, pasado o futuro.

### JLC-VERB-007 — potencial seleccionado por construcción
El potencial aparece, entre otros contextos:
- después de auxiliares de movimiento;
- después de zanda “poder”;
- después de verbos de querer/gustar;
- en propósito;
- después de ca'ru' “todavía no”;
- después de zándaca “tal vez”;
- en ciertos imperativos.

### JLC-VERB-008 — irrealizado
El irrealizado aparece, entre otros contextos, con negación de acciones pasadas que no sucedieron.

### JLC-VERB-009 — estativo no determina tiempo
El estativo na- puede aparecer en contextos presentes, pasados o futuros.

### JLC-VERB-010 — paradigmas documentados
Juego 1A: riree / biree / caree / guiree / niree / huaree / zaree.
Juego 1B: richesa / guchesa / cachesa / guichesa / nichesa / huachesa / zachesa.
Juego 2: rucaa / bicaa / cucaa / gucaa / nucaa / huacaa / zucaa.

No generalizar a verbos cuya clase no esté documentada.

### JLC-VERB-011 — orden de análisis verbal
1. negación/construcción;
2. auxiliar de movimiento;
3. juego + aspecto;
4. causatividad/alternancia de raíz;
5. raíz/compuesto;
6. partículas dependientes;
7. persona;
8. contraste con lema/paradigma.

Prohibido usar como estrategia principal “quitar un prefijo y buscar lo que sobra”.

---

## Capítulo 7 — Causatividad y cambio de valencia

### JLC-CAUS-001
Una causativa añade un causante al evento y cambia la valencia del verbo.
Uso: analizar causante y participante causado; no calcar automáticamente “hacer + verbo”.

### JLC-CAUS-002
GP documenta una estrategia causativa frecuente con `si-` después del prefijo aspectual; muchas formas siguen Juego 2.
Restricción: sólo con lema/paradigma documentado.

### JLC-CAUS-003
GP documenta además causativos con `g-`, `z-`, `s-`, `ch-` y alternancias iniciales frecuentes:
`z→s`, `g→c/qu`, `dx→ch`, `d→t`, `x→xh`.
No usar como sustituciones globales.

### JLC-CAUS-004
Algunos causativos cambian también de juego aspectual. Deben compararse paradigmas completos.

### JLC-CAUS-005
Hay dobles causativos y grados causativos. Mantener como inventario cerrado.

### JLC-CAUS-006
Hay causativos sin prefijo visible, expresados por cambio de clase/juego en verbos específicos.

### JLC-CAUS-007
Pérez Báez 2015 refina la arquitectura:
`(NEG) + TAM + (AUX) + (DERIVACIÓN) + RAÍZ + SUJETO + OBJETO`
El `u` causativo pertenece a derivación, no a TAM.
Relaciones: mediopasivo, causativo, más/menos activo, equipolente, cadenas `u-`, `u-g-`, `u-si-/u-zi-`.

### JLC-CAUS-008
Algunas estrategias causativas varían entre hablantes o están en retroceso.
`RECHAZADO_POR_UN_HABLANTE != INCORRECTO`.
Generación y corrección requieren evidencia léxica o de hablante de Juchitán.

---

## Capítulo 7 — Imperativos y mandatos

### JLC-IMP-001 — imperativo como construcción, no como tiempo
Dominio: modo / sintaxis / aspecto
Regla:
El imperativo expresa orden, petición, exhortación o instrucción. No debe analizarse como “presente” ni como simple futuro.
Uso:
- TUTOR: separar modo imperativo de tiempo/aspecto.
- GENERATOR: seleccionar construcción imperativa por fuerza pragmática.

### JLC-IMP-002 — relación con potencial
Dominio: modo / aspecto
Regla:
La Gramática Popular documenta usos del potencial en ciertos imperativos, especialmente imperativos suaves/negativos y construcciones dependientes.
Uso:
- ANALYZER: un potencial puede tener función imperativa según el contexto.
- GENERATOR: no mapear “orden” a una única forma verbal.

### JLC-IMP-003 — imperativo negativo
Dominio: negación / modo
Regla:
Los mandatos negativos pueden seleccionar construcciones distintas de los afirmativos y deben analizarse conjuntamente con negación y potencial.
Uso:
- CORRECTOR: no sustituir forma afirmativa por negativa mecánicamente.
- GENERATOR: resolver NEG + construcción imperativa + persona.

### JLC-IMP-004 — fuerza pragmática
Dominio: pragmática
Regla:
Una misma intención española (“haz X”) puede corresponder a:
- orden directa;
- petición;
- exhortación;
- permiso/invitación;
- prohibición.
Uso:
- GENERATOR: seleccionar forma según relación social y contexto.
- TUTOR: explicar diferencia entre traducción literal y función comunicativa.

### JLC-IMP-005 — persona destinataria
Dominio: persona / modo
Regla:
El imperativo se organiza alrededor del destinatario, típicamente 2SG/2PL, pero algunas exhortaciones incluyen primera persona plural.
Uso:
- GENERATOR: distinguir “haz”, “hagan”, “hagamos”.
- ANALYZER: integrar persona dependiente con la construcción imperativa.

### JLC-IMP-006 — no extrapolar desde español
Dominio: seguridad de generación
Regla:
No asumir equivalencias universales:
- “por favor” no necesariamente cambia sólo una partícula;
- imperativo español no implica forma imperativa única;
- “vamos a…” puede ser exhortativo, futuro o movimiento.
Uso:
- Priorizar ejemplos documentados y corpus paralelo de Juchitán.

---

## Capítulo 7 — Verbos de movimiento y auxiliares

### JLC-MOVE-001 — `ir` y `venir` tienen comportamiento especial
Dominio: morfología verbal / movimiento
Regla:
Los verbos `ir` y `venir` presentan conjugaciones progresivas especiales y no deben analizarse como verbos regulares.
Fuente: Gramática Popular §7.6.
Uso:
- ANALYZER: consultar paradigma especial antes de segmentar.
- CORRECTOR: no corregir sus formas por analogía con otros verbos.
- GENERATOR: usar paradigmas documentados.

### JLC-MOVE-002 — progresivo singular especial
Dominio: aspecto / movimiento
Regla:
Para `ir` y `venir`, el prefijo progresivo `ca-` se usa solamente para plural; el singular usa formas especiales con `z-`.
Fuente: Gramática Popular §7.6.
Uso:
- No generar `cayeedabe`/formas análogas para singular por regla general.

### JLC-MOVE-003 — `ir` progresivo vs completivo
Dominio: aspecto / semántica
Regla:
En `ir`, la forma progresiva con `z-` puede expresar que la persona se fue y todavía no regresa; la completiva puede expresar que fue y ya regresó.
Ejemplos GP:
- `Ma' zebe` — “Ya se fue” (todavía no regresa).
- `Ma' guyebe` — “Ya fue” (y regresó).
Uso:
- TUTOR: explicar diferencia de resultado/discurso, no sólo tiempo.
- GENERATOR: seleccionar según si el retorno está completado/relevante.

### JLC-MOVE-004 — `venir`: tono distingue progresivo y futuro
Dominio: tono / aspecto / movimiento
Regla:
La forma superficial `zeedabe` puede corresponder a progresivo “ya viene” o futuro “vendrá”, distinguidos por tono.
Fuente: Gramática Popular §7.6.
Uso:
- CORRECTOR: no normalizar tono antes de análisis.
- ANALYZER: mantener múltiples hipótesis si la información tonal no está disponible.
- TUTOR: explicar que misma secuencia segmental puede tener funciones diferentes por tono.

### JLC-MOVE-005 — auxiliares de movimiento + potencial
Dominio: sintaxis verbal
Regla:
`ir` y `venir` tienen formas auxiliares que acompañan a un verbo principal en potencial para expresar movimiento con intención.
Ejemplo semántico:
- ir + POT(ver) = ir para verlo / ir a verlo.
Fuente: Gramática Popular, Cuadros 35–36.
Uso:
- ANALYZER: reconocer AUX_MOV + VERBO_POTENCIAL como construcción.
- GENERATOR: no traducir `ir a + infinitivo` español de manera literal; usar construcción documentada cuando corresponda.

### JLC-MOVE-006 — paradigma auxiliar de `ir`
Dominio: auxiliares / aspecto
Formas documentadas:
- habitual: `ri-...`
- completivo: `ye-...`
- progresivo: `ze-...`
- potencial: `chi-...`
- irrealizado: `ni-...`
- futuro: `zi-...`
Ejemplos GP con `ver`:
`Riguuyabe ni`, `Yeguuyabe ni`, `Zeguuyabe ni`, `Chiguuyabe ni`, `Niguuyabe ni`, `Ziguuyabe ni`.
Uso:
- Inventario cerrado/documentado; no reconstruir mecánicamente verbos nuevos.

### JLC-MOVE-007 — paradigma auxiliar de `venir`
Dominio: auxiliares / aspecto
Formas documentadas:
`Redaguuyabe ni`, `Bedaguuyabe ni`, `Zedaguuyabe ni`, `Ñedaguuyabe ni`, etc.
La forma auxiliar de `venir` usa vocal sencilla donde el verbo pleno presenta vocal quebrada.
Fuente: Gramática Popular, Cuadro 36.
Uso:
- ANALYZER: distinguir forma plena y auxiliar.
- TUTOR: mostrar que auxiliar puede tener forma reducida/alterada.

### JLC-MOVE-008 — movimiento con intención vs movimiento simultáneo
Dominio: semántica / sintaxis
Regla:
Con un verbo principal en potencial, los auxiliares expresan movimiento con intención (“ir/venir para hacer X”).
Con una lista restringida de verbos de raíz inicial y, pueden expresar movimiento durante la acción:
- `Ziyuunabe` — “Va llorando”.
- `Zedayuunabe` — “Viene llorando”.
Fuente: Gramática Popular §7.6.
Uso:
- GENERATOR: distinguir propósito de acción simultánea.
- No extender el segundo patrón a cualquier verbo.

### JLC-MOVE-009 — relevancia COR001
Dominio: benchmark
Casos:
- FB-062 requiere revisar si la traducción española y la forma de movimiento están alineadas.
- COR001 “¿A dónde vas?” tiene forma documentada compatible con paradigma especial.
- COR001 “¿De dónde vienes?” requiere paradigma especial de `venir`.
- FB-076 `zanda + verbo` muestra selección de potencial, aunque `zanda` no sea auxiliar de movimiento.
Uso:
- Pruebas del ANALYZER y GENERATOR deben cubrir verbos de movimiento antes de generación libre.


---

## Capítulo 7 — Verbos compuestos

### JLC-COMP-001 — verbo compuesto como unidad semántica compleja
Dominio: morfología / léxico / semántica
Regla:
Un verbo compuesto puede contener más de una pieza léxica o morfológica y funcionar como una sola unidad verbal.
Uso:
- ANALYZER: no asumir que una palabra ortográfica corresponde a una sola raíz simple.
- TUTOR: mostrar componentes cuando su análisis esté documentado.
- GENERATOR: reutilizar patrones sólo cuando la combinación esté atestiguada o sea productiva de forma demostrable.

### JLC-COMP-002 — composición no equivale a traducción literal
Dominio: semántica
Regla:
El significado de un compuesto puede ser parcialmente composicional o lexicalizado.
Uso:
- Mantener dos capas:
  1. análisis morfológico/literal;
  2. significado natural de la unidad.
- No generar una traducción natural sumando glosas morfema por morfema.

### JLC-COMP-003 — palabra ortográfica vs estructura morfológica
Dominio: tokenización / morfología
Regla:
Una sola palabra ortográfica puede contener varias unidades morfológicas.
Ejemplos ya confirmados en el proyecto:
- `guendaró`
- `guendanabani`
Uso:
- TOKENIZER: conservar la palabra ortográfica.
- MORPH_ANALYZER: permitir segmentación interna.
- CORRECTOR: no insertar espacios sólo porque se reconozcan dos componentes.

### JLC-COMP-004 — variantes de unión y cambios fonológicos
Dominio: morfofonología
Regla:
Al combinarse los componentes de un verbo o palabra compleja pueden producirse fusiones, pérdidas o cambios fonológicos.
Uso:
- No esperar concatenación transparente.
- Requiere paradigma, fuente o evidencia de hablante.

### JLC-COMP-005 — compuestos lexicalizados
Dominio: léxico
Regla:
Cuando una combinación adquiere un significado convencional no predecible por simple suma de partes, debe almacenarse como unidad lexicalizada además de conservar su análisis interno.
Campos:
- surface
- components
- literal_analysis
- conventional_meaning
- provenance
- dialect/community
Uso:
- TUTOR: explicar literal vs natural.
- GENERATOR: preferir unidad lexicalizada para naturalidad.

### JLC-COMP-006 — composición productiva vs lista cerrada
Dominio: arquitectura
Regla:
Distinguir:
- patrón productivo documentado;
- compuesto lexicalizado individual;
- hipótesis de segmentación.
No tratar un ejemplo aislado como permiso para fabricar compuestos nuevos.

### JLC-COMP-007 — relevancia para `zeenda`
Dominio: benchmark
Regla:
FB-062 `zeenda` debe permanecer como hipótesis de análisis interno `zee + nda'` hasta confirmación lingüística.
La ausencia de espacio no es evidencia contra la segmentación morfológica.
No convertir la hipótesis en etimología ni significado composicional confirmado.


---

## Capítulo 7 — Frases verbales y construcciones complejas

### JLC-VP-001 — frase verbal como construcción
Dominio: sintaxis verbal
Regla:
Varias palabras ortográficamente separadas pueden funcionar juntas como una sola construcción verbal.
Uso:
- ANALYZER: analizar dependencias entre verbos y partículas, no sólo tokens aislados.
- TUTOR: explicar la construcción completa antes de glosar palabra por palabra.
- GENERATOR: seleccionar patrones documentados de combinación verbal.

### JLC-VP-002 — verbo rector y verbo dependiente
Dominio: sintaxis / aspecto
Regla:
Un verbo o partícula puede determinar el aspecto o forma del verbo dependiente.
Casos ya documentados:
- `zanda` + potencial.
- auxiliares de movimiento + verbo principal en potencial.
Uso:
- No traducir los verbos de una frase de manera independiente.

### JLC-VP-003 — serialización y secuencias verbales
Dominio: sintaxis verbal
Regla:
Algunas secuencias de verbos expresan un solo evento complejo, como movimiento + propósito, capacidad + acción o comienzo/continuidad de acción.
Uso:
- Mantener análisis de roles semánticos y dependencia entre predicados.
- No asumir coordinación simple (“X y Y”) cuando hay subordinación o serialización.

### JLC-VP-004 — propósito
Dominio: semántica / sintaxis
Regla:
Construcciones de movimiento u otros verbos pueden introducir una acción de propósito.
Interpretación:
“ir para hacer X” ≠ “ir haciendo X”.
Uso:
- GENERATOR: distinguir INTENCIÓN/PROPÓSITO de SIMULTANEIDAD.

### JLC-VP-005 — capacidad
Dominio: modalidad / sintaxis
Regla:
`zanda` “poder” selecciona potencial en el verbo dependiente.
Uso:
- TUTOR: explicar que la forma del segundo verbo está gobernada por la construcción.
- GENERATOR: `PODER + ACCIÓN` debe resolverse como construcción, no como dos traducciones aisladas.

### JLC-VP-006 — negación y frase verbal
Dominio: negación / sintaxis
Regla:
La negación puede afectar la selección aspectual del verbo y debe analizarse antes de segmentar la forma verbal.
Uso:
- CORRECTOR: no evaluar una forma negada con el paradigma afirmativo aislado.
- ANALYZER: contexto de negación precede al análisis aspectual.

### JLC-VP-007 — composicionalidad parcial
Dominio: semántica
Regla:
Una frase verbal puede tener significado convencional o pragmático no predecible por suma literal.
Campos:
- literal_structure
- conventional_meaning
- pragmatic_function
- source_examples
Uso:
- TUTOR: distinguir literal, natural y función comunicativa.
- GENERATOR: preferir construcción documentada cuando la intención coincida.

### JLC-VP-008 — prioridad de corpus paralelo
Dominio: arquitectura / evidencia
Regla:
Las frases verbales deben aprenderse prioritariamente de:
1. Gramática Popular;
2. literatura/texto paralelo de Juchitán;
3. Dictionaria/examples;
4. hablantes contemporáneos.
Uso:
- Corpus paralelo es evidencia clave para naturalidad y equivalencia no literal.


---

## Negación — arquitectura compartida

### JLC-NEG-001 — negación como construcción
Dominio: sintaxis / aspecto / modo
Regla:
La negación debe analizarse como parte de una construcción completa y no como una palabra independiente que se añade sin efectos sobre el verbo.
Uso:
- ANALYZER: detectar negación antes de identificar aspecto/persona.
- CORRECTOR: no comparar una forma negativa únicamente con un paradigma afirmativo aislado.
- GENERATOR: seleccionar la forma negativa documentada de la construcción.

### JLC-NEG-002 — interacción con aspecto
Dominio: aspecto
Regla:
La negación puede condicionar la selección de aspecto. En contextos documentados, una acción pasada que no ocurrió puede aparecer en irrealizado.
Uso:
- No mapear `no + pasado español` automáticamente a completivo.
- Distinguir “no ocurrió” de “ocurrió y fue negativo” según la construcción.

### JLC-NEG-003 — negación y potencial
Dominio: modo / aspecto
Regla:
Ciertas prohibiciones, mandatos negativos y expresiones de “todavía no” seleccionan potencial u otras formas no idénticas al afirmativo.
Uso:
- GENERATOR: no producir prohibición insertando sólo una partícula negativa ante un imperativo afirmativo.
- TUTOR: explicar la selección de forma dependiente.

### JLC-NEG-004 — alcance de la negación
Dominio: semántica
Regla:
El motor debe determinar qué parte de la proposición está negada:
- evento;
- participante;
- propiedad;
- existencia;
- posibilidad/capacidad;
- tiempo/aspecto.
Uso:
- Evitar traducciones erróneas por tratar toda negación como “no + verbo”.

### JLC-NEG-005 — negación y persona
Dominio: morfología / benchmark
Regla:
Las marcas de persona siguen siendo relevantes dentro de construcciones negativas.
Caso:
- COR001 FB-099 `qui riené` — “No entiendo”.
La negación `qui` no elimina la necesidad de analizar la forma verbal y su persona.
Uso:
- Preservar tono/diacríticos antes del análisis.

### JLC-NEG-006 — negación lexicalizada / expresiones convencionales
Dominio: semántica / pragmática
Regla:
Algunas expresiones negativas pueden tener significado convencional no reducible a traducción literal.
Uso:
- Mantener:
  - estructura literal;
  - significado natural;
  - función pragmática;
  - provenance.
- Priorizar corpus paralelo de Juchitán para naturalidad.

### JLC-NEG-007 — orden de análisis negativo
Dominio: arquitectura
Orden:
1. identificar marcador/construcción negativa;
2. determinar alcance;
3. identificar construcción rectora;
4. resolver aspecto;
5. resolver raíz;
6. resolver persona;
7. producir traducción literal;
8. producir interpretación natural.



---

## Interrogación — preguntas y función pragmática

### JLC-INT-001 — pregunta sí/no vs pregunta de contenido
Dominio: sintaxis / pragmática
Regla:
Distinguir:
- interrogativa polar: respuesta esperada sí/no;
- interrogativa de contenido: pregunta por persona, lugar, cantidad, manera, causa, etc.
Uso:
- ANALYZER: clasificar tipo de interrogativa antes de interpretar partículas/palabras.
- GENERATOR: seleccionar construcción según el tipo de información buscada.

### JLC-INT-002 — interrogación no equivale sólo a entonación
Dominio: fonología / sintaxis
Regla:
La función interrogativa puede involucrar:
- palabras interrogativas;
- partículas;
- orden;
- tono/entonación;
- combinación de estas.
Uso:
- CORRECTOR: no inferir interrogación sólo por signo gráfico.
- TUTOR: distinguir tono léxico de entonación interrogativa.

### JLC-INT-003 — preguntas pragmáticamente no interrogativas
Dominio: pragmática
Regla:
Una estructura interrogativa puede realizar funciones como:
- petición;
- oferta;
- sugerencia;
- confirmación.
Ejemplo conceptual:
“¿Puedes repetirlo?” = forma interrogativa, función de petición.
Uso:
- TUTOR: explicar forma gramatical y función comunicativa por separado.
- GENERATOR: partir de intención pragmática y luego elegir una interrogativa si es natural.

### JLC-INT-004 — palabras interrogativas como construcciones
Dominio: léxico / sintaxis
Regla:
Formas equivalentes a “qué”, “quién”, “dónde”, “cuánto”, “cómo” deben almacenarse con:
- distribución;
- construcción típica;
- restricciones;
- ejemplos paralelos.
Uso:
- No traducir palabra interrogativa aislada sin su patrón sintáctico.

### JLC-INT-005 — cantidad/precio
Dominio: benchmark / semántica
Regla:
FB-079 `pagala sacani` es caso de referencia para interrogación de precio.
Uso:
- conservar análisis literal y significado natural;
- mantener evidencia acústica de `s` y continuidad de `sacani`;
- preguntar/confirmar función tonal final con hablante.

### JLC-INT-006 — interrogación y tono
Dominio: fonología / pragmática
Regla:
La subida final de F0 puede ser entonación interrogativa, tono léxico o interacción de ambas.
Uso:
- ANALYZER: no reasignar marcas tonales por “sonar a pregunta”.
- AUDIO: mantener capa tonal separada de función interrogativa.

### JLC-INT-007 — orden de análisis interrogativo
Dominio: arquitectura
Orden:
1. detectar interrogación por contexto/estructura;
2. clasificar polar vs contenido;
3. identificar palabra/partícula interrogativa;
4. analizar verbo y aspecto;
5. resolver tono léxico por separado;
6. inferir función pragmática;
7. producir traducción literal;
8. producir interpretación natural.


---

## Adverbios, preposiciones y partículas

### JLC-ADV-001 — adverbio como modificador
Dominio: sintaxis / semántica
Regla:
Los adverbios pueden modificar verbo, adjetivo, otro adverbio o la oración completa, aportando información de tiempo, lugar, manera, intensidad, frecuencia o actitud.
Uso:
- ANALYZER: identificar qué elemento modifica el adverbio.
- TUTOR: explicar función, no sólo traducción.
- GENERATOR: ubicarlo según patrón documentado, no por calco del español.

### JLC-ADV-002 — tiempo y aspecto son capas distintas
Dominio: semántica temporal
Regla:
Palabras como “ayer”, “mañana”, “siempre”, “todavía” aportan localización o frecuencia temporal, pero no sustituyen el análisis aspectual del verbo.
Uso:
- No inferir aspecto únicamente desde el adverbio.
- No inferir tiempo únicamente desde el prefijo aspectual.

### JLC-ADV-003 — frecuencia
Dominio: aspecto / adverbial
Regla:
Expresiones de frecuencia pueden reforzar una lectura habitual, pero habitual y frecuencia léxica no son la misma cosa.
Uso:
- “todos los días” puede apoyar habitual, pero el aspecto debe analizarse independientemente.

### JLC-PREP-001 — relaciones espaciales y semánticas
Dominio: sintaxis / semántica
Regla:
Las relaciones equivalentes a “en”, “de”, “con”, “para”, “a”, etc. no deben mapearse palabra por palabra desde español.
Uso:
- Almacenar construcciones completas con su relación semántica:
  ORIGEN, DESTINO, LOCACIÓN, COMPAÑÍA, INSTRUMENTO, PROPÓSITO, POSESIÓN, etc.

### JLC-PREP-002 — una misma forma puede cubrir varias relaciones
Dominio: polisemia / sintaxis
Regla:
Una partícula o preposición puede tener más de una función según la construcción.
Uso:
- ANALYZER: resolver por contexto.
- GENERATOR: seleccionar por relación semántica, no por traducción aislada.

### JLC-PART-001 — partículas gramaticales
Dominio: pragmática / sintaxis
Regla:
Partículas pequeñas pueden marcar énfasis, foco, evidencialidad, modalidad, discurso u otras funciones que no siempre tienen traducción directa.
Uso:
- No eliminarlas como “ruido”.
- TUTOR: explicar función aunque no haya equivalente español.
- GENERATOR: no insertar partículas sin patrón documentado.

### JLC-PART-002 — `nda'` como caso de análisis abierto
Dominio: benchmark / partículas
Regla:
`nda'` está documentada como partícula con funciones pragmáticas; su función en FB-062 `zeenda`/`zee+nda'` sigue abierta.
Uso:
- Mantener hipótesis morfológica sin fijar significado.
- Requiere confirmación contextual/hablante.

### JLC-PART-003 — alcance pragmático
Dominio: pragmática
Regla:
Las partículas pueden afectar una palabra, un constituyente o toda la oración.
Uso:
- ANALYZER: estimar alcance antes de glosar.
- TUTOR: distinguir “qué significa” de “qué efecto produce”.

### JLC-ADV-004 — prioridad de corpus
Dominio: evidencia
Regla:
Adverbios y partículas deben aprenderse prioritariamente mediante ejemplos de uso y texto paralelo, porque su significado aislado suele ser insuficiente.
Uso:
- Priorizar literatura de Juchitán y ejemplos contextualizados.


---

## Sintaxis básica y orden de constituyentes

### JLC-SYN-001 — orden básico V-S-O
Dominio: sintaxis
Regla:
La Gramática Popular describe como orden básico una organización verbal inicial, típicamente:
VERBO + SUJETO + OBJETO
con extensiones para objeto indirecto y otros complementos.
Uso:
- ANALYZER: preferir lectura verbal inicial cuando la evidencia lo permita.
- GENERATOR: no calcar automáticamente el orden SVO del español.
- TUTOR: explicar que el verbo puede aparecer antes del sujeto.

### JLC-SYN-002 — orden básico no equivale a orden obligatorio
Dominio: sintaxis / pragmática
Regla:
El orden básico puede alterarse por foco, tópico, contraste, interrogación u otras funciones discursivas.
Uso:
- ANALYZER: no marcar como error una desviación del orden básico sin revisar función informativa.
- GENERATOR: usar movimiento sólo con patrón documentado.

### JLC-SYN-003 — sujeto pronominal y sujeto recuperable
Dominio: sintaxis / persona
Regla:
La persona puede estar codificada dentro del verbo o mediante pronombres dependientes, y ciertos sujetos pueden omitirse si son recuperables por contexto.
Uso:
- No exigir un pronombre independiente equivalente a “yo/tú/él” en cada oración.
- TUTOR: distinguir sujeto semántico de palabra pronominal independiente.

### JLC-SYN-004 — objeto y participantes
Dominio: sintaxis / valencia
Regla:
La estructura de argumentos depende de la valencia del verbo.
Uso:
- ANALYZER: identificar verbo antes de asignar sujeto/objeto.
- GENERATOR: consultar marco argumental del lema.

### JLC-SYN-005 — tópico y foco
Dominio: pragmática / sintaxis
Regla:
Un constituyente puede desplazarse o destacarse para indicar:
- tema/tópico;
- foco informativo;
- contraste;
- corrección.
Uso:
- TUTOR: explicar por qué una frase no sigue el orden básico.
- GENERATOR: no mover constituyentes sin intención discursiva.

### JLC-SYN-006 — foco no es énfasis genérico
Dominio: pragmática
Regla:
FOCO = información seleccionada como especialmente relevante o contrastiva.
TÓPICO = entidad o asunto sobre el que se organiza el enunciado.
No confundir ambos con “hablar más fuerte”.
Uso:
- Mantener campos `information_structure` y `pragmatic_function`.

### JLC-SYN-007 — análisis por capas
Dominio: arquitectura
Orden sugerido:
1. localizar predicado principal;
2. identificar clase/aspecto/persona verbal;
3. recuperar valencia;
4. asignar participantes;
5. detectar tópico/foco;
6. analizar modificadores;
7. producir estructura literal;
8. producir interpretación natural.

### JLC-SYN-008 — generación no calca español
Dominio: generación
Regla:
El GENERATOR_ENGINE debe partir de:
- intención;
- predicado;
- participantes;
- estructura informativa;
y después seleccionar orden de didxazá.
No usar español SVO como plantilla intermedia obligatoria.


---

## Combinación de oraciones: coordinación y subordinación

### JLC-CLAUSE-001 — oración compleja
Una oración compleja puede contener dos o más oraciones relacionadas por coordinación o subordinación.
Fuente: Gramática Popular, cap. 14.

### JLC-COORD-001 — coordinación con `ne`
`ne` coordina oraciones con valor equivalente a “y”. Con más de dos coordinadas puede aparecer entre cada par o sólo antes de la última.
Fuente: Gramática Popular §14.1.

### JLC-SUB-001 — complemento oracional sin `que`
El didxazá no requiere una conjunción equivalente al español `que` para introducir una oración que funciona como complemento directo. El complemento sigue después del sujeto o del objeto indirecto del verbo principal.
Fuente: Gramática Popular §14.2.1.
Ejemplo: `Gúdxibe lii [cheu' Lulá']` ≈ “Él dijo que te vayas a Oaxaca”.

### JLC-SUB-002 — `querer` y `saber cómo`
Los verbos equivalentes a `querer` y `saber` en el sentido de “saber cómo hacer algo” requieren un complemento oracional cuyo sujeto comparte referencia con el sujeto principal.
Fuente: Gramática Popular §14.2.1.

### JLC-SUB-003 — subordinadas adverbiales
Las subordinadas adverbiales pueden expresar tiempo, lugar, modo, propósito, causa, concesión, condición o comparación.
Fuente: Gramática Popular §14.2.3.

### JLC-SUB-004 — `la?` como frontera
Cuando una subordinada adverbial aparece al principio, puede terminar con la partícula `la?`, descrita por la Gramática como equivalente funcional de una coma.
Fuente: Gramática Popular §14.2.3.

### JLC-SUB-005 — relaciones temporales
No existe una sola equivalencia mecánica para “cuando”. La GP documenta distintas construcciones para cuando, antes de que y mientras.
Fuente: Gramática Popular §14.2.3.

### JLC-SUB-006 — locativo `ra`
`ra` puede introducir una oración locativa con sentido equivalente a “donde” en construcciones documentadas.
Fuente: Gramática Popular §14.2.3.

### JLC-SUB-007 — subordinación y aspecto
La subordinación puede condicionar el aspecto del verbo dependiente; el potencial aparece en varios contextos subordinados documentados.
Uso: resolver primero la relación entre cláusulas y luego el aspecto.

### JLC-SUB-008 — generación por relación semántica
El generador debe representar primero relaciones como CAUSA, CONDICIÓN, TIEMPO, PROPÓSITO, CONCESIÓN, LUGAR, COMPARACIÓN o COMPLEMENTO, y después seleccionar la construcción didxazá correspondiente.
El español funciona como puente semántico, no como plantilla sintáctica.


---

## Oraciones relativas

### JLC-REL-001 — relativa como modificador nominal
Dominio: sintaxis / frase nominal
Regla:
Una oración relativa se presenta dentro de una frase nominal y funciona como modificador del sustantivo, de manera semejante a un adjetivo.
Fuente: Gramática Popular §14.3.
Uso:
- ANALYZER: vincular la relativa con el sustantivo antecedente.
- TUTOR: explicar que una oración completa puede describir a un nombre.
- GENERATOR: construir la frase nominal completa, no traducir sólo `que`.

### JLC-REL-002 — `ni` como relativo
Dominio: sintaxis / relativización
Regla:
La Gramática Popular documenta `ni` con función REL en oraciones relativas.
Ejemplos:
- `gunaa [ni nadxii Ale]` — “la mujer que ama a Alex / a quien Alex ama”.
- `ba'du' [ni bí'yalu']` — “el niño que viste”.
Fuente: Gramática Popular §14.3.
Uso:
- No reducir `ni` a una única glosa española.
- Resolver la función del referente dentro de la relativa por estructura y valencia.

### JLC-REL-003 — rol interno ambiguo por traducción
Dominio: sintaxis / semántica
Regla:
Una misma relativa puede admitir traducciones españolas distintas según la asignación de roles; la forma relativa no codifica necesariamente mediante una palabra equivalente a `quien/a quien` la función española.
Fuente: GP ejemplo 166a.
Uso:
- ANALYZER: usar valencia, orden y contexto para decidir roles.
- TUTOR: separar estructura didxazá de las alternativas naturales en español.

### JLC-REL-004 — relativo oblicuo / relación preposicional
Dominio: relativización / preposiciones
Regla:
La relativa puede modificar un antecedente que corresponde a un participante oblicuo. La GP ejemplifica una construcción literalmente equivalente a “el niño que vendiste huevos a”.
Fuente: Gramática Popular §14.3, ejemplo 167.
Uso:
- No exigir una forma española equivalente a `a quien`.
- ANALYZER: reconstruir la relación oblicua dentro de la relativa.

### JLC-REL-005 — relativas sin antecedente expreso
Dominio: nominalización / sintaxis
Regla:
Una oración relativa puede aparecer sin sustantivo antecedente y funcionar por sí misma como sujeto u objeto, con significado indefinido equivalente a “lo que...”.
Ejemplos:
- `[ni bí'nilu' que]` — “lo que hiciste”.
- `[ni nápalu']` — “lo que tienes”.
Fuente: Gramática Popular §14.3.
Uso:
- ANALYZER: permitir `REL_CLAUSE` como argumento nominal.
- GENERATOR: no insertar obligatoriamente un sustantivo equivalente a “cosa”.

### JLC-REL-006 — antecedente + relativa como una unidad
Dominio: arquitectura
Regla:
La unidad de análisis debe ser:
`[ANTECEDENTE [RELATIVA]]`
y no una secuencia lineal independiente.
Uso:
- Mantener enlace `relative_head`.
- Calcular el rol del antecedente en la oración principal y por separado su rol recuperado dentro de la relativa.

### JLC-REL-007 — generación por función, no por `que`
Dominio: generación
Regla:
El generador debe partir de:
1. entidad a describir;
2. proposición que la identifica;
3. papel de esa entidad dentro de la proposición;
4. construcción relativa documentada.
No debe partir de `que = ni` como sustitución mecánica.

### JLC-REL-008 — relativa vs complemento
Dominio: desambiguación
Regla:
Distinguir:
- complemento oracional de un verbo: “dijo [que...]”;
- relativa que modifica un nombre: “el niño [que...]”.
La ausencia/presencia de un sustantivo antecedente y la función sintáctica de la cláusula son diagnósticos clave.
Uso:
- ANALYZER: no confundir `ni` relativo con otros usos de `ni`.


---

## Texto corrido 01 — `Chonna bi'chi'` (“Los tres hermanos”)

### JLC-TEXT-001 — texto corrido como evidencia de integración
Dominio: discurso / sintaxis / morfología
Regla:
Los textos completos de GP deben tratarse como evidencia integrada para observar:
- encadenamiento aspectual;
- referencia pronominal;
- coordinación;
- subordinación;
- estructura informativa;
- léxico en contexto.
Fuente: Gramática Popular cap. 15.

### JLC-TEXT-002 — apertura narrativa con `Sicarí'`
Dominio: discurso
Ejemplo:
`Sicarí' bizaacalú chonna ba'dunguiiu.`
GP: “Esto fue lo que aconteció a tres jóvenes.”
Análisis documentado:
`sicarí'` “así”; `bizaacalú` = C-acontecer-cara.
Uso:
- `sicarí'` funciona como organizador de apertura narrativa.
- No reducirlo a glosa aislada sin función discursiva.

### JLC-TEXT-003 — orden verbal inicial en narrativa
Dominio: sintaxis
Ejemplos:
`Biaana stubi guionna' bí'chica'.`
“Los tres hermanos se quedaron solos.”
`Guti jñaaca'.`
“Murió su madre.”
Uso:
- confirma verbo inicial en discurso narrativo real.
- sujeto/participante puede aparecer después o estar incorporado/poseído.

### JLC-TEXT-004 — posesión inherente en texto corrido
Dominio: posesión
Ejemplo:
`jñaaca'` = “su madre / madre de ellos”.
Uso:
- confirma que parentesco poseído aparece sin una palabra independiente equivalente a “su”.
- integrar POS + persona/plural dentro de análisis nominal.

### JLC-TEXT-005 — coordinación con `ne`
Dominio: coordinación
Ejemplo:
`Chupa que ... ne stobi que ...`
“Dos de ellos ... y el otro ...”
Uso:
- confirma `ne` como coordinador en narrativa.

### JLC-TEXT-006 — relativo `ni` en discurso real
Dominio: relativización
Ejemplo:
`guiropa' ni nuu xpiaani' que`
“los dos que eran inteligentes”
Uso:
- confirma relativa postnominal con `ni` en texto narrativo.
- analizar antecedente + relativa como unidad.

### JLC-TEXT-007 — demostrativo `que` y seguimiento referencial
Dominio: discurso / frase nominal
Regla:
El texto usa repetidamente `que` tras nombres o grupos nominales para mantener/reidentificar referentes.
Uso:
- estudiar como parte del sistema demostrativo/discursivo.
- no traducir siempre de manera independiente en español natural.

### JLC-TEXT-008 — completivo como motor narrativo
Dominio: aspecto / discurso
Regla:
En el arranque del cuento predominan formas completivas para avanzar la secuencia de eventos:
aconteció, quedaron, murió, frieron, buscaron...
Uso:
- el completivo tiene función narrativa de eventos cerrados/secuenciados, no sólo “pasado”.


---

## Texto corrido 02 — diálogo, deseo y potencial en `Chonna bi'chi'`

### JLC-TEXT-009 — paso de narración a diálogo
Dominio: discurso
Regla:
En texto corrido, el análisis debe distinguir:
- voz del narrador;
- habla directa de personajes;
- contenido pensado, soñado o deseado.
Uso:
- ANALYZER: representar `speaker`, `addressee`, `speech_mode`.
- TUTOR: explicar cuándo cambia la voz discursiva.
- GENERATOR: no mantener automáticamente el mismo registro narrativo dentro del diálogo.

### JLC-TEXT-010 — discurso directo como cambio de deixis
Dominio: pragmática / persona
Regla:
Al entrar en habla directa cambian los centros de referencia:
- primera persona = hablante del diálogo;
- segunda persona = interlocutor;
- tiempo/lugar pueden reinterpretarse desde ese hablante.
Uso:
- Resolver persona dentro del marco del discurso citado, no desde el narrador.

### JLC-TEXT-011 — deseo y evento no realizado
Dominio: modalidad / aspecto
Regla:
Los pasajes donde los personajes hablan de lo que quieren, esperan, sueñan o podrían hacer introducen eventos no realizados.
Uso:
- ANALYZER: considerar potencial/irrealizado según construcción documentada.
- TUTOR: distinguir evento narrado como hecho de evento concebido/deseado.

### JLC-TEXT-012 — comparación como relación semántica
Dominio: semántica / sintaxis
Regla:
Cuando los personajes comparan sueños, cualidades o resultados, el motor debe representar:
`COMPARE(entity_a, entity_b, dimension)`
antes de seleccionar la construcción superficial.
Uso:
- No reducir comparación a una sola palabra equivalente a “más”.

### JLC-TEXT-013 — transición aspectual por plano discursivo
Dominio: aspecto / discurso
Regla:
En narración, el completivo puede avanzar la historia; dentro de diálogo, deseo o plan pueden aparecer potencial, futuro u otras formas.
Uso:
- El aspecto depende también del plano discursivo:
  NARRATED_EVENT vs PROPOSED_EVENT vs DESIRED_EVENT vs EXPECTED_EVENT.

### JLC-TEXT-014 — contenido de sueño
Dominio: discurso / evidencialidad
Regla:
Un sueño introduce un mundo discursivo no idéntico al mundo narrado.
Uso:
- Representar `embedded_world = dream`.
- No interpretar automáticamente eventos del sueño como hechos del relato principal.
- TUTOR: separar “ocurrió en la historia” de “ocurrió dentro del sueño”.

### JLC-TEXT-015 — seguimiento de referentes en diálogo
Dominio: discurso / referencia
Regla:
Al alternar narrador y personajes, pronombres dependientes, demostrativos y omisión de tercera persona deben resolverse contra el hablante activo y el referente vigente.
Uso:
- Mantener pila de referentes discursivos.
- No resolver tercera persona sólo por proximidad lineal.


---

## Texto corrido 03 — desenlace, inferencia y coherencia narrativa

### JLC-TEXT-016 — significado dependiente de contexto amplio
Dominio: discurso / semántica
Regla:
La interpretación de una oración en texto corrido puede depender de información introducida varias oraciones antes.
Uso:
- ANALYZER: mantener contexto discursivo persistente.
- TUTOR: explicar antecedentes relevantes cuando una frase aislada sea insuficiente.
- GENERATOR: conservar coherencia entre eventos y referentes.

### JLC-TEXT-017 — expectativa narrativa
Dominio: pragmática / discurso
Regla:
Un relato puede establecer una expectativa mediante planes, promesas, comparaciones o conocimiento compartido y luego explotarla en el desenlace.
Uso:
- Representar `narrative_expectation` y su satisfacción/ruptura cuando sea relevante.
- No reducir ironía o giro a semántica local de una sola oración.

### JLC-TEXT-018 — inferencia
Dominio: semántica / pragmática
Regla:
Parte del significado de un texto puede ser inferido y no expresado literalmente.
Distinguir:
- `asserted`: dicho explícitamente;
- `entailed`: consecuencia lingüística;
- `inferred`: conclusión contextual plausible.
Uso:
- TUTOR: marcar inferencias como tales.
- GENERATOR: no convertir inferencias del lector en hechos explícitos sin intención.

### JLC-TEXT-019 — ironía y contraste narrativo
Dominio: pragmática
Regla:
La ironía narrativa puede surgir de la diferencia entre:
- lo que un personaje cree o espera;
- lo que el narrador/lector sabe;
- lo que finalmente ocurre.
Uso:
- ANALYZER: representar perspectivas separadas.
- TUTOR: explicar el contraste sin atribuir a una palabra aislada el significado irónico.

### JLC-TEXT-020 — perspectiva de personaje
Dominio: discurso
Regla:
Cada personaje puede mantener un estado epistémico propio:
- qué sabe;
- qué cree;
- qué ha visto;
- qué ignora.
Uso:
- Resolver acciones y reacciones con `character_knowledge_state`.
- Distinguir conocimiento del narrador y conocimiento de personaje.

### JLC-TEXT-021 — referencia a través de varias oraciones
Dominio: correferencia
Regla:
Pronombres, posesivos, demostrativos y sujetos omitidos pueden recuperar referentes establecidos a distancia.
Uso:
- No resolver referencia únicamente por el sustantivo más cercano.
- Mantener saliencia y continuidad temática.

### JLC-TEXT-022 — eventos principales vs fondo
Dominio: aspecto / discurso
Regla:
En narrativa, ciertos eventos hacen avanzar la historia mientras otros aportan estado, descripción, explicación o contexto.
Uso:
- Etiquetas:
  `FOREGROUND_EVENT`
  `BACKGROUND_STATE`
  `EXPLANATION`
  `QUOTED_CONTENT`
- El completivo suele correlacionarse con primer plano narrativo, pero no debe convertirse en equivalencia absoluta.

### JLC-TEXT-023 — unidad mínima para tutor de textos
Dominio: pedagogía
Regla:
Para una frase de texto corrido, el tutor debe poder entregar:
1. frase;
2. segmentación;
3. traducción literal;
4. traducción natural;
5. antecedente/referentes;
6. función dentro del relato;
7. inferencias necesarias;
8. provenance.


---

## Texto corrido 04 — `Xtiidxa' ti binnigüé'` (“Cuento de un borracho”)

### JLC-TEXT-024 — irrealizado bajo deseo/intención
`gucala'dxi' nidi'di'` = “quiso atravesar”.
GP analiza `gucala'dxi'` como C-querer y `nidi'di'` como I-pasar.
El irrealizado aparece en una acción deseada/no afirmada todavía como realizada.
Fuente: GP §15.2, ej. 188.

### JLC-TEXT-025 — `ante` + irrealizado + `la?`
`Ante ñábabe la?` = “Antes de lanzarse...”.
`ñábabe` = I-caer-3P.
La subordinada temporal prospectiva puede usar irrealizado; `la?` marca frontera.
Fuente: GP §15.2, ej. 189.

### JLC-TEXT-026 — diálogo e imperativo
`bicaa ndo'pa' ca de'chu'` = “colócate esa jícara en la espalda”.
Mantener el imperativo como construcción documentada, no derivarlo mecánicamente.
Fuente: GP §15.2, ej. 189.

### JLC-TEXT-027 — negación + irrealizado
`Laabe qué ninabe` = “Él no quiso”.
`qué` NEG + `ninabe` I-querer-3P.
Fuente: GP §15.2, ej. 190.

### JLC-TEXT-028 — alternancia por estatus del evento
`qué ninabe, biábabe guiigu'`
combina irrealizado bajo negación con completivo de caer en el evento efectivamente realizado.
Fuente: GP §15.2, ej. 190.

### JLC-TEXT-029 — progresivo como fondo narrativo
`Galaati' zebe la? ...` = “Cuando iba a la mitad del río...”.
`zebe` = PR-ir-3P.
Fuente: GP §15.2, ej. 191.

### JLC-TEXT-030 — progresivo interrumpido por completivo
Patrón textual documentado:
BACKGROUND_PROGRESSIVE → FOREGROUND_COMPLETIVE.
Ej.: “iba...” → “un remolino lo hundió”.
Fuente: GP §15.2, ej. 191.

### JLC-TEXT-031 — `ora` + eventos logrados
`Ora gunda gulee íquebe la? gunábabe...`
contiene C-poder + C-sacar + C-pedir.
Fuente: GP §15.2, ej. 192.

### JLC-TEXT-032 — partes del cuerpo y espacio
`de'chu'` “tu espalda”; `íquebe` “su cabeza”.
Analizar posesión y estructura corporal antes de calcar preposiciones españolas.

### JLC-ASPECT-REV-001 — revisión de `irrealizado`
La explicación anterior “pasaría/habría pasado si...” era demasiado estrecha.
Definición ampliada:
IRREALIZADO presenta un evento como no realizado o no aseverado como hecho dentro de construcciones como contrafactual, deseo/intención, ciertos negativos y ciertas subordinadas prospectivas.


---

## Texto corrido 05 — `Diidxazá` (“El Zapoteco”)

### JLC-TEXT-033 — género poético como capa interpretativa
Dominio: discurso / género
Regla:
Un texto poético puede usar personificación, metáfora, repetición y equivalencias no literales.
Uso:
- ANALYZER: separar estructura lingüística de figura retórica.
- TUTOR: ofrecer análisis literal y lectura poética por capas.
- GENERATOR: no usar poesía como plantilla neutral de conversación sin marcar género.
Fuente: GP §15.3.

### JLC-TEXT-034 — estativo de decir como atribución
Dominio: aspecto / evidencialidad discursiva
Ejemplo:
`Nácabe ma' che' diidxazá` ≈ “Dicen que se va el zapoteco”.
GP: `nácabe` = ES-decir-PL-3P.
Regla:
La forma estativa de “decir” puede introducir una afirmación atribuida a otros.
Uso:
- representar `reported_claim`, no asumir compromiso directo del hablante.
Fuente: GP ej. 193.

### JLC-TEXT-035 — `ma'` no fija por sí solo el aspecto
Dominio: adverbio / aspecto
Regla:
`ma'` “ya” coocurre en el poema con potencial, futuro y completivo.
Consecuencia:
El adverbio temporal/discursivo no determina por sí solo el aspecto verbal.
Fuente: GP ejs. 193–194.

### JLC-TEXT-036 — potencial de movimiento en metáfora
Dominio: aspecto / semántica
Ejemplo:
`che' diidxazá` = P-ir + lengua zapoteca, traducido “se va el zapoteco”.
Regla:
Una forma potencial puede participar en una predicación metafórica de desaparición.
Uso:
- no inferir movimiento físico automáticamente.
Fuente: GP ej. 193.

### JLC-TEXT-037 — futuro explícito
Dominio: aspecto / discurso
Ejemplos:
- `zaní' laa` ≈ “lo hablará”
- `ziné ... laa` ≈ “se la llevará”
- `zanitilu'` ≈ “te perderás”
Regla:
El futuro aparece en predicciones y proyecciones explícitas.
Uso:
- distinguir FUTURE_ASSERTION de potencial y habitual.
Fuente: GP ejs. 193, 194, 196.

### JLC-TEXT-038 — negación existencial/pronominal
Dominio: negación
Ejemplo:
`ma' guiruti' zaní' laa` ≈ “ya nadie lo hablará”.
Regla:
La negación puede estar distribuida mediante un pronombre negativo como `guiruti'` “nadie”, no sólo mediante `qué`.
Uso:
- identificar tipo de negación antes de buscar marcador verbal.
Fuente: GP ej. 193.

### JLC-TEXT-039 — completivo con resultado discursivo
Dominio: aspecto
Ejemplo:
`ma' birá, biluxe` ≈ “ya se acabó, terminó / ha muerto”.
Regla:
Completivos de terminar/acabarse pueden describir estado resultante y recibir traducción española no literal.
Fuente: GP ej. 193.

### JLC-TEXT-040 — habitual para práctica social
Dominio: aspecto / discurso
Ejemplo:
`guirá' riní' diidxastiá` ≈ “sólo hablan español”.
GP analiza `riní'` como H-hablar.
Regla:
El habitual puede describir una práctica social vigente, no sólo una rutina individual.
Fuente: GP ej. 194.

### JLC-TEXT-041 — relativo plural `cani`
Dominio: relativización / número
Ejemplo:
`cani bidiideche lii` ≈ “quienes te menospreciaron”.
GP: PL-REL + C-dar-espalda + 2SG.
Regla:
`cani` funciona como forma relativa plural en el ejemplo.
Uso:
- distinguir `ni` relativo de `cani` plural relativo.
Fuente: GP ej. 195.

### JLC-TEXT-042 — compuesto verbal idiomático
Dominio: composición / semántica
Ejemplo:
`bidiideche` = C-dar-espalda, traducido “menospreciaron”.
Regla:
Un compuesto con parte del cuerpo puede tener significado convencional no recuperable por suma literal.
Uso:
- almacenar literal `dar-espalda` y significado convencional `menospreciar`.
Fuente: GP ej. 195.

### JLC-TEXT-043 — negación + potencial en conocimiento
Dominio: negación / aspecto
Ejemplo:
`que gannadica' pabiá'` ≈ “no saben cuánto”.
GP: NEG + P-saber-PL + cuánto.
Regla:
El potencial aparece dentro de una construcción negativa de saber.
No asignar significado “quizá” automáticamente al potencial.
Fuente: GP ej. 195.

### JLC-TEXT-044 — habitual causativo/compuesto `rusibani`
Dominio: morfología / aspecto
Ejemplo:
`diidxa' rusibani naa` ≈ “lengua que me da la vida”.
GP: H-dar-vida + 1SG.
Regla:
El habitual puede caracterizar una relación duradera/definitoria.
Fuente: GP ej. 196.

### JLC-TEXT-045 — persona explícita + persona verbal
Dominio: persona / foco
Ejemplo:
`naa nanna` ≈ “yo sé”.
GP: `naa` 1SG independiente + `nanna` ES-saber-1SG.
Regla:
Un pronombre independiente puede coexistir con persona ya codificada en el predicado, con valor discursivo/enfático.
Uso:
- no tratar esta aparente redundancia como error.
Fuente: GP ej. 196.

### JLC-TEXT-046 — subordinada temporal poética
Dominio: subordinación / aspecto
Ejemplo:
`dxi iuiti gubidxa ca` ≈ “el día que muera el sol”.
GP: día + P-perderse + sol + demostrativo.
Regla:
La subordinada temporal puede seleccionar potencial para un evento futuro/no realizado.
Fuente: GP ej. 196.

### JLC-TEXT-047 — personificación de la lengua
Dominio: pragmática / género
Regla:
El poema trata `diidxazá` como interlocutor de segunda persona:
- `lii`
- `zanitilu'`
Esto es personificación, no evidencia de que el sustantivo léxico sea humano en el sistema pronominal general.
Uso:
- no generalizar selección pronominal poética a prosa neutral.
Fuente: GP ejs. 195–196.


---

## Texto corrido 06 — `Bacaanda'` (“El sueño”)

### JLC-TEXT-048 — verbo complejo `guniéxcaanda'`
Dominio: composición / persona / discurso
Ejemplo:
`Nuchi' guniéxcaanda'`
“Anoche soñé que...”
GP analiza la forma como C-hablar-1SG-sueño-1SG.
Regla:
La expresión de “soñar” aparece como verbo complejo lexicalizado; no debe reconstruirse por traducción española palabra por palabra.
Fuente: Gramática Popular §15.4, ej. 197.

### JLC-TEXT-049 — inclusivo en estado compartido
Dominio: persona / estativo
Ejemplo:
`zúbanu`
“estábamos sentados”
GP: ES-sentado-1PLINC.
Regla:
El inclusivo `nu` codifica un “nosotros” que incluye al interlocutor o referente compartido del poema.
Fuente: GP ej. 197.

### JLC-TEXT-050 — relaciones espaciales con partes del cuerpo
Dominio: espacio / léxico corporal
Ejemplo:
`xañee ti yaga`
“al pie / debajo de un árbol”
GP glosa `xañee` como “bajo-pie”.
Regla:
Las relaciones espaciales pueden conceptualizarse mediante partes del cuerpo.
Uso:
- no calcar automáticamente preposiciones españolas;
- almacenar BODY_PART_SCHEMA + SPACE_RELATION.
Fuente: GP ej. 197.

### JLC-TEXT-051 — progresivo descriptivo
Dominio: aspecto / discurso
Ejemplos:
`caguiñe ti bi nanda`
“soplaba un viento frío”
`cusaba stale bandaga`
“tiraba muchas hojas”
Regla:
El progresivo puede construir el escenario sensorial de un poema o narración, no sólo marcar una acción focal en curso.
Fuente: GP ej. 197.

### JLC-TEXT-052 — coordinación de fondo con `ne`
Dominio: coordinación / discurso
Ejemplo:
progresivo del viento `ne` progresivo de hojas que caen.
Regla:
`ne` coordina estados/eventos paralelos dentro del fondo descriptivo.
Fuente: GP ej. 197.

### JLC-TEXT-053 — relativa/locativa con `ra`
Dominio: subordinación locativa
Ejemplo:
`gaxha neza ra nuunu`
“cerca del camino donde estábamos”
GP:
`ra` LOC + `nuunu` ES-estar-1PLINC.
Regla:
`ra` introduce una localización definida por una oración completa.
Fuente: GP ej. 198.

### JLC-TEXT-054 — progresivo de flujo
Dominio: aspecto / lexical semantics
Ejemplo:
`cuxooñe' ti nisa ya`
“fluía un arroyo limpio”
GP: PR-correr + agua limpia.
Regla:
Un verbo equivalente a “correr” puede conceptualizar flujo de agua; traducción natural española puede ser “fluir”.
Uso:
- conservar literal y natural.
Fuente: GP ej. 198.

### JLC-TEXT-055 — comparación con `sicagá`
Dominio: comparación / discurso
Ejemplo:
`sicagá dxa nisa ...`
“como aquella agua...”
Regla:
`sicagá` introduce comparación/similitud en el poema.
Uso:
- almacenar como construcción comparativa contextual, no simple equivalencia universal.
Fuente: GP §15.4.

### JLC-TEXT-056 — relativo `ni` dentro de imagen poética
Dominio: relativización
Ejemplo:
`ni rusa'bu' ...`
“que derramabas...”
GP: REL + H-CAUS-caerse-2SG.
Regla:
La relativa amplía el referente comparado y participa en una imagen poética compleja.
Fuente: GP §15.4, ej. 198.

### JLC-TEXT-057 — causativo lexicalizado de caída
Dominio: causatividad / aspecto
Ejemplo:
`rusa'bu'`
GP: H-CAUS-caerse-2SG
Traducción natural: “derramabas”.
Regla:
“hacer caer” puede lexicalizarse como “derramar” según el objeto/contexto.
Uso:
- no producir traducción literal “hacer caer” cuando el sentido convencional sea flujo/derrame.
Fuente: GP ej. 198.

### JLC-TEXT-058 — poesía y cambio de traducción aspectual
Dominio: traducción / aspecto
Regla:
La traducción española publicada puede usar imperfecto (“derramabas”) para una forma habitual didxazá.
Consecuencia:
No identificar tiempo verbal español con aspecto didxazá.
Fuente: GP ej. 198.

### JLC-TEXT-059 — capas de una imagen poética
Dominio: tutor / semántica
Regla:
Para una imagen poética, el tutor debe distinguir:
1. forma morfológica;
2. estructura literal;
3. referente;
4. comparación/metáfora;
5. traducción literaria natural.
Uso:
Evitar enseñar metáfora como significado léxico básico.


---

## Texto corrido 07 — trabalenguas como evidencia fonológica

### JLC-TONGUE-001 — trabalenguas como prueba de contraste
Dominio: fonología / léxico
Regla:
Los trabalenguas reúnen formas fonológicamente cercanas para explotar contrastes reales de la lengua.
Uso:
- ANALYZER: no colapsar cadenas parecidas.
- CORRECTOR: elevar umbral antes de proponer sustitución entre vecinos fonológicos.
- TUTOR: mostrar qué rasgo distingue formas próximas.

### JLC-TONGUE-002 — similitud gráfica ≠ identidad léxica
Dominio: ortografía / fonología
Regla:
Dos formas que difieren en un segmento, tono, glotalización, longitud vocálica o acento pueden ser palabras distintas.
Uso:
- preservar diacríticos y apóstrofos;
- no normalizar antes del análisis;
- comparar representación fonológica además de superficie.

### JLC-TONGUE-003 — tono y glotalización como rasgos contrastivos
Dominio: fonología
Regla:
En Juchitán, tono, tipo vocálico y glotalización pueden distinguir significados.
Uso:
- mantener campos separados:
  `segmental_form`
  `tone`
  `vowel_type`
  `glottalization`
  `stress`
- si faltan datos, conservar ambigüedad.

### JLC-TONGUE-004 — pares/minimalidad práctica
Dominio: pruebas
Regla:
Los trabalenguas pueden alimentar un banco de “vecinos mínimos” o casi mínimos para probar:
- reconocimiento;
- corrección;
- audio;
- tutoría.
Uso:
- testear que el corrector no confunda formas cercanas sólo por distancia de edición.

### JLC-TONGUE-005 — velocidad no elimina estructura
Dominio: audio / discurso
Regla:
En habla rápida pueden reducirse fronteras acústicas sin que cambie necesariamente la estructura morfológica u ortográfica.
Uso:
- no inferir espacios desde pausas acústicas;
- no inferir ausencia de morfema por reducción fonética.

### JLC-TONGUE-006 — repetición como evidencia de categoría
Dominio: análisis
Regla:
La repetición de secuencias similares dentro de un trabalenguas ayuda a identificar qué parte se mantiene y cuál contrasta.
Uso:
- alinear variantes para localizar rasgo contrastivo;
- no atribuir significado por mera semejanza.

### JLC-TONGUE-007 — valor para ASR y tutor
Dominio: arquitectura
Regla:
Los trabalenguas son P0/P1 para entrenamiento/evaluación de discriminación auditiva, pero no para generación conversacional neutral.
Uso:
- AUDIO_ENGINE: discriminación de contrastes.
- TUTOR_ENGINE: ejercicios de escucha/pronunciación.
- GENERATOR_ENGINE: no usar como fuente estilística general.


---

## Texto corrido 08 — receta e instrucciones procedimentales

### JLC-PROC-001 — género procedimental
Dominio: discurso / pragmática
Regla:
Una receta organiza acciones orientadas a una meta mediante una secuencia temporal y causal.
Uso:
- ANALYZER: distinguir `GOAL`, `INGREDIENT`, `INSTRUMENT`, `STEP`, `RESULT`.
- TUTOR: explicar acción + orden + propósito.
- GENERATOR: modelar procedimientos como secuencia estructurada, no como frases aisladas.

### JLC-PROC-002 — imperativos/instrucciones
Dominio: modo
Regla:
Las recetas concentran mandatos e instrucciones y permiten observar formas imperativas en contexto no confrontativo.
Uso:
- diferenciar orden fuerte de instrucción procedimental.
- `speech_act = instruction`, aunque la forma sea imperativa.

### JLC-PROC-003 — secuencia temporal
Dominio: discurso / tiempo
Regla:
Las acciones procedimentales se organizan por relaciones como:
FIRST, THEN, AFTER, UNTIL, WHEN_READY.
Uso:
- GENERATOR: preservar dependencia entre pasos.
- No tratar cada verbo como evento independiente sin orden.

### JLC-PROC-004 — aspecto en procedimientos
Dominio: aspecto
Regla:
El aspecto seleccionado en una instrucción depende de la construcción procedural y de si la acción se presenta como mandato, resultado alcanzado o estado objetivo.
Uso:
- no mapear automáticamente imperativo español a una única forma aspectual.

### JLC-PROC-005 — “hasta que” y condición de terminación
Dominio: subordinación / aspecto
Regla:
Las recetas suelen usar una condición de terminación:
hacer X hasta que Y alcance cierto estado.
Uso:
- representar `TERMINATION_CONDITION`.
- El estado Y no es un evento independiente, sino criterio para detener el paso anterior.

### JLC-PROC-006 — cantidades y medida
Dominio: semántica / numerales
Regla:
Ingredientes pueden aparecer con números, cuantificadores, unidades, recipientes o porciones.
Uso:
- almacenar cantidad separada del sustantivo:
  `quantity`
  `unit/container`
  `ingredient`
- no asumir equivalencia 1:1 de unidades españolas y didxazá.

### JLC-PROC-007 — instrumentos y relaciones espaciales
Dominio: sintaxis / semántica
Regla:
Una instrucción puede especificar instrumento, recipiente, superficie o destino.
Uso:
- distinguir:
  INSTRUMENT (“con…”)
  CONTAINER (“en…”)
  DESTINATION (“a…”)
  SOURCE (“de…”)
- seleccionar construcción didxazá por relación semántica.

### JLC-PROC-008 — objetos omitidos por continuidad
Dominio: discurso / referencia
Regla:
En procedimientos, el objeto procesado puede omitirse cuando sigue siendo altamente saliente:
“muélelo; después ponlo…”
Uso:
- mantener `current_patient/topic`.
- no interpretar cada sujeto/objeto cero como entidad nueva.

### JLC-PROC-009 — cambio de estado
Dominio: semántica verbal
Regla:
Las recetas contienen muchos verbos de cambio de estado:
cocer, moler, mezclar, cortar, hervir, dorar, secar, etc.
Uso:
- registrar `initial_state`, `process`, `result_state`.
- útil para causatividad y valencia.

### JLC-PROC-010 — resultado vs manera
Dominio: traducción
Regla:
Una instrucción española puede lexicalizar resultado donde didxazá lexicaliza manera, o viceversa.
Uso:
- tutor conserva literal + natural.
- generador parte de la meta procedural, no del verbo español aislado.

### JLC-PROC-011 — valor para corpus práctico
Dominio: evidencia
Regla:
Las recetas y otros procedimientos tienen alta prioridad para:
- lenguaje de cocina;
- secuencias de instrucciones;
- imperativos;
- medidas;
- conversación orientada a tareas.
No usar como sustituto de diálogo espontáneo, pero sí como evidencia de lenguaje funcional.


---

# Síntesis estructural de la Gramática Popular

## JLC-SYNTH-001 — fonología
Conocimiento consolidado:
- tono contrastivo;
- vocal simple, cortada/glotal y quebrada;
- acento y tono no son intercambiables;
- diacríticos/apóstrofos no deben eliminarse antes del análisis;
- habla rápida no determina límites ortográficos.
Implicación:
CORRECTOR y AUDIO_ENGINE deben preservar forma fonológica completa.

## JLC-SYNTH-002 — persona
Conocimiento consolidado:
- pronombres dependientes;
- 1SG con `-a'/-ya'` y fusiones;
- 2SG con `-lu'/-u'` y alternancias;
- 3P persona/animal/cosa;
- inclusivo `nu` vs exclusivo `du`;
- tercera persona puede recuperarse por contexto;
- pronombre independiente puede coexistir con persona verbal por foco/énfasis.
Implicación:
PERSON != cadena fija.

## JLC-SYNTH-003 — nombres y posesión
Conocimiento consolidado:
- tres estrategias de posesión;
- clase de nombres siempre poseídos;
- parentesco y partes del cuerpo especialmente relevantes;
- cambios morfofonológicos bajo posesión;
- cadenas posesivas;
- derivación nominal con `guenda/enda`.
Implicación:
token ortográfico y morfología interna deben mantenerse separados.

## JLC-SYNTH-004 — sistema verbal
Conocimiento consolidado:
- juegos verbales determinan realizaciones aspectuales;
- habitual, completivo, progresivo, perfecto, potencial, irrealizado, estativo y futuro;
- aspecto no equivale a tiempo español;
- potencial e irrealizado dependen fuertemente de construcción;
- verbos de movimiento tienen paradigmas especiales;
- causativos pueden alterar raíz, derivación y juego;
- verbos compuestos y auxiliares requieren análisis estructural.
Implicación:
prohibido analizar mediante simple “strip prefix + lookup”.

## JLC-SYNTH-005 — aspecto revisado
Resumen operativo:
- HABITUAL: práctica/característica recurrente;
- COMPLETIVO: evento presentado como completo; frecuente en primer plano narrativo;
- PROGRESIVO: evento en curso; puede servir de fondo descriptivo;
- PERFECTO: categoría propia; requiere tratamiento cauteloso y verificación detallada antes de generalizar semántica;
- POTENCIAL: forma seleccionada por múltiples construcciones; no equivale a “quizá”;
- IRREALIZADO: evento no realizado/no aseverado como hecho en ciertos contextos de deseo, negación, prospectividad y contrafactualidad;
- ESTATIVO: estado/predicación estable, sin equivalencia automática con “estar”;
- FUTURO: proyección futura explícita.
Implicación:
ASPECT_MEANING debe ser construcción-dependiente.

## JLC-SYNTH-006 — sintaxis
Conocimiento consolidado:
- orden básico verbal inicial;
- orden no obligatorio;
- tópico/foco alteran orden;
- valencia determina participantes;
- sujeto independiente no es obligatorio si persona está recuperable;
- complementos oracionales pueden carecer de equivalente de `que`;
- subordinadas codifican tiempo, lugar, causa, propósito, condición, comparación, etc.;
- relativas con `ni/cani`;
- relativas sin antecedente pueden funcionar nominalmente.
Implicación:
GENERATOR parte de estructura semántica, no de SVO español.

## JLC-SYNTH-007 — negación e interrogación
Conocimiento consolidado:
- negación interactúa con aspecto/modo;
- prohibición no se deriva sumando “no” al afirmativo;
- hay negación verbal y pronombres negativos;
- interrogación polar vs de contenido;
- tono léxico y entonación interrogativa son capas distintas;
- pregunta puede funcionar pragmáticamente como petición.
Implicación:
forma gramatical y función pragmática se representan por separado.

## JLC-SYNTH-008 — espacio, adverbios y partículas
Conocimiento consolidado:
- preposiciones españolas no tienen mapeo 1:1;
- modelar ORIGEN, DESTINO, LOCACIÓN, INSTRUMENTO, PROPÓSITO, etc.;
- relaciones espaciales pueden usar partes del cuerpo;
- partículas pueden tener función pragmática/discursiva sin traducción léxica directa;
- corpus contextual es prioritario para partículas.
Implicación:
LEXEME_TRANSLATION no basta.

## JLC-SYNTH-009 — discurso
Conocimiento consolidado:
- narración distingue primer plano/fondo;
- diálogo cambia deixis;
- sueños, pensamientos y discurso citado crean mundos embebidos;
- referencia puede cruzar varias oraciones;
- personajes mantienen estados de conocimiento distintos;
- inferencia no debe confundirse con afirmación explícita;
- género modifica interpretación.
Implicación:
ANALYZER necesita contexto discursivo persistente.

## JLC-SYNTH-010 — géneros y provenance
Clases de evidencia:
- gramática: regla explícita;
- narración: discurso/referencia/aspecto;
- poesía: metáfora, énfasis, registro literario;
- trabalenguas: fonología/discriminación;
- receta: procedimiento/imperativos/secuencia;
- corpus paralelo: naturalidad y equivalencia;
- hablante: aceptabilidad contemporánea.
Regla:
Ningún género debe extrapolarse automáticamente a otro.

## JLC-SYNTH-011 — uso formal de trabalenguas
Prioridad:
- TUTOR_ENGINE: ejercicios auditivos de discriminación y pronunciación;
- AUDIO_ENGINE/ASR: benchmark de contrastes cercanos;
- CORRECTOR_ENGINE: pruebas anti-sobrecorrección con vecinos fonológicos;
- PHONOLOGY_TESTSET: pares mínimos/casi mínimos con tono, glotalización, tipo vocálico y consonantes.
No usar:
- como corpus de frecuencia;
- como modelo de conversación;
- como plantilla estilística del GENERATOR_ENGINE.

## JLC-SYNTH-012 — huecos aún abiertos
P0:
1. convertir reglas documentales en estructuras ejecutables;
2. enlazar lemas con paradigmas completos;
3. inventario robusto de partículas/construcciones;
4. modelado tonal usable por corrector/tutor/audio;
5. validar variación contemporánea de Juchitán;
6. corpus paralelo en prosa/conversación para naturalidad;
7. resolver benchmarks COR001 sin overfitting.
P1:
8. marcos de valencia;
9. productividad derivativa real;
10. estructura informativa tópico/foco;
11. coreferencia entre oraciones;
12. registro y género.

## JLC-SYNTH-013 — criterio de suficiencia
La Gramática Popular ya aporta una base estructural suficiente para construir un primer vertical slice lingüístico real.
No aporta por sí sola:
- cobertura léxica suficiente;
- naturalidad conversacional contemporánea;
- productividad segura de todas las reglas;
- decisiones completas de ortografía moderna;
- validación acústica/tonal para todas las formas.
Conclusión:
la siguiente fase no debe ser “seguir extrayendo reglas del libro” indefinidamente, sino convertir lo ya aprendido en capacidad ejecutable y contrastarlo con corpus/hablantes.



---

# SEGUNDA PASADA INTEGRAL — CORRECCIONES, COBERTURA Y CONTROL DE CONTRADICCIONES

## Estado
`SECOND_PASS_GP_2001 = COMPLETE_FOR_DOCUMENTARY_COVERAGE`

Esta segunda pasada compara la arquitectura acumulada del núcleo con la estructura completa de la
*Gramática popular del zapoteco del Istmo* (2001), incluidos sus capítulos 3–15, los seis textos
finales y el Apéndice para lingüistas.

Regla de precedencia:
- Las reglas `JLC-SP2-*` de esta sección **corrigen o precisan** cualquier formulación anterior incompatible.
- Una formulación anterior no se elimina para conservar historial, pero queda `SUPERSEDED` cuando así se indica.
- Las observaciones de la Gramática se mantienen separadas de análisis posteriores de otras fuentes.

## JLC-SP2-001 — propósito documental de la Gramática
Fuente: GP, Propósito.
La obra es una descripción de la estructura del diidxazá y declara explícitamente que no pretende
ser un método para aprender a hablarlo.
Uso:
- `SOURCE_FACT` y `TUTORIAL_TRANSFORMATION` deben almacenarse por separado.
- Una explicación didáctica creada por el tutor no debe atribuirse a la GP como si fuera formulación de la fuente.

## JLC-SP2-002 — tono lingüístico vs representación ortográfica
Corrige una ambigüedad de versiones anteriores.

Hechos compatibles:
1. El tono es lingüísticamente contrastivo y puede tener función léxica o gramatical.
2. La tradición ortográfica descrita en las fuentes del proyecto no exige representación tonal
   sistemática en toda escritura ordinaria.

Arquitectura:
- `phonological_tone`
- `orthographic_tone_mark`
- `tone_source`
- `tone_confidence`

Regla:
- No borrar marcas presentes antes del análisis.
- No inferir que la ausencia de tilde implica ausencia de tono.
- No añadir una marca tonal automáticamente sin evidencia normativa/contextual suficiente.

## JLC-SP2-003 — corrección de fuente del causativo
`SUPERSEDES` cualquier atribución del causativo a GP §7.2.

Fuente correcta:
- GP §7.1: significado/valencia del causativo.
- GP §7.4: variantes formales del causativo.

Regla documental:
- si la forma sencilla es intransitiva, la causativa se vuelve transitiva;
- si la forma sencilla es transitiva, la causativa admite dos complementos;
- `si-` es el marcador causativo más común y aparece después del marcador aspectual;
- GP documenta además causativos con `g-`, `z-`, `s-`, `ch-`, cambios de consonante inicial,
  dos prefijos causativos, dos formas causativas y verbos sin prefijo causativo.

## JLC-SP2-004 — perfecto: corrección semántica
`SUPERSEDES` la simplificación pedagógica anterior de “acción ya ocurrida con relevancia presente”.

Fuente: GP §7.2.4.
Regla:
- perfecto `hua-/huay-`;
- la GP lo describe como acción repetida a lo largo del tiempo;
- no se usa si la acción nunca se ha realizado antes;
- es común en contextos negativos para indicar que la acción no ocurre durante el intervalo indicado.

Ejemplos documentados:
- `Ma' huayeeda Betu chonna tiru` — Beto ya vino tres veces.
- `Ma' chonna gubidxa qué huayahua'` — No he comido por tres días.

Uso:
- No equiparar automáticamente PF con el perfecto del español o del inglés.
- La interpretación debe usar el intervalo temporal y la construcción completa.

## JLC-SP2-005 — progresivo ambulativo
Fuente: GP §7.2.3.
Además del progresivo ordinario, `cana-` expresa progresivo ambulativo: movimiento durante la acción.
Ejemplo:
- `canayubi` — anda buscando.
Uso:
- distinguir `PROGRESSIVE` de `AMBULATIVE_PROGRESSIVE`.

## JLC-SP2-006 — Juego 1C potencial: cautela de representación
`SUPERSEDES` la afirmación demasiado fuerte `Juego 1C potencial = Ø` como regla ejecutable universal.

La tabla de la GP presenta el ejemplo superficial `sa'` “camine” sin una segmentación de prefijo
transparentemente equivalente a los demás juegos.
Regla:
- almacenar la superficie paradigmática documentada;
- no generar un “prefijo cero” por simple analogía;
- requerir lema/clase y paradigma confirmado para análisis o generación.

Estado:
`DOCUMENTED_SURFACE / UNDERLYING_ANALYSIS_UNRESOLVED_IN_GP_CORE`

## JLC-SP2-007 — Juego 2 y vocal `u`: grado de certeza
Fuente: GP §7.3.
La GP observa que el Juego 2 presenta `u` en la mayoría de los aspectos y que la mayoría de sus
verbos son causativos; propone **como posibilidad** que `u` sea vocal temática vinculada al causativo.
Regla:
- en provenance GP: `HYPOTHESIS`, no `CERTAIN_RULE`;
- análisis posteriores (p. ej. Pérez Báez/Kaufman) deben registrarse como evidencia separada.

---

# COBERTURA RECUPERADA — CAPÍTULOS SUBREPRESENTADOS EN v0.25

## JLC-SP2-NP-001 — orden interno de la frase nominal
Fuente: GP §§4.4, 6.

Esquema documental general:
`{CANTIDAD | INTERROGACIÓN} + SUSTANTIVO + CALIFICACIÓN + POSESIÓN + DEMOSTRATIVO`

Reglas:
- calificativos, posesivos y demostrativos siguen al sustantivo;
- cantidad e interrogación lo preceden;
- una relativa puede integrarse en la frase nominal;
- el poseedor se coloca según la construcción posesiva correspondiente;
- existe aposición de nombre propio + frase nominal descriptiva;
- frases nominales pueden coordinarse con `ne` “y” y `pacaa` “o”.

Ejemplo complejo:
`xpi'cuhuiinilu' [ni bedanelu' neegue] que`
≈ “aquel pequeño perro tuyo que llevaste ayer”.

## JLC-SP2-PRON-001 — pronombres independientes
Fuente: GP §5.1.1.

Inventario documental:
- `naa` — 1SG
- `lii` — 2SG / usted
- `laa ~ laabe` — 3SG persona
- `laa ~ laame` — 3SG animal
- `laa ~ laani ~ ni` — 3SG cosa
- `laadu` — 1PL exclusivo
- `laanu` — 1PL inclusivo
- `laatu` — 2PL
- `laaca' ~ laacabe` — 3PL personas
- `laaca' ~ laacame` — 3PL animales
- `laaca' ~ laacani ~ cani` — 3PL cosas

Funciones documentadas:
- complemento directo;
- complemento indirecto;
- término de preposición;
- coordinación;
- respuesta;
- énfasis/foco del sujeto.

Regla:
pronombre independiente y marca dependiente de sujeto pueden coexistir en construcciones de énfasis.

## JLC-SP2-PRON-002 — reflexivo `laca`
Fuente: GP §5.6.
`laca` participa en reflexividad y en reiteración/enfasis de identidad del sujeto.
Ejemplos:
- `Gudiñe' laca naa` — me pegué a mí mismo.
- `Laca laabe bí'nibe ni` — él mismo lo hizo.
Regla:
no reducir `laca` a pronombre personal ni a simple intensificador sin analizar la construcción.

## JLC-SP2-PRON-003 — pronombres negativos
Fuente: GP §5.7.
- `guiruti'` — nadie
- `gasti'` — nada
Aparecen con negación oracional; la forma aspectual del verbo depende de la construcción.
No tratar la doble expresión negativa como redundancia errónea por analogía con español prescriptivo.

## JLC-SP2-ADJ-001 — calificativos
Fuente: GP §6.1.
Los calificativos:
- expresan propiedades como tamaño, color, textura, forma o calidad;
- siguen al sustantivo;
- son invariantes respecto a género y número del sustantivo.

## JLC-SP2-ADJ-002 — adjetivos verbales / estativos
Fuente: GP §6.2.
La mayoría de los adjetivos pueden funcionar también como verbos de estado con `na-`.
Ejemplos:
- `nahuiini'` — es chico.
- `nasoo` — es alto.
No insertar cópula española automáticamente.

## JLC-SP2-ADJ-003 — cantidad
Fuente: GP §6.3.
La categoría incluye:
- cardinales;
- ordinales;
- cantidades aproximadas.

Formas documentadas entre las aproximativas:
`guirá'`, `guidubi`, `caadxi`, `huaxié'`, `galaa`, `gasti'`, `stale`.
La repetición puede intensificar cantidad (`stale stale`).
`aronda'` “y medio” aparece después del sustantivo.

## JLC-SP2-DET-001 — artículos y demostrativos
Fuente: GP §§6.4–6.5.
- no hay equivalentes exactos y obligatorios de `el/la`;
- `ca` “ese” puede funcionar en contextos traducibles con artículo definido;
- `ti`, reducción de `tobi` “uno”, puede funcionar como artículo indefinido.
Regla:
no generar artículo por copia 1:1 desde español.

## JLC-SP2-ADJ-004 — posesivos
Fuente: GP §6.6.
`xti' + pronombre dependiente` puede funcionar como adjetivo/pronombre posesivo.
No concuerda con género ni número del objeto poseído.
Ejemplo:
`xtinne'` puede cubrir “mi/mis/mío/mía/míos/mías” según contexto.

## JLC-SP2-ADJ-005 — interrogativos nominales
Fuente: GP §6.7.
Antes del sustantivo:
- `xi` — cuál, inanimado;
- `tu` — cuál, persona/animal;
- `guná'` — cuál;
- `panda` — cuántos;
- `pabiá'` — cuánto, magnitud/tamaño.

## JLC-SP2-ADJ-006 — modificación de adjetivos
Fuente: GP §6.8.
`nabé` y `dunabé` pueden intensificar un calificativo con valor aproximado a “muy”.
No convertir “muy” en sustitución léxica universal: la construcción y el adjetivo importan.

---

# ADVERBIOS, PARTÍCULAS Y CONECTORES

## JLC-SP2-ADV-001 — categorías
Fuente: GP cap. 8.
La GP distingue adverbios de:
- tiempo;
- lugar;
- modo;
- negación;
- interrogación;
- introducción;
- además de adverbios/partículas dependientes.

## JLC-SP2-ADV-002 — tiempo y posición
Adverbios temporales pueden aparecer antes o después del predicado según la construcción.
Frases nominales también pueden funcionar adverbialmente como expresiones temporales.
Ejemplos documentados incluyen `ma'`, `neegue'`, `yanadxí`, `numbá'`, `yanna`, `nagá`, `huidxe`.

## JLC-SP2-ADV-003 — lugar
Fuente: GP §8.2.
- `rarí'` — aquí
- `racá` — allí
- `raricá'` — allá
- `raqué` — aquel lugar

## JLC-SP2-ADV-004 — interrogación
Fuente: GP §8.6.
Formas documentadas:
- `padxí` — cuándo
- `pora` — a qué hora
- `xiñee` — por qué
- `ximodo` — cómo
- `xidé` — de qué
- `pagala` — qué precio / cuánto cuesta

## JLC-SP2-PART-001 — partículas dependientes
Fuente: GP §8.5.
Partículas documentadas entre predicado y sujeto/huésped según construcción:
- `di'` — refuerzo negativo;
- `pe'` — énfasis/certeza/exactitud;
- `xa` — inverso/opuesto de la acción;
- `saa` — recíproco, exige sujeto plural;
- `si` — “tan pronto como”.
Regla:
no tratarlas como sufijos léxicos intercambiables; registrar alcance y posición.

## JLC-SP2-DISC-001 — adverbios de introducción
Fuente: GP §8.7.
- `sicarí'` — fórmula frecuente de apertura narrativa;
- `óraque / para` — entonces;
- `zacá / zaqué` — así;
- `raqueca` — allí mismo;
- `de raqué` — de allí;
- `nagá de ngue` — después de eso;
- `laaca` — también.
Uso:
son evidencia directa para cohesión textual y generación narrativa, no necesariamente para conversación neutra.

---

# PREPOSICIONES, CONJUNCIONES E INTERJECCIONES

## JLC-SP2-PREP-001 — sistema preposicional
Fuente: GP cap. 9.
La GP distingue:
1. usos relacionales de sustantivos de partes del cuerpo;
2. `runi` usado como preposición;
3. “preposiciones verdaderas”, incluidas formas de origen español.
Regla:
no proyectar inventario preposicional español ni asumir traducción 1:1.

## JLC-SP2-PREP-002 — ambigüedad de partes del cuerpo
Una base corporal puede ser:
- sustantivo poseído;
- término relacional/preposicional.
Resolver por estructura y complementación, no por forma aislada.

## JLC-SP2-CONJ-001 — coordinación
Fuente: GP caps. 4.4, 10, 14.1.
- `ne` = y;
- `pacaa` = o;
pueden coordinar frases y otras unidades según construcción.
La repetición de la conjunción es posible pero no obligatoria.

## JLC-SP2-INTJ-001 — interjecciones
Fuente: GP cap. 11.
El capítulo confirma una clase propia de interjecciones.
Estado:
`LEXICAL_INVENTORY_REQUIRED`.
No inventar análisis productivo hasta incorporar el inventario exacto del capítulo.

---

# ORACIÓN SIMPLE Y CAMBIOS DE ORDEN

## JLC-SP2-CLAUSE-001 — valencia básica
Fuente: GP §§12.1–12.3.
Mantener tipos estructurales separados:
- intransitiva;
- transitiva;
- transitiva con complemento indirecto.
La valencia del lema es requisito para análisis, causativización y generación.

## JLC-SP2-COP-001 — copulativas
Fuente: GP §12.4.
La GP documenta varias estrategias copulativas/predicativas; no reducir “ser/estar” a `nga`.
Las construcciones estativas, nominales y otras predicaciones deben conservarse como patrones distintos.

## JLC-SP2-WEATHER-001 — condiciones atmosféricas
Fuente: GP §12.5.
Las expresiones meteorológicas constituyen una clase de construcción propia.
No imponer sujeto expletivo español (“hace”, “hay”, “está”) como plantilla.

## JLC-SP2-ORDER-001 — énfasis
Fuente: GP §13.1.
El orden básico puede modificarse cuando un elemento se enfatiza/focaliza.
Regla:
orden superficial ≠ valencia; representar estructura informativa por separado.

## JLC-SP2-Q-001 — preguntas
Fuente: GP §13.2.
Distinguir preguntas polares y preguntas con palabra interrogativa.
No asumir que interrogación se reduce a entonación.

## JLC-SP2-NEG-001 — oración negativa
Fuente: GP §13.3 y §8.4.
La negación tiene construcciones propias y puede seleccionar/interactuar con aspecto.
No formar negativos mediante simple adición de una palabra equivalente a “no”.

---

# ORACIONES COMPLEJAS

## JLC-SP2-SUB-001 — preguntas indirectas
Fuente: GP §14.2.2.
La segunda pasada recupera este subtipo que estaba subrepresentado.
Debe almacenarse aparte de:
- pregunta directa;
- complemento declarativo;
- relativa;
- subordinada adverbial.

## JLC-SP2-SUB-002 — subordinación por relación
Fuente: GP §14.2.
Mantener relaciones semánticas explícitas antes de generar forma:
`COMPLEMENT`, `INDIRECT_QUESTION`, `TIME`, `PLACE`, `MANNER`, `PURPOSE`,
`CAUSE`, `CONCESSION`, `CONDITION`, `COMPARISON`.

## JLC-SP2-REL-001 — relativa dentro de frase nominal
Fuente: GP §14.3 y ejemplos del cap. 4.
La relativa es parte de la estructura de la frase nominal y puede combinarse con posesión,
adjetivación y demostración.
No analizar `ni` exclusivamente como pronombre independiente: puede participar en relativas según construcción.

---

# TEXTOS FINALES Y GÉNERO

## JLC-SP2-TEXT-001 — cobertura de los seis textos
La GP incluye:
1. `Chonna bi'chi'` — narración;
2. `Xtiidxa' ti binnigüé'` — narración;
3. `Diidxazá` — texto poético;
4. `Bacaanda'` — sueño/relato;
5. trabalenguas;
6. `Caldu Benda` — receta.

Regla:
`genre` es metadato obligatorio para reutilizar evidencia.

## JLC-SP2-RECIPE-001 — receta: evidencia concreta
La primera pasada era demasiado abstracta.
La receta documenta directamente:
- secuenciación con `Ora ma' ...`;
- potencial en instrucciones impersonales/procedimentales;
- acciones encadenadas;
- cantidades y tiempo de cocción;
- opción/condición con `zanda ... pa racala'dxi'`.

Ejemplos útiles:
- `Cui' bia' chonna litru nisa.` — se pone a hervir unos tres litros de agua.
- `Gáguini bia' quince minutu.` — debe cocerse unos quince minutos.
Uso:
corpus de procedimiento e instrucciones, no conversación neutra.

## JLC-SP2-TONGUE-001 — trabalenguas
Ratifica la decisión ya tomada:
- fonología;
- discriminación auditiva;
- pronunciación;
- benchmark ASR/audio;
- anti-sobrecorrección del corrector;
- pares mínimos/casi mínimos.
No usar:
- frecuencia;
- naturalidad conversacional;
- estilo neutral del generador.

---

# APÉNDICE PARA LINGÜISTAS — HUECO P0 RECUPERADO

## JLC-SP2-APP-001 — función del apéndice
Fuente: GP, Apéndice para lingüistas.
El apéndice ofrece tratamiento técnico de:
- consonantes;
- vocales;
- combinaciones fonéticas de palabras en frases y compuestos.

Prioridad:
`P0_CORRECTOR_AUDIO`.

Regla de arquitectura:
una forma superficial en habla/frase puede diferir de su forma aislada; por ello:
- no convertir automáticamente reducción fonética en nueva ortografía;
- conservar `citation_form`, `surface_form`, `phrase_context`;
- segmentación ortográfica, morfológica y fonológica deben ser capas distintas.

## JLC-SP2-APP-002 — hueco residual deliberado
La segunda pasada confirma que el apéndice debe explotarse como módulo técnico independiente
antes de automatizar todas las combinaciones fonéticas de frontera.
Estado:
`KNOWN_GAP / SOURCE_LOCATED / NOT_SAFE_FOR_AUTOCORRECTION_YET`.

Esto no es un hueco inadvertido: queda registrado explícitamente como pendiente de implementación.

---

# MATRIZ DE CIERRE DE COBERTURA

## JLC-SP2-CLOSE-001
Cobertura documental tras segunda pasada:

- Cap. 3 fonología/alfabeto: CUBIERTO; apéndice técnico pendiente de formalización exhaustiva.
- Cap. 4 sustantivos/frase nominal: CUBIERTO.
- Cap. 5 pronombres: CUBIERTO tras añadir independientes, reflexivo y negativos.
- Cap. 6 adjetivos/determinación/cantidad: CUBIERTO tras esta pasada.
- Cap. 7 verbos: CUBIERTO descriptivamente; perfecto y causativo corregidos; Juego 1C marcado con cautela.
- Cap. 8 adverbios/partículas: CUBIERTO descriptivamente; inventarios adicionales pueden ampliarse lexicalmente.
- Cap. 9 preposiciones: CUBIERTO arquitectónicamente; inventario léxico por completar.
- Cap. 10 conjunciones: CUBIERTO arquitectónicamente.
- Cap. 11 interjecciones: CAPÍTULO LOCALIZADO; inventario léxico exacto pendiente.
- Cap. 12 oración básica: CUBIERTO arquitectónicamente.
- Cap. 13 orden/pregunta/negación: CUBIERTO.
- Cap. 14 combinación de oraciones: CUBIERTO; preguntas indirectas añadidas.
- Cap. 15 textos: CUBIERTO por género; receta concretada.
- Apéndice: LOCALIZADO Y MARCADO P0; formalización técnica completa pendiente.

Interpretación de “cerrado”:
No significa que cada lexema y cada ejemplo del libro esté convertido a dato ejecutable.
Significa que ya no hay **secciones estructurales invisibles**: lo aún no formalizado está declarado
como pendiente conocido, con ubicación y función.

## JLC-SP2-CLOSE-002 — errores/contradicciones resueltos
1. Perfecto ≠ “resultado vigente ahora” por regla general.
2. Causativo pertenece a §7.1/§7.4, no §7.2.
3. Tono contrastivo y tono no marcado sistemáticamente en ortografía no son contradictorios.
4. Juego 1C potencial no debe operacionalizarse como “prefijo cero” sin paradigma.
5. Hipótesis de `u` en Juego 2 debe conservar el grado de certeza de la GP.
6. Género textual limita qué evidencia puede generalizarse.
7. Frase nominal/adjetivos/pronombres independientes/partículas ya no quedan fuera del core.
8. El apéndice técnico queda como pendiente explícito, no como omisión inadvertida.

## JLC-SP2-CLOSE-003 — criterio antes de volver a COR001
Puede volver a ejecutarse el benchmark sólo si:
- estas correcciones tienen precedencia sobre reglas anteriores;
- el analizador consulta frase nominal, persona independiente/dependiente, partículas, aspecto y discurso;
- `NO_ENCONTRADO` sigue significando falta de evidencia, no error;
- la salida mantiene provenance y grado de certeza.


---

# APÉNDICE PARA LINGÜISTAS — FORMALIZACIÓN TÉCNICA

## Estado
`GP_APPENDIX_TECHNICAL_EXTRACTION = COMPLETE`
`APPENDIX_DOCUMENTARY_GAP = CLOSED`
`APPENDIX_RUNTIME_IMPLEMENTATION = PENDING`

Fuente: Pickett, Black & Marcial Cerqueda, *Gramática popular del zapoteco del Istmo*,
Apéndice para lingüistas, pp. 123–125.

## JLC-APP-PHON-001 — inventario consonántico
La GP clasifica consonantes por modo, punto de articulación y oposición fuerte/débil.
Arquitectura mínima:
`phoneme_id`, `practical_orthography`, `phonetic_symbol_source`, `manner`, `place`,
`strength`, `voicing_tendency`, `source`.
La grafía práctica y la representación fonética son capas distintas.

## JLC-APP-PHON-002 — fuerte/débil
La GP documenta:
- fuertes `p, t, k(c/qu), ch`;
- débiles correlativas `b, d, g(g/gu), dx`;
- fricativas `s~z`, `xh~x`;
- oposición fuerte/débil también en nasales, laterales y vibrantes.
No reducir FORTIS/LENIS a simple sordo/sonoro.

## JLC-APP-PHON-003 — fuertes postónicas
Cuando una consonante fuerte sigue a sílaba tónica, puede realizarse más larga.
Ejemplos GP:
`chupa`, `gueta`, `saca` con realizaciones fonéticas prolongadas.
No duplicar consonantes en ortografía por esa duración.

## JLC-APP-PHON-004 — débiles
`b,d,g,dx` son generalmente sonoras; si se ensordecen, siguen siendo menos fuertes que sus
correlatas fuertes. `b,d,g` no presentan la fricativización intervocálica típica del español.
No imponer alofonía castellana al AUDIO_ENGINE.

## JLC-APP-PHON-005 — velarización de `n`
`n` ante `g/c` y al final de palabra puede realizarse velarmente.
Ejemplos: `nga`, `pan`.
No alterar la ortografía por esta realización.

## JLC-APP-VOW-001 — vocales
Inventario básico: `i e a o u`.
Separar:
`vowel_quality`, `vowel_type`, `tone`, `stress`.
Los tipos vocálicos siguen siendo sencilla, cortada y quebrada.

## JLC-APP-PROS-001 — acento principal
Cuando dos palabras forman una frase estrecha o compuesto, la sílaba tónica de la palabra
principal conserva los rasgos tónicos y las demás tónicas pueden volverse átonas.
Mantener:
`citation_form`, `orthographic_form`, `morphological_components`,
`phonological_phrase`, `primary_stress_host`, `phonetic_surface_form`.

## JLC-APP-PROS-002 — neutralización contextual
Las vocales cortadas/quebradas de formas aisladas pueden realizarse como sencillas cuando
pierden el acento principal.
Ejemplos:
`ba'du' + huiini' -> ba'duhuiini'`, pronunciación aproximada `baduhuiini'`.
`dxaapa' + huiini' -> dxaapahuiini'`, pronunciación aproximada `dxapahuiini'`.

Regla crítica:
`PHONETIC_NEUTRALIZATION != ORTHOGRAPHIC_DELETION`.

## JLC-APP-PROS-003 — posición media
Sílabas átonas en posición media de la emisión pueden perder acústicamente rasgos de
corte/quiebre. No inferir pérdida morfológica, error ortográfico ni nueva entrada léxica.

## JLC-APP-PROS-004 — no toda adyacencia neutraliza
La GP contrasta compuestos/frases estrechas con frases como:
`ba'du laadu`
`beeda ba'du'`
donde se conservan rasgos tónicos de las palabras.
El motor debe distinguir:
`LEXICAL_COMPOUND`, `TIGHT_PHONOLOGICAL_PHRASE`, `ORDINARY_SYNTACTIC_PHRASE`.
La GP no ofrece un algoritmo exhaustivo para clasificar toda secuencia nueva.

## JLC-APP-ORTH-001 — forma de cita vs superficie
La ortografía de referencia no debe derivarse directamente de pronunciación contextual.
Jerarquía:
1. forma ortográfica documentada;
2. análisis morfológico;
3. estructura prosódica;
4. realización fonética contextual.

## JLC-APP-ENGINE-001 — pipeline
Para audio/corrección:
1. preservar ortografía original;
2. recuperar forma de cita;
3. analizar morfología;
4. detectar compuesto/frase estrecha;
5. asignar acento principal;
6. permitir reglas fonéticas;
7. comparar con audio;
8. sólo entonces evaluar ortografía.

Prohibido:
`audio_surface -> spelling_correction`.

## JLC-APP-ENGINE-002 — impacto sobre `zeenda`
El Apéndice fortalece una regla metodológica, no confirma segmentación.
La continuidad/reducción acústica no prueba si `zeenda` es compuesto, palabra simple o frase estrecha.
Estado permanece: `SEGMENTATION_HYPOTHESIS`.

## JLC-APP-ENGINE-003 — trabalenguas
Deben probar:
A. `LEXICAL_CONTRAST`: diferencias fonológicas reales.
B. `CONTEXTUAL_ALLOPHONY`: variantes contextuales de una misma forma.
Evitar tanto colapsar contrastes como inventar errores ortográficos por reducción contextual.

## JLC-APP-TEST-001 — regresiones mínimas
- `chupa`: duración fuerte no produce *chuppa.
- `gueta`: [tt] no produce duplicación gráfica.
- `saca`: [kk] no produce duplicación gráfica.
- `nga`: velarización de `n` no cambia grafía.
- `pan`: `n` final velar no cambia grafía.
- `ba'duhuiini'`: reducción glotal acústica interna no autoriza borrar apóstrofo documentado.
- `dxaapahuiini'`: vocal sencilla contextual no autoriza reescribir forma de cita.
- `ba'du laadu` / `beeda ba'du'`: permitir conservación de prominencia en frase ordinaria.

## JLC-APP-CERTAINTY-001 — límites
Confirmado por GP:
inventario, fuerte/débil, duración postónica, comportamiento general de débiles,
velarización de `n`, neutralización prosódica y diferencia forma aislada/contextual.

No confirmado como algoritmo general:
detección automática de compuestos, clasificación exhaustiva de frases fonológicas,
reglas completas de tono en frontera, pronunciación contemporánea de todos los hablantes,
ortografía normativa moderna de toda variante.

Regla: abstenerse cuando la fuente no decide.
