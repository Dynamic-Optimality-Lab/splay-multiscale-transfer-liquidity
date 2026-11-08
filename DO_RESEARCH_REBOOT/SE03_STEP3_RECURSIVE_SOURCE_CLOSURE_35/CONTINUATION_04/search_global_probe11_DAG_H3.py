"""Exact source-subgraph augmentation; no arbitrary HIGH endpoint edges."""
from pathlib import Path
wrapper=Path(__file__).with_name('search_global_probe11_DAG_v2.py').read_text()
injection=r'''
import re
source=source.replace('global_probe11_LOW_model.pkl','global_probe11_LOW_H3_model.pkl')
source=source.replace('global_probe11_DAG_','global_probe11_H3_DAG_')
source=source.replace('independent_probe11_DAG_conversion.json','independent_probe11_H3_augmentation.json')
source=source.replace('from probe11_dag_apply import Apply','from probe11_dag_apply_bounded import Apply')
source=source.replace('for h in (1,2):','for h in (1,2,3):')
def optional_group(match):
    indent,rest=match.group(1),match.group(2)
    return indent+'data=groups.get((h,g,x))\n'+indent+'if data is None:continue\n'+indent+rest
source=re.sub(r'(?m)^([ \t]*)data=groups\[h,g,x\];(.*)$',optional_group,source)
old="out.append({'B_source':bs,'B_target':b,'A_source':asrc,'A_target':a,'H':h,'Q':q,'helper_DELETE':y or None,'KEEP':x,'weight':w})"
new="""if h==3:
                code=y;word=[]
                while code>1:word.append(code%12);code//=12
                assert code==1;word.reverse();assert word and word[-1]==x and all(1<=k<=11 for k in word)
            else:word=([y,x] if y else [x])
            out.append({'B_source':bs,'B_target':b,'A_source':asrc,'A_target':a,'H':h,'Q':q,'KEEP':x,'weight':w,
              'A_word':[{'kind':'D' if j<len(word)-1 else 'K','key':k} for j,k in enumerate(word)]})"""
assert source.count(old)==1;source=source.replace(old,new)
source=source.replace('LOW_ALL_NATIVE11_COMPLETE','LOW_AND_ADDED_H3_SUBGRAPH_COMPLETE')
exec(compile(source,str(Path(__file__).resolve()),'exec'))
'''
old="exec(compile(source,str(Path(__file__).resolve()),'exec'))"
assert wrapper.count(old)==1
wrapper=wrapper.replace(old,injection)
exec(compile(wrapper,str(Path(__file__).resolve()),'exec'))
