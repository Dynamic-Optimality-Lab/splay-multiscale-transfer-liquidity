"""Pin unchanged research for the mandatory gate review only."""
import hashlib
import json
import subprocess
from pathlib import Path

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];BASE=HERE.parent
OLD=BASE/'route_c_fe02_deep_closure_20261101_v001'
STAGE=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def git(*a):return subprocess.check_output(['git','--no-optional-locks',*a],cwd=ROOT,text=True).strip()


def main():
    pins=read(OLD/'entry_source_pins.json');files=dict(pins['files'])
    for p,h in files.items():assert sha(ROOT/p)==h,p
    d=read(OLD/'delivery_manifest.json')
    assert {p.name for p in OLD.iterdir()}==set(d['files'])|{'delivery_manifest.json'}
    for p,h in d['files'].items():assert sha(OLD/p)==h,p
    for p in OLD.iterdir():
        assert p.is_file();files[p.relative_to(ROOT).as_posix()]=sha(p)
    assert len(files)==1184
    prefix=BASE.relative_to(ROOT).as_posix()+'/'
    expected={p for p in files if p.startswith(prefix)}
    actual={p.relative_to(ROOT).as_posix() for p in BASE.rglob('*') if p.is_file() and HERE not in p.parents}
    assert actual==expected and len(actual)==1038
    stage={p.relative_to(STAGE).as_posix():sha(p) for p in STAGE.rglob('*') if p.is_file()}
    assert stage==pins['stage_files'] and len(stage)==125
    assert git('rev-parse','HEAD')==pins['head']
    assert git('branch','--show-current')==pins['branch']
    assert git('status','--short','--untracked-files=no')==pins['tracked_status']==''
    result=dict(head=pins['head'],branch=pins['branch'],tracked_status='',files=files,
        prior_campaign_files=1038,stage_files=stage,gate_sha256=sha(HERE/'CG00_PRE_EXECUTION_GATE_REVIEW.md'),
        proof_campaign_gate='FAIL; mandatory review only',matching_terminal='FROZEN')
    with (HERE/'entry_source_pins.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(dict(status='PASS',inherited_files=len(files),prior_inventory=1038,
        Stage11G_files=125,proof_campaign_gate='FAIL; review only')))


if __name__=='__main__':main()
