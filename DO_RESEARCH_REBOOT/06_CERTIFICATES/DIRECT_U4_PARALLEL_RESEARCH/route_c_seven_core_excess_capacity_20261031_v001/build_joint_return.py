"""Complete the gated, fixed-component source-return construction.

No source engine, new key size, fitted coefficient, or source-table mutation.
All output is exclusive creation. Source action counts use physical occurrences.
"""
import hashlib
import json
import sys
from collections import deque
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OLD = HERE.parent / 'route_c_seven_core_return_obstruction_20261031_v001'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load(p):
    return json.loads(p.read_text(encoding='utf-8'))


def save(name, value):
    with (HERE / name).open('x', encoding='utf-8') as f:
        json.dump(value, f, indent=2, ensure_ascii=False)
        f.write('\n')


def ceildiv(a, b):
    return (a+b-1)//b


def main():
    entry = load(HERE / 'entry_source_pins.json')
    for rel, h in entry['files'].items():
        assert sha(ROOT / rel) == h, rel
    gate = HERE / 'EC00A_JOINT_COMPONENT_COMPLETION_GATE.md'
    assert gate.is_file()
    cap = load(HERE / 'capacity_certificate.json')
    tab = load(OLD / 'source_transition_table.json')
    graph = load(OLD / 'reachable_relation_certificate.json')
    oldaudit = load(OLD / 'independent_audit.json')
    assert cap['status'] == 'UNBOUNDED_CORE_TAIL_EXCESS'
    assert oldaudit['status'] == 'PASS'
    assert cap['source_table_sha256'] == oldaudit['source_table_sha256'] == sha(OLD / 'source_transition_table.json')
    assert cap['source_relation_sha256'] == oldaudit['relation_sha256'] == sha(OLD / 'reachable_relation_certificate.json')
    pairs, adj, labels = graph['pair_ids'], graph['outgoing_edges'], cap['component_labels']
    trans, cores = tab['transitions'], tab['cores']
    pair_id = {tuple(p): i for i, p in enumerate(pairs)}
    u = cap['loop_edges'][0][0]
    assert u == 1871
    cid = labels[u]
    C = {i for i, label in enumerate(labels) if label == cid}
    assert len(C) == 18232 and all(pairs[i][0] != pairs[i][1] for i in C)

    def tr(tree_id, key):
        row = trans[7*tree_id+key-1]
        assert (row['source'], row['key']) == (tree_id, key)
        return row

    def route(start, target):
        todo, pred = deque([start]), {start: None}
        while todo:
            s = todo.popleft()
            if s == target:
                break
            for key, t, delta in adj[s]:
                if t in C and t not in pred:
                    pred[t] = (s, key, t, max(delta, 0))
                    todo.append(t)
        assert target in pred, (start, target)
        path, s = [], target
        while s != start:
            edge = pred[s]
            path.append(list(edge))
            s = edge[0]
        return path[::-1]

    def path_keys(edges):
        return [e[1] for e in edges]

    fragment = None
    for s in sorted(C):
        for k, t, delta in adj[s]:
            if t not in C or tr(pairs[s][1], k)['q'] != 3:
                continue
            for l, v, delta2 in adj[t]:
                if v in C and tr(pairs[t][1], l)['q'] >= 2:
                    fragment = [[s, k, t, max(delta, 0)], [t, l, v, max(delta2, 0)]]
                    break
            if fragment:
                break
        if fragment:
            break
    if fragment is None:
        save('joint_return_certificate.json', dict(status='J_FRAGMENT_ABSENT', component=cid,
            component_size=len(C), new_source_engine_calls=0, automatic_successor_launched=False))
        print('J_FRAGMENT_ABSENT; stopped fixed-component completion')
        return

    to_fragment = route(u, fragment[0][0])
    from_fragment = route(fragment[-1][2], u)
    W_edges = cap['loop_edges'] + to_fragment + fragment + from_fragment
    W_keys = path_keys(W_edges)
    assert W_keys[0] == 4

    def has_scan(keys):
        return any([keys[(i+j) % len(keys)] for j in range(7)] in
                   [list(range(1, 8)), list(range(7, 0, -1))] for i in range(len(keys)))

    def replay(start, word):
        a_id, b_id = start
        rows = []
        for occurrence, (mode, key) in enumerate(word):
            ar = tr(a_id, key)
            br = tr(b_id, key) if mode == 'KEEP' else None
            na, nb = ar['target'], br['target'] if br else b_id
            rows.append(dict(occurrence=occurrence, mode=mode, key=key,
                source_pair=[a_id, b_id], target_pair=[na, nb],
                A_source_table_row=7*a_id+key-1,
                B_source_table_row=7*b_id+key-1 if br else None,
                d_A=ar['depth'], a=ar['a'], A_events=ar['events'],
                d_B=br['depth'] if br else None, q=br['q'] if br else 0,
                z=br['z'] if br else 0, B_events=br['events'] if br else [],
                delta=(br['q'] if br else 0)-2*ar['a'],
                diagonal_before=a_id == b_id, diagonal_after=na == nb))
            a_id, b_id = na, nb
        assert (a_id, b_id) == tuple(start), ('nonreturn', start, (a_id, b_id))
        assert all(r['a'] > 0 for r in rows)
        assert all(rows[i]['key'] != rows[(i+1) % len(rows)]['key'] for i in range(len(rows)))
        kept = [r for r in rows if r['mode'] == 'KEEP']
        q = [r['q'] for r in kept]
        assert max(q) <= 3
        used, helpers = set(), []
        for i, value in enumerate(q):
            j = (i+1) % len(q)
            if value >= 3 and q[j] <= 1:
                assert i not in used and j not in used
                used.update([i, j])
                helpers.append([i, j, max(value+q[j]-4, 0)])
        G = sum(max(v-2, 0) for v in q)
        J = sum(h[2] for h in helpers)+sum(max(v-2, 0) for i, v in enumerate(q) if i not in used)
        assert J == sum(q[i] == 3 and q[(i+1) % len(q)] >= 2 for i in range(len(q)))
        summary = dict(actions=len(rows), KEEP_actions=len(kept),
            physical_resets=sum(r['mode'] == 'DELETE' for r in rows),
            resets_one_StepEv=all(r['a'] == 1 for r in rows if r['mode'] == 'DELETE'),
            A=sum(r['a'] for r in rows), Q_B=sum(q), Z_B=sum(r['z'] for r in kept),
            E=sum(max(r['delta'], 0) for r in kept),
            C_D=sum(2*r['a'] for r in rows if r['mode'] == 'DELETE'), G_B=G, J_B=J,
            q_profile=q, A_profile=[r['a'] for r in rows], helper_pairs=helpers,
            positive_occurrences=[r['occurrence'] for r in kept if r['delta'] > 0],
            J_contributing_occurrences=[kept[i]['occurrence'] for i in range(len(q))
                if q[i] == 3 and q[(i+1) % len(q)] >= 2],
            diagonal_source_occurrences=[r['occurrence'] for r in rows if r['diagonal_before']],
            nowhere_diagonal=not any(r['diagonal_before'] or r['diagonal_after'] for r in rows),
            distinct_source_pairs=len({tuple(r['source_pair']) for r in rows}),
            full_cyclic_request_core_scan=has_scan([r['key'] for r in rows]),
            full_cyclic_KEEP_core_scan=has_scan([r['key'] for r in kept]),
            paired_closed=True, all_cyclic_A_root_blocks_singletons=True)
        return dict(start_pair=list(start), word=[dict(mode=m, key=k) for m, k in word],
                    replay=rows, **summary)

    W = replay(pairs[u], [('KEEP', k) for k in W_keys])
    assert W['E'] >= 1 and W['J_B'] >= 1 and W['G_B'] >= W['J_B']
    mdiag = max(ceildiv(3, W['E']), ceildiv(3, W['G_B']), ceildiv(5, W['J_B']))
    prefix = [('DELETE', 3), ('DELETE', 5), ('KEEP', 7)]
    approach = [6, 5, 3, 7, 1]
    exit_keys = [4, 2, 6, 4, 1, 3, 2, 5, 4, 2, 1]
    diag_word = prefix+[('KEEP', k) for k in approach+W_keys*mdiag+exit_keys]
    diagonal = replay([0, 0], diag_word)
    assert (diagonal['E'], diagonal['G_B'], diagonal['J_B'], diagonal['C_D']) == (
        2+mdiag*W['E'], 2+mdiag*W['G_B'], mdiag*W['J_B'], 4)
    assert (diagonal['A'], diagonal['Q_B'], diagonal['Z_B']) == (
        24+mdiag*W['A'], 21+mdiag*W['Q_B'], 8+mdiag*W['Z_B'])
    assert diagonal['E'] > 4 and diagonal['G_B'] >= 5 and diagonal['J_B'] >= 5

    recurrent = None
    for s in sorted(C):
        aid, bid = pairs[s]
        if aid != 0:
            continue
        at = aid
        for k in [3, 5]:
            ar = tr(at, k)
            assert ar['a'] == 1 and len(ar['events']) == 1 and ar['events'][0][0] == 'RR'
            at = ar['target']
        at = tr(at, 7)['target']
        bt = tr(bid, 7)['target']
        t = pair_id.get((at, bt))
        if t in C:
            recurrent = [s, t]
            break

    off = None
    if recurrent is not None:
        s0, t0 = recurrent
        enter = route(t0, u)
        leave = route(u, s0)
        moff = max(ceildiv(5, W['E']), ceildiv(5, W['G_B']), ceildiv(6, W['J_B']))
        off_word = prefix+[('KEEP', k) for k in path_keys(enter)+W_keys*moff+path_keys(leave)]
        off = replay(pairs[s0], off_word)
        assert off['physical_resets'] == 2 and off['resets_one_StepEv']
        assert off['E'] > off['C_D'] == 4 and off['G_B'] >= 5 and off['J_B'] >= 5
        assert off['nowhere_diagonal']
        assert not off['full_cyclic_request_core_scan'] and not off['full_cyclic_KEEP_core_scan']
        # Source reachability uses the banked predecessor tree, never cycle capacity.
        reach, v = [], s0
        while v:
            p, k = graph['predecessors'][v]
            reach.append([p, k, v])
            v = p
        reach.reverse()
        off.update(recurrent_reset_input_state=s0, recurrent_reset_output_state=t0,
            path_after_resets_to_u=enter, path_from_u_to_start=leave, repeat_count=moff,
            reachability_only_prefix=prefix+[('KEEP', k) for p, k, v in reach],
            reachability_graph_edges=reach, reachability_prefix_credit_used=False,
            non_simple_closed_walk=off['distinct_source_pairs'] < off['actions'],
            request_word_not_proper_power=True)

    result = dict(status='JOINT_THRESHOLD_RETURN_CONSTRUCTED', date='2026-11-01',
        completion_gate_sha256=sha(gate), capacity_sha256=sha(HERE / 'capacity_certificate.json'),
        source_table_sha256=sha(OLD / 'source_transition_table.json'),
        source_relation_sha256=sha(OLD / 'reachable_relation_certificate.json'),
        source_audit_sha256=sha(OLD / 'independent_audit.json'),
        component=cid, component_size=len(C), entry_state=u,
        original_E_loop=cap['loop_edges'], local_J_fragment=fragment,
        path_to_fragment=to_fragment, path_from_fragment=from_fragment,
        joint_loop_edges=W_edges, joint_loop=W, diagonal_repeat_count=mdiag,
        diagonal_return=diagonal, off_diagonal_reset_input_found=recurrent is not None,
        off_diagonal_return=off, mirrored_key_map='x -> 14-x; swap children; mapped source events',
        new_source_engine_calls=0, larger_finite_fits=0, new_active_core_sizes=0,
        FI_acceptance='NOT ESTABLISHED', UD_rejection_every_cut='NOT ESTABLISHED',
        matching_terminal_line='FROZEN', universal_CD='OPEN', automatic_successor_launched=False)
    save('joint_return_certificate.json', result)
    fields = ['actions', 'physical_resets', 'A', 'Q_B', 'Z_B', 'E', 'C_D', 'G_B', 'J_B',
              'nowhere_diagonal', 'full_cyclic_request_core_scan', 'full_cyclic_KEEP_core_scan']
    print(json.dumps(dict(status=result['status'], J_fragment=fragment,
        W_word=W_keys, W={k: W[k] for k in fields}, m_diagonal=mdiag,
        diagonal={k: diagonal[k] for k in fields}, recurrent_input=recurrent,
        off_diagonal={k: off[k] for k in fields} if off else None,
        m_off=off['repeat_count'] if off else None), indent=2))


if __name__ == '__main__':
    main()
