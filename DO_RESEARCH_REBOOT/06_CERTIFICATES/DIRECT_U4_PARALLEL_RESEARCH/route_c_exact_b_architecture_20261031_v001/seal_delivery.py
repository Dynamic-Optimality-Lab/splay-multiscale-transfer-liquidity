"""Exclusive final preservation seal and delivery manifest; no old file writes."""
import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
STAGE = ROOT / 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def save(name, obj):
    with (HERE / name).open('x', encoding='utf-8') as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write('\n')

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()

def main():
    pins = json.loads((HERE / 'entry_source_pins.json').read_text(encoding='utf-8'))
    for rel, value in pins['files'].items():
        assert digest(ROOT / rel) == value, rel
    stage = {p.relative_to(STAGE).as_posix(): digest(p) for p in STAGE.rglob('*') if p.is_file()}
    assert stage == pins['stage_files'] and len(stage) == 125
    head = git('rev-parse', 'HEAD')
    branch = git('branch', '--show-current')
    status = git('status', '--porcelain=v1', '--untracked-files=no')
    assert head == pins['head'] and branch == pins['branch'] and status == pins['tracked_status'] == ''
    audit = json.loads((HERE / 'independent_audit.json').read_text(encoding='utf-8'))
    assert audit['status'] == 'PASS'
    assert digest(HERE / 'exact_b_architecture_certificate.json') == audit['certificate_sha256']
    save('final_integrity.json', dict(status='PASS', date='2026-10-31',
         source_and_previous_run_files_unchanged=len(pins['files']),
         inherited_source_pins= pins['inherited_pin_count'],
         stage_11G_files_unchanged=len(stage), stage_inventory_unchanged=True,
         head=head, branch=branch, tracked_status=status,
         original_proof_obligations_discharged=0, next_campaign_launched=False))
    files = {p.name: digest(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name != 'delivery_manifest.json'}
    save('delivery_manifest.json', dict(date='2026-10-31', files=files, manifest_excludes_itself=True))
    print(json.dumps(dict(status='PASS', preserved_files=len(pins['files']),
                         stage_11G_files=len(stage), sealed_artifacts=len(files)), indent=2))

if __name__ == '__main__':
    main()
