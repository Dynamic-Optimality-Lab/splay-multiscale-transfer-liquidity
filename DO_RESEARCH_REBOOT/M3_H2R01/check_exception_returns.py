"""Finite B-only closure test of the three failed fringe kernels through negative runs."""
import json,itertools,time
from pathlib import Path
BASE=Path('DO_RESEARCH_REBOOT/M3_H2R01');OUT=BASE/'exception_returns.json'
def main():
    assert not OUT.exists();start=time.process_time()
    failures=json.loads((BASE/'fringe_kernel_certificate.json').read_text())['failures']
    c=json.loads(Path('DO_RESEARCH_REBOOT/M3_LDR01/negative_run_census.json').read_text())
    out=[[] for _ in c['nodes']]
    for e in c['edges']:out[e['source']].append(e)
    returns=[];best={};queries=0
    for i,f in enumerate(failures):
        stack=[(f['exit_core'],[],0)]
        while stack:
            node,path,deficit=stack.pop();queries+=1
            for j,g in enumerate(failures):
                if node==g['entry_core']:
                    r={'from_exception':i,'to_exception':j,'negative_return':path,
                       'return_deficit':deficit,'block_weight':f['w']-deficit}
                    returns.append(r);key=(i,j)
                    if key not in best or r['block_weight']<best[key]['block_weight']:best[key]=r
            if len(path)<2:
                for e in out[node]:stack.append((e['destination'],path+[e],deficit+e['deficit']))
    cycles=[]
    for k in (1,2,3):
        for order in itertools.permutations(range(len(failures)),k):
            if order[0]!=min(order):continue
            pairs=list(zip(order,order[1:]+order[:1]))
            if all(p in best for p in pairs):
                links=[best[p] for p in pairs];weight=sum(r['block_weight'] for r in links)
                if weight<0:cycles.append({'exceptions':order,'links':links,'weight':weight,'scope':'B-only candidate; A/full-state lifting required'})
    result={'status':'COMPLETE','return_states_checked':queries,'returns':returns,
            'negative_B_cycle_candidates':cycles,'cpu_seconds':round(time.process_time()-start,3),
            'scope':'only the three H2 exceptions joined by strictly negative low runs, not arbitrary helper/high returns'}
    with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result),flush=True)
if __name__=='__main__':main()
