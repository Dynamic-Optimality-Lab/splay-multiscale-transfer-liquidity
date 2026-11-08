"""Exclusive FE01 entry capture for reproduction in a fresh sibling."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
BASE=HERE.parent
PG=BASE/'route_c_pf_positive_gap_closure_20261101_v001'


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--directive',type=Path,default=Path('C:/Users/Saif malik/.codex/attachments/ef3cc792-e6af-475f-ac6b-df65d59f6c59/Pasted text.txt'))
    args=parser.parse_args()
    assert not (HERE/'entry_source_pins.json').exists(),'use a fresh sibling, never overwrite pins'
    old=read(PG/'entry_source_pins.json');pins=dict(old['files'])
    for rel,h in pins.items():assert sha(ROOT/rel)==h,rel
    for p in BASE.rglob('*'):
        if p.is_file() and HERE not in p.parents:pins[p.relative_to(ROOT).as_posix()]=sha(p)
    stage=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'
    stage_now={p.relative_to(stage).as_posix():sha(p) for p in stage.rglob('*') if p.is_file()}
    assert stage_now==old['stage_files'] and len(stage_now)==125
    for name,h in read(PG/'delivery_manifest.json')['files'].items():assert sha(PG/name)==h
    head,branch,tracked=git('rev-parse','HEAD'),git('branch','--show-current'),git('status','--porcelain=v1','--untracked-files=no')
    assert branch=='coarse-double-branch' and not tracked
    directive=dict(path=str(args.directive),sha256=sha(args.directive)) if args.directive.is_file() else dict(path=str(args.directive),availability='not present on this reproduction host')
    result=dict(head=head,branch=branch,tracked_status=tracked,files=pins,stage_files=stage_now,
        gate_sha256=sha(HERE/'FE00_FOUR_RULE_GATE.md'),
        prior_campaign_files=sum(p.is_file() and HERE not in p.parents for p in BASE.rglob('*')),
        user_directive=directive,matching_terminal='FROZEN')
    with (HERE/'entry_source_pins.json').open('x',encoding='utf-8') as f:
        json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(dict(status='ENTRY_PINNED',head=head,inherited_files=len(pins),stage_11g=125)))


if __name__=='__main__':main()
