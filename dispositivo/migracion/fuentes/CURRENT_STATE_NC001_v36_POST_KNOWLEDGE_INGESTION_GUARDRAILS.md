# CURRENT_STATE_NC001_v36_POST_KNOWLEDGE_INGESTION_GUARDRAILS

## Status

`PASS / ADDITIVE_GUARDRAILS_MATERIALIZED`

## Active route

The COR001 evidence-gap queue remains preserved but is **not the active work route**.

```text
COR001 = ANALYSIS_TARGET_ONLY
COR001_GAP_QUEUE = FROZEN_PENDING_LATER_INTEGRATION
ACTIVE_LINGUISTIC_ROUTE = LITERATURE_STUDY + INDEPENDENT_JUCHITAN_DEVELOPMENT_AUDIO
```

No `zanda`, `stobi`, `ra`, or other COR001 gap was resolved in v0.35.

## New hardening

- missing context can never block locally supportable Analyzer work;
- context is optional refinement only;
- unresolved context-sensitive interpretation is not an error;
- new knowledge layers must preserve prior local capability unless independent evidence invalidates the prior analysis;
- Analyzer/Tutor/Generator/Corrector use asymmetric decision thresholds;
- tendencies/frequencies/attestations/hypotheses/project derivations remain epistemically distinct;
- no single source or genre becomes an implicit global grammar;
- optional discourse/prosodic corpus metadata is additive and non-blocking;
- raw audio, transcription, speaker confirmation, linguistic analysis and orthographic adjudication remain distinct layers.

## Analyzer interface

`non_licensing_analyzer_orchestrator_v0_35.py` versions the v0.26 interface with an optional `context_segments` channel.

In v0.35:

- local analysis is performed exactly from the supplied surface and existing local evidence channels;
- optional context is recorded only as channel metadata;
- context cannot change local lexical/morphological evidence;
- no discourse rule has been implemented from BH2019 yet.

## Development corpus

`DevelopmentCorpusProtocol_v0_35` and `UtteranceRecordTemplate_v0_35.json` add optional provenance/context/prosody fields while preserving v0.22 acceptance rules.

An isolated utterance remains valid development evidence and a valid Analyzer target.

## Literature

BH2019 reading is in progress. Current stopping point: Chapter 5, before detailed §5.2 chiastic conversational structures.

No partial-reading observation is automatically promoted to generation or correction.

## Next work

1. Continue BH2019 at §5.2, then Chapter 6.
2. Classify source claims before executable adoption.
3. Begin independent Juchitán development-audio acquisition using the additive v0.35 protocol.
4. Use new independent evidence later to test/refine the graph and device.
