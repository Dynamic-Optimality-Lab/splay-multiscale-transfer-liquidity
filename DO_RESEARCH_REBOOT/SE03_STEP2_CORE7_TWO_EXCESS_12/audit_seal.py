"""Final scope/dependency/receipt integrity, not a formal proof checker.
No source experiments repeated after the accepted independent phases.
"""
import hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
def read(n):return json.loads((B/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def unpack(v):return {tuple(x['demand']):tuple(x['unit']) for x in v}
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
def main():
    entry=read('entry.json');pins=read('dependency_pins.json')
    assert git('branch','--show-current')==entry['branch'] and git('rev-parse','HEAD')==entry['head']
    assert not git('status','--porcelain','--untracked-files=no')
    for v in pins['pins']:assert sha(ROOT/v['path'])==v['sha256'],v['path']
    for v in pins['external_pins']:assert sha(Path(v['path']))==v['sha256'],v['path']
    oldlines=set(entry['worktree_status'].splitlines());newlines=set(git('status','--porcelain','--untracked-files=all').splitlines())
    assert oldlines<=newlines
    assert all(line.startswith('?? DO_RESEARCH_REBOOT/SE03_STEP2_CORE7_TWO_EXCESS_12/') for line in newlines-oldlines)
    assert not list(B.rglob('__pycache__'))
    required=['SOURCE_SPEC','CORE7_TWO_SLOT_CLASSIFICATION','TWO_ANCHOR_PROVENANCE','PHYSICAL_BIT_INVENTORY',
        'CAMPAIGN11_TRANSFER_AUDIT','DONOR_COLLISION_LEDGER','SECOND_DONOR_THEOREM','ZERO_SURPLUS_TWO_SLOT',
        'TWO_DEMAND_EXCHANGE','PERIOD_CUT_VALIDITY','SOURCE_LIFTING','CASE_LEDGER','INDEPENDENT_AUDIT',
        'ADVERSARIAL_AUDIT','UNIFORM_TWO_SLOT_INTERFACE','FULL_PROOF','FINAL_VERDICT','CHECKPOINT',
        'SOURCE_PROVENANCE','IAGS_BOX','IAGS_CLOSURE']
    assert all((B/(n+'.md')).is_file() for n in required)
    for s in ('two_slot_allocator.py','audit_geometry.py','audit_construction2.py','audit_independent3.py',
            'audit_ownership.py','audit_controls.py','audit_seal.py','publish_metadata.py'):
        compile((B/s).read_text(),s,'exec')
    accepted=('geometry','construction2','independent3','ownership','controls')
    for ph in accepted:
        assert read('run_'+ph+'_result.json')['status']=='PASS'
        assert not read('audit_'+ph+'_exit.json')['error']
    failed=('construction','independent','independent2')
    for ph in failed:assert read('run_'+ph+'_result.json')['status']=='FAILED_OR_UNKNOWN'
    cert=read('two_slot_certificate.json')
    for field,name in [('full_proof_sha256','FULL_PROOF.md'),('independent_audit_sha256','independent_audit.json'),
            ('ownership_audit_sha256','ownership_audit.json'),('source_receipts_sha256','physical_receipts2.json'),
            ('allocator_sha256','two_slot_allocator.py')]:assert cert[field]==sha(B/name)
    ind=read('independent_audit.json');own=read('ownership_audit.json');old=read('historical_controls.json');src=read('physical_receipts2.json')
    assert ind['seven_Score_trees']==429 and ind['source_access_edges']==3003
    assert ind['critical_sectors']==132 and ind['predecessor_incidences']==198
    assert ind['actual_source_owner_fixtures']==432 and ind['actual_period_cut_transports']==2904
    assert ind['generic_owner_cases']==62208 and own['cases']==365976
    assert own['blocked_anchor_counts']['2']==1440 and own['seed_bits_already_owned']['2']==113616
    assert own['all_old_assignments_identical'] and own['all_old_successful_paths_identical']
    assert own['simultaneous_equals_original_common_full_exchange'] and own['sequential_second_endpoint_unchanged']
    assert old['exact_legacy_period_rows_replayed']==1856 and old['all_outputs_redirected_to12']
    gamma=read('historical10_gamma_period_ownership_audit.json')
    assert [gamma[k] for k in ('A','QF','QE','D12','D13')]==[34,30,24,0,2]
    assert gamma['units']==[[10,3,0],[10,3,1]] and gamma['full_demands']==[[9,1],[13,5]]
    assert 12 not in gamma['actual_maximum_cut_candidates_not_splitting_blocks']
    joint=read('joint_donor_certificate.json');assert len(joint['receipts'])==432
    inventory_count=0
    for fam in src['families']:
        rows=fam['rows'];U={(r['occurrence'],j,b) for r in rows for j in range(1,r['a']+1) for b in (0,1)}
        D={(r['occurrence'],k) for r in rows for k in range(1,r['qF']+1)};R=set(map(tuple,fam['R']))
        h0=unpack(fam['h0']);h=unpack(fam['independent_h']);seeds=fam['seed_receipts'];mm=fam['macros']
        assert len(R)==2 and set(h0)==D-R and set(h)==D
        assert len(set(h.values()))==len(h) and set(h.values())<=U
        assert len({v['predecessor_macro'] for v in seeds})==2 and len({tuple(v['seed_bit']) for v in seeds})==2
        for v in seeds:
            r,u=tuple(v['anchor_slot']),tuple(v['seed_bit']);pre=mm[v['predecessor_macro']]
            assert h[r]==u and r in R and u not in set(h0.values())
            assert pre['Q']<=1 and pre['H']>=1 and u==tuple(pre['units'][pre['Q']])
        assert fam['positive_surplus']>=2 and fam['alignment']['slot_count_before_division']==2
        for f in fam['fixtures']:
            a=unpack(f['paid']);add=unpack(f['additions']);ans=unpack(f['final']);alpha=unpack(f['anchors'])
            assert set(add)==D-set(a) and set(add.values())<=U-set(a.values())
            assert len(set(add.values()))==len(add) and ans=={**a,**add}
            assert set(ans)==D and len(set(ans.values()))==len(ans)
            assert set(alpha)==set(add) and set(alpha.values())<=R and len(set(alpha.values()))==len(alpha)
            inventory_count+=1
    assert inventory_count==432
    gates=read('completion_gates.json')
    assert set(gates['gates'])=={'L'+str(i) for i in range(1,17)}
    assert all(v['status']=='PASS' for v in gates['gates'].values()) and gates['Gate_U12']=='U-B'
    status=read('research_status_ledger.json')
    assert all(status[k]=='OPEN' for k in ('Step2','CD6','Step3','Universal_CD','Dynamic_Optimality'))
    assert status['unrestricted_core7']=='OPEN_NOT_EXECUTED' and status['Campaign13']=='NEXT_NOT_EXECUTED'
    proof=(B/'FULL_PROOF.md').read_text();assert 'ACTUAL immediately preceding genuine' in proof
    assert 'EVERY previous value' in proof and 'ORIGINAL common demands C' in proof
    assert 'variants102' in (B/'INDEPENDENT_AUDIT.md').read_text()
    # CPU/query records are charged INCLUDING failed drafts; leave controller
    # and this seal to the ordinary post-run final resource publication.
    total=entry['prior_uniform_CPU'];groups=dict(entry['inherited_group_CPU']);queries=0
    for p in B.glob('run_*_result.json'):
        r=json.loads(p.read_text());c=read('controller_'+r['phase']+'_exit.json')
        charge=r['child_CPU']+c['whole_process_CPU_seconds'];total+=charge;groups[r['group']]+=charge
        assert r['source_engine_calls']<2000000;queries+=r['source_engine_calls']
    assert queries==66285 and total+time.process_time()<7195
    assert all(groups[g]+(time.process_time() if g=='independent' else 0)<entry['group_caps'][g] for g in groups)
    out('dependency_revalidation.json',{'status':'ALL_FROZEN_BYTES_AND_OLD_WORKTREE_PRESERVED',
        'pins':len(pins['pins']),'external_directives':len(pins['external_pins']),
        'branch':entry['branch'],'HEAD':entry['head'],'tracked_status':'','new_paths_only':'Campaign12',
        'all_old_untracked_paths_still_present':True})
    out('seal_audit.json',{'status':'PASS_FINAL_SOURCE_OWNERSHIP_SCOPE_INTEGRITY','terminal_outcome':'A',
        'theorem':'C7_TWO_SLOT_FUNDING','Gate_U12':'U-B','dependencies_verified':len(pins['pins']),
        'source_reports':len(src['families']),'joint_source_owner_receipts':inventory_count,
        'authoritative_phases':accepted,'superseded_failed_phases_fully_charged':failed,
        'old_research_unchanged':True,'L1_L16':'PASS_DECLARED_MATHEMATICAL_PROOF_INTERFACE',
        'source_engine_calls_before_seal':queries,'CPU_before_current_seal':total,
        'Step2':'OPEN','CD6':'OPEN','Step3':'OPEN','Campaign13':'NEXT_NOT_EXECUTED',
        'trust':'source mathematical proof plus distinct implementation audit by same agent; this seal is integrity/scope validation, not a formal proof kernel'})
    print(json.dumps({'status':'SEALED_OUTCOME_A','pins':len(pins['pins']),'joint_receipts':inventory_count,'source_calls_all_runs':queries}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_seal_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0,'new_finite_tests':0})
