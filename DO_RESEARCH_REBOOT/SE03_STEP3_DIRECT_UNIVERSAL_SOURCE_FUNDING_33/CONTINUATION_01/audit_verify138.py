from pathlib import Path
p=Path(__file__).resolve().parents[2]/'SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/CONTINUATION_04/audit_probe11_HIGH_envelope.py'
s=p.read_text().replace('global_probe11_DAG_06.pkl','global_probe11_H3B_DAG_01.pkl')
s=s.replace('independent_probe11_DAG_checkpoint_06.json','independent_probe11_LOW_B_03.json')
s=s.replace('independent_probe11_HIGH_envelope_06.json','independent_probe11_HIGH_envelope_B01.json')
s=s.replace("'source_queries':0,'source_engine_calls':0,'LOW_closed':False",
 """'H_ge_4_selected_events':4,'H_ge_4_minimum_margin':worst+2,
      'H_ge_4_failed_envelopes':int((genuine&(margins+2<0)).sum()),
      'source_queries':0,'source_engine_calls':0,'LOW_closed':True""")
s=s.replace('audit_verify121_exit.json','audit_verify138_exit.json')
globals()['__file__']=str(p)
exec(compile(s,str(p),'exec'))
