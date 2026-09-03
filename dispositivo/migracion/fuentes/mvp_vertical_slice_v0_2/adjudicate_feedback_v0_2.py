#!/usr/bin/env python3
"""Adjudicate project-owner review without promoting it to native-speaker validation.

Safety invariants:
- OWNER review != NATIVE_SPEAKER validation.
- REVIEW_CANDIDATE != AUTO_CORRECT.
- A segmentation hypothesis may remain competing even when one morpheme is documented.
"""
from __future__ import annotations
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INP = ROOT / "ADJUDICATION_INPUT_v0_2.csv"
OUT = ROOT / "ADJUDICATION_RESULTS_v0_2.csv"

TRANSITIONS = {
    "FB-076": {
        "new_status": "OWNER_SUPPORTED_REVIEW_CANDIDATE",
        "auto_correct": "false",
        "native_validated": "false",
        "engine_action": "prefer chaahui' as review candidate; preserve original until speaker/source-context validation",
    },
    "FB-079": {
        "new_status": "PROBABLE_TRANSCRIPTION_CORRECTION",
        "auto_correct": "false",
        "native_validated": "false",
        "engine_action": "rank sacani above zaca ni' for review because exact semantic pattern + owner's audio re-listen agree",
    },
    "FB-062": {
        "new_status": "COMPETING_SEGMENTATION_HYPOTHESES",
        "auto_correct": "false",
        "native_validated": "false",
        "engine_action": "retain H1=eeda future allomorph hypothesis and H2=zee + nda' owner hypothesis; do not collapse",
    },
}

with INP.open(encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))

fields = list(rows[0]) + ["new_status", "auto_correct", "native_validated", "engine_action"]
with OUT.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    for row in rows:
        t = TRANSITIONS[row["case_id"]]
        w.writerow({**row, **t})

print(f"wrote {OUT}")
