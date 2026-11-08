import json,hashlib,subprocess,time
from pathlib import Path
from baseline import digest,BASE
def main():
    start=time.process_time();out=BASE/'integrity.json';assert not out.exists()
    b=json.loads((BASE/'entry_baseline.json').read_text());changed=[];missing=[]
    old={r['path'] for r in b['files']}
    for row in b['files']:
        p=Path(row['path'])
        if not p.is_file():missing.append(row['path'])
        elif digest(p)!=row['sha256']:changed.append(row['path'])
    unexpected=[p.as_posix() for p in Path('DO_RESEARCH_REBOOT').rglob('*') if p.is_file() and BASE not in p.parents and p.as_posix() not in old]
    status=subprocess.check_output(['git','status','--short','--untracked-files=no'],text=True)
    head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
    assert not changed and not missing and not unexpected and not status and head==b['head']
    obj={'status':'PASS','old_research_files_checked':len(old),'changed':changed,'missing':missing,'unexpected_new_paths':unexpected,
      'tracked_status':status,'head':head,'R1_R4_preserved':True,'new_writes_confined_to':BASE.as_posix(),
      'cpu_seconds':round(time.process_time()-start,3)}
    with out.open('x',encoding='utf-8') as f:json.dump(obj,f,indent=2)
    files=[{'path':p.as_posix(),'bytes':p.stat().st_size,'sha256':digest(p)} for p in sorted(BASE.iterdir()) if p.is_file()]
    result={'campaign':'M3_TWOGAP01','status':'STEPS_1_2_COMPLETE_CONSTRUCTED_PENDING_INDEPENDENT_CERTIFICATION',
      'signature':[1,1]+[0]*8,'mask_count':126,'chi8_regions':'both','private_branch_assignments':462916,
      'alpha_classes':29397,'A_access_options':430806,'J_range':[-2,0],'construction_side_explicit_residuals':23007924,
      'full_original_root_controls':18,'high_h0_correction_retained':True,'independent_step3_complete':False,
      'step4_complete':False,'full_M3_proved':False,'negative_original_cycle_certified':False,
      'old_audited_bank_promoted':False,'integrity':obj,'files':files,
      'next':['3: independent certificate audit','4: other positions/populations/support sizes; full coverage audit']}
    with (BASE/'final_manifest.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='files'},indent=2),flush=True)
if __name__=='__main__':main()
