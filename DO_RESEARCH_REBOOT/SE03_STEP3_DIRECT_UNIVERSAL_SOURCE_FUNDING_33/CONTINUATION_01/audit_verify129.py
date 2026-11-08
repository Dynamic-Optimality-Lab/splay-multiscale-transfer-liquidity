"""Reuse the independent decoder; check new checkpoint, not source closure."""
import sys
from pathlib import Path
p=Path(__file__).resolve().parents[2]/'SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/CONTINUATION_04/audit_probe11_DAG_checkpoint.py'
s=p.read_text();sys.argv.extend(['13','verify129'])
s=s.replace('as f:m=pickle.load(f)','as f:m={k:v for k,v in pickle.load(f).items() if k in ("B_count","roots","classes")}')
s=s.replace("name=f'global_probe11_DAG_{BATCH:02d}.pkl'","name=f'global_probe11_H3_DAG_{BATCH:02d}.pkl'")
s=s.replace("assert mx==now['max_D'] and not now['cycle']",
    """assert mx==now['max_D'] and not now['cycle']
    pending=list(now['pending'])
    assert len(set(pending))==len(pending) and all(0<=i<m['B_count'] for i in pending)
    assert set(pending)=={i for i,z in enumerate(now['inqueue']) if z}
    assert len(nn)+len(on)+len(memo)+2*m['B_count']<2000000""")
s=s.replace("f'independent_probe11_DAG_checkpoint_{BATCH:02d}.json'","f'independent_probe11_H3_DAG_checkpoint_{BATCH:02d}.json'")
globals()['__file__']=str(p)
exec(compile(s,str(p),'exec'))
