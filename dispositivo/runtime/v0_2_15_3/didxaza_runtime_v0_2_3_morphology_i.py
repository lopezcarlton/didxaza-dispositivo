#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Didxazá runtime v0.2.3 — Morphology I.

Conservative verb morphology:
- loads the operational DIC_VERB_2385 schema
- preserves PBK A/B/C/D class analysis
- recognizes documented habitual Headword surfaces
- recognizes exact documented analytical PDLMA TAM forms
- preserves multiple analyses
- emits only provisional person-suffix candidates

It DOES NOT:
- generate paradigms
- convert PDLMA into orthographic surface
- resolve na-
- apply orthographic suggestions/corrections
"""
from __future__ import annotations

from dataclasses import dataclass
from collections import defaultdict
from pathlib import Path
from typing import Optional, Mapping, Any, Iterable, Sequence
import csv
import re
import unicodedata

from didxaza_runtime_v0_2_0_foundation import (
    AUTO_CORRECT_ENABLED,
    ORTHOGRAPHIC_SUGGESTIONS_ENABLED,
    InputSchemaError,
    normalize_apostrophes,
    strip_tone_marks,
)

RUNTIME_VERSION = "0.2.3"
RUNTIME_STAGE = "MORPHOLOGY_I"
BOUND_ANALYSIS_STATUS = "NOT_IMPLEMENTED"
DIALECT_RESOLUTION_STATUS = "NOT_IMPLEMENTED"
MORPHOLOGY_STATUS = "IMPLEMENTED_CONSERVATIVE_RECOGNITION"

TAM_FIELDS = (
    "habitual",
    "potential",
    "completive",
    "progressive",
    "perfect",
    "future",
    "counterfactual",
    "andative",
)

TAM_LABELS = {
    "habitual": "HABITUAL",
    "potential": "POTENTIAL",
    "completive": "COMPLETIVE",
    "progressive": "PROGRESSIVE",
    "perfect": "PERFECT",
    "future": "FUTURE",
    "counterfactual": "COUNTERFACTUAL",
    "andative": "ANDATIVE",
}


@dataclass(frozen=True)
class PBKRule:
    rule_id: str
    phenomenon: str
    statement: str
    source_id: str
    pages: str
    status: str
    runtime_role: str


PBK_RULES = (
    PBKRule("PBK-VERB-001","verbal_template","TAM=(AUX=)(DERV=)=ROOT(=PL)(=SJT)","BIB059_PBK2016","p.5","HECHO_DOCUMENTAL","STRUCTURAL_CONSTRAINT"),
    PBKRule("PBK-VERB-003","class_A","HAB ri=; CMP be=/bi=; POT gi= + rising tone","BIB059_PBK2016","pp.7-9","HECHO_DOCUMENTAL","CLASS_DESCRIPTION"),
    PBKRule("PBK-VERB-004","class_B","HAB ri=; CMP gu=; POT gi= + rising tone","BIB059_PBK2016","pp.8,15-17","HECHO_DOCUMENTAL","CLASS_DESCRIPTION"),
    PBKRule("PBK-VERB-005","class_C","HAB ri=; CMP gu=; POT g*= with fortition/gemination","BIB059_PBK2016","pp.8,17-21","HECHO_DOCUMENTAL","CLASS_DESCRIPTION"),
    PBKRule("PBK-VERB-006","class_D","Class C-like TAM plus replacive initial in completive","BIB059_PBK2016","pp.8,21-27","HECHO_DOCUMENTAL","CLASS_DESCRIPTION"),
    PBKRule("PBK-VERB-007","diagnostic_tam","Potential and completive are crucial for class assignment","BIB059_PBK2016","pp.7-8","HECHO_DOCUMENTAL","ANALYSIS_CONSTRAINT"),
    PBKRule("PBK-VERB-009","potential_tone","Potential bears underlying rising tone","BIB059_PBK2016","pp.8-9,18-21","HECHO_DOCUMENTAL","ANALYSIS_CONSTRAINT"),
    PBKRule("PBK-VERB-012","g_plus_C","g + simple C produces regular fortis/geminate outcomes","BIB059_PBK2016","pp.4,17-18,37","HECHO_DOCUMENTAL","MORPHOPHONOLOGY"),
    PBKRule("PBK-VERB-019","class_migration","A~B and A~C alternating paradigms are documented","BIB059_PBK2016","pp.27-28,38","HECHO_DOCUMENTAL","AMBIGUITY_PRESERVATION"),
    PBKRule("PBK-VERB-020","irregularity","Irregularity is lexical, not a generic correction rule","BIB059_PBK2016","pp.27-29","HECHO_DOCUMENTAL","BLOCK_GENERATION"),
    PBKRule("PBK-DER-002","na_reanalysis","GP stative vs PBK participial analysis remains in conflict","BIB059_PBK2016","pp.6-7,n.6 p.38","CONFLICTO_ANALITICO","CONFLICT_PRESERVATION"),
)


@dataclass(frozen=True)
class VerbRecord:
    entry_id: str
    headword_raw: str
    pdlma_raw: str
    attribution_entry: str
    analysis_codes_raw: str
    verb_class: str
    class_status: str
    irregular: bool
    definition_es: str
    tam_forms: Mapping[str, tuple[str, ...]]


@dataclass(frozen=True)
class MorphAnalysis:
    entry_id: str
    observed_input: str
    input_layer: str
    recognition_basis: str
    tam: Optional[str]
    tam_status: str
    verb_class: str
    class_status: str
    irregular: bool
    root_analysis_raw: str
    pdlma_evidence_raw: Optional[str]
    headword_evidence_raw: str
    attribution: str
    source_ids: tuple[str, ...]
    rule_ids: tuple[str, ...]
    epistemic_status: str
    orthographic_surface_claim: bool = False


@dataclass(frozen=True)
class PersonCandidate:
    observed_input: str
    person: str
    matched_suffix: str
    source_id: str
    rule_id: str
    status: str = "PROVISIONAL"
    blocking_condition: str = "REQUIRES_LEMMA_PARADIGM_CONFIRMATION"


def surface_index(text: str) -> str:
    """Comparison-only surface index. It never becomes a normalized output."""
    return re.sub(
        r"\s+", " ",
        normalize_apostrophes(strip_tone_marks(text or "")).lower().strip()
    )


def pdlma_index(text: str) -> str:
    """Analytical exact-match index; preserves PDLMA symbols and tone markers."""
    return re.sub(r"\s+", " ", normalize_apostrophes(text or "").lower().strip())


def split_documented_variants(raw: str) -> tuple[str, ...]:
    """Split only explicit top-level ';' / '~' alternatives.

    Parenthetical notation and analytical symbols are retained verbatim.
    """
    raw = (raw or "").strip()
    if not raw:
        return ()
    parts = [x.strip() for x in re.split(r"\s*;\s*|\s+~\s+", raw) if x.strip()]
    return tuple(dict.fromkeys(parts))


def class_status(verb_class: str, analysis_codes: str) -> str:
    if verb_class in {"A~B", "A~C"}:
        return "ALTERNATING"
    if verb_class in {"A", "B", "C", "D"}:
        return "SINGLE_CLASS"
    if analysis_codes.strip() == "v:and":
        return "SPECIAL_ANDATIVE"
    if analysis_codes.strip() == "v:i vers":
        return "SPECIAL_UNCLASSED_VERSIVE"
    return "SPECIAL_UNCLASSIFIED"


class VerbInventoryLoader:
    REQUIRED = (
        "entry_id","headword","pdlma","attribution_entry","analysis_codes_raw",
        "verb_class","irregular","definition_es",
        "habitual","potential","completive","progressive","perfect",
        "future","counterfactual","andative"
    )

    @classmethod
    def load_csv(cls, path: str | Path) -> list[VerbRecord]:
        path = Path(path)
        if not path.exists():
            raise InputSchemaError(f"Verb inventory does not exist: {path}")
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                raise InputSchemaError("Verb inventory has no header")
            missing = [c for c in cls.REQUIRED if c not in reader.fieldnames]
            if missing:
                raise InputSchemaError("Missing DIC_VERB columns: " + ", ".join(missing))
            return [cls.from_row(r) for r in reader]

    @staticmethod
    def from_row(r: Mapping[str, str]) -> VerbRecord:
        vc = (r.get("verb_class") or "").strip()
        codes = (r.get("analysis_codes_raw") or "").strip()
        tams = {
            TAM_LABELS[field]: split_documented_variants(r.get(field, ""))
            for field in TAM_FIELDS
        }
        return VerbRecord(
            entry_id=(r.get("entry_id") or "").strip(),
            headword_raw=r.get("headword","") or "",
            pdlma_raw=r.get("pdlma","") or "",
            attribution_entry=r.get("attribution_entry","") or "",
            analysis_codes_raw=codes,
            verb_class=vc or "SPECIAL",
            class_status=class_status(vc, codes),
            irregular=(r.get("irregular","") or "").strip().upper() == "YES" or "irr" in codes,
            definition_es=r.get("definition_es","") or "",
            tam_forms=tams,
        )


class MorphologyEngine:
    def __init__(self, records: Iterable[VerbRecord]):
        self.records = {r.entry_id: r for r in records}
        self.by_headword_surface: dict[str, list[str]] = defaultdict(list)
        self.by_pdlma_tam: dict[str, list[tuple[str, str, str]]] = defaultdict(list)

        for r in self.records.values():
            # Only a documented habitual paradigm licenses the headword as a
            # HABITUAL recognition channel.
            if r.tam_forms.get("HABITUAL"):
                idx = surface_index(r.headword_raw)
                if idx:
                    self.by_headword_surface[idx].append(r.entry_id)

            for tam, variants in r.tam_forms.items():
                for raw in variants:
                    idx = pdlma_index(raw)
                    if idx:
                        self.by_pdlma_tam[idx].append((r.entry_id, tam, raw))

    @staticmethod
    def _root_raw(record: VerbRecord) -> str:
        # Preserve analytical source. Removing only the citation dash does not
        # project it into orthography.
        p = record.pdlma_raw.strip()
        return p[1:] if p.startswith("-") else p

    def analyze_surface(self, observed_surface: str) -> tuple[MorphAnalysis, ...]:
        idx = surface_index(observed_surface)
        out = []
        for entry_id in self.by_headword_surface.get(idx, []):
            r = self.records[entry_id]
            out.append(MorphAnalysis(
                entry_id=entry_id,
                observed_input=observed_surface,
                input_layer="ORTHOGRAPHIC_SURFACE",
                recognition_basis="DOCUMENTED_HEADWORD_SURFACE",
                tam="HABITUAL",
                tam_status="DOCUMENTED",
                verb_class=r.verb_class,
                class_status=r.class_status,
                irregular=r.irregular,
                root_analysis_raw=self._root_raw(r),
                pdlma_evidence_raw=r.tam_forms["HABITUAL"][0],
                headword_evidence_raw=r.headword_raw,
                attribution=r.attribution_entry,
                source_ids=("BIB054_DICTIONARIA","BIB059_PBK2016"),
                rule_ids=("PBK-VERB-001","PBK-VERB-008"),
                epistemic_status="SOURCE_DOCUMENTED",
                orthographic_surface_claim=True,
            ))
        return tuple(out)

    def analyze_pdlma(self, observed_pdlma: str) -> tuple[MorphAnalysis, ...]:
        idx = pdlma_index(observed_pdlma)
        out = []
        for entry_id, tam, raw_variant in self.by_pdlma_tam.get(idx, []):
            r = self.records[entry_id]
            rule_ids = ["PBK-VERB-001"]
            if tam in {"POTENTIAL","COMPLETIVE"}:
                rule_ids.append("PBK-VERB-007")
            if tam == "POTENTIAL":
                rule_ids.append("PBK-VERB-009")
            out.append(MorphAnalysis(
                entry_id=entry_id,
                observed_input=observed_pdlma,
                input_layer="PDLMA_ANALYTICAL",
                recognition_basis="DOCUMENTED_PDLMA_PARADIGM",
                tam=tam,
                tam_status="DOCUMENTED",
                verb_class=r.verb_class,
                class_status=r.class_status,
                irregular=r.irregular,
                root_analysis_raw=self._root_raw(r),
                pdlma_evidence_raw=raw_variant,
                headword_evidence_raw=r.headword_raw,
                attribution=r.attribution_entry,
                source_ids=("BIB054_DICTIONARIA","BIB059_PBK2016"),
                rule_ids=tuple(rule_ids),
                epistemic_status="SOURCE_DOCUMENTED",
                orthographic_surface_claim=False,
            ))
        return tuple(out)

    def person_candidates(self, observed_surface: str) -> tuple[PersonCandidate, ...]:
        """Graphical candidates only; never confirms person or reconstructs root."""
        s = normalize_apostrophes(observed_surface or "").lower()
        patterns = (
            ("2SG","lu'","GP-PERS-2SG-LU"),
            ("2SG","u'","GP-PERS-2SG-U"),
            ("1SG","ya'","GP-PERS-1SG-YA"),
            ("1SG","a'","GP-PERS-1SG-A"),
        )
        out = []
        for person, suffix, rule in patterns:
            if s.endswith(suffix):
                out.append(PersonCandidate(
                    observed_input=observed_surface,
                    person=person,
                    matched_suffix=suffix,
                    source_id="BIB004_GRAMATICA_POPULAR",
                    rule_id=rule,
                ))
        return tuple(out)


def status() -> dict[str, Any]:
    return {
        "runtime_version": RUNTIME_VERSION,
        "runtime_stage": RUNTIME_STAGE,
        "morphology_status": MORPHOLOGY_STATUS,
        "surface_habitual_recognition": "IMPLEMENTED_DOCUMENTED_HEADWORD_ONLY",
        "analytical_tam_recognition": "IMPLEMENTED_DOCUMENTED_PDLMA_ONLY",
        "surface_nonhabitual_tam_recognition": "NOT_IMPLEMENTED_WITHOUT_DOCUMENTED_SURFACE_MAPPING",
        "person_recognition": "PROVISIONAL_SUFFIX_CANDIDATES_ONLY",
        "pdlma_to_orthography": "PROHIBITED",
        "bound_analysis_status": BOUND_ANALYSIS_STATUS,
        "dialect_resolution_status": DIALECT_RESOLUTION_STATUS,
        "auto_correct_enabled": AUTO_CORRECT_ENABLED,
        "orthographic_suggestions_enabled": ORTHOGRAPHIC_SUGGESTIONS_ENABLED,
    }
