import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parent
rows=list(csv.DictReader((ROOT/'ADJUDICATION_RESULTS_v0_2.csv').open(encoding='utf-8')))
assert len(rows)==3
by={r['case_id']:r for r in rows}
assert all(r['auto_correct']=='false' for r in rows)
assert all(r['native_validated']=='false' for r in rows)
assert by['FB-076']['new_status']=='OWNER_SUPPORTED_REVIEW_CANDIDATE'
assert by['FB-079']['new_status']=='PROBABLE_TRANSCRIPTION_CORRECTION'
assert by['FB-062']['new_status']=='COMPETING_SEGMENTATION_HYPOTHESES'
assert 'do not collapse' in by['FB-062']['engine_action']
print('PASS: adjudication invariants preserved')
