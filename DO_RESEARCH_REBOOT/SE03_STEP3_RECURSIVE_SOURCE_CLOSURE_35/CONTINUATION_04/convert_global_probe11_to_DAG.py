import collections,hashlib,json,pickle,sys,time
from pathlib import Path
import numpy as np
F=Path(__file__).resolve().parent;P=F.parents[1];sys.path.insert(0,str(F));B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
from probe11_decision_dag import DAG
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    with (F/'global_probe11_LOW_model.pkl').open('rb') as f:m=pickle.load(f)
    with (F/'global_probe11_LOW_02.pkl').open('rb') as f:old=pickle.load(f)
    assert old['status']=='CHECKPOINT' and not old['tracking'];dag=DAG();mapping={};values_checked=0
    for pid,(g,entries) in old['profiles'].items():
        n=len(m['classes'][g-1]);size=1<<(n-1).bit_length();root=dag.changes(-1,size,[s for s,v in entries],[v for s,v in entries])
        expected=np.zeros(n,dtype=np.int32)
        for s,v in entries:expected[s]=v
        assert np.array_equal(dag.vector(root,n),expected);mapping[pid]=root;values_checked+=n
    columns=[mapping[p] for p in old['columns']];dag.collect(columns);assert len(dag.nodes)+m['A_count']+m['B_count']<2000000
    z={'status':'CONVERTED_CHECKPOINT_NOT_COMPLETE','nodes':dag.nodes,'nextid':dag.nextid,'columns':columns,
      'pending':collections.deque(range(m['B_count'])),'inqueue':bytearray([1])*m['B_count'],
      'processed':old['processed'],'updates':old['updates'],'max_D':old['max_D'],'tracking':False,'parents':{},
      'old_profile_roots':mapping,'all_B_rescheduled_for_v2_correction':True,'source_queries':0,
      'input_sha256':{p:sha(F/p) for p in ('global_probe11_LOW_02.pkl','global_probe11_LOW_model.pkl','DECISION_DAG_REPRESENTATION.md')}}
    with (F/'global_probe11_DAG_entry.pkl').open('xb') as f:pickle.dump(z,f,protocol=5)
    report={'status':z['status'],'old_unique_positive_cells':old['unique_positive_cells'],'DAG_nodes':len(dag.nodes),
      'old_profiles':len(mapping),'all_profile_domain_values_checked':values_checked,'all_B_rescheduled':len(columns),
      'source_queries':0,'JR35':'OPEN','input_sha256':z['input_sha256']}
    with (F/'global_probe11_DAG_entry.json').open('x',encoding='utf8') as f:json.dump(report,f,indent=2)
    print(json.dumps(report),flush=True);assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_proof233_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
