"""Independent immutable-engine derivation and backwards one-hole audit.
No primary source engine or geometry producer implementation is imported.
The public allocator is called as a black box against different checks.
"""
import collections,functools,importlib.util,itertools,json,sys,time
from pathlib import Path
from single_slot_allocator import extend_one
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
spec=importlib.util.spec_from_file_location('immutable_separate11',ROOT/'python/independent/splay.py')
I=importlib.util.module_from_spec(spec);spec.loader.exec_module(I)
started=time.process_time();calls=0;CAP=min(80,float(sys.argv[1])-4)
def move(t,x):
    global calls
    calls+=1;assert calls<1500000 and time.process_time()-started<CAP
    return I.trace(t,x)
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
@functools.lru_cache(None)
def alltrees(lo,hi):
    if lo>hi:return (('leaf',hi),)
    return tuple(I.node(k,l,r) for k in range(lo,hi+1) for l in alltrees(lo,k-1) for r in alltrees(k+1,hi))
def readB(t):return ('leaf',int(t[1:])) if isinstance(t,str) else I.node(t[0],readB(t[1]),readB(t[2]))
def L(t):return 0 if t[0]=='leaf' else 1 if t[2][0]==t[3][0]=='leaf' else L(t[2])+L(t[3])
def core(t,M):
    if t[0]=='leaf':return set()
    a,b=core(t[2],M),core(t[3],M)
    return a|b|{t[1]} if a or b or t[1] in M else set()
def qb(e):return sum(z[0]!='ZIG' for z in e)
def reflected(t):return ('leaf',7-t[1]) if t[0]=='leaf' else I.node(8-t[1],reflected(t[3]),reflected(t[2]))
def reverse_endpoint(D,U,a,h,p):
    inv={u:d for d,u in h.items()};matches=[]
    for unit in U-set(a.values()):
        u=unit;seen=set()
        while u in inv:
            d=inv[u]
            if d==p:matches.append(unit);break
            if d in seen:break
            seen.add(d);u=a[d]
    assert len(matches)==1
    return matches[0]
def main():
    # Independently derive all contexts/edges before reading primary table.
    ts=set(alltrees(1,7));assert len(ts)==429
    edges=set();inc=collections.defaultdict(list);hin=collections.Counter()
    for t in ts:
        for x in range(1,8):
            dest,ev=move(t,x);Q=qb(ev)
            assert dest in ts
            if Q==3:assert I.lookup(t,x)[1]==6 and L(t)==1
            if L(dest)==1:assert Q<=1;hin[Q]+=1
            edges.add((t,x,dest,Q));inc[dest].append((t,x,Q))
    supplied=json.loads((B/'geometry_certificate.json').read_text());primarytrees=[readB(t) for t in supplied['trees']]
    declared={(primarytrees[v['source']],v['target_key'],primarytrees[v['destination']],v['Q']) for v in supplied['transitions']}
    assert declared==edges and set(primarytrees)==ts
    classes=[];deep=[];predcount=0
    for u in range(2,7):
        M=set(range(1,8))-{u};valid={t for t in ts if t[1] in M and core(t,M)==set(range(1,8))}
        admitted=[v for v in edges if v[0] in valid and v[2] in valid and v[1] in M and v[1]!=v[0][1]]
        dd=[v for v in admitted if v[3]==3]
        for t,x,end,Q in dd:
            pp=[v for v in inc[t] if v[0] in valid and v[1] in M and v[1]!=v[0][1]]
            assert pp and all(v[2]<=1 for v in pp);predcount+=len(pp);deep.append((u,t,x,end))
        classes.append((u,len(valid),len(admitted),len(dd)))
    assert classes==[(v['unmarked'],v['core_contexts'],v['admitted_genuine_edges'],v['Q3_sectors']) for v in supplied['classes']]
    assert len(deep)==132 and predcount==198
    assert all((reflected(t),8-x,reflected(end),Q) in edges for t,x,end,Q in edges)
    # Exact new full/erased actual source trajectories, all old frame fields.
    receipts=json.loads((B/'physical_receipts2.json').read_text());source=[];fixtures=0;period_transports=0
    for fam in receipts['families']:
        R=readB(fam['initial_A_BF']);E0=readB(fam['initial_BE']);z=fam['erased'];A=BF=R;E=E0
        word=[tuple(v) for v in fam['word']];marks={x for m,x in word if m=='K'};U=set();D=set();Ec=set();sums=[0,0,0]
        Eprefix=R
        for copy in range(fam['alignment']['u']):
            for m,x in word:
                if m=='K' and x!=z:Eprefix=move(Eprefix,x)[0]
        assert Eprefix==E0
        for row,(m,x),chart in zip(fam['rows'],word,fam['charts']):
            t=row['occurrence'];assert core(BF,marks)==set(range(1,8))
            assert (A,BF,E)==tuple(readB(v) for v in row['before'])
            A,ae=move(A,x);be=ee=[]
            if m=='K':
                BF,be=move(BF,x)
                if x!=z:E,ee=move(E,x)
            assert (A,BF,E)==tuple(readB(v) for v in row['after'])
            assert [len(ae),qb(be),qb(ee)]==[row['a'],row['qF'],row['qE']]
            U|={(t,j,b) for j in range(1,len(ae)+1) for b in (0,1)}
            D|={(t,k) for k in range(1,qb(be)+1)};Ec|={(t,k) for k in range(1,qb(ee)+1)}
            sums=[a+b for a,b in zip(sums,(len(ae),qb(be),qb(ee)))]
        assert (A,BF,E)==(R,R,E0) and len(marks)==6
        mm=fam['macros'];h0={};spares=[];excess=[]
        for i,m in enumerate(mm):
            uu=[u for t in m['occurrences'] for u in sorted(U) if u[0]==t]
            dd=[d for t in m['occurrences'] for d in sorted(D) if d[0]==t]
            assert len(uu)==2*m['H'] and len(dd)==m['Q']
            n=min(len(uu),len(dd));h0.update(zip(dd[:n],uu[:n]));excess+=dd[n:]
            if len(uu)>len(dd):spares.append((i,uu[len(dd)]))
        assert len(excess)==1 and tuple(fam['R'])==excess[0] and spares
        h={tuple(v['demand']):tuple(v['unit']) for v in fam['independent_h']}
        assert h=={**h0,excess[0]:spares[0][1]} and len(set(h.values()))==len(h)==len(D)
        assert mm[fam['preceding_macro']]['Q']<=1 and fam['positive_surplus']>=1
        for f in fam['fixtures']:
            a={tuple(v['demand']):tuple(v['unit']) for v in f['paid']};p=tuple(f['missing']);u=tuple(f['new_unit'])
            assert set(a)==D-{p} and len(set(a.values()))==len(a)
            assert u==reverse_endpoint(D,U,a,h,p) and u not in set(a.values()) and u in U
            final={tuple(v['demand']):tuple(v['unit']) for v in f['final']}
            assert final=={**a,p:u} and len(set(final.values()))==len(final)==len(D)
            cur=p
            for d,v in f['path']:
                d=tuple(d);v=tuple(v);assert d==cur and h[d]==v
                if v in set(a.values()):cur=next(k for k,w in a.items() if w==v)
            assert tuple(f['path'][-1][1])==u
            fixtures+=1
        # BOTH donor and demand IDs transported through every possible cut.
        T=len(word);base=fam['alignment']['u']*T
        for delta in range(T):
            tau=lambda t:base+t if t>delta else base+t+T
            units={(tau(t),j,b) for t,j,b in U};dd={(tau(t),k) for t,k in D}
            mapped={(tau(d[0]),d[1]):(tau(v[0]),v[1],v[2]) for d,v in h.items()}
            assert set(mapped)==dd and set(mapped.values())<=units and len(set(mapped.values()))==len(mapped)
            period_transports+=1
        source.append({'reflected':fam['reflected'],'A':sums[0],'QF':sums[1],'QE':sums[2],
            'actual_R':list(excess[0]),'common_ordinal_demands':len(D&Ec),'source_units':len(U),'full_demands':len(D),
            'positive_surplus':fam['positive_surplus'],'genuine_core':7,'closure_A_BF_BE':True,
            'actual_fE':'any supplied certified owner map; NO fixture is claimed to be its numeric realization'})
    # Generic one-hole algorithm versus a distinct BACKWARDS verifier.
    cases=0;tight=0;maxpath=0
    for nU in (4,5):
        DD=tuple(range(4));UU=set(range(nU))
        for hs in itertools.permutations(sorted(UU),4):
            h=dict(zip(DD,hs))
            for p in DD:
                ds=tuple(d for d in DD if d!=p)
                for aa in itertools.permutations(sorted(UU),3):
                    paid=dict(zip(ds,aa));r=extend_one(DD,UU,paid,h)
                    assert r['unit']==reverse_endpoint(set(DD),UU,paid,h,p)
                    assert r['allocation']=={**paid,p:r['unit']}
                    maxpath=max(maxpath,len(r['path']));cases+=1;tight+=int(nU==4)
    assert cases==31104 and tight==2304
    result={'status':'PASS_COMPLETE_INDEPENDENT_C7_ONE_SLOT_COMPONENTS',
        'all_seven_Score_contexts':len(ts),'all_access_edges':len(edges),'Hamiltonian_incoming_by_Q':dict(hin),
        'five_mark_masks_source_classes':classes,'Q3_sectors':len(deep),'preceding_sector_incidences':predcount,
        'all_reflected_edges_checked':len(edges),'actual_source_reports':source,'source_paid_fixtures':fixtures,
        'period_cut_transports':period_transports,'one_hole_map_cases':cases,'tight_inventory_cases':tight,'maximum_map_path':maxpath,
        'universal_geometry':'second same-side double preserves a Score fork; no finite population inference',
        'universal_ownership':'complete h plus injective all-paid a -> free terminal, with ALL previous values fixed',
        'frozen_fE':'parametric ALL supplied certified maps; source never narrowed to auxiliary core9 and no fE values guessed',
        'source_eligibility':'inherited actual-period counting-unit/block-cyclic exchange, no new native policy',
        'source_engine_calls':calls,'new_finite_tests':cases+fixtures,
        'scope':'exactly core7 ONE excess slot only; Step2 and other classes OPEN',
        'trust':'same-agent distinct immutable source engine and backwards ownership checker, not external/formal certification'}
    out('independent_audit.json',result);print(json.dumps({k:v for k,v in result.items() if k not in ('actual_source_reports','five_mark_masks_source_classes')}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_independent_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,
        'source_engine_calls':calls,'new_finite_tests':31110})
