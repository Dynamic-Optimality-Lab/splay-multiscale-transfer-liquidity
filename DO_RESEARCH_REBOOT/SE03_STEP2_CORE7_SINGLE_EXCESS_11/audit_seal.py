"""Final C7 one-slot source/owner/scope/integrity seal, not full Step2."""
import hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
def read(n):return json.loads((B/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    pins=read('dependency_pins.json');bad=[]
    for v in pins['pins']:
        p=ROOT/v['path']
        if not p.is_file() or sha(p)!=v['sha256']:bad.append(v['path'])
    for v in pins['external_pins']:
        p=Path(v['path'])
        if not p.is_file() or sha(p)!=v['sha256']:bad.append(v['path'])
    assert not bad
    for phase in ('geometry','construction','construction2','independent','controls','ownership','blocked','stream'):
        v=read('run_'+phase+'_result.json');ex=read('audit_'+phase+'_exit.json')
        assert v['status']=='PASS' and not ex['error'] and v['termination'] is None
    g=read('geometry_certificate.json');ind=read('independent_audit.json');o=read('ownership_audit.json')
    assert g['raw_contexts']==429 and g['all_access_transitions']==3003
    assert g['Q3_sector_count']==132 and g['preceding_sector_incidences']==198
    assert sum(v['core_contexts'] for v in g['classes'])==1320
    assert sum(v['admitted_genuine_edges'] for v in g['classes'])==5784
    assert ind['status']=='PASS_COMPLETE_INDEPENDENT_C7_ONE_SLOT_COMPONENTS'
    assert ind['Q3_sectors']==132 and ind['preceding_sector_incidences']==198
    assert ind['one_hole_map_cases']==31104 and ind['tight_inventory_cases']==2304
    assert ind['period_cut_transports']==46 and ind['all_reflected_edges_checked']==3003
    assert o['cases']==696 and o['branches']=={'p_is_excess':464,'empty_residual':232}
    assert o['non_seed_terminal_donors']==30 and o['all_old_assignments_preserved']
    blocked=read('blocked_common_case.json')
    assert blocked['status']=='PASS_BLOCKED_OTHER_ROOT_WITH_COMMON_EXCESS_ANCHOR'
    assert blocked['Pstar']!=blocked['R'] and blocked['actual_anchor']==blocked['R']
    stream=read('source_stream_audit.json')
    assert stream['status']=='PASS_CAUSAL_INDEPENDENT_FULL_RECEIPT_AND_LEGAL_TRANSPORT'
    assert stream['universal_working_bound']==4 and all(r['max_working_units']<=4 for r in stream['reports'])
    ctrl=read('historical_controls.json')
    assert ctrl['status']=='PASS_ALL_REQUIRED_HISTORICAL_CONTROLS' and ctrl['exact_legacy_period_rows_replayed']==1856
    assert read('historical10_gamma_period_ownership_audit.json')['D12']==0
    assert read('historical10_gamma_period_ownership_audit.json')['D13']==2
    assert read('historical10normal_normalform_audit.json')['local_repair']=='REFUTED_EXACT'
    assert read('historical09_adversarial_audit.json')['reflected_paired_sectors']==62
    assert read('historical08_adversarial_audit.json')['four_leaf_frames']==720
    assert read('historical06_adversarial_audit.json')['complete_previous_packet_contexts']==144
    cert=read('single_slot_certificate.json')
    assert cert['status']=='C7_ONE_SLOT_SOURCE_FUNDING_PROVED'
    assert cert['allocator_sha256']==sha(B/'single_slot_allocator.py')
    assert cert['geometry_sha256']==sha(B/'geometry_certificate.json')
    assert cert['independent_audit_sha256']==sha(B/'independent_audit.json')
    assert cert['actual_receipts_sha256']==sha(B/'physical_receipts2.json')
    correction=read('construction_accounting_correction.json')
    assert correction['actual_source_calls']==102 and read('physical_receipts2.json')['source_engine_calls']==96
    assert read('completion_gates.json')['status']=='ALL_RELEVANT_K1_K14_PASS'
    assert all(v['status']=='PASS' for v in read('completion_gates.json')['gates'].values())
    needed=['SOURCE_SPEC.md','SOURCE_PROVENANCE.md','CORE7_ONE_SLOT_CLASSIFICATION.md','ANCHOR_INTERFACE.md',
        'AVAILABLE_BIT_INVENTORY.md','POSITIVE_SURPLUS_PROOF.md','ZERO_SURPLUS_RIGIDITY.md','ZERO_SURPLUS_DONOR.md',
        'NONLOCAL_DONOR_LEMMA.md','PHYSICAL_SINGLE_SLOT_INJECTION.md','CASE_LEDGER.md','INDEPENDENT_AUDIT.md',
        'ADVERSARIAL_AUDIT.md','UNIFORM_SINGLE_SLOT_INTERFACE.md','FULL_PROOF.md','FINAL_VERDICT.md','CHECKPOINT.md','IAGS_CLOSURE.md']
    assert all((B/n).is_file() for n in needed)
    proof=(B/'FULL_PROOF.md').read_text()
    assert '2H_- - Q_- >=1' in proof and 'h=h0 union{r->v}' in proof
    assert 'f\'=a union{p->u}' in proof and 'EVERY previous a value' in proof
    assert 'block/cyclic' in proof and 'not external review' in proof
    assert 'multi-slot' in proof and 'remain OPEN' in proof
    entry=read('entry.json')
    def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
    assert git('rev-parse','HEAD')==entry['head'] and git('branch','--show-current')==entry['branch']
    assert not git('status','--porcelain','--untracked-files=no')
    out('dependency_revalidation.json',{'status':'PASS','inherited_local_pins':len(pins['pins']),
        'external_pins':len(pins['external_pins']),'mismatches':bad})
    result={'status':'PASS_COMPLETE_C7_ONE_SLOT_FUNDING','terminal_outcome':'A','theorem':'C7_ONE_SLOT_FUNDING',
        'frozen_statement':'forall Pi in P7,1, Pstar={p} -> exists u in N_I(p), a union{p->u} complete with all previous values unchanged',
        'K1_K14':'ALL_PASS','Gate_A_to_J':'PASS_DECLARED_SOURCE_INTERFACE','U11':'PROVED_SINGLE_SLOT_COMPONENT','general_Gate_U':'U_OPEN',
        'source_positive_supply':'Q3 source is7-Score path; incoming path Q<=1 -> actual preceding own spare',
        'zero_surplus':'IMPOSSIBLE_UNIVERSAL_SOURCE','ownership':'ALL paid assignments fixed, not only common fE',
        'eligibility':'certified actual-counting-unit same-period block/cyclic stream and fixed-owner exchange; no new native policy',
        'actual_fE':'ALL supplied certified maps covered parametrically; no numerical fixture substituted',
        'one_period':'both IDs transported, no preperiod/extra copy spending','private_trees':'universal rigid-gap/source-ID proof',
        'old_pins_verified':len(pins['pins']),'branch':entry['branch'],'HEAD':entry['head'],'tracked_status':'',
        'R1_R4':'preserved','Bank25':25,'old_graph_solver_owners_and_semantics':'unchanged',
        'old_normalized_changing_chart_debt':'REFUTED unchanged','multi_slot':'OPEN_NOT_EXECUTED',
        'Step2':'OPEN','CD6_full_scope':'OPEN','Step3':'OPEN','Universal_CD':'OPEN','Dynamic_Optimality':'OPEN',
        'trust':'mathematical source proof with SAME-agent distinct implementation checks, no external/formal certification',
        'source_engine_calls':0,'new_finite_tests':0}
    out('seal_audit.json',result);print(json.dumps(result),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_seal_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0,'new_finite_tests':0})
