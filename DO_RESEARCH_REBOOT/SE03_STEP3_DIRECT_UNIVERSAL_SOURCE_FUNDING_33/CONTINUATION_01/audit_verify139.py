from pathlib import Path
p=Path(__file__).resolve().parents[2]/'SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/CONTINUATION_04/audit_probe11_H3_checkpoint13.py'
s=p.read_text().replace('global_probe11_H3_DAG_13.pkl','global_probe11_H3B_DAG_01.pkl')
s=s.replace('independent_probe11_HIGH_envelope_H3_13.json','independent_probe11_HIGH_envelope_B01.json')
s=s.replace('independent_probe11_H3_actual_signs_13.json','independent_probe11_H3_actual_signs_B01.json')
s=s.replace('CHECKPOINT13','CANDIDATE_B01').replace("'LOW_quiescent':False","'LOW_quiescent':True")
s=s.replace('audit_verify131_exit.json','audit_verify139_exit.json')
globals()['__file__']=str(p)
exec(compile(s,str(p),'exec'))
