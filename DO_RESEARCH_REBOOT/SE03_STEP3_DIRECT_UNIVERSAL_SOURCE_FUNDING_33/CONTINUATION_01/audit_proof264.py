"""Exact omitted H3 images, retaining every violating endpoint."""
from pathlib import Path
p=Path(__file__).resolve().parents[2]/'SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/CONTINUATION_04/resolve_probe11_H3_source.py'
s=p.read_text()
s=s.replace("as f:m=pickle.load(f)","as f:m={k:v for k,v in pickle.load(f).items() if k in ('A_count','classes','local','roots','B_Q','B_destination')}")
s=s.replace("as f:primitive=pickle.load(f)","as f:primitive={k:v for k,v in pickle.load(f).items() if k in ('destination','H','Q')}")
s=s.replace("cname=f'global_probe11_DAG_{NATIVE_BATCH:02d}.pkl'","cname='global_probe11_H3_DAG_14.pkl'")
s=s.replace("rows=[];proofs=[];compositions=0","mm.clear();ranges.clear();rows=[];proofs=[];compositions=0")
s=s.replace(")[:8]",")")
s=s.replace('probe11_H3_source_resolution_07.json','probe11_H3_source_resolution_14.json')
s=s.replace('audit_proof242_exit.json','audit_proof264_exit.json')
s=s.replace("'LOW_quiescence':False","'LOW_quiescence':True")
globals()['__file__']=str(p)
exec(compile(s,str(p),'exec'))
