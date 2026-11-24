"""Exact cyclic global credit teacher. It does not assert a universal mean bound."""
from collections import deque


def drawdown(deltas):
    """Maximum cyclic interval demand-minus-supply, length at most one lap."""
    n=len(deltas);assert n and sum(deltas)<=0
    prefix=[0]
    for v in deltas*2:prefix.append(prefix[-1]+v)
    queue=deque([0]);best=(0,0,0)
    for end in range(1,2*n+1):
        while queue and queue[0]<end-n:queue.popleft()
        if queue:
            value=prefix[end]-prefix[queue[0]]
            if value>best[0]:best=(value,queue[0],end)
        while queue and prefix[queue[-1]]>=prefix[end]:queue.pop()
        queue.append(end)
    return {'capacity':best[0],'start':best[1]%n,'length':best[2]-best[1]}


def cyclic_credit(events,C):
    assert C>=0 and sum(e['q'] for e in events)<=C*sum(e['a'] for e in events)
    word=[e['q']-C*e['a'] for e in events];cut=drawdown(word);capacity=cut['capacity']
    def sweep(start,record=False):
        G=start;rows=[];issued=paid=unpaid=0
        for e in events:
            old=G
            if e['a']:
                G=min(capacity,G+C);issue=G-old;pay=loss=0
            else:
                issue=0;pay=min(G,e['q']);loss=e['q']-pay;G-=pay
            assert G-old==issue-pay
            issued+=issue;paid+=pay;unpaid+=loss
            if record:rows.append({'id':e['id'],'before':old,'after':G,'issued':issue,'paid':pay,'unpaid':loss})
        return G,{'issued':issued,'paid':paid,'unpaid':unpaid,'rows':rows}
    G=capacity;passes=[]
    for _ in range(capacity+1):
        new,r=sweep(G);assert new<=G;passes.append([G,new])
        if new==G:break
        G=new
    else:raise AssertionError('monotone global reserve rank failed')
    final,result=sweep(G,True);assert final==G and result['unpaid']==0 and result['issued']==result['paid']
    # Periodic integral provenance: every debit gets a unique real original
    # A-unit slot, including credits crossing the original cyclic seam.
    def labels(initial):
        queue=deque(initial);assignments=[];next_slot={}
        for e,row in zip(events,result['rows']):
            for _ in range(row['issued']):
                identifier=tuple(e['id']);slot=next_slot.get(identifier,0);next_slot[identifier]=slot+1
                assert slot<C;queue.append([*identifier,slot])
            for _ in range(row['paid']):assignments.append({'B':e['id'],'A_credit':queue.popleft()})
        return list(queue),assignments
    tokens,unused=labels([['boundary_placeholder',i] for i in range(G)])
    for _ in range(3):
        end,assignments=labels(tokens)
        if end==tokens:break
        tokens=end
    else:raise AssertionError('credit labels did not stabilize')
    assert not any(a['A_credit'][0]=='boundary_placeholder' for a in assignments)
    assigned=[tuple(a['A_credit']) for a in assignments];assert len(assigned)==len(set(assigned))
    return {'C':C,'capacity':capacity,'max_cyclic_deficit':cut,'initial_greatest_fixed_point':G,
        'passes':passes,'closed':True,**result,'credit_assignments':assignments,
        'boundary_credit_labels':tokens,'physical_prefix_credit_used':False,
        'scope':'Exact certificate on this complete cost word; a global mean bound is not assumed for arbitrary sources.'}
