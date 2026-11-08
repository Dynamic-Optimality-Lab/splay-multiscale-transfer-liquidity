"""Independent append-only source/causal audit of the first sparse advance."""
import hashlib,json,pickle,sys,time
from pathlib import Path
from audit_verify36 import calc
from interior_projection_source_tools import fr,isnode,known,projections
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def pre(t):return () if not isnode(t) else (t[0],)+pre(t[1])+pre(t[2])
def main():
    with (B/'full_geometry_sparse_work_00.pkl').open('rb') as f:old=pickle.load(f)
    with (B/'full_geometry_sparse_work_01.pkl').open('rb') as f:new=pickle.load(f)
    pin=json.loads((B/'sparse_conversion_values_independent_audit.json').read_text());assert hashlib.sha256((B/'full_geometry_sparse_work_00.pkl').read_bytes()).hexdigest()==pin['input_sha256']['full_geometry_sparse_work_00.pkl']
    assert json.loads((B/'sparse_source_conversion_independent_audit.json').read_text())['status']=='PASS_EXACT_SPARSE_SOURCE_PREFIX_CONVERSION'
    Z=json.loads((B/'native10_source_actions.json').read_text());N=len(Z['trees']);mir=Z['mirror'];T=list(map(fr,Z['trees']));idx={t:i for i,t in enumerate(T)};O=pickle.loads((B/'native10_B_modal_factored_debt.pkl').read_bytes())
    def D(a,b):return O['base'][b]+O['residual'].get(min(a*N+b,mir[a]*N+mir[b]),0)
    n0=len(old['updates']);assert new['updates'][:n0]==old['updates'] and new['A'][:len(old['A'])]==old['A']
    geom={pre(t):i for i,t in enumerate(new['A'])};assert len(geom)==len(new['A'])
    low=dict(old['lower']);pred=dict(old['pred']);identities={};fixed={};checked=0
    def unary(t):
        key=pre(t)
        if key not in fixed:
            v=t
            while v[0]!=5:v=v[1 if 5<v[0] else 2]
            if isnode(v[1]) and isnode(v[2]):fixed[key]=None
            else:
                pi=projections(t,5);assert len(pi)==1;fixed[key]=idx[pi[0]]
        return fixed[key]
    for j in range(n0,len(new['updates'])):
        r=new['updates'][j];e=r['edge'];a=geom[pre(e['source_A'])];at=geom[pre(e['actual_A_target'])];b=e['source_B_core_index'];bt=e['B_target_core_index'];x=e['target_actual_key'];helper=e.get('DELETE_helper');key=pre(e['source_A']),helper,x
        assert e['source_A'][0]//2==T[b][0] and x!=e['source_A'][0] and bt==Z['destination'][b][x//2-1] and e['Q']==Z['Q'][b][x//2-1]
        if key not in identities:
            t=e['source_A'];h=0
            if helper is not None:t,c=calc(t,helper);h+=c;assert c==1
            t,c=calc(t,x);h+=c
            assert h==e['H'] and pre(t)==pre(e['actual_A_target']) and e['price']==2*h-e['Q'];identities[key]=True
        sf=unary(e['source_A']);tf=unary(e['actual_A_target']);assert tf is None
        sc=None if sf is not None else a*N+b;tc=at*N+bt;sv=D(sf,b) if sf is not None else low.get(sc,0)
        assert r['source_code']==sc and r['target_code']==tc and r['source_lower']==sv and r['parent']==(None if sc is None else pred.get(sc))
        assert r['new_lower']==sv-e['price'] and r['new_lower']>low.get(tc,0)
        low[tc]=r['new_lower'];pred[tc]=j;checked+=1
        if checked%1024==0 and time.process_time()-START>CAP-2:raise TimeoutError('SPARSE_CAUSAL_AUDIT_CAP')
    assert low==new['lower'] and pred==new['pred'] and max(low.values())==3 and new['counter'] is None
    files=('SPARSE_SOURCE_REGENERATION.md','full_geometry_sparse_solver.py','full_geometry_sparse_work_01.pkl','full_geometry_sparse_result_01.json','sparse_source_conversion_independent_audit.json','audit_verify70.py')
    receipt={'status':'PASS_SPARSE_SOURCE_ADVANCE_CAUSAL_LOWER_BOUNDS','new_causal_updates':checked,'distinct_formal_source_identities':len(identities),'old_causal_records_reused':n0,'positive_labels':len(low),'new_A_shapes':len(new['A'])-len(old['A']),'maximum_lower_label':3,'source_prefix_complete':False,'discovery_feasibility_not_proved':True,'fresh_concrete_source_queries':0,'source_queries':0,'source_engine_calls':0,'principal_U33':'OPEN','input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in files}}
    assert time.process_time()-START<CAP-1
    out('sparse_source_advance_01_independent_audit.json',receipt);print(json.dumps({k:v for k,v in receipt.items() if k!='input_sha256'}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify70_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
