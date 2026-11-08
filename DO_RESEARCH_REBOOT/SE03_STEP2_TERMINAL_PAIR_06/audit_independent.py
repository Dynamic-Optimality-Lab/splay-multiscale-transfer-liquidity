"""Independent symbolic audit: separate tuple engine and forward A frames.

No primary splay, predecessor, saturation, or grammar implementation is imported.
The objects checked are universally quantified gap contexts, not populations.
"""
import collections,functools,importlib.util,itertools,json,sys,time
from fractions import Fraction as F
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
spec=importlib.util.spec_from_file_location('separate_splay',ROOT/'python/independent/splay.py')
I=importlib.util.module_from_spec(spec);spec.loader.exec_module(I)
M={1,3,5,7,9,11};calls=0;began=time.process_time();CAP=min(80,float(sys.argv[1])-4)
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def guard():
    assert time.process_time()-began<CAP and calls<1500000
def splay(t,x):
    global calls
    calls+=1
    if calls%128==0:guard()
    return I.trace(t,x)
def freeze(v):return tuple(map(freeze,v)) if isinstance(v,list) else v
@functools.lru_cache(None)
def alltrees(lo,hi):
    if lo>hi:return (('leaf',lo),)
    return tuple(I.node(k,l,r) for k in range(lo,hi+1) for l in alltrees(lo,k-1) for r in alltrees(k+1,hi))
def density(t):
    if t[0]=='leaf':return 0,0,True
    _,k,l,r=t;lc,lm,lv=density(l);rc,rm,rv=density(r);cc=1+lc+rc;mm=int(k in M)+lm+rm
    return cc,mm,lv and rv and cc<=2*mm-int(k in M)
def bf_read(t):
    if isinstance(t,str):return ('leaf',int(t[1:]))
    return I.node(t[0],bf_read(t[1]),bf_read(t[2]))
def bf_write(t):return 'Q'+str(t[1]) if t[0]=='leaf' else (t[1],bf_write(t[2]),bf_write(t[3]))
def parents(t):
    result={}
    def visit(v,p):
        if v[0]=='leaf':return
        k=v[1]
        if k in M:result[k]=p;p=k
        visit(v[2],p);visit(v[3],p)
    visit(t,None);return result
def L(t):return sum(k not in set(parents(t).values()) for k in M)
def degree(t):return sum(p==t[1] for p in parents(t).values())
def legal(t,x):
    u=t;ks=[];dirs=[]
    while u[0]!='leaf' and u[1]!=x:
        ks.append(u[1]);d=0 if x<u[1] else 1;dirs.append(d);u=u[2+d]
    assert u[0]!='leaf'
    if not dirs or len(dirs)%2:return None
    if any(dirs[j]!=dirs[j+1] or ks[j] not in M or ks[j+1] in M for j in range(0,len(dirs),2)):return None
    z,ev=splay(t,x);assert len(ev)==len(dirs)//2 and all(e[0] in ('LL','RR') for e in ev)
    return z,len(ev)
def heap(t,r):
    p={k:i for i,k in enumerate(r)}
    return all(v is None or p[v]<p[k] for k,v in parents(t).items())
def rankword(w):
    ks=sorted(set(w));return tuple(ks.index(x) for x in w)
def slot(lo,hi):return ('leaf',F(lo),F(hi))
def fresh(k,lo,hi):return I.node(F(k),slot(lo,k),slot(k,hi))
def keys(t):return [] if t[0]=='leaf' else keys(t[2])+[t[1]]+keys(t[3])
def replace_at(t,p,u):
    if not p:return u
    _,k,l,r=t
    return I.node(k,replace_at(l,p[1:],u),r) if p[0]==0 else I.node(k,l,replace_at(r,p[1:],u))
def replace_slot(t,h,u):
    if t==h:return u
    if t[0]=='leaf':return t
    return I.node(t[1],replace_slot(t[2],h,u),replace_slot(t[3],h,u))
def refinements(t,x,anchors):
    u=t;p=()
    while u[0]!='leaf':
        if u[1]==x:return [(t,None,None)] if len(p) in (1,2) else []
        d=0 if x<u[1] else 1;p=p+(d,)
        if len(p)>2:return []
        u=u[2+d]
    _,lo,hi=u
    if not lo<x<hi:return []
    v=fresh(x,lo,hi);opts=[(replace_at(t,p,v),u,v)]
    if len(p)==1:
        cuts=sorted(set(keys(t)+list(map(F,anchors))+[lo,hi]))
        choices=[k for k in cuts if lo<k<hi and k!=x]
        choices += [(a+b)/2 for a,b in zip(cuts,cuts[1:]) if lo<=a<b<=hi]
        for k in choices:
            v=I.node(k,fresh(x,lo,k),slot(k,hi)) if x<k else I.node(k,slot(lo,k),fresh(x,k,hi))
            opts.append((replace_at(t,p,v),u,v))
    return opts
def frames(word,anchors,lo,hi):
    t=fresh(word[0],lo,hi);states={(t,t)};sizes=[1]
    for x in word[1:]:
        new=set()
        for initial,current in states:
            for refined,h,v in refinements(current,F(x),anchors):
                z,ev=splay(refined,F(x));assert len(ev)==1
                new.add((replace_slot(initial,h,v) if h is not None else initial,z))
        states=new;sizes.append(len(states))
        if not states:break
    return states,sizes
def Aread(t):
    if isinstance(t,dict):return slot(F(t['gap'][0]),F(t['gap'][1]))
    return I.node(F(t[0]),Aread(t[1]),Aread(t[2]))
def Aw(t):return {'gap':[str(t[1]),str(t[2])]} if t[0]=='leaf' else [str(t[1]),Aw(t[2]),Aw(t[3])]
def spine_possible(t,k,maxdepth=None):
    direction=0 if k<t[1] else 1;u=t;depth=0
    while True:
        if u[0]=='leaf':return u[1]<k<u[2] and (maxdepth is None or depth<=maxdepth)
        if u[1]==k:return maxdepth is None or depth<=maxdepth
        if maxdepth is not None and depth>=maxdepth:return False
        u=u[2+direction];depth+=1
def marked_on_spine(t,k):
    d=0 if k<t[1] else 1;u=t;depth=0
    while u[0]!='leaf':
        if u[1]==k:return depth
        u=u[2+d];depth+=1
    return None
def ss_inverse(t,k):
    x=t[1]
    if k<x:
        _,pp,left,cc=t[2];_,gg,aa,zz=left;assert gg==k
        return I.node(gg,aa,I.node(pp,zz,I.node(x,cc,t[3])))
    _,pp,aa,right=t[3];_,gg,cc,dd=right;assert gg==k
    return I.node(gg,I.node(pp,I.node(x,t[2],aa),cc),dd)
def main():
    # Independent COMPLETE core-context derivation from all ordered bracketings.
    raw=alltrees(1,11);states={t for t in raw if t[1] in M and density(t)[2]}
    assert len(raw)==58786 and len(states)==2394
    inc=collections.defaultdict(list);fwd=collections.defaultdict(list)
    for t in states:
        for x in M-{t[1]}:
            v=legal(t,x)
            if v is None or v[0] not in states:continue
            z,q=v;inc[z].append((t,x,q));fwd[t].append((z,x,q))
    assert sum(map(len,fwd.values()))==3698
    table=collections.defaultdict(set);tails=[]
    for t in states:
        if L(t)!=3:continue
        for z,a,q in fwd[t]:
            if q!=2 or L(z)!=2:continue
            for e,b,qq in fwd[z]:
                if qq!=2 or L(e)!=2:continue
                for probe,x,qqq in fwd[e]:
                    if qqq!=4 or x in (t[1],a,b):continue
                    pm=parents(t)
                    if x in set(pm.values()):continue
                    assert degree(t)==2, 'all previous cheap packets are H1/Q1 or H1/Q2'
                    for old,gg,q0 in inc[t]:
                        if q0 not in (1,2) or old[1]==x:continue
                        word=(old[1],gg,a,b,x);pat=rankword(word)
                        table[pat].add((bf_write(old),bf_write(t),q0,word));tails.append((pat,word))
    primary=json.loads((B/'grammar.json').read_text())
    assert set(table)=={tuple(r['rank_word']) for r in primary['order_profiles']}
    compatible=[];frame_audit=[]
    for pat,contexts in sorted(table.items()):
        n=len(set(pat));fs,sizes=frames(pat,range(n),-1,n)
        old=next(r for r in primary['order_profiles'] if tuple(r['rank_word'])==pat)
        assert bool(fs)==old['A_compatible'] and len(contexts)==old['B_templates']
        frame_audit.append({'rank_word':pat,'templates':len(contexts),'feasible':bool(fs)})
        if fs:compatible.extend(contexts)
    assert len(compatible)==8 and len(table)==32 and len(tails)==144
    supplied=json.loads((B/'sourceclosure.json').read_text())['remaining_compatible_tails']
    expected={(freeze(s['previous_BF']),freeze(s['pre_loss_BF']),s['previous_Q'],tuple(s['word'])) for s in supplied}
    assert set(compatible)==expected
    # New universal H2 root-spine lemma, independent forward decomposition.
    spine_cases=0;maxdepth=0
    for word in itertools.permutations(range(3)):
        fs,ss=frames(word,range(3),-1,3)
        for initial,end in fs:
            d=marked_on_spine(end,F(word[0]));assert d is not None and d<=4
            maxdepth=max(maxdepth,d);spine_cases+=1
    # Every actual tail has one of the supplied initial universally free frames.
    initial_by_origin={}
    for i,s in enumerate(supplied):
        fs,ss=frames(s['word'],range(1,12),0,12)
        initials={a for a,z in fs};assert len(initials)==1
        initial_by_origin[i]=initials
    cert=json.loads((B/'saturation3.json').read_text());assert cert['closed'] and not cert['goal']
    records=cert['records'];lookup=set();parsed=[]
    for r in records:
        a=Aread(r['A']);b=bf_read(r['BF']);rr=tuple(r['recent']);budget=r['budget']
        assert b in states and a[1]==b[1]==rr[0] and heap(b,rr)
        assert L(b) in (2,3), 'disjoint from every cold NEG2 target L4'
        parsed.append((a,b,rr,budget));lookup.add((a,b,rr,budget))
    # Seed coverage includes ALL heap-compatible recent orders, not only examples.
    seeds=0
    for i,s in enumerate(supplied):
        b=bf_read(s['previous_BF']);word=s['word'];budget=s['previous_Q']-1
        for rr in itertools.permutations(sorted(M)):
            if rr[0]!=b[1] or not heap(b,rr):continue
            rrr=rr
            for x in word[1:-1]:rrr=(x,)+tuple(y for y in rrr if y!=x)
            if rrr[-1]!=word[-1]:continue
            for a in initial_by_origin[i]:assert (a,b,rr,budget) in lookup;seeds+=1
    H1_edges=H2_rejections=0
    for a,b,rr,budget in parsed:
        for old,x,q in inc[b]:
            if q==3 and budget==1:
                # Any two-event source must retain the old synchronized root
                # on an outer spine. This rejects ALL anonymous helpers.
                if rr[1]!=old[1]:continue
                assert not spine_possible(a,F(old[1])), 'unclosed H2 source'
                H2_rejections+=1
            if q not in (1,2) or 2-q>budget or rr[1]!=old[1]:continue
            if not spine_possible(a,F(old[1]),2):continue
            d=marked_on_spine(a,F(old[1]));assert d==2, 'would need a refined non-SS inverse'
            before=ss_inverse(a,F(old[1]));z,ev=splay(before,a[1]);assert z==a and len(ev)==1
            rest=list(rr[1:])
            for pos in range(1,6):
                prior=tuple(rest[:pos]+[x]+rest[pos:])
                if not heap(old,prior):continue
                assert (before,old,prior,budget-(2-q)) in lookup, 'missing universal predecessor frame'
                H1_edges+=1
    assert seeds==240 and len(records)==260 and H1_edges==20
    report={'status':'PASS_UNIVERSAL_SYMBOLIC_COVERAGE_AND_CLOSURE',
        'raw_ordered_core_bracketings':len(raw),'density_contexts':len(states),'legal_source_edges':3698,
        'terminal_contexts':144,'rank_word_profiles':frame_audit,'surviving_tail_contexts':8,
        'universal_H2_spine_frames':spine_cases,'H2_max_old_root_depth':maxdepth,
        'seed_recent_frames':seeds,'backward_frames':len(records),'H1_predecessor_edges':H1_edges,
        'H2_predecessors_rejected_by_spine':H2_rejections,'all_frames_have_L2_or3':True,
        'cold_NEG2_targets_have_L4':'symbolic source proof required and inspected in final proof',
        'both_orientations':'all ordered contexts and rank words included; no debt symmetry assumed',
        'source_engine_calls':calls,'new_finite_tests':0,
        'scope':'mechanical universal-gap algebra audit by a separate immutable engine; same agent, no external peer review or formal assistant'}
    out('independent_audit.json',report);print(json.dumps({k:v for k,v in report.items() if k!='rank_word_profiles'}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_independent_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':calls,'new_finite_tests':0})
