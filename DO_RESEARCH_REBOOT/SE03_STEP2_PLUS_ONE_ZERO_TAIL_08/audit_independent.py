"""Independent Campaign08 forward terminal calculus and zero-closure audit.
Uses the distinct immutable engine and generic checker helpers only; no
Campaign08 source producer or predecessor implementation is imported.
"""
import collections,functools,importlib.util,itertools,json,sys,time
from fractions import Fraction as F
from pathlib import Path
B=Path(__file__).resolve().parent;OLD=B.parent/'SE03_STEP2_FINAL_PLUS_ONE_07'
spec=importlib.util.spec_from_file_location('prior_generic_checker',OLD/'audit_independent2.py')
d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d);a=d.a
started=time.process_time();CAP=min(100,float(sys.argv[1])-4)
def guard():assert time.process_time()-started<CAP and a.calls<1500000
a.guard=guard
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    states={t for t in a.alltrees(1,11) if t[1] in a.M and a.density(t)[2]};assert len(states)==2394
    inc=collections.defaultdict(list);fwd=collections.defaultdict(list);q3=q4=pair=0
    for t in states:
        for x in a.M-{t[1]}:
            n=a.legal(t,x)
            if n is None:continue
            end,q=n;assert end in states
            fwd[t].append((end,x,q));inc[end].append((t,x,q))
            if q==3:assert a.degree(end)>=3;q3+=1
            if q==4:assert a.degree(end)>=4 and a.L(end)>=4;q4+=1
    for t in states:
        for u,x,q in fwd[t]:
            if q==5:
                for end,y,qq in fwd[u]:assert qq==1 and a.L(end)==4 and a.degree(end)==1;pair+=1
    perms=list(itertools.permutations(sorted(a.M)))
    @functools.lru_cache(None)
    def orders(t):return tuple(r for r in perms if r[0]==t[1] and a.heap(t,r))
    @functools.lru_cache(None)
    def initial(word):
        fs,sz=a.frames(word,range(1,12),0,12)
        return tuple({d.canonical(v) for v,end in fs})
    # Independently derive the FINAL ZERO inverse before reading producer data.
    zero={};cases={};expectedgroups=collections.defaultdict(set);P1B=0
    for u in states:
        for end,y,q in fwd[u]:
            if q!=2:continue
            for probe,x,qx in fwd[end]:
                if qx!=4:continue
                rr=[]
                for r in orders(u):
                    rn=(y,)+tuple(k for k in r if k!=y)
                    if rn[-1]==x:
                        assert a.heap(end,rn);rr.append(r)
                if not rr:continue
                assert a.L(u)==a.L(end)==2 and a.degree(end)==2 and a.degree(u) in (1,2)
                zero[a.bf_write(u),a.bf_write(end),y,x]=(initial((u[1],y,x)),set(rr))
                for before,z,q0 in inc[u]:
                    if q0==3:P1B+=1;raise AssertionError('H2Q3 has no final-zero-compatible BF destination')
                    if q0!=1:continue
                    rp=[]
                    for r in orders(before):
                        r1=(z,)+tuple(k for k in r if k!=z);r2=(y,)+tuple(k for k in r1 if k!=y)
                        if r2[-1]!=x:continue
                        assert r1 in rr and a.heap(u,r1) and a.heap(end,r2);rp.append(r)
                    if not rp:continue
                    word=(before[1],z,y,x);assert len(set(word))==4
                    terms=initial(word);key=(a.bf_write(before),a.bf_write(u),a.bf_write(end),z,y,x)
                    cases[key]=(bool(terms),len(rp),a.L(before))
                    for term in terms:expectedgroups[term,before].update(rp)
    assert len(zero)==48 and len(cases)==64 and P1B==0
    suppliedzero=json.loads((B/'final_zero_inverse.json').read_text());seen=set();zero_cover=0
    for v in suppliedzero['sectors']:
        key=(a.freeze(v['BF_before_zero']),a.freeze(v['BF_after_zero']),v['zero_target'],v['cold_q4'])
        assert key in zero;seen.add(key);E,rr=zero[key]
        assert rr==set(map(tuple,v['recent_before_zero']))
        P={d.canonical(a.Aread(t)) for t in v['A_before_zero_terms']}
        assert all(any(d.includes(p,e) for p in P) for e in E)
        assert all(any(d.includes(e,p) for e in E) for p in P)
        zero_cover+=len(E)+len(P)
    assert seen==set(zero)
    producer=json.loads((B/'terminal_seeds.json').read_text())
    declared={(a.freeze(v['BF_before_plus']),a.freeze(v['BF_after_plus']),a.freeze(v['BF_after_zero']),
        v['plus_target'],v['zero_target'],v['cold_q4']):(v['A_initial_terms']>0,v['recent_orders'],v['L_before_plus'])
        for v in producer['terminal_cases']}
    assert declared==cases
    suppliedgroups={}
    for v in producer['groups']:
        suppliedgroups[d.canonical(a.Aread(v['A'])),a.bf_read(v['BF'])]=set(map(tuple,v['recent']))
    def regroup(groups):
        by=collections.defaultdict(list)
        for (t,b),rr in groups.items():
            for r in rr:by[b,r].append(t)
        return {key:tuple(sorted(set(v),key=d.size)) for key,v in by.items()}
    Eby,Pby=regroup(expectedgroups),regroup(suppliedgroups);assert set(Eby)==set(Pby)
    cover=0
    for key,E in Eby.items():
        P=Pby[key]
        assert all(any(d.includes(p,e) for p in P) for e in E)
        assert all(any(d.includes(e,p) for e in E) for p in P)
        cover+=len(E)+len(P)
    assert len(suppliedgroups)==320 and sum(map(len,suppliedgroups.values()))==3992
    cert=json.loads((B/'zero_closure.json').read_text());assert cert['closed'] and cert['goal'] is None and cert['bound'] is None
    by=collections.defaultdict(list);records=[];shapes=collections.Counter();private=collections.Counter()
    for v in cert['records']:
        t=d.canonical(a.Aread(v['A']));b=a.bf_read(v['BF']);r=tuple(v['recent']);L=a.L(b);deg=a.degree(b)
        assert b in states and t[1]==b[1]==r[0] and a.heap(b,r)
        assert L<=4 and deg<=3 and not (L==4 and deg in (1,4))
        if L==4:assert deg==2
        shapes[L,deg]+=1;private[sum(k.denominator!=1 for k in a.keys(t))]+=1
        by[b,r].append(t);records.append((t,b,r))
    by={key:tuple(sorted(set(v),key=d.size)) for key,v in by.items()}
    @functools.lru_cache(maxsize=150000)
    def contained(t,b,r):return any(d.includes(p,t) for p in by.get((b,r),()))
    for (t,b),rr in expectedgroups.items():
        for r in rr:assert contained(t,b,r)
    proposals=0
    for i,(t,b,r) in enumerate(records):
        if i%128==0:guard()
        # H2/Q4 output degree>=4 cannot enter any record. Paired H3/Q6
        # output (L4,degree1) cannot enter the stronger separated language.
        for old,x,q in inc[b]:
            if q!=2 or r[1]!=old[1]:continue
            base=list(r[1:]);prior=[]
            for pos in range(1,6):
                rr=tuple(base[:pos]+[x]+base[pos:])
                if a.heap(old,rr):prior.append(rr)
            if not prior:continue
            for before in d.inverse_H1(t,F(old[1])):
                for rr in prior:
                    assert contained(before,old,rr),'missing genuine zero source from the new closure'
                    proposals+=1
    assert len(records)==9624 and proposals==5872
    assert sum(v for (L,deg),v in shapes.items() if L==4)==720
    # Independent cold-target source shape, stronger than mere leaf counts.
    coldS=coldP=0
    for b in states:
        for end,x,q in fwd[b]:
            if q==4 and x not in set(a.parents(b).values()):
                assert a.L(end)==4 and a.degree(end)==4;coldS+=1
            if q==5:
                for e,y,qq in fwd[end]:assert qq==1 and a.L(e)==4 and a.degree(e)==1;coldP+=1
    assert (coldS,coldP)==(128,62)
    result={'status':'PASS_COMPLETE_INDEPENDENT_P1Z_RETURN_CERTIFICATE','BF_contexts':2394,'BF_edges':3698,
        'final_zero_sectors':len(zero),'final_zero_two_way_language_incidences':zero_cover,
        'P1A_BF_compositions':len(cases),'P1A_A_impossible_compositions':sum(not v[0] for v in cases.values()),
        'P1B_composable_sectors':P1B,'all_Q3_output_contexts_degree3plus':q3,
        'producer_seed_groups':len(suppliedgroups),'producer_recent_seed_frames':3992,
        'independent_forward_seed_groups':len(expectedgroups),'independent_recent_seed_frames':sum(map(len,expectedgroups.values())),
        'two_way_combined_seed_language_incidences':cover,'backward_frames':len(records),
        'zero_predecessor_incidences':proposals,'four_leaf_frames':720,
        'state_shapes':[{'leaves':k[0],'marked_root_degree':k[1],'frames':v} for k,v in sorted(shapes.items())],
        'private_explicit_roles':dict(private),'inverse_cases':dict(d.stats),
        'all_Q4_destinations_degree4plus':q4,'all_paired_zero_destinations_L4_degree1':pair,
        'cold_NEG2_S_targets_L4_degree4':coldS,'cold_NEG2_P_targets_L4_degree1':coldP,
        'source_separator':'language excludes (L4,degree1/4); all actual cold NEG2 targets have those shapes',
        'source_engine_calls':a.calls,'new_finite_tests':0,
        'trust':'same agent, distinct immutable splay engine and checker code; no external or formal certification'}
    out('independent_audit.json',result);print(json.dumps(result),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_independent_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,
        'source_engine_calls':a.calls,'old_semantic_rows_replayed':0,'new_finite_tests':0})
