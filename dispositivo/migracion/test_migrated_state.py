#!/usr/bin/env python3
"""Small consistency checks for artifacts explicitly migrated to the repo."""

from __future__ import annotations

import csv
import hashlib
import json
import sqlite3
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GENERATOR_DIR = ROOT / "dispositivo" / "generator"
RUNTIME_DIR = ROOT / "dispositivo" / "runtime" / "v0_2_15_3"
ANALYZER_DIR = ROOT / "dispositivo" / "analyzer"
RELEASE_MANIFEST_PATH = RUNTIME_DIR / "RELEASE_FILE_MANIFEST_v0_2_15_3.json"
RELEASE_ANCHOR_PATH = ROOT / "RELEASE_MANIFEST_ANCHOR_v0_2_15_3.json"
INPUT_LAYOUT_CONTRACT_PATH = GENERATOR_DIR / "INPUT_LAYOUT_CONTRACT_v1.json"

# Monotonic floor from the verified 2026-09-03 migration checkpoint.
# Additional exact payloads may be recovered later without making this test stale;
# falling below this floor is a migration-state regression.
MIGRATION_BASELINE_PRESENT_RELEASE_PAYLOADS = 39

sys.path.insert(0, str(GENERATOR_DIR))
sys.path.insert(0, str(ANALYZER_DIR))
sys.path.insert(0, str(RUNTIME_DIR))

from analyzer_v0_35_migrated_adapter import (  # noqa: E402
    build_migrated_analyzer,
    migrated_execution_state as analyzer_execution_state,
)
from generator_v0_5_migrated_adapter import migrated_execution_state  # noqa: E402
from didxaza_runtime_v0_2_15_3_surface_semantics_resolution_integrity import (  # noqa: E402
    status as surface_semantics_status,
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_release_anchor() -> dict:
    return json.loads(RELEASE_ANCHOR_PATH.read_text(encoding="utf-8"))


def load_input_layout_contract() -> dict:
    return json.loads(INPUT_LAYOUT_CONTRACT_PATH.read_text(encoding="utf-8"))


class MigratedStateTests(unittest.TestCase):
    def test_release_manifest_matches_independent_anchor(self) -> None:
        anchor = load_release_anchor()
        manifest_path = ROOT / anchor["artifact_path"]
        self.assertEqual(manifest_path.resolve(), RELEASE_MANIFEST_PATH.resolve())
        self.assertEqual(sha256(manifest_path), anchor["sha256"])
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(len(manifest["sha256"]), anchor["release_file_count"])
        self.assertEqual(anchor["cor001_policy"], "ANALYSIS_TARGET_ONLY")

    def test_exact_sqlite_and_critical_tables(self) -> None:
        path = RUNTIME_DIR / "BASE_CORRECTOR_DIDXAZA_SURFACE_SEMANTICS_v2_20.sqlite"
        self.assertEqual(
            sha256(path),
            "2379773426baf4e3eace87c61ec17f7a1e1b9164421e56cf736d35eb64a5ebed",
        )
        connection = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
        try:
            self.assertEqual(connection.execute("PRAGMA integrity_check").fetchone()[0], "ok")
            self.assertEqual(connection.execute("PRAGMA foreign_key_check").fetchall(), [])
            self.assertEqual(
                connection.execute("SELECT COUNT(*) FROM canonical_state_v17").fetchone()[0],
                22,
            )
            tables = {
                row[0]
                for row in connection.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                )
            }
            self.assertIn("verb_lexeme_class_v023", tables)
            self.assertIn("person_possession_exact_v0214", tables)
        finally:
            connection.close()

    def test_exact_verb_inventory(self) -> None:
        path = ANALYZER_DIR / "DIC_VERB_2385_v0_1.csv"
        self.assertEqual(
            sha256(path),
            "2bdf4afd4b61234c54585cda17ad648bfb71194e9463d193eb04a5a06aa3183d",
        )
        with path.open(encoding="utf-8-sig", newline="") as source:
            rows = list(csv.DictReader(source))
        self.assertEqual(len(rows), 2385)
        self.assertEqual(len({row["entry_id"] for row in rows}), 2385)

    def test_exact_dictionaria_inputs(self) -> None:
        expected = {
            "DICTIONARIA_entries_v0_2_15_2.csv": (
                "a093b8eb5087affb7d7d7f364bb0a423921c20e959d61fe7efcd85de62b249d0",
                9012,
            ),
            "DICTIONARIA_senses_v0_2_15_2.csv": (
                "244769e4b3d724e5373feb3ccd26405c517340d05b70d962564ed4a4142d2afb",
                9046,
            ),
            "DICTIONARIA_examples_v0_2_15_2.csv": (
                "2a6e906e8cc8dc43d69306a0a69332f257ae470b5caeb47d3aef72d17ba9af8b",
                9686,
            ),
        }
        for name, (expected_hash, expected_rows) in expected.items():
            path = RUNTIME_DIR / name
            self.assertEqual(sha256(path), expected_hash)
            with path.open(encoding="utf-8-sig", newline="") as source:
                rows = list(csv.reader(source))
            self.assertEqual(len(rows) - 1, expected_rows)

    def test_analyzer_instantiates_and_preserves_non_licensing_limits(self) -> None:
        state = analyzer_execution_state()
        self.assertEqual(
            state["status"],
            "REPRODUCIBLE_NON_LICENSING_PARTIAL_ANALYZER",
        )
        self.assertEqual(state["dictionaria_entries"], 9012)
        self.assertEqual(state["dictionaria_senses"], 9046)
        self.assertEqual(state["dictionaria_examples"], 9686)
        self.assertEqual(state["verb_inventory_rows"], 2385)
        self.assertEqual(state["person_possession_exact_rows"], 100)
        self.assertFalse(state["cor001_benchmark_allowed"])
        self.assertFalse(state["research_authority_assertion"])

        engine = build_migrated_analyzer()
        try:
            documented = engine.analyze("Quí rasé'", item_id="SMOKE-DOCUMENTED")
            unknown = engine.analyze(
                "FORMA_INEXISTENTE_SMOKE_20260901",
                item_id="SMOKE-ABSTENTION",
            )
        finally:
            engine.close()
        self.assertEqual(documented["analysis_status"], "PARTIAL_ANALYSIS_NON_LICENSING")
        self.assertEqual(unknown["analysis_status"], "ABSTAIN_NO_COMPONENT_EVIDENCE")
        for result in (documented, unknown):
            self.assertFalse(result["generation_license_assertion"])
            self.assertFalse(result["correction_assertion"])
            self.assertFalse(result["orthographic_authority_assertion"])
            self.assertFalse(result["rule_discovery_assertion"])

    def test_generator_migrated_subset_instantiates(self) -> None:
        state = migrated_execution_state()
        self.assertEqual(state["status"], "MIGRATED_SUBSET_INSTANTIATES")
        self.assertEqual(state["paradigm_cells"], 72)
        self.assertEqual(state["construction_inventory"], 6)
        self.assertEqual(state["generation_licenses"], 6)
        self.assertEqual(state["active_license_constructions"], ["C01", "C02"])
        self.assertEqual(sorted(state["integration_blockers"]), ["C03", "C04", "C05", "C06"])
        self.assertFalse(state["research_authority_assertion"])

    def test_generator_historical_duplicate_inputs_match_active_layout(self) -> None:
        contract = load_input_layout_contract()
        self.assertEqual(
            contract["canonical_active_input_dir"],
            "dispositivo/generator/inputs",
        )
        self.assertEqual(
            contract["historical_generator_layout_status"],
            "MIXED_LAYOUT_PRESERVED_UNMODIFIED",
        )
        duplicates = contract["duplicate_copies"]
        self.assertEqual(len(duplicates), 9)
        for pair in duplicates:
            copy_path = ROOT / pair["copy"]
            canonical_path = ROOT / pair["canonical"]
            self.assertTrue(copy_path.is_file(), pair["copy"])
            self.assertTrue(canonical_path.is_file(), pair["canonical"])
            self.assertEqual(
                sha256(copy_path),
                sha256(canonical_path),
                f"Historical input copy diverged: {pair['copy']} != {pair['canonical']}",
            )

    def test_exact_runtime_closure_tests_pass(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "unittest",
                "-v",
                "test_adversarial_repairs_v0_2_15_2.py",
                "test_replay_v0_2_15_2.py",
                "test_schema_v0_2_15_2.py",
                "test_surface_semantics_v0_2_15_3.py",
            ],
            cwd=RUNTIME_DIR,
            check=False,
            capture_output=True,
            text=True,
        )
        output = completed.stdout + completed.stderr
        self.assertEqual(completed.returncode, 0, output)
        self.assertIn("Ran 38 tests", output)
        self.assertIn("OK", output)

        state = surface_semantics_status()
        self.assertEqual(state["runtime_version"], "0.2.15.3")
        self.assertFalse(state["analysis_only_surface_promotion"])
        self.assertFalse(state["auto_correct_enabled"])
        self.assertFalse(state["orthographic_suggestions_enabled"])
        self.assertFalse(state["edit_execution_enabled"])
        self.assertFalse(state["user_visible_suggestions_enabled"])

    def test_all_present_release_payloads_are_exact(self) -> None:
        manifest = json.loads(RELEASE_MANIFEST_PATH.read_text(encoding="utf-8"))
        anchor = load_release_anchor()
        expected = manifest["sha256"]
        present = {
            name: sha256(RUNTIME_DIR / name)
            for name in expected
            if (RUNTIME_DIR / name).is_file()
        }
        mismatches = {
            name: actual
            for name, actual in present.items()
            if actual != expected[name]
        }
        self.assertEqual(len(expected), anchor["release_file_count"])
        self.assertGreaterEqual(
            len(present),
            MIGRATION_BASELINE_PRESENT_RELEASE_PAYLOADS,
            "Migrated release payload count regressed below the verified 2026-09-03 checkpoint",
        )
        self.assertEqual(mismatches, {})
        self.assertLessEqual(
            len(expected) - len(present),
            anchor["release_file_count"] - MIGRATION_BASELINE_PRESENT_RELEASE_PAYLOADS,
        )


if __name__ == "__main__":
    unittest.main()
