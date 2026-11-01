"""Scope check on already independently verified B rows; no new source requests."""
import hashlib
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
cp=HERE/'guarded_B_cycle_certificate.json'
cert=json.loads(cp.read_text(encoding='utf-8'))
audit=json.loads((HERE/'independent_audit.json').read_text(encoding='utf-8'))
assert audit['status']=='PASS' and audit['certificate_sha256']==hashlib.sha256(cp.read_bytes()).hexdigest()
rows=cert['selected_cycle']['full_cycle_replay'];profile=[]
for i in range(0,len(rows),2):
    x,r=rows[i:i+2]
    assert x['source_B'][0]==13 and x['key']<13 and r['key']==13
    assert x['destination_B']==r['source_B'] and 1<=r['d_B']<=2 and r['q']<=1
    profile.append(dict(query_occurrence=i,query_key=x['key'],query_q=x['q'],guard_occurrence=i+1,
      guard_q=r['q'],guard_depth=r['d_B'],minimum_guard_capacity=2,guaranteed_spare_if_query_positive=2-r['q'],
      residual_upper=max(x['q']+r['q']-4,0)))
H=sum(v['residual_upper'] for v in profile)
assert H==1
result=dict(status='PASS',B_G=audit['selected_G_B'],H_B=H,profile=profile,A_source_cases_executed=0,
  new_source_calls=0,two_one_StepEv_pure_reset_capacity=4,
  coupling_consequence='GB03 proves UD coverage when C_D>=H_B on this guarded cycle',
  B_headroom_target='ACHIEVED',strict_FI_only_reset_coupling='NOT ESTABLISHED; pure-reset coupling obstructed',
  certificate_sha256=audit['certificate_sha256'])
with (HERE/'guard_repayment_profile.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({k:v for k,v in result.items() if k!='profile'},indent=2))
