# ANALYSIS_CAPABILITY_GUARDRAILS_v0_35

## Purpose

Prevent newly ingested linguistic specificity from becoming a blocking dependency or from silently narrowing existing capabilities.

This is a hardening contract. It does **not** license any new linguistic rule, correction, generation pattern, or orthographic decision.

## 1. Graceful degradation

```text
ISOLATED_SENTENCE -> LOCAL_ANALYSIS_ALWAYS_ATTEMPTED
OPTIONAL_CONTEXT  -> MAY_REFINE_CONTEXT_SENSITIVE_CLAIMS
MISSING_CONTEXT   -> NEVER_BLOCKS_LOCAL_ANALYSIS
```

The Analyzer must return every locally supportable result from an isolated surface. If a discourse-sensitive conclusion cannot be resolved locally, only that conclusion remains unresolved.

Forbidden behavior:

```text
NO_CONTEXT -> ABSTAIN_FROM_ENTIRE_ANALYSIS
```

unless there is independently no local component evidence at all.

## 2. Monotonic capability

Adding a new optional evidence layer must not remove a previously supportable local analysis merely because that layer is absent.

```text
NEW_LAYER_ABSENT -> OLD_LOCAL_CAPABILITY_PRESERVED
```

A prior analysis may be withdrawn only when independent evidence demonstrates that the prior analysis itself was wrong, and that change must be provenance-bearing and regression-tested.

## 3. Local vs context-sensitive claims

Every conclusion that can depend on discourse context must be representable as one of:

- `LOCALLY_RESOLVED`
- `LOCALLY_COMPATIBLE_NOT_CONTEXTUALLY_RESOLVED`
- `MULTIPLE_LOCAL_HYPOTHESES`
- `CONTEXT_REFINED`
- `UNRESOLVED_FROM_AVAILABLE_EVIDENCE`

`UNRESOLVED` is not `INCORRECT`.

Context may refine:

- co-reference;
- topic/focus interpretation;
- discourse accessibility;
- participant tracking;
- discourse-naturalness diagnostics.

Context must not be required for basic lexical/morphological/local syntactic analysis when those channels have independent evidence.

## 4. Decision asymmetry

The same evidence does not authorize the same action in every product capability.

```text
ANALYZER  = broad / hypothesis-preserving / tolerant
TUTOR     = explanatory / uncertainty-visible
GENERATOR = conservative / only licensed realizations
CORRECTOR = most conservative / correction requires strongest admissible evidence
```

Consequences:

- an Analyzer hypothesis is never automatically a correction;
- an attested tendency is never automatically a generator rule;
- a Tutor explanation may describe alternatives without selecting one;
- lack of contextual naturalness evidence is never itself an orthographic error.

## 5. No frequency-to-rule promotion

```text
RECURRENT != REQUIRED
RARE != INVALID
FREQUENCY != GRAMMATICALITY
```

Corpus frequencies can guide review or pedagogy, but cannot create categorical constraints without independent evidence.

## 6. No source overfit

No single work, author, genre, elicitation method, speaker, or corpus may become an implicit global grammar.

All source-derived claims retain:

- source id;
- evidence method when known;
- community/dialect scope when known;
- genre/register when known;
- claim type;
- stated strength/limitations.

## 7. No context fabrication

When context is absent, the system must not invent a previous turn, discourse topic, speaker intention, referent chain, or focus structure in order to force one analysis.

## 8. No combinatorial obligation

A linguistically describable feature does not become a mandatory runtime field merely because it exists.

Only fields needed for a concrete decision should be required. New discourse/prosody fields are optional and default to `NOT_ANNOTATED` / `UNKNOWN`, not failure.

## 9. Preservation of raw evidence

Any enrichment layer must remain separable from raw evidence:

```text
AUDIO != TRANSCRIPTION != MORPHOLOGICAL_ANALYSIS != DISCOURSE_ANALYSIS != ORTHOGRAPHIC_ADJUDICATION
```

No downstream interpretation may overwrite an upstream evidence layer.

## 10. COR001 firewall

These guardrails do not change COR001:

```text
COR001 = ANALYSIS_TARGET_ONLY
COR001_FOR_RULE_DISCOVERY = PROHIBITED
COR001_FOR_CONTEXTUAL_RULE_DISCOVERY = PROHIBITED
```
