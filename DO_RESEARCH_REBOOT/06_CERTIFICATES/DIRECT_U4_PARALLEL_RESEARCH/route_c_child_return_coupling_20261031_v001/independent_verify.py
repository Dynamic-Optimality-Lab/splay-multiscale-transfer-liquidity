"""Pointer-source audit of all 265 exact child/DELETE-return words and reflection."""
import hashlib
import importlib.util
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASE = [13, 11, 12, 9, 10, 7, 8, 5, 6, 3, 4, 1, 2]
EXPECTED_A = [5, 3, 1, 3, 2, 3, 2, 2, 1, 2, 1, 2, 1]


def ck(ok, message):
    if not ok:
        raise AssertionError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':'), ensure_ascii=False).encode('utf-8')).hexdigest()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(name, value):
    with (HERE / name).open('x', encoding='utf-8') as f:
        json.dump(value, f, indent=2, ensure_ascii=False)
        f.write('\n')


def sweeps(word):
    out = []
    for i in range(len(word)):
        for low in (1, 2):
            pat = list(range(low, low+12))
            for orient, values in [('ascending', pat), ('descending', list(reversed(pat)))]:
                if (word+word)[i:i+12] == values:
                    out.append(dict(start=i, low=low, orientation=orient))
    return out


def main():
    ap = HERE / 'A_clock_certificate.json'
    cp = HERE / 'child_return_class_certificate.json'
    ac = json.loads(ap.read_text(encoding='utf-8'))
    cert = json.loads(cp.read_text(encoding='utf-8'))
    ck(ac['base'] == cert['base'] == BASE and cert['cap'] == 64 and len(cert['cases']) == 265,
        'literal base, cap and complete fixed class')
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
        return [] if t is None else inorder(t[1])+[t[0]]+inorder(t[2])

    def depth(t, key):
        d = 0
        while t is not None:
            if t[0] == key:
                return d
            t = t[1] if key < t[0] else t[2]
            d += 1
        raise AssertionError('present source key')

    def mirror_events(events):
        cm = {'LL': 'RR', 'RR': 'LL', 'LR': 'RL', 'RL': 'LR', 'ZIG': 'ZIG'}
        om = {'L': 'R', 'R': 'L', '-': '-'}
        return [[cm[e[0]], 14-e[2], 14-e[1], om[e[3]]] for e in events]

    def mirror_A(r):
        return dict(r, key=14-r['key'], source_A=mirror(r['source_A']),
            destination_A=mirror(r['destination_A']), A_events=mirror_events(r['A_events']))

    calls = trees = 0

    def access(t, key):
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
        ck((q, z, len(ev)) == (d//2, d%2, (d+1)//2), 'source grouped costs and B-double counts')
        calls += 1
        return dest, d, ev, q, z

    right = None
    for key in range(13, 4, -1):
        right = [key, None, right]
    initial = [2, [1, None, None], [4, [3, None, None], right]]
    ck(ac['initial_diagonal'] == cert['initial_diagonal'] == initial, 'fixed legal diagonal T*')
    A, mA = initial, mirror(initial)
    base_rows, phase_trees = [], []
    for phase, key in enumerate(BASE):
        pre = A
        A, d, ev, q, z = access(A, key)
        mA, md, me, mq, mz = access(mA, 14-key)
        row = dict(phase=phase, role='BASE_KEEP', mode='KEEP', key=key, source_A=pre,
            destination_A=A, d_A=d, a=len(ev), A_events=ev)
        ck(row == ac['base_rows'][phase], 'every base A source tree, cost and event')
        ck((mA, md, me, mq, mz) == (mirror(A), d, mirror_events(ev), q, z), 'base identity reflection')
        base_rows.append(row)
        phase_trees.append(A)
    ck(A == initial and mA == mirror(initial) and [r['a'] for r in base_rows] == EXPECTED_A,
        'banked A clock reverified with exact profile and closure')
    options, by_phase = [], {}
    for phase, tree in enumerate(phase_trees):
        choices = []
        for side, child in [('L', tree[1]), ('R', tree[2])]:
            if child is None:
                continue
            key, root = child[0], tree[0]
            child_tree, d1, ev1, q1, z1 = access(tree, key)
            returned, d2, ev2, q2, z2 = access(child_tree, root)
            mc, md1, me1, mq1, mz1 = access(mirror(tree), 14-key)
            mr, md2, me2, mq2, mz2 = access(mc, 14-root)
            ck(returned == tree and d1 == d2 == 1 and len(ev1) == len(ev2) == 1,
                'child and old-root return are actual inverse one-StepEv zigs')
            ck((mc, md1, me1, mq1, mz1) == (mirror(child_tree), d1, mirror_events(ev1), q1, z1) and
                (mr, md2, me2, mq2, mz2) == (mirror(tree), d2, mirror_events(ev2), q2, z2),
                'every child/return identity reflected and executed')
            opt = dict(phase=phase, side=side, root_key=root, child_key=key,
                child_row=dict(phase=phase, role='CHILD_KEEP', mode='KEEP', key=key,
                    source_A=tree, destination_A=child_tree, d_A=1, a=1, A_events=ev1),
                return_row=dict(phase=phase, role='RESET_RETURN', mode='DELETE', key=root,
                    source_A=child_tree, destination_A=returned, d_A=1, a=1, A_events=ev2))
            options.append(opt)
            choices.append(opt)
        by_phase[phase] = choices
    ck(options == ac['options'] and len(options) == 24 and calls == 122, 'all24 fixed child choices and A source calls')
    A_calls = calls
    words = [(g, h, og, oh) for g, h in itertools.combinations(range(13), 2)
        for og in by_phase[g] for oh in by_phase[h]]
    ck(len(words) == 265, 'complete two-distinct-phase enumeration')

    outcomes, filters, periods, transients = Counter(), Counter(), Counter(), Counter()
    nowhere = Counter()
    maxG1 = maxJ1 = maxE1 = -1
    maxE = maxJminusCD = None
    maxmargin = None
    max_child_q = 0
    total_rows = recurrent_rows = assignments = 0
    reflected_cases, local_cases = [], []
    for case_index, (g, h, og, oh) in enumerate(words):
        case = cert['cases'][case_index]
        ck(case['case_index'] == case_index and case['phases'] == [g, h] and
            case['sides'] == [og['side'], oh['side']] and case['child_keys'] == [og['child_key'], oh['child_key']],
            'literal lexicographic fixed phase/child domain')
        selected_options = {g: og, h: oh}
        a_word = []
        for phase, row in enumerate(base_rows):
            a_word.append(dict(row, position=len(a_word)))
            if phase in selected_options:
                opt = selected_options[phase]
                a_word.append(dict(opt['child_row'], position=len(a_word)))
                a_word.append(dict(opt['return_row'], position=len(a_word)))
        ck(a_word == case['A_word'] and len(a_word) == 17 and sum(r['a'] for r in a_word) == 32,
            'entire A source word and varying A costs are explicit')
        ck(all(a_word[i]['destination_A'] == a_word[(i+1) % 17]['source_A'] and
            a_word[i]['key'] != a_word[(i+1) % 17]['key'] for i in range(17)),
            'A whole-tree closure and one positive-cost leader per request')
        pure = [r for r in a_word if r['mode'] == 'DELETE']
        ck(len(pure) == 2 and all(r['a'] == 1 and r['d_A'] == 1 for r in pure), 'exact two pure one-StepEv resets')
        keep_word = [r['key'] for r in a_word if r['mode'] == 'KEEP']
        ck(keep_word == case['KEEP_word'], 'exact induced B query word')
        scan_hits = sweeps([r['key'] for r in a_word])+sweeps(keep_word)
        b, mb = initial, mirror(initial)
        seen = [b]
        boundaries = [dict(lap=0, B=b)]
        mboundaries = [dict(lap=0, B=mb)]
        rows = []
        reflected_stream = hashlib.sha256()
        start = end = None
        for lap in range(1, 65):
            for i, ar in enumerate(a_word):
                pre, mpre = b, mb
                if ar['mode'] == 'KEEP':
                    b, d, ev, q, z = access(b, ar['key'])
                    mb, md, me, mq, mz = access(mb, 14-ar['key'])
                    ck((mb, md, me, mq, mz) == (mirror(b), d, mirror_events(ev), q, z),
                        'every actual B transition, interval and orientation reflected')
                else:
                    d, ev, q, z = None, [], 0, 0
                    md, me, mq, mz = None, [], 0, 0
                row = dict(occurrence=len(rows), lap=lap-1, position=i, phase=ar['phase'],
                    role=ar['role'], mode=ar['mode'], key=ar['key'], d_A=ar['d_A'], a=ar['a'],
                    d_B=d, q=q, z=z, B_events=ev,
                    source_pair_sha256=digest([ar['source_A'], pre]),
                    destination_pair_sha256=digest([ar['destination_A'], b]),
                    diagonal_before=ar['source_A'] == pre, diagonal_after=ar['destination_A'] == b)
                ck(row == case['orbit_replay'][len(rows)], 'all reconstructed source pairs, destinations, events and costs')
                ck(q <= 2*ar['a'], 'every replayed B demand fits its actual own A pool')
                if ar['role'] == 'CHILD_KEEP':
                    max_child_q = max(max_child_q, q)
                mirrored = dict(row, key=14-ar['key'], d_B=md, q=mq, z=mz, B_events=me,
                    source_pair_sha256=digest([mirror(ar['source_A']), mpre]),
                    destination_pair_sha256=digest([mirror(ar['destination_A']), mb]))
                ck(mirrored['diagonal_before'] == (mirror(ar['source_A']) == mpre) and
                    mirrored['diagonal_after'] == (mirror(ar['destination_A']) == mb), 'reflected source diagonal indicators')
                reflected_stream.update((json.dumps(mirrored, separators=(',', ':'), ensure_ascii=False)+'\n').encode('utf-8'))
                rows.append(row)
            boundaries.append(dict(lap=lap, B=b))
            mboundaries.append(dict(lap=lap, B=mb))
            if b in seen:
                start, end = seen.index(b), lap
                break
            seen.append(b)
        ck(start is not None and boundaries == case['boundary_records'] and len(rows) == len(case['orbit_replay']),
            'first exact recurrence and all raw source boundary pairs')
        p_laps = end-start
        cyc = rows[17*start:17*end]
        kept = [r for r in cyc if r['mode'] == 'KEEP']
        q = [r['q'] for r in kept]
        used, helpers = set(), []
        for j, value in enumerate(q):
            k = (j+1) % len(q)
            if value >= 3 and q[k] <= 1:
                ck(j not in used and k not in used, 'one physical occurrence per helper cell')
                used.update((j, k))
                helpers.append(dict(high=j, helper=k, q_high=value, q_helper=q[k],
                    residual_upper_bound=max(value+q[k]-4, 0)))
        G = sum(max(value-2, 0) for value in q)
        J = sum(v['residual_upper_bound'] for v in helpers) + sum(max(value-2, 0) for j, value in enumerate(q) if j not in used)
        E = sum(max(r['q']-2*r['a'], 0) for r in cyc)
        CD = sum(2*r['a'] for r in cyc if r['mode'] == 'DELETE')
        diag = [i for i, r in enumerate(cyc) if r['diagonal_before']]
        cycle = dict(transient_laps=start, period_laps=p_laps, source_start=17*start, source_end=17*end,
            source_B=boundaries[start]['B'], paired_closed=True, cycle_length=17*p_laps,
            physical_resets=2*p_laps, A=32*p_laps, Q_B=sum(q), Z_B=sum(r['z'] for r in kept),
            E=E, C_D=CD, G_B=G, J_B=J, q_profile=q, immediate_helper_pairs=helpers,
            diagonal_source_occurrences=diag, distinct_source_pairs=len({r['source_pair_sha256'] for r in cyc}),
            core_scan_hits=scan_hits)
        ck(cycle == case['cycle'] and boundaries[start]['B'] == boundaries[end]['B'], 'entire cyclic cost/provenance record')
        ck(CD == 4*p_laps and sum(r['a'] for r in cyc) == 32*p_laps, 'physical source funding, no period relabeling')
        if p_laps != 1:
            outcome = 'MORE_THAN_TWO_PHYSICAL_RESETS'
        elif scan_hits:
            outcome = 'CONSECUTIVE_CORE_SCAN'
        elif G < 5:
            outcome = 'G_BELOW_FIVE'
        elif J < 5:
            outcome = 'J_BELOW_FIVE'
        elif E <= 4:
            outcome = 'EXCESS_NOT_OVER_RESET_CAPACITY'
        elif diag:
            outcome = 'NUMERIC_HIT_WITH_DIAGONAL_STATES'
        else:
            outcome = 'REQUESTED_COMPONENT_CERTIFIED'
        ck(outcome == case['outcome'], 'predeclared criteria and outcome ordering')
        outcomes[outcome] += 1
        periods[p_laps] += 1
        transients[start] += 1
        filters['G_at_least_5'] += G >= 5
        filters['J_at_least_5'] += J >= 5
        filters['G_and_J_at_least_5'] += G >= 5 and J >= 5
        filters['E_greater_than_C_D'] += E > CD
        filters['nowhere_diagonal'] += not diag
        if not diag:
            nowhere[p_laps] += 1
        if p_laps == 1:
            maxG1, maxJ1, maxE1 = max(maxG1, G), max(maxJ1, J), max(maxE1, E)
        maxE = E if maxE is None else max(maxE, E)
        maxJminusCD = J-CD if maxJminusCD is None else max(maxJminusCD, J-CD)
        maxmargin = E-CD if maxmargin is None else max(maxmargin, E-CD)
        total_rows += len(rows)
        recurrent_rows += len(cyc)
        units, demands = set(), set()
        assigned = 0
        for occurrence, r in enumerate(cyc):
            ordinal = 0
            ar = a_word[r['position']]
            for event_index, event in enumerate(r['B_events']):
                if event[0] == 'ZIG':
                    continue
                unit = (case_index, occurrence, ordinal//2, ordinal % 2)
                demand = (case_index, occurrence, event_index)
                ck(unit[2] < len(ar['A_events']) == r['a'], 'unit belongs to an actual own A event')
                ck(r['mode'] == 'KEEP' and unit not in units and demand not in demands, 'no source unit or demand reuse')
                units.add(unit)
                demands.add(demand)
                ordinal += 1
                assigned += 1
            ck(ordinal == r['q'], 'B event multiplicity exact')
        ck(assigned == cycle['Q_B'], 'every recurrent demand paid by its own physical A block')
        assignments += assigned
        local_cases.append(dict(case_index=case_index, period_laps=p_laps, E=E, C_D=CD,
            Q_B=assigned, locally_assigned_demands=assigned, all_cuts_local=True))
        reflected_cases.append(dict(case_index=case_index, phases=[g, h],
            sides=[{'L': 'R', 'R': 'L'}[side] for side in case['sides']],
            child_keys=[14-key for key in case['child_keys']], KEEP_word=[14-key for key in keep_word],
            boundary_records=mboundaries, paired_request_stream_sha256=reflected_stream.hexdigest(),
            transient_laps=start, period_laps=p_laps, A=32*p_laps, E=E, C_D=CD, G_B=G, J_B=J,
            Q_B=cycle['Q_B'], diagonal_source_occurrences=diag, outcome=outcome))
        if (case_index+1) % 75 == 0:
            print(json.dumps(dict(independent_cases_checked=case_index+1, max_single_G=maxG1,
                max_single_J=maxJ1, max_single_E=maxE1)), flush=True)
    ck(dict(outcomes) == cert['outcomes'] and dict(filters) == cert['filters'], 'all independent filters and class outcomes')
    ck({str(k): v for k, v in periods.items()} == cert['periods'] and
        {str(k): v for k, v in transients.items()} == cert['transients'], 'complete first-recurrence census')
    ck((maxG1, maxJ1, maxE1, maxmargin) == (cert['max_G_B_single_period'], cert['max_J_B_single_period'],
        cert['max_E_single_period'], cert['max_E_minus_C_D']) == (6, 4, 0, -4), 'exact maxima, not fitted bounds')
    ck(cert['outcome'] == 'EXACT_CHILD_RETURN_CLASS_EXCLUDED' and cert['selected_case'] is None and
        cert['all_declared_cases_examined'], 'no cap result, hidden success or changed scope')
    ck(calls == 2*cert['tuple_source_calls'] == 13112 and trees == 26224 and
        (total_rows, recurrent_rows) == (7361, 5219), 'complete bounded source audit counts')
    save('reflected_class_certificate.json', dict(base=[14-key for key in BASE], initial_diagonal=mirror(initial),
        base_rows=[mirror_A(r) for r in base_rows], cases=reflected_cases,
        stream_hash_format='compact source-order row JSON plus newline', all_streams_reconstructed_by_pointer_source=True))
    save('local_unit_audit.json', dict(status='PASS', map_rule='B double ordinal b uses own A event floor(b/2), bit b mod2',
        cases=local_cases, assignments_checked_normal=assignments, reflected_events_and_assignments_verified=True,
        alternative_cases_and_orientations_are_separate_resource_universes=True,
        reachability_prefix_units_used=0, later_lap_units_used=0, alternative_case_units_used=0,
        all_cuts_local=True, FI_UD_cut_recognizers_executed=0))
    result = dict(status='PASS', date='2026-10-31', A_clock_sha256=sha(ap), class_certificate_sha256=sha(cp),
        cases=265, cap_cases=0, periods=dict(periods), transients=dict(transients), outcomes=dict(outcomes), filters=dict(filters),
        source_A_clock_pointer_calls=A_calls, source_B_pointer_calls=calls-A_calls,
        total_pointer_source_calls=calls, strict_BST_tree_occurrences=trees,
        paired_request_rows_per_orientation=total_rows, recurrent_request_rows_per_orientation=recurrent_rows,
        nowhere_diagonal_cycles_by_period=dict(nowhere), max_child_query_q=max_child_q,
        max_G_B_single_period=maxG1, max_J_B_single_period=maxJ1, max_E_single_period=maxE1,
        max_E_all_cycles=maxE, max_E_minus_C_D=maxmargin, max_J_B_minus_C_D=maxJminusCD,
        local_assignments_checked_normal=assignments, requested_cycle='NOT FOUND',
        exact_fixed_class='EXCLUDED', general_child_return_obstruction_claimed=False,
        finite_fits=0, new_finite_key_sizes=0, adaptive_clock_changes=0, A_witness_searches=0, FI_UD_cut_trials=0,
        strict_FI_only_coverage='NOT ESTABLISHED', universal_CD='OPEN', matching_terminal_line='FROZEN')
    save('independent_audit.json', result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
