"""Exclusive final integrity seal preserving both producer versions and entries."""
import hashlib
import json
import subprocess
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
STAGE=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,value):
    with (HERE/name).open('x',encoding='utf-8') as f:
        json.dump(value,f,indent=2,ensure_ascii=False);f.write('\n')
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()

def main():
    entry=json.loads((HERE/'entry_source_pins_v002.json').read_text(encoding='utf-8'))
    for rel,value in entry['files'].items():assert sha(ROOT/rel)==value,rel
    first=HERE/'entry_source_pins.json'
    if first.exists():
        v1=json.loads(first.read_text(encoding='utf-8'))
        assert v1['files']==entry['files'] and v1['stage_files']==entry['stage_files']
    stage={p.relative_to(STAGE).as_posix():sha(p) for p in STAGE.rglob('*') if p.is_file()}
    assert stage==entry['stage_files'] and len(stage)==125
    head,branch=git('rev-parse','HEAD'),git('branch','--show-current')
    status=git('status','--porcelain=v1','--untracked-files=no')
    assert (head,branch,status)==(entry['head'],entry['branch'],entry['tracked_status']) and not status
    audit=json.loads((HERE/'independent_audit.json').read_text(encoding='utf-8'))
    assert audit['status']=='PASS' and audit['certificate_sha256']==sha(HERE/'delayed_shallow_certificate.json')
    freeze=HERE.parent/'route_c_full_form_obstruction_audit_20261031_v001/FF01_MATCHING_TERMINAL_FREEZE.md'
    assert 'FROZEN BY EXPLICIT USER INSTRUCTION' in freeze.read_text(encoding='utf-8')
    save('final_integrity.json',dict(status='PASS',date='2026-10-31',
      inherited_source_and_previous_run_files_unchanged=len(entry['files']),
      stage_11G_files_unchanged=len(stage),stage_inventory_unchanged=True,
      initial_entry_and_producer_preserved=first.exists(),corrected_producer_version='v002',
      head=head,branch=branch,tracked_status=status,matching_terminal_line='FROZEN',
      restricted_delayed_class_proved=True,universal_CD='OPEN',next_campaign_launched=False))
    files={p.name:sha(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='delivery_manifest.json'}
    save('delivery_manifest.json',dict(date='2026-10-31',files=files,manifest_excludes_itself=True))
    print(json.dumps(dict(status='PASS',preserved_files=len(entry['files']),stage_11G_files=len(stage),sealed_artifacts=len(files)),indent=2))

if __name__=='__main__':main()
