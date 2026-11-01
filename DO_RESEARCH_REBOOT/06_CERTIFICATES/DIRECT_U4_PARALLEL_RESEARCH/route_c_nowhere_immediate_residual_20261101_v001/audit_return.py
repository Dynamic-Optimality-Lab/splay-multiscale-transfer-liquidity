"""Fixed-source immediate-helper residual and nowhere-diagonal return audit."""
import hashlib
import json
import subprocess
import sys
from collections import Counter, deque
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
EC = HERE.parent / 'route_c_seven_core_excess_capacity_20261031_v001'
KC = HERE.parent / 'route_c_seven_core_return_obstruction_20261031_v001'
STAGE = ROOT / 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'


def read(p):
    return json.loads(p.read_text(encoding='utf-8'))


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def save(name, data):
    with (HERE / name).open('x', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def main():
    inherited = read(EC / 'entry_source_pins.json')
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
        gate_sha256=sha(HERE / 'NI00_FOUR_RULE_GATE.md')))
    manifest = read(EC / 'delivery_manifest.json')
    for name, h in manifest['files'].items():
        assert sha(EC / name) == h
    table, graph = read(KC / 'source_transition_table.json'), read(KC / 'reachable_relation_certificate.json')
    cap, prior = read(EC / 'capacity_certificate.json'), read(EC / 'joint_return_certificate.json')
    source_audit, graph_audit = read(KC / 'independent_audit.json'), read(EC / 'independent_audit.json')
    assert source_audit['status'] == graph_audit['status'] == 'PASS'
    assert source_audit['source_table_sha256'] == cap['source_table_sha256'] == sha(KC / 'source_transition_table.json')
    assert source_audit['relation_sha256'] == cap['source_relation_sha256'] == sha(KC / 'reachable_relation_certificate.json')
    pp, edges, labels = graph['pair_ids'], graph['outgoing_edges'], cap['component_labels']
    trees, tt = table['cores'], table['transitions']
    u, s0 = 1871, 12919
    cid = labels[u]
    C = {i for i, c in enumerate(labels) if c == cid}
    assert len(C) == 18232 and s0 in C and pp[s0] == [0, 4]
    assert all(pp[i][0] != pp[i][1] for i in C)

    def tr(tree, key):
        r = tt[7*tree+key-1]
        assert (r['source'], r['key']) == (tree, key)
        return r

    def route(start, target):
        queue, pred = deque([start]), {start: None}
        while queue:
            s = queue.popleft()
            if s == target:
                break
            for key, t, delta in edges[s]:
                if t in C and t not in pred:
                    pred[t] = [s, key, t, delta]
                    queue.append(t)
        assert target in pred
        result, at = [], target
        while at != start:
            edge = pred[at]
            result.append(edge)
            at = edge[0]
        return result[::-1]

    local, qualifying = [], []
    for s in sorted(C):
        for k, t, delta in edges[s]:
            if delta <= 0 or t not in C:
                continue
            ar, br = tr(pp[s][0], k), tr(pp[s][1], k)
            assert delta == 1 and ar['a'] == 1 and br['q'] == 3
            for l, v, delta2 in edges[t]:
                if v not in C:
                    continue
                ar2, br2 = tr(pp[t][0], l), tr(pp[t][1], l)
                spare = max(2*ar2['a']-br2['q'], 0)
                row = dict(first=[s, k, t, delta], second=[t, l, v, delta2],
                    a_first=ar['a'], q_first=br['q'], a_next=ar2['a'], q_next=br2['q'],
                    actual_immediate_spare=spare, surviving_residual=max(delta-spare, 0))
                local.append(row)
                if spare == 0:
                    assert ar2['a'] == 1 and br2['q'] == 2 and delta2 == 0
                    qualifying.append(row)
    chosen = qualifying[0] if qualifying else None
    return_edges = route(u, s0)
    if chosen:
        to_frag = route(u, chosen['first'][0])
        from_frag = route(chosen['second'][2], u)
        loop_edges = to_frag+[chosen['first'], chosen['second']]+from_frag
        loop_keys = [e[1] for e in loop_edges]
        branch = 'SURVIVING_IMMEDIATE_DEMAND_LOOP_FOUND'
    else:
        to_frag, from_frag, loop_edges = [], [], []
        loop_keys = [r['key'] for r in prior['joint_loop']['word']]
        branch = 'NO_INTERNAL_ZERO_SPARE_SUCCESSOR; fixed nowhere-diagonal control only'

    def replay(start, word, closed=True):
        aid, bid = start
        rows = []
        for i, (mode, key) in enumerate(word):
            ar = tr(aid, key)
            br = tr(bid, key) if mode == 'KEEP' else None
            na, nb = ar['target'], br['target'] if br else bid
            rows.append(dict(occurrence=i, mode=mode, key=key, source_pair=[aid, bid], target_pair=[na, nb],
                A_table_row=7*aid+key-1, B_table_row=7*bid+key-1 if br else None,
                d_A=ar['depth'], a=ar['a'], A_events=ar['events'],
                d_B=br['depth'] if br else None, q=br['q'] if br else 0, z=br['z'] if br else 0,
                B_events=br['events'] if br else [], delta=(br['q'] if br else 0)-2*ar['a'],
                diagonal_before=aid == bid, diagonal_after=na == nb))
            aid, bid = na, nb
        if closed:
            assert [aid, bid] == list(start)
        assert all(r['a'] > 0 for r in rows)
        return [aid, bid], rows

    def budgets(rows):
        kept = [r for r in rows if r['mode'] == 'KEEP']
        q = [r['q'] for r in kept]
        assert max(q) <= 3
        E = sum(max(r['delta'], 0) for r in kept)
        resid, helpers = 0, []
        for j, r in enumerate(kept):
            if r['delta'] <= 0:
                continue
            nxt = kept[(j+1) % len(kept)]
            spare = max(2*nxt['a']-nxt['q'], 0)
            rr = max(r['delta']-spare, 0)
            resid += rr
            helpers.append(dict(anchor=r['occurrence'], next_KEEP=nxt['occurrence'],
                excess=r['delta'], next_actual_spare=spare, residual=rr))
        used, pairs = set(), []
        for j, value in enumerate(q):
            k = (j+1) % len(q)
            if value == 3 and q[k] <= 1:
                assert j not in used and k not in used
                used.update([j, k])
                pairs.append([j, k, max(value+q[k]-4, 0)])
        J = sum(p[2] for p in pairs)+sum(max(value-2, 0) for j, value in enumerate(q) if j not in used)
        assert J == sum(q[j] == 3 and q[(j+1) % len(q)] >= 2 for j in range(len(q)))
        def scan(keys):
            return any([keys[(i+j) % len(keys)] for j in range(7)] in
                [list(range(1, 8)), list(range(7, 0, -1))] for i in range(len(keys)))
        return dict(actions=len(rows), A=sum(r['a'] for r in rows), Q_B=sum(q), Z_B=sum(r['z'] for r in kept),
            E=E, C_D=sum(2*r['a'] for r in rows if r['mode'] == 'DELETE'),
            G_B=sum(max(v-2, 0) for v in q), J_B=J, R_imm=resid,
            physical_resets=sum(r['mode'] == 'DELETE' for r in rows),
            resets_one_StepEv=all(r['a'] == 1 for r in rows if r['mode'] == 'DELETE'),
            nowhere_diagonal=not any(r['diagonal_before'] or r['diagonal_after'] for r in rows),
            singleton_cyclic_A_root_blocks=all(rows[i]['key'] != rows[(i+1) % len(rows)]['key'] for i in range(len(rows))),
            distinct_source_pairs=len({tuple(r['source_pair']) for r in rows}),
            full_cyclic_core_request_scan=scan([r['key'] for r in rows]),
            full_cyclic_core_KEEP_scan=scan([r['key'] for r in kept]),
            q_profile=q, a_profile=[r['a'] for r in rows], immediate_helper_residuals=helpers)

    loop_word = [('KEEP', k) for k in loop_keys]
    _, loop_rows = replay(pp[u], loop_word)
    loop_stats = budgets(loop_rows)
    prefix = [('DELETE', 3), ('DELETE', 5), ('KEEP', 7)]
    end, reset_rows = replay(pp[s0], prefix, closed=False)
    assert end == pp[0] and [r['a'] for r in reset_rows[:2]] == [1, 1] and reset_rows[2]['q'] == 2
    approach = [e[1] for e in cap['approach_edges']]
    assert approach == [6, 5, 3, 7, 1]
    bridge = prefix+[('KEEP', k) for k in approach]
    end, bridge_rows = replay(pp[s0], bridge, closed=False)
    assert end == pp[u]
    m = 5
    word = bridge+loop_word*m+[('KEEP', e[1]) for e in return_edges]
    _, rows = replay(pp[s0], word)
    stats = budgets(rows)
    assert stats['nowhere_diagonal'] and stats['singleton_cyclic_A_root_blocks']
    assert stats['physical_resets'] == 2 and stats['resets_one_StepEv'] and stats['C_D'] == 4
    if chosen:
        assert stats['R_imm'] >= 5 and stats['R_imm'] > stats['C_D']
        assert stats['G_B'] >= 5 and stats['J_B'] >= 5 and stats['E'] > stats['C_D']
    else:
        assert stats['G_B'] >= 5 and stats['J_B'] >= 5 and stats['E'] > stats['C_D']
    # Reachability prefix is separate from the recurrent period.
    reach, at = [], s0
    while at:
        parent, key = graph['predecessors'][at]
        reach.append([parent, key, at])
        at = parent
    reach.reverse()
    reachword = prefix+[('KEEP', k) for p, k, t in reach]
    reachend, reachrows = replay([0, 0], reachword, closed=False)
    assert reachend == pp[s0]
    save('local_fragment_certificate.json', dict(status='FINITE-EXACT', branch=branch,
        gate_sha256=sha(HERE / 'NI00_FOUR_RULE_GATE.md'),
        source_table_sha256=sha(KC / 'source_transition_table.json'),
        source_relation_sha256=sha(KC / 'reachable_relation_certificate.json'),
        source_audit_sha256=sha(KC / 'independent_audit.json'),
        source_graph_audit_sha256=sha(EC / 'independent_audit.json'),
        selected_component=cid, component_size=len(C), local_rows=local,
        internal_positive_edges_checked=len({tuple(r['first']) for r in local}),
        next_KEEP_fragments_checked=len(local), qualifying_fragments=qualifying,
        qualifying_count=len(qualifying), chosen=chosen, new_source_engine_calls=0,
        larger_finite_fits=0, new_active_core_sizes=0))
    save('nowhere_return_certificate.json', dict(status='THRESHOLD_AND_RESIDUAL_RETURN_CONSTRUCTED' if chosen else 'NOWHERE_DIAGONAL_NUMERIC_CONTROL_ONLY',
        local_certificate_sha256=sha(HERE / 'local_fragment_certificate.json'),
        start_state=s0, start_pair=pp[s0], loop_entry_state=u, loop_start_pair=pp[u],
        reset_destination_state=0, actual_recurrent_B_q_on_7=2,
        banked_approach=cap['approach_edges'], path_to_fragment=to_frag,
        path_from_fragment=from_frag, loop_edges=loop_edges,
        loop_word=[dict(mode=m, key=k) for m, k in loop_word], loop_replay=loop_rows, loop_stats=loop_stats,
        return_edges=return_edges, repeat_count=m,
        word=[dict(mode=mode, key=key) for mode, key in word], replay=rows, stats=stats,
        bridge_replay=bridge_rows, reachability_prefix_word=[dict(mode=m, key=k) for m, k in reachword],
        reachability_prefix_replay=reachrows, reachability_graph_edges=reach,
        reachability_prefix_credit_used=False, proper_power_of_reset_word=False,
        surviving_internal_fragment_per_loop=bool(chosen),
        FI_acceptance='NOT CLASSIFIED', UD_rejection_every_cut='NOT ESTABLISHED',
        matching_terminal_line='FROZEN', universal_CD='OPEN', automatic_successor_launched=False))
    print(json.dumps(dict(branch=branch, local_fragments=len(local), qualifying=len(qualifying),
        chosen=chosen, loop_word=loop_keys, loop_stats={k:loop_stats[k] for k in
            ['actions','E','G_B','J_B','R_imm']}, return_word=[e[1] for e in return_edges],
        full_stats={k:stats[k] for k in ['actions','A','Q_B','Z_B','E','C_D','G_B','J_B','R_imm',
            'physical_resets','nowhere_diagonal','full_cyclic_core_request_scan','full_cyclic_core_KEEP_scan']},
        inherited_files=len(pins)), indent=2))


if __name__ == '__main__':
    main()
