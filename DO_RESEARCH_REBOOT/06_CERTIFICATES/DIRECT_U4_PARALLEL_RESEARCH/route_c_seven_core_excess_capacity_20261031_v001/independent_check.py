"""Independent exact graph and source-composition audit; imports no builder.

The source basis is the hash-pinned complete transition table, independently
executed in both tuple and pointer source engines in the preceding campaign.
This checker verifies composition and all claims, without new engine contexts.
"""
import hashlib
import json
import sys
from collections import Counter, deque
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OLD = HERE.parent / 'route_c_seven_core_return_obstruction_20261031_v001'
checks = Counter()


def ck(test, label):
    if not test:
        raise AssertionError(label)
    checks[label] += 1


def read(p):
    return json.loads(p.read_text(encoding='utf-8'))


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def save(name, data):
    with (HERE / name).open('x', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')


def main():
    entry = read(HERE / 'entry_source_pins.json')
    for rel, expected in entry['files'].items():
        ck(sha(ROOT / rel) == expected, 'preserved inherited file')
    table = read(OLD / 'source_transition_table.json')
    graph = read(OLD / 'reachable_relation_certificate.json')
    basis = read(OLD / 'independent_audit.json')
    cap = read(HERE / 'capacity_certificate.json')
    joint = read(HERE / 'joint_return_certificate.json')
    for record in [cap, joint]:
        ck(record['source_table_sha256'] == sha(OLD / 'source_transition_table.json'), 'table provenance')
        ck(record['source_relation_sha256'] == sha(OLD / 'reachable_relation_certificate.json'), 'relation provenance')
        ck(record['source_audit_sha256'] == sha(OLD / 'independent_audit.json'), 'pointer audit provenance')
    ck(joint['completion_gate_sha256'] == sha(HERE / 'EC00A_JOINT_COMPONENT_COMPLETION_GATE.md'), 'predeclared completion gate')
    ck(joint['capacity_sha256'] == sha(HERE / 'capacity_certificate.json'), 'capacity provenance')
    ck(basis['status'] == 'PASS' and basis['pointer_source_calls'] == 6038, 'source basis independently executed')
    ck(basis['source_table_sha256'] == sha(OLD / 'source_transition_table.json'), 'basis table pin')
    ck(basis['relation_sha256'] == sha(OLD / 'reachable_relation_certificate.json'), 'basis relation pin')
    ck(graph['queue_exhausted'] and not graph['state_cap_used'], 'old finite relation complete')
    trees, tt, fringe = table['cores'], table['transitions'], table['fringe']
    pp, ee = graph['pair_ids'], graph['outgoing_edges']
    pindex = {tuple(p): i for i, p in enumerate(pp)}
    labels = cap['component_labels']

    def transition(tree, key):
        return tt[tree*7+key-1]

    def embed(t):
        return None if t is None else [t[0], embed(t[1]), fringe if t[0] == 7 else embed(t[2])]

    def reflect(t):
        return None if t is None else [14-t[0], reflect(t[2]), reflect(t[1])]

    def reflect_events(events):
        cases = dict(LL='RR', RR='LL', LR='RL', RL='LR', ZIG='ZIG')
        orient = {'L': 'R', 'R': 'L', '-': '-'}
        return [[cases[kind], 14-hi, 14-lo, orient[o]] for kind, lo, hi, o in events]

    def inorder(t):
        return [] if t is None else inorder(t[1])+[t[0]]+inorder(t[2])

    def depth(t, key):
        d = 0
        while t[0] != key:
            t = t[1 if key < t[0] else 2]
            d += 1
        return d

    ck(len(trees) == 429 and len(tt) == 3003, 'fixed source basis dimensions')
    for i, t in enumerate(trees):
        ck(inorder(t) == list(range(1, 8)), 'core is strict BST')
        ck(inorder(embed(t)) == list(range(1, 14)), 'actual fringe embedding strict BST')
        ck(inorder(reflect(embed(t))) == list(range(1, 14)), 'reflected strict BST')
        for key in range(1, 8):
            tr = transition(i, key)
            ck((tr['source'], tr['key']) == (i, key), 'complete table row indexing')
            d = depth(t, key)
            ck((d, (d+1)//2, d//2, d % 2) == (tr['depth'], tr['a'], tr['q'], tr['z']), 'source cost conventions')
            ck(len(tr['events']) == tr['a'] and sum(ev[0] != 'ZIG' for ev in tr['events']) == tr['q'], 'grouped event accounting')
            ck(tr['mirror_key'] == 14-key and tr['mirror_events'] == reflect_events(tr['events']), 'all reflected source events')

    rev = [[] for _ in pp]
    internal_positive = []
    for s, (aid, bid) in enumerate(pp):
        ck(trees[aid][0] == trees[bid][0], 'common root state')
        expected = []
        if aid != bid:
            for key in range(1, 8):
                if key == trees[aid][0]:
                    continue
                ar, br = transition(aid, key), transition(bid, key)
                dest = pindex[(ar['target'], br['target'])]
                expected.append([key, dest, br['q']-2*ar['a']])
        ck(ee[s] == expected, 'all graph edges agree with source rows')
        for key, dest, delta in ee[s]:
            rev[dest].append(s)
            if delta > 0 and labels[s] == labels[dest]:
                internal_positive.append([s, key, dest, delta])
    ck(internal_positive == cap['internal_positive_edges'], 'positive internal edges complete')
    ck(len(pp) == 18450 and sum(map(len, ee)) == 109410, 'fixed relation dimensions')

    components = {}
    for s, c in enumerate(labels):
        components.setdefault(c, set()).add(s)
    condensed = {c: set() for c in components}
    for c, members in components.items():
        start = min(members)
        for reverse in [False, True]:
            seen, todo = {start}, [start]
            while todo:
                s = todo.pop()
                targets = rev[s] if reverse else [edge[1] for edge in ee[s]]
                for dest in targets:
                    if dest in members and dest not in seen:
                        seen.add(dest)
                        todo.append(dest)
            ck(seen == members, 'component strongly connected both directions')
        for s in members:
            for _, dest, _ in ee[s]:
                if labels[dest] != c:
                    condensed[c].add(labels[dest])
    indeg = {c: 0 for c in components}
    for values in condensed.values():
        for dest in values:
            indeg[dest] += 1
    todo = deque(c for c in indeg if not indeg[c])
    count = 0
    while todo:
        s = todo.popleft()
        count += 1
        for dest in condensed[s]:
            indeg[dest] -= 1
            if indeg[dest] == 0:
                todo.append(dest)
    ck(count == len(components) == cap['components'] == 218, 'component partition maximal via acyclic quotient')
    u = joint['entry_state']
    C = components[joint['component']]
    ck(u == 1871 and len(C) == joint['component_size'] == 18232, 'fixed selected component')
    ck(all(pp[s][0] != pp[s][1] for s in C), 'selected component off diagonal')

    def graph_path(edges, start, finish, inside=False):
        at = start
        for s, key, dest, weight in edges:
            ck(s == at and [key, dest, next(e[2] for e in ee[s] if e[0] == key)] in ee[s], 'literal graph path edges')
            ar, br = transition(pp[s][0], key), transition(pp[s][1], key)
            ck(dest == pindex[(ar['target'], br['target'])] and weight == max(br['q']-2*ar['a'], 0), 'literal source weighted edge')
            if inside:
                ck(s in C and dest in C, 'path stays in chosen component')
            at = dest
        ck(at == finish, 'literal path endpoint')

    graph_path(cap['approach_edges'], 0, u)
    graph_path(cap['loop_edges'], u, u, True)
    ck(sum(e[3] for e in cap['loop_edges']) == 1, 'positive E loop proves unbounded excess')
    frag = joint['local_J_fragment']
    graph_path(joint['path_to_fragment'], u, frag[0][0], True)
    graph_path(frag, frag[0][0], frag[-1][2], True)
    graph_path(joint['path_from_fragment'], frag[-1][2], u, True)
    ck(transition(pp[frag[0][0]][1], frag[0][1])['q'] == 3 and
       transition(pp[frag[1][0]][1], frag[1][1])['q'] >= 2, 'concrete local J fragment')
    graph_path(joint['joint_loop_edges'], u, u, True)

    def source_word(start, word):
        aid, bid = start
        rows, mirrored = [], []
        for i, r in enumerate(word):
            mode, key = r['mode'], r['key']
            ck(mode in ['DELETE', 'KEEP'] and 1 <= key <= 7, 'source mode and core query')
            ar = transition(aid, key)
            br = transition(bid, key) if mode == 'KEEP' else None
            na, nb = ar['target'], br['target'] if br else bid
            row = dict(occurrence=i, mode=mode, key=key, source_pair=[aid, bid], target_pair=[na, nb],
                A_source_table_row=7*aid+key-1, B_source_table_row=7*bid+key-1 if br else None,
                d_A=ar['depth'], a=ar['a'], A_events=ar['events'],
                d_B=br['depth'] if br else None, q=br['q'] if br else 0, z=br['z'] if br else 0,
                B_events=br['events'] if br else [], delta=(br['q'] if br else 0)-2*ar['a'],
                diagonal_before=aid == bid, diagonal_after=na == nb)
            full = dict(row, source_A=embed(trees[aid]), source_B=embed(trees[bid]),
                destination_A=embed(trees[na]), destination_B=embed(trees[nb]))
            mrow = dict(full, key=14-key, source_A=reflect(full['source_A']), source_B=reflect(full['source_B']),
                destination_A=reflect(full['destination_A']), destination_B=reflect(full['destination_B']),
                A_events=ar['mirror_events'], B_events=br['mirror_events'] if br else [])
            ck(mrow['A_events'] == reflect_events(row['A_events']) and mrow['B_events'] == reflect_events(row['B_events']), 'actual replay reflected events')
            ck(depth(full['source_A'], key) == depth(mrow['source_A'], 14-key) == row['d_A'], 'actual replay A depths')
            if br:
                ck(depth(full['source_B'], key) == depth(mrow['source_B'], 14-key) == row['d_B'], 'actual replay B depths')
            ck(full['destination_A'][0] == key and mrow['destination_A'][0] == 14-key, 'actual access root alignment')
            ck(mode == 'KEEP' or full['destination_B'] == full['source_B'], 'DELETE freezes B')
            rows.append(full)
            mirrored.append(mrow)
            aid, bid = na, nb
        return [aid, bid], rows, mirrored

    def budgets(rows):
        n = len(rows)
        ck(all(rows[i]['key'] != rows[(i+1) % n]['key'] for i in range(n)), 'cyclic maximal A root blocks are singletons')
        ck(all(r['a'] >= 1 for r in rows), 'all block leaders positive')
        kept = [r for r in rows if r['mode'] == 'KEEP']
        q = [r['q'] for r in kept]
        used, pairs = set(), []
        for i in range(len(q)):
            j = (i+1) % len(q)
            if q[i] >= 3 and q[j] <= 1:
                ck(i not in used and j not in used, 'high low helper pairs disjoint')
                used.update([i, j])
                pairs.append([i, j, max(q[i]+q[j]-4, 0)])
        J = sum(v[2] for v in pairs)+sum(max(q[i]-2, 0) for i in range(len(q)) if i not in used)
        # The simplified formula is checked rather than assumed.
        ck(J == sum(q[i] == 3 and q[(i+1) % len(q)] >= 2 for i in range(len(q))), 'J formula for seven core')
        def scan(keys):
            return any([keys[(i+j) % len(keys)] for j in range(7)] in
                [list(range(1, 8)), list(range(7, 0, -1))] for i in range(len(keys)))
        return dict(actions=n, physical_resets=sum(r['mode'] == 'DELETE' for r in rows),
            A=sum(r['a'] for r in rows), Q_B=sum(q), Z_B=sum(r['z'] for r in kept),
            E=sum(max(r['q']-2*r['a'], 0) for r in kept),
            C_D=sum(2*r['a'] for r in rows if r['mode'] == 'DELETE'),
            G_B=sum(max(qi-2, 0) for qi in q), J_B=J, q_profile=q, helper_pairs=pairs,
            nowhere_diagonal=not any(r['diagonal_before'] or r['diagonal_after'] for r in rows),
            full_cyclic_request_core_scan=scan([r['key'] for r in rows]),
            full_cyclic_KEEP_core_scan=scan([r['key'] for r in kept]))

    full_replays = {}
    for name in ['joint_loop', 'diagonal_return']:
        record = joint[name]
        end, rows, mrows = source_word(record['start_pair'], record['word'])
        ck(end == record['start_pair'], 'actual source pair closure')
        for compact, full in zip(record['replay'], rows):
            ck(all(full[k] == v for k, v in compact.items()), 'replay agrees with independent source composition')
        result = budgets(rows)
        for k, v in result.items():
            ck(record[k] == v, 'exact claimed whole word budgets and predicates')
        ck(all(r['a'] == 1 for r in rows if r['mode'] == 'DELETE'), 'one StepEv physical resets')
        full_replays[name] = dict(replay=rows, mirrored_replay=mrows, independent_budgets=result)

    W, H = joint['joint_loop'], joint['diagonal_return']
    Wkeys = [r['key'] for r in W['word']]
    ck(W['start_pair'] == pp[u] and Wkeys == [e[1] for e in joint['joint_loop_edges']], 'loop source identity anchored at u')
    ck((W['E'], W['G_B'], W['J_B'], W['A'], W['Q_B'], W['Z_B']) == (2, 3, 1, 36, 31, 13), 'fixed loop exact integers')
    prefix_word = [dict(mode='DELETE', key=3), dict(mode='DELETE', key=5), dict(mode='KEEP', key=7)]
    prefix_word += [dict(mode='KEEP', key=k) for k in [6, 5, 3, 7, 1]]
    exit_word = [dict(mode='KEEP', key=k) for k in [4, 2, 6, 4, 1, 3, 2, 5, 4, 2, 1]]
    ep, prefix_rows, _ = source_word([0, 0], prefix_word)
    ex, exit_rows, _ = source_word(pp[u], exit_word)
    ck(ep == pp[u] and ex == [0, 0], 'uniform family prefix and exit source identities')
    base_end, base, _ = source_word([0, 0], prefix_word+exit_word)
    basebudget = budgets(base)
    ck((basebudget['E'], basebudget['G_B'], basebudget['J_B'], basebudget['A'], basebudget['Q_B'], basebudget['Z_B']) == (2, 2, 0, 24, 21, 8), 'zero copy literal base')
    ck(prefix_rows[-1]['q'] == 1 and W['q_profile'][0] == 3 and W['q_profile'][-1] == 1 and exit_rows[0]['q'] == 3, 'all m J seam identity')
    m = max((3+W['E']-1)//W['E'], (3+W['G_B']-1)//W['G_B'], (5+W['J_B']-1)//W['J_B'])
    ck(m == joint['diagonal_repeat_count'] == 5, 'repeat count from exact ceilings')
    ck(H['word'] == prefix_word+W['word']*m+exit_word, 'literal word implements derived repeat count')
    for name, base_value, step in [('E', 2, 2), ('G_B', 2, 3), ('J_B', 0, 1), ('A', 24, 36), ('Q_B', 21, 31), ('Z_B', 8, 13)]:
        ck(H[name] == base_value+m*step, 'verified all m affine identity at certificate instance')
    ck((H['E'], H['C_D'], H['G_B'], H['J_B']) == (12, 4, 17, 5), 'requested numerical conjunction')
    ck(H['physical_resets'] == 2 and H['E'] > H['C_D'] and H['G_B'] >= 5 and H['J_B'] >= 5, 'literal requested bounds and physical resets')
    ck(Counter((r['mode'], r['key']) for r in H['word'] if r['mode'] == 'DELETE') == Counter({('DELETE', 3): 1, ('DELETE', 5): 1}), 'reset word is not proper power')

    # Complete audit of the one predeclared recurrent-input predicate.
    rejected_inputs = []
    for state in sorted(C):
        aid, bid = pp[state]
        if aid != 0:
            continue
        a = aid
        dcosts = []
        for k in [3, 5]:
            ar = transition(a, k)
            dcosts.append(ar['a'])
            a = ar['target']
        a = transition(a, 7)['target']
        br = transition(bid, 7)
        dest = pindex.get((a, br['target']))
        ck(dest not in C, 'no fixed R7 recurrent reset input')
        rejected_inputs.append(dict(state=state, source_pair=pp[state], DELETE_costs=dcosts,
            actual_B_q_on_7=br['q'], destination_pair=[a, br['target']], destination_state=dest,
            diagonal_destination=a == br['target']))
    ck(len(rejected_inputs) == 34 and not joint['off_diagonal_reset_input_found'] and joint['off_diagonal_return'] is None, 'fixed recurrent-input check failed without substitution')

    # Explicit physical units, not a multiplication of the two-reset capacity.
    rows = full_replays['diagonal_return']['replay']
    units, demands = [], []
    for r in rows:
        i = r['occurrence']
        units += [[0, i, e, bit] for e in range(r['a']) for bit in [0, 1]]
        if r['mode'] == 'KEEP':
            demands += [[0, i, e] for e, event in enumerate(r['B_events']) if event[0] != 'ZIG']
    ck(len(units) == len({tuple(x) for x in units}) == 2*H['A'], 'all physical A units distinct')
    ck(len(demands) == len({tuple(x) for x in demands}) == H['Q_B'], 'all B double demands distinct')
    keep = [r for r in rows if r['mode'] == 'KEEP']
    immediate_spare = []
    for j, r in enumerate(keep):
        if r['delta'] <= 0:
            continue
        nxt = keep[(j+1) % len(keep)]
        ck(r['delta'] == 1 and nxt['q'] < 2*nxt['a'], 'positive excess has actual immediate spare helper')
        immediate_spare.append(dict(demand_occurrence=r['occurrence'], helper_occurrence=nxt['occurrence'],
            demand_excess=1, helper_actual_spare=2*nxt['a']-nxt['q']))
    ck(len(immediate_spare) == 12 and len({r['helper_occurrence'] for r in immediate_spare}) == 12, 'immediate helpers distinct; numeric example does not assert novel charging coverage')

    # Table source contexts contain only queries and rotated keys <=7; arbitrary
    # untouched right fringe may be substituted at 7.right in the source identity.
    ck(all(1 <= lo <= hi <= 7 for row in tt for _, lo, hi, _ in row['events']), 'source rotations stay in active core')
    save('full_source_replays.json', dict(verification='composition of pinned independently executed source rows',
        source_table_sha256=sha(OLD / 'source_transition_table.json'), **full_replays))
    save('uniform_return_identity.json', dict(status='PROVED—RESTRICTED DOMAIN',
        quantifiers='For every integer m>=0 and every untouched BST fringe F with keys greater than7, including empty F',
        initial='(R_[1,7] with F at7.right, same tree)',
        prefix=prefix_word, loop=W['word'], exit=exit_word, loop_start_pair=pp[u],
        identity='prefix * W^m * exit returns the exact initial A/B pair',
        E='2+2m', C_D=4, G_B='2+3m', J_B='m', A='24+36m', Q_B='21+31m', Z_B='8+13m',
        actions='19+24m', physical_resets=2, reset_a_values=[1, 1],
        threshold='all m>=5 satisfy E>C_D and G_B,J_B>=5',
        all_size_specialization='For every n>=7 choose F=R_[8,n]; no new finite sizes replayed',
        reflection='reverse key order, swap children, and reflect grouped events',
        J_boundary_values=dict(last_prefix_q=1, first_W_q=3, last_W_q=1, first_exit_q=3),
        recurrent_R7_inputs=rejected_inputs, arbitrary_n_non_diagonal_cycle_claimed=False,
        immediate_spare_helpers_for_H5=immediate_spare,
        new_original_CD_walk_class_settled=False, FI_acceptance='NOT CLASSIFIED', UD_rejection_every_cut='NOT ESTABLISHED',
        matching_terminal_line='FROZEN', universal_CD='OPEN'))
    save('independent_audit.json', dict(status='PASS', date='2026-11-01',
        joint_return_sha256=sha(HERE / 'joint_return_certificate.json'),
        full_source_replays_sha256=sha(HERE / 'full_source_replays.json'),
        uniform_identity_sha256=sha(HERE / 'uniform_return_identity.json'),
        source_table_sha256=sha(OLD / 'source_transition_table.json'),
        source_basis_audit_sha256=sha(OLD / 'independent_audit.json'),
        independent_checks=dict(checks), components=218, selected_component_size=18232,
        fixed_R7_inputs_checked=len(rejected_inputs),
        fixed_R7_input_result='NONE returns to chosen off-diagonal component',
        diagonal_return_actions=139, physical_resets=2, A=204, Q_B=176, Z_B=73,
        E=12, C_D=4, G_B=17, J_B=5, nowhere_diagonal=False,
        new_source_engine_calls=0, larger_finite_fits=0, new_active_core_sizes=0,
        numeric_return_identity='PROVED—RESTRICTED DOMAIN; all m, arbitrary untouched fringe',
        strict_FI_only_closed_walk_coverage='NOT ESTABLISHED', universal_CD='OPEN',
        matching_terminal_line='FROZEN', automatic_successor_launched=False))
    print(json.dumps(dict(status='PASS', checks=sum(checks.values()), E=12, C_D=4, G_B=17, J_B=5,
        physical_resets=2, uniform_family='all m>=0; all untouched fringes',
        fixed_recurrent_inputs_checked=len(rejected_inputs), all_fixed_inputs_diagonalize=all(r['diagonal_destination'] for r in rejected_inputs),
        new_source_engine_calls=0), indent=2))


if __name__ == '__main__':
    main()
