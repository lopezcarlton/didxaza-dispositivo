#!/usr/bin/env python3
"""Execution adapter for the subset of Generator_v0.5 migrated to this repo.

The historical ``generator_v0_5.py`` is preserved unchanged.  This module only
binds that implementation to the single input directory that is complete in
the repository.  It does not promote the migrated subset to linguistic or
pedagogical authority.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

from generator_v0_5 import LicensedGeneratorV02


HERE = Path(__file__).resolve().parent
MIGRATED_INPUTS = HERE / "inputs"


def build_migrated_generator(
    canonical_analyzer: Callable[[str], dict[str, Any]] | None = None,
) -> LicensedGeneratorV02:
    """Instantiate the reproducible subset using only migrated artifacts."""

    return LicensedGeneratorV02(
        inputs_dir=MIGRATED_INPUTS,
        licenses_path=MIGRATED_INPUTS / "GenerationLicense_v0_33_c02_default_qui.jsonl",
        blockers_path=MIGRATED_INPUTS / "IntegrationBlockers_v0_1.jsonl",
        evidence_path=MIGRATED_INPUTS / "GenerationEvidenceAtoms_v0_33_c02_default_qui.jsonl",
        slot_fillers_path=MIGRATED_INPUTS / "AuthorizedSlotFillers_v0_33.jsonl",
        adoptions_path=MIGRATED_INPUTS / "AdoptionRecords_v1.jsonl",
        orth_resolutions_path=MIGRATED_INPUTS / "OrthographicResolutions_v0_9.jsonl",
        canonical_analyzer=canonical_analyzer,
    )


def migrated_execution_state() -> dict[str, Any]:
    """Describe capability actually materialized by the files in this repo."""

    engine = build_migrated_generator()
    active_constructions = sorted({row["construction_id"] for row in engine.licenses})
    blockers = {
        construction_id: row["reason"]
        for construction_id, row in sorted(engine.blockers.items())
    }
    return {
        "status": "MIGRATED_SUBSET_INSTANTIATES",
        "historical_implementation": "generator_v0_5.py",
        "input_profile": "generator/inputs",
        "paradigm_cells": len(engine.cells),
        "construction_inventory": len(engine.constructions),
        "generation_licenses": len(engine.licenses),
        "active_license_constructions": active_constructions,
        "integration_blockers": blockers,
        "readiness_matrix_v14": "MIGRATED_SNAPSHOT_NOT_REPRODUCIBLE_WITH_CURRENT_FILES",
        "research_authority_assertion": False,
    }


def main() -> None:
    print(json.dumps(migrated_execution_state(), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
