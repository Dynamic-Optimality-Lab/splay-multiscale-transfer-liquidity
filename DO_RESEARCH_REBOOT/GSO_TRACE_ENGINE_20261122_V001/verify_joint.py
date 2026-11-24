"""Independent rational local-value/cyclic-bank certificate verification."""
import sys
import json
from fractions import Fraction
from collections import Counter
sys.dont_write_bytecode=True
import verify as V


def main():
    cert=V.read(V.HERE/'joint_001/CERTIFICATE.json.gz');assert cert['status']=='FINITE_EXACT_JOINT'
    f={s:Fraction(v) for s,v in cert['values'].items()};c=Fraction(cert['c']);d=Fraction(cert['d']);H=Fraction(cert['H']);assert min(c,d,H)>=0
    total=0;source_summaries=[]
    for h in cert['histories']:
        i=h['index'];z=V.read(V.HERE/f'run_001/trace_{i:02d}.json.gz');owner={x:j for j,p in enumerate(z['blocks']) for x in p};events=[]
        for r in z['operations']:
            if r['k']:events.append({'id':['K',r['id']],'a':0,'q':0,'k':1,'scope':[owner[r['target']]],'delta':{}})
            for s in z['steps'][r['steps'][0]:r['steps'][1]]:
                delta=Counter(s['signature_after'].values());delta.subtract(s['signature_before'].values());events.append({k:s[k] for k in ('id','a','q','k','scope')}|{'delta':dict(delta)})
        stock={str(b):Fraction(v) for b,v in h['initial'].items()};start=stock.copy();assert set(stock)=={str(j) for j in range(len(z['blocks']))} and all(0<=v<=H for v in stock.values())
        assert len(events)==len(h['events']);lhs_sum=Fraction(0);budget=Fraction(0)
        for e,r in zip(events,h['events']):
            assert r['id']==e['id'] and set(r['before'])==set(r['after'])=={str(b) for b in e['scope']}
            before={b:Fraction(v) for b,v in r['before'].items()};after={b:Fraction(v) for b,v in r['after'].items()}
            assert all(stock[b]==v for b,v in before.items()) and all(0<=v<=H for v in after.values())
            phi=sum(v*f[s] for s,v in e['delta'].items() if v);change=sum(after.values())-sum(before.values());lhs=e['q']+phi+change;rhs=c*e['a']+d*e['k'];assert lhs<=rhs
            stock.update(after);lhs_sum+=lhs;budget+=rhs;total+=1
        assert stock==start and lhs_sum==z['Q_B'] and budget==c*z['A']+d*z['K_B'] and z['Q_B']<=budget
        source_summaries.append({'source_index':i,'events':len(events),'A':z['A'],'Q_B':z['Q_B'],'total_exact_signed_potential_and_bank_change':str(lhs_sum-z['Q_B']),'closed_bank':True})
    out={'passed':True,'events':total,'sources':source_summaries,'c':str(c),'d':str(d),'H':str(H),'scope':'Finite exact complete-history joint certificate. Per-source bank tables are not a universal update rule.','root_status':'OPEN'}
    if not (V.HERE/'FINAL_MANIFEST.json').exists():(V.HERE/'JOINT_INDEPENDENT_VERIFICATION.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(out))


if __name__=='__main__':main()
