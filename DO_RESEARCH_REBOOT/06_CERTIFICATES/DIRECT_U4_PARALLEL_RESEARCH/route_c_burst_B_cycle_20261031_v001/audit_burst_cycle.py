"""One gated 13-key burst/restoration cycle; exact tuple source, no search."""
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OLD = HERE.parent / 'route_c_guarded_B_cycle_20261031_v001'
STAGE = ROOT / 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'
WORD = [13, 11, 9] + list(range(1, 13)) + list(range(11, 0, -1))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(name, value):
    with (HERE / name).open('x', encoding='utf-8') as f:
        json.dump(value, f, indent=2, ensure_ascii=False)
        f.write('\n')


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def main():
    inherited = json.loads((OLD / 'entry_source_pins.json').read_text(encoding='utf-8'))
    pins = dict(inherited['files'])
    for rel, digest in pins.items():
        assert sha(ROOT / rel) == digest, rel
    for path in HERE.parent.rglob('*'):
        if path.is_file() and HERE not in path.parents:
            pins[path.relative_to(ROOT).as_posix()] = sha(path)
    stage = {p.relative_to(STAGE).as_posix(): sha(p) for p in STAGE.rglob('*') if p.is_file()}
    assert stage == inherited['stage_files'] and len(stage) == 125
    assert not git('status', '--porcelain=v1', '--untracked-files=no')
    assert git('rev-parse', 'HEAD') == inherited['head']
    assert git('branch', '--show-current') == inherited['branch']
    save('entry_source_pins.json', dict(date='2026-10-31', head=git('rev-parse', 'HEAD'),
        branch=git('branch', '--show-current'), tracked_status='', files=pins,
        stage_files=stage, inherited_pins=len(inherited['files']),
        gate_sha256=sha(HERE / 'BC00_FOUR_RULE_GATE.md')))

    spec = importlib.util.spec_from_file_location('tuple_source', ROOT / 'python/independent/splay.py')
    s = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(s)
    L = s.LEAF

    def raw(t):
        return None if t == L else [t[1], raw(t[2]), raw(t[3])]

    def left_vine(keys):
        t = L
        for key in keys:
            t = s.node(key, t, L)
        return t

    def find(t, key):
        while t != L:
            if t[1] == key:
                return t
            t = t[2] if key < t[1] else t[3]
        raise AssertionError('present source key')

    def row(t, x, i):
        assert s.is_valid(t) and s.inorder(t) == list(range(1, 14))
        found, d = s.lookup(t, x)
        assert found
        after, events = s.trace(t, x)
        q = sum(e[0] != 'ZIG' for e in events)
        z = sum(e[0] == 'ZIG' for e in events)
        assert (q, z, len(events)) == (d // 2, d % 2, (d + 1) // 2)
        assert s.is_valid(after) and s.inorder(after) == list(range(1, 14))
        return after, dict(occurrence=i, key=x, source_B=raw(t), destination_B=raw(after),
            d_B=d, q=q, z=z, B_events=events)

    initial = s.vine(13)
    b = initial
    states = [b]
    rows = []
    scan_checks = []
    for i, x in enumerate(WORD):
        b, r = row(b, x, i)
        rows.append(r)
        states.append(b)
        if 3 <= i <= 14:
            assert b[1] == x and b[2] == left_vine(range(1, x))
            intact_fringe = None
            if x < 12:
                intact_fringe = find(b, 13) == s.node(13, s.node(12, L, L), L)
                assert intact_fringe
            scan_checks.append(dict(occurrence=i, key=x, scanned_left_vine=True,
                unrequested_core_13_12_fringe_preserved=intact_fringe))
        if i >= 15:
            expected_right = s.vine(13)
            expected_right = find(expected_right, x + 1)
            assert b == s.node(x, left_vine(range(1, x)), expected_right)
            assert (r['d_B'], r['q'], r['z']) == (1, 0, 1)
    closed = b == initial
    distinct = len(set(states[:-1]))
    assert closed and distinct == len(WORD) == 26
    assert [r['d_B'] for r in rows[:3]] == [12, 7, 4]
    assert [r['q'] for r in rows[:3]] == [6, 3, 2]
    t12 = s.node(12, left_vine(range(1, 12)), s.node(13, L, L))
    assert states[15] == t12

    q = [r['q'] for r in rows]
    pairs = []
    covered = set()
    for i in range(26):
        j = (i + 1) % 26
        assert WORD[i] != WORD[j]
        if q[i] >= 3 and q[j] <= 1:
            assert i not in covered and j not in covered
            covered.update((i, j))
            pairs.append(dict(high=i, helper=j, q_high=q[i], q_helper=q[j],
                residual_upper_bound=max(q[i] + q[j] - 4, 0)))
    singletons = [dict(occurrence=i, q=q[i], residual_upper_bound=max(q[i] - 2, 0))
        for i in range(26) if i not in covered]
    G = sum(max(v - 2, 0) for v in q)
    J = sum(p['residual_upper_bound'] for p in pairs) + sum(p['residual_upper_bound'] for p in singletons)
    protected = []
    for i, r in enumerate(rows):
        if r['q'] < 3:
            continue
        j = (i + 1) % 26
        source = states[i]
        collar = [source[1]] + [t[1] for t in source[2:] if t != L]
        record = dict(occurrence=i, key=r['key'], q=r['q'], raw_surplus=r['q'] - 2,
            previous_B_root=source[1], previous_B_root_and_children=collar,
            successor_occurrence=j, successor_key=WORD[j], successor_q=q[j],
            successor_returns_to_previous_B_root=WORD[j] == source[1],
            successor_in_previous_root_collar=WORD[j] in collar,
            fresh_UD_own_work_ceiling=q[j], guaranteed_spare_from_minimum_two_unit_pool=max(2 - q[j], 0))
        assert not record['successor_returns_to_previous_B_root']
        assert not record['successor_in_previous_root_collar'] and q[j] >= 2
        protected.append(record)
    assert G >= 5 and J >= 5 and not pairs
    assert (G, J, sum(q), sum(r['z'] for r in rows)) == (5, 5, 20, 19)
    cert = dict(schema='burst-restoration-source-cycle-v1', date='2026-10-31', key_size=13,
        word=WORD, initial_diagonal_B=raw(initial), full_cycle_replay=rows,
        increasing_scan_checkpoints=scan_checks, increasing_scan_terminal_B=raw(t12),
        closed=True, simple=True, distinct_source_states=distinct, reachability_prefix_length=0,
        Q_B=sum(q), Z_B=sum(r['z'] for r in rows), G_B=G, J_B=J,
        q_profile=q, d_profile=[r['d_B'] for r in rows], z_profile=[r['z'] for r in rows],
        immediate_high_low_pairs=pairs, residual_singleton_cells=singletons,
        protected_surplus_bursts=protected, threshold=5, planned_pure_reset_capacity=4,
        outcome='B_COMPONENT_AND_IMMEDIATE_HELPER_GATE_CERTIFIED',
        source_paths=['python/independent/splay.py', 'python/liquidity/legacy_embedding.py'],
        finite_fits=0, size_sweeps=0, adaptive_generator_changes=0, A_resets_executed=0,
        FI_UD_cut_trials=0, actual_E_or_C_D_certified=False, delayed_UD_coverage='OPEN',
        strict_FI_only_closed_walk_coverage='NOT ESTABLISHED', universal_CD='OPEN',
        matching_terminal_line='FROZEN')
    save('burst_B_cycle_certificate.json', cert)
    print(json.dumps(dict(preserved_files=len(pins), stage_files=len(stage), outcome=cert['outcome'],
        length=26, Q_B=cert['Q_B'], Z_B=cert['Z_B'], G_B=G, J_B=J, q_profile=q,
        simple=True, automatic_high_low_pairs=pairs, protected_surplus_bursts=protected), indent=2))


if __name__ == '__main__':
    main()
