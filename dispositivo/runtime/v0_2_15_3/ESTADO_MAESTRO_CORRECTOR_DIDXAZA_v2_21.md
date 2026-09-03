# ESTADO MAESTRO DEL CORRECTOR DIDXAZÁ — v2.21

## Checkpoint vigente

`v0.2.15.3 — Surface Semantics & Resolution Integrity — CLOSED_PASS`

DB: `BASE_CORRECTOR_DIDXAZA_SURFACE_SEMANTICS_v2_20.sqlite`  
Canonical state: `canonical_state_v17`

## Estado COR001

```text
107 frases
RT-B-PARTIAL = 75
RT-E-PRESERVE = 32
accepted exact spans = 190
ORTHOGRAPHIC_UNRESOLVED = 128
analysis_open = 129
analysis_review = 2
CandidateEdit = 0
UtteranceValidation = 0
```

Partition unresolved:
```text
86 NONE
31 HYPOTHESIS_ONLY
8 RETRIEVAL_ONLY
3 ANALYSIS_POSITIVE
```

## Invariantes vigentes

- COR001 = TEST CORPUS, no gold standard.
- RETRIEVAL != VALIDATION.
- ANALYSIS_POSITIVE != SURFACE_POSITIVE.
- PDLMA != SURFACE.
- NEAR_MATCH_TO_SURFACE = PROHIBITED.
- TONE_STRIPPING_FOR_EXACT_SURFACE = PROHIBITED.
- SOURCE_COVERAGE != DIALECT_SCOPE.
- UNKNOWN has no named-dialect fallback.
- Person/Possession surface evidence requires exact documentary record.
- Derivational analysis cannot claim surface evidence in the current pipeline.
- Exact TOKEN/SPAN acceptance requires exact coordinates.
- `JUCHITAN_HISTORICAL_SOURCE` is a documentary provenance scope alias; community compatibility canonicalizes it to JUCHITAN without universalization.
- AUTO_CORRECT / visible suggestions / edit execution remain OFF.

## External audit disposition

- DeepSeek provenance grouping bug: FALSE POSITIVE.
- Claude ResolutionVector/person-possession mismatch: CONFIRMED + REPAIRED.
- Claude non-self-contained canonical release: FALSE POSITIVE caused by reduced audit ZIP; canonical release clean-replays.
- Claude/Kimi historical scope concern: CLARIFIED + HARDENED.
- Kimi derivational surface flag: CONFIRMED legacy semantic defect + SANITIZED.
- Kimi parent/subspan API risk: HARDENED.

## Siguiente paso

`v0.2.16 — Source Expansion IV`

Primero auditar BIB001–BIB084 y priorizar nuevas fuentes de superficie. No usar COR001 para seleccionar qué extraer.
