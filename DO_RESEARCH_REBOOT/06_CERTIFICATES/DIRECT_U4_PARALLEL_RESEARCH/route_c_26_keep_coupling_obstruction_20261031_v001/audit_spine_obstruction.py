"""Source-frame spine identities and the fixed 26-KEEP coupling obstruction."""
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OLD = HERE.parent / 'route_c_burst_B_cycle_20261031_v001'
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


def n(key, left, right):
    return [key, left, right]


def templates():
    return [
        ('LL', n('g', n('p', n('x', 'A', 'B'), 'C'), 'D'),
         n('x', 'A', n('p', 'B', n('g', 'C', 'D'))), {'g': 10, 'p': 7, 'x': 3}, 2, '-'),
        ('RR', n('g', 'A', n('p', 'B', n('x', 'C', 'D'))),
         n('x', n('p', n('g', 'A', 'B'), 'C'), 'D'), {'g': 3, 'p': 7, 'x': 10}, 2, '-'),
        ('LR', n('g', n('p', 'A', n('x', 'B', 'C')), 'D'),
         n('x', n('p', 'A', 'B'), n('g', 'C', 'D')), {'g': 10, 'p': 3, 'x': 7}, 2, '-'),
        ('RL', n('g', 'A', n('p', n('x', 'B', 'C'), 'D')),
         n('x', n('g', 'A', 'B'), n('p', 'C', 'D')), {'g': 3, 'p': 10, 'x': 7}, 2, '-'),
        ('ZIG_L', n('g', n('x', 'A', 'B'), 'C'),
         n('x', 'A', n('g', 'B', 'C')), {'g': 7, 'x': 3}, 1, 'L'),
        ('ZIG_R', n('g', 'A', n('x', 'B', 'C')),
         n('x', n('g', 'A', 'B'), 'C'), {'g': 3, 'x': 7}, 1, 'R'),
    ]


def symbolic_spine(t):
    return ['RS(' + t + ')'] if isinstance(t, str) else [t[0]] + symbolic_spine(t[2])


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
    assert (git('rev-parse', 'HEAD'), git('branch', '--show-current')) == (inherited['head'], inherited['branch'])
    save('entry_source_pins.json', dict(date='2026-10-31', head=inherited['head'], branch=inherited['branch'],
        tracked_status='', files=pins, stage_files=stage, inherited_pins=len(inherited['files']),
        gate_sha256=sha(HERE / 'AC00_FOUR_RULE_GATE.md')))

    spec = importlib.util.spec_from_file_location('tuple_source', ROOT / 'python/independent/splay.py')
    s = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(s)
    L = s.LEAF
    calls = 0

    def raw(t):
        return None if t == L else [t[1], raw(t[2]), raw(t[3])]

    def access(t, key):
        nonlocal calls
        assert s.is_valid(t) and s.inorder(t) == list(range(1, 14))
        found, d = s.lookup(t, key)
        assert found
        out, ev = s.trace(t, key)
        q, z = sum(e[0] != 'ZIG' for e in ev), sum(e[0] == 'ZIG' for e in ev)
        assert (q, z, len(ev)) == (d // 2, d % 2, (d + 1) // 2)
        assert s.is_valid(out) and s.inorder(out) == list(range(1, 14))
        calls += 1
        return out, d, ev, q, z

    def spine(t):
        out = []
        while t != L:
            out.append(t[1])
            t = t[3]
        return out

    frame_rows = []
    for case, before, after, ranks, rotations, orient in templates():
        b = symbolic_spine(before)
        a = symbolic_spine(after)
        removed = [key for key in b if key not in a]
        large = [key for key in b if key in ranks and ranks[key] > ranks['x']]
        assert all(key in a for key in large)
        assert all(key in ranks and ranks[key] < ranks['x'] for key in removed)
        assert [key for key in b if key.startswith('RS(')] == [key for key in a if key.startswith('RS(')]
        assert len(removed) <= rotations
        fringe_keys = {'A': [1, 2], 'B': [4, 5, 6], 'C': [8, 9], 'D': [11, 12, 13]}
        if case.startswith('ZIG'):
            fringe_keys['C'] = list(range(8, 14))
        fringes = {key: s.balanced(value) for key, value in fringe_keys.items()}

        def instantiate(t):
            if isinstance(t, str):
                return fringes[t]
            return s.node(ranks[t[0]], instantiate(t[1]), instantiate(t[2]))

        source, expected = instantiate(before), instantiate(after)
        dest, d, ev, q, z = access(source, ranks['x'])
        expected_case = 'ZIG' if case.startswith('ZIG') else case
        assert dest == expected and d == rotations and len(ev) == 1
        assert ev[0] == (expected_case, min(ranks.values()), max(ranks.values()), orient)
        assert all(y in spine(dest) for y in spine(source) if y > ranks['x'])
        frame_rows.append(dict(case=case, before_template=before, after_template=after, pivot_keys=ranks,
            source_right_spine=b, destination_right_spine=a, removed_pivot_tokens=removed,
            old_greater_pivots_retained=large, arbitrary_fringe_spine_suffix_unchanged=True,
            elementary_rotations=rotations, source_B=raw(source), destination_B=raw(dest),
            access_key=ranks['x'], d=d, events=ev, q=q, z=z))

    oldcert = json.loads((OLD / 'burst_B_cycle_certificate.json').read_text(encoding='utf-8'))
    assert oldcert['word'] == WORD and oldcert['G_B'] == 5
    b = s.vine(13)
    b_rows = []
    for i, key in enumerate(WORD):
        before = b
        b, d, ev, q, z = access(b, key)
        r = dict(occurrence=i, key=key, source_B=raw(before), destination_B=raw(b),
            d_B=d, q=q, z=z, B_events=ev)
        assert json.loads(json.dumps(r)) == oldcert['full_cycle_replay'][i]
        b_rows.append(r)
    assert b == s.vine(13)
    assert sum(max(r['q'] - 2, 0) for r in b_rows) == 5

    initial = s.vine(13)
    A = B = initial
    control = []

    def paired(mode, key):
        nonlocal A, B
        preA, preB = A, B
        A, da, ea, qa, za = access(A, key)
        db = s.lookup(B, key)[1]
        if mode == 'KEEP':
            B, _, eb, q, z = access(B, key)
        else:
            eb, q, z = [], 0, 0
        control.append(dict(occurrence=len(control), mode=mode, key=key,
            source_A=raw(preA), source_B=raw(preB), destination_A=raw(A), destination_B=raw(B),
            d_A=da, d_B=db, a=len(ea), q=q, z=z, A_events=ea, B_events=eb,
            diagonal_before=preA == preB, diagonal_after=A == B))

    for i, key in enumerate(WORD):
        paired('KEEP', key)
        if i == 14:
            assert key == 12
            paired('DELETE', 13)
            paired('DELETE', 12)
    assert A == B == initial and len(control) == 28
    blocks = []
    for r in control:
        if r['a'] > 0:
            blocks.append(dict(leader=r['occurrence'], key=r['key'], a=r['a'],
                occurrences=[], keeps=[], q=0))
        else:
            assert blocks and blocks[-1]['key'] == r['key']
        block = blocks[-1]
        block['occurrences'].append(r['occurrence'])
        block['q'] += r['q']
        if r['mode'] == 'KEEP':
            block['keeps'].append(r['occurrence'])
    E = sum(max(v['q'] - 2*v['a'], 0) for v in blocks)
    pure = [v for v in blocks if not v['keeps']]
    CD = sum(2*v['a'] for v in pure)
    assert len(pure) == 2 and all(v['a'] == 1 for v in pure)
    assert (E, CD, sum(r['a'] for r in control)) == (0, 4, 41)
    table = []
    for T in range(6):
        a13 = max(1, 6-T)
        e13 = max(6-2*a13, 0)
        e11 = 0 if T == 0 else 1
        upper = e13 + e11
        assert upper <= 2*T
        table.append(dict(pure_A_grouped_events=T, d_A13_lower_bound=12-2*T,
            a13_lower_bound=a13, e13_upper_bound=e13, e11_upper_bound=e11,
            E_cell_upper_bound=upper, C_D_cell=2*T))
    save('spine_symbolic_certificate.json', dict(schema='source-spine-coupling-obstruction-v1',
        date='2026-10-31', frames=frame_rows,
        symbolic_status='six source frame identities with arbitrary-fringe suffixes',
        global_right_rotation_removes_old_spine_vertices=0,
        global_left_rotation_removes_at_most_old_spine_vertices=1,
        per_splay_elementary_rotations='2*q+z <= 2*a',
        post_KEEP12_processed_spine_vertices=2, descending_KEEP_additions=11,
        hot_13_depth_lower_bound='12-2*T', integer_case_table=table,
        tail_case=dict(T_at_least=6, E_cell_at_most=5, C_D_cell_at_least=12),
        two_one_StepEv_reset_result=dict(T_total=2, C_D=4, a13_at_least=4, E_at_most=1,
            E_greater_than_C_D_possible=False),
        positive_powers_and_arbitrary_A_insertions='analytic cell proof: E<=C_D',
        requested_fixed_word_coupling='REFUTED—EXACT by source structural obstruction',
        actual_FI_UD_cut_trials=0, word_searches=0, larger_finite_fits=0))
    save('fixed_word_and_reset_control.json', dict(schema='source-paired-reset-control-v1',
        date='2026-10-31', word=WORD, key_size=13, old_B_certificate_sha256=sha(OLD / 'burst_B_cycle_certificate.json'),
        unchanged_B_cycle=b_rows, initial_diagonal=raw(initial), control_rows=control,
        control_blocks=blocks, control_pure_blocks=pure, control_E=E, control_C_D=CD,
        control_A=41, control_Q_B=20, control_Z_B=19, control_closed=True,
        control_role='nonvacuity only; not a candidate with E>C_D',
        tuple_source_accesses=calls, all_reset_positions_covered_by='analytic invariant, not enumeration',
        requested_coupling_exists=False, all_W_powers_UD_covered='analytic corollary of inherited minimum-cut lemma',
        strict_FI_only_coverage='NOT ESTABLISHED', universal_CD='OPEN', matching_terminal_line='FROZEN'))
    print(json.dumps(dict(preserved_files=len(pins), stage_files=len(stage), tuple_source_calls=calls,
        source_frame_cases=len(frame_rows), unchanged_B_rows=len(b_rows), paired_control_requests=len(control),
        control_E=E, control_C_D=CD, requested_two_reset_E_upper=1,
        requested_two_reset_C_D=4, fixed_word_and_powers='E<=C_D by analytic cell proof'), indent=2))


if __name__ == '__main__':
    main()
