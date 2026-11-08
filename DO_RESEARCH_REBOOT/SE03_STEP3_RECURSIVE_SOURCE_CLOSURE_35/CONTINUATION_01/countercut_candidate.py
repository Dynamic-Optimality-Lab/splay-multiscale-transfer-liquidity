"""Candidate source countercut:11 new A splays and3 critical B splays.
Full B recurrence and Gamma blocks are symbolic source theorems, not a
claimed numerical full-history replay. Save every new primitive result.
"""
import importlib.util,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;C=F.parent;P=C.parent;B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01';START=time.process_time();CAP=float(sys.argv[1]);QCAP=int(sys.argv[2])
sp=importlib.util.spec_from_file_location('functional_original_splay',B/'audit_core39.py');S=importlib.util.module_from_spec(sp);sp.loader.exec_module(S);S.CAP=CAP;S.QCAP=min(14,QCAP);S.START=START;S.CALLS=0
def right(lo,hi):return None if lo>hi else (lo,None,right(lo+1,hi))
def left(lo,hi):return None if lo>hi else (hi,left(lo,hi-1),None)
def comb(lo,hi):return None if lo>hi else (2*lo,(2*lo-1,None,None),comb(lo+1,hi))
def t_before(i):
    p=2*i-1
    return (1,None,(2,None,(p,left(3,2*i-2),(2*i,None,(15,comb(i+1,7),None)))))
def low_marked(x=1):
    if x==13:return (13,(12,None,None),(14,None,(15,None,None)))
    return (x,None if x==1 else (x-1,None,None),low_marked(x+2))
def out(n,z):
    with (F/n).open('x',encoding='utf-8') as f:json.dump(z,f,indent=2)
def main():
    assert QCAP>=14
    A=initial=low_marked();rows=[];selected=[];splays=[]
    # K1 is an A root identity. The following11 operations are all actual
    # A accesses before the last selected consumer, in their true order.
    word=[]
    for i,x in enumerate(range(3,14,2),1):
        if i>1:word.append(('K',1,'anchor'))
        word.append(('K',x,'consumer'))
    for j,(kind,x,role) in enumerate(word,1):
        aa=A;A,a,_,ev=S.splay(A,x,True);r=dict(local_operation=j,kind=kind,key=x,role=role,A_before=aa,A_after=A,a=a,events=ev);rows.append(r)
        if x in (5,9,13):selected.append(r)
    out('new_A_primitive_rows.json',dict(initial=initial,rows=rows,fresh_splays=S.CALLS,scope='local A access word only; no Gamma cost or full B replay claimed'))
    for i,r in zip((2,4,6),selected):
        target=2*i+1;before=t_before(i);after,H,q,ev=S.splay(before,target,True)
        ancestors=[S.at(before,S.search(before,target)[:k])[0] for k in range(len(S.search(before,target)))]
        marked_anc=[g for g in ancestors if g%2]
        assert r['a']==1 and q==3 and marked_anc==[1,2*i-1,15]
        splays.append(dict(i=i,target=target,B_before=before,B_after=after,q=q,events=ev,old_marked_ancestors=marked_anc,A_local_operation=r['local_operation']))
    out('critical_B_primitive_rows.json',dict(rows=splays,fresh_splays=3,scope='three critical sources instantiated from symbolic closed-family formula'))
    # Actual unit names use exact source labels: c is DELETE1 following
    # the initial genuine K15; v_i is the selected genuine K(2i+1).
    N={str(x):[['c',1,b] for b in (0,1)]+[[f'v{x}',1,b] for b in (0,1)] for x in (5,9,13)}
    union={tuple(u) for nn in N.values() for u in nn};assert len(union)==8
    out('countercut_candidate.json',dict(status='CANDIDATE_PENDING_SYMBOLIC_SOURCE_AND_INDEPENDENT_AUDIT',r=8,physical_keys=list(range(1,16)),marked=list(range(1,16,2)),targets=[5,9,13],demand_count=9,unit_count=8,pools=N,sigma=3,overlap=4,local_unused=0,deficit=1,source_queries=S.CALLS,source_engine_calls=S.CALLS,primitive_scope='11 A and3 critical B accesses; whole closed family proved separately',old_source_or_owner_modified=False))
    assert S.CALLS==14
    print('CANDIDATE_9_DEMANDS_8_UNITS_CRITICAL_COSTS_MATCH',flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_core44_exit.json').open('x') as f:json.dump(dict(whole_process_CPU_seconds=time.process_time(),error=error,source_queries=S.CALLS,source_engine_calls=S.CALLS),f)
