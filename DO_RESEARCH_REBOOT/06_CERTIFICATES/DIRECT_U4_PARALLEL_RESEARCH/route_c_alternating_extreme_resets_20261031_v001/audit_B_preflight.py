"""The one predeclared alternating-extreme B orbit; no replacement word."""
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OLD = HERE.parent / 'route_c_26_keep_coupling_obstruction_20261031_v001'
STAGE = ROOT / 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'
WORD = [9, 5, 13, 3, 11, 7, 1, 2, 10, 6, 13, 4, 12, 8, 1]
CAP = 64


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(name, value):
    with (HERE / name).open('x', encoding='utf-8') as f:
        json.dump(value, f, indent=2, ensure_ascii=False)
        f.write('\n')


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def main():
    old = json.loads((OLD / 'entry_source_pins.json').read_text(encoding='utf-8'))
    pins = dict(old['files'])
    for rel, digest in pins.items():
        assert sha(ROOT / rel) == digest, rel
    for p in HERE.parent.rglob('*'):
        if p.is_file() and HERE not in p.parents:
            pins[p.relative_to(ROOT).as_posix()] = sha(p)
    stage = {p.relative_to(STAGE).as_posix(): sha(p) for p in STAGE.rglob('*') if p.is_file()}
    assert stage == old['stage_files'] and len(stage) == 125
    assert not git('status', '--porcelain=v1', '--untracked-files=no')
    assert (git('rev-parse', 'HEAD'), git('branch', '--show-current')) == (old['head'], old['branch'])
    save('entry_source_pins.json', dict(date='2026-10-31', head=old['head'], branch=old['branch'],
        tracked_status='', files=pins, stage_files=stage, inherited_pins=len(old['files']),
        gate_sha256=sha(HERE / 'AE00_FOUR_RULE_GATE.md')))
    spec = importlib.util.spec_from_file_location('tuple_source', ROOT / 'python/independent/splay.py')
    s = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(s)
    L = s.LEAF

    def raw(t):
        return None if t == L else [t[1], raw(t[2]), raw(t[3])]

    initial = b = s.vine(13)
    seen = {b: 0}
    boundaries = [dict(lap=0, B=raw(b))]
    rows = []
    start = end = None
    assert len(WORD) == 15 and set(WORD) == set(range(1, 14))
    assert all(WORD[i] != WORD[(i+1) % 15] for i in range(15))
    assert all(WORD[(i-1) % 15] != WORD[(i+1) % 15] for i in range(15))
    for lap in range(1, CAP+1):
        for key in WORD:
            found, d = s.lookup(b, key)
            assert found and d > 0 and s.inorder(b) == list(range(1, 14))
            before = b
            b, ev = s.trace(b, key)
            q, z = sum(e[0] != 'ZIG' for e in ev), sum(e[0] == 'ZIG' for e in ev)
            assert (q, z, len(ev)) == (d//2, d%2, (d+1)//2)
            assert s.inorder(b) == list(range(1, 14))
            rows.append(dict(occurrence=len(rows), lap=lap-1, word_position=len(rows) % 15,
                key=key, source_B=raw(before), destination_B=raw(b), d_B=d, q=q, z=z, B_events=ev))
        boundaries.append(dict(lap=lap, B=raw(b)))
        if b in seen:
            start, end = seen[b], lap
            break
        seen[b] = lap
    recurrent = None
    if start is None:
        outcome = 'OPEN_B_FIRST_REPEAT_CAP'
    else:
        cyc = rows[15*start:15*end]
        q = [r['q'] for r in cyc]
        paired = set()
        helper_pairs = []
        for i, value in enumerate(q):
            j = (i+1) % len(q)
            if value >= 3 and q[j] <= 1:
                assert i not in paired and j not in paired
                paired.update((i, j))
                helper_pairs.append(dict(high=i, helper=j, q_high=value, q_helper=q[j],
                    residual_upper_bound=max(value+q[j]-4, 0)))
        G = sum(max(value-2, 0) for value in q)
        J = sum(p['residual_upper_bound'] for p in helper_pairs) + sum(max(v-2, 0) for i, v in enumerate(q) if i not in paired)
        period = end-start
        recurrent = dict(transient_laps=start, period_laps=period, source_start=15*start,
            source_end=15*end, source_B=cyc[0]['source_B'], length=len(cyc),
            q_profile=q, d_profile=[r['d_B'] for r in cyc],
            Q_B=sum(q), Z_B=sum(r['z'] for r in cyc), G_B=G, J_B=J,
            immediate_helper_pairs=helper_pairs, two_effective_resets_capacity=4*period,
            budget_passes=G>4*period)
        outcome = ('B_BUDGET_BLOCKED' if G <= 4*period else
            ('B_PERIOD_EXCLUDES_ONE_WORD_TWO_RESET_CYCLE' if period != 1 else 'B_GATE_PASSES_A_CLASS_AUTHORIZED'))
    cert = dict(schema='alternating-extreme-B-preflight-v1', date='2026-10-31', word=WORD,
        key_size=13, initial_diagonal=raw(initial), cap=CAP, full_B_replay=rows,
        boundary_records=boundaries, recurrent_B=recurrent, outcome=outcome,
        declared_gap_pairs=105, A_policy_cases_executed=0, word_replacements=0,
        larger_finite_fits=0, FI_UD_cut_trials=0, matching_terminal_line='FROZEN', universal_CD='OPEN')
    save('B_preflight_certificate.json', cert)
    print(json.dumps(dict(outcome=outcome, preserved_files=len(pins), stage_files=len(stage),
        B_source_calls=len(rows), recurrent_B=recurrent, A_policy_cases_executed=0), indent=2))


if __name__ == '__main__':
    main()
