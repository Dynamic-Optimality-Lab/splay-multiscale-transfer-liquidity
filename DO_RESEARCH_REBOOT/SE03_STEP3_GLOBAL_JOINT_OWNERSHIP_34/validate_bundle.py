"""Charged final status/dependency validation, not a universal proof check."""
import hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parent;B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
START=time.process_time();CAP=float(sys.argv[1])
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def main():
    required='SOURCE_INTEGRITY C33_INHERITANCE_LEDGER JIO34_PRINCIPAL_THEOREM GATE_U14_EXACT_CONTRACT EXACT_RESIDUAL_SOURCE_OWNERSHIP EXACT_GLOBAL_FEASIBILITY_MODEL JOINT_INTERIOR_EXTERIOR_ALLOCATION MINIMAL_GLOBAL_OWNER_OBSTRUCTION SHARED_RETIREMENT_COLLISION_RESOLUTION SOURCE_FORCED_GLOBAL_COMPATIBILITY GLOBAL_FROZEN_OWNER_EXTENSION GLOBAL_BANK25_SCHEDULING_PROOF ALL_SUPPORT_SOURCE_TRANSFER C33_WITNESS_RECONSTRUCTION_TEST HISTORICAL_COUNTEREXAMPLE_REGISTRY SOURCE_CLASS_COVERAGE JIO34_GATE_U14_BRIDGE E_R2_E_R3_STATUS UNCONDITIONAL_GATE_U_READINESS IAGS_PROOF_TREE PROOF_STATUS_REGISTRY FINAL_VERDICT CHECKPOINT C35_EXACT_HANDOFF POOLED_RETIREMENT_SOURCE_LAW OPERATION_RETIREMENT_EXACTNESS'.split()
    assert all((F/(n+'.md')).is_file() for n in required) and not (F/'FULL_PROOF.md').exists()
    for d in read(F/'dependency_manifest.json')['dependencies']:assert sha(Path(d['path']))==d['sha256']
    for name in ('independent_pool_audit.json','independent_new_source_and_lemma_audit.json','independent_retirement_exactness_audit.json'):
        rec=read(F/name)
        for p,h in rec['input_sha256'].items():assert sha(F/p)==h
    assert read(F/'independent_pool_audit.json')['source_receipts'][0]['current_owners']['old_values_preserved']==36
    assert read(F/'independent_pool_audit.json')['source_receipts'][0]['accepted_four_endpoints']['unpaid']==4
    assert read(F/'independent_new_source_and_lemma_audit.json')['source_queries']==418
    assert all(c['full_core']==7 and c['full_triple_and_chart_closure'] for c in read(F/'independent_new_source_and_lemma_audit.json')['source_receipts'])
    positive=['proof168','core40','verify80','verify81','verify83'];negative=['core41','core42','verify82']
    assert all(read(B/f'run_{p}_result.json')['status']=='PASS' for p in positive)
    assert all(read(B/f'run_{p}_result.json')['status']=='FAILED_OR_UNKNOWN' for p in negative)
    assert not (F/'maximal_diagnostic_source.json').exists() and not (F/'maximal_nonmonotone_source_control.json').exists()
    for n in ('JIO34_PRINCIPAL_THEOREM','PROOF_STATUS_REGISTRY','FINAL_VERDICT','CHECKPOINT','UNCONDITIONAL_GATE_U_READINESS'):
        assert 'OPEN' in (F/(n+'.md')).read_text(encoding='utf-8')
    result=dict(status='PASS_BUNDLE_INTEGRITY_AND_ACCURATE_SCOPE_STATUS',input_sha256={n+'.md':sha(F/(n+'.md')) for n in required},new_mathematical_result='OUTCOME_A_L_STRUCTURAL_PARTIAL',JIO34='OPEN',C33='OPEN',unconditional_Gate_U='OPEN',Universal_CD='OPEN',Dynamic_Optimality='OPEN',no_full_proof_written=True,old_owners_unchanged=True,historical_input_hashes_unchanged=True,failed_runs_retained=negative,new_source_queries=0,source_queries=0,source_engine_calls=0,verification_scope='hash/status/accounting consistency, not an independent proof of arbitrary-source expansion')
    with (F/'bundle_validation.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    assert time.process_time()-START<CAP-1
    print(result['status'],flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_proof169_exit.json').open('x') as f:json.dump(dict(whole_process_CPU_seconds=time.process_time(),error=error,source_queries=0,source_engine_calls=0),f)
