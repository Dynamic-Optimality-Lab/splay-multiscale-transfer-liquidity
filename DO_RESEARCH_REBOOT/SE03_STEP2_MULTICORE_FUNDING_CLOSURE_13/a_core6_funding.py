"""Restricted actual source builder, NOT arbitrary A-core/inventory theorem."""
from source_funding import own_map
from debt_funding import labels_core,normalize,freeze
def build(rows,comparison):
    if comparison['core']!=9 or comparison['max_debt']!=2:raise ValueError('verified restricted9 comparison only')
    M={r['target'] for r in rows if r['genuine_F']};S=labels_core(rows[0]['before'][1],M)
    if len(M)!=6 or len(S)!=9:raise ValueError('support/BF source core')
    mrank={x:i+1 for i,x in enumerate(sorted(M))};srank={x:i+1 for i,x in enumerate(sorted(S))}
    if tuple(sorted(srank[x] for x in M))!=tuple(comparison['BF_marks']):raise ValueError('restricted BF mask')
    ai={freeze(t):i for i,t in enumerate(comparison['A_trees'])};bi={freeze(t):i for i,t in enumerate(comparison['BF_trees'])}
    pair={tuple(v):d for v,d in zip(comparison['states'],comparison['debt'])}
    def ashape(t):
        if isinstance(t,str):return None
        if t[0] not in M:
            if labels_core(t,M):raise ValueError('A marked core has anonymous ancestors: outside theorem')
            return None
        return (mrank[t[0]],ashape(t[1]),ashape(t[2]))
    def debt(A,BF):
        if labels_core(A,M)!=M:raise ValueError('A marked core must have EXACTLY6 nodes at macro boundaries')
        return pair[ai[ashape(A)],bi[normalize(BF,S)]]
    v=own_map(rows);mm=v['macros'];by={r['occurrence']:r for r in rows};dd=[]
    for m in mm:
        before=by[m['occurrences'][0]]['before'];after=by[m['occurrences'][-1]]['after']
        a,b=debt(before[0],before[1]),debt(after[0],after[1]);assert 2*m['H']-m['Q']+b-a>=0
        dd.append((a,b))
    top=max(a for a,b in dd);cut=next(i for i,(a,b) in enumerate(dd) if a==top);h=dict(v['h0']);bank=[];proof=[]
    for j in range(len(mm)):
        i=(cut+j)%len(mm);m=mm[i];a,b=dd[i];assert len(bank)==top-a
        n=min(len(m['units']),m['Q']);missing=m['demands'][n:]
        for d in missing:assert bank;h[d]=bank.pop(0)
        bank=(bank+m['units'][n:])[:top-b];assert len(bank)==top-b
        proof.append({'macro':i,'H':m['H'],'Q':m['Q'],'D_source':a,'D_target':b,'new_pairs':[(d,h[d]) for d in missing],'carry':bank[:]})
    assert not bank and set(h)==v['D'] and len(set(h.values()))==len(h)
    v.update({'h':h,'source_receipt':proof,'full_cut_before_macro':cut,'working_bound':6})
    return v
