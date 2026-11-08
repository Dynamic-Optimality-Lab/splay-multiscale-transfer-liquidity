from pathlib import Path
p=Path(__file__).with_name('audit_core50.py')
s=p.read_text()
old="s=s.replace('audit_core49_exit.json','audit_core50_exit.json')"
new="""s=s.replace('range(1,(e-prev)%N)','range(1,((e-prev)%N or N))')
s=s.replace('audit_core49_exit.json','audit_core51_exit.json')"""
assert s.count(old)==1;s=s.replace(old,new)
exec(compile(s,str(p),'exec'))
