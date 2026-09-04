#!/usr/bin/env python3
"""Technical tests for the controlled Biyubi exact source layer.

These tests use synthetic rows only. The controlled 23,601-row Biyubi payload is
not stored in the public repository and is verified separately by registered
snapshot hash when mounted.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from analyzer_v0_35_3_biyubi_exact_fallback_adapter import (  # noqa: E402
    BiyubiExactFallbackAnalyzer,
)
from biyubi_exact_source import (  # noqa: E402
    BiyubiControlledSource,
    EXPECTED_NONEMPTY_ROWS,
    EXPECTED_SNAPSHOT_SHA256,
    SOURCE_ID,
    STATUS_EXACT_ENTRY,
    STATUS_EXACT_TOKEN,
    STATUS_NO_EXACT,
)


class BiyubiExactSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = BiyubiControlledSource.from_rows(
            [
                (1, "Biina ladxidua'", "Mi corazón lloró"),
                (2, "Nanna'", "Sé, lo sé, conozco"),
                (3, "Binni nayaani' xquendabiaani'", "Persona sabia"),
                (4, "mani", "animal"),
            ]
        )

    def test_registered_snapshot_contract(self):
        self.assertEqual(
            EXPECTED_SNAPSHOT_SHA256,
            "53a01c4661e465930289ff042a2def58627ab8fc26d0b812feb65b47714e3b75",
        )
        self.assertEqual(EXPECTED_NONEMPTY_ROWS, 23601)
        self.assertEqual(SOURCE_ID, "SRC-BIYUBI-DICCIONARIO-DIDXAZA-ESPANOL")

    def test_exact_entry_is_distinct_from_token_attestation(self):
        nanna = self.source.lookup("nanna'")
        self.assertEqual(nanna["biyubi_status"], STATUS_EXACT_ENTRY)
        self.assertEqual(nanna["exact_entry_count"], 1)
        self.assertEqual(nanna["exact_token_attestation_count"], 1)

        ladxidua = self.source.lookup("ladxidua'")
        self.assertEqual(ladxidua["biyubi_status"], STATUS_EXACT_TOKEN)
        self.assertEqual(ladxidua["exact_entry_count"], 0)
        self.assertEqual(ladxidua["exact_token_attestation_count"], 1)

    def test_outer_sentence_punctuation_and_case_do_not_block_exact_match(self):
        result = self.source.lookup("NANNA',")
        self.assertEqual(result["biyubi_status"], STATUS_EXACT_ENTRY)
        self.assertEqual(result["exact_entry_count"], 1)

    def test_tones_diacritics_and_apostrophe_codepoints_are_not_stripped(self):
        self.assertEqual(self.source.lookup("nánna'")["biyubi_status"], STATUS_NO_EXACT)
        self.assertEqual(self.source.lookup("nanna")["biyubi_status"], STATUS_NO_EXACT)
        self.assertEqual(self.source.lookup("nanna’")["biyubi_status"], STATUS_NO_EXACT)

    def test_no_near_match(self):
        self.assertEqual(self.source.lookup("ladxidua")["biyubi_status"], STATUS_NO_EXACT)
        self.assertEqual(self.source.lookup("binebiaya'")["biyubi_status"], STATUS_NO_EXACT)

    def test_source_policy_is_non_normative(self):
        row = self.source.lookup("mani")
        self.assertFalse(row["generation_license_assertion"])
        self.assertFalse(row["correction_assertion"])
        self.assertFalse(row["orthographic_authority_assertion"])
        self.assertFalse(row["rule_discovery_assertion"])
        self.assertFalse(row["match_contract"]["near_match"])
        self.assertFalse(row["match_contract"]["strip_tone"])
        self.assertFalse(row["match_contract"]["pdlma_to_surface"])


class _FakeBaseAnalyzer:
    def __init__(self):
        self.retrieval = object()
        self.bound = object()
        self.morph2 = object()
        self.morph1 = object()
        self.db = object()
        self.verb_meta = {}
        self.person_exact = []
        self.runtime_root = Path(".")
        self.sqlite_path = Path("fake.sqlite")
        self.verb_inventory_path = Path("fake.csv")
        self.closed = False

    def close(self):
        self.closed = True

    def analyze(self, surface, **kwargs):
        tokens = surface.split()
        return {
            "analysis_status": "ABSTAIN_NO_COMPONENT_EVIDENCE",
            "analysis_status_promotion_basis": None,
            "surface_original": surface,
            "token_count": len(tokens),
            "matched_token_count": 0,
            "matched_token_indexes": [],
            "effective_evidence_token_indexes": [],
            "effective_evidence_token_count": 0,
            "effective_evidence_coverage_ratio": 0.0,
            "unresolved_token_indexes_after_exact_fallback": list(range(len(tokens))),
            "fallback_policy": {
                "matched_token_count_not_inflated_by_fallback": True,
                "unresolved_not_incorrect": True,
            },
            "limitations": [],
            "generation_license_assertion": False,
            "correction_assertion": False,
            "orthographic_authority_assertion": False,
            "rule_discovery_assertion": False,
        }


class BiyubiFallbackWrapperTests(unittest.TestCase):
    def test_unmounted_source_preserves_existing_analysis(self):
        engine = BiyubiExactFallbackAnalyzer(_FakeBaseAnalyzer(), None)
        result = engine.analyze("nanna' binebiaya'")
        self.assertEqual(result["current_adapter_version"], "0.35.3")
        self.assertEqual(result["biyubi_source_status"], "NOT_MOUNTED")
        self.assertEqual(result["analysis_status"], "ABSTAIN_NO_COMPONENT_EVIDENCE")
        self.assertEqual(result["effective_evidence_after_biyubi_token_count"], 0)
        self.assertEqual(result["unresolved_token_indexes_after_biyubi"], [0, 1])

    def test_mounted_source_adds_only_exact_secondary_evidence(self):
        source = BiyubiControlledSource.from_rows(
            [(1, "Nanna'", "Sé, lo sé, conozco")]
        )
        engine = BiyubiExactFallbackAnalyzer(_FakeBaseAnalyzer(), source)
        result = engine.analyze("nanna' binebiaya'")

        self.assertEqual(result["biyubi_source_status"], "MOUNTED_REGISTERED_SNAPSHOT")
        self.assertEqual(result["biyubi_exact_attested_token_indexes"], [0])
        self.assertEqual(result["unresolved_token_indexes_after_biyubi"], [1])
        self.assertEqual(result["effective_evidence_after_biyubi_token_count"], 1)
        self.assertEqual(result["analysis_status"], "PARTIAL_ANALYSIS_NON_LICENSING")
        self.assertEqual(
            result["analysis_status_promotion_basis"],
            "BIYUBI_EXACT_SECONDARY_ATTESTATION_ONLY",
        )
        self.assertFalse(result["orthographic_authority_assertion"])
        self.assertTrue(
            result["fallback_policy"]["biyubi_attestation_not_orthographic_authority"]
        )
        self.assertTrue(result["fallback_policy"]["biyubi_absence_not_incorrect"])


if __name__ == "__main__":
    unittest.main()
