"""Preserve old rows and add every audited checkpoint14 H3 endpoint."""
from pathlib import Path
p=Path(__file__).resolve().parents[2]/'SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/CONTINUATION_04/augment_probe11_H3_model.py'
s=p.read_text()
s=s.replace("with (F/'global_probe11_LOW_model.pkl')","with (F/'global_probe11_LOW_H3_model.pkl')")
s=s.replace('global_probe11_DAG_07.pkl','global_probe11_H3_DAG_14.pkl')
s=s.replace('independent_probe11_H3_source_07.json','independent_probe11_H3_source_14.json')
s=s.replace('probe11_H3_source_resolution_07.json','probe11_H3_source_resolution_14.json')
old="a=np.array([(s,t,c) for (s,t),c in sorted(rows.items())],dtype=np.int32);model['groups'][key]=a;count+=len(a)"
new="""a=np.array([(s,t,c) for (s,t),c in sorted(rows.items())],dtype=np.int32)
        if key in old['groups']:
            previous=old['groups'][key]
            assert not {(int(s),int(t)) for s,t,c in previous}&set(rows)
            model['groups'][key]=np.concatenate((previous,a))
        else:model['groups'][key]=a
        count+=len(a)"""
assert s.count(old)==1;s=s.replace(old,new)
s=s.replace("model['H_counts'][3]=count","model['H_counts'][3]=old['H_counts'].get(3,0)+count")
s=s.replace("modelpath=F/'global_probe11_LOW_H3_model.pkl'","modelpath=F/'global_probe11_LOW_H3B_model.pkl'")
s=s.replace('global_probe11_H3_DAG_entry.pkl','global_probe11_H3B_DAG_entry.pkl')
s=s.replace('global_probe11_H3_augmentation.json','global_probe11_H3B_augmentation.json')
s=s.replace("('global_probe11_LOW_H3_model.pkl','global_probe11_H3B_DAG_entry.pkl'","('global_probe11_LOW_H3B_model.pkl','global_probe11_H3B_DAG_entry.pkl'")
s=s.replace('audit_proof243_exit.json','audit_proof265_exit.json')
globals()['__file__']=str(p)
exec(compile(s,str(p),'exec'))
