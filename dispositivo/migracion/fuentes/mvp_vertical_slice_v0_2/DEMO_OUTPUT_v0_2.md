# Demo de salida — MVP_LINGUISTICO_001 vertical slice v0.2

## FB-076

**Entrada:** `zanda guiniu' ni stobi cha hui ga' la`  
**Intención:** ¿Puedes repetirlo más despacio?

**Estado nuevo:** `OWNER_SUPPORTED_REVIEW_CANDIDATE`.

**Candidato preferido para revisión:** `chaahui'` = “despacio”.

**Qué cambió:** el responsable del proyecto considera `chaahui'` un buen candidato después de revisar la evidencia. El motor puede subir su prioridad en la cola de revisión, pero **no lo convierte todavía en corrección automática ni en validación de hablante nativo**.

---

## FB-079

**Entrada:** `pagala zaca ni'`  
**Intención:** ¿Cuánto cuesta?

**Estado nuevo:** `PROBABLE_TRANSCRIPTION_CORRECTION`.

**Candidato preferido:** `Pàgàla sacani.`

**Evidencia convergente:**

1. Dictionaria contiene el ejemplo exacto `Pàgàla sacani.` = “¿Cuánto cuesta (la cosa)?”.
2. Pickett aporta evidencia histórica para el dominio de precio (`pagaḻa`, `saca`).
3. Al volver a escuchar el audio, el responsable del proyecto percibe la consonante más como **s** que como **z**.

**Hipótesis acústica:** la prominencia percibida al final podría relacionarse con la prosodia tonal y no con el acento español. Se conserva como hipótesis; **no se codifica todavía un tono concreto para la `i`**, porque el ejemplo ortográfico disponible `sacani` no lo marca.

**Acción del motor:** rankear `sacani` muy por encima de `zaca ni'` para revisión y proponer una corrección de transcripción, pero sin `AUTO_CORRECT`.

---

## FB-062

**Entrada:** `zenda de ra ñaa`  
**Intención:** Vengo de la milpa.

**Estado nuevo:** `COMPETING_SEGMENTATION_HYPOTHESES`.

**Hechos ya estables:** `ra ñaa` = milpa/parcela; `eeda` = venir; Dictionaria documenta una partícula pragmática independiente `nda'`.

**H1:** `zenda` corresponde de algún modo a una forma flexionada de `eeda`; Dictionaria ofrece futuro `z.eeda ~ z.ee*da`.

**H2 (propuesta del responsable del proyecto):** la grabación podría segmentarse `zee + nda'`.

**Precaución:** el `nda'` de H2 sí está documentado como partícula, pero el `zee` independiente del snapshot actual de Dictionaria no significa “venir”. Por tanto H2 es lingüísticamente interesante pero todavía no puede darse por demostrada.

**Acción del motor:** mostrar ambas hipótesis, no autocorregir, y dirigir la siguiente revisión al audio y al análisis morfológico.
