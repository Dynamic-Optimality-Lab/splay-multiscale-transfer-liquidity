"""Actual-ID instantiation of the complete native10 source credit law."""
import json
from pathlib import Path
B=Path(__file__).resolve().parent
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
class Allocator:
    def __init__(self):
        z=json.loads((B/'native10_source_actions.json').read_text());c=json.loads((B/'native10_credit_certificate.json').read_text());self.N=len(z['trees']);self.index={fr(t):i for i,t in enumerate(z['trees'])};self.mirror=z['mirror'];self.level=dict(c['nonzero_debt'])
    def debt(self,state):
        a,b=(self.index[fr(t)] for t in state[:2]);N=self.N
        return self.level.get(min(a*N+b,self.mirror[a]*N+self.mirror[b]),0)
    def build(self,rows,macros,h0):
        rm={r['occurrence']:r for r in rows};ss=[[rm[t] for t in m['occurrences']] for m in macros];ds=[self.debt(s[0]['before']) for s in ss];dt=[self.debt(s[-1]['after']) for s in ss];assert all(dt[i]==ds[(i+1)%len(ds)] for i in range(len(ds)))
        K=max(ds);cut=ds.index(K);bank=[];h=dict(h0);log=[];peak=0
        for j in range(len(macros)):
            i=(cut+j)%len(macros);m=macros[i];ev=[(r['occurrence'],k) for r in ss[i] for k in range(1,r['a']+1)];c=min(len(ev),3);sel=[e+(b,) for e in ev[:c] for b in (0,1)];dd=m['demands'];fixed={d:h0[d] for d in dd if d in h0};assert set(fixed.values())<=set(sel) and len(bank)==K-ds[i]
            margin=2*c-len(dd)+dt[i]-ds[i];assert margin>=0;peak=max(peak,len(bank)+len(sel));pool=[u for u in sel if u not in fixed.values()]+bank;new=[]
            for d in dd:
                if d not in fixed:u=pool.pop(0);h[d]=u;new.append((d,u))
            keep=K-dt[i];assert len(pool)>=keep;released=pool[keep:];bank=pool[:keep];log.append({'macro_index':i,'occurrences':m['occurrences'],'H':len(ev),'Q':len(dd),'D_source':ds[i],'D_target':dt[i],'c':c,'selected':sel,'fixed':list(fixed.items()),'new':new,'carry':bank,'released':released,'margin':margin})
        assert not bank and peak<=9 and all(h[d]==u for d,u in h0.items()) and len(set(h.values()))==len(h)
        return {'h':h,'max_debt':K,'working_peak':peak,'cut_before_macro':cut,'receipt':log}
