from pathlib import Path
p=Path(__file__).resolve().parents[2]/'SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/CONTINUATION_04/derive_FP_SI34_countercut.py'
s=p.read_text().replace("initial=tup(cert['source']['initial_full_B']);BF=initial;rows=[]",
 """assert cert['source']['initial_full_B']=={'kind':'right_vine','keys':[1,15]}
    initial=V.vine(1,15);BF=initial;rows=[]""")
s=s.replace('audit_core49_exit.json','audit_core50_exit.json')
globals()['__file__']=str(p)
exec(compile(s,str(p),'exec'))
