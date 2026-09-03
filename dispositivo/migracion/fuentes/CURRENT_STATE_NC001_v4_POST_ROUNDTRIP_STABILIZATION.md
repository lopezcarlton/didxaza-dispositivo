# CURRENT_STATE_NC001_v4_POST_ROUNDTRIP_STABILIZATION

## Governing state

- Architecture v1.1: FROZEN, unchanged.
- Canonical predecessor: runtime v0.2.15.3.
- Runtime/SQLite canonical SHA-256: exact-match gate remains required.
- MVP_LINGUISTICO_001 v0.1/v0.2: historical read-only antecedents; no legacy similarity path reused.
- COR001: `ANALYSIS_TARGET_ONLY`.

## Generator

`Generator_v0.2 = ROUNDTRIP_CONTRACT_STABILIZED`

Dependency remains:

`GENERATOR_RUNTIME_DEPENDENCY = MATERIALIZED_INPUTS_WITH_VERIFIED_CANONICAL_ADAPTER`

This is still not a general runtime-wired generator or a general analyzer.

## Round-trip contract

`ROUNDTRIP_CONTRACT_VERSION = 0.2`

`ROUNDTRIP_ANALYSIS_SEMANTICS = STRUCTURAL_COMPATIBILITY_ONLY_NON_LICENSING`

The bridge may analyze surfaces that are not generation-licensed. Generation always requires an independent persisted GenerationLicense plus all existing provenance/orthography/scope gates.

Novel round-trip now matches exact construction, candidate, cell, TAM, person, Juchitán scope, recognized slots, and construction-required predicate-valence subtype.

## Novel generation state

Only one active novel license exists:

`GL-NC001-C01-V01-C3SG-ALREADY-NOVEL-001`

surface: `Ma' beedabe`

status: `LICENSED_NOVEL_RECOMBINATION`

surface origin: `PROJECT_GENERATED`

whole-surface evidence: `NULL`

No second novel license was attempted or added in this checkpoint.

## Key stabilization finding

The first C01 independent construction evidence is scoped to a temporal-adverb + completive **intransitive assertion**.

The canonical SQLite already preserves Dictionaria/PBK analysis-code subtypes in `verb_lexeme_class_v023`.

- `eeda` carries `vA:i` and satisfies the intransitive construction scope.
- `e7` carries `vC:t`; therefore structural recognition of `Ma' güé` does not license its generation under the current intransitive C01 construction evidence.

This closes the main overgeneralization risk discovered after the first novel license.

## Construction blockers unchanged

- C03: `MISSING_QUESTION_PATTERN`
- C04: `INTERROGATIVE_DOMAIN_SCOPE_MISMATCH`
- C05: `MISSING_NOUN_POSSESSION_LICENSE_SET`
- C06: `DEPENDENT_POTENTIAL_OUT_OF_SCOPE`

No TIME added to C04. No POTENTIAL expansion.

## Safety invariants

- no paradigm inference;
- no self-licensing;
- no whole-surface/evidence laundering;
- no near-match or similarity generation;
- no tone stripping for generation decisions;
- no PDLMA->surface generation;
- exact orthographic gates remain mandatory;
- ANALYZED does not imply GENERATION_LICENSED;
- transitivity/valence is not inferred from surface;
- canonical bytes remain immutable.

## Next hito

Start in a new chat from this checkpoint.

Do **not** mass-generate.

Next objective: find exactly one candidate for a second novel recombination whose predicate-frame compatibility is independently licensed. Prefer reuse of current runtime/SQLite and current 12-verb slice. If no compatible predicate/frame evidence exists, abstain and materialize only the missing evidence layer; do not infer valence or expand TAM/constructions.
