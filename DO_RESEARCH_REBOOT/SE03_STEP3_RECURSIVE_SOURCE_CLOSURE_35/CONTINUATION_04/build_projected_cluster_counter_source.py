"""Exact closed witness from accepted complete native11 primitives."""
import collections,hashlib,json,pickle,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;B=F.parents[1]/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time();PHASE=sys.argv[3]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=F/'probe11_source_actions.pkl';au=F/'independent_probe11_source_actions.json'
    with ap.open('rb') as f:z=pickle.load(f)
    T=z['trees'];D=z['destination'];H=z['H'];Q=z['Q'];index={a:i for i,a in enumerate(T)}
    n=11;R=None;left=None
    for k in range(n,0,-1):R=(k,None,R)
    for k in range(2,n):left=(k,left,None)
    As=(1,None,(n,left,None));root=index[R];start=index[As]
    def goto(a,b):
        todo=collections.deque([a]);parents={a:None}
        while b not in parents:
            t=todo.popleft()
            for k,v in enumerate(D[t],1):
                u=int(v)
                if u not in parents:parents[u]=(t,k);todo.append(u)
            assert time.process_time()-START<CAP-4
        out=[]
        while b!=a:b,k=parents[b];out.append(k)
        return list(reversed(out))
    prep=goto(root,start);A=start
    for k in range(n,1,-1):A=int(D[A,k-1])
    reset=goto(A,start)
    w=[('K',k) for k in range(n,1,-1)]+[('D',k) for k in reset]+[('K',1)]
    A=BF=BE=root;cf=ce=();ts=0;erase=2
    def one(kind,k):
        nonlocal A,BF,BE,cf,ce,ts
        ts+=1;ba,bf,be=A,BF,BE;af=int(H[A,k-1]);A=int(D[A,k-1]);qf=qe=0;gf=ge=False
        if kind=='K':
            gf=T[BF][0]!=k;qf=int(Q[BF,k-1]);BF=int(D[BF,k-1])
            if gf:cf=(k,)+tuple(x for x in cf if x!=k)
            if k!=erase:
                ge=T[BE][0]!=k;qe=int(Q[BE,k-1]);BE=int(D[BE,k-1])
                if ge:ce=(k,)+tuple(x for x in ce if x!=k)
        return {'t':ts,'kind':kind,'key':k,'A_before':T[ba],'BF_before':T[bf],'BE_before':T[be],
          'A_after':T[A],'BF_after':T[BF],'BE_after':T[BE],'a':af,'qF':qf,'qE':qe,
          'genuine_F':gf,'genuine_E':ge,'chart_F':cf,'chart_E':ce}
    prefix=[one('D',k) for k in prep];assert A==start and BF==BE==root
    def state():return A,BF,BE,cf,ce
    seen={state():0};copies=[];bounds=[state()]
    for _ in range(16):
        rows=[one(kind,k) for kind,k in w];assert A==start and BF==root
        copies.append(rows);bounds.append(state())
        if state() in seen:
            u=seen[state()];v=len(copies);break
        seen[state()]=len(copies)
    else:raise AssertionError('bounded producer did not find recurrence')
    prefix+=sum(copies[:u],[]);rows=sum(copies[u:v],[]);assert bounds[u]==bounds[v]
    assert {r['key'] for r in rows if r['genuine_F']}==set(range(1,n+1))
    r=rows[0];assert (r['kind'],r['key'],r['a'],r['qF'])==('K',n,1,5)
    assert rows[-1]['kind']=='K' and rows[-1]['key']==1 and rows[-1]['genuine_F'] and rows[-1]['a']==0
    def labels(t):
        ans=set()
        def go(t):
            if t is None:return frozenset()
            a=go(t[1])|go(t[2])|{t[0]};ans.add(a);return a
        go(t);return ans
    ps=len(labels(r['BF_before'])-labels(r['A_before']))
    pm=len(labels(r['BF_before'])-labels(r['A_after']))
    pt=len(labels(r['BF_after'])-labels(r['A_after']))
    assert (ps,pm,pt)==(9,10,9)
    Acount=sum(x['a'] for x in rows);QF=sum(x['qF'] for x in rows);QE=sum(x['qE'] for x in rows)
    assert QF<=2*Acount
    result={'status':'ORIGINAL_REACHABLE_PAIRED_CLOSED_PROJECTION_REFUTATION',
      'physical_keys':list(range(1,n+1)),'M':list(range(1,n+1)),'S':list(range(1,n+1)),'erased_key':erase,
      'initial_diagonal':R,'initial_A_preparation':prep,'A_reset_word':reset,'source_word':w,
      'prefix_rows':prefix,'period_rows':rows,'period':[rows[0]['t'],rows[-1]['t']],
      'preperiod_copies':u,'actual_period_copies':v-u,'A':Acount,'QF':QF,'QE':QE,
      'target_t':r['t'],'target_macro':{'H':1,'Q':5,'Phi_before_A':ps,'Phi_after_A':pm,'Phi_after_B':pt,
        'signed_margin':-3,'neutral_demand_ids':[(r['t'],k) for k in range(1,5)],
        'candidate_local_neighborhood':[(r['t'],1,b) for b in (0,1)],'candidate_cut_deficiency':2},
      'CD_counterexample':False,'JR35':'OPEN','source_queries':0,'source_engine_calls':0,
      'input_sha256':{str(p):sha(p) for p in [ap,au,F/'PROJECTED_CLUSTER_ACCESS_THEOREM.md']}}
    with (F/'projected_cluster_closed_counter_source.json').open('x',encoding='utf8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k not in ('prefix_rows','period_rows','input_sha256','initial_diagonal')}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/f'audit_{PHASE}_exit.json').open('x',encoding='utf-8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
