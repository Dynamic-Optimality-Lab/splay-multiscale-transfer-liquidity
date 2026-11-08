"""Final integrity manifest: no source or prior research may have changed."""
import json,hashlib,subprocess,sys,os
from pathlib import Path
from datetime import datetime,timezone
BASE=Path('DO_RESEARCH_REBOOT/M3_H2R01');OUT=BASE/'manifest.json';ROOT=Path.cwd()
REPORT="DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/IAGS_WSIGN02A_ZERO_COST_IMPOSSIBILITY/IAGS_11G_S03_M3_H2R01_TERMINAL_DEBT_REPAYMENT.md"
IAGS=REPORT.rsplit('/',1)[0]+'/'
def physical(rel):
    p=str(ROOT/rel)
    return Path('\\\\?\\'+p) if os.name=='nt' else Path(p)
def blob(rel):return physical(rel).read_bytes()
def fingerprint(rel):return {'path':rel,'bytes':len(blob(rel)),'sha256':hashlib.sha256(blob(rel)).hexdigest()}
def git(*args):return subprocess.check_output(['git',*args],text=True).strip()
def main():
    assert not OUT.exists()
    baseline=json.loads((BASE/'entry_baseline.json').read_text())
    assert len(baseline)==74
    for row in baseline:assert hashlib.sha256(blob(row['path'])).hexdigest()==row['sha256'],row['path']
    assert not git('diff','--name-only') and not git('diff','--cached','--name-only')
    head=git('rev-parse','HEAD');branch=git('branch','--show-current')
    assert head=='fea2a25b05e97f726b6e1891cebb12c4cfca821a' and branch=='coarse-double-branch'
    remote=git('ls-remote','--heads','origin','coarse-double-branch').split()
    assert remote==[head,'refs/heads/coarse-double-branch']
    untracked=set(git('ls-files','--others','--exclude-standard').splitlines())
    old={r['path'] for r in baseline};new=untracked-old
    assert all(p==REPORT or p.startswith(BASE.as_posix()+'/') for p in new),new
    assert not any('__pycache__' in p or p.endswith('.pyc') for p in new)
    audit=json.loads((BASE/'audit_results.json').read_text());assert audit['status']=='COMPLETE'
    kernel=json.loads((BASE/'fringe_kernel_certificate.json').read_text())
    assert kernel['status']=='FAILED_SIGNED_EXTENSION' and len(kernel['failures'])==3
    sources=[
      'DO_RESEARCH_REBOOT/RESEARCH_RULES.md','python/independent/splay.py',
      'DO_RESEARCH_REBOOT/M2_SEP01/experiment.py',
      'DO_RESEARCH_REBOOT/M3_PHI01/verify_full_mixed.py',
      'DO_RESEARCH_REBOOT/M3_CHR01/verify_original_controls.py',
      'DO_RESEARCH_REBOOT/M3_CHR01/fragment_graph.py',
      'DO_RESEARCH_REBOOT/M3_CHR01/graph_catalog.json',
      'DO_RESEARCH_REBOOT/M3_CHR01/potential.bin',
      'DO_RESEARCH_REBOOT/M3_CHR01/edge_audit.json',
      'DO_RESEARCH_REBOOT/M3_LDR01/negative_run_census.json',
      'DO_RESEARCH_REBOOT/M3_LDR01/census_replay.json',
      'DO_RESEARCH_REBOOT/M3_LDR01/core_rotation_certificate.json']
    pc='DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/'
    strict='DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/'
    sources += [pc+x for x in ('PC_B_CONTROLLER.py','PC_ROTATION_INTERPRETER.py','PC_TYPED_DAG.py',
       'PC_STRUCTURAL_WITNESS.py','PC_ATOM_INVENTORY.py','PC_CONCRETIZE.py','PC_LOW_COMPILER.py')]
    sources += [strict+x for x in ('STRICT_LOW_COMPILER.py','STRICT_B_CONTROLLER.py',
       'STRICT_SOURCE_REPAIRS.py','STRICT_INVENTORY.py')]
    sources += ['DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE/STRICT_HIGH_COMPILER.py']
    sources += [IAGS+x for x in (
       'IAGS_WSIGN02D_UNIVERSAL_LOW_CREDIT_BOUND.md',
       'IAGS_11G_S03_M2_SEP01_SEPARATED_KEY8_REPAYMENT.md',
       'IAGS_11G_S03_M2_DSK01_DIRTY_SMALLER_KEY_SIGN.md',
       'IAGS_11G_S03_M3_PHI01_MIXED_HIGH_DEFICIT_EXCLUSION.md',
       'IAGS_11G_S03_M3_LDR01_LOW_DEFICIT_RUN_REPAYMENT.md',
       'IAGS_11G_S03_M3_CHR01_CHEAP_HELPER_CYCLE_CLOSURE.md')]
    files=[fingerprint(p) for p in sorted(new) if p!=OUT.as_posix()]
    data={'campaign':'IAGS-11G-S03-M3-H2R01','completed_utc':datetime.now(timezone.utc).isoformat(),
      'status':'COMPLETE','branch':branch,'local_head':head,'remote_branch_ref':remote[1],'remote_branch_tip':remote[0],
      'tracked_tree_unchanged':True,'baseline_files_preserved':74,'new_paths_confined_to_authorized_scope':True,
      'no_bytecode_created':True,'SMT_solver_invoked':False,'backend_switched':False,'graph':'G_AF','bank25':25,
      'principal_theorem':{'status':'PROVED—RESTRICTED DOMAIN','scope':'all original chi8 sigma=0 H=2 low edges; all masks, A witnesses, port shadows and macros',
         'potential':'Qbar=min(CHR01 Q extended by 0,-psi)','inequality':'Qbar(t)-Qbar(s)<=4-q'},
      'additional_theorem':{'status':'PROVED—RESTRICTED DOMAIN','scope':'all original chi8 H=2 weight-zero low helpers, arbitrary masks/signatures/fringe/A',
         'kernel_queries':43758,'retained_zero_kernel_rows':1024,'inequality':'Qbar(t)-Qbar(s)<=0'},
      'failed_extension':{'status':'REFUTED—EXACT','scope':'uniform capped potential inequality for chi8 H=2 weight +1',
         'full_original_counteredges':3,'actual_weights':[1,1,1],'reduced_weights':[-1,-1,-1],
         'kernels':[[952,2,1917],[1710,2,1937],[2538,3,2141]],'is_negative_cycle':False},
      'signed_walk_bound':{'scope':'named class F in report, preserving the old CHR01 H1 premises and adding proved H2 cases',
         'finite_path':'W>=Theta(last)-Theta(first)>=-2','fully_closed_walk':'W>=0'},
      'ledger':{'M1':'OPEN','M2':'PROVED—UNIVERSAL (inherited)','M3':'OPEN','Step03':'OPEN','Step04':'UNAUTHORIZED',
         'restricted_CoarseDouble':'OPEN','DynamicOptimality':'OPEN','negative_mixed_cycle':'NONE CERTIFIED'},
      'certificate':audit,'resources':{'original_low_DAG_nodes':1400081,'symbolic_primitive_cases':570,
         'symbolic_scalar_identities':65550,'CPU_gates':'all completed below registered 120/300 seconds; no cap increases',
         'computation':'exact integer finite enumeration and unchanged original DAG evaluation'},
      'files_excluding_this_manifest':files,'dependencies':[fingerprint(p) for p in sources],
      'entry_baseline':baseline}
    with OUT.open('x',encoding='utf-8') as f:json.dump(data,f,indent=2,ensure_ascii=False)
    # Recheck both preservation and saved manifest bytes after writing.
    saved=json.loads(OUT.read_text(encoding='utf-8'))
    for row in saved['files_excluding_this_manifest']+baseline:
        assert hashlib.sha256(blob(row['path'])).hexdigest()==row['sha256']
    assert not git('diff','--name-only') and not git('diff','--cached','--name-only')
    print(json.dumps({'status':'COMPLETE','old_files_preserved':74,'new_artifacts_including_manifest':len(files)+1,
        'dependencies_hashed':len(sources),'manifest_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),
        'tracked_tree_unchanged':True,'remote_tip':remote[0],'M3':'OPEN','negative_mixed_cycles_certified':0}),flush=True)
if __name__=='__main__':main()

