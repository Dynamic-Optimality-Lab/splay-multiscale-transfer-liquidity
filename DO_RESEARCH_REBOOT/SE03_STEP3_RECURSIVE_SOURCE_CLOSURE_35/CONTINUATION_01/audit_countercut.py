"""Independent mutable-parent checks of the14 critical original accesses.
No producer imports. Whole B recurrence is a separate symbolic proof.
"""
import hashlib,importlib.util,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;C=F.parent;P=C.parent;B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01';START=time.process_time();CAP=float(sys.argv[1]);QCAP=int(sys.argv[2])
sp=importlib.util.spec_from_file_location('mutable_independent',B/'audit_verify79.py');V=importlib.util.module_from_spec(sp);sp.loader.exec_module(V);V.CAP=CAP;V.QCAP=QCAP;V.START=START;V.CALLS=0
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def lchain(a,b):
    z=None
    for x in range(a,b+1):z=(x,z,None)
    return z
def comb(a,b):
    z=None
    for j in reversed(range(a,b+1)):z=(2*j,(2*j-1,None,None),z)
    return z
def ancestors(state,k):
    p=state.nodes[k].parent;aa=[]
    while p is not None:aa.append(p.k);p=p.parent
    return aa[::-1]
def main():
    assert QCAP>=14
    z=read(F/'new_A_primitive_rows.json');b=read(F/'critical_B_primitive_rows.json');candidate=read(F/'countercut_candidate.json')
    # Independently build the exact15-key start tree from its terminal right end.
    a=(14,None,(15,None,None))
    for x in range(13,0,-2):a=(x,None if x==1 else (x-1,None,None),a)
    assert V.eq(a,z['initial']);A=V.Mutable(a);check=[]
    expected_word=[3,1,5,1,7,1,9,1,11,1,13];assert [r['key'] for r in z['rows']]==expected_word
    states={}
    for r in z['rows']:
        assert V.eq(A.snapshot(),r['A_before']);path=ancestors(A,r['key']);aa,_,ev=A.splay(r['key'],True)
        assert aa==r['a'] and V.eq(ev,r['events']) and V.eq(A.snapshot(),r['A_after']);states[r['local_operation']]=r
        assert A.nodes[15].left is A.nodes[15].right is None
        if r['key'] in (5,9,13):
            assert path==[1,r['key']-2] and aa==1
            assert [s['pivot'] for s in ev[0]['rotations']]==[1,r['key']-2]
            # The previous consumer's birth-to-demand interval has just
            # anchor1 and this event; its ancestry survives that anchor.
            prev=z['rows'][r['local_operation']-3];anchor=z['rows'][r['local_operation']-2]
            assert prev['key']==r['key']-2 and anchor['key']==1
            assert V.ancestor(anchor['A_before'],prev['key'],r['key']) and V.ancestor(anchor['A_after'],prev['key'],r['key'])
            check.append(dict(target=r['key'],A_event_cost=1,actual_own_rotation_pivots=path))
    assert sum(r['a'] for r in z['rows'])==13
    for rec in b['rows']:
        i=rec['i'];p=2*i-1
        before=(1,None,(2,None,(p,lchain(3,2*i-2),(2*i,None,(15,comb(i+1,7),None)))))
        assert V.eq(before,rec['B_before']);BF=V.Mutable(before);marked=[g for g in ancestors(BF,rec['target']) if g%2]
        H,q,ev=BF.splay(rec['target'],True)
        assert q==3 and marked==[1,p,15] and V.eq(ev,rec['events']) and V.eq(BF.snapshot(),rec['B_after'])
        assert all(e['pattern'] in ('LL','RR') and e['grandparent']%2 and not e['parent']%2 for e in ev)
    assert V.CALLS==14
    # Source-interval proof supplies EXACT R sets, not merely possible donor
    # subsets. Check the resulting literal graph with all pool choices allowed.
    pools={k:{tuple(u) for u in v} for k,v in candidate['pools'].items()};un=set().union(*pools.values());assert len(un)==8
    assert all(len(nn)==4 for nn in pools.values()) and sum(len(nn)-3 for nn in pools.values())==3
    assert sum(map(len,pools.values()))-len(un)==4 and all(len(pools[k]-set().union(*(pools[j] for j in pools if j!=k)))==2 for k in pools)
    proof=B/'UNIFORM_A_REALIZATION_OVER_CLOSED_B.md';pdf=B/'primary_1907_06310v3.pdf';receipt=B/'uniform_A_realization_independent_audit.json'
    assert sha(proof)=='907419177de92dab3a4a13313969e12ade15c94805fe8358c1a5294d4fbfa574'
    assert sha(pdf)=='f7aa79010984db5104c81846d7d0862bb4b83c1f13cbc84c922757e340c36f1c'
    assert read(receipt)['input_sha256']['UNIFORM_A_REALIZATION_OVER_CLOSED_B.md']==sha(proof)
    docs=['SYMBOLIC_B_CLOSURE.md','SOURCE_CONSTRUCTION.md','EXACT_NEGATIVE_CUT.md','DEPENDENCIES_AND_SCOPE.md']
    result=dict(status='PASS_DISTINCT_CRITICAL_SOURCE_EXECUTIONS_AND_COUNTERCUT_ARITHMETIC',input_sha256={n:sha(F/n) for n in ['new_A_primitive_rows.json','critical_B_primitive_rows.json','countercut_candidate.json',*docs]},A_checks=check,new_A_queries=11,new_B_queries=3,source_queries=14,source_engine_calls=14,first_DELETE1='proved as original LL depth2, not freshly replayed',full_B_closure='symbolic source induction, independent free-term audit separate',Gamma_and_erased_period='accepted transformation theorem plus deterministic finite recurrence; NOT numerically expanded',full_new_source_replayed=False,physical_pool_union=8,original_selected_demands=9,old_sources_owners_unchanged=True,trust='same-agent distinct implementation; not external peer review/formal proof assistant')
    with (F/'independent_critical_source_audit.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    assert time.process_time()-START<CAP-1
    print(result['status'],flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_verify87_exit.json').open('x') as f:json.dump(dict(whole_process_CPU_seconds=time.process_time(),error=error,source_queries=V.CALLS,source_engine_calls=V.CALLS),f)
