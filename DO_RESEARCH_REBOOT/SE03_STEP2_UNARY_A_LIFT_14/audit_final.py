"""Final new-theorem/dependency seal, no repeated semantic checks."""
import hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
def read(n):return json.loads((B/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
def main():
    expected='8c378d49283b3738b18e7175886772a98025e4e9'
    assert git('branch','--show-current')=='coarse-double-branch' and git('rev-parse','HEAD')==expected
    assert not git('status','--porcelain','--untracked-files=no')
    pins=read('dependency_pins.json')
    for p in pins['pins']:assert sha(ROOT/p['path'])==p['sha256'],p['path']
    for p in pins['external_pins']:assert sha(Path(p['path']))==p['sha256'],p['path']
    unary=read('unary_seal.json');assert unary['status']=='PROVED_UNIVERSAL_NAMED_UNARY_SOURCE_DOMAIN'
    for p in unary['files']:assert sha(B/p['path'])==p['sha256'],p['path']
    for phase in ('branch_grammar2','branch9_2','branch_independent2','branch_all','branch_tables','branch_owners'):
        assert read('run_'+phase+'_result.json')['status']=='PASS'
    a=read('branch_all_independent_audit.json');assert a['status'].startswith('PASS_ALL_38')
    receipts=a['receipts'];assert len(receipts)==38
    direct=[r for r in receipts if r['status']=='PASS_ALL_SOURCE_SIGNED_CONSTRAINTS']
    mirrors=[r for r in receipts if r['status']=='PROVED_BY_ORDER_REVERSAL']
    assert len(direct)==23 and len(mirrors)==15
    counts={};maxima={};stats={}
    for k in (9,10,11):
        rr=[r for r in receipts if r['core']==k];dd=[r for r in direct if r['core']==k]
        counts[k]=len(rr);maxima[k]=max(r['max_debt'] for r in dd)
        stats[k]={'masks':len(rr),'direct':len(dd),'mirrors':len(rr)-len(dd),
            'direct_synchronized_states':sum(r['synchronized_states'] for r in dd),
            'LOW_inequalities':sum(sum(r['LOW_rows'].values()) for r in dd),
            'HIGH_hyperedges':sum(r['HIGH_hyperedges'] for r in dd),'max_debt':maxima[k]}
    assert counts=={9:21,10:16,11:1} and maxima=={9:2,10:3,11:3}
    assert next(r for r in direct if r['core']==11)['q5_q1_sectors']==62
    for r in direct:
        assert sha(B/r['file'])==r['sha256'] and read('audit_'+r['file'])==r
        assert r['synchronized_states']<2000000 and r['working_bank_bound']<=11
    owners=read('branch_physical_owner_audit.json')
    assert owners['status']=='PASS_ACTUAL_PHYSICAL_FUNDING_AND_FROZEN_OWNER_INTERFACE'
    assert len(owners['reports'])==36 and owners['all_existing_allocations_preserved']
    assert owners['working_bound']==11 and owners['Bank25']==25 and owners['old_semantic_rows_replayed']==0
    assert {(r['core'],r['reflected']) for r in owners['reports']}=={(k,m) for k in (9,10,11) for m in (False,True)}
    assert all(r['all_old_natural_values_fixed'] and r['working_units']<=11 for r in owners['reports'])
    # The first failed outer tuple/list comparison is retained, not promoted.
    assert read('run_branch_independent_result.json')['status']=='FAILED_OR_UNKNOWN'
    names=['FULL_PROOF.md','SOURCE_SPEC.md','CASE_LEDGER.md','INDEPENDENT_AUDIT.md','CHECKPOINT.md','FINAL_VERDICT.md',
        'BRANCH_QUOTIENT_BOX.md','branch_frames2.py','branch_grammar2.json','branch_independent_audit2.json',
        'audit_branch_independent2.py','branch_all.py','audit_branch_all.py','branch_all_construction.json',
        'audit_branch_tables.py','branch_all_independent_audit.json','branch_funding.py','audit_branch_owners.py',
        'branch_physical_owner_audit.json','unary_seal.json']
    names+= [r['file'] for r in direct]+['audit_'+r['file'] for r in direct]
    out('funding_seal.json',{'status':'PROVED_SOURCE_UNIFORM_CORE9_10_11_PHYSICAL_FUNDING','branch':git('branch','--show-current'),'HEAD':expected,
        'tracked_tree':'CLEAN','inherited_local_pins_revalidated':len(pins['pins']),'external_pins_revalidated':len(pins['external_pins']),
        'unary_lift':'SEPARATELY_PROVED_ZERO_CORRECTION','all_private_and_unary_populations':'ARBITRARY_BY_SOURCE_LIFT',
        'stats':stats,'boundary_bank':3,'working_bank':11,'Bank25':25,'frozen_owners':'PRESERVED_PARAMETRICALLY_FOR_ORIGINAL_CERTIFIED_fE_AND_a',
        'trust':'computer-assisted complete symbolic source quotient; distinct immutable implementation, same agent; no external/formal certification',
        'new_finite_tests':0,'Step2_final_assembly':'OPEN','CD6_final_assembly':'OPEN','Step3':'OPEN','Universal_CD':'OPEN','Dynamic_Optimality':'OPEN',
        'files':[{'path':n,'sha256':sha(B/n)} for n in names]})
    print(json.dumps({'status':'CORE9_10_11_FUNDING_SEALED','stats':stats,'working_bank':11,'pins':len(pins['pins'])}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_final_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0,'old_semantic_rows_replayed':0})
