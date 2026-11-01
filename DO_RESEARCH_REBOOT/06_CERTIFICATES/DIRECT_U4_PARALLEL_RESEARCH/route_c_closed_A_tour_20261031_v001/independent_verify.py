"""Pointer-source verification of every fixed A-tour omission and reflection."""
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
TOUR = [3, 2, 4, 6, 5, 7, 9, 8, 10, 12, 11, 13, 11, 12, 10, 8, 9, 7, 5, 6, 4, 2, 3, 1]


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
    patterns = []
    w = word+word
    for i in range(len(word)):
        for low in (1, 2):
            pattern = list(range(low, low+12))
            for orient, values in [('ascending', pattern), ('descending', list(reversed(pattern)))]:
                if w[i:i+12] == values:
                    patterns.append(dict(start=i, low=low, orientation=orient))
    return patterns


def main():
    ap = HERE / 'closed_A_identity_certificate.json'
    cp = HERE / 'mode_class_certificate.json'
    ac = json.loads(ap.read_text(encoding='utf-8'))
    cert = json.loads(cp.read_text(encoding='utf-8'))
    ck(ac['tour'] == cert['tour'] == TOUR and cert['cap'] == 64 and len(cert['cases']) == 276,
        'literal predeclared tour, cap and full mode class')
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

    def T(root):
        left = None
        for key in range(1, root):
            left = [key, left, None]
        right = None
        for key in range(13, root, -1):
            right = [key, None, right]
        return [root, left, right]

    def mev(events):
        cm = {'LL': 'RR', 'RR': 'LL', 'LR': 'RL', 'RL': 'LR', 'ZIG': 'ZIG'}
        om = {'L': 'R', 'R': 'L', '-': '-'}
        return [[cm[e[0]], 14-e[2], 14-e[1], om[e[3]]] for e in events]

    calls = trees = 0

    def access(t, key):
        nonlocal calls, trees
        ck(inorder(t) == list(range(1, 14)), 'strict input BST and exact thirteen keys')
        trees += 1
        d = depth(t, key)
        out, events = p.splay_trace(ptr(t), key)
        dest = raw(out)
        ck(inorder(dest) == list(range(1, 14)), 'strict output BST and exact thirteen keys')
        trees += 1
        ev = [[e['case'], e['lo'], e['hi'], e['orient']] for e in events]
        q, z = sum(e[0] != 'ZIG' for e in ev), sum(e[0] == 'ZIG' for e in ev)
        ck((q, z, len(ev)) == (d//2, d%2, (d+1)//2), 'source grouped events and doubles')
        calls += 1
        return dest, d, ev, q, z

    A = initial = T(1)
    mA = mirror(initial)
    a_rows = []
    for i, key in enumerate(TOUR):
        pre = A
        A, d, ev, q, z = access(A, key)
        mA, md, me, mq, mz = access(mA, 14-key)
        row = dict(position=i, key=key, source_A=pre, destination_A=A, d_A=d, a=1, A_events=ev)
        ck(row == ac['A_trace'][i] and A == T(key), 'every exact A identity and one-StepEv')
        ck((mA, md, me, mq, mz) == (mirror(A), d, mev(ev), q, z), 'A identity reflection')
        ck(d in (1, 2) and len(ev) == 1, 'A cost proved independently of modes')
        a_rows.append(row)
    ck(A == initial and mA == mirror(initial), 'A closes exactly after twenty-four actions')
    ck(ac['initial_diagonal'] == cert['initial_diagonal'] == initial and not sweeps(TOUR),
        'diagonal source and no full consecutive core scan')
    A_calls = calls

    outcomes, periods, transients = Counter(), Counter(), Counter()
    reflected_cases = []
    local_units = []
    max_depth = 0
    maxG = maxJ = maxE = 0
    no_diag = Counter()
    total_rows = recurrent_rows = 0
    maxG1 = maxJ1 = -1
    expected_pairs = list(itertools.combinations(range(24), 2))
    for case_index, omitted_tuple in enumerate(expected_pairs):
        case = cert['cases'][case_index]
        omitted = list(omitted_tuple)
        modes = ['DELETE' if i in omitted else 'KEEP' for i in range(24)]
        keep_word = [key for i, key in enumerate(TOUR) if modes[i] == 'KEEP']
        ck(case['case_index'] == case_index and case['DELETE_positions'] == omitted and
            case['modes'] == modes and case['KEEP_word'] == keep_word, 'complete lexicographic mode domain')
        b, mb = initial, mirror(initial)
        seen = [b]
        boundaries = [dict(lap=0, B=b)]
        mboundaries = [dict(lap=0, B=mb)]
        rows = []
        start = end = None
        reflected_stream = hashlib.sha256()
        for lap in range(1, 65):
            for i, key in enumerate(TOUR):
                pre, mpre = b, mb
                if modes[i] == 'KEEP':
                    b, d, ev, q, z = access(b, key)
                    mb, md, me, mq, mz = access(mb, 14-key)
                    ck((mb, md, me, mq, mz) == (mirror(b), d, mev(ev), q, z), 'all B reflection source events')
                    max_depth = max(max_depth, d)
                else:
                    d, ev, q, z = None, [], 0, 0
                    md, me, mq, mz = None, [], 0, 0
                row = dict(occurrence=len(rows), lap=lap-1, position=i, mode=modes[i], key=key,
                    d_A=a_rows[i]['d_A'], a=1, d_B=d, q=q, z=z, B_events=ev,
                    source_pair_sha256=digest([a_rows[i]['source_A'], pre]),
                    destination_pair_sha256=digest([a_rows[i]['destination_A'], b]),
                    diagonal_before=a_rows[i]['source_A'] == pre,
                    diagonal_after=a_rows[i]['destination_A'] == b)
                ck(row == case['orbit_replay'][len(rows)], 'every physical request source pair, destination pair, depth and event')
                mr = dict(row, key=14-key, d_B=md, q=mq, z=mz, B_events=me,
                    source_pair_sha256=digest([mirror(a_rows[i]['source_A']), mpre]),
                    destination_pair_sha256=digest([mirror(a_rows[i]['destination_A']), mb]))
                reflected_stream.update((json.dumps(mr, separators=(',', ':'), ensure_ascii=False)+'\n').encode('utf-8'))
                ck(mr['diagonal_before'] == (mirror(a_rows[i]['source_A']) == mpre) and
                    mr['diagonal_after'] == (mirror(a_rows[i]['destination_A']) == mb), 'reflected pair diagonal flags')
                rows.append(row)
            boundaries.append(dict(lap=lap, B=b))
            mboundaries.append(dict(lap=lap, B=mb))
            if b in seen:
                start, end = seen.index(b), lap
                break
            seen.append(b)
        ck(start is not None and boundaries == case['boundary_records'] and len(rows) == len(case['orbit_replay']),
            'first exact pair repeat with full transient provenance')
        period = end-start
        cyc = rows[24*start:24*end]
        kept = [r for r in cyc if r['mode'] == 'KEEP']
        q = [r['q'] for r in kept]
        used, helper_pairs = set(), []
        for j, value in enumerate(q):
            k = (j+1) % len(q)
            if value >= 3 and q[k] <= 1:
                ck(j not in used and k not in used, 'disjoint helper cells')
                used.update((j, k))
                helper_pairs.append(dict(high=j, helper=k, q_high=value, q_helper=q[k],
                    residual_upper_bound=max(value+q[k]-4, 0)))
        G = sum(max(v-2, 0) for v in q)
        J = sum(v['residual_upper_bound'] for v in helper_pairs) + sum(max(v-2, 0) for j, v in enumerate(q) if j not in used)
        E = sum(max(r['q']-2, 0) for r in cyc)
        CD = 2*sum(r['mode'] == 'DELETE' for r in cyc)
        diagonal = [i for i, r in enumerate(cyc) if r['diagonal_before']]
        cycle = dict(transient_laps=start, period_laps=period, source_start=24*start, source_end=24*end,
            source_B=boundaries[start]['B'], paired_closed=True, cycle_length=24*period,
            resets=2*period, A=24*period, C_D=CD, E=E, Q_B=sum(q), Z_B=sum(r['z'] for r in kept),
            G_B=G, J_B=J, q_profile=q, immediate_helper_pairs=helper_pairs,
            diagonal_source_occurrences=diagonal,
            distinct_source_pairs=len({r['source_pair_sha256'] for r in cyc}),
            kept_key_count=len(set(keep_word)), KEEP_core_sweeps=sweeps(keep_word))
        ck(cycle == case['cycle'] and boundaries[start]['B'] == boundaries[end]['B'],
            'actual paired closure and every recurrent cost/source invariant')
        ck(E == G and CD == 4*period and all(v <= 2 for v in q), 'no source positive in any examined recurrent cycle')
        if period != 1:
            outcome = 'MORE_THAN_TWO_PHYSICAL_RESETS'
        elif sweeps(keep_word):
            outcome = 'CONSECUTIVE_CORE_SCAN'
        elif G < 5:
            outcome = 'G_BELOW_FIVE'
        elif J < 5:
            outcome = 'J_BELOW_FIVE'
        elif diagonal:
            outcome = 'BUDGET_HIT_WITH_DIAGONAL_STATES'
        else:
            outcome = 'REQUESTED_COMPONENT_CERTIFIED'
        ck(outcome == case['outcome'], 'predeclared success predicates unchanged')
        outcomes[outcome] += 1
        periods[period] += 1
        transients[start] += 1
        if not diagonal:
            no_diag[period] += 1
        maxG, maxJ, maxE = max(maxG, G), max(maxJ, J), max(maxE, E)
        if period == 1:
            maxG1, maxJ1 = max(maxG1, G), max(maxJ1, J)
        total_rows += len(rows)
        recurrent_rows += len(cyc)
        units, demands = set(), set()
        count = 0
        for occurrence, r in enumerate(cyc):
            ord_double = 0
            for event_index, ev in enumerate(r['B_events']):
                if ev[0] == 'ZIG':
                    continue
                unit = (case_index, occurrence, 0, ord_double)
                demand = (case_index, occurrence, event_index)
                ck(r['mode'] == 'KEEP' and ord_double in (0, 1), 'each own B double fits one of two actual A units')
                ck(unit not in units and demand not in demands, 'local source units and demands never reused')
                units.add(unit)
                demands.add(demand)
                ord_double += 1
                count += 1
            ck(ord_double == r['q'], 'source event multiplicity exactly counted')
        ck(count == cycle['Q_B'], 'all B doubles pay locally in this finite class')
        local_units.append(dict(case_index=case_index, period_laps=period, A=24*period, Q_B=count,
            E=0, C_D=CD, locally_assigned_demands=count, all_cuts_local=True))
        reflected_cases.append(dict(case_index=case_index, DELETE_positions=omitted, modes=modes,
            KEEP_word=[14-key for key in keep_word], boundary_records=mboundaries,
            paired_request_stream_sha256=reflected_stream.hexdigest(),
            transient_laps=start, period_laps=period, A=24*period, Q_B=cycle['Q_B'],
            G_B=G, J_B=J, E=E, C_D=CD, diagonal_source_occurrences=diagonal, outcome=outcome))
        if (case_index+1) % 75 == 0:
            print(json.dumps(dict(independent_cases_checked=case_index+1, max_G_B=maxG, max_J_B=maxJ)), flush=True)
    ck(dict(outcomes) == cert['outcomes'], 'complete outcome census')
    ck({str(k): v for k, v in periods.items()} == cert['periods'] and
        {str(k): v for k, v in transients.items()} == cert['transients'], 'complete recurrence census')
    ck(cert['outcome'] == 'EXACT_MODE_CLASS_EXCLUDED' and cert['selected_case'] is None and
        cert['all_declared_cases_examined'], 'no hidden stop or cap result')
    ck((maxG1, maxJ1) == (cert['max_G_B_single_period'], cert['max_J_B_single_period']) == (0, 0),
        'exact single-period G/J maxima')
    ck((calls, A_calls, trees, total_rows, recurrent_rows) == (21168, 48, 42336, 11520, 9216),
        'bounded source verification counts')
    save('reflected_class_certificate.json', dict(tour=[14-key for key in TOUR], initial_diagonal=mirror(initial),
        cases=reflected_cases, full_stream_format='compact sorted-order row JSON plus newline, hashed in source order',
        cases_reconstructed_from_literal_source=True, max_G_B=0, max_J_B=0, max_E=0))
    save('local_unit_audit.json', dict(status='PASS', map_rule='B double ordinal b in row t uses A unit (case,t,event0,bit=b)',
        cases=local_units, assignments_checked_normal=sum(v['locally_assigned_demands'] for v in local_units),
        reflected_assignment_events_verified=True, all_maps_are_separate_resource_universes=True,
        prefix_units_used=0, other_case_units_used=0, later_lap_units_used=0,
        FI_UD_cut_recognizers_executed=0, all_cuts_succeed_because_all_demands_pay_locally=True))
    result = dict(status='PASS', date='2026-10-31', A_identity_sha256=sha(ap), mode_class_sha256=sha(cp),
        cases=276, all_cases_first_repeat_verified=True, cap_cases=0, periods=dict(periods), transients=dict(transients),
        outcomes=dict(outcomes), source_A_identity_pointer_calls=A_calls,
        source_B_pointer_calls=calls-A_calls, total_pointer_source_calls=calls,
        strict_BST_tree_occurrences=trees, paired_request_rows_per_orientation=total_rows,
        recurrent_request_rows_per_orientation=recurrent_rows, no_diagonal_cycles_by_period=dict(no_diag),
        max_replayed_B_depth=max_depth, max_G_B_all_cycles=maxG, max_J_B_all_cycles=maxJ, max_E_all_cycles=maxE,
        max_G_B_single_period=maxG1, max_J_B_single_period=maxJ1,
        local_assignments_checked_normal=sum(v['locally_assigned_demands'] for v in local_units),
        exact_requested_witness='NOT FOUND', entire_declared_mode_class='EXCLUDED',
        new_finite_key_sizes=0, finite_fits=0, A_witness_searches=0, adaptive_tour_changes=0, FI_UD_cut_trials=0,
        general_non_scanning_two_reset_nonexistence_claimed=False,
        strict_FI_only_coverage='NOT ESTABLISHED', universal_CD='OPEN', matching_terminal_line='FROZEN')
    save('independent_audit.json', result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
