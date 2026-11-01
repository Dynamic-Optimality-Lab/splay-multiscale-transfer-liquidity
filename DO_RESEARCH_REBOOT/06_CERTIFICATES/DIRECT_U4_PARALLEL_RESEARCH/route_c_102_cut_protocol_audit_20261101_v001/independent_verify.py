"""Independent fixed-cut verification by source-subtree entry and debt queues.

No producer import, splay engine, old writer, new word or size fit. All ledgers
are checked against independent facts and unit-by-unit FIFO assignments.
"""
import hashlib
import json
import sys
from collections import Counter, deque
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
NI = HERE.parent / 'route_c_nowhere_immediate_residual_20261101_v001'
UD = HERE.parent / 'route_c_unbounded_depth_charging_20261031_v001'
FI = HERE.parent / 'route_c_first_intervention_ceiling_20261031_v001'
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
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')


def nodes_to(tree, key):
    result = []
    while tree is not None:
        result.append(tree)
        if tree[0] == key:
            return result
        tree = tree[1 if key < tree[0] else 2]
    raise AssertionError('present source key')


def depth(tree, key):
    return len(nodes_to(tree, key))-1


def keys(tree):
    return [] if tree is None else keys(tree[1])+[tree[0]]+keys(tree[2])


def mirror(tree):
    return None if tree is None else [14-tree[0], mirror(tree[2]), mirror(tree[1])]


def reflected_events(events):
    cases = dict(LL='RR', RR='LL', LR='RL', RL='LR', ZIG='ZIG')
    orient = {'L': 'R', 'R': 'L', '-': '-'}
    return [[cases[kind], 14-hi, 14-lo, orient[o]] for kind, lo, hi, o in events]


def original_frame_ceiling(tree, x, y, source_events):
    px, py = nodes_to(tree, x), nodes_to(tree, y)
    d, h = len(px)-1, len(py)-1
    common = 0
    while common < min(len(px), len(py)) and px[common][0] == py[common][0]:
        common += 1
    ops = []
    for top in range(d-2, -1, -2):
        g, p = px[top][0], px[top+1][0]
        case = ('L' if x < g else 'R')+('L' if x < p else 'R')
        ops.append(dict(case=case, site_depth=top, grandparent=g, parent=p))
    if d % 2:
        ops.append(dict(case='ZIG', site_depth=0, grandparent=tree[0], parent=None))
    ck([op['case'] for op in ops] == [e[0] for e in source_events], 'original source frame word agrees with recorded source')
    entry = None
    gain = outer = matched = 0
    if d == 0:
        role, cap = 'root_noop', h
    elif x == y:
        role, cap = 'accessed', 0
    else:
        # Original subtree membership determines entry, without the LCA test.
        entry = next(i for i, op in enumerate(ops)
            if y in keys(nodes_to(tree, op['grandparent'])[-1]))
        op = ops[entry]
        if op['case'] == 'ZIG':
            role = 'zig_root' if y == op['grandparent'] else 'zig_fringe'
            gain = 1
        elif y == op['parent']:
            role, gain = 'parent', 0
        else:
            role = 'grandparent' if y == op['grandparent'] else 'fringe'
            gain = 2
        later = [op['case'] for op in ops[entry+1:] if op['case'] != 'ZIG']
        outer = len(later)
        matched = later.count('LL' if y < x else 'RR')
        cap = h+gain-outer-matched
    return dict(source_depth=h, access_depth=d, lca_depth=common-1, operations=ops,
        entry_operation=entry, entry_role=role, first_gain_allowance=gain,
        outer_doubles=outer, matching_outer_doubles=matched,
        target_side='equal' if x == y else ('left' if y < x else 'right'),
        upper_depth=min(h+2, max(0, cap)))


def independent_facts(rows):
    facts = {}
    for i, anchor in enumerate(rows):
        if anchor['delta'] <= 0:
            continue
        changes = []
        for distance in range(1, len(rows)):
            j = (i+distance) % len(rows)
            payer = rows[j]
            if payer['delta'] <= 0:
                y = payer['key']
                h = depth(anchor['destination_B'], y)
                old = h//2+len(changes) if payer['mode'] == 'KEEP' else 0
                new, profile, actual = old, None, None
                first = changes[0] if changes else None
                if first is not None:
                    row = rows[first]
                    ck(row['source_B'] == anchor['destination_B'], 'first intervention has exact post-anchor source tree')
                    profile = original_frame_ceiling(row['source_B'], row['key'], y, row['B_events'])
                    actual = depth(row['destination_B'], y)
                    ck(actual <= profile['upper_depth'] <= h+2, 'first post depth checked after source-only frame estimate')
                    new = profile['upper_depth']//2+len(changes)-1 if payer['mode'] == 'KEEP' else 0
                ck(payer['q'] <= new <= old, 'each source fact covers own work and FI refines UD')
                facts[f'{i}:{j}'] = dict(anchor=i, payer=j, tracked_key=y, h=h, k=len(changes),
                    cyclic_distance=distance, intervening_B_changes=list(changes), first_intervention=first,
                    frame_profile=profile, actual_first_post_depth_for_verification=actual,
                    UD_ceiling=old, FI_ceiling=new, actual_payer_q_for_validation=payer['q'])
            # Update only AFTER evaluating the current payer: strictly between.
            if payer['mode'] == 'KEEP' and payer['d_B'] > 0:
                changes.append(j)
    return facts


def independently_scan(rows, facts, protocol, cut, orientation):
    cap = {i: 2*row['a'] for i, row in enumerate(rows)}
    credits = {i: [[0, i, e, b] for e in range(row['a']) for b in [0, 1]] for i, row in enumerate(rows)}
    demands = {i: [[0, i, e] for e, ev in enumerate(row['B_events']) if ev[0] != 'ZIG'] for i, row in enumerate(rows)}
    legal_units = {tuple(u) for v in credits.values() for u in v}
    legal_demands = {tuple(d) for v in demands.values() for d in v}
    seen_units, seen_demands, visited = set(), set(), set()
    claims, steps, history, progress, pending = [], [], [], {}, deque()

    def claim(demand, unit, kind, donor):
        ck(tuple(demand) in legal_demands and tuple(unit) in legal_units, 'physical source demand and unit membership')
        ck(demand[0] == unit[0] == 0 and 0 <= demand[1] < 102 and 0 <= unit[1] < 102, 'one physical period only and no startup ID')
        ck(tuple(demand) not in seen_demands and tuple(unit) not in seen_units, 'no unit or demand reused within pass')
        ck(unit[1] == donor, 'donor pool is the current physical occurrence')
        seen_demands.add(tuple(demand))
        seen_units.add(tuple(unit))
        claims.append(dict(demand=demand, unit=unit, kind=kind))

    for turn, j in enumerate(list(range(cut, 102))+list(range(cut))):
        ck(j not in visited, 'physical pool visited exactly once')
        visited.add(j)
        row = rows[j]
        before = sum(len(rem) for _, rem in pending)
        hist = list(history)
        if row['delta'] > 0:
            for k in range(cap[j]):
                claim(demands[j][k], credits[j][k], 'positive_own', j)
            history.append(j)
            progress[j] = 0
            pending.append((j, deque(demands[j][cap[j]:])))
            ids, minimum, reserved, outgoing, loans = [], None, cap[j], cap[j], []
            own, retired, kind = cap[j], 0, 'positive'
        else:
            ids = [f'{i}:{j}' for i in history]
            minimum = min(facts[s][protocol+'_ceiling'] for s in ids) if ids else None
            reserved = cap[j] if minimum is None else min(cap[j], minimum)
            ck(row['q'] <= reserved, 'one frozen reservation covers own demands')
            for k in range(row['q']):
                claim(demands[j][k], credits[j][k], 'payer_own', j)
            outgoing, loans = reserved, []
            while outgoing < cap[j] and pending:
                anchor, remaining = pending[0]
                ck(anchor in history and anchor != j, 'loan only to a previously encountered positive')
                offset, start_unit, count = progress[anchor], outgoing, 0
                while outgoing < cap[j] and remaining:
                    ck(outgoing >= reserved, 'loans use only suffix outside own reservation')
                    claim(remaining.popleft(), credits[j][outgoing], 'loan', j)
                    outgoing += 1
                    progress[anchor] += 1
                    count += 1
                loans.append(dict(anchor=anchor, residual_start=offset, residual_end=offset+count,
                    unit_start=start_unit, unit_end=outgoing))
                if not remaining:
                    pending.popleft()
            own, retired, kind = row['q'], cap[j]-row['q']-(outgoing-reserved), 'payer'
        ck(sum(1 for u in seen_units if u[1] == j) == cap[j]-retired, 'physical pool retired with exact unused unit count')
        after = sum(len(rem) for _, rem in pending)
        ck(after == (before+row['delta'] if row['delta'] > 0 else max(0, before-(cap[j]-reserved))), 'deterministic total debt recurrence')
        # History remains complete even when the queue has no debt for an anchor.
        ck(set(progress) == set(history), 'paid anchor facts retained in history')
        step = dict(turn=turn, occurrence=j, key=row['key'], kind=kind, capacity=cap[j], q=row['q'],
            history_before=hist, fact_ids=ids, minimum_ceiling=minimum, reservation=reserved,
            own_units_used=own, loans=loans, suffix_end=outgoing, retired_unused=retired, debt_before=before,
            history_after=list(history), residual_cursors=[[i, progress[i]] for i in history], debt_after=after)
        steps.append(step)
    ck(visited == set(range(102)), 'all102 recurrent pools visited once')
    remaining_by_anchor = {i: list(rem) for i, rem in pending}
    unpaid = [dict(anchor=i, remaining=len(remaining_by_anchor[i]), demands=remaining_by_anchor[i])
        for i in history if i in remaining_by_anchor]
    unassigned = legal_demands-seen_demands
    ck(unassigned == {tuple(d) for u in unpaid for d in u['demands']}, 'rejected tail exactly equals unassigned demand identities')
    ck(len(claims)+len(unassigned) == 98 and len(legal_units) == 274, 'exact one-period capacity and demand accounting')
    if not unpaid:
        ck(seen_demands == legal_demands and len(seen_units) == 98, 'accepted pass is a full98-demand injection')
    return dict(pass_namespace=f'{orientation}:{protocol}:cut{cut}', orientation=orientation,
        protocol=protocol, cut=cut, periods_scanned=1, startup_units_used=0,
        accepted=not unpaid, final_debt=len(unassigned), unpaid=unpaid, steps=steps,
        assignments=claims, assigned_demands=len(claims), unused_physical_units=274-len(claims),
        pool_visits=102, physical_period_id=0)


def main():
    entry = read(HERE / 'entry_source_pins.json')
    for rel, h in entry['files'].items():
        ck(sha(ROOT / rel) == h, 'inherited source or research file preserved')
    ck(entry['gate_sha256'] == sha(HERE / 'CA00_FOUR_RULE_GATE.md'), 'gate precedes audit and is preserved')
    summary = read(HERE / 'cut_summary.json')
    fact_cert = read(HERE / 'source_fact_table.json')
    ledger = read(HERE / 'cut_ledgers.json')
    ck(summary['cut_ledgers_sha256'] == sha(HERE / 'cut_ledgers.json'), 'cut-ledger hash')
    ck(summary['fact_table_sha256'] == ledger['source_fact_table_sha256'] == sha(HERE / 'source_fact_table.json'), 'source-fact hash')
    ck(fact_cert['source_replays_sha256'] == summary['source_replays_sha256'] == sha(NI / 'full_source_replays.json'), 'fixed source replay hash')
    ck(fact_cert['UD_rule_sha256'] == sha(UD / 'UD01_ARBITRARY_DEPTH_SPLIT_PAYER_THEOREM.md'), 'authoritative UD rule hash')
    ck(fact_cert['FI_rule_sha256'] == sha(FI / 'FI01_SOURCE_FRAME_CEILING_AND_CHARGING.md'), 'authoritative FI rule hash')
    nia = read(NI / 'independent_audit.json')
    ck(nia['status'] == 'PASS' and nia['full_source_replays_sha256'] == summary['source_replays_sha256'], 'independent complete source composition inherited')
    replay = read(NI / 'full_source_replays.json')
    rows_by_orientation = {'normal': replay['cycle'], 'reflected': replay['mirrored_cycle']}
    for a, b in zip(rows_by_orientation['normal'], rows_by_orientation['reflected']):
        ck(b['key'] == 14-a['key'], 'source query reflection')
        for name in ['source_A', 'source_B', 'destination_A', 'destination_B']:
            ck(b[name] == mirror(a[name]) and keys(a[name]) == list(range(1, 14)), 'actual reflected strict source BST')
        ck(b['A_events'] == reflected_events(a['A_events']) and b['B_events'] == reflected_events(a['B_events']), 'recorded reflected grouped events')
    facts, fresh_trials, accepted = {}, {}, {}
    ud_keep_inequalities = []
    for orientation, rows in rows_by_orientation.items():
        ck(len(rows) == 102, 'exact fixed102-action object')
        for i, row in enumerate(rows):
            ck(row['source_A'] == rows[i-1]['destination_A'] and row['source_B'] == rows[i-1]['destination_B'], 'cyclic exact paired source closure')
            ck(row['source_A'] != row['source_B'] and row['destination_A'] != row['destination_B'], 'nowhere diagonal recurrent period')
            ck(row['a'] > 0 and row['key'] != rows[i-1]['key'], 'all102 cyclic root blocks singleton positive leaders')
            ck(row['a'] == (depth(row['source_A'], row['key'])+1)//2, 'actual A source grouped cost')
            ck(row['q'] == sum(e[0] != 'ZIG' for e in row['B_events']), 'actual physical B double demands')
            if row['mode'] == 'KEEP':
                ck(row['q'] == depth(row['source_B'], row['key'])//2 and row['z'] == depth(row['source_B'], row['key']) % 2, 'B depth and zero-double zig conventions')
            else:
                ck(row['source_B'] == row['destination_B'] and row['a'] == 1, 'two actual one-StepEv DELETEs freeze B')
        fs = independent_facts(rows)
        ck(fs == fact_cert[orientation] and len(fs) == 485, 'all485 independent source facts agree exactly')
        facts[orientation] = fs
        for name, f in fs.items():
            if rows[f['payer']]['mode'] == 'KEEP':
                C = 2*rows[f['payer']]['a']
                ck(f['UD_ceiling'] >= C, 'every UD KEEP reservation consumes entire pool')
                if orientation == 'normal':
                    ud_keep_inequalities.append(dict(fact_id=name, anchor=f['anchor'], payer=f['payer'],
                        h=f['h'], k=f['k'], ceiling=f['UD_ceiling'], capacity=C,
                        nonnegative_slack=f['UD_ceiling']-C))
        fresh_trials[orientation], accepted[orientation] = {}, {}
        for protocol in ['UD', 'FI']:
            fresh_trials[orientation][protocol] = []
            accepted[orientation][protocol] = []
            recorded = ledger['trials'][orientation][protocol]
            ck(len(recorded) == 102 and [t['cut'] for t in recorded] == list(range(102)), 'all102 physical cuts present in order')
            for cut in range(102):
                trial = independently_scan(rows, fs, protocol, cut, orientation)
                ck(trial == recorded[cut], 'entire independent FIFO ledger matches producer')
                if trial['accepted']:
                    accepted[orientation][protocol].append(cut)
                fresh_trials[orientation][protocol].append(trial)
        for cut in range(102):
            old, new = fresh_trials[orientation]['UD'][cut], fresh_trials[orientation]['FI'][cut]
            for a, b in zip(old['steps'], new['steps']):
                ck(a['history_after'] == b['history_after'] and b['reservation'] <= a['reservation'], 'FI reserve dominance with retained paid facts')
                ck(b['debt_after'] <= a['debt_after'], 'FI debt no larger after every aligned step')
            ck(not old['accepted'] or new['accepted'], 'every UD successful cut preserved')
    ud, fi = accepted['normal']['UD'], accepted['normal']['FI']
    ck(accepted['normal'] == accepted['reflected'], 'all cut classifications preserved by source reflection')
    ck(ud == summary['UD_accepted_cuts'] == [] and fi == summary['FI_accepted_cuts'], 'exact summary accepted-cut sets')
    ck(len(fi) == 92 and summary['status'] == 'STRICT_FI_ONLY_WITNESS_VERIFIED', 'strict new FI-only source witness')
    rejected = sorted(set(range(102))-set(fi))
    positives = [i for i, r in enumerate(rows_by_orientation['normal']) if r['delta'] > 0]
    ck(positives == [17, 34, 51, 68, 85], 'five physical positive identities')
    ck(rejected == [j for i in positives for j in [i+1, i+2]], 'exact ten FI rejected cuts split repayment triple')
    ck(len(ud_keep_inequalities) == 475, 'all475 UD KEEP facts prevent lending')
    for orientation in rows_by_orientation:
        for cut in range(102):
            udtrial = fresh_trials[orientation]['UD'][cut]
            ck(all(rows_by_orientation[orientation][s['occurrence']]['mode'] == 'DELETE'
                for s in udtrial['steps'] if s['loans']), 'UD loans come only from the two DELETE pools')
            ck(sum(l['residual_end']-l['residual_start'] for s in udtrial['steps'] for l in s['loans']) <= 4,
                'four total DELETE units cannot repay five debts')
    triple_proofs = []
    chosen = fresh_trials['normal']['FI'][0]
    ck(chosen['accepted'] and len(chosen['assignments']) == 98, 'cut0 full FI injection')
    for i in positives:
        f = facts['normal'][f'{i}:{i+2}']
        profile = f['frame_profile']
        ck((f['h'], f['k'], f['UD_ceiling'], f['FI_ceiling']) == (3, 1, 2, 1), 'repeatable source ceiling improvement')
        ck((profile['entry_role'], profile['first_gain_allowance'], profile['outer_doubles'],
            profile['matching_outer_doubles'], profile['upper_depth']) == ('parent', 0, 1, 0, 2), 'RL entry parent and LR outer source depth bound')
        step = next(s for s in chosen['steps'] if s['occurrence'] == i+2)
        ck(step['reservation'] == 1 and step['capacity'] == 2 and step['q'] == 1, 'FI frees exactly one suffix unit at delayed KEEP5')
        assignment = dict(demand=[0, i, 2], unit=[0, i+2, 0, 1], kind='loan')
        ck(assignment in chosen['assignments'], 'physical third B-double paid by delayed KEEP5 bit1')
        triple_proofs.append(dict(anchor=i, immediate_KEEP=i+1, delayed_payer=i+2,
            fact=f, physical_assignment=assignment))
    ck(all(rows_by_orientation['normal'][a['unit'][1]]['mode'] == 'KEEP' for a in chosen['assignments']), 'cut0 uses no DELETE or startup credit')
    normal_ud_hist = dict(Counter(t['final_debt'] for t in fresh_trials['normal']['UD']))
    normal_fi_hist = dict(Counter(t['final_debt'] for t in fresh_trials['normal']['FI']))
    ck({str(k):v for k,v in normal_ud_hist.items()} == summary['UD_final_debt_histogram'], 'all UD rejected-tail totals')
    ck({str(k):v for k,v in normal_fi_hist.items()} == summary['FI_final_debt_histogram'], 'all FI final-tail totals')
    save('UD_no_KEEP_lending_certificate.json', dict(status='FINITE-EXACT',
        fixed_source_object='NI H5;102 physical blocks', inequalities=ud_keep_inequalities,
        inequality='c_UD(anchor,payer)>=2a_payer for every positive anchor and every KEEP payer',
        KEEP_loans_possible=False, positive_residual_demand=5, total_DELETE_capacity=4,
        final_debt_lower_bound_every_cut=1, accepted_UD_cuts=[],
        independent_of_cut_by_complete_cyclic_fact_coverage=True))
    save('FI_three_block_payment_certificate.json', dict(status='PROVED—RESTRICTED DOMAIN',
        cut0_full_injection=chosen['assignments'], source_triples=triple_proofs,
        source_depth_identity='h=3, entry parent mu=0, one outer LR double, no matching RR: U=2',
        ceilings='c_UD=2; c_FI=1; actual payer q=1 and capacity2',
        accepted_cuts=fi, rejected_cuts=rejected, selected_cut=0, demand_count=98,
        distinct_units_used=98, DELETE_units_used=0, startup_units_used=0, reused_units=0,
        source_fringe_extension='fixed H5, arbitrary untouched F>7; all facts and reservations unchanged',
        general_m_protocol_classification_claimed=False))
    save('independent_audit.json', dict(status='PASS', date='2026-11-01', checks=dict(checks),
        source_fact_table_sha256=sha(HERE / 'source_fact_table.json'),
        cut_ledgers_sha256=sha(HERE / 'cut_ledgers.json'), cut_summary_sha256=sha(HERE / 'cut_summary.json'),
        UD_no_KEEP_lending_sha256=sha(HERE / 'UD_no_KEEP_lending_certificate.json'),
        FI_three_block_payment_sha256=sha(HERE / 'FI_three_block_payment_certificate.json'),
        source_entry_method='original subtree membership, independently of producer LCA selection',
        debt_implementation='unit-by-unit oldest-debt queue; producer uses residual slices',
        normal_passes_checked=204, reflected_passes_checked=204, source_facts_checked=970,
        steps_checked=41616, periods_per_pass=1, physical_pool_visits_per_pass=102,
        UD_accepted_count=0, FI_accepted_count=92, FI_rejected_cuts=rejected,
        UD_final_debt_histogram=normal_ud_hist, FI_final_debt_histogram=normal_fi_hist,
        strict_FI_closed_walk_enlargement='PROVED—RESTRICTED DOMAIN witness in FI\\UD',
        source_reachable=True, nowhere_diagonal=True, recurrent_resets=2,
        selected_FI_cut=0, selected_injection_demands=98, selected_injection_units=98,
        startup_units_used=0, reused_units=0, new_source_engine_calls=0,
        larger_finite_fits=0, new_source_words=0, new_m_values_audited=0,
        matching_terminal_line='FROZEN', universal_CD='OPEN', automatic_successor_launched=False))
    print(json.dumps(dict(status='PASS', independent_checks=sum(checks.values()),
        cuts_checked_per_protocol=102, normal_passes=204, reflected_passes=204,
        UD_accepts=0, FI_accepts=92, FI_rejected_cuts=rejected,
        chosen_FI_cut=0, full_injection=98, reused_units=0, startup_units=0,
        UD_KEEP_loans_possible=False, strict_FI_only_witness=True), indent=2))


if __name__ == '__main__':
    main()
