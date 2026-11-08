"""One falsifying original source: Gamma55. No source search."""
import json,time,sys,importlib.util,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();queries=0
def out(n,v):
    with (B/n).open('x') as f:json.dump(v,f,indent=2)
def main():
    global queries
    sp=importlib.util.spec_from_file_location('original_source33',P/'SE03_STEP2_COLD_NEG2_01/source_model.py');S=importlib.util.module_from_spec(sp);sp.loader.exec_module(S)
    original=S.path
    def path(t,x):
        global queries
        if queries>=QCAP or time.process_time()-START>=CAP-2:raise TimeoutError('source cap')
        queries+=1;return original(t,x)
    S.path=path
    r=55;n=2*r-1;K=lambda a:[('K',x) for x in a]
    ascending=list(range(3,n+1,2));descending=list(range(n-2,0,-2))
    w=K(ascending+descending[:-1])+[('D',n),('D',1),('K',1),('K',n),('D',2),('D',n)]+K([1]+ascending+descending)
    assert len(w)==4*r+2
    initial=S.vine(n);state=(initial,initial,initial);order=S.inorder(initial);prefix=None;rows=[];snapshots={}
    for copy in range(2):
        if copy==1:period_initial=state
        for local,(mode,x) in enumerate(w,1):
            t=copy*len(w)+local;a,b,e=state;before=state;bfroot=b[0];eroot=e[0]
            a,pa,ea=S.trace(a,x);pb=pe='';eb=ee=[]
            if mode=='K':b,pb,eb=S.trace(b,x)
            if mode=='K' and x!=3:e,pe,ee=S.trace(e,x)
            state=(a,b,e);assert all(S.inorder(v)==order for v in state)
            if copy==1:
                row={'occurrence':t,'local':local,'mode':mode,'target':x,'a':len(ea),'qF':len(pb)//2,'qE':len(pe)//2,
                     'A_path':pa,'BF_path':pb,'BE_path':pe,'A_events':ea,'BF_events':eb,'BE_events':ee,
                     'genuine_F':mode=='K' and bfroot!=x,'genuine_E':mode=='K' and x!=3 and eroot!=x}
                rows.append(row)
                if mode=='K' and x==n and row['qF']==r-1:
                    snapshots={'occurrence':t,'local':local,'before':before,'after':state};critical=row
        assert state[0]==state[1]==initial
        if copy==0:prefix=state
    assert state==period_initial and prefix==period_initial
    assert sum(v['a'] for v in rows)==6*r-2 and sum(v['qF'] for v in rows)==6*r-6 and sum(v['qE'] for v in rows)==6*r-12
    assert (critical['a'],critical['qF'],critical['qE'])==(1,r-1,r-2)
    U=[(v['occurrence'],j,b) for v in rows for j in range(1,v['a']+1) for b in (0,1)]
    DF=[(v['occurrence'],j) for v in rows for j in range(1,v['qF']+1)];DE=[(v['occurrence'],j) for v in rows for j in range(1,v['qE']+1)]
    # Explicit STATIC count maps demonstrate nonvacuity, not a Bank25 receipt.
    def raw(which):
        ends=[i for i,v in enumerate(rows) if v['genuine_'+which]];mp={}
        for j,i in enumerate(ends):
            prev=ends[j-1];seg=rows[prev+1:i+1] if prev<i else rows[prev+1:]+rows[:i+1]
            units=[(v['occurrence'],k,b) for v in seg for k in range(1,v['a']+1) for b in (0,1)]
            demands=[(rows[i]['occurrence'],k) for k in range(1,rows[i]['q'+which]+1)]
            mp.update(zip(demands,units))
        demands=set(DF if which=='F' else DE);missing=sorted(demands-mp.keys());occupied=set(mp.values())
        prep=next(v for v in rows if v['mode']=='D' and v['target']==n)
        free=[u for u in U if u[0]==prep['occurrence'] and u not in occupied]
        assert len(free)>=len(missing);mp.update(zip(missing,free));assert set(mp)==demands and len(set(mp.values()))==len(mp)
        return [{'demand':d,'unit':u} for d,u in sorted(mp.items())]
    receipt={'r':r,'n':n,'word':w,'initial_diagonal':initial,'reaching_prefix':w,'period_start':len(w)+1,'period_end':2*len(w),
        'period_initial':period_initial,'period_final':state,'rows':rows,'critical':snapshots,'U':U,'DF':DF,'DE':DE,
        'H_count':raw('F'),'fE_count':raw('E'),'counts':{'A':6*r-2,'QF':6*r-6,'QE':6*r-12,'slack':6*r+2},
        'full_endpoint_lower_bound':(r-2)//2,'common_endpoint_lower_bound':(r-3)//2,
        'frozen_owner_for_EP_counterexample':[], 'raw_count_maps_are_normalized_licensed_receipts':False,
        'claim':'every full injection and every common owner injection has endpoint peak>=26; no GateU14 working-bank refutation claimed'}
    out('Gamma55_original_source.json',receipt)
    print(json.dumps({'status':'EXACT_GAMMA55_SOURCE','ops':len(w),'counts':receipt['counts'],'critical':{k:critical[k] for k in ('occurrence','a','qF','qE')},'queries':queries}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_source_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':queries})
