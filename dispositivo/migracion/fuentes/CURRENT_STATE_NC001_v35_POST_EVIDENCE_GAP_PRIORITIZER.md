# CURRENT_STATE_NC001_v35_POST_EVIDENCE_GAP_PRIORITIZER

## Status

`PASS / EVIDENCE_GAP_PRIORITY_QUEUE_MATERIALIZED`

## Change

The v0.31 COR001 span-level graph is now triaged by `EvidenceGapPrioritizer_v0.34` without resolving any gap from COR001 itself.

Preserved graph counts:

- 107 graphs;
- 141 unresolved nodes / 109 unique unresolved surfaces;
- 61 ambiguity nodes / 32 unique ambiguity surfaces.

New actionable distinction:

- exact canonical lexical evidence already exists for `zanda` (Pickett) and `stobi` (Pickett), so these are integration gaps rather than missing-evidence gaps;
- 11 additional unresolved surfaces have exact canonical example-attestation evidence that requires review but cannot be promoted automatically to lexeme identity;
- `ra` is the highest-impact homography because it blocks Morphology I contextual promotion;
- recurrence and orthographic-neighbor recall are triage signals only.

## Preserved invariants

- COR001 = `ANALYSIS_TARGET_ONLY`
- no COR001 Spanish for analysis or disambiguation
- `PRIORITY_SCORE != CONFIDENCE`
- `RECURRENCE != EVIDENCE`
- `EXACT_EXAMPLE_NGRAM != LEXEME_IDENTITY`
- `ORTHOGRAPHIC_NEIGHBOR != EQUIVALENCE`
- ambiguity remains unresolved until independent evidence adjudicates it
- no correction, rule discovery, full parse or generation license from the graph/queue
- `ANALYZED != GENERATION_LICENSED`

## Regression

`238 tests + 9 subtests PASS`

## Next milestone

`INTEGRATE_EXISTING_EXACT_DOCUMENTARY_GAPS_v0`, beginning with exact Pickett lexical evidence for `zanda` and `stobi`.
