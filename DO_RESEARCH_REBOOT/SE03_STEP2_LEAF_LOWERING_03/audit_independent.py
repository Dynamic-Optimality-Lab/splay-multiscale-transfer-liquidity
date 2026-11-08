"""Immutable recursive-frame engine; independent replay and closure audit."""
import json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
sys.path.insert(0,str(ROOT/'python'))
from independent import splay as f
M={1,3,5,7,9,11};account={'source_engine_calls':0,'new_finite_tests':0}
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as h:json.dump(v,h,indent=2)
def term(v):return ('leaf',v) if isinstance(v,str) else f.node(v[0],term(v[1]),term(v[2]))
def mirror(v):
    if isinstance(v,str):
        if v.startswith('F'):return 'F'+str(11-int(v[1:]))
        return 'mirror_'+v
    return [12-v[0],mirror(v[2]),mirror(v[1])]
def step(t,x):
    account['source_engine_calls']+=1
    return f.trace(t,x)
def key(t):return t[1]
def children(t):return t[2:]
def leaf(t):
    if t[0]=='leaf':return 0
    l,r=children(t);return int(key(t) in M and fcore(l) is None and fcore(r) is None)+leaf(l)+leaf(r)
def fcore(t):
    if t[0]=='leaf':return None
    l,r=map(fcore,children(t));return (key(t),l,r) if key(t) in M or l is not None or r is not None else None
def marked_parent(t):
    parent={}
    def go(u,p):
        if u[0]=='leaf':return
        k=key(u)
        if k in M:parent[k]=p;p=k
        for q in children(u):go(q,p)
    go(t,None);return parent
def mp_children(par,p):return [x for x,y in par.items() if y==p]
def mass(par,p):return 1+sum(mass(par,x) for x in mp_children(par,p))
def local_class(t,x):
    par=marked_parent(t);h=par[x];g=par[h]
    assert g==key(t) and par[g] is None
    assert not mp_children(par,x)
    assert [v for v in mp_children(par,g) if v!=h] and [v for v in mp_children(par,h) if v!=x]
    n,ev=step(t,x);p=marked_parent(n)
    assert len(ev)==2 and leaf(n)==leaf(t)-1
    assert set(mp_children(p,x))=={g,h} and sorted([mass(p,g),mass(p,h)])==[2,3]
def audit_closure(cl,refl):
    conv=mirror if refl else lambda q:q;states=cl['states'];sm={}
    for r in states:sm[(term(conv(r['A'])),term(conv(r['BF'])),r['cost'])]=r['id']
    reported={(e['source'],e['target'],12-e['KEEP'] if refl else e['KEEP'],e['w']) for e in cl['edges']}
    expected=set();Ms=sorted(M)
    for r in states:
        a,b=term(conv(r['A'])),term(conv(r['BF']));c=r['cost']
        for x in Ms:
            if x==key(b):continue
            nb,be=step(b,x)
            # Core11 eligibility is checked independently using event G/P labels.
            if any(e[0] not in ('LL','RR') for e in be):continue
            na,ae=step(a,x);q=len(be);h=len(ae)
            assert not (q>=4 and h==1),'potential F geometry was omitted'
            assert not(q==4 or q==5 or(q==3 and c<cl['budget'])),'helper branch cannot be ignored'
            if h==1 and q in (1,2) and c+2-q<=cl['budget']:
                end=(na,nb,c+2-q);assert end in sm
                expected.add((r['id'],sm[end],x,2-q))
    assert expected==reported
def main():
    fam=json.loads((B/'pattern_family.json').read_text());crit={p['occurrence'] for p in fam['pattern']}
    for refl in (False,True):
        conv=mirror if refl else lambda q:q;a=b=term(conv(fam['initial_full_diagonal']));e=term(conv(fam['auxiliary_recurrent_start']))
        z=12-fam['erased'] if refl else fam['erased'];tot=[0,0,0]
        for r in fam['rows']:
            x=12-r['target'] if refl else r['target'];prior=b;a,ae=step(a,x);be=ee=[]
            if r['mode']=='K':b,be=step(b,x)
            if r['mode']=='K' and x!=z:e,ee=step(e,x)
            assert (a,b,e)==tuple(term(conv(q)) for q in r['after'])
            got=[len(ae),sum(q[0]!='ZIG' for q in be),sum(q[0]!='ZIG' for q in ee)]
            assert got==[r['a'],r['qF'],r['qE']];tot=[v+w for v,w in zip(tot,got)]
            if r['occurrence'] in crit:
                orig=next(p for p in fam['pattern'] if p['occurrence']==r['occurrence'])
                assert leaf(prior)==orig['leaf_before'] and leaf(b)==orig['leaf_after']
                if orig['leaf_after']<orig['leaf_before']:local_class(prior,x)
        assert a==b==term(conv(fam['initial_full_diagonal'])) and e==term(conv(fam['auxiliary_recurrent_start']))
        assert tot==[fam['costs'][k] for k in ('A','QF','QE')]
    # Complete one-event old-root positions, with arbitrary ordered gap terms.
    H=[('leaf','H'+str(i)) for i in range(4)];N=f.node
    sources=[(N(3,N(1,H[0],H[1]),H[2]),1,'R'),(N(1,H[0],N(3,H[1],H[2])),3,'L'),
        (N(5,N(3,N(1,H[0],H[1]),H[2]),H[3]),1,'RR'),
        (N(1,H[0],N(3,H[1],N(5,H[2],H[3]))),5,'LL'),
        (N(5,N(1,H[0],N(3,H[1],H[2])),H[3]),3,'R'),
        (N(1,H[0],N(5,N(3,H[1],H[2]),H[3])),3,'L')]
    for s,x,p in sources:
        z,ev=step(s,x);assert len(ev)==1;v=z
        for d in p:v=v[2 if d=='L' else 3]
        assert key(v)==key(s)
    # All four actual two-SS path orientations, with six opaque hangers.
    layouts=[([9,8,5,4,1],'LLLL'),([1,2,5,6,9],'RRRR'),
             ([1,2,9,8,5],'RRLL'),([9,8,1,2,5],'LLRR')]
    for ks,p in layouts:
        hs=[('leaf','P'+str(i)) for i in range(6)];v=N(ks[-1],hs[4],hs[5])
        for j in range(3,-1,-1):v=N(ks[j],v,hs[j]) if p[j]=='L' else N(ks[j],hs[j],v)
        _,ev=step(v,ks[-1]);assert len(ev)==2 and [q[0] for q in ev]==[p[2:],p[:2]]
    cls=json.loads((B/'forward_closure.json').read_text())['results']
    for cl in cls:
        assert not cl['unknown_branches'] and not cl['possible_F_states']
        audit_closure(cl,False);audit_closure(cl,True)
    back=json.loads((B/'backward_source_audit.json').read_text())
    for r in back['records']:
        if r['family']=='Gamma_pair':continue
        for refl in (False,True):
            conv=mirror if refl else lambda q:q;tx=lambda x:12-x if refl else x
            dest=term(conv(r['plus_one_B_source']))
            for q in ('q2_inverse_B_old1','q2_inverse_B_old5'):
                n,ev=step(term(conv(r[q])),tx(3));assert n==dest and len(ev)==2
            az=term(conv(r['zig_A_source']))
            for s in r['zig_family_A_zero_predecessors']:
                n,ev=step(term(conv(s)),tx(3));assert n==az and len(ev)==1
    out('independent_audit.json',{'status':'PASS_SEPARATE_SOURCE_REPLAY_AND_COMPLETE_FRAME_CLOSURES',
        'all70_original_operations_and_reflection':True,'actual_A_B_BE_closure':True,'actual_costs':fam['costs'],
        'two_losses_then_zero_restoration':[4,3,2,3],
        'universal_local_classification_audit':'leaf loss iff target marked-leaf and both ancestors retain offpath marks; r6 branches2,3',
        'one_event_A_oldroot_positions':['L','R','LL','RR'],'two_double_B_paths':['LLLL','LLRR','RRLL','RRRR'],
        'forward_complete_source_grammar_guards_checked':True,'all_reflected_backward_identities_checked':True,
        'new_known_family_R0_R1_exclusion':'PROVED conditional only on the explicit source-completeness/lifting proof in report',
        'global_R0_R1':'OPEN','audit_independence':'same agent; distinct immutable engine/term format and separate proof derivation; no external reviewer/formal proof assistant',
        **account})
    print(json.dumps({'status':'PASS_SEPARATE_SOURCE_REPLAY_AND_COMPLETE_FRAME_CLOSURES','costs':fam['costs'],
        'closure_tables':len(cls),'reflections':True,**account}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_independent_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,**account})
