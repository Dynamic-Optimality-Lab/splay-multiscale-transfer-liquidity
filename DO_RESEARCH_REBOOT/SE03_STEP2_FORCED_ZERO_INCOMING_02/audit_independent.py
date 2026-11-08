"""Separate recursive-frame engine and derivations; no source search imported.
This is an independent implementation audit by the same agent, not peer review.
"""
import hashlib,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
sys.path.insert(0,str(ROOT/'python'))
from independent import splay as f
account={'source_engine_calls':0,'new_finite_tests':0}
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as g:json.dump(v,g,indent=2)
def term(v):return ('leaf',v) if isinstance(v,str) else f.node(v[0],term(v[1]),term(v[2]))
def step(v,x):
    account['source_engine_calls']+=1
    return f.trace(v,x)
def mirror(v):
    if isinstance(v,str):return 'F'+str(11-int(v[1:]))
    return [12-v[0],mirror(v[2]),mirror(v[1])]
M=set((1,3,5,7,9,11))
def core(v):
    if isinstance(v,str):return None
    l,r=core(v[1]),core(v[2])
    return (v[0],l,r) if v[0] in M or l is not None or r is not None else None
def walk(v):
    if v is not None:
        yield v
        yield from walk(v[1]);yield from walk(v[2])
def leafcount(v):return sum(q[0] in M and q[1] is None and q[2] is None for q in walk(v))
def Uunary(v):return all(q[0] in M or q[1] is None or q[2] is None for q in walk(v))
def main():
    fam=json.loads((B/'incoming_family_v2.json').read_text());initial=fam['initial_A_B'];er=fam['auxiliary_recurrent_start']
    for refl in (False,True):
        conv=mirror if refl else lambda q:q
        a=b=term(conv(initial));e=term(conv(er));z=5 if refl else 7
        costs=[0,0,0]
        for row in fam['rows']:
            x=12-row['target'] if refl else row['target'];a,ae=step(a,x);be=ee=[]
            if row['mode']=='K':b,be=step(b,x)
            if row['mode']=='K' and x!=z:e,ee=step(e,x)
            assert (a,b,e)==tuple(term(conv(t)) for t in row['after'])
            got=[len(ae),sum(q[0]!='ZIG' for q in be),sum(q[0]!='ZIG' for q in ee)]
            assert got==[row['a'],row['qF'],row['qE']]
            costs=[x+y for x,y in zip(costs,got)]
        assert a==b==term(conv(initial)) and e==term(conv(er))
        assert costs==[fam['costs'][k] for k in ('A','QF','QE')]
    # Symbolic two-inner-frame identities: no finite BST instantiation.
    # k labels stand for any actual ordered five path vertices; holes opaque.
    N=f.node;A,Bb,C,D,E,F=(('leaf',q) for q in 'ABCDEF')
    ll=N(9,N(8,N(7,N(6,N(5,A,Bb),C),D),E),F)
    ln,lev=step(ll,5)
    assert ln==N(5,A,N(8,N(6,Bb,N(7,C,D)),N(9,E,F)))
    # Unmarked P=8 has both marked G=7 and G=9 as descendants.
    rr=N(1,A,N(2,Bb,N(3,C,N(4,D,N(5,E,F)))))
    rn,rev=step(rr,5)
    assert rn==N(5,N(2,N(1,A,Bb),N(4,N(3,C,D),E)),F)
    assert [q[0] for q in lev]==['LL','LL'] and [q[0] for q in rev]==['RR','RR']
    # Inverse-one-frame source representatives used by the universal H1 lemma.
    zig=N(3,N(1,A,N(2,Bb,C)),D);zg,ze=step(zig,1)
    assert zg==N(1,A,N(3,N(2,Bb,C),D)) and len(ze)==1
    # Extra anonymous parent p<1. Its right fragment and key2 subtree remain exact.
    lr=N(3,N(0,A,N(1,Bb,N(2,C,D))),E);lg,le=step(lr,1)
    assert lg==N(1,N(0,A,Bb),N(3,N(2,C,D),E)) and [q[0] for q in le]==['LR']
    known=json.loads((B/'forced_regions.json').read_text())['records'];ks=[]
    for r in known:
        q=core(r['F_state']['BF']);t=core(r['T_state']['BF'])
        assert q[0]==1 and Uunary(q) and leafcount(q)<=2
        assert leafcount(t)>=4
        ks.append({'family':r['family'],'F_U_unary':True,'F_marked_leaves':leafcount(q),'T_marked_leaves':leafcount(t)})
    # Algebra check of packet-cost grammar; exhaustion is supplied by H>=1,Q bounds.
    zero=[];plus=[]
    for H in range(1,9):
        for Q in range(5):
            w=2*min(H,4)-Q
            if w==0:zero.append([H,Q])
            if w==1:plus.append([H,Q])
    assert zero==[[1,2],[2,4]] and plus==[[1,1],[2,3]]
    assert [H for H in range(2,9) if 2*min(H,4)-6==0]==[3]
    assert not any(2*min(H,4)-6==1 for H in range(2,9))
    out('independent_audit.json',{'status':'PASS_SEPARATE_SOURCE_AND_FRAME_DERIVATIONS','new_family_and_reflection_replayed':True,
        'same_exact_F_T_checked_again':True,'actual_costs':fam['costs'],'known_core_shapes':ks,
        'two_inner_LL_and_RR_free_term_identities':True,'inverse_H1_zig_and_LR_free_term_identities':True,
        'symbolic_scope':'opaque ordered holes; arbitrary finite gap substitutions, no hole internals inspected',
        'universal_logic_audit':{'forced_values_and_zero_closure':'telescoping proved in RETURN_BARRIER.md',
            'cost_grammar':'H and Q lower/upper bounds plus parity; H>=4 pair and H>=3 singleton positive',
            'core11_first_entry':'q>=3 output lies N1/N2; outgoing q4/q5 incompatible by inherited fan bound',
            'U_unary_extreme_destination':'second SS double creates a branching unmarked vertex; later outer frames preserve it',
            'zero_closure_of_restricted_known_B_shapes':'no final zero edge, so no nonempty finite zero path',
            'core11_F_T_disjoint':'q>=4 source has at most two marked leaves; negative-two target at least four',
            'global_return_barrier':'NOT PROVED; generic F/Z and core9/10 left open'},
        'independence':'same agent, separate immutable recursive-frame engine; not external peer review or full formalization',
        'new_potential_constructed':False,'architecture_refuted':False,**account})
    print(json.dumps({'status':'PASS_SEPARATE_SOURCE_AND_FRAME_DERIVATIONS','known_shapes':ks,**account}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_independent_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,**account})
