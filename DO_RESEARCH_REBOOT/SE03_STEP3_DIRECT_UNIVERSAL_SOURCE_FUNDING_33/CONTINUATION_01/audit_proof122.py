"""Test geometric extremal contractions, not extrema of debt values."""
import json,pickle,time,sys,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def fr(t):return tuple(map(fr,t)) if isinstance(t,list) else t
def pre(t):return () if not isinstance(t,tuple) else (t[0],)+pre(t[1])+pre(t[2])
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    Z=json.loads((B/'native10_source_actions.json').read_text());N=len(Z['trees']);mir=Z['mirror'];order=[pre(fr(t)) for t in Z['trees']];assert order==sorted(order)
    O=pickle.loads((B/'native10_B_modal_factored_debt.pkl').read_bytes());D=lambda a,b:O['base'][b]+O['residual'].get(min(a*N+b,mir[a]*N+mir[b]),0)
    with (B/'full_geometry_work_02.pkl').open('rb') as f:w=pickle.load(f)
    bad={};checked=0
    for e in w['edges'].values():
        for name,pick in (('lexicographically_first',min),('lexicographically_last',max)):
            if name in bad:continue
            a=pick(e['source_contraction_indices']);at=pick(e['target_contraction_indices']);ds=D(a,e['source_B_core_index']);dt=D(at,e['B_target_core_index'])
            if e['price']+dt-ds<0:r=e.copy();r.update(projection_rule=name,old_source_A_index=a,old_projected_target_index=at,D_source=ds,D_target=dt,signed_margin=e['price']+dt-ds);bad[name]=r
        checked+=1
        if len(bad)==2:break
        if time.process_time()-START>CAP-4:break
    out('extremal_full_geometry_contraction_candidates.json',{'status':'BOTH_GEOMETRIC_EXTREMAL_SELECTORS_REFUTED_RAW' if len(bad)==2 else 'GEOMETRIC_EXTREMAL_DISCOVERY_OPEN','failures':bad,'source_constraints_read':checked,'not_debt_value_extrema':True,'closed_source_embedding':'PENDING for new failures; prior matching sources may be reused','source_queries':0,'source_engine_calls':0,'principal_U33':'OPEN'});print(json.dumps({'status':'GEOMETRIC_SELECTOR_DISCOVERY','read':checked,'failures':{k:{x:e[x] for x in ('H','Q','price','D_source','D_target','signed_margin')} for k,e in bad.items()}}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof122_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
