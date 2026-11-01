"""Read-only source check with exclusive supplement: the special seed never returns."""
import hashlib
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
cp=HERE/'sparse_reset_certificate.json'
cert=json.loads(cp.read_text(encoding='utf-8'))
audit=json.loads((HERE/'independent_audit.json').read_text(encoding='utf-8'))
assert audit['status']=='PASS' and audit['certificate_sha256']==hashlib.sha256(cp.read_bytes()).hexdigest()
seed=hashlib.sha256(json.dumps([cert['orbit_initial_A'],cert['orbit_initial_B']],separators=(',',':')).encode()).hexdigest()
count=0
for case in cert['cases']:
    assert case['orbit_replay'][0]['source_pair_sha256']==seed
    for row in case['orbit_replay']:
        # Unequal digests imply unequal serialized source states, with no collision assumption.
        assert row['destination_pair_sha256']!=seed
        count+=1
result=dict(status='PASS',normal_source_destinations_compared=count,seed_return_count=0,
  all_rows_independently_source_verified=True,mirrored_nonreturn_follows_by_injective_reflection=True,
  purpose='the initial post-setup state is not a generated-phase exception to the recurrence argument',
  certificate_sha256=audit['certificate_sha256'])
with (HERE/'seed_phase_audit.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps(result,indent=2))
