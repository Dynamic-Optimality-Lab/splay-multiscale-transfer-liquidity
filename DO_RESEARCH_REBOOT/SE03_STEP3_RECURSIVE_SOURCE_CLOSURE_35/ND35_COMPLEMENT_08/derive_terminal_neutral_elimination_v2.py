"""Correct the annotation direction: A label loss is a MISSING-label addition.

The failed v1/phase298 and its charges remain unchanged. No mathematical
claim is accepted from that failed run.
"""
from pathlib import Path
p=Path(__file__).with_name('derive_terminal_neutral_elimination.py');s=p.read_text()
old="losses=[i for i in aindices if I in fine[i]['removed']]"
assert s.count(old)==1;s=s.replace(old,"losses=[i for i in aindices if I in fine[i]['added']]")
s=s.replace("F/'derive_terminal_neutral_elimination.py')}}", "F/'derive_terminal_neutral_elimination.py',F/'derive_terminal_neutral_elimination_v2.py')}}")
s=s.replace('audit_proof298_exit.json','audit_proof299_exit.json')
exec(compile(s,str(Path(__file__).resolve()),'exec'))
