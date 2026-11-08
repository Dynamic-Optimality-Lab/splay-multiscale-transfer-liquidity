"""Discard an image only when its exact maximum upper bound is nonpositive.

All model edges have H>=1. The target function is everywhere nonnegative.
Thus max(source)+Q<=2 implies every update candidate is <=0. This changes
neither a source edge nor the monotone fixed point, including with tracking.
"""
from pathlib import Path
p=Path(__file__).with_name('search_global_probe11_DAG_H3_v2.py')
s=p.read_text()
mark='assert parent.count(marker)==1'
assert s.count(mark)==1
extra=r'''
extra += """
needle='bt=int(m[\\'B_destination\\'][b,x-1]);q=int(m[\\'B_Q\\'][b,x-1]);target=columns[bt];ck=(g,source,x,q);nt=len(classes[x-1])'
assert source.count(needle)==1
source=source.replace(needle,needle+'\\n            if ap.maximum(source)+q<=2:continue')
"""
'''
s=s.replace(mark,extra+mark)
exec(compile(s,str(Path(__file__).resolve()),'exec'))
