"""Actual-ID marked-leaf channels in the original closed maximal core.
Partial map and explicit branch frontier, never an assumed full allocator.
"""
import collections
def node(t):return isinstance(t,(tuple,list))
def marked_tree(t,M):
    parent={};children={x:[] for x in M}
    def visit(t,last=None):
        if not node(t):return
        x=t[0]
        if x in M:
            parent[x]=last
            if last is not None:children[last].append(x)
            last=x
        visit(t[1],last);visit(t[2],last)
    visit(t);assert set(parent)==set(M)
    return parent,children
def macros(rows):
    ends=[i for i,r in enumerate(rows) if r['genuine_F']];mm=[]
    for j,end in enumerate(ends):
        prev=ends[j-1];seg=rows[prev+1:end+1] if prev<end else rows[prev+1:]+rows[:end+1]
        assert seg and not any(r['qF'] for r in seg[:-1])
        mm.append({'rows':seg,'occurrences':[r['occurrence'] for r in seg],
            'H':sum(r['a'] for r in seg),'Q':sum(r['qF'] for r in seg),
            'units':[(r['occurrence'],j,b) for r in seg for j in range(1,r['a']+1) for b in (0,1)],
            'demands':[(r['occurrence'],j) for r in seg for j in range(1,r['qF']+1)]})
    return mm
def build(rows,M):
    mm=macros(rows);deaths=collections.defaultdict(list);births=[];h={};R=set();ledger=[];D=set();U=set();h0={}
    for i,m in enumerate(mm):
        x=m['rows'][-1]['target'];parent,ch=marked_tree(m['rows'][0]['before'][1],M)
        _,newch=marked_tree(m['rows'][-1]['after'][1],M)
        ancestors=[];u=parent[x]
        while u is not None:ancestors.append(u);u=parent[u]
        assert len(ancestors)==m['Q']
        oldleaf={v for v in M if not ch[v]};newleaf={v for v in M if not newch[v]}
        unary=[v for v in ancestors if len(ch[v])==1];branch=[v for v in ancestors if len(ch[v])>=2];z=int(x in oldleaf)
        assert newleaf-oldleaf==set(unary) and oldleaf-newleaf==({x} if z else set())
        assert len(newleaf)-len(oldleaf)==len(unary)-z
        reserve=m['units'][0] if z else None
        if z:deaths[x].append((i,reserve))
        branch_demands=[]
        for d,v in zip(m['demands'],ancestors):
            if v in unary:births.append((i,d,v))
            else:branch_demands.append(d)
        free=[u for u in m['units'] if u!=reserve];paid=min(len(free),len(branch_demands))
        h.update(zip(branch_demands[:paid],free));R.update(branch_demands[paid:]);D.update(m['demands']);U.update(m['units'])
        h0.update(zip(m['demands'],m['units']))
        ledger.append({'macro':i,'occurrences':m['occurrences'],'target':x,'H':m['H'],'Q':m['Q'],'ancestors_bottom_up':ancestors,
            'unary':unary,'branch':branch,'z':z,'leaf_before':sorted(oldleaf),'leaf_after':sorted(newleaf),
            'reserve':reserve,'local_branch_pairs':list(zip(branch_demands[:paid],free)),
            'branch_unpaid':branch_demands[paid:],'signed_leaf_residual':2*m['H']-len(branch)-z})
    channels=[]
    for i,d,key in births:
        assert deaths[key]
        candidates=[(j,u) for j,u in deaths[key] if j<i];j,u=max(candidates) if candidates else max(deaths[key])
        assert d not in h;h[d]=u
        channels.append({'marked_key':key,'birth_macro':i,'death_macro':j,'demand':d,'unit':u,'wraps_given_seam':j>i})
    assert set(h)==D-R and len(set(h.values()))==len(h) and set(h.values())<=U
    assert len(R)==sum(max(len(e['branch'])+e['z']-2*e['H'],0) for e in ledger)
    deep=[]
    for i,m in enumerate(mm):
        if m['Q']!=len(M)-1:continue
        nxt=(i+1)%len(mm);assert mm[nxt]['Q']==1
        dd=set(m['demands']+mm[nxt]['demands']);assert dd<=set(h)
        deep.append({'macro_indices':[i,nxt],'demands':sorted(dd),'H':m['H']+mm[nxt]['H'],'Q':len(M),
            'natural_excess':sorted(set(m['demands'])-set(h0))})
    return {'h':h,'R':R,'D':D,'U':U,'h0':h0,'macros':ledger,'channels':channels,'deep':deep}
def augment_partial(D,U,a,h):
    assert len(set(a.values()))==len(a) and len(set(h.values()))==len(h)
    assert set(a)<=D and set(h)<=D and set(a.values())|set(h.values())<=U
    inv={u:d for d,u in a.items()};extra={};blocked={};paths=[];visited=set()
    for p in sorted(D-set(a)):
        d=p;steps=[]
        while d in h:
            assert d not in visited;visited.add(d);u=h[d];steps.append((d,u))
            if u not in inv:extra[p]=u;break
            d=inv[u]
        else:blocked[p]=d
        paths.append({'root':p,'steps':steps,'frontier':blocked.get(p),'terminal':extra.get(p)})
    answer={**a,**extra};assert len(set(answer.values()))==len(answer)
    assert len(set(blocked.values()))==len(blocked) and set(blocked.values())<=D-set(h)
    assert D-set(answer)==set(blocked)
    return {'allocation':answer,'additions':extra,'blocked_frontier':blocked,'paths':paths}
