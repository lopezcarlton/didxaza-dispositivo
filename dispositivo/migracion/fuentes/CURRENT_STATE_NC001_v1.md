# CURRENT_STATE_NC001_v1 — 2026-08-28

## Frozen governance

```text
ARCHITECTURE = v1.1 FROZEN
CANONICAL_PREDECESSOR = v0.2.15.3
COR001_ROLE = ANALYSIS_TARGET_ONLY
HOLDOUT_PROTOCOL = SEALED
HOLDOUT_CONTENT = NOT_ACQUIRED / NOT_SEEN
```

## NC001 foundations materialized

```text
VERBS_SELECTED = 12
VERB_CLASSES = A | C | D
TARGET_TAM = HABITUAL | COMPLETIVE
TARGET_PERSON = 1SG | 2SG | 3SG_HUMAN
CONSTRUCTIONS = 6
PARADIGM_CELLS_TOTAL = 72
PARADIGM_ATTESTED = 12
PARADIGM_UNATTESTED = 60
CONCEPT_MAPPING_ROWS = 2
ORTHOGRAPHIC_ADOPTION_RECORDS = 8
VALIDATION_QUEUE_GROUPS = 7
DEV_CORPUS_REAL_UTTERANCES = 0
```

## Construction status

- C01: partial data readiness; generation still requires runtime integration and all licenses.
- C02: partial data readiness for directly attested H/C negative patterns only.
- C03: blocked — no direct polar surface pattern materialized.
- C04: partial data readiness for exact authorized interrogative patterns only.
- C05: blocked for generation — no small licensed noun/possessor set materialized yet.
- C06: generator disabled — dependent POTENTIAL is outside frozen TAM scope.

## Orthographic status

The draft profile is conservative, not a global norm. It preserves observed surface and prohibits PDLMA→surface, strip-tone, strip-accent, near-match→surface, destructive normalization and global clitic/compound spacing rules.

## Development corpus

Acquisition scaffolding is ready: audio-first protocol, 20 situational prompts, session/unit and utterance templates. No didxazá utterances were generated as placeholders.

## Current hard blockers

### B1 — canonical runtime assets not mounted
No executable v0.2.15.3 runtime or `BASE_CORRECTOR_DIDXAZA_SURFACE_SEMANTICS_v2_20.sqlite` is present in the active filesystem. Creating a parallel runtime is prohibited.

### B2 — real development audio not yet acquired
The next evidence-bearing corpus step requires newly recorded speech from documented Juchitán speaker(s).

### B3 — speaker judgments not executed
Only the judgment protocol/template exists.

### B4 — holdout content not acquired
The protocol is sealed; content remains unseen.

## Next safe execution

Parallel external prerequisites:

```text
A. MOUNT_CANONICAL_RUNTIME_v0.2.15.3 + SQLITE -> VERIFY HASH -> GAP_ANALYSIS -> MINIMAL MIGRATION
B. RECORD_DEV_AUDIO_FIRST_JUCHITAN -> SPEAKER_CONFIRM -> SPEAKER_ATTESTATION -> DEVELOPMENT ANALYSIS
```

Do not open/acquire holdout into development. Do not use COR001 to close any blocker.
