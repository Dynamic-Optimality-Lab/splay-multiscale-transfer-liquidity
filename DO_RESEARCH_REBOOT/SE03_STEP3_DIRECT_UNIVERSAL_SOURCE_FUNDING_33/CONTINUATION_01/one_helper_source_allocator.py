"""Instantiate the independently checked source-state law on actual rows."""
import json
from pathlib import Path
B=Path(__file__).resolve().parent
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def build(rows,macros,h0,helper=3):
    aa=json.loads((B/'ten_anchor_LOW_source_schemas.json').read_text());ff=json.loads((B/'nine_label_native_action_cache.json').read_text());cc=json.loads((B/('one_helper_p%d_certificate.json'%helper)).read_text());assert 1<=helper<=5
    ai={fr(t):i for i,t in enumerate(aa['trees'])};bi={fr(t):i for i,t in enumerate(ff['trees'])};D=dict(cc['nonzero_debt']);N=len(bi);marks=[k for k in range(1,11) if k!=helper];rank={k:i+1 for i,k in enumerate(marks)}
    def bf(t):
        def prune(v):
            if isinstance(v,str):return None
            k,l,r=v
            if k==helper:assert isinstance(l,str) and isinstance(r,str);return None
            return rank[k],prune(l),prune(r)
        def gaps(v,upper=9):
            if v is None:return 'F'+str(upper)
            k,l,r=v;return k,gaps(l,k-1),gaps(r,upper)
        return gaps(prune(fr(t)))
    def debt(state):return D.get(ai[fr(state[0])]*N+bi[bf(state[1])],0)
    rm={r['occurrence']:r for r in rows};segs=[[rm[t] for t in m['occurrences']] for m in macros];ds=[debt(seg[0]['before']) for seg in segs];dt=[debt(seg[-1]['after']) for seg in segs]
    assert all(dt[i]==ds[(i+1)%len(macros)] for i in range(len(macros)));K=max(ds);cut=ds.index(K);bank=[];h=dict(h0);receipt=[];peak=0
    for j in range(len(macros)):
        i=(cut+j)%len(macros);m=macros[i];assert len(bank)==K-ds[i];ev=[(r['occurrence'],k) for r in segs[i] for k in range(1,r['a']+1)];H=len(ev);c=min(H,3);selected=[e+(b,) for e in ev[:c] for b in (0,1)];dd=m['demands'];fixed={d:h0[d] for d in dd if d in h0}
        assert set(fixed.values())<=set(selected) and 2*c-len(dd)+dt[i]-ds[i]>=0;peak=max(peak,len(bank)+len(selected));pool=bank+[u for u in selected if u not in fixed.values()];new=[]
        for d in dd:
            if d not in fixed:u=pool.pop(0);h[d]=u;new.append((d,u))
        keep=K-dt[i];assert len(pool)>=keep;release=pool[keep:];bank=pool[:keep]
        receipt.append({'macro_index':i,'occurrences':m['occurrences'],'H':H,'Q':len(dd),'D_source':ds[i],'D_target':dt[i],'c':c,'selected':selected,'fixed':list(fixed.items()),'new':new,'carry':bank,'released':release,'signed_margin':2*c-len(dd)+dt[i]-ds[i]})
    assert not bank and len(set(h.values()))==len(h) and peak<=8 and all(h[d]==u for d,u in h0.items())
    return {'h':h,'working_peak':peak,'max_debt':K,'cut_before_macro':cut,'receipt':receipt}
