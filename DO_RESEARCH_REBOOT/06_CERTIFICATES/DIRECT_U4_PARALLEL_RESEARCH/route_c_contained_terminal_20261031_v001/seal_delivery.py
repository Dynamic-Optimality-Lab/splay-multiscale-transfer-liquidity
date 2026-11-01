"""Final exclusive seal of this run; no old files are written."""
import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
STAGE = ROOT / 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def save(name,value):
    with (HERE / name).open('x',encoding='utf-8') as f:
        json.dump(value,f,indent=2,ensure_ascii=False);f.write('\n')

def git(*args):
    return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()

def main():
    pins = json.loads((HERE / 'entry_source_pins.json').read_text(encoding='utf-8'))
    for rel,value in pins['files'].items():
        assert sha(ROOT / rel) == value, rel
    stage = {p.relative_to(STAGE).as_posix():sha(p) for p in STAGE.rglob('*') if p.is_file()}
    assert stage == pins['stage_files'] and len(stage) == 125
    head,branch = git('rev-parse','HEAD'),git('branch','--show-current')
    status = git('status','--porcelain=v1','--untracked-files=no')
    assert (head,branch,status) == (pins['head'],pins['branch'],pins['tracked_status']) and not status
    audit = json.loads((HERE / 'independent_audit.json').read_text(encoding='utf-8'))
    assert audit['status'] == 'PASS' and audit['certificate_sha256'] == sha(HERE / 'contained_terminal_certificate.json')
    save('final_integrity.json',dict(status='PASS',date='2026-10-31',
         inherited_source_and_previous_run_files_unchanged=len(pins['files']),
         stage_11G_files_unchanged=len(stage),stage_inventory_unchanged=True,
         head=head,branch=branch,tracked_status=status,
         next_campaign_launched=False,original_proof_obligations_discharged=0))
    files = {p.name:sha(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name != 'delivery_manifest.json'}
    save('delivery_manifest.json',dict(date='2026-10-31',files=files,manifest_excludes_itself=True))
    print(json.dumps(dict(status='PASS',preserved_files=len(pins['files']),stage_11G_files=len(stage),sealed_artifacts=len(files)),indent=2))

if __name__ == '__main__':
    main()
