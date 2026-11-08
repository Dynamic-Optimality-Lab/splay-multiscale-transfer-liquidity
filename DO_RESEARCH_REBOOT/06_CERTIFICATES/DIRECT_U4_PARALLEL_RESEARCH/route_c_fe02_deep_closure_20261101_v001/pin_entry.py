"""Append-only entry pinning, before new source evaluation."""
import hashlib
import json
import subprocess
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
BASE=HERE.parent
OLD=BASE/'route_c_fe02_turn_reset_20261101_v001'
STAGE=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def git(*a):return subprocess.check_output(['git','--no-optional-locks',*a],cwd=ROOT,text=True).strip()


def main():
    prior=read(OLD/'entry_source_pins.json')
    files=dict(prior['files'])
    for p,h in files.items():assert sha(ROOT/p)==h,p
    manifest=read(OLD/'delivery_manifest.json')
    assert {p.name for p in OLD.iterdir()}==set(manifest['files'])|{'delivery_manifest.json'}
    for p,h in manifest['files'].items():assert sha(OLD/p)==h,p
    for p in OLD.iterdir():
        assert p.is_file()
        files[p.relative_to(ROOT).as_posix()]=sha(p)
    assert len(files)==1166
    prefix=BASE.relative_to(ROOT).as_posix()+'/'
    expected={p for p in files if p.startswith(prefix)}
    actual={p.relative_to(ROOT).as_posix() for p in BASE.rglob('*') if p.is_file() and HERE not in p.parents}
    assert actual==expected and len(actual)==1020
    stage={p.relative_to(STAGE).as_posix():sha(p) for p in STAGE.rglob('*') if p.is_file()}
    assert stage==prior['stage_files'] and len(stage)==125
    assert git('rev-parse','HEAD')==prior['head']
    assert git('branch','--show-current')==prior['branch']
    assert git('status','--short','--untracked-files=no')==prior['tracked_status']==''
    data=dict(head=prior['head'],branch=prior['branch'],tracked_status='',files=files,
        stage_files=stage,prior_campaign_files=1020,
        gate_hashes={p.name:sha(p) for p in HERE.glob('DC00*.md')},matching_terminal='FROZEN',
        inherited_turn_reset_manifest_sha256=sha(OLD/'delivery_manifest.json'))
    with (HERE/'entry_source_pins.json').open('x',encoding='utf-8') as f:json.dump(data,f,indent=2);f.write('\n')
    print(json.dumps(dict(status='PASS',inherited_files=len(files),prior_campaign_files=1020,
        Stage11G_files=125,head=prior['head'])))


if __name__=='__main__':main()
