"""Complete actual-ID core8 independent source allocator using the new
mark-independent table. No source engine; caller supplies certified rows.
"""
import json,collections
from pathlib import Path
B=Path(__file__).resolve().parent
def fr(v):return tuple(fr(x) for x in v) if isinstance(v,list) else v
def build(rows,macros,h0):
    src=json.loads((B/'eight_core_B_source_relation.json').read_text());D=json.loads((B/'eight_core_B_law_result.json').read_text())['D']
    index={fr(t):i for i,t in enumerate(src['trees'])}
    # This executable instantiation has the8 explicit anchor labels. The
    # theorem handles order-normalization and arbitrary gap substitution.
    def debt(t):return D[index[fr(t)]]
    ds=[debt(m['rows'][0]['before'][1]) for m in macros];dt=[debt(m['rows'][-1]['after'][1]) for m in macros]
    assert all(dt[i]==ds[(i+1)%len(macros)] for i in range(len(macros)))
    K=max(ds);cut=ds.index(K);bank=[];h=dict(h0);receipt=[];peak=0
    for j in range(len(macros)):
        i=(cut+j)%len(macros);m=macros[i];assert len(bank)==K-ds[i]
        events=[(r['occurrence'],k) for r in m['rows'] for k in range(1,r['a']+1)];H=len(events);c=min(H,2)
        selected=[ev+(b,) for ev in events[:c] for b in (0,1)];dd=m['demands'];fixed={d:h0[d] for d in dd if d in h0}
        assert set(fixed.values())<=set(selected);assert 2*c-len(dd)+dt[i]-ds[i]>=0
        peak=max(peak,len(bank)+len(selected));free=[u for u in selected if u not in fixed.values()];pool=bank+free;added=[]
        for d in dd:
            if d not in fixed:
                assert pool;u=pool.pop(0);h[d]=u;added.append((d,u))
        keep=K-dt[i];assert len(pool)>=keep;released=pool[keep:];bank=pool[:keep]
        receipt.append({'macro_index':i,'ds':ds[i],'dt':dt[i],'c':c,'selected':selected,'fixed':list(fixed.items()),
                        'new':added,'carry':bank,'released':released,'margin':2*c-len(dd)+dt[i]-ds[i]})
    assert not bank and len(set(h.values()))==len(h) and peak<=5 and all(h[d]==u for d,u in h0.items())
    return {'h':h,'cut_before_macro':cut,'maxD':K,'working_peak':peak,'receipt':receipt}
