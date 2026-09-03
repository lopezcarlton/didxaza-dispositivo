# FB-062 — competing analyses after owner review

**Observed COR001 transcription:** `zenda de ra ñaa`  
**Spanish prompt:** “Vengo de la milpa.”

## Stable evidence

- `ra ñaa` is supported as “milpa/parcela”; therefore the earlier idea that the failure arose because the system was literally searching for Spanish *milpa* is rejected.
- Dictionaria entry `eeda` means “venir”. Its stored paradigm gives Future `z.eeda*; ~ z.ee*da*`.
- Dictionaria contains an independent entry `nda'` tagged as a **particle**, described as a particle that tends to precede or follow a verb for pragmatic functions such as emphasis.

## H1 — inflected form of `eeda` “venir”

`zenda` may be an imperfect transcription/perception of a form related to the documented future/allomorphic forms of `eeda` (`zeeda`, PDLMA `z.eeda* ~ z.ee*da*`).

**Support:** semantic match “venir” + documented paradigm.  
**Problem:** the Spanish prompt is present first person “vengo”; the system has not established the TAM/person of the recorded didxazá form, and the observed spelling does not directly equal the documented form.

## H2 — `zee + nda'`

The project owner proposes that the recording may contain two units perceived/transcribed together: `zee` + pragmatic `nda'`.

**Support:** `nda'` is independently documented as a pragmatic particle capable of occurring around verbs.  
**Problem:** in the current Dictionaria snapshot, standalone `zee` is **not** the verb “venir”: one `zee` entry is a noun “elote” and another is a verb related to scattering/irrigating. Therefore the `zee` portion of H2 is not yet source-supported as “come”.

## Engine decision

**Status:** `COMPETING_SEGMENTATION_HYPOTHESES`.

The engine must not silently choose H1 or H2. It should surface both, state what evidence supports each component, and request targeted review of the audio/segmentation. This is a model case for future acoustic + morphological adjudication.
