import unittest,sqlite3
from pathlib import Path
DB=Path(__file__).with_name('BASE_CORRECTOR_DIDXAZA_EVIDENCE_INTEGRITY_v2_19.sqlite')
class SchemaTests(unittest.TestCase):
 def setUp(self):self.c=sqlite3.connect(DB)
 def tearDown(self):self.c.close()
 def test_integrity(self):self.assertEqual(self.c.execute('pragma integrity_check').fetchone()[0],'ok')
 def test_no_fk_violations(self):self.assertEqual(self.c.execute('pragma foreign_key_check').fetchall(),[])
 def test_runtime_version(self):self.assertEqual(self.c.execute("select value from canonical_state_v16 where key='runtime_version'").fetchone()[0],'0.2.15.2')
 def test_fix_registry(self):self.assertEqual(self.c.execute('select count(*) from evidence_integrity_fix_registry_v02152').fetchone()[0],10)
 def test_p0_fixed(self):self.assertEqual(self.c.execute("select count(*) from evidence_integrity_fix_registry_v02152 where severity='P0' and status='FIXED'").fetchone()[0],3)
 def test_replay_107(self):self.assertEqual(self.c.execute('select count(*) from cor001_replay_v02152').fetchone()[0],107)
 def test_replay_core(self):
  self.assertEqual(self.c.execute('select sum(orthographic_unresolved_tokens),sum(candidate_edits),sum(utterance_validation) from cor001_replay_v02152').fetchone(),(128,0,0))
 def test_analysis_visibility(self):
  self.assertEqual(self.c.execute('select sum(analysis_open_tokens),sum(analysis_review_tokens) from cor001_replay_v02152').fetchone(),(129,2))
 def test_migration_recovery_present(self):
  self.assertEqual(self.c.execute("select count(*) from schema_migration_log where migration_id='MIG-v2.16-v2.17-person-possession-AUDIT-RECOVERY'").fetchone()[0],1)
 def test_repair_migration_present(self):
  self.assertEqual(self.c.execute("select count(*) from schema_migration_log where migration_id='MIG-v2.18-v2.19-evidence-integrity-repair'").fetchone()[0],1)
 def test_hard_flags(self):
  d=dict(self.c.execute("select key,value from canonical_state_v16 where key in ('auto_correct_enabled','orthographic_suggestions_enabled','edit_execution_enabled')"))
  self.assertEqual(set(d.values()),{'NO'})
if __name__=='__main__':unittest.main()
