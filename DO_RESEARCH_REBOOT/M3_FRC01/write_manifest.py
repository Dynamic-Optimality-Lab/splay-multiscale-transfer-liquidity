"""Final preservation and provenance manifest for the authorized fringe compensation campaign."""
import json,hashlib,subprocess,os
from pathlib import Path
from datetime import datetime,timezone
BASE=Path('DO_RESEARCH_REBOOT/M3_FRC01');OUT=BASE/'manifest.json';ROOT=Path.cwd()
REPORT="DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/IAGS_WSIGN02A_ZERO_COST_IMPOSSIBILITY/IAGS_11G_S03_M3_FRC01_FRINGE_EXCEPTION_COMPENSATION.md"
IAGS=REPORT.rsplit('/',1)[0]+'/'
def physical(rel):
    p=str(ROOT/rel)
    return Path('\\\\?\\'+p) if os.name=='nt' else Path(p)
def fp(rel):
    b=physical(rel).read_bytes()
    return {'path':rel,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def git(*args):return subprocess.check_output(['git',*args],text=True).strip()
def main():
    assert not OUT.exists()
    old=json.loads((BASE/'entry_baseline.json').read_text())
    assert len(old)==95
    for row in old:assert fp(row['path'])['sha256']==row['sha256'],row['path']
    assert not git('diff','--name-only') and not git('diff','--cached','--name-only')
    head=git('rev-parse','HEAD');branch=git('branch','--show-current')
    assert head=='fea2a25b05e97f726b6e1891cebb12c4cfca821a' and branch=='coarse-double-branch'
    remote=git('ls-remote','--heads','origin','coarse-double-branch').split()
    assert remote==[head,'refs/heads/coarse-double-branch']
    paths=set(git('ls-files','--others','--exclude-standard').splitlines())
    new=paths-{r['path'] for r in old}
    assert all(p==REPORT or p.startswith(BASE.as_posix()+'/') for p in new),new
    assert not any('__pycache__' in p or p.endswith('.pyc') for p in new)
    c=json.loads((BASE/'compensation_certificate.json').read_text())
    audit=json.loads((BASE/'audit_results.json').read_text())
    controls=json.loads((BASE/'original_compensation_controls.json').read_text())
    assert c['status']==audit['status']==controls['status']=='COMPLETE'
    assert c['R']==[1917,1937,2141,2965] and c['all_retained_H2_fringe_rows_pass']
    assert all(r['new_reduced_weight']==0 for r in c['fixed_exceptions'])
    assert audit['maximum_neutral_delays_before_repayment']==1
    deps=[
      'DO_RESEARCH_REBOOT/RESEARCH_RULES.md',
      'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/11G_SOLVER_AND_ARCHITECTURE_FREEZE.json',
      'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/11G_RESOURCE_LEDGER.json',
      'python/independent/splay.py',
      'DO_RESEARCH_REBOOT/M2_SEP01/experiment.py',
      'DO_RESEARCH_REBOOT/M3_PHI01/verify_full_mixed.py',
      'DO_RESEARCH_REBOOT/M3_LDR01/negative_run_census.json',
      'DO_RESEARCH_REBOOT/M3_LDR01/census_replay.json',
      'DO_RESEARCH_REBOOT/M3_LDR01/core_rotation_certificate.json',
      'DO_RESEARCH_REBOOT/M3_CHR01/verify_original_controls.py',
      'DO_RESEARCH_REBOOT/M3_CHR01/graph_catalog.json',
      'DO_RESEARCH_REBOOT/M3_CHR01/potential.bin',
      'DO_RESEARCH_REBOOT/M3_CHR01/edge_audit.json',
      'DO_RESEARCH_REBOOT/M3_H2R01/terminal_potential.py',
      'DO_RESEARCH_REBOOT/M3_H2R01/original_fringe_controls.py',
      'DO_RESEARCH_REBOOT/M3_H2R01/original_fringe_controls.json',
      'DO_RESEARCH_REBOOT/M3_H2R01/terminal_floor_certificate.json',
      'DO_RESEARCH_REBOOT/M3_H2R01/fringe_kernel_certificate.json',
      'DO_RESEARCH_REBOOT/M3_H2R01/ten_node_rotation_certificate.json',
      'DO_RESEARCH_REBOOT/M3_H2R01/audit_results.json']
    pc='DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/'
    strict='DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/'
    deps += [pc+p for p in ('PC_B_CONTROLLER.py','PC_ROTATION_INTERPRETER.py','PC_TYPED_DAG.py',
          'PC_STRUCTURAL_WITNESS.py','PC_ATOM_INVENTORY.py','PC_CONCRETIZE.py','PC_LOW_COMPILER.py')]
    deps += [strict+p for p in ('STRICT_LOW_COMPILER.py','STRICT_B_CONTROLLER.py','STRICT_SOURCE_REPAIRS.py','STRICT_INVENTORY.py')]
    deps += ['DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE/STRICT_HIGH_COMPILER.py']
    deps += [IAGS+p for p in (
        'IAGS_WSIGN02C_QUANTITATIVE_TRANSFER.md','IAGS_WSIGN02D_UNIVERSAL_LOW_CREDIT_BOUND.md',
        'IAGS_11G_S03_M2_SEP01_SEPARATED_KEY8_REPAYMENT.md',
        'IAGS_11G_S03_M2_DSK01_DIRTY_SMALLER_KEY_SIGN.md',
        'IAGS_11G_S03_M3_PHI01_MIXED_HIGH_DEFICIT_EXCLUSION.md',
        'IAGS_11G_S03_M3_LDR01_LOW_DEFICIT_RUN_REPAYMENT.md',
        'IAGS_11G_S03_M3_CHR01_CHEAP_HELPER_CYCLE_CLOSURE.md',
        'IAGS_11G_S03_M3_H2R01_TERMINAL_DEBT_REPAYMENT.md')]
    files=[fp(p) for p in sorted(new) if p!=OUT.as_posix()]
    result={'campaign':'IAGS-11G-S03-M3-FRC01','completed_utc':datetime.now(timezone.utc).isoformat(),
      'status':'COMPLETE','outcome':'A, registered compensation theorem proved at stated chi8 scope',
      'branch':branch,'local_head':head,'remote_branch_ref':remote[1],'remote_branch_tip':remote[0],
      'tracked_tree_unchanged':True,'baseline_files_preserved':95,'new_paths_confined_to_authorized_scope':True,
      'no_bytecode_created':True,'SMT_solver_invoked':False,'backend_switched':False,'graph':'G_AF','bank25':25,
      'principal_theorem':{'status':'PROVED—RESTRICTED DOMAIN',
         'scope':'every original chi8 H=2 low edge, all masks/signatures/A witnesses/macros',
         'construction':'Qnew=Qbar-1 when sigma[0]>0 and core_id in R; Qnew=Qbar otherwise; midpoint correction zero',
         'R':[1917,1937,2141,2965],'new_range':[-2,0],'inequality':'Qnew(t)-Qnew(s)<=4-q',
         'all_prior_cap_valid_chi8_edge_inequalities_preserved':True},
      'repayment_theorem':{'status':'PROVED—RESTRICTED DOMAIN',
         'scope':'all occurrences of the three original +1 H=2 fringe patterns in chi8',
         'maximum_successors_to_repay':2,'maximum_neutral_H1_delay_edges':1,
         'unique_neutral_kernel':[2141,6,2965],
         'bound':'sum old reduced weights over helper, optional neutral delay and repayer >=0',
         'unpaid_exception_debt_at_end_of_finite_path_at_most':1},
      'mixed_walk_corollary':{'scope':'all original chi8 high/H2 edges plus prior cap-valid H1 edges or H1 from corrected basin',
          'finite_path_bound':'W>=Theta(last)-Theta(first)>=-2','full_closed_walk_bound':'W>=0',
          'is_full_M3_theorem':False},
      'fresh_evidence':{'R_access_queries':36,'original_B_replays':36,'H2_fringe_rows':16842,'Gamma0_rows':4224,
          'original_low_root_controls':7,'original_high_root_controls':1,'shared_state_compensation_blocks':4,
          'point_controls_are_closed_cycles':False,'DAG_nodes_low':1400081,'DAG_nodes_high':53455,
          'full_original_root_audit':True,'all_saved_ordinary_fields_and_shared_high_midpoint_checked':True,
          'CPU_seconds_finite':c['cpu_seconds'],'CPU_seconds_controls':controls['cpu_seconds'],
          'CPU_seconds_audit':audit['cpu_seconds']},
      'inherited_evidence':{'primitive_symbolic_cases':570,'rerun_this_campaign':False,'all_prior_files_hash_preserved':True},
      'ledger':{'M1':'OPEN','M2':'PROVED—UNIVERSAL (inherited)','M3':'OPEN','Step03':'OPEN','Step04':'UNAUTHORIZED',
          'restricted_CoarseDouble':'OPEN','DynamicOptimality':'OPEN','negative_mixed_cycles_certified':0},
      'files_excluding_this_manifest':files,'dependencies':[fp(p) for p in deps],'entry_baseline':old}
    with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2,ensure_ascii=False)
    saved=json.loads(OUT.read_text(encoding='utf-8'))
    for row in saved['files_excluding_this_manifest']+old:assert fp(row['path'])['sha256']==row['sha256']
    assert not git('diff','--name-only') and not git('diff','--cached','--name-only')
    print(json.dumps({'status':'COMPLETE','old_files_preserved':95,'new_artifacts_including_manifest':len(files)+1,
       'dependencies_hashed':len(deps),'manifest_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),
       'tracked_tree_unchanged':True,'remote_tip':head,'M3':'OPEN','all_chi8_H2_helpers':'PROVED',
       'maximum_successors_to_repay':2}),flush=True)
if __name__=='__main__':main()

