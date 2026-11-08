"""Append-only source-generator variant for arbitrarily long zero runs."""
from pathlib import Path
B=Path(__file__).resolve().parent;s=(B/'audit_discovery2.py').read_text()
start=s.index('def counter_word(r):');end=s.index('def main():',start)
new="""def counter_word(r):
    n=2*r-1;old=list(range(3,n+1,2))
    # Prepare the entire monotone return stack before the genuine K3.
    # Subsequent K5,K7,...,Kn each have one actual A event.
    return [('K',3),('K',n)]+[('D',y) for y in range(n-2,2,-2)]+[('K',3)]+[('K',y) for y in old[1:]+old[-2::-1]]+[('K',1)]+[('D',y) for y in range(n,0,-1)]
"""
s=s[:start]+new+s[end:]
s=s.replace('assert len(rr)<=4 and len(spare)>=2*(n-1)','assert len(rr)<=r-4 and len(spare)>=2*(n-1)')
s=s.replace("reports.append({'r':r,","reports.append({'family':'unbounded_zero_run','r':r,")
s=s.replace("'leaf_source_certificates2.json'","'zero_run_source_certificates.json'")
s=s.replace("'audit_discovery2_exit.json'","'audit_zero_run_exit.json'")
with (B/'audit_zero_run.py').open('x',encoding='utf-8') as f:f.write(s)
