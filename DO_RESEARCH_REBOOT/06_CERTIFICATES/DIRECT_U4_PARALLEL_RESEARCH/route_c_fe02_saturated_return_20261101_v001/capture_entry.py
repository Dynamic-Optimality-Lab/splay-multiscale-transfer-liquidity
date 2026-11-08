"""Exclusive FE02 entry capture for a fresh sibling reproduction."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
BASE=HERE.parent
FE=BASE/'route_c_fe01_first_entry_20261101_v001'


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--directive',type=Path,default=Path('C:/Users/Saif malik/.codex/attachments/f02bc2fc-76b9-45b6-9b6b-3b22d958f65d/Pasted text.txt'))
    args=parser.parse_args();assert not (HERE/'entry_source_pins.json').exists()
    old=read(FE/'entry_source_pins.json');pins=dict(old['files'])
    for rel,h in pins.items():assert sha(ROOT/rel)==h,rel
    for name,h in read(FE/'delivery_manifest.json')['files'].items():assert sha(FE/name)==h,name
    audit=read(FE/'independent_audit.json');assert audit['status']=='PASS' and audit['total_checks']==350259
    for p in BASE.rglob('*'):
        if p.is_file() and HERE not in p.parents:pins[p.relative_to(ROOT).as_posix()]=sha(p)
    stage=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'
    stage_now={p.relative_to(stage).as_posix():sha(p) for p in stage.rglob('*') if p.is_file()}
    assert stage_now==old['stage_files'] and len(stage_now)==125
    head,branch,tracked=git('rev-parse','HEAD'),git('branch','--show-current'),git('status','--porcelain=v1','--untracked-files=no')
    assert branch=='coarse-double-branch' and not tracked
    directive=dict(path=str(args.directive),sha256=sha(args.directive)) if args.directive.is_file() else dict(path=str(args.directive),availability='not present on reproduction host')
    value=dict(head=head,branch=branch,tracked_status=tracked,files=pins,stage_files=stage_now,
        gate_sha256=sha(HERE/'FE02_00_FOUR_RULE_GATE.md'),
        prior_campaign_files=sum(p.is_file() and HERE not in p.parents for p in BASE.rglob('*')),
        inherited_FE01_audit_sha256=sha(FE/'independent_audit.json'),inherited_FE01_checks=350259,
        user_directive=directive,matching_terminal='FROZEN')
    with (HERE/'entry_source_pins.json').open('x',encoding='utf-8') as f:
        json.dump(value,f,indent=2);f.write('\n')
    print(json.dumps(dict(status='ENTRY_PINNED',head=head,inherited_files=len(pins['files']))))


if __name__=='__main__':main()
