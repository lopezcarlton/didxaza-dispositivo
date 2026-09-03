# Status transitions introduced in vertical slice v0.2

This patch adds **review provenance** without confusing project-owner judgment with native-speaker validation.

| State | Meaning | May auto-correct? |
|---|---|---:|
| `REVIEW_CANDIDATE` | Source-derived candidate requiring review | No |
| `OWNER_SUPPORTED_REVIEW_CANDIDATE` | Project owner judges the candidate plausible/useful | No |
| `PROBABLE_TRANSCRIPTION_CORRECTION` | Exact/near-exact documentary evidence converges with audio re-listen | No |
| `COMPETING_SEGMENTATION_HYPOTHESES` | Two analyses remain live; evidence does not select one | No |
| `NATIVE_SPEAKER_VALIDATED` | Reserved for explicit native-speaker validation | Not automatically; separate policy required |

## Invariants

`PROJECT_OWNER_REVIEW != NATIVE_SPEAKER_VALIDATION`

`PROBABLE_TRANSCRIPTION_CORRECTION != ORTHOGRAPHICALLY_VALIDATED`

`SEGMENTATION_HYPOTHESIS != MORPHOLOGICAL_FACT`

`SOURCE_SUPPORTED_COMPONENT != SOURCE_SUPPORTED_WHOLE_ANALYSIS`
