"""Targeted residual dirty-edge probe: predecessor of a left sentinel claimant."""
import sys,json,time
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'DO_RESEARCH_REBOOT/M2_SEP01'))
from experiment import annotate,edge,chi
OUT=Path('DO_RESEARCH_REBOOT/M2_DSK01/left_successor_probe.json')
assert not OUT.exists()
rows=[];valid=[];start=time.process_time()
for x in range(8):
    c=x+1
    raw={'root':x,'kl':[2]*19,'rl':[19]*19,'kr':[2]*19,'rr':[19]*19}
    for i in range(1,x+1):raw['kl'][i]=0;raw['rl'][i]=i-1
    for i in range(x,8):raw['kr'][i]=0;raw['rr'][i]=i+1
    raw['kl'][c]=0;raw['rl'][c]=19
    state=annotate(raw);assert state
    for length in range(14,19):
        e,status=edge(state,x,length)
        rows.append({'target':x,'claimant':c,'d':length,'status':status})
        if e:valid.append(e)
result={'status':'COMPLETE','cases':len(rows),'valid_negative_edges':len(valid),
        'cpu_seconds':round(time.process_time()-start,3),'rows':rows,'edges':valid}
with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
print(json.dumps({k:v for k,v in result.items() if k not in ('rows','edges')}),
      'valid_cases',json.dumps([r for r in rows if r['status']=='VALID']),flush=True)

