"""Final exact-source provenance and all-gate P1Z assembly seal."""
import hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
def read(n):return json.loads((B/n).read_text())
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    pins=read('dependency_pins.json');bad=[]
    for p in pins['pins']:
        q=ROOT/p['path']
        if not q.is_file() or sha(q)!=p['sha256']:bad.append(p['path'])
    for p in pins['external_pins']:
        q=Path(p['path'])
        if not q.is_file() or sha(q)!=p['sha256']:bad.append(p['path'])
    assert not bad
    zero=read('final_zero_inverse.json');seeds=read('terminal_seeds.json');closure=read('zero_closure.json')
    sep=read('separator.json');ind=read('independent_audit.json');adv=read('adversarial_audit.json');ctrl=read('source_control_replay.json')
    assert zero['sector_count']==48 and zero['H2Q3_composable_sector_count']==0
    assert seeds['status']=='COMPLETE_NEW_P1Z_TERMINAL_SEED_GRAMMAR' and len(seeds['terminal_cases'])==64
    assert closure['closed'] and not closure['goal'] and closure['bound'] is None and not closure['queue']
    assert len(closure['records'])==9624 and closure['statistics']['predecessor_proposals']==5872
    assert sep['status']=='ROOT_DEGREE_SEPARATES_NEG2' and not sep['four_leaf_NEG2_root_degree_candidates']
    assert ind['status']=='PASS_COMPLETE_INDEPENDENT_P1Z_RETURN_CERTIFICATE'
    assert ind['zero_predecessor_incidences']==5872 and ind['four_leaf_frames']==720 and ind['P1B_composable_sectors']==0
    assert ind['two_way_combined_seed_language_incidences']==6936 and ind['final_zero_two_way_language_incidences']==3936
    assert adv['status']=='PASS_ADVERSARIAL_P1Z_SOURCE_INTERFACES' and adv['reflected_frames_covered']==9624
    assert ctrl['status']=='PASS_ALL_MANDATORY_CONTROLS_AND_NEW_NORMAL_FORMS' and len(ctrl['families'])==18
    assert ctrl['old_semantic_rows_replayed']==1234
    for phase in ('seeds','closure','separator','independent','adversarial','controls'):assert read('run_'+phase+'_result.json')['status']=='PASS'
    needed=['SOURCE_SPEC.md','FINAL_ZERO_INVERSE.md','H1Q1_PLUS_ONE_INVERSE.md','H2Q3_PLUS_ONE_INVERSE.md',
        'TERMINAL_SEEDS.md','BACKWARD_ZERO_LANGUAGE.md','NEG2_SEPARATION.md','SOURCE_PROVENANCE.md',
        'CASE_LEDGER.md','FULL_PROOF.md','INDEPENDENT_AUDIT.md','SOURCE_REPLAY.md','FINAL_VERDICT.md','CHECKPOINT.md','IAGS_CLOSURE.md']
    assert all((B/f).is_file() for f in needed)
    proof=(B/'FULL_PROOF.md').read_text();assert 'Pre+1(Pre0_final(F11_q4)) subset gamma(L0)' in proof
    assert 'Pre0(gamma(L)) subset gamma(L)' in proof and 'T11^-2 intersect gamma(L) = empty' in proof
    assert 'INCLUDING720 four-leaf frames' in proof and 'H2/Q3' in proof
    entry=read('entry.json')
    def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
    assert git('branch','--show-current')==entry['branch'] and git('rev-parse','HEAD')==entry['head']
    assert not git('status','--porcelain','--untracked-files=no')
    out('dependency_revalidation.json',{'status':'PASS','inherited_local_pins':len(pins['pins']),
        'external_pins':len(pins['external_pins']),'mismatches':bad})
    result={'status':'PASS_COMPLETE_P1Z_RETURN_ASSEMBLY','terminal_outcome':'A','theorem':'P1Z-RETURN',
        'frozen_statement':'T11^-2 intersect Pre0*(Pre+1(Pre0_final(F11_q4))) = empty',
        'gates_A_to_K':{k:'PASS' for k in 'ABCDEFGHIJK'},'assembly_K1_to_K12':{str(k):'PASS' for k in range(1,13)},
        'H1Q1':'new complete g,v,y,x source seeds','H2Q3':'all actual two-event arrangements source-excluded by marked degree',
        'final_zero':'actual neutral H1Q2 source J2/K2','arbitrary_zero_prefix':'complete backward closure/induction',
        'source_separator':'actual cold NEG2 shapes(4,4)/(4,1); every represented L4 has degree2',
        'four_leaf_frames_retained':720,'private_BSTs_and_both_orientations':'covered by complete symbolic lifting',
        'independent_implementation':'distinct immutable engine and inverse/forward semantic coverage',
        'full_source_operations_and_charts':'preserved; one-way necessary projection only, no realization/splice claim',
        'physical_ownership':'no donor assigned or old owner changed','R1_R4':'preserved','Bank25':25,
        'old06_and07_proofs':'unchanged, sealed scopes preserved','old_chart_normalization':'REFUTED unchanged',
        'historical_controls':'18 cases/1234 period rows, all actual A/BF/BE/recent/chart boundaries verified',
        'branch':entry['branch'],'HEAD':entry['head'],'tracked_status':'','pins_verified':len(pins['pins']),
        'trust':'same-agent computer-assisted independent recomputation; no external or formal certification',
        'Step2':'OPEN','CD6':'OPEN','Step3':'OPEN','Universal_CD':'OPEN','Dynamic_Optimality':'OPEN',
        'source_engine_calls':0,'old_semantic_rows_replayed':0,'new_finite_tests':0}
    out('seal_audit.json',result);print(json.dumps(result),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_seal_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,
        'source_engine_calls':0,'old_semantic_rows_replayed':0,'new_finite_tests':0})
