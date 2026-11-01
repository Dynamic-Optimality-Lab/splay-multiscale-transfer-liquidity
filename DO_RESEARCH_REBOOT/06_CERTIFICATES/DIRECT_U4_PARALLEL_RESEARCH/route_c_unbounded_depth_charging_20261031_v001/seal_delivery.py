"""Exclusive final seal for arbitrary-key charging; no old file mutations."""
import hashlib
import json
import subprocess
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
STAGE=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,value):
    with (HERE/name).open('x',encoding='utf-8') as f:json.dump(value,f,indent=2,ensure_ascii=False);f.write('\n')
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()

def main():
    entry=json.loads((HERE/'entry_source_pins.json').read_text(encoding='utf-8'))
    for rel,h in entry['files'].items():assert sha(ROOT/rel)==h,rel
    stage={p.relative_to(STAGE).as_posix():sha(p) for p in STAGE.rglob('*') if p.is_file()}
    assert stage==entry['stage_files'] and len(stage)==125
    head,branch,status=git('rev-parse','HEAD'),git('branch','--show-current'),git('status','--porcelain=v1','--untracked-files=no')
    assert (head,branch,status)==(entry['head'],entry['branch'],entry['tracked_status']) and not status
    audit=json.loads((HERE/'independent_audit.json').read_text(encoding='utf-8'))
    assert audit['status']=='PASS' and audit['certificate_sha256']==sha(HERE/'arbitrary_key_certificate.json')
    assert audit['prior_successful_SL_cuts_preserved']==314 and audit['old_source_controls_preserved']==10
    ledger=json.loads((HERE/'proof_status_ledger.json').read_text(encoding='utf-8'))
    assert ledger['universal_CD']=='OPEN' and ledger['matching_terminal_line']=='FROZEN' and not ledger['next_campaign_launched']
    freeze=HERE.parent/'route_c_full_form_obstruction_audit_20261031_v001/FF01_MATCHING_TERMINAL_FREEZE.md'
    assert 'FROZEN BY EXPLICIT USER INSTRUCTION' in freeze.read_text(encoding='utf-8')
    save('final_integrity.json',dict(status='PASS',date='2026-10-31',inherited_source_and_previous_run_files_unchanged=len(entry['files']),
      stage_11G_files_unchanged=len(stage),stage_inventory_unchanged=True,head=head,branch=branch,tracked_status=status,
      matching_terminal_line='FROZEN',restricted_arbitrary_depth_class_proved=True,strict_extension_of_SL=True,
      universal_CD='OPEN',next_campaign_launched=False))
    files={p.name:sha(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='delivery_manifest.json'}
    save('delivery_manifest.json',dict(date='2026-10-31',files=files,manifest_excludes_itself=True))
    print(json.dumps(dict(status='PASS',preserved_files=len(entry['files']),stage_11G_files=len(stage),sealed_artifacts=len(files)),indent=2))

if __name__=='__main__':main()
