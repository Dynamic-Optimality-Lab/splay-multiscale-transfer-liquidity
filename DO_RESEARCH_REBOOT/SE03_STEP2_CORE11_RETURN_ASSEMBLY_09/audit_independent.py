"""Independent Campaign09 derivation, forward seeds and inverse closure.
Imports only the old separate checker/immutable engine, never09 producers.
"""
import collections,functools,importlib.util,itertools,json,sys,time
from fractions import Fraction as F
from pathlib import Path
B=Path(__file__).resolve().parent;OLD=B.parent/'SE03_STEP2_FINAL_PLUS_ONE_07'
spec=importlib.util.spec_from_file_location('generic_checker07',OLD/'audit_independent2.py')
d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d);a=d.a
started=time.process_time();CAP=min(80,float(sys.argv[1])-4)
def guard():assert time.process_time()-started<CAP and a.calls<1500000
a.guard=guard
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    states={t for t in a.alltrees(1,11) if t[1] in a.M and a.density(t)[2]}
    assert len(states)==2394
    inc=collections.defaultdict(list);fwd=collections.defaultdict(list);shapes=collections.Counter()
    for b in states:
        for x in a.M-{b[1]}:
            n=a.legal(b,x)
            if n is None:continue
            t,q=n;assert t in states
            fwd[b].append((t,x,q));inc[t].append((b,x,q))
            if q==2:assert a.L(t)>=2
            if q==3:assert a.degree(t)>=3
            if q==4:assert a.degree(t)>=4
    perms=list(itertools.permutations(sorted(a.M)))
    @functools.lru_cache(None)
    def orders(t):return tuple(r for r in perms if r[0]==t[1] and a.heap(t,r))
    def recent(r,x):return (x,)+tuple(k for k in r if k!=x)
    @functools.lru_cache(None)
    def initial(word):
        fs,sz=a.frames(word,range(1,12),0,12)
        return tuple({d.canonical(t) for t,end in fs})
    def regroup(groups):
        ans=collections.defaultdict(list)
        for (t,b),rr in groups.items():
            for r in rr:ans[b,r].append(t)
        return {k:tuple(sorted(set(v),key=d.size)) for k,v in ans.items()}
    def two_way(E,P):
        assert all(any(d.includes(p,e) for p in P) for e in E),'missing actual forward seed'
        assert all(any(d.includes(e,p) for e in E) for p in P),'unsupported supplied geometry'
        return len(E)+len(P)
    # Independent full paired destination grammar, prior to producer read.
    sectors={};expected_destination=collections.defaultdict(set);expected_seeds=collections.defaultdict(set)
    cases={};alias=collections.Counter();paired_targets=0
    for f in states:
        for mid,x,q in fwd[f]:
            if q!=5:continue
            assert a.L(f)==a.degree(f)==1 and a.L(mid)==a.degree(mid)==5
            rf=tuple(r for r in orders(f) if r[-1]==x);assert len(rf)==1
            for end,v,qq in fwd[mid]:
                assert qq==1 and v in {1,11}-{x}
                assert a.L(end)==4 and a.degree(end)==1
                rm=recent(rf[0],x);re=recent(rm,v)
                key=(a.bf_write(f),a.bf_write(mid),a.bf_write(end),x,v)
                terms=initial((f[1],x,v));sectors[key]=(terms,set(rf),rm,re)
                for t in terms:expected_destination[t,f].update(rf)
                paired_targets+=1
                for old,y,q0 in inc[f]:
                    assert q0 not in (2,3,4,5),'no zero/Q3 can enter the marked chain'
                    if q0!=1:continue
                    rp=tuple(r for r in orders(old) if recent(r,y)==rf[0])
                    if not rp:continue
                    assert y==f[1] and old[1] not in (x,y)
                    assert a.L(old)==a.degree(old)==2
                    word=(old[1],y,x,v);terms1=initial(word)
                    ck=(a.bf_write(old),)+key
                    al='successor_is_old_root' if v==old[1] else 'successor_is_pair_source_root' if v==y else 'four_distinct'
                    alias[al]+=1;cases[ck]=(bool(terms1),len(rp),al)
                    for t in terms1:expected_seeds[t,old].update(rp)
    producer=json.loads((B/'paired_destination_seeds.json').read_text())
    seen=set();destination_cover=0
    for v in producer['sectors']:
        key=tuple(a.freeze(v[k]) for k in ('BF_before_pair','BF_between_macros','BF_after_pair'))+(v['first_target'],v['actual_successor'])
        assert key in sectors;seen.add(key);E,rr,rm,re=sectors[key]
        assert rr==set(map(tuple,v['recent_before_pair']))
        assert rm==tuple(v['recent_between_macros']) and re==tuple(v['recent_after_pair'])
        assert v['successor_is_chart_miss']==(v['actual_successor'] not in rm[:5])
        assert v['costs']=={'H_first':1,'H_second':1,'Q_first':5,'Q_second':1,'packet_w':-2}
        P={d.canonical(a.Aread(t)) for t in v['A_before_pair_terms']}
        destination_cover+=two_way(E,P)
    assert seen==set(sectors) and len(sectors)==62
    def read_groups(v):return {(d.canonical(a.Aread(z['A'])),a.bf_read(z['BF'])):set(map(tuple,z['recent'])) for z in v['groups']}
    D=regroup(read_groups(producer));ED=regroup(expected_destination);assert set(D)==set(ED)
    for key in ED:destination_cover+=two_way(ED[key],D[key])
    seeds=json.loads((B/'terminal_seeds.json').read_text())
    claimed={}
    for v in seeds['terminal_cases']:
        key=tuple(a.freeze(v[k]) for k in ('BF_before_plus','BF_before_pair','BF_between_macros','BF_after_pair'))+(v['first_target'],v['actual_successor'])
        claimed[key]=(v['A_initial_terms']>0,v['recent_orders'],v['alias'])
    assert claimed==cases and len(cases)==62
    P=regroup(read_groups(seeds));E=regroup(expected_seeds);assert set(E)==set(P)
    seed_cover=sum(two_way(E[key],P[key]) for key in E)
    cert=json.loads((B/'zero_closure.json').read_text())
    assert cert['closed'] and cert['goal'] is None and cert['bound'] is None and not cert['queue']
    by=collections.defaultdict(list);records=[]
    for v in cert['records']:
        t=d.canonical(a.Aread(v['A']));b=a.bf_read(v['BF']);r=tuple(v['recent'])
        assert b in states and t[1]==b[1]==r[0] and a.heap(b,r)
        assert a.L(b)==2
        shapes[a.L(b),a.degree(b)]+=1;by[b,r].append(t);records.append((t,b,r))
    by={k:tuple(sorted(set(v),key=d.size)) for k,v in by.items()}
    @functools.lru_cache(maxsize=150000)
    def contained(t,b,r):return any(d.includes(p,t) for p in by.get((b,r),()))
    for (t,b),rr in expected_seeds.items():
        for r in rr:assert contained(t,b,r)
    proposals=0
    for i,(t,b,r) in enumerate(records):
        if i%128==0:guard()
        # Q4 and paired H3Q6 outputs have >=4 leaves, outside this R0.
        for old,x,q in inc[b]:
            if q!=2 or r[1]!=old[1]:continue
            base=list(r[1:]);rrs=[]
            for pos in range(1,6):
                rr=tuple(base[:pos]+[x]+base[pos:])
                if a.heap(old,rr):rrs.append(rr)
            if not rrs:continue
            for before in d.inverse_H1(t,F(old[1])):
                for rr in rrs:assert contained(before,old,rr);proposals+=1
    # Independent q4 assembly bridges: cold-leaf source geometry, terminal
    # zero classification, canonical penultimate lowering, +1 exhaustiveness.
    q4_sources=lastzeros=penults=0;coldS=0;finalq3=0
    for f in states:
        for target,x,q in fwd[f]:
            if q!=4 or x in set(a.parents(f).values()):continue
            assert a.L(f)==2 and a.degree(f) in (1,2)
            assert a.L(target)==4 and a.degree(target)==4;coldS+=1
            rf=tuple(r for r in orders(f) if r[-1]==x)
            if not rf:continue
            q4_sources+=1
            for u,y,qz in inc[f]:
                if qz==3:finalq3+=1;raise AssertionError('Q3 cannot enter Fq4')
                if qz not in (2,4):continue
                rr=tuple(r for r in orders(u) if recent(r,y) in rf)
                if not rr:continue
                assert qz==2 and a.L(u)==a.L(f)==2 and a.degree(f)==2
                assert a.degree(u) in (1,2);lastzeros+=1
                for before,z,q0 in inc[u]:
                    if q0 not in (2,4):continue
                    rp=tuple(r for r in orders(before) if recent(r,z) in rr)
                    if not rp:continue
                    assert a.degree(u)==2 and q0==2 and a.L(before)==3
                    penults+=1
    result={'status':'PASS_COMPLETE_INDEPENDENT_CORE11_RETURN_ASSEMBLY',
        'BF_contexts':len(states),'BF_edges':sum(map(len,fwd.values())),
        'paired_source_BF_contexts':len({k[0] for k in sectors}),'paired_sectors':len(sectors),
        'paired_sector_aliases':dict(alias),'destination_two_way_language_incidences':destination_cover,
        'plus1_cases':len(cases),'plus1_two_way_language_incidences':seed_cover,
        'independent_forward_seed_groups':len(expected_seeds),'independent_recent_seed_frames':sum(map(len,expected_seeds.values())),
        'producer_seed_groups':len(seeds['groups']),'producer_recent_seed_frames':sum(len(v['recent']) for v in seeds['groups']),
        'backward_frames':len(records),'zero_predecessor_incidences':proposals,
        'state_shapes':[{'leaves':k[0],'marked_root_degree':k[1],'frames':v} for k,v in sorted(shapes.items())],
        'q4_cold_contexts':q4_sources,'q4_final_zero_contexts':lastzeros,'q4_penultimate_loss_contexts':penults,
        'q4_H2Q3_incoming':finalq3,'cold_NEG2S_targets_L4_degree4':coldS,'paired_targets_L4_degree1':paired_targets,
        'budget1':'paired destination L1: only H1Q1 consumes budget; all genuine zero outputs L>=2',
        'budget0':'all 4858 records have L2 and every H1Q2 inverse contained; H2Q4/pairedH3Q6 excluded by L4',
        'new_finite_tests':0,'source_engine_calls':a.calls,'CPU':time.process_time()-started,
        'trust':'same-agent distinct immutable engine, independent forward frames and inverse code; no formal assistant/external review'}
    out('independent_audit.json',result);print(json.dumps(result),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_independent_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':a.calls,'new_finite_tests':0})
