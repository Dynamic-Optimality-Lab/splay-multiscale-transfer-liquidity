"""New structural predicates on pinned witness states; no old words replayed."""
import json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;OLD=B.parent/'SE03_STEP2_COLD_NEG2_01'
sys.path.insert(0,str(OLD))
from source_model import core,labels
M={1,3,5,7,9,11};account={'source_engine_calls':0,'new_finite_tests':0}
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def freeze(v):return tuple(freeze(q) for q in v) if isinstance(v,list) else v
def parents(t):
    result={}
    def walk(v,p):
        if not isinstance(v,tuple):return
        k=v[0]
        if k in M:result[k]=p;p=k
        walk(v[1],p);walk(v[2],p)
    walk(t,None);return result
def main():
    controls=[]
    for q in json.loads((OLD/'symbolic_replay.json').read_text())['families']:
        controls.append((q['name'],q['rows'],q['charts']))
    p=B.parent/'SE03_STEP2_LEAF_LOWERING_03/pattern_family.json';q=json.loads(p.read_text());controls.append(('zero_restore',q['rows'],q['charts']))
    for name in ('entry_family','e1_family'):
        q=json.loads((B.parent/'SE03_STEP2_FIRST_LOWERING_04'/f'{name}.json').read_text());controls.append((name,q['rows'],q['charts']))
    checks=[]
    for name,rows,cc in controls:
        for r,c in zip(rows,cc):
            b=freeze(r['after'][1]);pa=parents(b);order=c['recent_after'];pos={k:i for i,k in enumerate(order)}
            assert set(pa)==M and all(p is None or pos[p]<pos[k] for k,p in pa.items())
            cb=core(b,M);assert labels(cb)==set(range(1,12))
            # Most recent retained key determines BE root, never its shape.
            z=3 if name in ('Omega_plus','Gamma_pair','entry_family','e1_family') else 7 if name=='Sigma_singleton' else 11
            assert r['after'][2][0]==next(k for k in order if k!=z)
        checks.append({'fixture':name,'actual_boundary_states_checked':len(rows),'recency_heap':True,
            'auxiliary_root_rule':True,'old_source_words_replayed':False})
    out('frontier_predicate_audit.json',{'status':'PASS_NEW_SOURCE_PREDICATES_ON_MANDATORY_FIXTURES','fixtures':checks,
        'proof_scope':'universal proofs in report; finite stored-state checks are controls, not their proof',**account})
    print(json.dumps({'status':'PASS_NEW_SOURCE_PREDICATES_ON_MANDATORY_FIXTURES','fixtures':checks,**account}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_frontier_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,**account})
