"""Separate immutable source engine, local frame identities, and marked-count audit."""
import itertools,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
sys.path.insert(0,str(ROOT/'python'))
from independent import splay as f
M={1,3,5,7,9,11};account={'source_engine_calls':0,'new_finite_tests':0}
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as h:json.dump(v,h,indent=2)
def term(v):return ('leaf',v) if isinstance(v,str) else f.node(v[0],term(v[1]),term(v[2]))
def mirror(v):return 'F'+str(11-int(v[1:])) if isinstance(v,str) else [12-v[0],mirror(v[2]),mirror(v[1])]
def step(t,x):
    account['source_engine_calls']+=1;return f.trace(t,x)
def core(t):
    if t[0]=='leaf':return None
    l,r=core(t[2]),core(t[3]);return (t[1],l,r) if t[1] in M or l is not None or r is not None else None
def labels(t):return set() if t is None else {t[0]}|labels(t[1])|labels(t[2])
def par(t):
    p={}
    def go(u,a):
        if u[0]=='leaf':return
        if u[1] in M:p[u[1]]=a;a=u[1]
        go(u[2],a);go(u[3],a)
    go(t,None);return p
def child(p,x):return [k for k,v in p.items() if v==x]
def mass(p,x):return 1+sum(mass(p,y) for y in child(p,x))
def leaves(p):return sum(not child(p,k) for k in p)
def depth(t,x):
    d=0
    while t[0]!='leaf':
        if t[1]==x:return d
        t=t[2 if x<t[1] else 3];d+=1
    raise AssertionError(('absent',x))
def word_step(a,b,e,r,mode,x,z):
    a,ae=step(a,x);be=ee=[]
    if mode=='K':
        b,be=step(b,x);r=[x]+[q for q in r if q!=x]
        if x!=z:e,ee=step(e,x)
    return a,b,e,r,[len(ae),sum(v[0]!='ZIG' for v in be),sum(v[0]!='ZIG' for v in ee)]
def rootmap_checks():
    count=0;tests={'q2_into_L2':0,'q2_neutral_L2':0,'cold_q4_shapes':0,'q5_sources':0}
    for vals in itertools.product(*[[j for j in range(6) if j!=i] for i in range(1,6)]):
        p={0:None,**{i:vals[i-1] for i in range(1,6)}};ok=True
        for i in range(1,6):
            seen=set();k=i
            while k is not None and k not in seen:seen.add(k);k=p[k]
            if k is not None:ok=False;break
        if not ok:continue
        count+=1;L=leaves(p)
        for x in range(1,6):
            ancestors=[];k=p[x]
            while k is not None:ancestors.append(k);k=p[k]
            q=len(ancestors);n=p.copy();n[x]=None
            for g in ancestors:n[g]=x
            if q==2 and leaves(n)==2:
                tests['q2_into_L2']+=1
                assert not child(p,x) and L in (2,3)
                sizes=sorted(mass(n,y) for y in child(n,x))
                assert sizes==([1,4] if L==2 else [2,3])
                if L==2:
                    tests['q2_neutral_L2']+=1
                    assert sorted(mass(p,y) for y in child(p,0)) in ([5],[2,3])
            if q==4 and not child(p,x):
                tests['cold_q4_shapes']+=1
                assert L==2 and len(child(p,0)) in (1,2)
                if len(child(p,0))==2:assert sorted(mass(p,y) for y in child(p,0))==[1,4]
            if q==5:
                tests['q5_sources']+=1;assert L==1
            if q>=2:assert len(child(n,x))>=2
            if q==3:assert leaves(n)>=3
            if q==4:assert leaves(n)>=4
    assert count==1296
    return {'rooted_labeled_marked_parent_maps':count,'count_checks':tests,
        'scope':'independent finite stress-check of universal count identities; no BST realization or weighted graph claim'}
def main():
    fam=json.loads((B/'partial_family.json').read_text());cases=[]
    for refl in (False,True):
        conv=mirror if refl else lambda q:q;a=b=e=term(conv(fam['initial']));z=9 if refl else 3
        for mode,k in fam['reaching_prefix']:
            x=12-k if refl else k;a=step(a,x)[0]
            if mode=='K':
                b=step(b,x)[0]
                if x!=z:e=step(e,x)[0]
        assert a==b==term(conv(fam['initial'])) and e==term(conv(fam['auxiliary_recurrent_start']))
        r=[]
        for mode,x in reversed(fam['word']):
            if mode=='K' and x not in r:r.append(x)
        if refl:r=[12-x for x in r]
        r0=r[:];tot=[0,0,0]
        for row,chart in zip(fam['rows'],fam['charts']):
            assert (a,b,e)==tuple(term(conv(q)) for q in row['before'])
            x=12-row['target'] if refl else row['target'];old=r[:]
            a,b,e,r,cost=word_step(a,b,e,r,row['mode'],x,z)
            assert (a,b,e)==tuple(term(conv(q)) for q in row['after'])
            assert cost==[row['a'],row['qF'],row['qE']];tot=[i+j for i,j in zip(tot,cost)]
            assert r==([12-q for q in chart['recent_after']] if refl else chart['recent_after'])
            assert (row['mode']=='K' and x not in old[:5])==chart['cold']
            pb=par(b);pos={x:i for i,x in enumerate(r)}
            assert all(v is None or pos[v]<pos[k] for k,v in pb.items())
            assert e[1]==next(k for k in r if k!=z) and labels(core(b))==set(range(1,12))
        assert a==b==term(conv(fam['initial'])) and e==term(conv(fam['auxiliary_recurrent_start'])) and r==r0
        assert tot==[fam['costs'][k] for k in ('A','QF','QE')]
        # Complete zero suffix from the new post-first-loss state. All actual
        # zero types are included or excluded by marked depth/A depth budget.
        post=fam['critical'][0]['post_first_loss'];front=fam['critical'][0]['frontier_state']
        aa,bb=term(conv(post['A'])),term(conv(post['BF']));fa,fb=term(conv(front['A'])),term(conv(front['BF']))
        actual=[]
        for A0,B0,label in [(aa,bb,'post'),(fa,fb,'frontier')]:
            for x in M:
                if x==B0[1]:continue
                bn,bev=step(B0,x)
                if any(v[0] not in ('LL','RR') for v in bev):continue
                q=len(bev);d=depth(A0,x)
                assert q!=5
                if q==4:assert d>4
                if q==2 and d<=2:
                    an,ae=step(A0,x);assert len(ae)==1 and label=='post'
                    assert (an,bn)==(fa,fb);actual.append(x)
        assert actual==([11] if refl else [1])
        assert depth(fa,1 if refl else 11)==8
        cases.append({'reflected':refl,'all_new_original_operations_and_reaching_prefix_equal':True,
            'costs':fam['costs'],'new_first_loss':'3->2','zero_suffix_exactly_one_possible_move':True,
            'frontier_only_relaxed_B_conditions':True,'cold_A_depth':8,'restricted_zero_suffix_exclusion':True})
    # Exact LL turnaround identity with arbitrary ordered hangers.
    U,V,W,Z=(('leaf',q) for q in 'UV WZ'.replace(' ',''));N=f.node
    source=N(5,N(3,N(1,U,V),W),Z);dest,ev=step(source,1)
    assert dest==N(1,U,N(3,V,N(5,W,Z))) and [v[0] for v in ev]==['LL']
    # Preservation frames for the first upper-cut node a=5, b=7.
    H=[('leaf','H'+str(i)) for i in range(6)];fixed=N(7,H[4],H[5])
    frames=[(N(5,N(3,N(1,H[0],H[1]),H[2]),fixed),1),
            (N(5,N(1,H[0],N(3,H[1],H[2])),fixed),3),
            (N(1,H[0],N(5,N(3,H[1],H[2]),fixed)),3),
            (N(5,N(3,H[0],H[1]),fixed),3)]
    for s,x in frames:
        n,ev=step(s,x);t=n
        while t[1]!=5:t=t[2 if 5<t[1] else 3]
        assert t[3]==fixed
    placement=[]
    for file in ('entry_family','e1_family'):
        old=json.loads((B.parent/'SE03_STEP2_FIRST_LOWERING_04'/f'{file}.json').read_text());p=old['critical'][0]['post_lowering_state']
        pm=par(term(p['BF']));root=p['BF'][0]
        placement.append({'fixture':file,'root':root,'marked_children':child(pm,root),
            'marked_branch_sizes':sorted(mass(pm,x) for x in child(pm,root)),
            'both_marked_children_right':all(x>root for x in child(pm,root))})
    assert placement[1]['both_marked_children_right']
    treechecks=rootmap_checks()
    out('independent_audit.json',{'status':'PASS_STRUCTURAL_SUFFIX_REDUCTION_AND_NEW_SOURCE_WITNESS',
        'new_source_cases':cases,'placement_controls':placement,'parent_count_controls':treechecks,
        'turnaround_exact_free_term_identity':True,'shield_first_upper_node_frames':True,
        'universal_proof_basis':'symbolic source equations/counting/induction in reports, NOT finite negative preparation search',
        'full_E0_suffix_universal':'OPEN','full_E1_suffix_universal':'OPEN','complete_cheap_return':False,
        'independence':'same-agent separate immutable recursive-frame engine and term representation; not external peer review/formal verification',**account})
    print(json.dumps({'status':'PASS_STRUCTURAL_SUFFIX_REDUCTION_AND_NEW_SOURCE_WITNESS','cases':cases,
        'marked_parent_maps':treechecks['rooted_labeled_marked_parent_maps'],**account}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_independent_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,**account})
