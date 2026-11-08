"""Physical own-spare allocator from an independently verified BF comparison.
Does not change h0, any prior a value, source replay or frozen fE.
"""
from source_funding import own_map
def labels_core(t,M):
    if isinstance(t,str):return set()
    l,r=labels_core(t[1],M),labels_core(t[2],M)
    return l|r|{t[0]} if l or r or t[0] in M else set()
def normalize(t,S):
    rank={x:i+1 for i,x in enumerate(sorted(S))}
    def visit(t,lo,hi):
        if isinstance(t,str) or t[0] not in S:return 'F'+str(hi)
        k=rank[t[0]];return (k,visit(t[1],lo,k-1),visit(t[2],k+1,hi))
    return visit(t,1,len(S))
def freeze(v):return tuple(map(freeze,v)) if isinstance(v,list) else v
def build(rows,certificate):
    if certificate['status']!='PROVED_COMPLETE_NECESSARY_BF_COMPARISON':raise ValueError('not a verified BF comparison')
    k=certificate['core'];M={r['target'] for r in rows if r['genuine_F']};S=labels_core(rows[0]['before'][1],M)
    if len(M)!=6 or len(S)!=k:raise ValueError('source support/core')
    ranks={x:i+1 for i,x in enumerate(sorted(S))};marks=tuple(sorted(ranks[x] for x in M));offset=0;table=None
    for v in certificate['mask_summaries']:
        n=v['states']
        if tuple(v['marks'])==marks:
            table={freeze(t):d for t,d in zip(certificate['trees'][offset:offset+n],certificate['debt'][offset:offset+n])};break
        offset+=n
    if table is None:raise ValueError('source mask missing from complete comparison')
    value=own_map(rows);mm=value['macros'];by={r['occurrence']:r for r in rows};debts=[]
    for m in mm:
        if m['H']<1 or m['Q']>(k-1)//2:raise ValueError('natural source macro costs')
        s=normalize(by[m['occurrences'][0]]['before'][1],S);t=normalize(by[m['occurrences'][-1]]['after'][1],S)
        ds,dt=table[s],table[t];assert 2-m['Q']+dt-ds>=0
        debts.append((ds,dt))
    dmax=max(a for a,b in debts);start=next(i for i,(a,b) in enumerate(debts) if a==dmax)
    h=dict(value['h0']);bank=[];records=[];peak=0
    for j in range(len(mm)):
        i=(start+j)%len(mm);m=mm[i];ds,dt=debts[i]
        assert len(bank)==dmax-ds
        n=min(len(m['units']),m['Q']);missing=m['demands'][n:];spares=m['units'][n:]
        for d in missing:
            assert bank;h[d]=bank.pop(0)
        target=dmax-dt;available=bank+spares
        assert len(available)>=target
        retained=available[:target];peak=max(peak,n+max(len(bank),target))
        records.append({'macro':i,'debt_before':ds,'debt_after':dt,'critical_demands':missing,
            'funded':[(d,h[d]) for d in missing],'bank_out':retained,'spare_ids':spares})
        bank=retained
    assert not bank and set(h)==value['D'] and len(set(h.values()))==len(h)
    assert set(h.values())<=value['U'] and all(h[d]==u for d,u in value['h0'].items())
    assert peak<=25
    value.update({'h':h,'debt_receipts':records,'full_cut_before_macro':start,'dmax':dmax,'max_working_units':peak,
        'source_positive_surplus':sum(max(2*m['H']-m['Q'],0) for m in mm)})
    return value
