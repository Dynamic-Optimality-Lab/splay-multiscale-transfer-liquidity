"""Exact zero-H1 closure and explicit one-unit repair of the H2 fringe kernels."""
import sys,json,time,hashlib
from pathlib import Path
from collections import deque,Counter
from functools import lru_cache
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_H2R01','DO_RESEARCH_REBOOT/M3_PHI01','python/independent']
import splay as S
from terminal_potential import CappedPotential
BASE=Path('DO_RESEARCH_REBOOT/M3_FRC01');OUT=BASE/'compensation_certificate.json'
@lru_cache(None)
def all_trees(a,b):
    if a==b:return (S.LEAF,)
    return tuple(S.node(k,l,r) for k in range(a,b) for l in all_trees(a,k) for r in all_trees(k+1,b))
def main():
    assert not OUT.exists();start=time.process_time();P=CappedPotential()
    assert len(P.trees)==4862 and set(P.trees)==set(all_trees(0,9))
    kernel=json.loads(Path('DO_RESEARCH_REBOOT/M3_H2R01/fringe_kernel_certificate.json').read_text())
    failures=kernel['failures'];seeds=sorted({r['exit_core'] for r in failures})
    assert seeds==[1917,1937,2141] and all(P.psi[u]==0 for u in seeds)
    R=set(seeds);queue=deque(seeds);rows=[];parent={u:None for u in seeds}
    while queue:
        u=queue.popleft();t=P.trees[u]
        for x in range(9):
            h=S.lookup(t,x)[1];v=P.ids[S.trace(t,x)[0]];w=2-h//2
            row={'source':u,'target':x,'destination':v,'depth':h,'w':w,'psi_source':P.psi[u],'psi_destination':P.psi[v]}
            rows.append(row)
            if w==0 and P.psi[v]==0 and v not in R:
                R.add(v);queue.append(v);parent[v]={'source':u,'target':x}
        assert len(rows)<=43758 and time.process_time()-start<120,'UNKNOWN: basin cap'
    bad_depth=[r for r in rows if r['depth']>=6]
    if bad_depth:
        result={'status':'REFUTED_DEPTH_INVARIANT','R':sorted(R),'bad_rows':bad_depth,'rows':rows,
                'cpu_seconds':round(time.process_time()-start,3)}
        with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
        print(json.dumps({k:v for k,v in result.items() if k!='rows'}),flush=True);return
    def val(i):return -P.psi[i]-int(i in R)
    for r in rows:
        assert P.psi[r['source']]==0 and r['w']>=0
        assert r['w']!=0 or P.psi[r['destination']]>=1 or r['destination'] in R
        r['new_source']=val(r['source']);r['new_destination']=val(r['destination'])
        r['reduced_weight']=r['w']-r['new_destination']+r['new_source']
        assert r['reduced_weight']>=0,r
    h2rows=[];counts=Counter()
    for r in kernel['rows']:
        if not r['gap0_childless_at_exit']:continue
        u=r['entry_core'];v=r['exit_core'];a=val(u);b=val(v);red=r['w']-b+a
        assert -2<=a<=0 and -2<=b<=0 and red>=0,r
        if r['w']==0:assert P.psi[v]>=1
        h2rows.append({'entry_core':u,'target':r['target'],'exit_core':v,'q':r['q'],'w':r['w'],
                       'new_source':a,'new_destination':b,'reduced_weight':red})
        counts[str(r['w'])]+=1
    terminal=[]
    for e in json.loads(Path('DO_RESEARCH_REBOOT/M3_LDR01/negative_run_census.json').read_text())['edges']:
        q=e['depth']//2;v=e['destination'];assert P.psi[v]>=q-2
        assert val(v)<=2-q
        terminal.append({'preterminal':e['source'],'target':e['target'],'destination':v,
                         'q':q,'new_destination':val(v),'H2_weight':4-q,'minimum_source_value':-2,
                         'worst_case_reduced_weight':4-q-val(v)-2})
        assert terminal[-1]['worst_case_reduced_weight']>=0
    fixed=[]
    for f in failures:
        u=f['entry_core'];v=f['exit_core']
        assert u not in R and v in R and val(u)==-2 and val(v)==-1
        fixed.append({**f,'new_source':val(u),'new_destination':val(v),'new_reduced_weight':f['w']-val(v)+val(u)})
        assert fixed[-1]['new_reduced_weight']==0
    node_rows=[{'id':u,'tree':S.serial(P.trees[u]),'psi':P.psi[u],
                'maximum_core_depth':max(S.lookup(P.trees[u],x)[1] for x in range(9)),
                'discovered_from':parent[u],'core_root':P.trees[u][1]} for u in sorted(R)]
    result={'status':'COMPLETE','ordered_core_trees':4862,'seed_ids':seeds,'R':sorted(R),'R_nodes':node_rows,
            'R_access_queries':len(rows),'maximum_depth_in_R':max(r['depth'] for r in rows),
            'all_R_H1_accesses_repaid':True,'zero_psi_zero_cost_closure':True,
            'retained_H2_fringe_rows':len(h2rows),'H2_weight_counts':dict(counts),
            'all_retained_H2_fringe_rows_pass':True,'Gamma0_cheap_terminal_rows':len(terminal),
            'fixed_exceptions':fixed,'h1_rows':rows,'h2_fringe_rows':h2rows,'Gamma0_terminal_rows':terminal,
            'new_range':[-2,0],'patch_scope':'chi8, sigma[0]>0, core_id in R',
            'old_CHR01_signature_zero_untouched':True,'cpu_seconds':round(time.process_time()-start,3)}
    assert result['cpu_seconds']<120
    with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k not in ('h1_rows','h2_fringe_rows','Gamma0_terminal_rows')},indent=2),flush=True)
if __name__=='__main__':main()
