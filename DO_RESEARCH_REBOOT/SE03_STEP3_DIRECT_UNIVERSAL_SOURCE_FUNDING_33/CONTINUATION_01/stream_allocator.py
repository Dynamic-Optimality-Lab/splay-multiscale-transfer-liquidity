"""Selected-bit OFFLINE BLOCK allocation under the written static license.
Actual event IDs enter once; assigned output is not an unassigned bank.
No original tree is operated or simulated here.
"""
from collections import deque
def allocate(events,selected,fixed,demands,incoming,outgoing):
    selected=set(selected);fixed=dict(fixed);inverse={u:d for d,u in fixed.items()}
    demands=list(demands);bank=deque(incoming);iterator=iter(events);payments={};released=[];trace=[];peak=len(bank)
    assert len(inverse)==len(fixed) and set(inverse)<=selected and set(fixed)<=set(demands)
    assert len(set(incoming))==len(incoming)
    missing=[d for d in demands if d not in fixed];allunits=set();read_units=set()
    def visit():
        nonlocal peak
        event=next(iterator);units=[event+(b,) for b in (0,1)]
        assert not set(units)&read_units;read_units.update(units);allunits.update(units)
        peak=max(peak,len(bank)+2);before=list(bank);emitted=[];free=[]
        for u in units:
            if u in inverse:payments[inverse[u]]=u;emitted.append((inverse[u],u))
            elif u in selected:bank.append(u);free.append(u)
            else:released.append(u)
        trace.append({'event':event,'before':before,'fixed_emitted':emitted,'free_added':free,'bank_after_visit':list(bank)})
    assert len(incoming)+len(selected)-len(fixed)>=len(missing)+outgoing
    for d in missing:
        while not bank:visit()
        u=bank.popleft();assert d not in payments;payments[d]=u
        trace.append({'pay_missing':d,'unit':u,'bank_after_payment':list(bank)})
    while len(bank)>outgoing:released.append(bank.pop())
    while len(bank)<outgoing:visit()
    while len(bank)>outgoing:released.append(bank.pop())
    while True:
        try:visit()
        except StopIteration:break
        while len(bank)>outgoing:released.append(bank.pop())
    assert set(payments)==set(demands) and len(set(payments.values()))==len(payments)
    assert len(bank)==outgoing and selected<=allunits and not allunits.intersection(incoming)
    assert set(payments.values()).isdisjoint(bank) and set(payments.values()).isdisjoint(released) and set(bank).isdisjoint(released)
    assert set(payments.values())|set(bank)|set(released)==allunits|set(incoming)
    return {'payments':payments,'carry':list(bank),'released':released,'peak':peak,'trace':trace}
