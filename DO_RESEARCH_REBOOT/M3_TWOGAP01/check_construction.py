"""Construction-side residual check; independent certification is still step3."""
import json,time,hashlib
from pathlib import Path
from collections import Counter
from prefix_profiles import BASE
def main():
    start=time.process_time();out=BASE/'construction_check.json';assert not out.exists()
    c=json.loads((BASE/'relation.json').read_text());p=json.loads((BASE/'potential_sparse.json').read_text());N=c['classes'];labels={int(k):v for k,v in p['labels'].items()}
    bc=json.loads(Path('DO_RESEARCH_REBOOT/M3_LDR01/negative_run_census.json').read_text());psi=[r['psi'] for r in bc['nodes']];roots=[r['tree'][0] for r in bc['nodes']]
    cc=json.loads(Path('DO_RESEARCH_REBOOT/M3_H1F01/cheap_census.json').read_text());K=json.loads(Path('DO_RESEARCH_REBOOT/M3_H2R01/fringe_kernel_certificate.json').read_text())
    h2={(r['entry_core'],r['target']):(r['exit_core'],r['w']) for r in K['rows'] if r['gap0_childless_at_exit']}
    byroot={r:[] for r in range(9)}
    for a,s in enumerate(c['shadows']):byroot[s[0][2]].append(a)
    for k,v in labels.items():
        b,a=divmod(k,N);assert -2<=v<=-psi[b] and c['shadows'][a][0][2]==roots[b]
    checked=0;analytic=Counter();hist=Counter();minimum=10;nodes=0
    for b in range(4862):
        for a in byroot[roots[b]]:
            key=b*N+a;du=labels.get(key,-psi[b]);nodes+=1
            if du==0:
                # Every negative H1 destination has psi>=-w; H2 w>=0.
                analytic['zero_source_states']+=1;continue
            for o in c['options'][a]:
                if o['H']==1:
                    h=cc['B_depth'][b][o['target']]
                    if not h:analytic['nongenuine']+=1;continue
                    bb=cc['B_destination'][b][o['target']];w=2-h//2
                else:
                    z=h2.get((b,o['target']))
                    if z is None:analytic['nonchildless_exit']+=1;continue
                    bb,w=z
                if w>=2:analytic['range']+=1;continue
                dv=labels.get(bb*N+o['destination'],-psi[bb]);res=w-dv+du
                assert res>=0,(b,a,o,du,dv,w);hist[res]+=1;minimum=min(minimum,res);checked+=1
            assert time.process_time()-start<300,'UNKNOWN construction check CPU cap'
    for b in range(4862):
        for x in range(9):
            h=cc['B_depth'][b][x];bb=cc['B_destination'][b][x];w=2-h//2
            if w<0:assert -psi[bb]<=w
    assert all(w>=0 for bb,w in h2.values())
    result={'status':'FINITE_EXACT_CONSTRUCTION_SIDE_PASS','synchronized_product_states':nodes,'explicit_residuals':checked,
      'minimum_residual':minimum,'residual_histogram':dict(hist),'analytic':dict(analytic),
      'changed_states':len(labels),'range':[-2,0],'potential_sha256':hashlib.sha256((BASE/'potential_sparse.json').read_bytes()).hexdigest(),
      'cpu_seconds':round(time.process_time()-start,3),'independent_certification_complete':False,'full_M3_proved':False}
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':main()
