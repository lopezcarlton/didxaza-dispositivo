# DevelopmentCorpusProtocol_v0_35

This version **extends v0_22 additively**. All v0_22 evidence/lifecycle/holdout rules remain in force.

## Non-lossy acquisition hierarchy

When available, preserve:

```text
continuous_audio
  -> speaker_turn
     -> optional intonation_unit annotations
        -> transcription/analysis layers
```

Neither `turn` nor `intonation_unit` annotation is required for an utterance to remain valid development evidence. Missing discourse/prosodic annotation is `NOT_ANNOTATED`, never rejection.

## Elicitation-method provenance

Each record may label one acquisition method:

- `SPONTANEOUS_CONVERSATION`
- `NATURALISTIC_TASK`
- `NONLINGUISTIC_TRIGGER`
- `STRUCTURED_GAME`
- `MEANING_CONTEXT_PROMPT`
- `TRANSLATION_ELICITATION`
- `SPEAKER_JUDGMENT`
- `OTHER_DOCUMENTED_METHOD`

Method labels describe provenance; they do not create a confidence score or automatic ranking.

## Audio-first preference, not evidence erasure

Independent development acquisition should prefer spontaneous/naturalistic/nonlinguistic elicitation when the goal is natural discourse. Translation elicitation remains a separately labeled evidence type when deliberately used; it must never be relabeled as spontaneous speech.

## Optional discourse metadata

The following fields are allowed but never required for local Analyzer operation or evidence acceptance:

- `conversation_id`
- `turn_id`
- `previous_turn_ids`
- `interaction_context_ref`
- `intonation_units[]`
- `discourse_annotation_status`
- `prosodic_segmentation_status`

Potential later annotations such as topic, focus, co-reference, accessibility or episode boundary must be stored as downstream analysis, never as raw speaker evidence.

## Context firewall

```text
MISSING_CONTEXT != INVALID_UTTERANCE
MISSING_CONTEXT != ANALYZER_BLOCK
CONTEXT_ANNOTATION != SPEAKER_ATTESTATION
```

A single isolated utterance remains a legitimate analysis target and development-corpus record.

## Raw-layer preservation

- never overwrite continuous audio with segmented clips;
- never overwrite raw transcription with a normalized/adjudicated surface;
- never overwrite speaker judgment with project analysis;
- never infer missing discourse context and store it as observed evidence.

## Holdout

All v0_22 holdout seals remain unchanged.
