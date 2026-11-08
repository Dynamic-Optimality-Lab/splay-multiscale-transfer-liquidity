"""Actual physical funding for the precisely verified unary boundary domain."""
import importlib.util,json,sys
from pathlib import Path
B=Path(__file__).resolve().parent;OLD=B.parent/'SE03_STEP2_MULTICORE_FUNDING_CLOSURE_13'
sys.path.insert(0,str(OLD))
from source_funding import own_map,with_owners
from debt_funding import labels_core,normalize,freeze
def build(rows):
    c=json.loads((OLD/'cheap_A_comparison.json').read_text())['reports'][0]
    M={r['target'] for r in rows if r['genuine_F']};S=labels_core(rows[0]['before'][1],M)
    if len(M)!=6 or len(S)!=9:raise ValueError('source six-mark/core9 domain')
    mr={x:i+1 for i,x in enumerate(sorted(M))};sr={x:i+1 for i,x in enumerate(sorted(S))}
    if tuple(sorted(sr[x] for x in M))!=tuple(c['BF_marks']):raise ValueError('verified core9 mask')
    ai={freeze(t):i for i,t in enumerate(c['A_trees'])};bi={freeze(t):i for i,t in enumerate(c['BF_trees'])};D={tuple(s):d for s,d in zip(c['states'],c['debt'])}
    def project(t):
        unknown=[]
        def go(t):
            if isinstance(t,str) or not labels_core(t,M):return None
            if t[0] in M:return (mr[t[0]],go(t[1]),go(t[2]))
            l,r=labels_core(t[1],M),labels_core(t[2],M)
            if bool(l)==bool(r):raise ValueError('branching anonymous A ancestor outside unary theorem')
            unknown.append(t[0]);return go(t[1] if l else t[2])
        a=go(t)
        if len(unknown)>1:raise ValueError('more than one anonymous A ancestor outside unary theorem')
        return a,len(unknown)
    def debt(A,F):
        a,count=project(A);return D[ai[a],bi[normalize(F,S)]],count
    v=own_map(rows);mm=v['macros'];by={r['occurrence']:r for r in rows};dd=[];counts=[]
    for m in mm:
        before=by[m['occurrences'][0]]['before'];after=by[m['occurrences'][-1]]['after']
        a,ca=debt(before[0],before[1]);b,cb=debt(after[0],after[1]);assert 2*m['H']-m['Q']+b-a>=0
        dd.append((a,b));counts.append((ca,cb))
    top=max(a for a,b in dd);cut=next(i for i,(a,b) in enumerate(dd) if a==top);h=dict(v['h0']);bank=[];receipt=[]
    for j in range(len(mm)):
        i=(cut+j)%len(mm);m=mm[i];a,b=dd[i];assert len(bank)==top-a
        n=min(len(m['units']),m['Q']);missing=m['demands'][n:]
        for d in missing:assert bank;h[d]=bank.pop(0)
        candidate=bank+m['units'][n:];assert len(candidate)>=top-b;bank=candidate[:top-b]
        receipt.append({'macro':i,'H':m['H'],'Q':m['Q'],'D_before':a,'D_after':b,'anon_counts':counts[i],
            'new_pairs':[(d,h[d]) for d in missing],'carry':bank[:]})
    assert not bank and set(h)==v['D'] and len(set(h.values()))==len(h)
    assert all(h[d]==u for d,u in v['h0'].items())
    v.update({'h':h,'source_receipt':receipt,'full_cut_before_macro':cut,'working_bound':6})
    return v
