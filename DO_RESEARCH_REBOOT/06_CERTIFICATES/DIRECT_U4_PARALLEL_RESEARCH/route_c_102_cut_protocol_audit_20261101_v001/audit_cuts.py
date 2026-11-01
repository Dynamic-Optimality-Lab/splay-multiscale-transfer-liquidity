"""Fixed source witness, established UD/FI rules, all102 physical cuts.

No source engine imports, old writers, new word/size fits, or startup credit.
"""
import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
NI = HERE.parent / 'route_c_nowhere_immediate_residual_20261101_v001'
UD = HERE.parent / 'route_c_unbounded_depth_charging_20261031_v001'
FI = HERE.parent / 'route_c_first_intervention_ceiling_20261031_v001'
STAGE = ROOT / 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'


def read(p):
    return json.loads(p.read_text(encoding='utf-8'))


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def save(name, value):
    with (HERE / name).open('x', encoding='utf-8') as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
        f.write('\n')


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def path(tree, key):
    nodes, directions = [], []
    while tree is not None:
        nodes.append(tree[0])
        if tree[0] == key:
            return nodes, directions
        side = 'L' if key < tree[0] else 'R'
        directions.append(side)
        tree = tree[1 if side == 'L' else 2]
    raise AssertionError('present source key')


def depth(tree, key):
    return len(path(tree, key)[1])


def envelope(tree, x, y):
    px, directions = path(tree, x)
    py, _ = path(tree, y)
    d, h = len(directions), len(py)-1
    common = 0
    while common < min(len(px), len(py)) and px[common] == py[common]:
        common += 1
    ops = []
    for index in range(d//2):
        top = d-2*(index+1)
        ops.append(dict(case=''.join(directions[top:top+2]), site_depth=top,
            grandparent=px[top], parent=px[top+1]))
    if d % 2:
        ops.append(dict(case='ZIG', site_depth=0, grandparent=px[0], parent=None))
    role = 'root_noop' if d == 0 else ('accessed' if x == y else None)
    entry = None
    mu = outer = matched = 0
    candidate = h
    if role == 'accessed':
        candidate = 0
    if role is None:
        entry = next(i for i, op in enumerate(ops) if op['site_depth'] <= common-1)
        op = ops[entry]
        if op['case'] == 'ZIG':
            role = 'zig_root' if y == op['grandparent'] else 'zig_fringe'
            mu = 1
        elif y == op['parent']:
            role, mu = 'parent', 0
        else:
            role = 'grandparent' if y == op['grandparent'] else 'fringe'
            mu = 2
        following = [op for op in ops[entry+1:] if op['case'] != 'ZIG']
        outer = len(following)
        matching = 'LL' if y < x else 'RR'
        matched = sum(op['case'] == matching for op in following)
        candidate = h+mu-outer-matched
    return dict(source_depth=h, access_depth=d, lca_depth=common-1, operations=ops,
        entry_operation=entry, entry_role=role, first_gain_allowance=mu,
        outer_doubles=outer, matching_outer_doubles=matched,
        target_side='equal' if y == x else ('left' if y < x else 'right'),
        upper_depth=min(h+2, max(0, candidate)))


def fact_table(rows):
    n = len(rows)
    positives = [i for i, row in enumerate(rows) if row['delta'] > 0]
    payers = [i for i, row in enumerate(rows) if row['delta'] <= 0]
    facts = {}
    for i in positives:
        post = rows[i]['destination_B']
        for j in payers:
            y = rows[j]['key']
            distance = (j-i) % n
            assert distance > 0
            between = [(i+k) % n for k in range(1, distance)
                if rows[(i+k) % n]['mode'] == 'KEEP' and rows[(i+k) % n]['d_B'] > 0]
            h, k = depth(post, y), len(between)
            keep = rows[j]['mode'] == 'KEEP'
            old = h//2+k if keep else 0
            first = between[0] if between else None
            profile, actual = None, None
            fresh = old
            if between:
                fr = rows[first]
                assert fr['source_B'] == post
                profile = envelope(fr['source_B'], fr['key'], y)
                assert [op['case'] for op in profile['operations']] == [ev[0] for ev in fr['B_events']]
                actual = depth(fr['destination_B'], y)
                assert actual <= profile['upper_depth']
                fresh = profile['upper_depth']//2+k-1 if keep else 0
            assert rows[j]['q'] <= fresh <= old
            facts[f'{i}:{j}'] = dict(anchor=i, payer=j, tracked_key=y, h=h, k=k,
                cyclic_distance=distance, intervening_B_changes=between,
                first_intervention=first, frame_profile=profile,
                actual_first_post_depth_for_verification=actual,
                UD_ceiling=old, FI_ceiling=fresh, actual_payer_q_for_validation=rows[j]['q'])
    return facts


def scan(rows, facts, protocol, cut, orientation):
    n = len(rows)
    units = {i: [[0, i, e, bit] for e in range(row['a']) for bit in [0, 1]] for i, row in enumerate(rows)}
    demands = {i: [[0, i, e] for e, ev in enumerate(row['B_events']) if ev[0] != 'ZIG'] for i, row in enumerate(rows)}
    history, cursors, steps, assignments = [], {}, [], []
    for turn in range(n):
        j = (cut+turn) % n
        row, cap = rows[j], len(units[j])
        history_before = list(history)
        debt_before = sum(rows[i]['delta']-cursors[i] for i in history)
        if row['delta'] > 0:
            for d, u in zip(demands[j][:cap], units[j]):
                assignments.append(dict(demand=d, unit=u, kind='positive_own'))
            history.append(j)
            cursors[j] = 0
            step = dict(turn=turn, occurrence=j, key=row['key'], kind='positive', capacity=cap,
                q=row['q'], history_before=history_before, fact_ids=[], minimum_ceiling=None,
                reservation=cap, own_units_used=cap, loans=[], suffix_end=cap,
                retired_unused=0, debt_before=debt_before)
        else:
            ids = [f'{i}:{j}' for i in history]
            ceiling = min(facts[s][protocol+'_ceiling'] for s in ids) if ids else None
            reserve = min(cap, ceiling) if ids else cap
            assert row['q'] <= reserve
            for d, u in zip(demands[j], units[j][:reserve]):
                assignments.append(dict(demand=d, unit=u, kind='payer_own'))
            cursor, loans = reserve, []
            for i in history:
                owed = rows[i]['delta']-cursors[i]
                amount = min(owed, cap-cursor)
                if amount <= 0:
                    continue
                offset = cursors[i]
                ds = demands[i][2*rows[i]['a']+offset:2*rows[i]['a']+offset+amount]
                us = units[j][cursor:cursor+amount]
                assert len(ds) == len(us) == amount
                for d, u in zip(ds, us):
                    assignments.append(dict(demand=d, unit=u, kind='loan'))
                loans.append(dict(anchor=i, residual_start=offset, residual_end=offset+amount,
                    unit_start=cursor, unit_end=cursor+amount))
                cursors[i] += amount
                cursor += amount
            step = dict(turn=turn, occurrence=j, key=row['key'], kind='payer', capacity=cap,
                q=row['q'], history_before=history_before, fact_ids=ids, minimum_ceiling=ceiling,
                reservation=reserve, own_units_used=row['q'], loans=loans, suffix_end=cursor,
                retired_unused=cap-row['q']-(cursor-reserve), debt_before=debt_before)
        step.update(history_after=list(history), residual_cursors=[[i, cursors[i]] for i in history],
            debt_after=sum(rows[i]['delta']-cursors[i] for i in history))
        steps.append(step)
    unpaid = [dict(anchor=i, remaining=rows[i]['delta']-cursors[i],
        demands=demands[i][2*rows[i]['a']+cursors[i]:]) for i in history if rows[i]['delta'] > cursors[i]]
    ds = [tuple(a['demand']) for a in assignments]
    us = [tuple(a['unit']) for a in assignments]
    assert len(ds) == len(set(ds)) == len(us) == len(set(us))
    assert len(assignments)+sum(t['remaining'] for t in unpaid) == sum(len(x) for x in demands.values()) == 98
    allunits = {tuple(u) for pool in units.values() for u in pool}
    alldemands = {tuple(d) for pool in demands.values() for d in pool}
    assert set(us) <= allunits and set(ds) <= alldemands
    if not unpaid:
        assert set(ds) == alldemands
    return dict(pass_namespace=f'{orientation}:{protocol}:cut{cut}', orientation=orientation,
        protocol=protocol, cut=cut, periods_scanned=1, startup_units_used=0,
        accepted=not unpaid, final_debt=sum(t['remaining'] for t in unpaid), unpaid=unpaid,
        steps=steps, assignments=assignments, assigned_demands=len(assignments),
        unused_physical_units=274-len(assignments), pool_visits=n, physical_period_id=0)


def compact(trial):
    return dict(cut=trial['cut'], accepted=trial['accepted'], final_debt=trial['final_debt'],
        unpaid=trial['unpaid'], loans=[dict(payer=s['occurrence'], **loan)
            for s in trial['steps'] for loan in s['loans']], assigned_demands=trial['assigned_demands'])


def main():
    inherited = read(NI / 'entry_source_pins.json')
    pins = dict(inherited['files'])
    for rel, h in pins.items():
        assert sha(ROOT / rel) == h, rel
    for p in HERE.parent.rglob('*'):
        if p.is_file() and HERE not in p.parents:
            pins[p.relative_to(ROOT).as_posix()] = sha(p)
    stage = {p.relative_to(STAGE).as_posix(): sha(p) for p in STAGE.rglob('*') if p.is_file()}
    assert stage == inherited['stage_files'] and len(stage) == 125
    assert (git('rev-parse', 'HEAD'), git('branch', '--show-current'),
        git('status', '--porcelain=v1', '--untracked-files=no')) == (inherited['head'], inherited['branch'], '')
    save('entry_source_pins.json', dict(date='2026-11-01', files=pins, stage_files=stage,
        head=inherited['head'], branch=inherited['branch'], tracked_status='',
        gate_sha256=sha(HERE / 'CA00_FOUR_RULE_GATE.md')))
    for name, h in read(NI / 'delivery_manifest.json')['files'].items():
        assert sha(NI / name) == h
    nia = read(NI / 'independent_audit.json')
    assert nia['status'] == 'PASS'
    assert nia['full_source_replays_sha256'] == sha(NI / 'full_source_replays.json')
    assert read(FI / 'independent_audit.json')['status'] == 'PASS'
    replay = read(NI / 'full_source_replays.json')
    rows, mirror_rows = replay['cycle'], replay['mirrored_cycle']
    assert len(rows) == len(mirror_rows) == 102
    for rs in [rows, mirror_rows]:
        for i, row in enumerate(rs):
            assert row['occurrence'] == i and row['a'] > 0
            assert row['source_A'] == rs[i-1]['destination_A'] and row['source_B'] == rs[i-1]['destination_B']
            assert row['key'] != rs[i-1]['key']
            assert row['delta'] == row['q']-2*row['a']
            assert row['mode'] == 'KEEP' or not row['B_events']
        assert (sum(r['a'] for r in rs), sum(r['q'] for r in rs)) == (137, 98)
    normals, reflected = fact_table(rows), fact_table(mirror_rows)
    assert len(normals) == len(reflected) == 485
    save('source_fact_table.json', dict(source_replays_sha256=sha(NI / 'full_source_replays.json'),
        UD_rule_sha256=sha(UD / 'UD01_ARBITRARY_DEPTH_SPLIT_PAYER_THEOREM.md'),
        FI_rule_sha256=sha(FI / 'FI01_SOURCE_FRAME_CEILING_AND_CHARGING.md'),
        normal=normals, reflected=reflected, first_entry_method='original source LCA depth',
        actual_first_post_depth_used_only_for_verification=True,
        actual_payer_q_substituted_for_ceiling=False, exact_repeated_depth_propagation=False))
    trials = {}
    for orientation, rs, fs in [('normal', rows, normals), ('reflected', mirror_rows, reflected)]:
        trials[orientation] = {}
        for protocol in ['UD', 'FI']:
            trials[orientation][protocol] = [scan(rs, fs, protocol, cut, orientation) for cut in range(102)]
        for cut in range(102):
            old, fresh = trials[orientation]['UD'][cut], trials[orientation]['FI'][cut]
            for os, ns in zip(old['steps'], fresh['steps']):
                assert os['history_after'] == ns['history_after']
                assert ns['reservation'] <= os['reservation']
                assert ns['debt_after'] <= os['debt_after']
            assert not old['accepted'] or fresh['accepted']
    for protocol in ['UD', 'FI']:
        for a, b in zip(trials['normal'][protocol], trials['reflected'][protocol]):
            assert compact(a) == compact(b)
    save('cut_ledgers.json', dict(schema='fixed102-cut-UD-FI-ledgers-v1',
        source_fact_table_sha256=sha(HERE / 'source_fact_table.json'),
        physical_period_ids_allowed=[0], prefix_occurrences_allowed=[],
        independent_pass_namespaces=True, trials=trials))
    ud = [t['cut'] for t in trials['normal']['UD'] if t['accepted']]
    fi = [t['cut'] for t in trials['normal']['FI'] if t['accepted']]
    new = sorted(set(fi)-set(ud))
    status = 'STRICT_FI_ONLY_WITNESS_VERIFIED' if not ud and fi else (
        'FIXED_WITNESS_SEPARATION_REFUTED_UD_ACCEPTS' if ud else 'BOTH_REJECT_ALL_CUTS')
    selected = {}
    for protocol, accepted in [('UD', ud), ('FI', fi)]:
        cut = accepted[0] if accepted else 0
        trial = trials['normal'][protocol][cut]
        selected[protocol] = dict(cut=cut, accepted=trial['accepted'], final_debt=trial['final_debt'],
            repayments=[dict(payer=s['occurrence'], payer_mode=rows[s['occurrence']]['mode'],
                payer_key=s['key'], capacity=s['capacity'], reservation=s['reservation'],
                history=s['history_before'], minimum_ceiling=s['minimum_ceiling'],
                fact=normals[f"{loan['anchor']}:{s['occurrence']}"], **loan)
                for s in trial['steps'] for loan in s['loans']])
    summary = dict(status=status, date='2026-11-01', gate_sha256=sha(HERE / 'CA00_FOUR_RULE_GATE.md'),
        source_replays_sha256=sha(NI / 'full_source_replays.json'),
        fact_table_sha256=sha(HERE / 'source_fact_table.json'), cut_ledgers_sha256=sha(HERE / 'cut_ledgers.json'),
        cuts_per_protocol=102, normal_passes=204, reflected_passes=204, periods_per_pass=1,
        UD_accepted_cuts=ud, FI_accepted_cuts=fi, FI_additional_accepted_cuts=new,
        UD_final_debt_histogram=dict(Counter(t['final_debt'] for t in trials['normal']['UD'])),
        FI_final_debt_histogram=dict(Counter(t['final_debt'] for t in trials['normal']['FI'])),
        selected_ledgers=selected, source_cycle_actions=102, A=137, Q_B=98, Z_B=63,
        E=5, C_D=4, G_B=5, J_B=5, R_imm=5, nowhere_diagonal=True,
        recurrent_resets=2, reused_units=0, startup_units_used=0, new_source_engine_calls=0,
        larger_finite_fits=0, new_source_words=0, source_word_searches=0,
        strict_new_FI_closed_walk_coverage=bool(not ud and fi),
        matching_terminal_line='FROZEN', universal_CD='OPEN', automatic_successor_launched=False)
    save('cut_summary.json', summary)
    print(json.dumps(dict(status=status, UD_accepted_count=len(ud), FI_accepted_count=len(fi),
        UD_accepted_cuts=ud, FI_additional_cuts=new,
        UD_final_debt_histogram=summary['UD_final_debt_histogram'],
        FI_final_debt_histogram=summary['FI_final_debt_histogram'],
        selected_repayments={p: [dict(anchor=r['anchor'], payer=r['payer'], key=r['payer_key'],
            mode=r['payer_mode'], reserve=r['reservation'], capacity=r['capacity'],
            h=r['fact']['h'], k=r['fact']['k'], c_UD=r['fact']['UD_ceiling'], c_FI=r['fact']['FI_ceiling'])
            for r in selected[p]['repayments']] for p in ['UD', 'FI']},
        preserved_files=len(pins)), indent=2))


if __name__ == '__main__':
    main()
