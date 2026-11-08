from pathlib import Path
p=Path(__file__).resolve().parents[2]/'SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/CONTINUATION_04/audit_natural_owner_creator.py'
s=p.read_text()
for var in ('pred','death'):
    for key in ('before','after'):s=s.replace(f"{var}['{key}']",f"{var}['A_{key}']")
s=s.replace('audit_verify142_exit.json','audit_verify143_exit.json')
globals()['__file__']=str(p)
exec(compile(s,str(p),'exec'))
