#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Didxazá runtime v0.2.2 — Context & Provenance.

Builds on v0.2.1 Retrieval.

Adds:
- executable context profiles
- source profiles / coverage
- attribution registry with explicit UNKNOWN behavior
- validation events that distinguish production/review/orthographic validation
- provenance wrappers for retrieval matches

Still disabled/not implemented:
- morphology
- grammatical BOUND analysis
- inferential dialect resolution
- orthographic suggestions
- automatic correction
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Optional, Mapping, Any, Sequence, Iterable
from pathlib import Path
import csv
import json
import re

from didxaza_runtime_v0_2_0_foundation import (
    AUTO_CORRECT_ENABLED,
    ORTHOGRAPHIC_SUGGESTIONS_ENABLED,
    ContextProfile,
    InputSchemaError,
)
from didxaza_runtime_v0_2_1_retrieval import (
    RetrievalEngine,
    SpanLexicalMatch,
)

RUNTIME_VERSION = "0.2.2"
RUNTIME_STAGE = "CONTEXT_PROVENANCE"
MORPHOLOGY_STATUS = "NOT_IMPLEMENTED"
BOUND_ANALYSIS_STATUS = "NOT_IMPLEMENTED"
DIALECT_RESOLUTION_STATUS = "NOT_IMPLEMENTED"

UNKNOWN = "UNKNOWN"
NOT_APPLICABLE = "NOT_APPLICABLE"

CONTEXT_FIELDS = (
    "speaker_id",
    "community",
    "dialect_core",
    "dialect_membership",
    "membership_strength",
    "transition_status",
    "corpus_id",
    "editorial_profile",
    "production_context",
    "age_group",
    "literacy_language",
)

VALIDATION_KINDS = frozenset({
    "SPEAKER_PRODUCED",
    "SPEAKER_REVIEWED",
    "SPEAKER_ORTHOGRAPHICALLY_VALIDATED",
    "PROJECT_EDITORIAL_DECISION",
})


@dataclass(frozen=True)
class SourceProfile:
    source_id: str
    source_type: str
    evidence_roles: tuple[str, ...]
    historical_period: Optional[str]
    communities: tuple[str, ...]
    dialect_scope: tuple[str, ...]
    normative_scope: tuple[str, ...]
    analytical_scope: tuple[str, ...]
    coverage_profile: Mapping[str, Any]
    status: str = "CURRENT"


@dataclass(frozen=True)
class AttributionRecord:
    attribution_code: str
    source_id: str
    speaker_or_contributor_id: Optional[str]
    community: str
    dialect_core: str
    evidence_source: str
    confidence_status: str


@dataclass(frozen=True)
class AttributionResolution:
    attribution_code: str
    source_id: str
    mapping_status: str
    speaker_or_contributor_id: Optional[str]
    community: str
    dialect_core: str
    evidence_source: Optional[str]
    confidence_status: str


@dataclass(frozen=True)
class ValidationEvent:
    validation_id: str
    target_ref: str
    target_start: Optional[int]
    target_end: Optional[int]
    validator_type: str
    speaker_id: Optional[str]
    community: str
    validation_kind: str
    validation_date: Optional[str]
    notes: Optional[str]

    def __post_init__(self):
        if self.validation_kind not in VALIDATION_KINDS:
            raise ValueError(f"Unsupported validation_kind: {self.validation_kind}")
        if (self.target_start is None) ^ (self.target_end is None):
            raise ValueError("target_start and target_end must be both set or both null")
        if self.target_start is not None:
            if self.target_start < 0 or self.target_end < self.target_start:
                raise ValueError("Invalid target span")

    @property
    def is_explicit_orthographic_validation(self) -> bool:
        return self.validation_kind in {
            "SPEAKER_ORTHOGRAPHICALLY_VALIDATED",
            "PROJECT_EDITORIAL_DECISION",
        }


@dataclass(frozen=True)
class ProvenancedSpanMatch:
    lexical_match: SpanLexicalMatch
    context: ContextProfile
    source_profile: SourceProfile
    attribution_resolutions: tuple[AttributionResolution, ...]


def _norm_context_value(value: Optional[str], *, optional: bool = False) -> Optional[str]:
    if value is None:
        return None if optional else UNKNOWN
    value = str(value).strip()
    if not value:
        return None if optional else UNKNOWN
    return value


def context_from_row(row: Mapping[str, Any], defaults: Optional[Mapping[str, Any]] = None) -> ContextProfile:
    """Build context without dialect inference.

    Row values override defaults. Missing core dialect fields remain UNKNOWN.
    """
    defaults = defaults or {}

    def get(name: str, optional: bool = False):
        if name in row and row[name] not in (None, ""):
            return _norm_context_value(row[name], optional=optional)
        return _norm_context_value(defaults.get(name), optional=optional)

    return ContextProfile(
        speaker_id=get("speaker_id", optional=True),
        community=get("community"),
        dialect_core=get("dialect_core"),
        dialect_membership=get("dialect_membership"),
        membership_strength=get("membership_strength"),
        transition_status=get("transition_status"),
        corpus_id=get("corpus_id", optional=True),
        editorial_profile=get("editorial_profile", optional=True),
        production_context=get("production_context", optional=True),
        age_group=get("age_group", optional=True),
        literacy_language=get("literacy_language", optional=True),
    )


class ContextInputValidator:
    """Validates core corpus columns while allowing optional context columns."""

    REQUIRED_COLUMNS = ("ID", "Bloque", "Español", "Didxazá_original")

    @classmethod
    def validate_csv(cls, path: str | Path):
        path = Path(path)
        if not path.exists():
            raise InputSchemaError(f"Input file does not exist: {path}")
        try:
            with path.open("r", encoding="utf-8-sig", newline="") as f:
                reader = csv.DictReader(f)
                if reader.fieldnames is None:
                    raise InputSchemaError("CSV has no header")
                missing = [c for c in cls.REQUIRED_COLUMNS if c not in reader.fieldnames]
                if missing:
                    raise InputSchemaError("Missing required columns: " + ", ".join(missing))
                rows = list(reader)
                return rows, tuple(reader.fieldnames)
        except UnicodeDecodeError as e:
            raise InputSchemaError(f"Input is not valid UTF-8: {e}") from e


def parse_attribution_codes(raw: str) -> tuple[str, ...]:
    """Preserve source attribution codes without guessing their identity.

    Dictionaria may use separators in metadata; this parser only separates
    explicit codes. It does not infer community or contributor identity.
    """
    raw = (raw or "").strip()
    if not raw:
        return ()
    codes = [x.strip() for x in re.split(r"[;,|]+", raw) if x.strip()]
    return tuple(dict.fromkeys(codes))


class AttributionRegistry:
    def __init__(self, records: Iterable[AttributionRecord] = ()):
        self._records = {(r.attribution_code, r.source_id): r for r in records}

    def add(self, record: AttributionRecord) -> None:
        self._records[(record.attribution_code, record.source_id)] = record

    def resolve(self, attribution_code: str, source_id: str) -> AttributionResolution:
        rec = self._records.get((attribution_code, source_id))
        if rec is None:
            return AttributionResolution(
                attribution_code=attribution_code,
                source_id=source_id,
                mapping_status="UNKNOWN_NOT_MAPPED",
                speaker_or_contributor_id=None,
                community=UNKNOWN,
                dialect_core=UNKNOWN,
                evidence_source=None,
                confidence_status="UNKNOWN",
            )
        return AttributionResolution(
            attribution_code=rec.attribution_code,
            source_id=rec.source_id,
            mapping_status="DOCUMENTED_MAPPING",
            speaker_or_contributor_id=rec.speaker_or_contributor_id,
            community=rec.community,
            dialect_core=rec.dialect_core,
            evidence_source=rec.evidence_source,
            confidence_status=rec.confidence_status,
        )


class SourceRegistry:
    def __init__(self, profiles: Iterable[SourceProfile] = ()):
        self._profiles = {p.source_id: p for p in profiles}

    def add(self, profile: SourceProfile) -> None:
        self._profiles[profile.source_id] = profile

    def get(self, source_id: str) -> Optional[SourceProfile]:
        return self._profiles.get(source_id)

    def require(self, source_id: str) -> SourceProfile:
        p = self.get(source_id)
        if p is None:
            raise KeyError(f"Unknown source_id: {source_id}")
        return p

    def all(self) -> tuple[SourceProfile, ...]:
        return tuple(self._profiles.values())


# Source scopes below are materialized only from explicit statements in the
# project state master; they are not runtime inferences.
DEFAULT_SOURCE_PROFILES = (
    SourceProfile(
        source_id="BIB015_ALFABETO_POPULAR_1956",
        source_type="HISTORICAL_ORTHOGRAPHY",
        evidence_roles=("HISTORICAL_NORM", "ORTHOGRAPHY"),
        historical_period="1956",
        communities=("JUCHITAN",),
        dialect_scope=("CENTRAL_JUCHITAN_WEIGHTED",),
        normative_scope=("HISTORICAL_ORTHOGRAPHY",),
        analytical_scope=(),
        coverage_profile={
            "representativeness": "CENTRAL_JUCHITAN_WEIGHTED",
            "note": "Historical reference; not assumed dialect-neutral.",
        },
    ),
    SourceProfile(
        source_id="BIB004_GRAMATICA_POPULAR",
        source_type="GRAMMAR",
        evidence_roles=("MORPHOLOGY", "ORTHOGRAPHIC_SURFACE", "PEDAGOGICAL_GRAMMAR"),
        historical_period="1998_PRINT_2001_ELECTRONIC",
        communities=("JUCHITAN",),
        dialect_scope=("JUCHITAN_PRIMARY",),
        normative_scope=("HISTORICAL_PEDAGOGICAL_SURFACE",),
        analytical_scope=("MORPHOLOGY", "POSSESSION", "TAM", "PRONOUNS"),
        coverage_profile={
            "representativeness": "JUCHITAN_PRIMARY",
            "note": "Describes mainly Juchitán.",
        },
    ),
    SourceProfile(
        source_id="BIB056_CUADERNO_2015",
        source_type="LITERACY_MATERIAL",
        evidence_roles=("CONTEMPORARY_USAGE", "ORTHOGRAPHY_PEDAGOGICAL", "TONE_PEDAGOGICAL"),
        historical_period="2015",
        communities=("LA_VENTOSA", "SANTA_MARIA_XADANI", "JUCHITAN"),
        dialect_scope=("MULTI_COMMUNITY",),
        normative_scope=("PILOT_NOT_FINAL_NORM",),
        analytical_scope=("ORTHOGRAPHY", "TONE_PEDAGOGY"),
        coverage_profile={
            "representativeness": "THREE_COMMUNITY_PILOT",
            "note": "Pilot material, not definitive norm.",
        },
    ),
    SourceProfile(
        source_id="BIB054_DICTIONARIA",
        source_type="LEXICOGRAPHIC_RESOURCE",
        evidence_roles=("LEXICON", "EXAMPLES", "PDLMA_ANALYSIS", "DOCUMENTED_USAGE"),
        historical_period=None,
        communities=("LA_VENTOSA", "JUCHITAN", "SANTA_MARIA_XADANI"),
        dialect_scope=("MULTI_COMMUNITY",),
        normative_scope=(),
        analytical_scope=("LEXICAL", "MORPHOLOGICAL", "BOUND", "TONE"),
        coverage_profile={
            "representativeness": "MULTI_COMMUNITY_UNEQUAL_COVERAGE",
            "note": "Greater weight from La Ventosa; does not represent all Isthmus varieties.",
        },
    ),
    SourceProfile(
        source_id="BIB063_CARDONA",
        source_type="DIALECTOLOGY",
        evidence_roles=("DIALECTOLOGY", "PHONATION", "LEXICAL_VARIATION", "COMMUNITY_COMPARISON"),
        historical_period="2018_THESIS_CITED_2020",
        communities=("JUC", "SBA", "UNH", "XAD", "IXA", "IXE", "TEH", "ESP", "COM"),
        dialect_scope=("SOUTH", "CENTRAL", "NORTH", "TRANSITION"),
        normative_scope=(),
        analytical_scope=("DIALECTOLOGY", "PHONATION", "VARIATION"),
        coverage_profile={
            "representativeness": "NINE_COMMUNITIES_36_PARTICIPANTS",
            "note": "Variation evidence is not a correctness hierarchy.",
        },
    ),
    SourceProfile(
        source_id="BIB084_DEANDA2022",
        source_type="LEARNER_PRODUCTION_STUDY",
        evidence_roles=("LEARNER_PRODUCTION", "PEDAGOGICAL_DIFFICULTY"),
        historical_period="2022_THESIS_2023_REPOSITORY",
        communities=("RANCHO_EL_LLANO_SAN_BLAS_ATEMPA", "SBA"),
        dialect_scope=("SOUTH",),
        normative_scope=(),
        analytical_scope=("LEARNER_ORTHOGRAPHY", "PEDAGOGY"),
        coverage_profile={
            "representativeness": "LEARNER_SAMPLE",
            "normative_warning": "LEARNER_PRODUCTION != NORMATIVE_EVIDENCE",
        },
    ),
)


def default_source_registry() -> SourceRegistry:
    return SourceRegistry(DEFAULT_SOURCE_PROFILES)


def provenance_for_match(
    engine: RetrievalEngine,
    match: SpanLexicalMatch,
    context: ContextProfile,
    source_registry: SourceRegistry,
    attribution_registry: AttributionRegistry,
    source_id: str = "BIB054_DICTIONARIA",
) -> ProvenancedSpanMatch:
    """Attach source/context provenance without changing lexical retrieval."""
    profile = source_registry.require(source_id)
    resolutions = []
    seen = set()
    for entry_id in match.entry_ids:
        entry = engine.entries[entry_id]
        for code in parse_attribution_codes(entry.attribution):
            key = (code, source_id)
            if key in seen:
                continue
            seen.add(key)
            resolutions.append(attribution_registry.resolve(code, source_id))
    return ProvenancedSpanMatch(
        lexical_match=match,
        context=context,
        source_profile=profile,
        attribution_resolutions=tuple(resolutions),
    )


def status() -> dict[str, Any]:
    return {
        "runtime_version": RUNTIME_VERSION,
        "runtime_stage": RUNTIME_STAGE,
        "auto_correct_enabled": AUTO_CORRECT_ENABLED,
        "orthographic_suggestions_enabled": ORTHOGRAPHIC_SUGGESTIONS_ENABLED,
        "morphology_status": MORPHOLOGY_STATUS,
        "bound_analysis_status": BOUND_ANALYSIS_STATUS,
        "dialect_resolution_status": DIALECT_RESOLUTION_STATUS,
        "context_profile": "IMPLEMENTED",
        "source_profile": "IMPLEMENTED",
        "attribution_map": "IMPLEMENTED_DOCUMENTED_ONLY",
        "validation_event": "IMPLEMENTED",
    }
