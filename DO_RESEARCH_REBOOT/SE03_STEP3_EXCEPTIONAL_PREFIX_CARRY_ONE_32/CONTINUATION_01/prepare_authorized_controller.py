"""Metadata-only resource amendment and first exact bounded batch wrappers."""
import json,ast
from pathlib import Path
B=Path(__file__).resolve().parent
def write(n,s):
    with (B/n).open('x',encoding='utf-8') as f:f.write(s)
e=json.loads((B/'entry.json').read_text());am=json.loads((B/'resource_amendment.json').read_text())
assert am['user_answer_verbatim']=='Authorize the bounded query increase' and am['usage_reset'] is False
v=dict(e);v['remaining_conservative_queries']=am['new_cumulative_query_cap']-e['inherited_conservative_queries']
v['query_limit']=am['new_cumulative_query_cap'];v['phase_query_caps']=dict(e['phase_query_caps'],cold=50000,verify=50000)
v['resource_amendment']='resource_amendment.json'
write('entry_authorized.json',json.dumps(v,indent=2))
source=(B/'run_phase.py').read_text().replace("B/'entry.json'","B/'entry_authorized.json'")
write('run_phase_authorized.py',source)
for backend,phase in [('producer','cold001'),('independent','verify001')]:
    body='import sys\nfrom cold_frames import run\nrun('+repr(backend)+',0,50,'+repr(phase)+',float(sys.argv[1]),int(sys.argv[2]))\n'
    ast.parse(body);write('audit_'+phase+'.py',body)
ast.parse((B/'cold_frames.py').read_text())
print(json.dumps({'status':'AUTHORIZED_CONTROLLER_READY','cumulative_query_limit':v['query_limit'],'new_allowance':v['remaining_conservative_queries'],'per_batch':50000,'CPU_caps_unchanged':v['group_caps']}),flush=True)
