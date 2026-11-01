"""One recurrent A clock and all 265 fixed two-child-return source words."""
import hashlib
import importlib.util
import itertools
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OLD = HERE.parent / 'route_c_closed_A_tour_20261031_v001'
STAGE = ROOT / 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'
BASE = [13, 11, 12, 9, 10, 7, 8, 5, 6, 3, 4, 1, 2]
EXPECTED_A = [5, 3, 1, 3, 2, 3, 2, 2, 1, 2, 1, 2, 1]
CAP = 64


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':'), ensure_ascii=False).encode('utf-8')).hexdigest()


def save(name, value):
    with (HERE / name).open('x', encoding='utf-8') as f:
        json.dump(value, f, indent=2, ensure_ascii=False)
        f.write('\n')


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def scans(word):
    out = []
    for i in range(len(word)):
        for low in (1, 2):
            asc = list(range(low, low+12))
            for orient, pat in [('ascending', asc), ('descending', asc[::-1])]:
                if (word+word)[i:i+12] == pat:
                    out.append(dict(start=i, low=low, orientation=orient))
    return out


def budgets(q):
    used, pairs = set(), []
    for i, value in enumerate(q):
        j = (i+1) % len(q)
        if value >= 3 and q[j] <= 1:
            assert i not in used and j not in used
            used.update((i, j))
            pairs.append(dict(high=i, helper=j, q_high=value, q_helper=q[j],
                residual_upper_bound=max(value+q[j]-4, 0)))
    G = sum(max(v-2, 0) for v in q)
    J = sum(p['residual_upper_bound'] for p in pairs) + sum(max(v-2, 0) for i, v in enumerate(q) if i not in used)
    return G, J, pairs


def main():
    inherited = json.loads((OLD / 'entry_source_pins.json').read_text(encoding='utf-8'))
    pins = dict(inherited['files'])
    for rel, h in pins.items():
        assert sha(ROOT / rel) == h, rel
    for p in HERE.parent.rglob('*'):
        if p.is_file() and HERE not in p.parents:
            pins[p.relative_to(ROOT).as_posix()] = sha(p)
    stage = {p.relative_to(STAGE).as_posix(): sha(p) for p in STAGE.rglob('*') if p.is_file()}
    assert stage == inherited['stage_files'] and len(stage) == 125
    assert not git('status', '--porcelain=v1', '--untracked-files=no')
    assert (git('rev-parse', 'HEAD'), git('branch', '--show-current')) == (inherited['head'], inherited['branch'])
    save('entry_source_pins.json', dict(date='2026-10-31', head=inherited['head'], branch=inherited['branch'],
        tracked_status='', files=pins, stage_files=stage, inherited_pins=len(inherited['files']),
        gate_sha256=sha(HERE / 'CR00_FOUR_RULE_GATE.md')))
    spec = importlib.util.spec_from_file_location('tuple_source', ROOT / 'python/independent/splay.py')
    s = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(s)
    L = s.LEAF
    calls = 0

    def raw(t):
        return None if t == L else [t[1], raw(t[2]), raw(t[3])]

    def access(t, key):
        nonlocal calls
        assert s.inorder(t) == list(range(1, 14))
        found, d = s.lookup(t, key)
        assert found
        out, ev = s.trace(t, key)
        q, z = sum(e[0] != 'ZIG' for e in ev), sum(e[0] == 'ZIG' for e in ev)
        assert (q, z, len(ev)) == (d//2, d%2, (d+1)//2)
        assert s.inorder(out) == list(range(1, 14))
        calls += 1
        return out, d, ev, q, z

    right = L
    for key in range(13, 4, -1):
        right = s.node(key, L, right)
    initial = s.node(2, s.node(1, L, L), s.node(4, s.node(3, L, L), right))
    historical_path = HERE.parent / 'route_c_sparse_reset_strictness_20261031_v001/sparse_reset_certificate.json'
    historical = json.loads(historical_path.read_text(encoding='utf-8'))
    assert raw(initial) == historical['shared_B_boundary_states']['1']
    assert historical['skeleton'] == BASE
    A = initial
    base_rows, phase_trees = [], []
    for phase, key in enumerate(BASE):
        pre = A
        A, d, ev, q, z = access(A, key)
        base_rows.append(dict(phase=phase, role='BASE_KEEP', mode='KEEP', key=key,
            source_A=raw(pre), destination_A=raw(A), d_A=d, a=len(ev), A_events=ev))
        phase_trees.append(A)
    assert A == initial and [r['a'] for r in base_rows] == EXPECTED_A and sum(EXPECTED_A) == 28
    options = []
    by_phase = {}
    for phase, tree in enumerate(phase_trees):
        root = tree[1]
        choices = []
        for side, child in [('L', tree[2]), ('R', tree[3])]:
            if child == L:
                continue
            key = child[1]
            child_tree, d1, ev1, q1, z1 = access(tree, key)
            returned, d2, ev2, q2, z2 = access(child_tree, root)
            assert returned == tree and d1 == d2 == 1 and len(ev1) == len(ev2) == 1
            assert ev1[0][0] == ev2[0][0] == 'ZIG' and ev1[0][3] != ev2[0][3]
            option = dict(phase=phase, side=side, root_key=root, child_key=key,
                child_row=dict(phase=phase, role='CHILD_KEEP', mode='KEEP', key=key,
                    source_A=raw(tree), destination_A=raw(child_tree), d_A=1, a=1, A_events=ev1),
                return_row=dict(phase=phase, role='RESET_RETURN', mode='DELETE', key=root,
                    source_A=raw(child_tree), destination_A=raw(returned), d_A=1, a=1, A_events=ev2))
            choices.append(option)
            options.append(option)
        by_phase[phase] = choices
    assert len(options) == 24 and calls == 61
    save('A_clock_certificate.json', dict(schema='recurrent-A-child-return-clock-v1', date='2026-10-31',
        key_size=13, initial_diagonal=raw(initial), base=BASE, base_rows=base_rows, options=options,
        historical_certificate_sha256=sha(historical_path), base_grouped_A=28,
        expanded_grouped_A=32, pure_reset_C_D=4, fixed_A_source_calls=calls,
        local_identity='KEEP child then DELETE old root are inverse root zigs'))

    class_words = []
    for g, h in itertools.combinations(range(13), 2):
        for og in by_phase[g]:
            for oh in by_phase[h]:
                class_words.append((g, h, og, oh))
    assert len(class_words) == 265
    cases, outcomes, periods, transients = [], Counter(), Counter(), Counter()
    selected = None
    filters = Counter()
    maxG1 = maxJ1 = maxE1 = -1
    max_margin = None
    for case_index, (g, h, og, oh) in enumerate(class_words):
        chosen = {g: og, h: oh}
        a_word = []
        for phase, base_row in enumerate(base_rows):
            a_word.append(dict(base_row, position=len(a_word)))
            if phase in chosen:
                opt = chosen[phase]
                a_word.append(dict(opt['child_row'], position=len(a_word)))
                a_word.append(dict(opt['return_row'], position=len(a_word)))
        assert len(a_word) == 17 and sum(r['a'] for r in a_word) == 32
        assert sum(r['mode'] == 'DELETE' for r in a_word) == 2
        assert all(a_word[i]['key'] != a_word[(i+1) % 17]['key'] for i in range(17))
        assert a_word[0]['source_A'] == a_word[-1]['destination_A'] == raw(initial)
        assert all(a_word[i]['destination_A'] == a_word[(i+1) % 17]['source_A'] for i in range(17))
        source_word = [r['key'] for r in a_word]
        keep_word = [r['key'] for r in a_word if r['mode'] == 'KEEP']
        scan_hits = scans(source_word)+scans(keep_word)
        b = initial
        seen = {b: 0}
        boundaries = [dict(lap=0, B=raw(b))]
        rows, b_states = [], [b]
        start = end = None
        for lap in range(1, CAP+1):
            for i, ar in enumerate(a_word):
                pre = b
                if ar['mode'] == 'KEEP':
                    b, d, ev, q, z = access(b, ar['key'])
                else:
                    d, ev, q, z = None, [], 0, 0
                rows.append(dict(occurrence=len(rows), lap=lap-1, position=i, phase=ar['phase'],
                    role=ar['role'], mode=ar['mode'], key=ar['key'], d_A=ar['d_A'], a=ar['a'],
                    d_B=d, q=q, z=z, B_events=ev,
                    source_pair_sha256=digest([ar['source_A'], raw(pre)]),
                    destination_pair_sha256=digest([ar['destination_A'], raw(b)]),
                    diagonal_before=ar['source_A'] == raw(pre), diagonal_after=ar['destination_A'] == raw(b)))
                b_states.append(b)
            boundaries.append(dict(lap=lap, B=raw(b)))
            if b in seen:
                start, end = seen[b], lap
                break
            seen[b] = lap
        cycle = None
        if start is None:
            outcome = 'OPEN_FIRST_REPEAT_CAP'
        else:
            period = end-start
            cyc = rows[17*start:17*end]
            kept = [r for r in cyc if r['mode'] == 'KEEP']
            q = [r['q'] for r in kept]
            G, J, helpers = budgets(q)
            E = sum(max(r['q']-2*r['a'], 0) for r in cyc)
            CD = sum(2*r['a'] for r in cyc if r['mode'] == 'DELETE')
            diag = [i for i, r in enumerate(cyc) if r['diagonal_before']]
            assert CD == 4*period and sum(r['a'] for r in cyc) == 32*period
            assert boundaries[start]['B'] == boundaries[end]['B']
            cycle = dict(transient_laps=start, period_laps=period, source_start=17*start, source_end=17*end,
                source_B=boundaries[start]['B'], paired_closed=True, cycle_length=17*period,
                physical_resets=2*period, A=32*period, Q_B=sum(q), Z_B=sum(r['z'] for r in kept),
                E=E, C_D=CD, G_B=G, J_B=J, q_profile=q,
                immediate_helper_pairs=helpers, diagonal_source_occurrences=diag,
                distinct_source_pairs=len({r['source_pair_sha256'] for r in cyc}), core_scan_hits=scan_hits)
            periods[period] += 1
            transients[start] += 1
            filters['G_at_least_5'] += G >= 5
            filters['J_at_least_5'] += J >= 5
            filters['G_and_J_at_least_5'] += G >= 5 and J >= 5
            filters['E_greater_than_C_D'] += E > CD
            filters['nowhere_diagonal'] += not diag
            if period == 1:
                maxG1, maxJ1, maxE1 = max(maxG1, G), max(maxJ1, J), max(maxE1, E)
            margin = E-CD
            max_margin = margin if max_margin is None else max(max_margin, margin)
            if period != 1:
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
        case = dict(case_index=case_index, phases=[g, h], sides=[og['side'], oh['side']],
            child_keys=[og['child_key'], oh['child_key']], A_word=a_word, KEEP_word=keep_word,
            boundary_records=boundaries, orbit_replay=rows, cycle=cycle, outcome=outcome)
        cases.append(case)
        outcomes[outcome] += 1
        if outcome == 'REQUESTED_COMPONENT_CERTIFIED':
            selected = case_index
            prefix = []
            cycfull = []
            for k, r in enumerate(rows):
                ar = a_word[r['position']]
                full = dict(r, source_A=ar['source_A'], destination_A=ar['destination_A'], A_events=ar['A_events'],
                    source_B=raw(b_states[k]), destination_B=raw(b_states[k+1]))
                if k < 17*start:
                    prefix.append(full)
                else:
                    cycfull.append(dict(full, occurrence=k-17*start, original_occurrence=k))
            save('selected_witness_certificate.json', dict(case_index=case_index, initial_diagonal=raw(initial),
                reachability_prefix=prefix, full_cycle_replay=cycfull, cycle=cycle,
                matching_terminal_line='FROZEN', strict_FI_only_coverage='NOT ESTABLISHED'))
            break
        if (case_index+1) % 50 == 0:
            print(json.dumps(dict(cases_completed=case_index+1, max_single_G_B=maxG1,
                max_single_J_B=maxJ1, max_single_E=maxE1)), flush=True)
    overall = ('REQUESTED_COMPONENT_CERTIFIED' if selected is not None else
        ('OPEN_CAP_CASES' if outcomes['OPEN_FIRST_REPEAT_CAP'] else 'EXACT_CHILD_RETURN_CLASS_EXCLUDED'))
    save('child_return_class_certificate.json', dict(schema='two-child-return-source-class-v1', date='2026-10-31',
        key_size=13, initial_diagonal=raw(initial), base=BASE, cap=CAP, declared_cases=265,
        cases=cases, selected_case=selected, outcome=overall, outcomes=dict(outcomes),
        filters=dict(filters), periods=dict(periods), transients=dict(transients),
        max_G_B_single_period=maxG1, max_J_B_single_period=maxJ1, max_E_single_period=maxE1,
        max_E_minus_C_D=max_margin, all_declared_cases_examined=len(cases) == 265,
        tuple_source_calls=calls, fixed_A_source_calls=61, A_closure_assumed=False,
        A_witness_searches=0, finite_fits=0, new_finite_key_sizes=0, adaptive_clock_changes=0,
        FI_UD_cut_trials=0, matching_terminal_line='FROZEN', strict_FI_only_coverage='NOT ESTABLISHED', universal_CD='OPEN'))
    print(json.dumps(dict(outcome=overall, cases=len(cases), outcomes=dict(outcomes), filters=dict(filters),
        periods=dict(periods), transients=dict(transients), max_G_B_single_period=maxG1,
        max_J_B_single_period=maxJ1, max_E_single_period=maxE1, max_E_minus_C_D=max_margin,
        selected_case=selected, tuple_source_calls=calls, preserved_files=len(pins), stage_files=len(stage)), indent=2))


if __name__ == '__main__':
    main()
