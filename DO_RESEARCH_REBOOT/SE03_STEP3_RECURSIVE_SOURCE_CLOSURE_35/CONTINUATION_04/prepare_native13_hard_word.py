"""Thirteen genuine keys, ranked full states, literal B-cycle discovery."""
import hashlib,importlib.util,json,pickle,random,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01';sys.path.insert(0,str(F))
import ranked_source_bst as R
CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();V=None
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
class Reserve(Exception):pass
def main():
    global V
    with (F/'probe11_source_actions.pkl').open('rb') as f:old=pickle.load(f)
    sp=importlib.util.spec_from_file_location('n13_new_Hamiltonian_source',B/'audit_core39.py');V=importlib.util.module_from_spec(sp);sp.loader.exec_module(V)
    V.CAP=CAP;V.START=START;V.QCAP=QCAP;V.CALLS=0;fresh=[]
    def kernel(t,n,x):
        if V.CALLS>=max(0,QCAP-60):raise Reserve()
        z,h,q,e=V.splay(t,x,True);fresh.append({'n':n,'source':t,'target':x,'destination':z,'H':h,'Q':q,'events':e});return z,h,q
    lift=R.Lift(old,kernel);rng=random.Random(35132160);best=None;trials=0;stop=None
    try:
        while trials<5000 and time.process_time()-START<CAP-4:
            trials+=1;word=list(range(1,14));rng.shuffle(word);state=R.unrank(13,1,0);seen={state:0};copies=[]
            for copy in range(4):
                rows=[]
                for x in word:
                    a=state;state,h,q=lift.action(state,13,x)
                    rows.append({'KEEP':x,'B_source':R.rank_tree(a,1,13),'B_target':R.rank_tree(state,1,13),'Q':q})
                copies.append(rows)
                if state in seen:u=seen[state];L=copy+1-u;break
                seen[state]=copy+1
            else:continue
            if L!=1:continue
            rows=copies[u];Q=sum(r['Q'] for r in rows)
            if best is None or Q>best['Q']:best={'word':word,'rows':rows,'prefix_B_copies':u,'period_B_copies':1,'Q':Q}
            if Q>=29:break
    except Reserve:stop='PRESERVED_60_QUERY_RESERVE'
    assert best is not None
    best.update({'status':'LITERAL_CLOSED_NATIVE13_HARD_B_WORD','native13_states':R.C[13],
      'root_counts':[R.C[i]*R.C[12-i] for i in range(13)],'root_offsets':R.OFF[13],
      'next_key_by_root':{R.unrank(13,1,r['B_source'])[0]:r['KEEP'] for r in best['rows']},
      'sampled_permutations':trials,'B_only_minimum_A_event_margin':26-best['Q'],'stop':stop,
      'source_cached_substitutions':lift.substitutions,'fresh_Hamiltonian_actions':fresh,
      'source_queries':V.CALLS,'source_engine_calls':V.CALLS,'JR35':'OPEN',
      'input_sha256':{str(p):sha(p) for p in (F/'ranked_source_bst.py',F/'probe11_source_actions.pkl',F/'independent_probe11_source_actions.json',B/'OFF_PATH_LEAF_SOURCE_LIFT.md')}})
    with (F/'native13_hard_B_word.json').open('x',encoding='utf8') as f:json.dump(best,f,indent=2)
    print(json.dumps({k:v for k,v in best.items() if k not in ('rows','fresh_Hamiltonian_actions','input_sha256')}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        n=0 if V is None else V.CALLS
        with (B/'audit_core55_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':n,'source_engine_calls':n},f)
