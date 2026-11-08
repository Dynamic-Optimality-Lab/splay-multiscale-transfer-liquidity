from entry import BASE,sha
from pathlib import Path
import json,subprocess
def main():
    out=BASE/'integrity.json';assert not out.exists();e=json.loads((BASE/'entry_baseline.json').read_text());old={r['path'] for r in e['files']}
    assert all(Path(r['path']).is_file() and sha(Path(r['path']))==r['sha256'] for r in e['files'])
    extra=[p.as_posix() for p in Path('DO_RESEARCH_REBOOT').rglob('*') if p.is_file() and BASE not in p.parents and p.as_posix() not in old];assert not extra
    assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],text=True)
    assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==e['head']
    f=json.loads((BASE/'finite_audit.json').read_text());s=json.loads((BASE/'source_audit.json').read_text());assert f['status']=='INDEPENDENT_FINITE_EXACT_PASS' and s['status']=='INDEPENDENT_ORIGINAL_SOURCE_AND_FULL_CLOSURE_PASS'
    integrity={'status':'PASS','old_files_unchanged':len(old),'new_writes_confined_here':True,'head':e['head'],'tracked_tree_clean':True}
    with out.open('x',encoding='utf-8') as z:json.dump(integrity,z,indent=2)
    manifest={'status':'PROVED_RESTRICTED_DOMAIN_INDEPENDENT_AUDIT_PASS','signature':[1,1]+[0]*8,'masks':126,'regions':'both',
      'arbitrary_walk_bound':-7,'closed_walk_lower_bound':0,'new_sign_sectors':126,'full_M3_proved':False,'step3_complete':True,
      'R1_R4_preserved':True,'integrity':integrity,'files':[{'path':p.as_posix(),'sha256':sha(p)} for p in sorted(BASE.iterdir()) if p.is_file()]}
    with (BASE/'final_manifest.json').open('x',encoding='utf-8') as z:json.dump(manifest,z,indent=2)
    print(json.dumps({k:v for k,v in manifest.items() if k!='files'},indent=2),flush=True)
if __name__=='__main__':main()
