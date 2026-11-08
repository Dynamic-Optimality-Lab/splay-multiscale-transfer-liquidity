"""Final read-only provenance and preservation audit for the one-gap cheap-helper campaign."""
import json,hashlib,subprocess,os
from pathlib import Path
from datetime import datetime,timezone
BASE=Path('DO_RESEARCH_REBOOT/M3_H1F01');OUT=BASE/'manifest.json';ROOT=Path.cwd()
REPORT="DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/IAGS_WSIGN02A_ZERO_COST_IMPOSSIBILITY/IAGS_11G_S03_M3_H1F01_ONE_GAP_CHEAP_HELPERS.md"
IAGS=REPORT.rsplit('/',1)[0]+'/'
def native(rel):
    s=str(ROOT/rel)
    return Path('\\\\?\\'+s) if os.name=='nt' else Path(s)
def fp(rel):
    b=native(rel).read_bytes()
    return {'path':rel,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def git(*args):return subprocess.check_output(['git',*args],text=True).strip()
def main():
    assert not OUT.exists()
    baseline=json.loads((BASE/'entry_baseline.json').read_text());assert len(baseline)==106
    for r in baseline:assert fp(r['path'])['sha256']==r['sha256'],r['path']
    assert not git('diff','--name-only') and not git('diff','--cached','--name-only')
    branch=git('branch','--show-current');head=git('rev-parse','HEAD')
    assert branch=='coarse-double-branch' and head=='fea2a25b05e97f726b6e1891cebb12c4cfca821a'
    remote=git('ls-remote','--heads','origin','coarse-double-branch').split()
    assert remote==[head,'refs/heads/coarse-double-branch']
    untracked=set(git('ls-files','--others','--exclude-standard').splitlines())
    new=untracked-{r['path'] for r in baseline}
    assert all(p==REPORT or p.startswith(BASE.as_posix()+'/') for p in new),new
    assert not any('__pycache__' in p or p.endswith('.pyc') for p in new)
    c=json.loads((BASE/'graph_catalog.json').read_text());ea=json.loads((BASE/'edge_audit.json').read_text())
    oa=json.loads((BASE/'original_audit.json').read_text());sol=json.loads((BASE/'completion_result.json').read_text())
    assert ea['status']=='FINITE_EXACT_VERIFIED' and oa['status']=='COMPLETE'
    assert sol['status']=='COMPLETED_LABELS_UNAUDITED' # now independently verified by edge_audit, retained as historical output
    assert c['nodes']==342796 and c['edges']==ea['edges_regenerated_and_checked']==1915587
    assert ea['potential_range']==[-2,0] and ea['minimum_new_residual']==0
    repaired=sum(r['edges'] for r in ea['cheap_old_failures_repaired']);assert repaired==24799
    assert oa['total_roots_replayed']==16 and oa['closed_mixed_cycle_weight']==4
    deps=[
      'DO_RESEARCH_REBOOT/RESEARCH_RULES.md','python/independent/splay.py',
      'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/11G_SOLVER_AND_ARCHITECTURE_FREEZE.json',
      'DO_RESEARCH_REBOOT/M3_LDR01/negative_run_census.json',
      'DO_RESEARCH_REBOOT/M3_LDR01/core_rotation_certificate.json',
      'DO_RESEARCH_REBOOT/M3_LDR01/census_replay.json',
      'DO_RESEARCH_REBOOT/M3_CHR01/graph_catalog.json',
      'DO_RESEARCH_REBOOT/M3_CHR01/potential.bin',
      'DO_RESEARCH_REBOOT/M3_CHR01/fragment_graph.py',
      'DO_RESEARCH_REBOOT/M3_CHR01/verify_original_controls.py',
      'DO_RESEARCH_REBOOT/M3_PHI01/verify_full_mixed.py',
      'DO_RESEARCH_REBOOT/M3_PHI01/full_mixed_controls.json',
      'DO_RESEARCH_REBOOT/M3_H2R01/terminal_potential.py',
      'DO_RESEARCH_REBOOT/M3_H2R01/fringe_kernel.py',
      'DO_RESEARCH_REBOOT/M3_H2R01/fringe_kernel_certificate.json',
      'DO_RESEARCH_REBOOT/M3_H2R01/ten_node_rotation_certificate.json',
      'DO_RESEARCH_REBOOT/M3_H2R01/terminal_floor_certificate.json',
      'DO_RESEARCH_REBOOT/M3_FRC01/compensated_potential.py',
      'DO_RESEARCH_REBOOT/M3_FRC01/compensation_certificate.json',
      'DO_RESEARCH_REBOOT/M3_FRC01/verify_original_compensation.py',
      'DO_RESEARCH_REBOOT/M3_FRC01/audit_results.json']
    pc='DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/'
    st='DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/'
    deps += [pc+p for p in ('PC_B_CONTROLLER.py','PC_ROTATION_INTERPRETER.py','PC_TYPED_DAG.py',
         'PC_STRUCTURAL_WITNESS.py','PC_ATOM_INVENTORY.py','PC_CONCRETIZE.py','PC_LOW_COMPILER.py')]
    deps += [st+p for p in ('STRICT_LOW_COMPILER.py','STRICT_B_CONTROLLER.py','STRICT_SOURCE_REPAIRS.py','STRICT_INVENTORY.py')]
    deps += ['DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE/STRICT_HIGH_COMPILER.py']
    deps += [IAGS+p for p in ('IAGS_WSIGN02C_QUANTITATIVE_TRANSFER.md','IAGS_WSIGN02D_UNIVERSAL_LOW_CREDIT_BOUND.md',
        'IAGS_11G_S03_M2_SEP01_SEPARATED_KEY8_REPAYMENT.md','IAGS_11G_S03_M2_DSK01_DIRTY_SMALLER_KEY_SIGN.md',
        'IAGS_11G_S03_M3_PHI01_MIXED_HIGH_DEFICIT_EXCLUSION.md','IAGS_11G_S03_M3_LDR01_LOW_DEFICIT_RUN_REPAYMENT.md',
        'IAGS_11G_S03_M3_CHR01_CHEAP_HELPER_CYCLE_CLOSURE.md','IAGS_11G_S03_M3_H2R01_TERMINAL_DEBT_REPAYMENT.md',
        'IAGS_11G_S03_M3_FRC01_FRINGE_EXCEPTION_COMPENSATION.md')]
    files=[fp(p) for p in sorted(new) if p!=OUT.as_posix()]
    result={'campaign':'IAGS-11G-S03-M3-H1F01','completed_utc':datetime.now(timezone.utc).isoformat(),
      'status':'COMPLETE','outcome':'A at registered restricted one-gap physical joint scope',
      'branch':branch,'local_head':head,'remote_branch_ref':remote[1],'remote_branch_tip':remote[0],
      'tracked_tree_unchanged':True,'baseline_files_preserved':106,'new_paths_confined_to_authorized_scope':True,
      'no_bytecode_created':True,'SMT_solver_invoked':False,'backend_switched':False,'graph':'G_AF','bank25':25,
      'theorem':{'status':'PROVED—RESTRICTED DOMAIN','mu':341,'sigma':[1]+[0]*9,'region':'chi8',
         'A_scope':'all physical ten-key trees with canonical depth-six prefixes and exact canonical physical alpha7 endpoints',
         'H1_scope':'physical H1 accesses and full macros by inherited unit-charge fusion',
         'H2_scope':'Gamma0 arbitrary original witnesses by floor; Gamma1 physical canonical-prefix two-change macros by two-KEEP normalization',
         'high_scope':'all original chi8 OM/MO legs, same midpoint, via range',
         'path_bound':'W>=Theta(last)-Theta(first)>=-2','full_closed_walk_bound':'W>=0',
         'all_masks_or_signatures':False,'coarser_port_alpha_boundaries_covered':False,
         'global_replacement_for_FRC01':False},
      'certificate':{'status':'FINITE-EXACT VERIFIED','ordinary_states':342796,'low_edges':1915587,
         'physical_A_trees':16796,'physical_A_shadows':1188,'old_cheap_H1_failures_repaired':24799,
         'old_projected_cheap_failures_all_targets':762,'changed_states':7439,'table_range':[-2,0],
         'potential_below_corrected_and_negative_psi':True,'minimum_reduced_weight':0,
         'potential_sha256':ea['potential_sha256'],'all_CSR_edges_independently_regenerated':True,
         'original_root_controls':16,'original_low_roots':14,'original_high_roots':2,
         'closed_mixed_control_weight':4,'hidden_fringe_port_control':True,
         'noncanonical_high_abstract_shadow_control':True},
      'ledger':{'M1':'OPEN','M2':'PROVED—UNIVERSAL (inherited)','M3':'OPEN','Step03':'OPEN','Step04':'UNAUTHORIZED',
         'restricted_CoarseDouble':'OPEN','DynamicOptimality':'OPEN','negative_mixed_cycles_certified':0},
      'resources':{'state_cap':2000000,'edge_cap':5000000,'source_case_query_bound_plus_small_controls':727532+32,
         'completion_internal_edge_scans':sol['edge_scans'],'final_edge_inequalities':1915587,
         'source_files_modified':0,'all_phase_CPU_caps_passed':True},
      'files_excluding_this_manifest':files,'dependencies':[fp(p) for p in deps],'entry_baseline':baseline}
    with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2,ensure_ascii=False)
    saved=json.loads(OUT.read_text(encoding='utf-8'))
    for r in saved['files_excluding_this_manifest']+baseline:assert fp(r['path'])['sha256']==r['sha256']
    assert not git('diff','--name-only') and not git('diff','--cached','--name-only')
    print(json.dumps({'status':'COMPLETE','old_files_preserved':106,'new_artifacts_including_manifest':len(files)+1,
        'dependencies_hashed':len(deps),'manifest_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),
        'tracked_tree_unchanged':True,'remote_tip':head,'M3':'OPEN','repaired_joint_edges':24799,
        'sector_mu':341,'sector_sigma':[1]+[0]*9}),flush=True)
if __name__=='__main__':main()

