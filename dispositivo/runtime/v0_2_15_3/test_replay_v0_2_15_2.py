import unittest,csv,json
from pathlib import Path
ROOT=Path(__file__).parent
M=json.loads((ROOT/'COR001_REPLAY_METRICS_v0_2_15_2.json').read_text())
MAN=json.loads((ROOT/'RUN_MANIFEST_COR001_v0_2_15_2.json').read_text())

class ReplayTests(unittest.TestCase):
    def test_rows(self): self.assertEqual(M['rows'],107)
    def test_actions_match_v0215(self): self.assertEqual(M['actions'],{'RT-B-PARTIAL':75,'RT-E-PRESERVE':32})
    def test_unresolved_match_v0215(self): self.assertEqual(M['orthographic_unresolved_total'],128)
    def test_accepted_match_v0215(self): self.assertEqual(M['accepted_exact_spans_total'],190)
    def test_analysis_vectors_cover_all_tokens(self):
        self.assertEqual(M['analysis_vector_scope'],'ALL_TOKENS_NOT_ONLY_ORTHOGRAPHIC_UNRESOLVED')
        self.assertEqual(M['analysis_open_total'],129)
        self.assertEqual(M['analysis_review_total'],2)
    def test_qualification_totals_match_v0215(self):
        self.assertEqual(M['qualification_totals'],{'NONE':86,'HYPOTHESIS_ONLY':31,'RETRIEVAL_ONLY':8,'ANALYSIS_POSITIVE':3})
    def test_no_named_dictionaria_coverage_scope(self): self.assertEqual(M['dictionaria_named_scope_claims'],0)
    def test_no_combined_three_community_scope(self):
        self.assertNotIn('LA_VENTOSA|JUCHITAN|SANTA_MARIA_XADANI',M['claim_scope_counts'])
    def test_hard_safety(self):
        self.assertEqual(M['candidate_edits_total'],0);self.assertEqual(M['utterance_validations_total'],0)
        self.assertFalse(M['auto_correct_enabled']);self.assertFalse(M['visible_suggestions_enabled']);self.assertFalse(M['edit_execution_enabled'])
    def test_manifest_has_all_source_checksums(self):
        keys=set(MAN['checksums'])
        self.assertTrue({'cor001_input','dictionaria_entries','dictionaria_senses','dictionaria_examples','pickett_backfill','documentary_alignment_registry','person_possession_registry','repair_runtime'} <= keys)
    def test_source_coverage_separate_in_details(self):
        first=json.loads((ROOT/'COR001_REPLAY_DETAILED_v0_2_15_2.jsonl').read_text(encoding='utf-8').splitlines()[0])
        self.assertEqual(first['source_coverage_metadata']['BIB054_DICTIONARIA'],['LA_VENTOSA','JUCHITAN','SANTA_MARIA_XADANI'])
        self.assertEqual(first['dialect_scope_policy'],'INDIVIDUAL_EVIDENCE_UNKNOWN_UNLESS_EXPLICIT_MAPPING')
    def test_summary_107_and_no_validation(self):
        with (ROOT/'COR001_REPLAY_SUMMARY_v0_2_15_2.csv').open(encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
        self.assertEqual(len(rows),107);self.assertTrue(all(r['utterance_validation']=='False' for r in rows))

if __name__=='__main__':unittest.main()
