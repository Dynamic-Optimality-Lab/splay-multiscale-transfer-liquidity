"""Independent source composition, complete fragment audit and exact unit cut.

Imports no producer, repository engine or writer. The pinned old source table
was independently executed in both orientations in tuple and pointer engines.
"""
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
KC = HERE.parent / 'route_c_seven_core_return_obstruction_20261031_v001'
EC = HERE.parent / 'route_c_seven_core_excess_capacity_20261031_v001'
checks = Counter()


def ck(test, name):
    if not test:
        raise AssertionError(name)
    checks[name] += 1


def read(p):
    return json.loads(p.read_text(encoding='utf-8'))


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def save(name, data):
    with (HERE / name).open('x', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')


def main():
    pins = read(HERE / 'entry_source_pins.json')
    for rel, expected in pins['files'].items():
        ck(sha(ROOT / rel) == expected, 'inherited file unchanged')
    ck(pins['gate_sha256'] == sha(HERE / 'NI00_FOUR_RULE_GATE.md'), 'pre-execution gate unchanged')
    local = read(HERE / 'local_fragment_certificate.json')
    result = read(HERE / 'nowhere_return_certificate.json')
    table = read(KC / 'source_transition_table.json')
    graph = read(KC / 'reachable_relation_certificate.json')
    cap = read(EC / 'capacity_certificate.json')
    source_audit, component_audit = read(KC / 'independent_audit.json'), read(EC / 'independent_audit.json')
    ck(source_audit['status'] == component_audit['status'] == 'PASS', 'independent source basis passed')
    ck(source_audit['pointer_source_calls'] == 6038, 'pinned complete pointer contexts already executed')
    ck(local['source_table_sha256'] == source_audit['source_table_sha256'] == sha(KC / 'source_transition_table.json'), 'table provenance')
    ck(local['source_relation_sha256'] == source_audit['relation_sha256'] == sha(KC / 'reachable_relation_certificate.json'), 'graph provenance')
    ck(local['source_audit_sha256'] == sha(KC / 'independent_audit.json'), 'source audit provenance')
    ck(local['source_graph_audit_sha256'] == sha(EC / 'independent_audit.json'), 'old SCC audit provenance')
    ck(result['local_certificate_sha256'] == sha(HERE / 'local_fragment_certificate.json'), 'local certificate provenance')
    ck(local['gate_sha256'] == sha(HERE / 'NI00_FOUR_RULE_GATE.md'), 'local computation follows gate')
    cores, transitions, fringe = table['cores'], table['transitions'], table['fringe']
    pairs, out = graph['pair_ids'], graph['outgoing_edges']
    labels = cap['component_labels']
    C = {s for s, c in enumerate(labels) if c == local['selected_component']}
    ck(len(C) == local['component_size'] == 18232, 'fixed component size')
    ck(all(pairs[s][0] != pairs[s][1] for s in C), 'component nowhere diagonal')
    ck(pairs[12919] == [0, 4] and result['start_state'] == 12919, 'predeclared source reset input')
    ck(result['loop_entry_state'] == 1871, 'fixed loop entry')

    def tr(tree, key):
        row = transitions[tree*7+key-1]
        ck((row['source'], row['key']) == (tree, key), 'source row lookup')
        return row

    # Check connectivity separately from the producer's BFS path choices.
    rev = {s: [] for s in C}
    for s in C:
        for key, t, delta in out[s]:
            if t in C:
                rev[t].append(s)
    for reverse in [False, True]:
        seen, stack = {1871}, [1871]
        while stack:
            s = stack.pop()
            for t in rev[s] if reverse else [e[1] for e in out[s] if e[1] in C]:
                if t not in seen:
                    seen.add(t)
                    stack.append(t)
        ck(seen == C, 'chosen component strongly connected both directions')

    local_rows, qualifiers, positive = [], [], set()
    for s in sorted(C):
        for k, t, delta in out[s]:
            if delta <= 0 or t not in C:
                continue
            first_a, first_b = tr(pairs[s][0], k), tr(pairs[s][1], k)
            ck((first_a['a'], first_b['q'], delta) == (1, 3, 1), 'actual positive source edge')
            positive.add((s, k, t, delta))
            for l, v, delta2 in out[t]:
                if v not in C:
                    continue
                second_a, second_b = tr(pairs[t][0], l), tr(pairs[t][1], l)
                spare = max(2*second_a['a']-second_b['q'], 0)
                row = dict(first=[s, k, t, delta], second=[t, l, v, delta2],
                    a_first=first_a['a'], q_first=first_b['q'],
                    a_next=second_a['a'], q_next=second_b['q'],
                    actual_immediate_spare=spare, surviving_residual=max(delta-spare, 0))
                local_rows.append(row)
                ck([first_a['target'], first_b['target']] == pairs[t] and
                   [second_a['target'], second_b['target']] == pairs[v], 'two source edges actual pair targets')
                ck(delta2 == second_b['q']-2*second_a['a'], 'second source edge delta')
                if spare == 0:
                    ck((second_a['a'], second_b['q'], delta2) == (1, 2, 0), 'zero spare gives aligned J contribution')
                    qualifiers.append(row)
    ck(local_rows == local['local_rows'], 'local classification complete and exact')
    ck(qualifiers == local['qualifying_fragments'] and len(qualifiers) == local['qualifying_count'] == 16, 'all sixteen qualifying fragments')
    ck(local['internal_positive_edges_checked'] == len(positive) == 282, 'all internal positive edges checked')
    ck(local['next_KEEP_fragments_checked'] == len(local_rows) == 1508, 'all internal successor cases checked')
    ck(local['chosen'] == qualifiers[0], 'lexicographic witness fixed before closure')

    def check_path(edges, start, finish, restrict_C=True):
        state = start
        for s, key, t, delta in edges:
            ck(state == s and [key, t, delta] in out[s], 'explicit source graph path')
            if restrict_C:
                ck(s in C and t in C, 'internal connector stays off diagonal')
            state = t
        ck(state == finish, 'source graph path endpoint')

    frag = local['chosen']
    check_path(result['path_to_fragment'], 1871, frag['first'][0])
    check_path([frag['first'], frag['second']], frag['first'][0], frag['second'][2])
    check_path(result['path_from_fragment'], frag['second'][2], 1871)
    check_path(result['loop_edges'], 1871, 1871)
    check_path(result['return_edges'], 1871, 12919)
    approach = []
    for s, key, t, weight in result['banked_approach']:
        delta = next(e[2] for e in out[s] if e[0] == key)
        ck(weight == max(delta, 0), 'banked approach weights')
        approach.append([s, key, t, delta])
    check_path(approach, 0, 1871, False)
    ck(all(pairs[s][0] != pairs[s][1] and pairs[t][0] != pairs[t][1] for s, k, t, d in approach), 'transient seed bridge off diagonal')

    def embed(t):
        return None if t is None else [t[0], embed(t[1]), fringe if t[0] == 7 else embed(t[2])]

    def mirror(t):
        return None if t is None else [14-t[0], mirror(t[2]), mirror(t[1])]

    def mev(events):
        case = dict(LL='RR', RR='LL', LR='RL', RL='LR', ZIG='ZIG')
        orient = {'L': 'R', 'R': 'L', '-': '-'}
        return [[case[kind], 14-hi, 14-lo, orient[o]] for kind, lo, hi, o in events]

    def inorder(t):
        return [] if t is None else inorder(t[1])+[t[0]]+inorder(t[2])

    def depth(t, key):
        d = 0
        while t[0] != key:
            t = t[1 if key < t[0] else 2]
            d += 1
        return d

    def compose(start, word):
        a, b = start
        compact, full, reflected = [], [], []
        for i, request in enumerate(word):
            mode, key = request['mode'], request['key']
            ar = tr(a, key)
            br = tr(b, key) if mode == 'KEEP' else None
            na, nb = ar['target'], br['target'] if br else b
            row = dict(occurrence=i, mode=mode, key=key, source_pair=[a, b], target_pair=[na, nb],
                A_table_row=7*a+key-1, B_table_row=7*b+key-1 if br else None,
                d_A=ar['depth'], a=ar['a'], A_events=ar['events'],
                d_B=br['depth'] if br else None, q=br['q'] if br else 0, z=br['z'] if br else 0,
                B_events=br['events'] if br else [], delta=(br['q'] if br else 0)-2*ar['a'],
                diagonal_before=a == b, diagonal_after=na == nb)
            actual = dict(row, source_A=embed(cores[a]), source_B=embed(cores[b]),
                destination_A=embed(cores[na]), destination_B=embed(cores[nb]))
            mr = dict(actual, key=14-key, source_A=mirror(actual['source_A']), source_B=mirror(actual['source_B']),
                destination_A=mirror(actual['destination_A']), destination_B=mirror(actual['destination_B']),
                A_events=ar['mirror_events'], B_events=br['mirror_events'] if br else [])
            for tree in [actual[k] for k in ['source_A', 'source_B', 'destination_A', 'destination_B']]+[mr[k] for k in ['source_A', 'source_B', 'destination_A', 'destination_B']]:
                ck(inorder(tree) == list(range(1, 14)), 'actual source replay strict BST')
            ck(depth(actual['source_A'], key) == depth(mr['source_A'], 14-key) == row['d_A'], 'normal and reflected A source depth')
            ck(len(row['A_events']) == row['a'] == (row['d_A']+1)//2, 'source A grouped cost')
            if br:
                ck(depth(actual['source_B'], key) == depth(mr['source_B'], 14-key) == row['d_B'], 'normal and reflected B source depth')
                ck(row['q'] == row['d_B']//2 == sum(e[0] != 'ZIG' for e in row['B_events']), 'source B double demand')
                ck(row['z'] == row['d_B'] % 2, 'B zig cost')
            else:
                ck(actual['source_B'] == actual['destination_B'] and not row['B_events'], 'DELETE leaves B unchanged')
            ck(mr['A_events'] == mev(row['A_events']) and mr['B_events'] == mev(row['B_events']), 'actual source reflected grouped events')
            ck(row['a'] > 0, 'positive A source leader')
            compact.append(row)
            full.append(actual)
            reflected.append(mr)
            a, b = na, nb
        return [a, b], compact, full, reflected

    def compute(rows):
        keep = [r for r in rows if r['mode'] == 'KEEP']
        q = [r['q'] for r in keep]
        used, helper_pairs = set(), []
        for i, value in enumerate(q):
            j = (i+1) % len(q)
            if value >= 3 and q[j] <= 1:
                ck(i not in used and j not in used, 'J helper pairs disjoint')
                used.update([i, j])
                helper_pairs.append(max(value+q[j]-4, 0))
        J = sum(helper_pairs)+sum(max(v-2, 0) for i, v in enumerate(q) if i not in used)
        residuals = []
        for i, row in enumerate(keep):
            if row['delta'] > 0:
                nxt = keep[(i+1) % len(keep)]
                spare = max(2*nxt['a']-nxt['q'], 0)
                residuals.append(dict(anchor=row['occurrence'], next_KEEP=nxt['occurrence'],
                    excess=row['delta'], next_actual_spare=spare, residual=max(row['delta']-spare, 0)))
        def scan(keys):
            return any([keys[(i+j) % len(keys)] for j in range(7)] in
                [list(range(1, 8)), list(range(7, 0, -1))] for i in range(len(keys)))
        return dict(actions=len(rows), A=sum(r['a'] for r in rows), Q_B=sum(q), Z_B=sum(r['z'] for r in keep),
            E=sum(max(r['delta'], 0) for r in keep), C_D=sum(2*r['a'] for r in rows if r['mode'] == 'DELETE'),
            G_B=sum(max(v-2, 0) for v in q), J_B=J, R_imm=sum(r['residual'] for r in residuals),
            physical_resets=sum(r['mode'] == 'DELETE' for r in rows),
            resets_one_StepEv=all(r['a'] == 1 for r in rows if r['mode'] == 'DELETE'),
            nowhere_diagonal=all(not r['diagonal_before'] and not r['diagonal_after'] for r in rows),
            singleton_cyclic_A_root_blocks=all(rows[i]['key'] != rows[(i+1) % len(rows)]['key'] for i in range(len(rows))),
            distinct_source_pairs=len({tuple(r['source_pair']) for r in rows}),
            full_cyclic_core_request_scan=scan([r['key'] for r in rows]), full_cyclic_core_KEEP_scan=scan([r['key'] for r in keep]),
            q_profile=q, a_profile=[r['a'] for r in rows], immediate_helper_residuals=residuals)

    start = [0, 4]
    loop_end, loop, loop_full, loop_ref = compose(pairs[1871], result['loop_word'])
    ck(loop_end == pairs[1871] and loop == result['loop_replay'], 'exact joint loop source return')
    loopstats = compute(loop)
    ck(loopstats == result['loop_stats'], 'loop costs independently reconstructed')
    ck((loopstats['E'], loopstats['G_B'], loopstats['J_B'], loopstats['R_imm']) == (1, 1, 1, 1), 'one aligned surviving source demand per loop')
    ck(loopstats['actions'] == 17 and loopstats['nowhere_diagonal'], 'loop shape and source pairs')
    bridgeword = result['word'][:8]
    bridge_end, bridge, _, _ = compose(start, bridgeword)
    ck(bridge_end == pairs[1871] and bridge == result['bridge_replay'], 'actual recurrent reset bridge')
    ck([r['a'] for r in bridge[:2]] == [1, 1] and [r['A_events'][0][0] for r in bridge[:2]] == ['RR', 'RR'], 'two one StepEv RR resets')
    ck(bridge[2]['q'] == 2 and bridge[2]['target_pair'] == pairs[0], 'actual recurrent B source at KEEP7')
    returnword = [dict(mode='KEEP', key=e[1]) for e in result['return_edges']]
    return_end, back, _, _ = compose(pairs[1871], returnword)
    ck(return_end == start, 'exact source return to R7 and B4')
    ck(result['word'] == bridgeword+result['loop_word']*5+returnword, 'five physical KEEP loop copies and only two reset events')
    end, rows, full, reflected = compose(start, result['word'])
    ck(end == start and rows == result['replay'], 'whole recurrent source identity')
    stats = compute(rows)
    ck(stats == result['stats'], 'all whole source predicates and budgets')
    ck((stats['E'], stats['C_D'], stats['G_B'], stats['J_B'], stats['R_imm']) == (5, 4, 5, 5, 5), 'requested bounds and surviving immediate demand')
    ck(stats['nowhere_diagonal'] and stats['physical_resets'] == 2 and stats['resets_one_StepEv'] and stats['singleton_cyclic_A_root_blocks'], 'nowhere diagonal two reset pure-block scope')
    ck(not stats['full_cyclic_core_request_scan'] and not stats['full_cyclic_core_KEEP_scan'], 'non-scanning at every cyclic seven-core window')
    ck(Counter((r['mode'], r['key']) for r in rows if r['mode'] == 'DELETE') == Counter({('DELETE', 3): 1, ('DELETE', 5): 1}), 'request word not a proper power of reset word')
    reach_end, reach, reach_full, reach_ref = compose([0, 0], result['reachability_prefix_word'])
    ck(reach_end == start and reach == result['reachability_prefix_replay'], 'actual source reachability from diagonal')
    ck(not result['reachability_prefix_credit_used'], 'reachability prefix not counted as cycle funding')

    # All-m proof: a returning loop and no high in either bridge ensure that
    # every E/G/J/R contribution is internal to a loop copy. No seam fitting.
    base_end, base, _, _ = compose(start, bridgeword+returnword)
    basestats = compute(base)
    ck(base_end == start and basestats['nowhere_diagonal'], 'zero-copy source return')
    ck((basestats['actions'], basestats['A'], basestats['Q_B'], basestats['Z_B']) == (17, 22, 18, 8), 'base exact affine constants')
    ck((basestats['E'], basestats['G_B'], basestats['J_B'], basestats['R_imm']) == (0, 0, 0, 0), 'base has no positive or high B count')
    ck(max(r['q'] for r in bridge+back) <= 2, 'no external high at any cyclic seam')
    positive_loop = [i for i, r in enumerate(loop) if r['delta'] > 0]
    ck(positive_loop == [9] and loop[9]['q'] == 3 and loop[10]['q'] == 2 and loop[10]['a'] == 1, 'all-m internal aligned residual')
    ck(loop[0]['q'] == loop[-1]['q'] == 1, 'loop seam cannot alter J or surviving demand')
    ck(all(1 <= lo <= hi <= 7 for row in transitions for _, lo, hi, _ in row['events']), 'untouched fringe substitution uses core rotations only')

    # Exact restricted Hall cut: five pair pools, plus ALL four DELETE units,
    # cannot cover the25 B demands in the five disjoint (KEEP6,KEEP4) pairs.
    all_units = [[0, r['occurrence'], ev, bit] for r in rows for ev in range(r['a']) for bit in [0, 1]]
    all_demands = [[0, r['occurrence'], ev] for r in rows if r['mode'] == 'KEEP'
                   for ev, event in enumerate(r['B_events']) if event[0] != 'ZIG']
    ck(len(all_units) == len({tuple(u) for u in all_units}) == 274, 'distinct physical A units in recurrent period')
    ck(len(all_demands) == len({tuple(d) for d in all_demands}) == 98, 'distinct recurrent B double demands')
    pair_occurrences, pair_units, pair_demands = [], [], []
    for rr in stats['immediate_helper_residuals']:
        i, j = rr['anchor'], rr['next_KEEP']
        ck(j == i+1 and rows[i]['key'] == 6 and rows[j]['key'] == 4, 'internal adjacent source pair')
        ck((rows[i]['a'], rows[i]['q'], rows[j]['a'], rows[j]['q']) == (1, 3, 1, 2), 'pair five demands versus four units')
        ck(rr['residual'] == 1 and rr['next_actual_spare'] == 0, 'full generous immediate helper still insufficient')
        pair_occurrences += [i, j]
        for r in [rows[i], rows[j]]:
            pair_units += [[0, r['occurrence'], ev, bit] for ev in range(r['a']) for bit in [0, 1]]
            pair_demands += [[0, r['occurrence'], ev] for ev, e in enumerate(r['B_events']) if e[0] != 'ZIG']
    delete_units = [[0, r['occurrence'], ev, bit] for r in rows if r['mode'] == 'DELETE'
                    for ev in range(r['a']) for bit in [0, 1]]
    ck(len(set(pair_occurrences)) == 10, 'five source pair supports disjoint')
    ck(len(pair_demands) == len({tuple(d) for d in pair_demands}) == 25, 'cut distinct demand count')
    ck(len(pair_units) == len({tuple(u) for u in pair_units}) == 20, 'cut pair capacity count without reuse')
    ck(len(delete_units) == 4 and not ({tuple(u) for u in delete_units} & {tuple(u) for u in pair_units}), 'all reset units additional and distinct')
    ck(len(pair_demands)-len(pair_units)-len(delete_units) == 1, 'restricted Hall deficit one')

    save('full_source_replays.json', dict(verification='composition of independently executed source rows',
        source_table_sha256=sha(KC / 'source_transition_table.json'),
        cycle=full, mirrored_cycle=reflected, loop=loop_full, mirrored_loop=loop_ref,
        reachability_prefix=reach_full, mirrored_reachability_prefix=reach_ref))
    save('immediate_helper_cut.json', dict(status='REFUTED—EXACT for complete repayment using only immediate pair pools plus all DELETE units',
        domain='actual five disjoint positive KEEP / immediate next KEEP source pairs in H5',
        pair_source_occurrences=pair_occurrences, demands=pair_demands,
        pair_capacity_units=pair_units, all_DELETE_units=delete_units,
        distinct_demands=25, distinct_pair_units=20, distinct_DELETE_units=4, deficit=1,
        original_Hall_graph_claimed=False, arbitrary_delayed_KEEP_credit_excluded_from_this_template=True,
        no_reused_units=True, reachability_prefix_units_used=0,
        all_m_cut='5m distinct pair demands versus4m pair units+4 DELETE units; deficit m-4',
        meaning='any full repayment for m>=5 needs a KEEP unit outside the immediate pair supports',
        universal_CD_counterexample_claimed=False))
    save('uniform_nowhere_identity.json', dict(status='PROVED—RESTRICTED DOMAIN',
        quantifiers='all integers m>=0, every untouched BST fringe F>7 including empty',
        start_pair_core_ids=start, start_A_core=cores[0], start_B_core=cores[4],
        prefix=bridgeword, loop=result['loop_word'], return_word=returnword,
        actions='17+17m', A='22+23m', Q_B='18+16m', Z_B='8+11m',
        E='m', C_D=4, G_B='m', J_B='m', R_imm='m', physical_resets=2,
        each_DELETE_a=1, nowhere_diagonal=True, paired_closed=True,
        threshold='every m>=5 satisfies all numerical bounds and R_imm>C_D',
        n_extension='all n>=7 by replacing fringe with R_[8,n]; arbitrary fringe also permitted',
        source_reachability_prefix_separate=True, prefix_units_used=0,
        proper_power_of_reset_word=False, simple_cycle_claimed=False,
        FI_acceptance='NOT CLASSIFIED', UD_rejection_every_cut='NOT ESTABLISHED', universal_CD='OPEN'))
    save('independent_audit.json', dict(status='PASS', date='2026-11-01', checks=dict(checks),
        source_table_sha256=sha(KC / 'source_transition_table.json'),
        local_certificate_sha256=sha(HERE / 'local_fragment_certificate.json'),
        return_certificate_sha256=sha(HERE / 'nowhere_return_certificate.json'),
        full_source_replays_sha256=sha(HERE / 'full_source_replays.json'),
        immediate_helper_cut_sha256=sha(HERE / 'immediate_helper_cut.json'),
        uniform_identity_sha256=sha(HERE / 'uniform_nowhere_identity.json'),
        local_positive_edges=282, successor_fragments=1508, qualifying_fragments=16,
        concrete_actions=102, A=137, Q_B=98, Z_B=63, E=5, C_D=4, G_B=5, J_B=5, R_imm=5,
        physical_resets=2, reset_a_values=[1, 1], nowhere_diagonal=True, cyclic_full_core_scan=False,
        distinct_source_pairs=stats['distinct_source_pairs'], source_reachable=True,
        restricted_Hall_deficit=1, prefix_credit_used=0, new_source_engine_calls=0,
        larger_finite_fits=0, new_active_core_sizes=0,
        strict_FI_only_coverage='NOT ESTABLISHED', matching_terminal_line='FROZEN', universal_CD='OPEN',
        automatic_successor_launched=False))
    print(json.dumps(dict(status='PASS', checks=sum(checks.values()), actions=102,
        E=5, C_D=4, G_B=5, J_B=5, R_imm=5, nowhere_diagonal=True,
        pair_demands=25, immediate_pair_units_plus_DELETE=24, strict_cut_deficit=1,
        all_m_identity='E=G_B=J_B=R_imm=m', new_source_engine_calls=0), indent=2))


if __name__ == '__main__':
    main()
