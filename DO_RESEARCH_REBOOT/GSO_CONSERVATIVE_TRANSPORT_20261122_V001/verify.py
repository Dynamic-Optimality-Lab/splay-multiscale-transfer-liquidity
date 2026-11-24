"""Independent immutable physical replay and exact primal/cut verification.

Imports neither this teacher, its graph compiler, its policy, nor a flow solver.
The sole splay primitive is the pinned immutable original full-tree verifier.
"""
import sys
import json
import gzip
import time
import hashlib
import importlib.util
from pathlib import Path
from collections import Counter

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
spec = importlib.util.spec_from_file_location('transport_immutable_physical',
            ROOT / 'DO_RESEARCH_REBOOT/COVER_FLOW_AUDIT_20261121_V001/verify.py')
V = importlib.util.module_from_spec(spec); sys.modules[spec.name] = V; spec.loader.exec_module(V)


def read(path):
    with (gzip.open(path, 'rt', encoding='utf-8') if path.suffix == '.gz' else path.open(encoding='utf-8')) as stream:
        return json.load(stream)


def raw(t):
    children = {}; stack = [t]
    while stack:
        x = stack.pop(); assert str(x.k) not in children
        children[str(x.k)] = [x.l.k if x.l else None, x.r.k if x.r else None]
        stack.extend(k for k in (x.l, x.r) if k)
    return {'root': t.k, 'children': children}


def immutable(t):
    nodes = {}; entered = set(); stack = [(t['root'], False)]
    while stack:
        key, ready = stack.pop()
        if ready:
            l, r = t['children'][str(key)]
            nodes[key] = V.node(key, nodes[l] if l is not None else None, nodes[r] if r is not None else None)
            assert (l is None or nodes[l].hi < key) and (r is None or nodes[r].lo > key)
        else:
            assert key not in entered; entered.add(key); stack.append((key, True))
            for child in t['children'][str(key)]:
                if child is not None:
                    stack.append((child, False))
    assert len(nodes) == len(t['children'])
    return nodes[t['root']]


def physical(z):
    source = z['source']; keys = sorted(map(int, source['initial_A']['children']))
    assert keys == sorted(map(int, source['initial_B']['children']))
    assert all(1 <= len(block) <= 5 for block in z['blocks'])
    assert [key for block in z['blocks'] for key in block] == keys
    owner = {x: j for j, block in enumerate(z['blocks']) for x in block}
    if source.get('diagonal'):
        reach = {a: immutable(source['diagonal']) for a in ('A', 'B')}
        for mode, target in source.get('prefix', []):
            for a in ('A', 'B') if mode == 'K' else ('A',):
                reach[a], _ = V.rebuild(reach[a], target, lambda *x: None, lambda *x: None)
        assert all(raw(reach[a]) == source['initial_'+a] for a in reach)
    else:
        assert source['initial_A'] == source['initial_B'] and not source.get('prefix')
    trees = {a: immutable(source['initial_'+a]) for a in ('A', 'B')}
    maps = {a: {int(k): list(v) for k, v in source['initial_'+a]['children'].items()} for a in trees}
    parents = {a: {k: None for k in keys} for a in trees}
    roots = {a: source['initial_'+a]['root'] for a in trees}
    for a in trees:
        for k, children in maps[a].items():
            for child in children:
                if child is not None:
                    assert parents[a][child] is None; parents[a][child] = k
    event_tape = []; pos = 0; A = Q = KB = bits = 0
    for op, ((mode, target), saved_op) in enumerate(zip(source['operations'], z['operations']), 1):
        assert saved_op['id'] == op and saved_op['mode'] == mode and saved_op['target'] == target
        genuine = int(mode == 'K' and roots['B'] != target); KB += genuine
        assert genuine == saved_op['k']
        if genuine:
            event_tape.append({'id': ['K', op], 'a': 0, 'q': 0, 'k': 1, 'scope': [owner[target]]})
        start = pos; aa = qq = 0
        for actor in ('A', 'B') if mode == 'K' else ('A',):
            seen_steps = {}; seen_bits = Counter()

            def emit(step, bit, typ, promoted, pivot, demoted):
                nonlocal bits
                bits += 1
                if step not in seen_steps:
                    seen_steps[step] = z['steps'][pos+step-1]
                record = seen_steps[step]
                assert record['id'] == [actor, op, step] and record['type'] == typ and record['target'] == target
                original = record['bits'][bit]
                y, p = promoted.k, pivot.k
                pa = parents[actor]; ch = maps[actor]; grand = pa[p]
                assert pa[y] == p
                assert ch[p] == [pivot.l.k if pivot.l else None, pivot.r.k if pivot.r else None]
                assert ch[y] == [promoted.l.k if promoted.l else None, promoted.r.k if promoted.r else None]
                side = int(y > p); middle = ch[y][1-side]
                scope = sorted({owner[k] for k in (y, p, grand, middle) if k is not None})
                expected = {'id': [actor, op, step, bit], 'promoted': y, 'demoted': p,
                            'grandparent': grand, 'middle': middle, 'footprint': scope}
                assert {key: original[key] for key in expected} == expected
                ch[p][side] = middle
                if middle is not None:
                    pa[middle] = p
                ch[y][1-side] = p; pa[p] = y; pa[y] = grand
                if grand is None:
                    roots[actor] = y
                else:
                    assert ch[grand][int(p > grand)] == p
                    ch[grand][int(p > grand)] = y
                assert ch[p] == [demoted.l.k if demoted.l else None, demoted.r.k if demoted.r else None]
                seen_bits[step] += 1

            trees[actor], depth = V.rebuild(trees[actor], target, emit, lambda *x: None)
            assert roots[actor] == target
            for step in sorted(seen_steps):
                record = seen_steps[step]
                nbits = seen_bits[step]
                assert nbits == len(record['bits']) and nbits in (1, 2)
                a, q = int(actor == 'A'), int(actor == 'B' and nbits == 2)
                scope = sorted({i for bit in record['bits'] for i in bit['footprint']})
                assert (record['a'], record['q'], record['k'], record['scope']) == (a, q, 0, scope)
                event_tape.append({'id': record['id'], 'a': a, 'q': q, 'k': 0, 'scope': scope})
                aa += a; qq += q
            assert len(seen_steps) == (depth+1)//2
            pos += len(seen_steps)
        assert (saved_op['steps'], saved_op['a'], saved_op['q']) == ([start, pos], aa, qq)
        A += aa; Q += qq
    assert len(source['operations']) == len(z['operations']) and pos == len(z['steps'])
    assert (A, Q, KB) == (z['A'], z['Q_B'], z['K_B'])
    assert all(raw(trees[a]) == source['initial_'+a] for a in trees)
    assert len({tuple(e['id']) for e in event_tape}) == len(event_tape)
    return event_tape, {'operations': len(z['operations']), 'real_rotations': bits, 'A': A, 'Q_B': Q, 'K_B': KB}


def edges(z, tape, H):
    initial = [i+2 for i in range(len(z['blocks']))]; latest = list(initial)
    nextnode = len(initial)+2; result = []; outputs = []; hubs = []
    for e in tape:
        hub = nextnode; nextnode += 1; hubs.append(hub); lanes = []
        for i in e['scope']:
            result.append((latest[i], hub, z['Q_B']+1, 'input'))
            new = nextnode; nextnode += 1
            result.append((hub, new, H, 'storage')); lanes.append([i, len(result)-1]); latest[i] = new
        outputs.append(lanes)
        if e['a'] or e['k']:
            result.append((0, hub, 8*H if e['a'] else H, 'A_supply' if e['a'] else 'KEEP_supply'))
        if e['q']:
            result.append((hub, 1, 1, 'demand'))
    for i, start in enumerate(initial):
        if latest[i] != start:
            result.append((latest[i], start, H, 'cyclic_storage'))
    return result, nextnode, hubs, outputs


def voucher_check(z, saved):
    genuine = [o['id'] for o in z['operations'] if o['k']]
    assert set(saved) == set(map(str, genuine)); used = set(); n = len(z['operations'])
    for index, current in enumerate(genuine):
        previous = genuine[index-1]; selected = tuple(saved[str(current)])
        assert selected[0] == 'A' and selected not in used; used.add(selected)
        op = selected[1]
        assert (previous < op <= current) if previous < current else (op > previous or op <= current)
        actual = next(s for s in z['steps'][z['operations'][op-1]['steps'][0]:z['operations'][op-1]['steps'][1]] if tuple(s['id']) == selected)
        assert actual['a'] and actual['bits'][0]['id'] == list(selected)+[0]
    assert len(used) == z['K_B'] <= z['A']


def certificate(z, tape, cert):
    H = cert['H']; graph, n, hubs, outputs = edges(z, tape, H)
    assert (n, len(graph), cert['c'], cert['d']) == (cert['nodes'], cert['edges'], 8*H, H)
    flows = dict(cert['positive_edge_flows']); assert len(flows) == len(cert['positive_edge_flows'])
    net = [0]*n
    for index, amount in flows.items():
        u, v, cap, _ = graph[index]
        assert type(amount) is int and 0 < amount <= cap
        net[u] -= amount; net[v] += amount
    assert net[0] == -cert['paid'] and net[1] == cert['paid'] and all(x == 0 for x in net[2:])
    assert cert['demand'] == z['Q_B']
    if cert['status'] == 'FINITE_EXACT_TRANSPORT':
        assert cert['paid'] == z['Q_B']
        assert all(flows.get(i, 0) == cap for i, (_, _, cap, kind) in enumerate(graph) if kind == 'demand')
    else:
        left = set(cert['cut']['source_side_nodes']); assert 0 in left and 1 not in left and all(0 <= x < n for x in left)
        crossing = [[i, cap, kind] for i, (u, v, cap, kind) in enumerate(graph) if u in left and v not in left]
        assert crossing == cert['cut']['edges'] and sum(e[1] for e in crossing) == cert['cut']['capacity'] == cert['paid'] < z['Q_B']
    expected_outputs = [{'id': e['id'], 'stocks': [[i, flows.get(edge, 0)] for i, edge in outputs[j]]}
                        for j, e in enumerate(tape) if e['id'][0] == 'B' and e['q']]
    assert expected_outputs == cert['B_outputs']
    return {'H': H, 'paid': cert['paid'], 'Q_B': z['Q_B'], 'status': cert['status'],
            'cyclic_storage_conservation_checked': True, 'shared_original_A_supply_checked': True}


def main():
    start = time.perf_counter(); summary = read(HERE/'TEACHER_SUMMARY.json'); checked = []; cases = []; totals = Counter()
    by_tag = {}
    for row in summary['cases']:
        by_tag.setdefault(row['tag'], []).append(row)
    for tag, rows in by_tag.items():
        first = read(HERE/rows[0]['certificate']); path = ROOT/first['trace']['path']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == first['trace']['sha256']
        z = read(path); tape, stats = physical(z); totals.update({k: stats[k] for k in ('operations', 'real_rotations')})
        voucher_check(z, read(HERE/f'inputs/{tag}_vouchers.json.gz'))
        for row in rows:
            cert = read(HERE/row['certificate']); assert cert['trace'] == first['trace']
            checked.append({'tag': tag, **certificate(z, tape, cert)})
        cases.append({'tag': tag, 'source': z['source']['name'], **stats})
        print(json.dumps({'verified': tag, 'capacity_tests': len(rows)}), flush=True)
    result = {'passed': True, 'physical_sources': len(cases), 'capacity_certificates': len(checked),
              'totals': dict(totals), 'sources': cases, 'certificates': checked,
              'seconds': time.perf_counter()-start,
              'scope': 'Every physical original bit, source reachability and exact paired closure; all integer primal/cut and original-A voucher constraints. Full cyclic Pi from earlier pins is reused only at its stated original-source scopes.',
              'independence': 'No current teacher, graph compiler, policy or flow-solver import; pinned immutable rotations plus separate graph construction and integer checks. Same-agent implementation independence.',
              'universal_CD': 'OPEN'}
    if not (HERE/'FINAL_MANIFEST.json').exists():
        (HERE/'INDEPENDENT_VERIFICATION.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps({k: result[k] for k in ('passed', 'physical_sources', 'capacity_certificates', 'totals', 'seconds')}))


if __name__ == '__main__':
    main()
