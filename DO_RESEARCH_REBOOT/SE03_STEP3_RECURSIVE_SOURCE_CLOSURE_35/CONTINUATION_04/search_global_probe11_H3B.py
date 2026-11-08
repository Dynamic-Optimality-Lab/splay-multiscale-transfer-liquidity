"""Literal source-model extension B, exact lossless DAG and bounded caches."""
from pathlib import Path
p=Path(__file__).with_name('search_global_probe11_DAG_H3_v2.py')
s=p.read_text()
mark='assert parent.count(marker)==1'
addition=r'''
extra += r"""
source=source.replace('global_probe11_LOW_H3_model.pkl','global_probe11_LOW_H3B_model.pkl')
source=source.replace('global_probe11_H3_DAG_','global_probe11_H3B_DAG_')
source=source.replace('independent_probe11_H3_augmentation.json','independent_probe11_H3B_augmentation.json')
needle="bt=int(m['B_destination'][b,x-1]);q=int(m['B_Q'][b,x-1]);target=columns[bt];ck=(g,source,x,q);nt=len(classes[x-1])"
assert source.count(needle)==1
source=source.replace(needle,needle+'\n            if ap.maximum(source)+q<=2:continue')
"""
'''
assert s.count(mark)==1;s=s.replace(mark,addition+mark)
exec(compile(s,str(Path(__file__).resolve()),'exec'))
