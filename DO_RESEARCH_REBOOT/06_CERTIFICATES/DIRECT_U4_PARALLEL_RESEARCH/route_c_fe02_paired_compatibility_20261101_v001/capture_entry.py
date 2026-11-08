"""Exclusive preservation capture for fresh FE02 continuation reproduction."""
import hashlib
import json
import subprocess
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
BASE=HERE.parent
OLD=BASE/'route_c_fe02_saturated_return_20261101_v001'


def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()


def main():
    assert not (HERE/'entry_source_pins.json').exists(),'use a fresh sibling'
    inherited=read(OLD/'entry_source_pins.json');pins=dict(inherited['files'])
    pins.update(read(OLD/'additional_dependency_pins.json')['files'])
    for rel,h in pins.items():assert sha(ROOT/rel)==h,rel
    for name,h in read(OLD/'delivery_manifest.json')['files'].items():assert sha(OLD/name)==h,name
    for p in BASE.rglob('*'):
        if p.is_file() and HERE not in p.parents:pins[p.relative_to(ROOT).as_posix()]=sha(p)
    stage=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'
    stage_now={p.relative_to(stage).as_posix():sha(p) for p in stage.rglob('*') if p.is_file()}
    assert stage_now==inherited['stage_files'] and len(stage_now)==125
    head,branch,tracked=git('rev-parse','HEAD'),git('branch','--show-current'),git('status','--porcelain=v1','--untracked-files=no')
    assert branch=='coarse-double-branch' and not tracked
    value=dict(head=head,branch=branch,tracked_status=tracked,files=pins,stage_files=stage_now,
        gate_sha256=sha(HERE/'PC00_FOUR_RULE_GATE.md'),
        prior_campaign_files=sum(p.is_file() and HERE not in p.parents for p in BASE.rglob('*')),
        authorization='current user resumes/refines FE02; no FE03',matching_terminal='FROZEN')
    with (HERE/'entry_source_pins.json').open('x',encoding='utf-8') as f:
        json.dump(value,f,indent=2);f.write('\n')
    print(json.dumps(dict(status='ENTRY_PINNED',head=head,inherited_files=len(pins))))


if __name__=='__main__':main()
