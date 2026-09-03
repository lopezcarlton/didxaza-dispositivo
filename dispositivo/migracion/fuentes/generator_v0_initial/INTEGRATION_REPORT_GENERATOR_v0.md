# Generator_v0 — integration report

## Status

`IMPLEMENTED_CONSERVATIVE_SCAFFOLD / NO_CANONICAL_RUNTIME_MODIFICATION`

Canonical v0.2.15.3 runtime and SQLite remain byte-unchanged. `Generator_v0` is a separate slice package.

## Integrity gate

Registered canonical hashes:

- runtime ZIP: `6e5c3e8ee9bb5dbd04666537dc423724eb4bc402440e670e5be81cfa54b5d7e5`
- SQLite: `2379773426baf4e3eace87c61ec17f7a1e1b9164421e56cf736d35eb64a5ebed`

Both matched exactly before integration work.

MVP v0.1/v0.2 have no previously registered canonical package hash in mounted records; they were inspected read-only and their observed hashes are recorded in `MVP_REUSE_MAP_v1.md`.

## Generator policy

`Generator_v0` has no free morphology and no near-match path. A positive output requires:

1. exact request signature;
2. materialized construction;
3. direct `ATTESTED` paradigm cell with `evidence_id`;
4. `JUCHITAN_EXPLICIT` cell scope;
5. `SOURCE_EXACT_RENDERING` orthography;
6. source/speaker attestation origin;
7. a license whose assembled surface equals an independently attested whole surface exactly.

Thus the initial licenses demonstrate the assembly machinery without claiming novel productive generation.

## Positive licenses in v0

- C01: `Ma'` + `benda'` -> `Ma' benda'` (`GP §8.1, ej. 97a`).
- C02: `Qué` + `reedabe` + `guirá' dxi` -> `Qué reedabe guirá' dxi` (`GP §8.4, ej. 104a`).

Both are `ZERO_NOVELTY_ATTESTED_ASSEMBLY`. `may_license_new_combinations=false`.

## Blocking findings

- C03: direct polar pattern absent -> `MISSING_QUESTION_PATTERN`.
- C04: scope/inventory inconsistency: inventory uses `Padxí`/WHEN but frozen scope does not list TIME among authorized content-question subdomains -> `INTERROGATIVE_DOMAIN_SCOPE_MISMATCH`.
- C05: licensed noun/possessor set absent -> `MISSING_NOUN_POSSESSION_LICENSE_SET`.
- C06: POTENTIAL complement outside NC001 -> `DEPENDENT_POTENTIAL_OUT_OF_SCOPE`.

No frozen scope was silently changed.

## MVP reuse result

The old `ReviewCandidate` model is reused only through a non-licensing compatibility adapter. Legacy similarity and confidence do not enter generator decisions. v0.2 review states also remain non-licensing.

## Runtime reuse result

`runtime_reuse_adapter_v0.py` hash-gates the canonical runtime/DB, then imports the existing `generator_view` from `didxaza_runtime_v0_2_6_evidence_adjudication.py`. A test proves a documented supported claim enters the view while retrieval-only evidence does not.

## Next data gates

To move from zero-novelty assembly to genuinely new licensed recombination, materialize one or more independently authorized slot-substitution patterns without analogy. Highest priority:

1. resolve C04 TIME scope inconsistency by explicit adjudication (do not silently add TIME);
2. materialize direct C03 polar question pattern;
3. materialize a small C05 noun/possessor license table;
4. expand direct TAM/person cells through independent development evidence.
