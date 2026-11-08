"""Lossless exact row sharing on a completed, already independently checked debt."""
import hashlib,json,pickle,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1]
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    with (F/'active_a9_02.pkl').open('rb') as f:z=pickle.load(f)
    assert z['status']=='COMPLETE'
    profiles={};index=[]
    for row in z['level']:
        key=tuple(sorted(row.items()))
        if key not in profiles:profiles[key]=len(profiles)
        index.append(profiles[key])
    cells=sum(len(key) for key in profiles)
    r={'status':'EXACT_EXTENTIONAL_PROFILE_COUNTS','original_positive_cells':z['nonzero_states'],
       'unique_profiles':len(profiles),'unique_profile_cells':cells,'column_indices':len(index),
       'ratio':cells/z['nonzero_states'],'profile_compression_is_bisimulation_claim':False,
       'meaning':'lossless symbolic debt function D(A,B)=profile[index(B)](A), not a source-state identification',
       'source_queries':0,'source_engine_calls':0,'input_sha256':{'active_a9_02.pkl':sha(F/'active_a9_02.pkl')}}
    with (F/'profile_representation_diagnosis.json').open('x',encoding='utf-8') as f:json.dump(r,f,indent=2)
    print(json.dumps(r),flush=True);assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_proof199_exit.json').open('x',encoding='utf-8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
