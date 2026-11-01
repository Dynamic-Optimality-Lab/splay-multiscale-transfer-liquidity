"""Independent pointer replay and exact structural-certificate checks; no search."""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
WORD = [13, 11, 9] + list(range(1, 13)) + list(range(11, 0, -1))


def ck(ok, message):
    if not ok:
        raise AssertionError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(name, value):
    with (HERE / name).open('x', encoding='utf-8') as f:
        json.dump(value, f, indent=2, ensure_ascii=False)
        f.write('\n')


def main():
    sp = HERE / 'spine_symbolic_certificate.json'
    cp = HERE / 'fixed_word_and_reset_control.json'
    sym = json.loads(sp.read_text(encoding='utf-8'))
    cert = json.loads(cp.read_text(encoding='utf-8'))
    spec = importlib.util.spec_from_file_location('pointer_source', ROOT / 'python/liquidity/legacy_embedding.py')
    p = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(p)

    def ptr(t):
        if t is None:
            return None
        z = p.mknode(t[0], ptr(t[1]), ptr(t[2]))
        for side in ('l', 'r'):
            if z[side] is not None:
                z[side]['p'] = z
        return z

    def raw(t):
        return None if t is None else [t['k'], raw(t['l']), raw(t['r'])]

    def mirror(t):
        return None if t is None else [14-t[0], mirror(t[2]), mirror(t[1])]

    def inorder(t):
        return [] if t is None else inorder(t[1]) + [t[0]] + inorder(t[2])

    def spine(t):
        out = []
        while t is not None:
            out.append(t[0])
            t = t[2]
        return out

    def depth(t, key):
        d = 0
        while t is not None:
            if t[0] == key:
                return d
            t = t[1] if key < t[0] else t[2]
            d += 1
        raise AssertionError('present source key')

    def events_mirror(ev):
        cm = {'LL': 'RR', 'RR': 'LL', 'LR': 'RL', 'RL': 'LR', 'ZIG': 'ZIG'}
        om = {'L': 'R', 'R': 'L', '-': '-'}
        return [[cm[e[0]], 14-e[2], 14-e[1], om[e[3]]] for e in ev]

    calls = trees = 0

    def access(t, key):
        nonlocal calls, trees
        ck(inorder(t) == list(range(1, 14)), 'exact source key set and strict BST')
        trees += 1
        d = depth(t, key)
        dest, ev = p.splay_trace(ptr(t), key)
        out = raw(dest)
        ck(inorder(out) == list(range(1, 14)), 'exact destination key set and strict BST')
        trees += 1
        events = [[e['case'], e['lo'], e['hi'], e['orient']] for e in ev]
        q, z = sum(e[0] != 'ZIG' for e in events), sum(e[0] == 'ZIG' for e in events)
        ck((q, z, len(ev)) == (d//2, d%2, (d+1)//2), 'grouped and elementary rotation counts')
        ck(all(y in spine(out) for y in spine(t) if y > key), 'right-spine retention at every audited normal/mirror access')
        ck(len(set(spine(t)) - set(spine(out))) <= 2*len(ev), 'right-spine deletion bounded by grouped capacity')
        calls += 1
        return out, d, events, q, z

    expected_tokens = {
        'LL': (['g', 'RS(D)'], ['x', 'p', 'g', 'RS(D)']),
        'RR': (['g', 'p', 'x', 'RS(D)'], ['x', 'RS(D)']),
        'LR': (['g', 'RS(D)'], ['x', 'g', 'RS(D)']),
        'RL': (['g', 'p', 'RS(D)'], ['x', 'p', 'RS(D)']),
        'ZIG_L': (['g', 'RS(C)'], ['x', 'g', 'RS(C)']),
        'ZIG_R': (['g', 'x', 'RS(C)'], ['x', 'RS(C)']),
    }

    def token_spine(t):
        return ['RS(' + t + ')'] if isinstance(t, str) else [t[0]] + token_spine(t[2])

    ck([r['case'] for r in sym['frames']] == list(expected_tokens), 'six exhaustive source frames')
    reflected_frames = []
    for r in sym['frames']:
        before, after = token_spine(r['before_template']), token_spine(r['after_template'])
        ck((before, after) == expected_tokens[r['case']], 'arbitrary-fringe symbolic right-spine table')
        ck(before == r['source_right_spine'] and after == r['destination_right_spine'], 'symbolic certificate tokens')
        pivots = r['pivot_keys']
        removed = [v for v in before if v not in after]
        ck(removed == r['removed_pivot_tokens'] and all(v in pivots and pivots[v] < pivots['x'] for v in removed),
            'only pivots below accessed x can leave the right spine')
        ck([v for v in before if v.startswith('RS(')] == [v for v in after if v.startswith('RS(')],
            'opaque fringe suffix retained identically')
        out, d, ev, q, z = access(r['source_B'], r['access_key'])
        ck((out, d, ev, q, z) == (r['destination_B'], r['d'], r['events'], r['q'], r['z']),
            'pointer source agrees with every instantiated frame rewrite')
        mout, md, mev, mq, mz = access(mirror(r['source_B']), 14-r['access_key'])
        ck((mout, md, mev, mq, mz) == (mirror(out), d, events_mirror(ev), q, z), 'source frame reflection')
        reflected_frames.append(dict(reflected_from=r['case'], source_B=mirror(r['source_B']),
            destination_B=mout, access_key=14-r['access_key'], d=md, events=mev, q=mq, z=mz))
    frame_calls = calls

    def bmirror(r):
        return dict(r, key=14-r['key'], source_B=mirror(r['source_B']),
            destination_B=mirror(r['destination_B']), B_events=events_mirror(r['B_events']))

    ck(cert['word'] == WORD and len(WORD) == 26, 'fixed original KEEP word')
    b, mb = cert['initial_diagonal'], mirror(cert['initial_diagonal'])
    normal_b, mirror_b = [], []
    for i, key in enumerate(WORD):
        before, mbefore = b, mb
        b, d, ev, q, z = access(b, key)
        mb, md, mev, mq, mz = access(mb, 14-key)
        row = dict(occurrence=i, key=key, source_B=before, destination_B=b,
            d_B=d, q=q, z=z, B_events=ev)
        mr = dict(occurrence=i, key=14-key, source_B=mbefore, destination_B=mb,
            d_B=md, q=mq, z=mz, B_events=mev)
        ck(row == cert['unchanged_B_cycle'][i] and mr == bmirror(row), 'unchanged B cycle and reflection')
        normal_b.append(row)
        mirror_b.append(mr)
    ck(b == cert['initial_diagonal'] and mb == mirror(b), 'normal and reflected B recurrence')
    ck(sum(max(r['q']-2, 0) for r in normal_b) == 5, 'complete raw excess budget')
    ck([i for i, r in enumerate(normal_b) if r['q'] >= 3] == [0, 1], 'only hot 13 and 11 can be positive')
    ck(normal_b[0]['d_B'] == 12 and normal_b[1]['d_B'] == 7, 'zero-pure-work diagonal hot A costs 6 and 4')
    b_calls = calls - frame_calls

    def cmirror(r):
        return dict(r, key=14-r['key'], source_A=mirror(r['source_A']), source_B=mirror(r['source_B']),
            destination_A=mirror(r['destination_A']), destination_B=mirror(r['destination_B']),
            A_events=events_mirror(r['A_events']), B_events=events_mirror(r['B_events']))

    policy = []
    for i, key in enumerate(WORD):
        policy.append(('KEEP', key))
        if i == 14:
            policy.extend([('DELETE', 13), ('DELETE', 12)])
    ck([(r['mode'], r['key']) for r in cert['control_rows']] == policy, 'one literal nonvacuity control')
    A = B = cert['initial_diagonal']
    mA = mB = mirror(A)
    normal_rows, mirror_rows = [], []
    for i, (mode, key) in enumerate(policy):
        preA, preB, mpreA, mpreB = A, B, mA, mB
        A, da, ea, qa, za = access(A, key)
        mA, mda, mea, mqa, mza = access(mA, 14-key)
        db, mdb = depth(B, key), depth(mB, 14-key)
        if mode == 'KEEP':
            B, _, eb, q, z = access(B, key)
            mB, _, meb, mq, mz = access(mB, 14-key)
        else:
            eb, q, z, meb, mq, mz = [], 0, 0, [], 0, 0
        row = dict(occurrence=i, mode=mode, key=key, source_A=preA, source_B=preB,
            destination_A=A, destination_B=B, d_A=da, d_B=db, a=len(ea), q=q, z=z,
            A_events=ea, B_events=eb, diagonal_before=preA == preB, diagonal_after=A == B)
        mr = dict(occurrence=i, mode=mode, key=14-key, source_A=mpreA, source_B=mpreB,
            destination_A=mA, destination_B=mB, d_A=mda, d_B=mdb, a=len(mea), q=mq, z=mz,
            A_events=mea, B_events=meb, diagonal_before=mpreA == mpreB, diagonal_after=mA == mB)
        ck(row == cert['control_rows'][i] and mr == cmirror(row), 'every paired-control input/output and event in both orientations')
        normal_rows.append(row)
        mirror_rows.append(mr)
    ck(A == B == cert['initial_diagonal'] and mA == mB == mirror(A), 'actual paired closure and diagonal reachability')
    blocks = []
    for r in normal_rows:
        if r['a']:
            blocks.append(dict(leader=r['occurrence'], key=r['key'], a=r['a'], occurrences=[], keeps=[], q=0))
        else:
            ck(blocks and blocks[-1]['key'] == r['key'], 'zero-A requests attach to their actual leader')
        block = blocks[-1]
        block['occurrences'].append(r['occurrence'])
        block['q'] += r['q']
        if r['mode'] == 'KEEP':
            block['keeps'].append(r['occurrence'])
    pure = [v for v in blocks if not v['keeps']]
    E = sum(max(v['q']-2*v['a'], 0) for v in blocks)
    CD = sum(2*v['a'] for v in pure)
    ck(blocks == cert['control_blocks'] and pure == cert['control_pure_blocks'], 'exact physical block decomposition')
    ck(len(pure) == 2 and all(v['a'] == 1 for v in pure), 'both resets are genuine pure one-StepEv blocks')
    ck((E, CD, sum(r['a'] for r in normal_rows), sum(r['q'] for r in normal_rows), sum(r['z'] for r in normal_rows)) ==
        (0, 4, 41, 20, 19), 'actual control costs, excess and capacity')
    ck(normal_rows[15]['mode'] == 'DELETE' and normal_rows[15]['key'] == 13 and
        normal_rows[16]['mode'] == 'DELETE' and normal_rows[16]['key'] == 12, 'fixed reset slots and keys')
    ck(normal_rows[14]['destination_A'] == normal_rows[16]['destination_A'], 'inverse reset zigs return A exactly')
    control_calls = calls - frame_calls - b_calls

    table = []
    for T in range(6):
        lower_depth = 12-2*T
        lower_a = max(1, (max(0, lower_depth)+1)//2)
        e13 = max(6-2*lower_a, 0)
        e11 = int(T != 0)
        ck(e13+e11 <= 2*T, 'complete finite integer branches of analytic bound')
        table.append(dict(pure_A_grouped_events=T, d_A13_lower_bound=lower_depth,
            a13_lower_bound=lower_a, e13_upper_bound=e13, e11_upper_bound=e11,
            E_cell_upper_bound=e13+e11, C_D_cell=2*T))
    ck(table == sym['integer_case_table'], 'independent integer proof branches')
    ck(sym['tail_case'] == dict(T_at_least=6, E_cell_at_most=5, C_D_cell_at_least=12), 'constant tail branch, not finite extrapolation')
    ck(sym['two_one_StepEv_reset_result'] == dict(T_total=2, C_D=4, a13_at_least=4,
        E_at_most=1, E_greater_than_C_D_possible=False), 'exact requested-coupling contradiction')
    ck(calls == 172 and trees == 344 and cert['tuple_source_accesses'] == 86, 'bounded complete source audit counts')
    save('reflected_source_certificate.json', dict(initial_diagonal=mirror(cert['initial_diagonal']),
        word=[14-key for key in WORD], reflected_frames=reflected_frames, B_cycle=mirror_b,
        control_rows=mirror_rows, control_E=0, control_C_D=4, paired_control_closed=True,
        spine_orientation='left spine and minimum key 1'))
    result = dict(status='PASS', date='2026-10-31', spine_certificate_sha256=sha(sp),
        paired_control_certificate_sha256=sha(cp), source_frame_cases=6, source_frame_pointer_calls=frame_calls,
        unchanged_B_pointer_calls=b_calls, paired_control_pointer_calls=control_calls,
        total_pointer_source_calls=calls, strict_BST_tree_occurrences=trees,
        arbitrary_fringe_symbolic_suffix_table_checked=True, all_retained_larger_spine_keys_checked=True,
        reflected_source_events_intervals_orientations_checked=True,
        control_pure_one_StepEv_resets=2, control_E=E, control_C_D=CD,
        requested_two_reset_E_at_most=1, requested_two_reset_C_D=4,
        requested_coupling='IMPOSSIBLE by analytic source obstruction',
        W_powers_arbitrary_A_insertions='E<=C_D by analytic cell proof',
        fixed_W_family_UD_coverage='inherited DELETE-only minimum-cut corollary',
        word_or_reset_policy_searches=0, larger_finite_fits=0, FI_UD_cut_trials=0,
        strict_FI_only_coverage='NOT ESTABLISHED', universal_CD='OPEN', matching_terminal_line='FROZEN')
    save('independent_audit.json', result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
