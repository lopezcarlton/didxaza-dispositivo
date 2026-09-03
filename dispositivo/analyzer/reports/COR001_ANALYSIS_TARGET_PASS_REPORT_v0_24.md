# COR001 analysis-target pass v0.24

## Result

`PASS / ANALYSIS_TARGET_OBSERVATION_COMPLETED`

This is **not** an accuracy evaluation. COR001 remains `ANALYSIS_TARGET_ONLY` and its supplied didxazá strings remain `SUPPLIED_DRAFT_TRANSCRIPTION / NOT_CANONICAL_PENDING_REVIEW`.

## Input

- 107 COR001 items.
- Exact 1:1 audio/workbook manifest from v0.23.
- The supplied draft didxazá string of each item was submitted unchanged to the current NC001 analyzer modules.
- Audio was not used to repair, normalize or reinterpret the supplied string in this pass.

## Analyzer stack exercised

The pass routed each surface through the currently materialized non-licensing exact analyzers:

1. C01/C02 round-trip bridge using the current v0.10 evidence/slot set and v0.9 orthographic resolutions.
2. C03 final-`lá` polar bridge.
3. C05 XTI possession bridge.
4. C05 inherently-possessed NP bridge.
5. C05 XH/X NP bridge.
6. Four exact typed C05 morphophonology bridges (`bere→xpere`, `doo→xtoo`, `gueta→xqueta`, `dxiiña'→xhiiña'`).

All preserve `generation_license_assertion=false`.

## Observation result

- `107 / 107`: `ABSTAIN_ALL_CURRENT_NC001_ANALYZERS`
- `0`: current construction recognitions on COR001 draft surfaces.
- No rule, license, orthographic resolution or construction was created from COR001.

These counts are **coverage observations, not correctness scores**. They do not mean that 107 COR001 items are wrong or that the analyzer made 107 errors.

## Harness calibration

To rule out a broken routing harness, the same analyzer instances were tested on the 12 currently licensed control surfaces. All 12 were recognized by the expected module:

- C01: `Ma' beedabe`, `Ma' gusé'`, `Ma' bidxiiché'`
- C02: `Qué rasé'`
- C03: `reedabe lá`
- C05: `bi'cu' xtibe`, `lidxi Ana`, `xhamigu Juana`, `xpere Juana`, `xtoo Juana`, `xqueta Juana`, `xhiiña' Juana`

Therefore the all-abstain COR001 result is not attributable to a dead analyzer harness.

## What the result demonstrates

The current NC001 "analyzer stack" is still a set of **narrow exact construction bridges**, materialized primarily to enforce round-trip and licensing safety around the generator. It is not yet a general-purpose analyzer orchestrator for arbitrary didxazá utterances.

COR001 exposes this architectural coverage gap without being used to discover how any unrecognized COR001 form should be analyzed.

The canonical v0.2.15.3 runtime already exposes reusable retrieval, morphology, evidence-adjudication and qualification components, but the project previously verified that it does not expose a single general analyzer entrypoint/orchestrator. The next engineering target should therefore be an analysis-only orchestrator that reuses those existing components and remains non-licensing.

## What this pass does NOT justify

This pass does not justify:

- adding a construction because it appears in COR001;
- changing spelling from a COR001 draft transcription;
- learning a morphology or lexical rule from COR001;
- measuring analyzer accuracy against the supplied Spanish or didxazá;
- promoting COR001 into DEVELOPMENT_NC001;
- treating an abstention as evidence that a COR001 form is invalid.

## Artifacts

- `COR001AnalysisObservations_v0_24.jsonl` — item-level observation ledger.
- `COR001AnalysisObservationSummary_v0_24.json` — aggregate coverage observations.
- `COR001AnalysisHarnessCalibration_v0_24.json` — independent calibration on the 12 licensed control surfaces.
- `run_cor001_analysis_target_pass_v0_24.py` — reproducible analysis-target runner.

## Next target

`MATERIALIZE_NON_LICENSING_ANALYZER_ORCHESTRATOR_v0`

Requirements:

1. Reuse canonical runtime v0.2.15.3 components; do not discover rules from COR001.
2. Preserve exact form, diacritics and apostrophes before analysis.
3. Route existing C01/C02/C03/C05 bridges as specialized analyzers.
4. Add analysis-only lexical/morphological observations only where already supported independently by canonical runtime/source evidence.
5. `ANALYZED != GENERATION_LICENSED` remains invariant.
6. Rerun COR001 strictly as `ANALYSIS_TARGET_ONLY`; changes in coverage are observations, never an optimization score.
