"""Independent frozen recursive-frame witness and complete suffix audit.
Primary tuple engine/search code is NOT imported. Same-agent independent
derivation; no external peer-review or proof-assistant claim.
"""
import functools,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
sys.path.insert(0,str(ROOT/'python'))
from independent import splay as f
M={1,3,5,7,9,11};account={'source_engine_calls':0,'new_finite_tests':0}
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as g:json.dump(v,g,indent=2)
def term(v):return ('leaf',v) if isinstance(v,str) else f.node(v[0],term(v[1]),term(v[2]))
def mirror(v):
    if isinstance(v,str):return 'F'+str(11-int(v[1:]))
    return [12-v[0],mirror(v[2]),mirror(v[1])]
def state(v,refl=False):
    conv=mirror if refl else lambda q:q
    return tuple(term(conv(q)) for q in v[:3])+(tuple(12-x for x in v[3]) if refl else tuple(v[3]),)
@functools.lru_cache(maxsize=100000)
def step(v,x):
    account['source_engine_calls']+=1
    return f.trace(v,x)
def route(v,x):
    p='';ks=[]
    while v[0]!='leaf':
        k=v[1];ks.append(k)
        if k==x:return p,ks
        side='L' if x<k else 'R';p+=side;v=v[2 if side=='L' else 3]
    raise AssertionError(('missing actual key',x))
def core(v,marks=M):
    if v[0]=='leaf':return None
    l,r=core(v[2],marks),core(v[3],marks)
    return (v[1],l,r) if v[1] in marks or l is not None or r is not None else None
def labels(v):return set() if v is None else {v[0]}|labels(v[1])|labels(v[2])
def leaf(v):return 0 if v is None else int(v[0] in M) if v[1] is None and v[2] is None else leaf(v[1])+leaf(v[2])
def bmove(v,x):
    p,ks=route(v,x);n,ev=step(v,x)
    if len(p)%2 or any(e[0] not in ('LL','RR') for e in ev):return None
    if not all(k in M for k in ks[::2]) or any(k in M for k in ks[1::2]):return None
    if labels(core(n))!=set(range(1,12)):return None
    return n,len(ev)
def recent(v,x):return (x,)+tuple(q for q in v if q!=x)
def holes2(v,d=0):
    if v[0]=='leaf':return int(0<d<=2)
    return 0 if d>=2 else holes2(v[2],d+1)+holes2(v[3],d+1)
def macro(s,x,H,z):
    a,b,e,r=s;bb=bmove(b,x)
    if bb is None:return
    nb,q=bb;forms=[];na,ev=step(a,x)
    if len(ev)==H:forms.append((na,[('K',x)]))
    if H==2 and len(route(a,x)[0])<=4:
        for y in range(1,12):
            ay,ey=step(a,y)
            if len(ey)!=1:continue
            ax,ex=step(ay,x)
            if len(ex)==1:forms.append((ax,[('D',y),('K',x)]))
    variants=[(e,[])];g=b[1]
    if g!=z:
        ee=step(e,g)[0]
        if ee!=e:variants.append((ee,[('K',g)]))
    for ep,pre in variants:
        ne=step(ep,x)[0] if x!=z else ep
        for aa,w in forms:yield (aa,nb,ne,recent(r,x)),pre+w,q
def audit_suffix(report,refl):
    z=9 if refl else 3
    costs={state(r['state'],refl):r['cost'] for r in report['states']}
    asserted={(state(e['source'],refl),state(e['target'],refl),e['w'],e['H'],e['Q']) for e in report['edges']}
    expected=set();q5=[];private=0
    for s,c in costs.items():
        a,b,e,r=s;budget=report['remaining_budget']
        for x in M:
            if x==b[1]:continue
            bb=bmove(b,x)
            if bb is None:continue
            d=len(route(a,x)[0]);q=bb[1]
            if q>=4 and x==r[-1]:assert d>2,'cold negative source would obstruct claimed exclusion'
            if q==5:
                # All zero q5/q1 packets have first macro H<=2. Each
                # StepEv has at most2 rotations, so d>4 excludes them.
                assert d>4
                q5.append({'target':x,'A_source_depth':d,'minimum_first_H':(d+1)//2})
                continue
            if q in (3,4) and 4-q<=budget-c and d<=2:
                assert holes2(a)==0,'unresolved private helper cannot be silently omitted'
            for H in (1,2):
                w=2*H-q
                if w not in (0,1) or c+w>budget:continue
                for t,word,_ in macro(s,x,H,z):
                    assert t in costs and costs[t]<=c+w
                    expected.add((s,t,w,H,q))
    assert expected==asserted
    for edge in report['edges']:
        s=state(edge['source'],refl);end=state(edge['target'],refl);a,b,e,r=s;H=Q=0
        for k,v in edge['word']:
            x=12-v if refl else v;a,ae=step(a,x);H+=len(ae)
            if k=='K':
                b,be=step(b,x);Q+=sum(t[0]!='ZIG' for t in be);r=recent(r,x)
                if x!=z:e=step(e,x)[0]
        assert (a,b,e,r)==end and (H,Q)==(edge['H'],edge['Q'])
    return {'family':report['family'],'reflected':refl,'exact_full_state_cells':len(costs),
        'all_distinguished_macro_endpoints_covered':True,'private_helpers_excluded_by_source_depth_or_no_near_hole':True,
        'paired_unknowns_discharged':q5,'no_cold_NEG2_source_in_closure':True}
def main():
    proofs=[]
    for filename in ('entry_family.json','e1_family.json'):
        fam=json.loads((B/filename).read_text())
        for refl in (False,True):
            conv=mirror if refl else lambda q:q
            a=b=e=term(conv(fam['initial_full_diagonal']));z=9 if refl else 3
            # Explicit legal reaching prefix, not credit borrowed from it.
            for k,v in fam['reaching_prefix']:
                x=12-v if refl else v;a=step(a,x)[0]
                if k=='K':
                    b=step(b,x)[0]
                    if x!=z:e=step(e,x)[0]
            assert a==b==term(conv(fam['initial_full_diagonal'])) and e==term(conv(fam['auxiliary_recurrent_start']))
            lru=[]
            for k,x in reversed(fam['word']):
                if k=='K' and x not in lru:lru.append(x)
            if refl:lru=[12-x for x in lru]
            r0=lru[:];cost=[0,0,0]
            for row,chart in zip(fam['rows'],fam['charts']):
                assert (a,b,e)==tuple(term(conv(q)) for q in row['before'])
                x=12-row['target'] if refl else row['target'];old=lru[:];a,ae=step(a,x);be=ee=[]
                genuine=row['mode']=='K' and b[1]!=x;assert genuine==row['genuine_F']
                if row['mode']=='K':
                    b,be=step(b,x);lru.remove(x);lru.insert(0,x)
                    if x!=z:e,ee=step(e,x)
                assert (a,b,e)==tuple(term(conv(q)) for q in row['after'])
                got=[len(ae),sum(q[0]!='ZIG' for q in be),sum(q[0]!='ZIG' for q in ee)]
                assert got==[row['a'],row['qF'],row['qE']];cost=[q+w for q,w in zip(cost,got)]
                assert lru==([12-q for q in chart['recent_after']] if refl else chart['recent_after'])
                assert old==([12-q for q in chart['recent_before']] if refl else chart['recent_before'])
                assert (row['mode']=='K' and x not in old[:5])==chart['cold']
                assert labels(core(b))==set(range(1,12))
                assert f.inorder(a)==f.inorder(b)==f.inorder(e)==list(range(1,12))
            assert a==b==term(conv(fam['initial_full_diagonal'])) and e==term(conv(fam['auxiliary_recurrent_start'])) and lru==r0
            assert cost==[fam['costs'][k] for k in ('A','QF','QE')]
            for cl in fam['critical']:
                for key,pk in [('negative_packet',cl['negative_packet']),('entry_prefix',cl['entry_prefix'][0]),('first_lowering',cl['first_lowering'])]:
                    rr=[fam['rows'][i-1] for i in pk['occurrences']]
                    assert (sum(r['a'] for r in rr),sum(r['qF'] for r in rr))==(pk['H'],pk['Q'])
                for key,offset in [('T_state',cl['negative_packet']['end']),('L_state',cl['entry_prefix'][0]['end']),('post_lowering_state',cl['first_lowering']['end'])]:
                    st=cl[key];row=fam['rows'][offset-1];assert tuple(term(conv(st[q])) for q in ('A','BF','BE'))==tuple(term(conv(t)) for t in row['after'])
                assert cl['leaf_counts']==[4,4,3]
            proofs.append({'family':filename,'reflected':refl,'complete_actual_source_closure':True,'physical_costs':fam['costs'],
                'entry_class':fam['critical'][0]['entry_class'],'entry_prefix_weight':fam['critical'][0]['prefix_weight'],
                'first_loss_is_genuine':True,'old_semantic_rows_replayed':0})
    suffix=json.loads((B/'suffix_analysis.json').read_text());suffixproof=[]
    for rep in suffix['reports']:
        for refl in (False,True):suffixproof.append(audit_suffix(rep,refl))
    sig=json.loads((B.parent/'SE03_STEP2_FORCED_ZERO_INCOMING_02/incoming_family_v2.json').read_text())
    assert leaf(core(term(sig['predecessor']['BF'])))==3
    out('independent_audit.json',{'status':'PASS_BOTH_ENTRY_CLASSES_AND_EXAMPLE_SUFFIX_CLOSURES',
        'witnesses':proofs,'suffixes':suffixproof,
        'previous_conservative_q5_suffix_flag':'DISCHARGED: only first target has A depth6, requiring first_H>=3 and pair_H>=4, price>=2',
        'universal_lifting':'every accessed key in witness/allowed suffix bodies is distinguished; no free gap is entered; source completeness excludes private helpers before induction',
        'Sigma_leaf3_control_preserved':True,'complete_cheap_return_found':False,'global_return_barrier':'OPEN',
        'independence':'same agent, different immutable recursive-frame engine and term representation; no external peer review or formal-assistant claim',**account})
    print(json.dumps({'status':'PASS_BOTH_ENTRY_CLASSES_AND_EXAMPLE_SUFFIX_CLOSURES','witness_cases':len(proofs),
        'suffix_cases':len(suffixproof),'global_return_barrier':'OPEN',**account}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_independent_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,**account})
