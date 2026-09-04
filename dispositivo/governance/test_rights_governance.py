#!/usr/bin/env python3
from __future__ import annotations

import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def load_json(name: str):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


class RightsGovernanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inventory = load_json("RIGHTS_PROVENANCE_INVENTORY_v3.json")
        cls.source_map = load_json("SQLITE_RIGHTS_SOURCE_MAP_v1.json")
        cls.source_map_v219 = load_json("SQLITE_V2_19_RIGHTS_SOURCE_MAP_v1.json")
        cls.replay_map = load_json("REPLAY_ARTIFACT_RIGHTS_MAP_v1.json")
        cls.supplement = load_json("SOURCE_PROFILE_SUPPLEMENT_v1.json")

    def test_blanket_license_remains_blocked_and_root_license_absent(self):
        self.assertEqual(
            self.inventory["blanket_license_status"],
            "BLOCKED_PENDING_RIGHTS_AND_DISTRIBUTION_ARCHITECTURE",
        )
        self.assertFalse((ROOT / "LICENSE").exists())
        self.assertFalse((ROOT / "LICENSE.txt").exists())
        self.assertFalse((ROOT / "LICENSE.md").exists())

    def test_supplement_matches_verified_source_profile_gap(self):
        missing = set(self.source_map["source_profile"]["verified_missing_but_used_source_ids"])
        supplemented = {row["source_id"] for row in self.supplement["profiles"]}
        self.assertEqual(
            missing,
            {"BIB003_PICKETT_VOCABULARIO", "BIB055_PICKETT_VOCABULARIO", "BIB059_PBK2016"},
        )
        self.assertEqual(supplemented, missing)
        self.assertFalse(self.supplement["historical_source_profile_mutated"])

    def test_pickett_source_ids_remain_distinct_and_unmerged(self):
        profiles = {row["source_id"]: row for row in self.supplement["profiles"]}
        self.assertIn("BIB003_PICKETT_VOCABULARIO", profiles)
        self.assertIn("BIB055_PICKETT_VOCABULARIO", profiles)
        self.assertNotEqual(
            profiles["BIB003_PICKETT_VOCABULARIO"]["source_id"],
            profiles["BIB055_PICKETT_VOCABULARIO"]["source_id"],
        )
        self.assertIn(
            "UNRESOLVED",
            profiles["BIB055_PICKETT_VOCABULARIO"]["relationship_to_BIB003"],
        )

    def test_verified_restricted_source_statuses_are_not_open(self):
        rights = self.source_map["rights_classification"]
        self.assertIn("NO_OPEN_LICENSE_VERIFIED", rights["BIB004_GRAMATICA_POPULAR"])
        self.assertIn("ALL_RIGHTS_RESERVED_NOTICE_OBSERVED", rights["BIB059_PBK2016"])
        self.assertIn("NO_OPEN_LICENSE_VERIFIED", rights["BIB003_PICKETT_VOCABULARIO"])

    def test_v219_inherits_mapped_source_boundaries_without_mutation(self):
        self.assertEqual(
            self.source_map_v219["database"]["sha256"],
            "c0433ff9a97fa8d4fb3d1ae5efc859b4ef2eacff1da92396fc5e8c22ff0215f4",
        )
        self.assertEqual(self.source_map_v219["database"]["sqlite_integrity_check"], "ok")
        self.assertEqual(
            self.source_map_v219["relationship_to_v2_20"]["source_bearing_shared_table_signatures"],
            "IDENTICAL_FOR_ALL_SHARED_TABLES_WITH_NONEMPTY_PROVENANCE_METADATA",
        )
        self.assertEqual(
            set(self.source_map_v219["source_profile"]["verified_missing_but_used_source_ids"]),
            {"BIB003_PICKETT_VOCABULARIO", "BIB055_PICKETT_VOCABULARIO", "BIB059_PBK2016"},
        )

    def test_cor001_replay_rights_map_preserves_analysis_target_policy(self):
        self.assertEqual(self.replay_map["cor001_policy"], "ANALYSIS_TARGET_ONLY")
        self.assertFalse(self.replay_map["benchmark_or_rule_discovery_use"])
        self.assertFalse(
            self.replay_map["cor001_rights_state"]["explicit_license_or_consent_metadata_in_audited_artifacts"]
        )
        self.assertIn(
            "DOES_NOT_PROVE_NO_PERMISSION_EXISTS",
            self.replay_map["cor001_rights_state"]["absence_interpretation"],
        )

    def test_text_bearing_cor001_artifacts_are_held_for_rights_review(self):
        rows = {Path(row["file"]).name: row for row in self.replay_map["artifacts"]}
        for name in (
            "COR001_REPLAY_INPUT_v0_2_15_2.csv",
            "COR001_REPLAY_DETAILED_v0_2_15_2.jsonl",
            "COR001_REPLAY_SUMMARY_v0_2_15_2.csv",
        ):
            self.assertIn(name, rows)
            status = rows[name]["distribution_status"]
            self.assertTrue("HOLD" in status or "REVIEW_REQUIRED" in status)
        self.assertEqual(rows["COR001_REPLAY_INPUT_v0_2_15_2.csv"]["record_count"], 107)
        self.assertEqual(rows["COR001_REPLAY_SUMMARY_v0_2_15_2.csv"]["record_count"], 107)

    def test_notice_and_current_audit_are_materialized(self):
        notice = (HERE / "THIRD_PARTY_ATTRIBUTION_v1.md").read_text(encoding="utf-8")
        audit = (HERE / "RIGHTS_PROVENANCE_AUDIT_v3.md").read_text(encoding="utf-8")
        self.assertIn("Didxazá–Spanish–English Dictionary", notice)
        self.assertIn("BIB004_GRAMATICA_POPULAR", audit)
        self.assertIn("BIB059_PBK2016", audit)
        self.assertIn("COR001_AUTHORITATIVE_RIGHTS_PROVENANCE = OPEN", audit)
        self.assertIn("BLANKET_LICENSE = BLOCKED", audit)


if __name__ == "__main__":
    unittest.main()
