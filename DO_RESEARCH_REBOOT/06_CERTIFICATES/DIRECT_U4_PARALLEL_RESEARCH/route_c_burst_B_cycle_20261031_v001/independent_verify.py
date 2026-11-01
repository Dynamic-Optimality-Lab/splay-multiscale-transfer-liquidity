"""Independent pointer-source replay, reflection and UD historical-ceiling audit."""
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


def save(name, value):
    with (HERE / name).open('x', encoding='utf-8') as f:
        json.dump(value, f, indent=2, ensure_ascii=False)
        f.write('\n')


def main():
    certpath = HERE / 'burst_B_cycle_certificate.json'
    cert = json.loads(certpath.read_text(encoding='utf-8'))
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
        return None if t is None else [14 - t[0], mirror(t[2]), mirror(t[1])]

    def vine(lo, hi):
        t = None
        for key in range(hi, lo - 1, -1):
            t = [key, None, t]
        return t

    def left(lo, hi):
        t = None
        for key in range(lo, hi + 1):
            t = [key, t, None]
        return t

    def inorder(t):
        return [] if t is None else inorder(t[1]) + [t[0]] + inorder(t[2])

    def depth(t, key):
        d = 0
        while t is not None:
            if t[0] == key:
                return d
            t = t[1] if key < t[0] else t[2]
            d += 1
        raise AssertionError('key must be present')

    def subtree(t, key):
        while t is not None:
            if t[0] == key:
                return t
            t = t[1] if key < t[0] else t[2]
        raise AssertionError('subtree root must exist')

    calls = trees = 0

    def access(t, key, i):
        nonlocal calls, trees
        ck(inorder(t) == list(range(1, 14)), 'strict source BST and all keys')
        trees += 1
        d = depth(t, key)
        out, ev = p.splay_trace(ptr(t), key)
        result = raw(out)
        ck(inorder(result) == list(range(1, 14)), 'strict destination BST and all keys')
        trees += 1
        events = [[e['case'], e['lo'], e['hi'], e['orient']] for e in ev]
        q, z = sum(e[0] != 'ZIG' for e in events), sum(e[0] == 'ZIG' for e in events)
        ck((q, z, len(ev)) == (d // 2, d % 2, (d + 1) // 2), 'exact grouped events')
        calls += 1
        return result, dict(occurrence=i, key=key, source_B=t, destination_B=result,
            d_B=d, q=q, z=z, B_events=events)

    def reflected_row(r):
        cm = {'LL': 'RR', 'RR': 'LL', 'LR': 'RL', 'RL': 'LR', 'ZIG': 'ZIG'}
        om = {'L': 'R', 'R': 'L', '-': '-'}
        return dict(r, key=14-r['key'], source_B=mirror(r['source_B']),
            destination_B=mirror(r['destination_B']),
            B_events=[[cm[e[0]], 14-e[2], 14-e[1], om[e[3]]] for e in r['B_events']])

    ck(cert['word'] == WORD and len(WORD) == 26, 'fixed predeclared word')
    initial = vine(1, 13)
    b, mb = initial, mirror(initial)
    ck(cert['initial_diagonal_B'] == b, 'legal diagonal and no warmup')
    rows, mrows, checks = [], [], []
    for i, key in enumerate(WORD):
        b, r = access(b, key, i)
        mb, mr = access(mb, 14-key, i)
        ck(r == cert['full_cycle_replay'][i], 'every tuple/pointer tree and source event')
        ck(mr == reflected_row(r), 'every mirrored key, interval, case and zig orientation')
        rows.append(r)
        mrows.append(mr)
        if 3 <= i <= 14:
            ck(b[0] == key and b[1] == left(1, key-1), 'increasing scan left-vine invariant')
            intact = None
            if key < 12:
                intact = subtree(b, 13) == [13, [12, None, None], None]
                ck(intact, 'unrequested core fringe remains intact')
            checks.append(dict(occurrence=i, key=key, scanned_left_vine=True,
                unrequested_core_13_12_fringe_preserved=intact))
        if i >= 15:
            ck(b == [key, left(1, key-1), vine(key+1, 13)], 'descending scan exact shape')
            ck((r['d_B'], r['q'], r['z']) == (1, 0, 1), 'one root zig, not a B double')
    ck(b == initial and mb == mirror(initial), 'source closure in both orientations')
    ck(len({json.dumps(r['source_B']) for r in rows}) == 26, 'all 26 source states distinct')
    ck(len({json.dumps(r['source_B']) for r in mrows}) == 26, 'mirrored simplicity')
    ck(rows[14]['destination_B'] == [12, left(1, 11), [13, None, None]], 'exact turnaround T12')
    ck(checks == cert['increasing_scan_checkpoints'], 'independent scan checkpoints')
    ck([r['d_B'] for r in rows[:3]] == [12, 7, 4], 'hot source depths')
    ck([r['q'] for r in rows] == cert['q_profile'], 'full q profile')
    ck([r['z'] for r in rows] == cert['z_profile'], 'full zig profile')
    ck([r['d_B'] for r in rows] == cert['d_profile'], 'full depth profile')
    q = [r['q'] for r in rows]
    pairs = [(i, (i+1) % 26) for i in range(26) if q[i] >= 3 and q[(i+1) % 26] <= 1]
    G = sum(max(v-2, 0) for v in q)
    used = {i for pair in pairs for i in pair}
    J = sum(max(q[i]+q[j]-4, 0) for i, j in pairs) + sum(max(q[i]-2, 0) for i in range(26) if i not in used)
    ck(not pairs and cert['immediate_high_low_pairs'] == [], 'no immediate high/low payer')
    ck((sum(q), sum(r['z'] for r in rows), G, J) == (20, 19, 5, 5), 'Q, Z, G and J')
    ck((cert['Q_B'], cert['Z_B'], cert['G_B'], cert['J_B']) == (20, 19, 5, 5), 'reported exact budgets')
    ck(all(rows[i]['d_B'] > 0 and WORD[i] != WORD[(i+1) % 26] for i in range(26)),
        'every B access is a genuine change, including 15 zig-only accesses')
    potential = [i for i in range(26) if q[i] >= 3]
    ck(potential == [0, 1], 'complete potential-positive set')
    delayed = []
    oldroot_returns = []
    for i in potential:
        source = rows[i]['source_B']
        collar = [source[0]] + [t[0] for t in source[1:] if t is not None]
        nxt = (i+1) % 26
        ck(WORD[nxt] not in collar and q[nxt] >= 2, 'no surplus-bearing root/collar return')
        for sep in range(1, 26):
            j = (i+sep) % 26
            k = sum(rows[(i+h) % 26]['d_B'] > 0 for h in range(1, sep))
            h = depth(rows[i]['destination_B'], WORD[j])
            c = h // 2 + k
            if q[j] <= 2:
                delayed.append(dict(anchor_occurrence=i, anchor_key=WORD[i], payer_occurrence=j,
                    payer_key=WORD[j], payer_q=q[j], forward_cyclic_separation=sep,
                    post_anchor_source_depth=h, genuine_intervening_B_changes=k,
                    UD_own_work_ceiling=c, guaranteed_spare_from_minimum_two_unit_pool=max(2-c, 0)))
        sep = next(h for h in range(1, 27) if WORD[(i+h) % 26] == source[0])
        j = (i+sep) % 26
        h = depth(rows[i]['destination_B'], source[0])
        oldroot_returns.append(dict(anchor_occurrence=i, anchor_key=WORD[i], old_B_root=source[0],
            return_occurrence=j, return_key=WORD[j], forward_cyclic_separation=sep,
            return_q=q[j], post_anchor_old_root_depth=h,
            genuine_intervening_B_changes=sep-1, UD_own_work_ceiling=h//2+sep-1))
    ck(len(delayed) == 48, 'all two times 24 nonpositive-potential source pairs')
    no_minimum_spare = all(v['UD_own_work_ceiling'] >= 2 for v in delayed)
    summary = {str(i): dict(entries=sum(v['anchor_occurrence'] == i for v in delayed),
        minimum_ceiling=min(v['UD_own_work_ceiling'] for v in delayed if v['anchor_occurrence'] == i))
        for i in potential}
    save('delayed_UD_ceiling_profile.json', dict(schema='historical-UD-source-ceilings-v1',
        status='FINITE-EXACT', full_period_length=26, potential_positive_anchors=potential,
        no_guaranteed_minimum_two_unit_pool_spare=no_minimum_spare,
        anchor_summary=summary, entries=delayed, first_old_root_returns=oldroot_returns,
        previous_period_facts_add_positive_full_period_delay=True,
        actual_A_costs_assumed=False, actual_UD_all_cut_rejection_claimed=False,
        reflection_verified_by_exact_source_symmetry=True))
    save('reflected_cycle_certificate.json', dict(initial_diagonal_B=mirror(initial),
        word=[14-key for key in WORD], full_cycle_replay=mrows, simple=True,
        Q_B=20, Z_B=19, G_B=5, J_B=5, reachability_prefix_length=0))
    ck(cert['finite_fits'] == cert['size_sweeps'] == cert['adaptive_generator_changes'] ==
        cert['A_resets_executed'] == cert['FI_UD_cut_trials'] == 0, 'bounded scope')
    ck(cert['matching_terminal_line'] == 'FROZEN' and cert['universal_CD'] == 'OPEN' and
        cert['actual_E_or_C_D_certified'] is False, 'no hidden paired claim')
    result = dict(status='PASS', date='2026-10-31', source_exact_recurrent_B_component='CERTIFIED',
        certificate_sha256=hashlib.sha256(certpath.read_bytes()).hexdigest(),
        key_size=13, length=26, Q_B=20, Z_B=19, G_B=5, J_B=5, simple=True,
        tuple_pointer_rows_checked=26, reflected_pointer_rows_checked=26,
        pointer_source_accesses=calls, strict_BST_tree_occurrences_validated=trees,
        immediate_high_low_pairs=0, delayed_anchor_payer_entries=len(delayed),
        delayed_ceiling_summary=summary, first_old_root_returns=oldroot_returns,
        no_guaranteed_minimum_pool_UD_spare=no_minimum_spare,
        finite_fits=0, size_sweeps=0, A_resets_executed=0, FI_UD_cut_trials=0,
        actual_E_or_C_D_certified=False, all_cut_UD_rejection='NOT ESTABLISHED',
        strict_FI_only_closed_walk_coverage='NOT ESTABLISHED', universal_CD='OPEN',
        matching_terminal_line='FROZEN')
    save('independent_audit.json', result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
