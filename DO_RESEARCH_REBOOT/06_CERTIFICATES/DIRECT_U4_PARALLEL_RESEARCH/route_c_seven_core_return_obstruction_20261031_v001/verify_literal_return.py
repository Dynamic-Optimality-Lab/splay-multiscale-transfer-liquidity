"""Compose one explicit failure-control return from the already verified table."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(name, value):
    with (HERE / name).open('x', encoding='utf-8') as f:
        json.dump(value, f, indent=2, ensure_ascii=False)
        f.write('\n')


def main():
    table = json.loads((HERE / 'source_transition_table.json').read_text(encoding='utf-8'))
    audit = json.loads((HERE / 'independent_audit.json').read_text(encoding='utf-8'))
    assert audit['status'] == 'PASS' and audit['source_table_sha256'] == sha(HERE / 'source_transition_table.json')
    cores, trans, F = table['cores'], table['transitions'], table['fringe']

    def embed(t):
        return None if t is None else [t[0], embed(t[1]), F if t[0] == 7 else embed(t[2])]

    def mirror(t):
        return None if t is None else [14-t[0], mirror(t[2]), mirror(t[1])]

    def mev(events):
        cm = {'LL': 'RR', 'RR': 'LL', 'LR': 'RL', 'RL': 'LR', 'ZIG': 'ZIG'}
        om = {'L': 'R', 'R': 'L', '-': '-'}
        return [[cm[e[0]], 14-e[2], 14-e[1], om[e[3]]] for e in events]

    initial = None
    for key in range(7, 0, -1):
        initial = [key, None, initial]
    start = cores.index(initial)
    A = B = start
    tail = [6, 5, 3, 7, 1, 4]
    ret = [2, 6, 4, 1, 3, 2, 5, 4, 2, 1]
    word = [('DELETE', 3), ('DELETE', 5), ('KEEP', 7)] + [('KEEP', x) for x in tail+ret]
    rows, mrows = [], []
    for occurrence, (mode, key) in enumerate(word):
        ar = trans[7*A+key-1]
        br = trans[7*B+key-1] if mode == 'KEEP' else None
        nextA = ar['target']
        nextB = br['target'] if br else B
        q = br['q'] if br else 0
        row = dict(occurrence=occurrence, mode=mode, key=key,
            source_A=embed(cores[A]), source_B=embed(cores[B]),
            destination_A=embed(cores[nextA]), destination_B=embed(cores[nextB]),
            d_A=ar['depth'], a=ar['a'], A_events=ar['events'],
            d_B=br['depth'] if br else None, q=q, z=br['z'] if br else 0,
            B_events=br['events'] if br else [], delta=q-2*ar['a'],
            diagonal_before=A == B, diagonal_after=nextA == nextB)
        assert row['a'] > 0
        mr = dict(row, key=14-key, source_A=mirror(row['source_A']), source_B=mirror(row['source_B']),
            destination_A=mirror(row['destination_A']), destination_B=mirror(row['destination_B']),
            A_events=mev(row['A_events']), B_events=mev(row['B_events']))
        rows.append(row)
        mrows.append(mr)
        A, B = nextA, nextB
    assert A == B == start
    assert all(rows[i]['key'] != rows[(i+1) % len(rows)]['key'] for i in range(len(rows)))
    assert len(rows) == 19 and sum(r['mode'] == 'DELETE' for r in rows) == 2
    assert all(r['a'] == 1 for r in rows if r['mode'] == 'DELETE')
    E = sum(max(r['delta'], 0) for r in rows)
    CD = sum(2*r['a'] for r in rows if r['mode'] == 'DELETE')
    kept = [r for r in rows if r['mode'] == 'KEEP']
    q = [r['q'] for r in kept]
    used, pairs = set(), []
    for i, value in enumerate(q):
        j = (i+1) % len(q)
        if value >= 3 and q[j] <= 1:
            assert i not in used and j not in used
            used.update((i, j))
            pairs.append(dict(high_KEEP=i, helper_KEEP=j, q_high=value, q_helper=q[j],
                residual_upper_bound=max(value+q[j]-4, 0)))
    G = sum(max(value-2, 0) for value in q)
    J = sum(v['residual_upper_bound'] for v in pairs) + sum(max(value-2, 0) for i, value in enumerate(q) if i not in used)
    def has_full_core_scan(keys):
        asc = list(range(1, 8))
        return any((keys+keys)[i:i+7] in (asc, asc[::-1]) for i in range(len(keys)))
    assert not has_full_core_scan([r['key'] for r in rows])
    assert not has_full_core_scan([r['key'] for r in kept])
    assert (E, CD, G, J) == (2, 4, 2, 0)
    result = dict(status='PASS', verification='composition of independently verified complete source table; no new engine calls',
        source_table_sha256=sha(HERE / 'source_transition_table.json'),
        source_audit_sha256=sha(HERE / 'independent_audit.json'), initial_diagonal=embed(initial),
        word=[dict(mode=m, key=k) for m, k in word], KEEP_amplification_tail=tail, KEEP_return_word=ret,
        replay=rows, mirrored_replay=mrows, paired_closed=True, source_actions=19, physical_resets=2,
        resets_one_StepEv=True, all_blocks_have_distinct_positive_leaders=True,
        A=sum(r['a'] for r in rows), Q_B=sum(q), Z_B=sum(r['z'] for r in kept),
        E=E, C_D=CD, G_B=G, J_B=J, q_profile=q, helper_pairs=pairs,
        positive_source_occurrences=[r['occurrence'] for r in rows if r['delta'] > 0],
        diagonal_source_occurrences=[r['occurrence'] for r in rows if r['diagonal_before']],
        distinct_source_pairs=len({json.dumps([r['source_A'], r['source_B']]) for r in rows}),
        full_core_consecutive_scan=False, requested_high_threshold_identity=False,
        maximum_possible_amplification_claimed=False, additional_engine_calls=0,
        new_word_classes=0, new_searches=0, matching_terminal_line='FROZEN', universal_CD='OPEN')
    save('literal_return_certificate.json', result)
    print(json.dumps({k:result[k] for k in ['status', 'paired_closed', 'source_actions', 'physical_resets',
        'A', 'Q_B', 'Z_B', 'E', 'C_D', 'G_B', 'J_B', 'positive_source_occurrences',
        'diagonal_source_occurrences', 'distinct_source_pairs', 'full_core_consecutive_scan', 'additional_engine_calls']}, indent=2))


if __name__ == '__main__':
    main()
