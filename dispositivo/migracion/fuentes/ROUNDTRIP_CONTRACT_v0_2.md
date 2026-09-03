# ROUNDTRIP_CONTRACT_v0_2

## Status

`STABILIZED_NARROW_CONTRACT`

This contract does not create a general didxazá analyzer and does not license generation by itself.

Canonical dependency remains:

`GENERATOR_RUNTIME_DEPENDENCY = MATERIALIZED_INPUTS_WITH_VERIFIED_CANONICAL_ADAPTER`

Round-trip mode:

`COMPOSED_CANONICAL_RUNTIME_WITH_EXISTING_NC001_SCHEMAS`

Analysis semantics:

`STRUCTURAL_COMPATIBILITY_ONLY_NON_LICENSING`

## Required round-trip output for novel generation

A novel GenerationLicense can pass the round-trip gate only when the injected analyzer returns:

- `analysis_status = ANALYZED`
- `roundtrip_contract_version = 0.2`
- `analysis_semantics = STRUCTURAL_COMPATIBILITY_ONLY_NON_LICENSING`
- `generation_license_assertion = false`
- exact compatible `construction_id`
- exact compatible `candidate_id`
- exact compatible `cell_id`
- exact compatible `tam`
- exact compatible `person`
- exact compatible `target_scope`
- exact compatible `recognized_slots`
- compatible predicate-valence subtype when the independent construction evidence carries a `predicate_valence_scope`.

No whole-surface attestation is required for novelty.

## Independence

The bridge does not read GenerationLicense or novelty-attempt files. It uses only:

- `ConstructionInventory_v1`
- `ParadigmTable_v1`
- `AuthorizedSlotFillers_v0_1`
- material evidence atoms
- verified runtime v0.2.15.3
- verified SQLite v2.20.

The canonical SQLite table `verb_lexeme_class_v023` is reused read-only for `analysis_codes_raw`. No valence relation is inferred from surface.

For the currently licensed C01 construction evidence, the already-existing documentary analysis is explicitly scoped to an **intransitive assertion**. The v0.2 evidence file merely structures that already-present restriction as:

`predicate_valence_scope = [INTRANSITIVE]`

This is not a new linguistic claim.

## Critical separation

`ANALYZED != GENERATION_LICENSED`

The bridge may structurally recognize a combination that the generator must still refuse.

Examples in the stabilization probes:

- `Ma' benda'` -> structurally analyzed; positive attested control.
- `Ma' beedabe` -> structurally analyzed and still licensed by the existing first novel GenerationLicense.
- `Ma' güé` -> structurally analyzed, but not generation-licensed. Its canonical lexeme subtype is incompatible with the current intransitive C01 construction evidence.
- `Ma' bídxaagabé` -> structurally analyzed, but not generation-licensed; the paradigm cell additionally carries an explicit pending-valency blocker.

## Exactness

The bridge remains exact-only. It abstains rather than normalize or near-match:

- `ma' beedabe`
- `Ma' beedabé`
- `Ma'  beedabe`
- `Ma' reedabe`
- bare `beedabe`.

No tone stripping, `SequenceMatcher`, PDLMA->surface, paradigm completion, or COR001 path is allowed.
