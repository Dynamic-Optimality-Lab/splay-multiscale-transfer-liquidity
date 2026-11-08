"""Checkpoint actual eight-mark SS B transitions for a bounded source falsifier."""
import hashlib,importlib.util,json,pickle,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;B=F.parents[1]/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
sys.path.insert(0,str(F));import ranked_source_bst as R
CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);PHASE=sys.argv[3];BATCH=int(sys.argv[4]);START=time.process_time();V=None
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def loadmod(name,p):
    sp=importlib.util.spec_from_file_location(name,p);z=importlib.util.module_from_spec(sp);sp.loader.exec_module(z);return z
def main():
    global V
    grammar=loadmod('B8_static_grammar_only',F/'build_B_grammar.py');trees=grammar.T(8,1);assert len(trees)==21318 and len(set(trees))==21318
    index={t:i for i,t in enumerate(trees)}
    with (F/'probe11_source_actions.pkl').open('rb') as f:old=pickle.load(f)
    V=loadmod('B8_actual_new_primitives',B/'audit_core39.py');V.CAP=CAP;V.START=START;V.QCAP=QCAP;V.CALLS=0
    fresh={};rows=[];start=0
    if BATCH>1:
        with (F/f'eight_core_B_source_{BATCH-1:02d}.pkl').open('rb') as f:z=pickle.load(f)
        assert z['trees']==trees;fresh=z['fresh'];rows=z['rows'];start=z['next_source']
    def kernel(t,n,x):
        k=(t,n,x)
        if k not in fresh:
            assert V.CALLS<QCAP
            after,h,q,_=V.splay(t,x,False);fresh[k]=(after,h,q)
        return fresh[k]
    lift=R.Lift(old,kernel);i=start
    while i<len(trees) and time.process_time()-START<CAP-4:
        t=trees[i];local=[]
        for x in range(1,16,2):
            if x==t[0]:continue
            u=t;path=[]
            while True:
                path.append(u[0])
                if u[0]==x:break
                u=u[1] if x<u[0] else u[2]
            if len(path)%2==0:continue
            if any(g%2==0 or p%2!=0 or (x<g)!=(x<p) for g,p in zip(path[:-1:2],path[1:-1:2])):continue
            out,h,q=lift.action(t,15,x);assert h==q==(len(path)-1)//2 and out in index
            local.append((i,index[out],x,q))
        rows.extend(local);i+=1
        assert 646646+2*len(index)+len(rows)+len(fresh)+22000+100000<2000000
    out={'status':'PRODUCER_B8_SS_TABLE_COMPLETE' if i==len(trees) else 'CHECKPOINT','trees':trees,'rows':rows,'next_source':i,'fresh':fresh,
      'source_queries':V.CALLS,'source_engine_calls':V.CALLS,'cached_leaf_substitutions':lift.substitutions,
      'source_admissibility':'actual ordinary SS edges only; no all-static-tree realization claim','JR35':'OPEN',
      'input_sha256':{str(p):sha(p) for p in (F/'build_B_grammar.py',F/'probe11_source_actions.pkl',F/'independent_probe11_source_actions.json',B/'OFF_PATH_LEAF_SOURCE_LIFT.md',F/'build_eight_core_source_falsifier.py')}}
    with (F/f'eight_core_B_source_{BATCH:02d}.pkl').open('xb') as f:pickle.dump(out,f,protocol=5)
    report={k:v for k,v in out.items() if k not in ('trees','rows','fresh')};report.update({'states':len(trees),'edges':len(rows),'fresh_bindings':len(fresh)})
    with (F/f'eight_core_B_source_{BATCH:02d}.json').open('x',encoding='utf8') as f:json.dump(report,f,indent=2)
    print(json.dumps(report),flush=True);assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        calls=0 if V is None else V.CALLS
        with (B/f'audit_{PHASE}_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':calls,'source_engine_calls':calls},f)
