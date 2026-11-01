"""File/Git preservation only. Does not import or execute either splay source."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OLD = HERE.parent / 'route_c_child_return_coupling_20261031_v001'
STAGE = ROOT / 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(name, value):
    with (HERE / name).open('x', encoding='utf-8') as f:
        json.dump(value, f, indent=2, ensure_ascii=False)
        f.write('\n')


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def stage_inventory():
    return {p.relative_to(STAGE).as_posix(): sha(p) for p in STAGE.rglob('*') if p.is_file()}


def entry():
    old = json.loads((OLD / 'entry_source_pins.json').read_text(encoding='utf-8'))
    pins = dict(old['files'])
    for rel, h in pins.items():
        assert sha(ROOT / rel) == h, rel
    for p in HERE.parent.rglob('*'):
        if p.is_file() and HERE not in p.parents:
            pins[p.relative_to(ROOT).as_posix()] = sha(p)
    stage = stage_inventory()
    assert stage == old['stage_files'] and len(stage) == 125
    assert not git('status', '--porcelain=v1', '--untracked-files=no')
    assert (git('rev-parse', 'HEAD'), git('branch', '--show-current')) == (old['head'], old['branch'])
    save('entry_source_pins.json', dict(date='2026-10-31', head=old['head'], branch=old['branch'],
        tracked_status='', files=pins, stage_files=stage, inherited_pins=len(old['files']),
        operation='read-only preservation pinning; no mathematical source execution'))
    print(json.dumps(dict(status='PASS', prior_files=len(pins), stage_11G_files=len(stage), new_splay_source_calls=0)))


def seal():
    ent = json.loads((HERE / 'entry_source_pins.json').read_text(encoding='utf-8'))
    for rel, h in ent['files'].items():
        assert sha(ROOT / rel) == h, rel
    prefix = HERE.parent.relative_to(ROOT).as_posix() + '/'
    previous = {p.relative_to(ROOT).as_posix() for p in HERE.parent.rglob('*') if p.is_file() and HERE not in p.parents}
    assert previous == {rel for rel in ent['files'] if rel.startswith(prefix)}
    stage = stage_inventory()
    assert stage == ent['stage_files'] and len(stage) == 125
    head, branch, status = git('rev-parse', 'HEAD'), git('branch', '--show-current'), git('status', '--porcelain=v1', '--untracked-files=no')
    assert (head, branch, status) == (ent['head'], ent['branch'], ent['tracked_status']) and not status
    ledger = json.loads((HERE / 'proof_status_ledger.json').read_text(encoding='utf-8'))
    assert ledger['requested_cycle'] == 'OPEN; NOT CONSTRUCTED'
    assert ledger['cycle_campaign_four_rule_gate'] == 'FAIL: rules 2, 3 and 4'
    assert ledger['new_splay_source_calls'] == ledger['new_finite_cases'] == ledger['finite_fits'] == 0
    assert not ledger['cycle_campaign_launched'] and not ledger['closed_cycle_verified']
    assert ledger['cycle_G_B'] is None and ledger['cycle_J_B'] is None
    assert ledger['prefix_positive_excess'] == 1 and ledger['prefix_pure_capacity'] == 4
    assert ledger['universal_CD'] == 'OPEN' and ledger['matching_terminal_line'] == 'FROZEN'
    assert not ledger['new_original_CD_walk_class_settled'] and not ledger['automatic_successor_launched']
    freeze = HERE.parent / 'route_c_full_form_obstruction_audit_20261031_v001/FF01_MATCHING_TERMINAL_FREEZE.md'
    assert 'FROZEN BY EXPLICIT USER INSTRUCTION' in freeze.read_text(encoding='utf-8')
    save('final_integrity.json', dict(status='PASS', date='2026-10-31',
        inherited_source_and_prior_files_unchanged=len(ent['files']), previous_research_inventory_unchanged=True,
        stage_11G_files_unchanged=len(stage), stage_inventory_unchanged=True, head=head, branch=branch, tracked_status=status,
        cycle_campaign_gate='FAILED; not launched', requested_cycle='OPEN; NOT CONSTRUCTED',
        new_splay_source_calls=0, new_finite_cases=0, finite_fits=0, matching_terminal_line='FROZEN',
        universal_CD='OPEN', automatic_successor_launched=False))
    files = {p.name: sha(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name != 'delivery_manifest.json'}
    save('delivery_manifest.json', dict(date='2026-10-31', files=files, manifest_excludes_itself=True))
    print(json.dumps(dict(status='PASS', prior_files=len(ent['files']), stage_11G_files=len(stage),
        sealed_artifacts=len(files), new_splay_source_calls=0, cycle_campaign='NOT LAUNCHED'), indent=2))


if __name__ == '__main__':
    assert len(sys.argv) == 2 and sys.argv[1] in ('entry', 'seal')
    entry() if sys.argv[1] == 'entry' else seal()
