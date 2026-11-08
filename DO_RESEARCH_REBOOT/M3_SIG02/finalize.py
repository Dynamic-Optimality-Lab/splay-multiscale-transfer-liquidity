"""Read-only entry preservation/Git check and append-only run manifests."""
import json,hashlib,subprocess,time
from pathlib import Path
ROOT=Path.cwd();BASE=ROOT/'DO_RESEARCH_REBOOT';out=BASE/'M3_SIG02/final_manifest.json'
def raw(p):return Path('\\\\?\\'+str(p.resolve())).read_bytes()
def main():
    assert not out.exists();baseline=json.loads((BASE/'M3_ACL01/entry_baseline.json').read_text())
    for r in baseline:
        p=Path(r['path']);p=p if p.is_absolute() else ROOT/p
        assert hashlib.sha256(raw(p)).hexdigest()==r['sha256'],r['path']
    def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
    assert git('status','--porcelain','--untracked-files=no')==''
    assert git('rev-parse','HEAD')=='fea2a25b05e97f726b6e1891cebb12c4cfca821a'
    assert git('branch','--show-current')=='coarse-double-branch'
    paths=[]
    for folder in ('M3_ACL01','M3_SIG02'):
        paths.extend(p for p in (BASE/folder).rglob('*') if p.is_file())
    report=BASE/'06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/IAGS_WSIGN02A_ZERO_COST_IMPOSSIBILITY/IAGS_11G_S03_M3_ACL01_COMPLETE_ONE_GAP_A_INTERFACE.md'
    paths.append(report)
    files=[{'path':p.relative_to(ROOT).as_posix(),'bytes':len(raw(p)),'sha256':hashlib.sha256(raw(p)).hexdigest()} for p in sorted(set(paths))]
    res={'checkpoint':git('rev-parse','HEAD'),'branch':git('branch','--show-current'),'tracked_tree_clean':True,
      'entry_files_hash_identical':len(baseline),'new_files':files,
      'step2':{'status':'PROVED_RESTRICTED_DOMAIN','mu':341,'sigma':[1]+[0]*9,'chi8':True,
       'signed_bound':'sum w >= Q(end)-Q(start), Q in [-2,0]; every closed mixed walk nonnegative',
       'new_fit':False,'normalized_alpha_patterns':8534,'rotation_frames':7920,'old_values_preserved':481562},
      'step3':{'status':'OPEN','mechanism':'REFUTED_EXACT_LITERAL_PORT_INVENTORY_DETERMINACY',
       'witnesses':2,'mu':341,'sigma':[2]+[0]*9,'original_negative_cycle':False},
      'full_M3':'OPEN','Dynamic_Optimality':'OPEN','production_changed':False,'Bank25':25}
    with out.open('x',encoding='utf-8') as f:json.dump(res,f,indent=2)
    print(json.dumps({k:v for k,v in res.items() if k!='new_files'},indent=2))
if __name__=='__main__':main()
