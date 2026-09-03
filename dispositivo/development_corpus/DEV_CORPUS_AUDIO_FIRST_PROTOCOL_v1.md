# DEV_CORPUS_AUDIO_FIRST_PROTOCOL_v1

## Status

`READY_FOR_EXTERNAL_ACQUISITION`

No development utterance has been created or claimed by this artifact. Real didxazá evidence begins only when a Juchitán speaker produces recorded speech.

## Scope

```text
ROLE = DEVELOPMENT_EVIDENCE
COMMUNITY = JUCHITAN (documented per speaker/session)
MODE = AUDIO_FIRST
TARGET_SIZE = 120..180 utterances
PREFERRED_UNIT = conversational microinteraction
HOLDOUT_RELATION = STRICTLY_SEPARATE
```

## Acquisition principle

Prompts describe **situations, intentions and tasks**, not target didxazá strings. Spanish may be used to explain the situation, but the speaker is asked to respond naturally in didxazá rather than translate a prepared sentence word-for-word.

Do not:
- show candidate spellings before recording;
- ask a speaker to repeat a project-generated didxazá form;
- force a selected verb, TAM, person or construction if the speaker chooses another expression;
- repair an utterance during recording to fill a paradigm cell;
- discard complete conversational units merely because they did not contain a desired form.

## Coverage goals, not quotas

Seek natural evidence across:
- C01–C06 when they arise naturally;
- 1SG / 2SG / 3SG_HUMAN;
- HABITUAL / COMPLETIVE;
- the 12 selected lexical targets as **coverage interests**, not mandatory wording.

C06 is especially important for analysis/tutoring, but its dependent POTENTIAL remains outside free generation.

## Recording sequence

1. Assign `session_id`, speaker IDs and prompt IDs before recording.
2. Record master audio continuously for each conversational unit when practical.
3. Preserve raw audio; do not edit linguistic content in the master.
4. After recording, segment utterances by listening.
5. Produce rough transcription preserving observed marks and uncertainty.
6. Ask speaker to confirm intended meaning/naturalness **without showing system suggestions**.
7. If the speaker offers an alternative spontaneously, store it as a separate speaker-attested record linked to the original.
8. Only then run project analysis on a development copy.

## Evidence classes

```text
RAW_AUDIO_MASTER
SPEAKER_PRODUCED
ROUGH_TRANSCRIPTION
SPEAKER_CONFIRMED_MEANING
SPEAKER_NATURALNESS_JUDGMENT
SPEAKER_ATTESTATION
PROJECT_ANALYSIS_DERIVED
```

`PROJECT_ANALYSIS_DERIVED` can never be promoted to source evidence.

## Minimal metadata — session/unit

- `dev_corpus_id`
- `conversation_unit_id`
- `recording_session_id`
- `speaker_ids[]`
- `speaker_roles[]`
- `community`
- `community_evidence_note`
- `acquisition_date`
- `prompt_id`
- `interaction_type`
- `register`
- `recording_file_ids[]`
- `consent_or_rights_ref`
- `notes_nonlinguistic`

## Minimal metadata — utterance

- `utterance_id`
- `conversation_unit_id`
- `speaker_id`
- `start_time`
- `end_time`
- `rough_transcription`
- `transcription_uncertainty`
- `speaker_confirmed_meaning_es`
- `speaker_naturalness_judgment`
- `spontaneous_alternative`
- `audio_ref`
- `source_status = DEVELOPMENT_EVIDENCE`

## Frequency

Before acquisition, selected verbs have `HIGH_FREQUENCY = NOT_MEASURED`. After a sufficiently documented development corpus exists, observed counts may be reported as **development-corpus frequencies**, never as population frequency without a separate sampling design.

## Separation from HOLDOUT_CONVERSATIONAL_001

Development prompts and recordings must use different IDs/directories from holdout material. No holdout conversation unit may be copied into this corpus, ValidationQueue, paradigm evidence, prompt examples or internal tests.

## Entry into linguistic inventories

A development utterance may update an inventory only through a new `SPEAKER_ATTESTATION` record that retains:
- exact audio link;
- exact observed/transcribed surface;
- speaker/community provenance;
- analyst interpretation separately;
- date and reviewer.

No surface is licensed merely because the analyzer can derive it.
