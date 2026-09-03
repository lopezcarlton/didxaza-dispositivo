#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class LegacyReviewCandidateAdapter:
    observed_surface: str
    proposed_surface: str
    span_start_token: int
    span_end_token: int
    candidate_type: str
    status: str
    semantic_anchor: str
    rationale: str
    evidence: tuple[dict[str, Any], ...]
    blockers: tuple[str, ...]
    licensing_effect: str = "NONE"
    may_auto_correct: bool = False
    may_license_generation: bool = False


def adapt_v01_review_candidate(candidate: dict[str, Any]) -> LegacyReviewCandidateAdapter:
    """Reuse the MVP REVIEW_CANDIDATE contract without importing its legacy ranking path.

    Legacy score/similarity fields are intentionally not propagated. The object can
    support analysis/review workflows only and can never become a generation license.
    """
    if candidate.get("status") != "REVIEW_CANDIDATE":
        raise ValueError("ONLY_REVIEW_CANDIDATE_CAN_BE_ADAPTED")
    blockers = tuple(candidate.get("blockers") or ()) + ("LEGACY_REVIEW_CANDIDATE_NON_LICENSING",)
    return LegacyReviewCandidateAdapter(
        observed_surface=candidate["observed"],
        proposed_surface=candidate["proposed"],
        span_start_token=int(candidate["span_start_token"]),
        span_end_token=int(candidate["span_end_token"]),
        candidate_type=candidate["candidate_type"],
        status="REVIEW_CANDIDATE",
        semantic_anchor=candidate.get("semantic_anchor", ""),
        rationale=candidate.get("rationale", ""),
        evidence=tuple(candidate.get("evidence") or ()),
        blockers=blockers,
    )


V02_REVIEW_STATES = frozenset({
    "REVIEW_CANDIDATE",
    "OWNER_SUPPORTED_REVIEW_CANDIDATE",
    "PROBABLE_TRANSCRIPTION_CORRECTION",
    "COMPETING_SEGMENTATION_HYPOTHESES",
    "NATIVE_SPEAKER_VALIDATED",
})


def v02_state_is_generation_license(state: str) -> bool:
    # Even NATIVE_SPEAKER_VALIDATED is not automatically an orthographic/generation license.
    if state not in V02_REVIEW_STATES:
        raise ValueError("UNKNOWN_V02_REVIEW_STATE")
    return False
