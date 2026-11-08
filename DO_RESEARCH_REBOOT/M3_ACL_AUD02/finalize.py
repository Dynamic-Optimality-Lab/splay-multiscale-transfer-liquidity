"""Preservation and exact artifact integrity for the repaired continuation."""
import json,hashlib,subprocess
from pathlib import Path
ROOT=Path.cwd();BASE=ROOT/'DO_RESEARCH_REBOOT';HERE=BASE/'M3_ACL_AUD02';out=HERE/'final_manifest.json'
def read(p):return Path('\\\\?\\'+str(p.resolve())).read_bytes()
def main():
    assert not out.exists();entry=json.loads((HERE/'entry_baseline.json').read_text())
    for r in entry:assert hashlib.sha256(read(ROOT/r['path'])).hexdigest()==r['sha256'],r['path']
    def git(*args):return subprocess.check_output(['git',*args],text=True,cwd=ROOT).strip()
    assert git('status','--porcelain','--untracked-files=no')==''
    assert git('rev-parse','HEAD')=='fea2a25b05e97f726b6e1891cebb12c4cfca821a'
    matches={}
    for name in ('ordinary_a','ordinary_b','offsets','targets','weights','meta','potential'):
        a=BASE/f'M3_MSK01/{name}.bin';b=BASE/f'M3_MSK01/replay_v2/{name}.bin'
        matches[name]=hashlib.sha256(read(a)).hexdigest()==hashlib.sha256(read(b)).hexdigest();assert matches[name]
    statuses={
      'AER_finite':json.loads((BASE/'M3_AER01/repair_certificate.json').read_text())['status'],
      'AER_original':json.loads((BASE/'M3_AER01/original_replay.json').read_text())['status'],
      'MSK_finite':json.loads((BASE/'M3_MSK01/replay_v2/edge_audit.json').read_text())['status'],
      'MSK_original':json.loads((BASE/'M3_MSK01/replay_v2/original_audit_v2.json').read_text())['status'],
      'ZER_original':json.loads((BASE/'M3_ZER01/certificate.json').read_text())['status']}
    assert all(v in ('PASS','FINITE_EXACT_VERIFIED') for v in statuses.values())
    files=[]
    for folder in ('M3_ACL_AUD02','M3_AER01','M3_MSK01','M3_ZER01'):
        for p in sorted((BASE/folder).rglob('*')):
            if p.is_file():files.append({'path':p.relative_to(ROOT).as_posix(),'bytes':len(read(p)),'sha256':hashlib.sha256(read(p)).hexdigest()})
    src=BASE/'06_CERTIFICATES'
    relevant=[src/'DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER'/n for n in ('PC_STRUCTURAL_WITNESS.py','PC_ROTATION_INTERPRETER.py','PC_ATOM_INVENTORY.py','PC_B_CONTROLLER.py','PC_TYPED_DAG.py')]
    relevant += [src/'DIRECT_CDK5N_11F_STRICT_CLOSURE'/n for n in ('STRICT_LOW_COMPILER.py','STRICT_HIGH_COMPILER.py','STRICT_B_CONTROLLER.py','STRICT_INVENTORY.py','STRICT_SOURCE_REPAIRS.py')]
    sources=[{'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(read(p)).hexdigest()} for p in relevant]
    result={'status':'PASS','entry_files_hash_identical':len(entry),'tracked_tree_clean':True,'checkpoint':git('rev-parse','HEAD'),
      'old_ACL01_full_source_potential':'REFUTED_EXACT_SUPERSEDED','AER_corrected_fixed_sector':'PROVED_RESTRICTED_DOMAIN',
      'MSK_all126_one_gap0_fringe_sectors':'PROVED_RESTRICTED_DOMAIN','ZER_all126_zero_fringe_sectors':'PROVED_RESTRICTED_DOMAIN',
      'combined_mask_signature_sectors':252,'range':[-2,0],'old_negative_residuals_fixed':2,
      'checks':statuses,'strict_resource_replay_data_identical':matches,'negative_mixed_cycle_certified':False,
      'full_M3':'OPEN','Dynamic_Optimality':'OPEN','Bank25':25,'files':files,'frozen_source_hashes':sources}
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k not in ('files','frozen_source_hashes')},indent=2))
if __name__=='__main__':main()
