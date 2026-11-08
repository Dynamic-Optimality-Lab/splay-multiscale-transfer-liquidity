"""Independent certificate/status integration audit; zero source transition calls."""
import hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;C=F.parent;P=C.parent
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def main():
    reg=read(F/'proof_boxes_v3.json');dep=read(F/'dependency_manifest.json')
    assert sha(B/'run_phase_1440.py')==dep['controller_sha256']=='f630e39f4fac093f3ab62cf6458dacbda7d17ac4e8e83be83c215a212e1cb40f'
    for v in dep['inherited']:assert sha(Path(v['path']))==v['sha256']
    old=read(C/'CONTINUATION_01/campaign_manifest.json')
    for n,h in old['artifacts'].items():assert sha(C/'CONTINUATION_01'/n)==h
    audit=read(F/'independent_symbolic_audit.json')
    for n,h in audit['input_sha256'].items():assert sha(F/n)==h
    required='UCF35_ROOT_THEOREM PREVIOUS_SI34_REFUTATION_INHERITANCE EXACT_GATE_U14_PARENT_CONTRACT SOURCE_DOMAIN_AND_OWNER_INPUTS COMPLETE_ORIGINAL_FUNDING_FEASIBILITY SOURCE_COMPLETE_DONOR_ELIGIBILITY GLOBAL_FULL_H_AND_FROZEN_EXCHANGE MINIMAL_COMPLETE_FUNDING_OBSTRUCTION COMPLETE_FEASIBILITY_DUAL_THEOREM IAGS_R2_SPEC RECURSIVE_PROOF_DEBT_LEDGER ACTIVE_PROOF_BOX WELL_FOUNDED_DECOMPOSITION PROOF_DEPENDENCY_GRAPH UPWARD_RECONSTRUCTION GLOBAL_DONOR_NONCOLLISION SMALLER_CORE_SOURCE_BRIDGE ARBITRARY_SUPPORT_SOURCE_PROOF BANK25_GLOBAL_CONSTRUCTION E_R2_E_R3_COMPLETION SI34_COUNTEREXAMPLE_REPAIR_AUDIT HISTORICAL_SOURCE_CONTROLS GLOBAL_FROZEN_EXTENSION_REFUTATION_TEST UCF35_PROOF_OR_REFUTATION GATE_U14_RECONSTRUCTION_STATUS FINAL_VERDICT CHECKPOINT'.split()
    for n in required:assert (F/(n+'.md')).is_file()
    nodes={b['id']:b for b in reg['boxes']}
    assert nodes['UCF35']['status']=='OPEN_MATHEMATICAL_BLOCKER'
    assert nodes['SRC35']['status']==nodes['COMPAT35']['status']=='OPEN'
    assert nodes['OTHER_SIMPLE35']['status']=='OPEN'
    assert reg['prior_root_SI34']=='REFUTED_IMMUTABLE' and not reg['A_UCF35'] and not reg['E_UCF35']
    assert not reg['all_original_license_countercut'] and not (F/'FULL_PROOF.md').exists()
    # Independently check the status DAG; proved reductions aren't mistaken for conclusions.
    def visit(id,path):
        assert id not in path
        b=nodes[id];assert (F/b['artifact']).exists()
        for ch in b['required_children']:visit(ch,path|{id})
    for id in nodes:visit(id,set())
    assert nodes['SC35']['reduction_measure'].startswith('each child macro count strictly below parent')
    assert 'no valid further closed-source descent' in nodes['OTHER_SIMPLE35']['reduction_measure']
    phases=['proof174','proof175','verify90','proof176']
    rr=[read(B/('run_'+n+'_result.json')) for n in phases]
    assert rr[0]['status']=='FAILED_OR_UNKNOWN' and all(z['status']=='PASS' for z in rr[1:])
    assert sum(z['source_queries'] for z in rr)==0
    base=read(C/'CONTINUATION_01/resources_checkpoint.json')
    assert base['source_queries']==2999999 and base['source_query_cap']==3000000
    report={'status':'PASS_WITH_SCOPE_LIMITS','source_queries':0,'source_engine_calls':0,
      'checks':['original controller and immutable dependencies','full previous SI34 manifest',
        'new symbolic audit input hashes','required artifacts','acyclic box graph and exact open parents',
        'actual strict-descending SC interface recorded','no invented all-license refutation',
        'failed producer phase retained','no source query consumption'],
      'SC35_review':'same-agent mathematical review of complete-state excision, edge partition, natural h0 and two-endpoint lifting; not a formal proof checker',
      'mechanical_SC35_scope':'DAG, hypotheses, dependency and open-leaf consistency only',
      'all_source_geometric_theorem_independently_certified':False,
      'SC35_further_independent_universal_audit':'PENDING; no source-simple credit theorem claimed',
      'external_peer_review':False,'proof_assistant_verification':False,
      'input_sha256':{str(p.relative_to(F)):sha(p) for p in sorted(F.glob('*.md'))},
      'registry_sha256':sha(F/'proof_boxes_v3.json'),'dependency_manifest_sha256':sha(F/'dependency_manifest.json')}
    with (F/'independent_integration_audit.json').open('x',encoding='utf-8') as f:json.dump(report,f,indent=2)
    print('INTEGRATION_PASS; SOURCE_SIMPLE_AND_COMPATIBILITY_CHILDREN_STILL_OPEN',flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_verify91_exit.json').open('x',encoding='utf-8') as f:
            json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
