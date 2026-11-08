"""Campaign07 independent full seed and ZERO-language audit.

Separate immutable engine, independent forward seeds, inverse algebra and
typed tree-language inclusion. No primary producer/predecessor code imported.
"""
import collections,functools,itertools,json,sys,time
from fractions import Fraction as F
from pathlib import Path
B=Path(__file__).resolve().parent;OLD=B.parent/'SE03_STEP2_TERMINAL_PAIR_06'
sys.path.insert(0,str(OLD))
import audit_independent as a
assert Path(a.__file__).resolve()==OLD/'audit_independent.py'
started=time.process_time();CAP=min(120,float(sys.argv[1])-4)
stats=collections.Counter()
def guard():
    assert time.process_time()-started<CAP and a.calls<1500000
a.guard=guard
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def canonical(t):
    allkeys=a.keys(t);bygap=collections.defaultdict(list)
    for k in allkeys:
        if k.denominator!=1:bygap[k.numerator//k.denominator].append(k)
    m={F(k):F(k) for k in range(13)}
    for gap,ks in bygap.items():
        ks=sorted(ks)
        for j,k in enumerate(ks,1):m[k]=F(gap)+F(j,len(ks)+1)
    def go(v):
        if v[0]=='leaf':return a.slot(m[v[1]],m[v[2]])
        return a.I.node(m[v[1]],go(v[2]),go(v[3]))
    return go(t)
def size(t):return 0 if t[0]=='leaf' else 1+size(t[2])+size(t[3])
@functools.lru_cache(maxsize=500000)
def includes(p,q):
    # A different language-inclusion implementation: collect a variable
    # unifier first, then check strict order and ALL free-slot intervals.
    bind={F(k):F(k) for k in range(13)};holes=[]
    def unify(x,y):
        if x[0]=='leaf':holes.append((x,y));return True
        if y[0]=='leaf':return False
        k,v=x[1],y[1]
        if k.denominator==1:
            if k!=v:return False
        else:
            if v.denominator==1 or k.numerator//k.denominator!=v.numerator//v.denominator:return False
            if k in bind and bind[k]!=v:return False
            bind[k]=v
        return unify(x[2],y[2]) and unify(x[3],y[3])
    if not unify(p,q):return False
    order=[bind[k] for k in sorted(bind)]
    if any(x>=y for x,y in zip(order,order[1:])):return False
    def within(v,lo,hi):
        if v[0]=='leaf':return lo<=v[1]<v[2]<=hi
        return lo<v[1]<hi and within(v[2],lo,hi) and within(v[3],lo,hi)
    return all(within(v,bind[h[1]],bind[h[2]]) for h,v in holes)
def get(t,p):
    for d in p:
        if t[0]=='leaf':return None
        t=t[2+d]
    return t
def extend(t,p,k=None):
    v=get(t,p)
    if v is None:return []
    if v[0]!='leaf':return [t] if k is None or v[1]==k else []
    _,lo,hi=v
    if k is not None:opts=[k] if lo<k<hi else []
    else:
        cuts=sorted(set(a.keys(t)+list(map(F,range(1,12)))+[lo,hi]))
        opts=[k for k in cuts if lo<k<hi]+[(l+r)/2 for l,r in zip(cuts,cuts[1:]) if lo<=l<r<=hi]
    return [a.replace_at(t,p,a.fresh(x,lo,hi)) for x in opts]
@functools.lru_cache(maxsize=50000)
def inverse_H1(t,oldroot):
    # Output frame positions for (old grandparent, optional old parent).
    # Each inverse is checked by the separate engine on arbitrary free slots.
    specs=[('zigL',(1,),None),('zigR',(0,),None),('LL',(1,1),(1,)),
           ('RR',(0,0),(0,)),('LR',(1,),(0,)),('RL',(0,),(1,))]
    result=set();x=t[1]
    for kind,gpos,ppos in specs:
        variants=[t]
        if ppos is not None:variants=[z for v in variants for z in extend(v,ppos)]
        variants=[z for v in variants for z in extend(v,gpos,oldroot)]
        for z in variants:
            l,r=z[2:]
            if kind=='zigL':_,gg,A,D=r;before=a.I.node(gg,a.I.node(x,l,A),D)
            elif kind=='zigR':_,gg,A,D=l;before=a.I.node(gg,A,a.I.node(x,D,r))
            elif kind=='LL':_,pp,A,R=r;_,gg,C,D=R;before=a.I.node(gg,a.I.node(pp,a.I.node(x,l,A),C),D)
            elif kind=='RR':_,pp,L,C=l;_,gg,A,Z=L;before=a.I.node(gg,A,a.I.node(pp,Z,a.I.node(x,C,r)))
            elif kind=='LR':_,pp,A,Z=l;_,gg,C,D=r;before=a.I.node(gg,a.I.node(pp,A,a.I.node(x,Z,C)),D)
            else:_,gg,A,Z=l;_,pp,C,D=r;before=a.I.node(gg,A,a.I.node(pp,a.I.node(x,Z,C),D))
            after,ev=a.splay(before,x)
            assert after==z and len(ev)==1 and includes(t,z)
            stats['inverse_'+kind]+=1;result.add(canonical(before))
    return tuple(result)
def main():
    states={t for t in a.alltrees(1,11) if t[1] in a.M and a.density(t)[2]};assert len(states)==2394
    inc=collections.defaultdict(list);fwd=collections.defaultdict(list);q4=pair=0
    for t in states:
        for x in a.M-{t[1]}:
            v=a.legal(t,x)
            if v is None:continue
            z,q=v;assert z in states
            fwd[t].append((z,x,q));inc[z].append((t,x,q))
            if q==2:assert a.L(z)>=2
            if q==4:assert a.L(z)>=4;q4+=1
    for t in states:
        for z,x,q in fwd[t]:
            if q!=5:continue
            for e,y,qq in fwd[z]:assert qq==1 and a.L(e)==4;pair+=1
    perms=list(itertools.permutations(sorted(a.M)))
    @functools.lru_cache(None)
    def orders(t):return tuple(r for r in perms if r[0]==t[1] and a.heap(t,r))
    @functools.lru_cache(None)
    def seedA(word):
        fs,sz=a.frames(word,range(1,12),0,12)
        return tuple({canonical(initial) for initial,end in fs})
    # Derive the terminal cases BEFORE reading the producer's claimed table.
    cases={};expectedgroups=collections.defaultdict(set)
    for b in states:
        for end,y,q in fwd[b]:
            if q!=1:continue
            for probe,x,qx in fwd[end]:
                if qx!=4:continue
                rr=[]
                for r in orders(b):
                    new=(y,)+tuple(k for k in r if k!=y)
                    if new[-1]!=x:continue
                    assert a.heap(end,new) and x not in set(a.parents(end).values())
                    rr.append(r)
                if not rr:continue
                initial=seedA((b[1],y,x));key=(a.bf_write(b),a.bf_write(end),y,x)
                cases[key]=(len(initial),len(rr),a.L(b),a.L(end))
                for t in initial:expectedgroups[(t,b)].update(rr)
    producer=json.loads((B/'terminal_seeds.json').read_text())
    claimedcases={(a.freeze(v['BF_before']),a.freeze(v['BF_after_plus']),v['plus_target'],v['cold_q4']):
                  (v['A_initial_terms'],v['recent_orders'],v['L_before'],v['L_after']) for v in producer['terminal_cases']}
    assert cases==claimedcases and len(cases)==144
    suppliedgroups={}
    for v in producer['groups']:
        t=canonical(a.Aread(v['A']));b=a.bf_read(v['BF']);suppliedgroups[(t,b)]=set(map(tuple,v['recent']))
    assert suppliedgroups==dict(expectedgroups)
    assert len(expectedgroups)==3136 and sum(map(len,expectedgroups.values()))==12480
    cert=json.loads((B/'zero_closure.json').read_text());assert cert['closed'] and cert['goal'] is None and cert['bound'] is None
    by=collections.defaultdict(list);records=[];leaves=collections.Counter();private=collections.Counter()
    for v in cert['records']:
        t=canonical(a.Aread(v['A']));b=a.bf_read(v['BF']);r=tuple(v['recent'])
        assert b in states and t[1]==b[1]==r[0] and a.heap(b,r)
        ell=a.L(b);assert 1<=ell<=3
        leaves[ell]+=1;private[sum(k.denominator!=1 for k in a.keys(t))]+=1
        by[b,r].append(t);records.append((t,b,r))
    for k,vs in by.items():by[k]=tuple(sorted(set(vs),key=size))
    @functools.lru_cache(maxsize=250000)
    def contained(t,b,r):return any(includes(p,t) for p in by.get((b,r),()))
    # Every true terminal seed, including the empty zero prefix, is covered.
    for (t,b),rr in expectedgroups.items():
        for r in rr:assert contained(t,b,r)
    proposals=0
    for n,(t,b,r) in enumerate(records):
        if n%128==0:guard()
        # All H2Q4 / paired H3Q6 outputs have L>=4, so none can enter R.
        for old,x,q in inc[b]:
            if q!=2 or r[1]!=old[1]:continue
            base=list(r[1:])
            prior=[]
            for pos in range(1,6):
                rr=tuple(base[:pos]+[x]+base[pos:])
                if a.heap(old,rr):prior.append(rr)
            if not prior:continue
            for before in inverse_H1(t,F(old[1])):
                for rr in prior:
                    assert contained(before,old,rr),'a genuine zero predecessor has no certified containing term'
                    proposals+=1
    assert len(records)==32436 and dict(leaves)=={1:2600,2:4444,3:25392}
    result={'status':'PASS_COMPLETE_INDEPENDENT_FINAL_PLUS1_CERTIFICATE',
        'BF_density_contexts':2394,'original_SS_edges':sum(map(len,fwd.values())),
        'terminal_cases':len(cases),'new_seed_term_BF_groups':len(expectedgroups),'seed_full_recent_frames':12480,
        'closed_backward_frames':len(records),'leaf_distribution':dict(leaves),'private_explicit_node_distribution':dict(private),
        'independently_checked_zero_predecessors':proposals,'inverse_source_cases':dict(stats),
        'q4_zero_output_contexts_L4plus':q4,'all_q5_q1_output_contexts_L4':pair,
        'H0Q0':'projected identity, not a genuine full macro; auxiliary effect unconstrained',
        'new_arbitrary_private_helpers':'H2/P3 outputs excluded by BF leaves, not by inventory bound',
        'negative_target_separation':'every cold NEG2 targetL4; all backward framesL<=3',
        'source_engine_calls':a.calls,'new_finite_tests':0,
        'trust':'same agent, distinct immutable engine and independent derivations; no formal assistant or external peer review'}
    out('independent_audit.json',result);print(json.dumps(result),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_independent_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':a.calls,'new_finite_tests':0})
