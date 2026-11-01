"""Independent pointer verification of the blocked B gate and reflection."""
import hashlib
import importlib.util
import itertools
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
WORD = [9, 5, 13, 3, 11, 7, 1, 2, 10, 6, 13, 4, 12, 8, 1]


def ck(ok, message):
    if not ok:
        raise AssertionError(message)


def save(name, value):
    with (HERE / name).open('x', encoding='utf-8') as f:
        json.dump(value, f, indent=2, ensure_ascii=False)
        f.write('\n')


def main():
    cp = HERE / 'B_preflight_certificate.json'
    cert = json.loads(cp.read_text(encoding='utf-8'))
    ck(cert['word'] == WORD and cert['cap'] == 64 and cert['key_size'] == 13, 'fixed gate parameters')
    ck(cert['outcome'] == 'B_BUDGET_BLOCKED', 'stop before A policies')
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

    def depth(t, key):
        d = 0
        while t is not None:
            if t[0] == key:
                return d
            t = t[1] if key < t[0] else t[2]
            d += 1
        raise AssertionError('present source key')

    def mirror_events(ev):
        cm = {'LL': 'RR', 'RR': 'LL', 'LR': 'RL', 'RL': 'LR', 'ZIG': 'ZIG'}
        om = {'L': 'R', 'R': 'L', '-': '-'}
        return [[cm[e[0]], 14-e[2], 14-e[1], om[e[3]]] for e in ev]

    def mirror_row(r):
        return dict(r, key=14-r['key'], source_B=mirror(r['source_B']),
            destination_B=mirror(r['destination_B']), B_events=mirror_events(r['B_events']))

    calls = trees = 0

    def access(t, key, i):
        nonlocal calls, trees
        ck(inorder(t) == list(range(1, 14)), 'exact source keys and strict BST')
        trees += 1
        d = depth(t, key)
        out, events = p.splay_trace(ptr(t), key)
        dest = raw(out)
        ck(inorder(dest) == list(range(1, 14)), 'exact destination keys and strict BST')
        trees += 1
        ev = [[e['case'], e['lo'], e['hi'], e['orient']] for e in events]
        q, z = sum(e[0] != 'ZIG' for e in ev), sum(e[0] == 'ZIG' for e in ev)
        ck((q, z, len(ev)) == (d//2, d%2, (d+1)//2), 'grouped source events')
        calls += 1
        return dest, dict(occurrence=i, lap=i//15, word_position=i % 15, key=key,
            source_B=t, destination_B=dest, d_B=d, q=q, z=z, B_events=ev)

    initial = None
    for key in range(13, 0, -1):
        initial = [key, None, initial]
    ck(cert['initial_diagonal'] == initial, 'literal R13 diagonal and no setup')
    b, mb = initial, mirror(initial)
    seen = [b]
    boundaries = [dict(lap=0, B=b)]
    rows, mrows = [], []
    start = end = None
    for lap in range(1, 65):
        for key in WORD:
            i = len(rows)
            b, r = access(b, key, i)
            mb, mr = access(mb, 14-key, i)
            ck(r == cert['full_B_replay'][i], 'all tuple/pointer events, source and destination trees')
            ck(mr == mirror_row(r), 'every reflected source tree, interval and orientation')
            rows.append(r)
            mrows.append(mr)
        boundaries.append(dict(lap=lap, B=b))
        if b in seen:
            start, end = seen.index(b), lap
            break
        seen.append(b)
    ck((start, end) == (1, 2), 'first exact boundary recurrence, one transient and one period')
    ck(boundaries == cert['boundary_records'] and len(rows) == 30, 'complete orbit provenance')
    cyc = rows[15:30]
    q = [r['q'] for r in cyc]
    ck(q == [2, 3, 1, 2, 3, 3, 1, 1, 2, 2, 1, 2, 2, 3, 1], 'complete recurrent q profile')
    ck(cyc[0]['source_B'] == cyc[-1]['destination_B'], 'true recurrent B closure')
    used = set()
    pairs = []
    for i, value in enumerate(q):
        j = (i+1) % 15
        if value >= 3 and q[j] <= 1:
            ck(i not in used and j not in used, 'disjoint physical high/low cells')
            used.update((i, j))
            pairs.append(dict(high=i, helper=j, q_high=value, q_helper=q[j],
                residual_upper_bound=max(value+q[j]-4, 0)))
    G = sum(max(value-2, 0) for value in q)
    J = sum(v['residual_upper_bound'] for v in pairs) + sum(max(value-2, 0) for i, value in enumerate(q) if i not in used)
    recurrent = dict(transient_laps=1, period_laps=1, source_start=15, source_end=30,
        source_B=cyc[0]['source_B'], length=15, q_profile=q,
        d_profile=[r['d_B'] for r in cyc], Q_B=sum(q), Z_B=sum(r['z'] for r in cyc),
        G_B=G, J_B=J, immediate_helper_pairs=pairs, two_effective_resets_capacity=4,
        budget_passes=G>4)
    ck(recurrent == cert['recurrent_B'] and (G, J, sum(q), sum(r['z'] for r in cyc)) == (4, 1, 29, 12),
        'exact G, J, Q and Z preflight')
    ck(cert['A_policy_cases_executed'] == 0 and cert['declared_gap_pairs'] == 105,
        'no unauthorized A continuation after blocked gate')
    gap_pairs = [list(pair) for pair in itertools.combinations(range(15), 2)]
    ck(len(gap_pairs) == 105 and len({tuple(pair) for pair in gap_pairs}) == 105, 'complete declared slot domain')
    save('budget_exclusion_certificate.json', dict(schema='exact-source-budget-exclusion-v1',
        status='PASS', domain='the certified reachable recurrent B orbit and declared two-slot policies',
        B_preflight_sha256=hashlib.sha256(cp.read_bytes()).hexdigest(),
        gap_pairs=gap_pairs, policies_executed=0, policies_excluded_by_budget=105,
        per_word_G_B=4, two_effective_pure_one_StepEv_resets_C_D=4,
        E_upper_bound=4, E_greater_than_C_D_possible=False,
        repeated_policy_laps=dict(p='any positive integer', E_at_most='4p', C_D='4p'),
        other_B_orbits_or_RESET_distributions='NOT CLASSIFIED', no_A_state_or_unit_assignment_assumed=True))
    save('reflected_B_certificate.json', dict(initial_diagonal=mirror(initial), word=[14-key for key in WORD],
        full_B_replay=mrows, transient_laps=1, period_laps=1, Q_B=29, Z_B=12, G_B=4, J_B=1))
    result = dict(status='PASS', date='2026-10-31', B_preflight_sha256=hashlib.sha256(cp.read_bytes()).hexdigest(),
        tuple_B_calls=30, pointer_B_calls=calls, strict_BST_tree_occurrences=trees,
        transient_laps=1, recurrent_period_laps=1, recurrent_Q_B=29, recurrent_Z_B=12,
        recurrent_G_B=G, recurrent_J_B=J, distinct_recurrent_B_sources=len({json.dumps(r['source_B']) for r in cyc}),
        declared_two_slot_policies=105, A_policy_cases_executed=0,
        all_declared_effective_policies_budget_excluded=True, requested_cycle='NOT FOUND',
        larger_finite_fits=0, word_replacements=0, FI_UD_cut_trials=0,
        universal_two_reset_cycle_nonexistence_claimed=False, strict_FI_only_coverage='NOT ESTABLISHED',
        universal_CD='OPEN', matching_terminal_line='FROZEN')
    save('independent_audit.json', result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
