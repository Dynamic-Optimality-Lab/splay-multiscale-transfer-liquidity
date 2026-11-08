"""Mine literal zero-cost full-pair cycles; a passing search proves nothing.

Exact rank endpoints, KEEP/DELETE commands and source costs are retained.
Zero reduced cost implies exact total Q=2A on every extracted cycle.
"""
import gc,hashlib,importlib.util,json,pickle,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
sys.path.insert(0,str(F));import ranked_source_bst as R
CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();PHASE=sys.argv[3];BATCH=int(sys.argv[4]);V=None
class StopQueries(Exception):pass
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    global V
    bp=F/'full_source13_beam_05.pkl'
    if BATCH==1:
        with bp.open('rb') as f:z=pickle.load(f)
        records=z['records'];fresh=z['fresh'];keys=sorted(records);i=0;edges=[];del z
    else:
        with (F/f'source13_tight_graph_{BATCH-1:02d}.pkl').open('rb') as f:z=pickle.load(f)
        records=z['records'];fresh=z['fresh'];keys=z['keys'];i=z['next_source'];edges=z['edges'];del z
    index={k:j for j,k in enumerate(keys)};N=len(keys)
    with (F/'probe11_source_actions.pkl').open('rb') as f:old=pickle.load(f)
    sp=importlib.util.spec_from_file_location('tight13_fresh',B/'audit_core39.py');V=importlib.util.module_from_spec(sp);sp.loader.exec_module(V)
    V.CAP=CAP;V.START=START;V.QCAP=QCAP;V.CALLS=0
    def fresh_action(t,n,x):
        k=t,n,x
        if k in fresh:return fresh[k]
        if V.CALLS>=max(0,QCAP-30):raise StopQueries
        out,h,q,_=V.splay(t,x,False);fresh[k]=(out,h,q);return fresh[k]
    lift=R.Lift(old,fresh_action);status='CHECKPOINT'
    try:
        while i<N and time.process_time()-START<CAP-4:
            a,b=key=keys[i];ta=R.unrank(13,1,a);tb=R.unrank(13,1,b);ar=ta[0];br=tb[0]
            actions=[]
            if ar!=br:actions.append(('KEEP',ar,ta,0))
            for x in R.near(ta):
                out,h,_=lift.action(ta,13,x);assert h==1
                actions.extend((('KEEP',x,out,h),('DELETE',x,out,h)))
            local=[]
            for kind,x,out,h in actions:
                aa=R.rank_tree(out,1,13)
                if kind=='KEEP' and x!=br:
                    outb,_,q=lift.action(tb,13,x);bb=R.rank_tree(outb,1,13)
                else:bb=b;q=0
                dest=(aa,bb)
                if dest in index and records[dest][0]-records[key][0]==q-2*h:
                    local.append((i,index[dest],kind,x,h,q))
            edges.extend(local);i+=1
            assert len(edges)<=250000
            assert 646646+58786+4*N+len(edges)+100000<2000000
        if i==N:status='COMPLETE_RETAINED_EXACT_ZERO_REDUCED_GRAPH'
    except StopQueries:status='QUERY_RESERVE_CHECKPOINT'
    out={'status':status,'records':records,'fresh':fresh,'keys':keys,'next_source':i,'edges':edges,
      'source_queries':V.CALLS,'source_engine_calls':V.CALLS,'source_states':N,'retained_edges':len(edges),
      'source_substitutions_this_batch':lift.substitutions,'JR35':'OPEN','not_exhaustive_full_source_graph':True,
      'input_sha256':{str(p):sha(p) for p in (bp,F/'ranked_source_bst.py',F/'probe11_source_actions.pkl',F/'mine_source13_tight_cycles.py')}}
    with (F/f'source13_tight_graph_{BATCH:02d}.pkl').open('xb') as f:pickle.dump(out,f,protocol=5)
    report={k:v for k,v in out.items() if k not in ('records','fresh','keys','edges')}
    with (F/f'source13_tight_graph_{BATCH:02d}.json').open('x',encoding='utf8') as f:json.dump(report,f,indent=2)
    print(json.dumps(report),flush=True);assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        n=0 if V is None else V.CALLS
        with (B/f'audit_{PHASE}_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':n,'source_engine_calls':n},f)
