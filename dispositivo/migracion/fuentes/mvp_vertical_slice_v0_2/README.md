# MVP_LINGUISTICO_001_VERTICAL_SLICE_v0_2

**Estado migratorio del subárbol:** `ARCHIVE_ONLY / NON_AUTHORITY / NOT_ACTIVE_TEST_SUITE`

Update driven by project-owner review of FB-076, FB-079 and FB-062.

## Main change

The engine now represents **degrees and provenance of human review** rather than treating every human comment as equivalent validation.

- FB-076: `chaahui'` promoted to owner-supported review candidate.
- FB-079: `sacani` promoted to probable transcription correction because documentary evidence and audio re-listen converge.
- FB-062: `zee + nda'` added as a competing segmentation hypothesis; `nda'` is source-supported as a pragmatic particle, but the whole segmentation is deliberately left unresolved.

No `AUTO_CORRECT` is enabled and no native-speaker validation is claimed.

## Migration / test-status note

`MIGRATION_MANIFEST_v1.md` classifies this recovered subárbol as `ARCHIVE_ONLY / NON_AUTHORITY`. Its historical filenames and payloads are preserved for genealogy; they are not the active validation suite of `didxaza-dispositivo`.

In particular, `test_adjudication_v0_2.py` is a historical import-time assertion script. It defines no `unittest.TestCase` and no unittest test methods; when its module-level assertions complete it prints:

```text
PASS: adjudication invariants preserved
```

That line means only that those historical module-level assertions completed in the environment where the script was run. It must not be interpreted as:

```text
CURRENT_CI_PASS
CURRENT_UNITTEST_COUNT > 0
LINGUISTIC_VALIDATION
NATIVE_SPEAKER_VALIDATION
KNOWLEDGE_AUTHORITY
```

Do not rewrite the archived script merely to make test discovery report cases. If the invariant needs current executable coverage, implement a new explicit test outside this archived source subtree and connect it to current artifacts.
