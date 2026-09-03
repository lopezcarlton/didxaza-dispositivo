# MVP_LINGUISTICO_001 — reuse map before Generator_v0

## Located artifacts

- `MVP_LINGUISTICO_001_VERTICAL_SLICE_v0_1.zip` — observed SHA-256 `f4819f1525036742e6915a2a9cbaf6cd7417d8ea4bdb7914fafdff93f960c948`.
- `MVP_LINGUISTICO_001_VERTICAL_SLICE_v0_2.zip` — observed SHA-256 `e6524d5d89ed42ff233f6216d29553de644de86e601af21e658627605a6185e2`.

No prior canonical SHA-256 for either MVP ZIP was found in the mounted project records. Therefore these hashes are recorded as **observed historical-artifact hashes**, not retroactively asserted as canonical.

The canonical runtime and DB are separately hash-gated and match their registered canonical hashes.

## v0.1 actual role

`didxaza_vertical_slice_v0_1.py` contains the original non-canonical `ReviewCandidate` engine. It combines Spanish semantic intent, Dictionaria/Pickett evidence, paradigm fields, formal similarity, segmentation candidates and explicit blockers.

## Reused

1. `REVIEW_CANDIDATE` remains an analysis/review state distinct from correction and validation.
2. Candidate provenance fields are preserved through `mvp_review_candidate_adapter_v0.py`.
3. Blockers remain first-class.
4. The abstention/non-autocorrection contract is preserved.
5. v0.2 review-state distinctions are preserved as review provenance, never as automatic generation licenses.

## Explicitly quarantined from Generator_v0

- `SequenceMatcher` / formal near-match ranking;
- destructive diacritic-insensitive normalization for choosing output surface;
- `clean_paradigm_surface()` and paradigm-derived surface proposals;
- COR001 replay/benchmark dependency;
- legacy `confidence` labels;
- case-specific COR001 handlers;
- owner review or `PROBABLE_TRANSCRIPTION_CORRECTION` as generation license.

These historical mechanisms may remain useful for analysis of the antecedent but cannot license NC001 output under architecture v1.1.

## Runtime reuse

Generator integration reuses the existing canonical `generator_view(claims)` from v0.2.6 through a hash-gated adapter. It is not reimplemented.
