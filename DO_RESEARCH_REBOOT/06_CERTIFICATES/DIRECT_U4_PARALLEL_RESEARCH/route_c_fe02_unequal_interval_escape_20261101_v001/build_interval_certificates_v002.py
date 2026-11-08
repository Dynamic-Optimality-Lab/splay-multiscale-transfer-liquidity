"""Append-only correction of one unmatched parenthesis in the v001 producer.

V001 failed at parsing before creating any output. No source/campaign
scope or computation changes; retain the original draft verbatim.
"""
from pathlib import Path

p=Path(__file__).with_name('build_interval_certificates.py')
s=p.read_text(encoding='utf-8')
old="    B=N(1,'L',N(2,None,N(3,None,N(4,None,N(5,'F'))))))"
new="    B=N(1,'L',N(2,None,N(3,None,N(4,None,N(5,'F')))))"
assert s.count(old)==1
exec(compile(s.replace(old,new),str(p)+' [v002 parse correction]','exec'),globals())
