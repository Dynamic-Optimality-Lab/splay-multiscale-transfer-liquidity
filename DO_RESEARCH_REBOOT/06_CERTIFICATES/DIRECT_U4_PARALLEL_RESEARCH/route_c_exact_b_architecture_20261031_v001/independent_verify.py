"""Independent pointer-source and integer-certificate verification; no producer import."""
import hashlib
import importlib.util
import json
import sys
from collections import Counter
from functools import lru_cache
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]

def ck(ok, msg):
    if not ok:
        raise AssertionError(msg)

def key(t):
    return json.dumps(t, separators=(',', ':'))

def main():
    path = HERE / 'exact_b_architecture_certificate.json'
    c = json.loads(path.read_text(encoding='utf-8'))
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
    def depth(t, x):
        d = 0
        while t is not None:
            if t[0] == x:
                return d
            t = t[1] if x < t[0] else t[2]
            d += 1
        raise AssertionError('absent request')
    cases = Counter()
    calls = 0
    def access(t, x):
        nonlocal calls
        d = depth(t, x)
        out, ev = p.splay_trace(ptr(t), x)
        calls += 1
        q = sum(e['case'] != 'ZIG' for e in ev)
        z = sum(e['case'] == 'ZIG' for e in ev)
        ck(q == d//2 and z == d%2 and len(ev) == (d+1)//2, 'source event units')
        out = raw(out)
        ck(out[0] == x, 'present-key root')
        cases.update(e['case'] for e in ev)
        return out, d, q, ev
    @lru_cache(None)
    def enumerate_bst(lo, hi):
        if lo > hi:
            return (None,)
        return tuple([r, a, b] for r in range(lo, hi+1)
                     for a in enumerate_bst(lo, r-1) for b in enumerate_bst(r+1, hi))
    btrees = c['B_trees']
    complete = enumerate_bst(1, 7)
    ck(len(btrees) == len(complete) == 429, 'Catalan seven-key count')
    ck(len({key(t) for t in btrees}) == 429 and
       {key(t) for t in btrees} == {key(t) for t in complete}, 'complete B classification')
    u = [2, None, None]
    v = [5, [4, None, None], [6, None, None]]
    expected_a = [[1, None, [3, u, [7, v, None]]],
                  [1, None, [7, [3, u, v], None]],
                  [3, [1, None, u], [7, v, None]],
                  [7, [1, None, [3, u, v]], None],
                  [7, [3, [1, None, u], v], None]]
    ck(c['n'] == 7 and c['core'] == [1, 3, 7] and c['A_trees'] == expected_a, 'frozen five A states')
    atrees = c['A_trees']
    ai = {key(t): i for i, t in enumerate(atrees)}
    bi = {key(t): i for i, t in enumerate(btrees)}
    comp = {(j, x): access(b, x) for j, b in enumerate(btrees) for x in (1, 3, 7)}
    a_access = {(i, x): access(a, x) for i, a in enumerate(atrees) for x in (1, 3, 7)}
    nodes = c['terminal_nodes']
    ck(len(nodes) == len({tuple(z) for z in nodes}) == 556, 'terminal node distinctness')
    ck(all(0 <= i < 5 and 0 <= j < 429 and atrees[i][0] == btrees[j][0] for i,j in nodes), 'same-root terminal domain')
    all_nodes = {(i, j) for i, a in enumerate(atrees) for j, b in enumerate(btrees) if a[0] == b[0]}
    ck({tuple(z) for z in nodes} == all_nodes, 'complete terminal inventory for minor')
    ni = {tuple(z): i for i, z in enumerate(nodes)}
    rows = c['rows']
    ck(len(rows) == 4290 and c['noop_rows'] == 2145, 'specified source row count')
    row_index, noops = 0, 0
    for i, a in enumerate(atrees):
        r = a[0]
        for j, b in enumerate(btrees):
            for x in (1, 3, 7):
                ap, da, qa, ae = a_access[i, x]
                ck(key(ap) in ai and da <= 2, 'closed core-only A operation')
                if da == 0:
                    ck(ap == a and not ae, 'omitted no-op is exact identity')
                    noops += 1
                    continue
                cr, dr, qr, _ = comp[j, r]
                cx, dx, qx, _ = comp[j, x]
                source = ni[i, bi[key(cr)]]
                target = ni[ai[key(ap)], bi[key(cx)]]
                expected = dict(A=i, B=j, request=x, source=source, target=target,
                                d_A=da, a=(da+1)//2, Q_source=qr, Q_target=qx,
                                d_B_source_root=dr, d_B_target_root=dx,
                                weight=2*((da+1)//2)+qr-qx)
                ck(rows[row_index] == expected, 'every exact DELETE provenance row')
                row_index += 1
    ck(row_index == 4290 and noops == 2145, 'complete row traversal')
    labels = c['feasible_minor_labels']
    ck(c['status'] == 'FINITE-EXACT-NO-NEGATIVE-CYCLE' and not c['negative_cycle'] and
       not c['witness'] and c['cycle_weight'] == 0, 'no false architecture refutation')
    ck(len(labels) == len(nodes) and all(type(x) is int for x in labels), 'exact integer certificate dimensions')
    ck(all(labels[e['target']]-labels[e['source']] <= e['weight'] for e in rows), 'all 4290 certificate inequalities')
    # Summing these verified inequalities excludes every negative cycle in this minor.
    # These numbers are not an all-size terminal formula.

    old_path = HERE.parent / 'route_c_root_step_refutation_20261031_v001/root_bound_countercertificate.json'
    old = json.loads(old_path.read_text(encoding='utf-8'))
    oldrow = old['controls'][0]
    a, b, ap = oldrow['source_A'], oldrow['source_B'], oldrow['destination_A']
    ck(a == expected_a[1] and ap == expected_a[3], 'old root-zig lies inside frozen minor')
    j = bi[key(b)]
    es = [e for e in rows if e['A'] == 1 and e['B'] == j and e['request'] == 7]
    ck(len(es) == 1, 'unique old counter row')
    e = es[0]
    ck((e['d_A'],e['a'],e['Q_source'],e['Q_target'],e['weight']) == (1,1,0,3,-1), 'old counter row requires a terminal drop')
    ck((labels[e['source']],labels[e['target']]) == (0,-1), 'finite consistency certificate distinguishes equal-K terminals')
    def clades(t):
        if t is None:
            return [], set()
        kl, sl = clades(t[1])
        kr, sr = clades(t[2])
        ks = kl+[t[0]]+kr
        ck(ks == sorted(set(ks)), 'valid ranked BST')
        return ks, sl | sr | {(ks[0],ks[-1])}
    def antichain_k_one(t, z):
        kt, st = clades(t)
        kz, sz = clades(z)
        ck(kt == kz == list(range(1,8)), 'old terminal same key set')
        st.remove((1,7))
        sz.remove((1,7))
        common = st & sz
        l, r = sorted(st-common), sorted(sz-common)
        active = [J for J in r if any(I[0] == J[0] or I[1] == J[1] for I in l)]
        ck(active and all((I[0] <= J[0] and J[1] <= I[1]) or
                          (J[0] <= I[0] and I[1] <= J[1]) for I in active for J in active),
           'every matching-active right interval is nested')
        # At most one active interval can be in a disjoint right antichain;
        # an existing endpoint edge attains one. Forced common pairs are exempt.
        f = len(st)-len(common)
        return f, 1, f-1
    c0 = comp[j, 1][0]
    c1 = comp[j, 7][0]
    ck(c0 == b and antichain_k_one(a,c0) == antichain_k_one(ap,c1) == (5,1,4),
       'unchanged antichain terminal values 4 and 4')
    # The weaker B inequality alone gives Phi(ap,b) >= K(ap,c1)+3=7,
    # while the equal-root boundary fixes Phi(a,b)=K(a,b)=4.
    lower_increment = 4+3-4
    ck(lower_increment == 3 > 2*e['a'], 'all weaker-B extensions of same terminal K fail DELETE')
    # Existing fixed six-DELETE prefix: no connector search and no pair fitting.
    initial = old['closed_witness']['initial_A']
    cur = initial
    for x in (4,7,3,5,7,1):
        cur = access(cur,x)[0]
    ck(initial == b and cur == a, 'old counter source reachable from diagonal with B frozen')

    result = dict(status='PASS', date='2026-10-31', n=7, A_states=5,
                  complete_B_states=429, terminal_vertices=556,
                  exact_DELETE_rows=4290, omitted_identity_rows=2145,
                  pointer_source_accesses=calls, pointer_event_cases=dict(cases),
                  producer_imported=False, graph_optimizer_used_by_verifier=False,
                  integer_inequalities_verified=4290,
                  integer_label_histogram=dict(Counter(labels)),
                  negative_cycles_in_frozen_minor=False,
                  architecture_universally_refuted=False,
                  exact_B_too_restrictive_globally='OPEN',
                  old_antichain_terminal_boundary_under_weaker_B='REFUTED-EXACT',
                  lower_DELETE_increment=3, DELETE_budget=2,
                  old_counter_source_reachable=True,
                  certificate_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                  old_countercertificate_sha256=hashlib.sha256(old_path.read_bytes()).hexdigest())
    with (HERE / 'independent_audit.json').open('x', encoding='utf-8') as f:
        json.dump(result, f, indent=2)
        f.write('\n')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
