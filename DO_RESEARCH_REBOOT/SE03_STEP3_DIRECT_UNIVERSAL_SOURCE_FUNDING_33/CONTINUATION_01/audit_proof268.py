"""Assemble the complete restricted sign certificate and source interfaces."""
import hashlib,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;F=B.parents[1]/'SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/CONTINUATION_04'
START=time.process_time();CAP=float(sys.argv[1])
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    low=json.loads((F/'independent_probe11_LOW_B_03.json').read_text())
    high=json.loads((F/'independent_probe11_HIGH_envelope_B01.json').read_text())
    three=json.loads((F/'independent_probe11_H3_actual_signs_B01.json').read_text())
    cp=F/'global_probe11_H3B_DAG_01.pkl';h=sha(cp)
    assert low['status']=='PASS_ALL_COMPLETE_NATIVE11_LOW_INEQUALITIES' and low['candidate_sha256']==h
    assert high['input_sha256'][cp.name]==h and high['H_ge_4_failed_envelopes']==0
    assert three['input_sha256'][cp.name]==h and not three['actual_H3_failure_controls'] and three['LOW_quiescent']
    pins=[F/'NATIVE11_FULL_SOURCE_THEOREM.md',cp,F/'independent_probe11_LOW_B_01.json',F/'independent_probe11_LOW_B_02.json',
      F/'independent_probe11_LOW_B_03.json',F/'independent_probe11_HIGH_envelope_B01.json',
      F/'independent_probe11_H3_actual_signs_B01.json',F/'independent_global_probe11_LOW_model.json',
      F/'independent_probe11_source_actions.json',B/'STREAMED_BLOCK_THEOREM.md',
      B.parents[1]/'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/UNIFORM_R_TRANSFER.md',
      B.parents[1]/'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/ABSOLUTE_PERIOD_ALIGNMENT.md']
    r={'status':'RESTRICTED_NATIVE11_SOURCE_SIGN_DERIVATION_COMPLETE','D_range':[0,4],
      'c':'min(H,4)','Bank25_conservative_working_bound':12,'source_queries':0,'source_engine_calls':0,
      'independent_sign_checks':'complete LOW, exact H3, all H>=4 envelope','physical_allocator_control':'PENDING',
      'domain':'eleven fixed accessed anchors with only rigid anchor-free hangers',
      'arbitrary_active_ancestors_or_support_extension':False,'JR35':'OPEN','reservation':'DEFERRED',
      'input_sha256':{str(p):sha(p) for p in pins}}
    with (F/'native11_full_source_certificate.json').open('x',encoding='utf8') as f:json.dump(r,f,indent=2)
    print(json.dumps({k:v for k,v in r.items() if k!='input_sha256'}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_proof268_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
