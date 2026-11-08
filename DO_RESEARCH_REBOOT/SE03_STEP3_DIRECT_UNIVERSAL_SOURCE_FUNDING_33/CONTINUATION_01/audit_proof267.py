from pathlib import Path
p=Path(__file__).with_name('audit_proof264.py')
s=p.read_text().replace('global_probe11_H3_DAG_14.pkl','global_probe11_H3B_DAG_01.pkl')
s=s.replace('probe11_H3_source_resolution_14.json','probe11_H3_source_resolution_B01.json')
s=s.replace('audit_proof264_exit.json','audit_proof267_exit.json')
exec(compile(s,str(p),'exec'))
