"""Independent A replay and pool/peeling checks; old B states reused.
Exactly16 new original A queries. Does not import producer routines.
"""
import collections,hashlib,importlib.util,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parent;C=P/'SE03_STEP3_GLOBAL_JOINT_OWNERSHIP_34';B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01';START=time.process_time();CAP=float(sys.argv[1]);QCAP=int(sys.argv[2])
def module(n,p):
    sp=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
V=module('accepted_mutable_source_auditor',B/'audit_verify79.py');V.CAP=CAP;V.QCAP=QCAP;V.START=START;V.CALLS=0
I=module('accepted_independent_pool_auditor',C/'audit_pools.py')
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def peel_check(mm,steps):
    active=set(range(len(mm)));selected=set()
    for st in steps:
        i=st['index'];assert i in active
        own={tuple(u) for u in mm[i]['N']};other=set().union(*({tuple(u) for u in mm[j]['N']} for j in active if j!=i)) if len(active)>1 else set();private=own-other;ss={tuple(u) for u in st['selected']}
        assert len(private)==st['private_count'] and len(ss)==mm[i]['Q'] and ss<=private and not ss&selected;selected|=ss;active.remove(i)
    return sorted(active)
def main():
    source=read(F/'compressed_A_closed_source.json');control=read(F/'compressed_A_pool_control.json');assert sha(F/'compressed_A_closed_source.json')==control['source_sha256']
    oldpath=Path(source['inherited_B_source']);assert sha(oldpath)==source['inherited_B_source_sha256'];old=read(oldpath);keep=[r for r in old['period_rows'] if r['kind']=='K'];assert len(keep)==len(source['period_rows'])==16
    A=V.Mutable(source['initial_A']);M={r['key'] for r in keep};allkeys=set(A.nodes);assert allkeys==set(range(1,14)) and M==set(range(1,14,2))
    cf,ce=list(old['period_boundary'][3]),list(old['period_boundary'][4]);initial_cf,initial_ce=cf[:],ce[:]
    for r,b in zip(source['period_rows'],keep):
        assert V.eq(A.snapshot(),r['A_before']);a,_,ev=A.splay(r['key'],True);assert a==r['a'] and V.eq(ev,r['A_events']) and V.eq(A.snapshot(),r['A_after'])
        for k in ('BF_before','BF_after','BE_before','BE_after','qF','qE'):assert r[k]==b[k]
        if r['BF_before'][0]!=r['key']:cf=[r['key']]+[x for x in cf if x!=r['key']]
        if r['key']!=3 and r['BE_before'][0]!=r['key']:ce=[r['key']]+[x for x in ce if x!=r['key']]
        assert cf==r['chart_F'] and ce==r['chart_E']
    assert V.eq(A.snapshot(),source['initial_A']) and cf==initial_cf and ce==initial_ce
    rr=I.canonical(source,'C33_36');mm,D,U,N,h0=I.reconstruct(rr)
    assert len(D)==36 and len(U)==48 and sum(r['a'] for r in rr)==24
    assert all(m['Q']<=2*m['H'] for m in mm)
    assert not peel_check(control['macros'],control['peeling_steps']) and not control['unpeeled_indices']
    assert I.flow(N,D)==len(D)
    # Independent literal macro pools must equal producer graph.
    for a,b in zip(mm,control['macros']):
        for k in ('N','T','demands'):assert a[k]=={tuple(u) for u in b[k]}
    saved=read(C/'pooled_source_results.json');cert=read(F/'peeling_core_and_birth_intersections.json');fixed=[]
    for a,b in zip(saved['cases'],cert['cases']):
        assert a['name']==b['source'] and not peel_check(a['macros'],b['steps'])
        fixed.append(dict(source=a['name'],complete_deletion_certificate=True,all_subsets_of_this_fixed_source_covered_by_order_restriction=True))
    deps=[F/'PRIVATE_CAPACITY_RECURSION.md',F/'CYCLIC_BIRTH_INTERSECTION.md',F/'SOURCE_COALITION_REDUCTION.md',F/'ROTATION_LEVEL_OVERLAP_IDENTITIES.md',F/'ABSTRACT_COMPENSATION_COUNTERMODEL.md']
    out=dict(status='PASS_DISTINCT_A_REPLAY_AND_FIXED_SOURCE_DELETION_CERTIFICATES',input_sha256={str(p):sha(p) for p in [F/'compressed_A_closed_source.json',F/'compressed_A_pool_control.json',F/'peeling_core_and_birth_intersections.json',C/'pooled_source_results.json',*deps]},source_queries=V.CALLS,source_engine_calls=V.CALLS,new_source_A=24,new_source_QF=36,new_source_A_and_B_charts_closed=True,new_source_reachability='inherited same-key A-only transformation theorem; no numerical preparation claimed',B_primitives_reused_without_replay=True,source_coordinates='local i with common absolute offset p, one actual original period',fixed_source_checks=fixed,uniform_source_peeling='NOT_PROVED',SI34='ACTIVE',trust='same-agent distinct implementation checking, not external or formal verification')
    with (F/'independent_source_and_recursion_audit.json').open('x',encoding='utf-8') as f:json.dump(out,f,indent=2)
    assert V.CALLS==16 and time.process_time()-START<CAP-1
    print(out['status'],flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_verify84_exit.json').open('x') as f:json.dump(dict(whole_process_CPU_seconds=time.process_time(),error=error,source_queries=V.CALLS,source_engine_calls=V.CALLS),f)
