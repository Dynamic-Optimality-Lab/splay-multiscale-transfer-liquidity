from pathlib import Path
p=Path(__file__).resolve().parents[2]/'SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/CONTINUATION_04/audit_projected_cluster_theorem.py'
s=p.read_text()
old="    assert set(af['S'])==set(old['physical_keys'])"
assert s.count(old)==1
s=s.replace(old,"    assert set(af['S'])==set(range(1,old['physical_keys']+1))")
s=s.replace('audit_verify126_exit.json','audit_verify127_exit.json')
globals()['__file__']=str(p)
exec(compile(s,str(p),'exec'))
