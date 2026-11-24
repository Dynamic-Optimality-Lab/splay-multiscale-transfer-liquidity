"""Exact unrestricted conservative bank teacher on original physical traces.

The existing named bank network is compiled sparsely for larger complete
sources. Integral primal/cut certificates are checked without trusting Dinic.
"""
import sys
import json
import gzip
import hashlib
from pathlib import Path
from collections import deque
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_flow

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
PREV = HERE.parent / 'GSO_PHYSICAL_BANK_RULE_20261122_V001'
TRACE = HERE.parent / 'GSO_TRACE_ENGINE_20261122_V001'
sys.path.insert(0, str(PREV))
import bank_rule as B
import fast_trace as F
sys.path.pop(0)


def load(path):
    with (gzip.open(path, 'rt', encoding='utf-8') if path.suffix == '.gz' else path.open(encoding='utf-8')) as stream:
        return json.load(stream)


def write(name, value):
    assert not (HERE / 'FINAL_MANIFEST.json').exists(), 'sealed output'
    path = HERE / name
    assert not path.exists(), 'use a fresh artifact name'
    path.parent.mkdir(parents=True, exist_ok=True)
    with (gzip.open(path, 'wt', encoding='utf-8') if path.suffix == '.gz' else path.open('w', encoding='utf-8')) as stream:
        json.dump(value, stream, separators=(',', ':') if path.suffix == '.gz' else None,
                  indent=None if path.suffix == '.gz' else 2)


def network(z, H):
    assert type(H) is int and H >= 1
    ev = B.events(z)
    c, d = 8 * H, H
    demand = sum(e['q'] for e in ev)
    inf = demand + 1
    initial = list(range(2, 2 + len(z['blocks'])))
    latest = initial.copy()
    node_count = len(initial) + 2
    rows, cols, caps, types = [], [], [], []
    hubs = []
    outputs = []

    def edge(u, v, cap, kind):
        rows.append(u); cols.append(v); caps.append(cap); types.append(kind)

    for j, e in enumerate(ev):
        hub = node_count; node_count += 1; hubs.append(hub)
        out = []
        for block in e['scope']:
            edge(latest[block], hub, inf, 'input')
            nxt = node_count; node_count += 1
            edge(hub, nxt, H, 'storage')
            latest[block] = nxt; out.append([block, len(caps) - 1])
        outputs.append(out)
        supply = c * e['a'] + d * e['k']
        if supply:
            edge(0, hub, supply, 'A_supply' if e['a'] else 'KEEP_supply')
        if e['q']:
            edge(hub, 1, e['q'], 'demand')
    for block in range(len(initial)):
        if latest[block] != initial[block]:
            edge(latest[block], initial[block], H, 'cyclic_storage')
    assert node_count <= 800000
    assert max(caps, default=0) < 2**31
    rr = np.asarray(rows, dtype=np.int32)
    cc = np.asarray(cols, dtype=np.int32)
    vv = np.asarray(caps, dtype=np.int64)
    graph = csr_matrix((vv, (rr, cc)), shape=(node_count, node_count))
    assert graph.nnz == len(caps), 'no duplicate capacity edges'
    return graph, ev, rr, cc, vv, types, hubs, outputs


def solve(z, H):
    graph, ev, rr, cc, vv, types, hubs, outputs = network(z, H)
    result = maximum_flow(graph, 0, 1, method='dinic')
    value = int(result.flow_value)
    # Original arcs have no reciprocal original arcs. Negative entries in the
    # returned antisymmetric matrix are residual bookkeeping, not real flows.
    ff = np.asarray(result.flow[rr, cc]).ravel().astype(np.int64)
    assert np.all(ff >= 0) and np.all(ff <= vv)
    balance = np.bincount(cc, weights=ff, minlength=graph.shape[0]) - np.bincount(rr, weights=ff, minlength=graph.shape[0])
    assert balance[0] == -value and balance[1] == value and np.all(balance[2:] == 0)
    # Recheck conservation exactly in integers rather than relying on float
    # bincount arithmetic, even though the trial values are tiny integers.
    exact = np.zeros(graph.shape[0], dtype=np.int64)
    np.add.at(exact, cc, ff); np.add.at(exact, rr, -ff)
    assert exact[0] == -value and exact[1] == value and np.all(exact[2:] == 0)
    demand = sum(e['q'] for e in ev)
    cert = {'status': 'FINITE_EXACT_TRANSPORT' if value == demand else 'EXACT_TRIAL_MINCUT',
            'source': z['source']['name'], 'H': H, 'c': 8 * H, 'd': H,
            'demand': demand, 'paid': value, 'nodes': graph.shape[0], 'edges': graph.nnz,
            'positive_edge_flows': [[int(i), int(ff[i])] for i in np.flatnonzero(ff)],
            'original_A_supply_bound': 8 * H * z['A'], 'KEEP_supply_bound': H * z['K_B'],
            'universal_CD': 'OPEN'}
    if value < demand:
        residual = graph - result.flow
        residual.eliminate_zeros()
        seen = np.zeros(graph.shape[0], dtype=np.bool_); seen[0] = True
        queue = deque([0])
        while queue:
            u = queue.popleft()
            for at in range(residual.indptr[u], residual.indptr[u + 1]):
                v = int(residual.indices[at])
                if residual.data[at] > 0 and not seen[v]:
                    seen[v] = True; queue.append(v)
        assert not seen[1]
        cut_indices = np.flatnonzero(seen[rr] & ~seen[cc])
        assert int(sum(int(vv[i]) for i in cut_indices)) == value
        cert['cut'] = {'source_side_nodes': [int(i) for i in np.flatnonzero(seen)],
                       'edges': [[int(i), int(vv[i]), types[i]] for i in cut_indices],
                       'capacity': value, 'shortfall': demand - value}
    # Save physical original-ID output profiles, rather than anonymous state
    # types. They are diagnostic finite flows, not a learned global policy.
    cert['B_outputs'] = [{'id': e['id'], 'stocks': [[block, int(ff[edge])] for block, edge in outputs[j]]}
                         for j, e in enumerate(ev) if e['id'][0] == 'B' and e['q']]
    return cert


def pin(path):
    return {'path': str(path.relative_to(ROOT)).replace('\\', '/'),
            'bytes': path.stat().st_size, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def vouchers(z):
    genuine = [op['id'] for op in z['operations'] if op['k']]
    out = {}; used = set(); count = len(z['operations'])
    for j, op in enumerate(genuine):
        previous = genuine[j - 1]
        k = previous % count + 1
        chosen = None
        while True:
            row = z['operations'][k - 1]
            for step in z['steps'][row['steps'][0]:row['steps'][1]]:
                if step['a'] and chosen is None:
                    chosen = tuple(step['id'])
            if k == op:
                break
            k = k % count + 1
        assert chosen is not None and chosen not in used
        used.add(chosen); out[str(op)] = list(chosen)
    assert len(out) == z['K_B'] <= z['A']
    return out
