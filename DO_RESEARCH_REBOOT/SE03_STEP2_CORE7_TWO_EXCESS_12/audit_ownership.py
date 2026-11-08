"""Two missing-edge completion: exact common-set exchange stability.
Exhaustive small-map controls audit a universal injective-path proof.
No abstract map is claimed to be a realized source or numeric sealed fE.
"""
import collections,importlib.util,itertools,json,time
from pathlib import Path
from two_slot_allocator import extend_two
B=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('licensed_common10',B.parent/'SE03_STEP2_FULL_FUNDING_CLOSURE_10/physical_exchange.py')
X=importlib.util.module_from_spec(spec);spec.loader.exec_module(X)
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def allmaps(D,U):
    for k in range(len(D)+1):
        for ds in itertools.combinations(D,k):
            for us in itertools.permutations(U,k):yield dict(zip(ds,us))
def reverse_common(D,U,l,h):
    inv={u:d for d,u in h.items()};a=dict(l)
    for terminal in U-set(l.values()):
        u=terminal;seen=set()
        while u in inv:
            d=inv[u]
            if d not in l:
                assert d not in a;a[d]=terminal;break
            assert d not in seen;seen.add(d);u=l[d]
    return a
def reverse_all(D,U,a,h):
    inv={u:d for d,u in h.items()};P=D-set(a);ans={}
    for free in U-set(a.values()):
        u=free;seen=set()
        while u in inv:
            d=inv[u]
            if d in P:
                assert d not in ans;ans[d]=free;break
            if d in seen:break
            seen.add(d);u=a[d]
    assert set(ans)==P and len(set(ans.values()))==len(P)
    return ans
def main():
    count=0;branches=collections.Counter();anchorclasses=collections.Counter();seedlocks=collections.Counter();examples={};longest=0
    for n in (3,4):
        D=tuple(range(n));U=set(range(n+1));locks=list(allmaps(D,tuple(sorted(U))))
        for hu in itertools.permutations(sorted(U),n):
            h=dict(zip(D,hu))
            for rr in itertools.combinations(D,2):
                R=set(rr);h0={d:u for d,u in h.items() if d not in R}
                for l in locks:
                    prior=X.exchange(D,U,l,h0);full=X.exchange(D,U,l,h)
                    a=prior['allocation'];assert a==reverse_common(set(D),U,l,h0)
                    ex=extend_two(D,U,a,h)
                    assert ex['allocation']==full['allocation']==reverse_common(set(D),U,l,h)
                    assert ex['additions']==reverse_all(set(D),U,a,h)
                    assert full['total'] and not full['blocked']
                    paths={v['root']:v for v in full['paths']}
                    assert all(paths[v['root']]==v for v in prior['paths'])
                    assert all(full['allocation'][d]==u for d,u in a.items())
                    P=ex['missing'];alpha={p:p if p in R else prior['blocked'][p]['owner'] for p in P}
                    assert set(alpha.values())<=R and len(set(alpha.values()))==len(P)
                    branches[str(len(P))]+=1
                    blocked=sum(p!=alpha[p] for p in P);anchorclasses[str(blocked)]+=1
                    locked_seeds=len(set(h[r] for r in R)&set(a.values()));seedlocks[str(locked_seeds)]+=1
                    nodes=[]
                    for v in ex['paths']:nodes.extend(d for d,u in v['steps'])
                    assert len(nodes)==len(set(nodes));longest=max(longest,len(nodes))
                    # Adding first pair cannot consume the other computed endpoint.
                    if len(P)==2:
                        p0=sorted(P)[0];seq=extend_two(D,U,{**a,p0:ex['additions'][p0]},h)
                        assert seq['additions']=={p:u for p,u in ex['additions'].items() if p!=p0}
                    key=f'holes{len(P)}_blocked{blocked}_seedlocks{locked_seeds}'
                    if key not in examples:examples[key]={'D':D,'U':sorted(U),'R':rr,'h':list(h.items()),'locked':list(l.items()),
                        'paid':list(a.items()),'anchors':list(alpha.items()),'paths':ex['paths'],'additions':list(ex['additions'].items())}
                    count+=1
    assert count==365976 and set(branches)=={'0','1','2'} and anchorclasses['2'] and seedlocks['2']
    # Algebraic U12 extension check only. No 3-slot source class is executed.
    algebra3=0
    D=set(range(4));U=set(range(4))
    for hu in itertools.permutations(range(4)):
        h=dict(zip(range(4),hu))
        for d in range(4):
            for u in range(4):
                a={d:u};adds=reverse_all(D,U,a,h)
                assert len(adds)==3 and len(set(adds.values()))==3
                algebra3+=1
    # A same-first-free rule fails even on actual closed source IDs.
    receipt=json.loads((B/'physical_receipts2.json').read_text());bad=None
    for f in receipt['families']:
        for v in f['fixtures']:
            if len(v['uncovered'])==2:
                p1,p2=v['uncovered'];u=v['Wstar'][0]
                bad={'source_variant':f['variant'],'reflected':f['reflected'],'erased':f['erased'],
                    'demands':[p1,p2],'naive_reused_bit':u,'actual_distinct_extension':v['additions'],
                    'status':'REFUTED_NAIVE_SAME_FIRST_FREE_ALGORITHM_ONLY','owner_fixture':'logical, no numerical sealed fE realization claimed'};break
        if bad:break
    assert bad is not None
    rejections=[]
    for label,D,U,a,h in [('duplicate_bit',{0,1},{0,1},{},{0:0,1:0}),
            ('other_copy_bit',{0,1},{0,1},{},{0:0,1:2}),('three_residual_scope',{0,1,2},{0,1,2},{},{0:0,1:1,2:2})]:
        try:extend_two(D,U,a,h)
        except ValueError:rejections.append(label)
        else:raise AssertionError(label)
    result={'status':'PASS_SIMULTANEOUS_LICENSED_COMMON_EXCHANGE_AND_ALL_OLD_PATHS_STABLE',
        'cases':count,'residual_branches':dict(branches),'blocked_anchor_counts':dict(anchorclasses),
        'seed_bits_already_owned':dict(seedlocks),'longest_total_path':longest,'examples':examples,
        'all_old_assignments_identical':True,'all_old_successful_paths_identical':True,
        'simultaneous_equals_original_common_full_exchange':True,'sequential_second_endpoint_unchanged':True,
        'generic_three_hole_algebra_only':algebra3,'three_slot_source_campaign':'NOT_EXECUTED',
        'pairwise_only_Hall_caution':{'three_demands':[0,1,2],'two_units':[0,1],'every_neighborhood':[0,1],
            'status':'abstract example, each pair matchable but triple not; NOT a source counterexample'},
        'naive_collision':bad,'rejected_invalid_inputs':rejections,
        'universal_proof':'injective finite directed ownership paths cannot merge or enter a cycle; completing h0 only at R preserves every successful common path',
        'source_engine_calls':0,'new_finite_tests':count+algebra3+len(rejections)}
    out('ownership_audit.json',result);print(json.dumps({k:v for k,v in result.items() if k not in ('examples','naive_collision','pairwise_only_Hall_caution')}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_ownership_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0})
