"""One proved closed A tour, all 276 two-DELETE assignments, no larger fits."""
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
OLD = HERE.parent / 'route_c_alternating_extreme_resets_20261031_v001'
STAGE = ROOT / 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'
TOUR = [3, 2, 4, 6, 5, 7, 9, 8, 10, 12, 11, 13, 11, 12, 10, 8, 9, 7, 5, 6, 4, 2, 3, 1]
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
    doubled = word * 2
    for i in range(len(word)):
        for low in (1, 2):
            asc = list(range(low, low+12))
            for orient, pattern in [('ascending', asc), ('descending', asc[::-1])]:
                if doubled[i:i+12] == pattern:
                    out.append(dict(start=i, low=low, orientation=orient))
    return out


def budgets(q):
    used = set()
    pairs = []
    for i, value in enumerate(q):
        j = (i+1) % len(q)
        if value >= 3 and q[j] <= 1:
            assert i not in used and j not in used
            used.update((i, j))
            pairs.append(dict(high=i, helper=j, q_high=value, q_helper=q[j],
                residual_upper_bound=max(value+q[j]-4, 0)))
    G = sum(max(value-2, 0) for value in q)
    J = sum(v['residual_upper_bound'] for v in pairs) + sum(max(value-2, 0) for i, value in enumerate(q) if i not in used)
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
        gate_sha256=sha(HERE / 'AT00_FOUR_RULE_GATE.md')))
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

    def T(root):
        left = L
        for key in range(1, root):
            left = s.node(key, left, L)
        right = L
        for key in range(13, root, -1):
            right = s.node(key, L, right)
        return s.node(root, left, right)

    assert len(TOUR) == 24 and not scans(TOUR)
    initial = T(1)
    A = initial
    a_trees = [A]
    a_rows = []
    for i, key in enumerate(TOUR):
        before = A
        A, d, ev, q, z = access(A, key)
        assert 1 <= d <= 2 and len(ev) == 1 and A == T(key)
        a_rows.append(dict(position=i, key=key, source_A=raw(before), destination_A=raw(A),
            d_A=d, a=1, A_events=ev))
        a_trees.append(A)
    assert A == initial
    save('closed_A_identity_certificate.json', dict(schema='closed-root-position-tour-v1', date='2026-10-31',
        key_size=13, initial_diagonal=raw(initial), tour=TOUR, A_trace=a_rows, source_A_sweeps=[],
        A_closes=True, grouped_A_per_lap=24, all_actions_one_StepEv=True,
        every_two_mode_omissions_pure_C_D_per_lap=4, universal_identity='S_x T_r=T_x for 1<=abs(x-r)<=2',
        finite_A_source_calls=calls))

    cases = []
    selected = None
    outcomes = Counter()
    periods = Counter()
    transients = Counter()
    max_g = max_j = -1
    for case_index, omitted in enumerate(itertools.combinations(range(24), 2)):
        omitted = list(omitted)
        modes = ['DELETE' if i in omitted else 'KEEP' for i in range(24)]
        keep_word = [key for i, key in enumerate(TOUR) if modes[i] == 'KEEP']
        keep_scans = scans(keep_word)
        b = initial
        seen = {b: 0}
        boundaries = [dict(lap=0, B=raw(b))]
        rows = []
        start = end = None
        for lap in range(1, CAP+1):
            for i, key in enumerate(TOUR):
                pre = b
                if modes[i] == 'KEEP':
                    b, d, ev, q, z = access(b, key)
                else:
                    d, ev, q, z = None, [], 0, 0
                rows.append(dict(occurrence=len(rows), lap=lap-1, position=i, mode=modes[i], key=key,
                    d_A=a_rows[i]['d_A'], a=1, d_B=d, q=q, z=z, B_events=ev,
                    source_pair_sha256=digest([a_rows[i]['source_A'], raw(pre)]),
                    destination_pair_sha256=digest([a_rows[i]['destination_A'], raw(b)]),
                    diagonal_before=a_trees[i] == pre, diagonal_after=a_trees[i+1] == b))
            boundaries.append(dict(lap=lap, B=raw(b)))
            if b in seen:
                start, end = seen[b], lap
                break
            seen[b] = lap
        cycle = None
        if start is None:
            outcome = 'OPEN_FIRST_REPEAT_CAP'
        else:
            p = end-start
            cyc = rows[24*start:24*end]
            kept = [r for r in cyc if r['mode'] == 'KEEP']
            q = [r['q'] for r in kept]
            G, J, helper_pairs = budgets(q)
            E = sum(max(r['q']-2*r['a'], 0) for r in cyc)
            CD = sum(2*r['a'] for r in cyc if r['mode'] == 'DELETE')
            diag = [i for i, r in enumerate(cyc) if r['diagonal_before']]
            assert E == G and CD == 4*p and len(cyc) == 24*p
            assert boundaries[start]['B'] == boundaries[end]['B']
            cycle = dict(transient_laps=start, period_laps=p, source_start=24*start, source_end=24*end,
                source_B=boundaries[start]['B'], paired_closed=True, cycle_length=24*p,
                resets=2*p, A=24*p, C_D=CD, E=E, Q_B=sum(q), Z_B=sum(r['z'] for r in kept),
                G_B=G, J_B=J, q_profile=q, immediate_helper_pairs=helper_pairs,
                diagonal_source_occurrences=diag,
                distinct_source_pairs=len({r['source_pair_sha256'] for r in cyc}),
                kept_key_count=len(set(keep_word)), KEEP_core_sweeps=keep_scans)
            periods[p] += 1
            transients[start] += 1
            if p == 1:
                max_g, max_j = max(max_g, G), max(max_j, J)
            if p != 1:
                outcome = 'MORE_THAN_TWO_PHYSICAL_RESETS'
            elif keep_scans:
                outcome = 'CONSECUTIVE_CORE_SCAN'
            elif G < 5:
                outcome = 'G_BELOW_FIVE'
            elif J < 5:
                outcome = 'J_BELOW_FIVE'
            elif diag:
                outcome = 'BUDGET_HIT_WITH_DIAGONAL_STATES'
            else:
                outcome = 'REQUESTED_COMPONENT_CERTIFIED'
        case = dict(case_index=case_index, DELETE_positions=omitted, modes=modes, KEEP_word=keep_word,
            boundary_records=boundaries, orbit_replay=rows, cycle=cycle, outcome=outcome)
        cases.append(case)
        outcomes[outcome] += 1
        if outcome == 'REQUESTED_COMPONENT_CERTIFIED':
            selected = case_index
            break
        if (case_index+1) % 50 == 0:
            print(json.dumps(dict(cases_completed=case_index+1, max_single_period_G_B=max_g,
                max_single_period_J_B=max_j)), flush=True)
    overall = ('REQUESTED_COMPONENT_CERTIFIED' if selected is not None else
        ('OPEN_CAP_CASES' if outcomes['OPEN_FIRST_REPEAT_CAP'] else 'EXACT_MODE_CLASS_EXCLUDED'))
    result = dict(schema='closed-A-two-omission-class-v1', date='2026-10-31', key_size=13,
        tour=TOUR, initial_diagonal=raw(initial), cap=CAP, declared_mode_assignments=276,
        cases=cases, outcome=overall, outcomes=dict(outcomes), periods=dict(periods), transients=dict(transients),
        max_G_B_single_period=max_g, max_J_B_single_period=max_j, selected_case=selected,
        all_declared_cases_examined=len(cases) == 276, first_success_stops_class=True,
        tuple_source_calls=calls, A_closure_assumed=False, A_witness_searches=0,
        finite_fits=0, new_finite_key_sizes=0, adaptive_tour_changes=0, FI_UD_cut_trials=0,
        universal_CD='OPEN', strict_FI_only_coverage='NOT ESTABLISHED', matching_terminal_line='FROZEN')
    save('mode_class_certificate.json', result)
    print(json.dumps(dict(outcome=overall, cases=len(cases), outcomes=dict(outcomes), periods=dict(periods),
        transients=dict(transients), max_G_B_single_period=max_g, max_J_B_single_period=max_j,
        selected_case=selected, tuple_source_calls=calls, preserved_files=len(pins), stage_files=len(stage)), indent=2))


if __name__ == '__main__':
    main()
