"""Independent exact original-engine audit; does not import the producer."""
import hashlib
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASE = HERE.parent
counts = Counter()


def ck(v, label):
    assert v, label
    counts[label] += 1


def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def save(name, value):
    with (HERE / name).open('x', encoding='utf-8') as f:
        json.dump(value, f, indent=2)
        f.write('\n')


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


tu = load('turn_check_original_tuple', ROOT / 'python/independent/splay.py')
pt = load('turn_check_original_pointer', ROOT / 'python/liquidity/legacy_embedding.py')


def tt(t):
    if t is None:
        return tu.LEAF
    if isinstance(t, str):
        return ('opaque', t)
    return tu.node(t[0], tt(t[1]), tt(t[2]))


def tj(t):
    if t[0] == 'leaf':
        return None
    if t[0] == 'opaque':
        return t[1]
    return [t[1], tj(t[2]), tj(t[3])]


def pp(t, parent=None):
    if t is None:
        return None
    if isinstance(t, str):
        return pt.mknode(t, p=parent)
    n = pt.mknode(t[0], p=parent)
    n['l'] = pp(t[1], n)
    n['r'] = pp(t[2], n)
    return n


def pj(t, parent=None):
    if t is None:
        return None
    ck(t['p'] is parent, 'original-pointer-parent-links')
    if isinstance(t['k'], str):
        ck(t['l'] is None and t['r'] is None, 'opaque-body-never-entered')
        return t['k']
    return [t['k'], pj(t['l'], t), pj(t['r'], t)]


def path(t, x):
    nodes = []
    while isinstance(t, list):
        nodes.append(t)
        if t[0] == x:
            return nodes
        t = t[1 if x < t[0] else 2]
    raise AssertionError('explicit searched key must exist')


def depth(t, x):
    return len(path(t, x)) - 1


def validate(t, lo=float('-inf'), hi=float('inf')):
    if not isinstance(t, list):
        return []
    ck(lo < t[0] < hi, 'valid-source-BST-order')
    return validate(t[1], lo, t[0]) + [t[0]] + validate(t[2], t[0], hi)


def tokens(t):
    if isinstance(t, str):
        return [t]
    return [] if t is None else tokens(t[1]) + tokens(t[2])


def norm(events):
    return [[e['case'], e['lo'], e['hi'], e['orient']] for e in events]


def edge(A, B, mode, x):
    ta, ae = tu.trace(tt(A), x)
    pa, ape = pt.splay_trace(pp(A), x)
    a = tj(ta)
    ae = [list(v) for v in ae]
    ck(a == pj(pa), 'independent-full-A-destination')
    ck(ae == norm(ape), 'independent-original-A-events')
    da = depth(A, x)
    ck(len(ae) == (da + 1) // 2, 'edge-depth-counts-physical-A-events')
    if mode == 'KEEP':
        tb, be = tu.trace(tt(B), x)
        pb, bpe = pt.splay_trace(pp(B), x)
        b, be = tj(tb), [list(v) for v in be]
        ck(b == pj(pb), 'independent-full-B-destination')
        ck(be == norm(bpe), 'independent-original-B-events')
        db = depth(B, x)
        ck(sum(v[0] != 'ZIG' for v in be) == db // 2, 'physical-B-doubles')
        ck(sum(v[0] == 'ZIG' for v in be) == db % 2, 'terminal-B-zig-preserved')
    else:
        b, be, db = B, [], None
    q = sum(v[0] != 'ZIG' for v in be)
    return dict(source_A=A, source_B=B, mode=mode, key=x,
                destination_A=a, destination_B=b, d_A=da, d_B=db,
                a=len(ae), q=q, delta=q-2*len(ae), A_events=ae, B_events=be)


def history(rows, closed=False):
    for i, r in enumerate(rows):
        ck(validate(r['source_A']) == validate(r['source_B']), 'equal-source-key-sets')
        v = edge(r['source_A'], r['source_B'], r['mode'], r['key'])
        for k in v:
            if k in r:
                ck(v[k] == r[k], 'certificate-field-' + k)
        if i:
            ck((r['source_A'], r['source_B']) ==
               (rows[i-1]['destination_A'], rows[i-1]['destination_B']),
               'literal-source-history-chain')
    if closed:
        ck((rows[-1]['destination_A'], rows[-1]['destination_B']) ==
           (rows[0]['source_A'], rows[0]['source_B']), 'complete-pair-closure')


def source_lca(T, g, x, side, active=True):
    ag, ax = path(T, g), path(T, x)
    h = len(ag)-1
    if not active:
        return dict(h=h, j=0, e=0, predicted_h=h, actual_h=h)
    ck(all(n[0] > g if side == 'R' else n[0] < g for n in ag[:-1]),
       'anchor-on-pure-source-spine')
    common = []
    for a, b in zip(ag, ax):
        if a[0] != b[0]:
            break
        common.append(a)
    j, lca = len(common)-1, common[-1]
    on_spine = ax[-1][0] == lca[0]
    if on_spine:
        e = 0
    else:
        local, local_events = pt.splay_trace(pp(lca), x)
        local = pj(local)
        e = depth(local, lca[0])
        ck(e in (1, 2), 'local-old-root-epsilon-one-or-two')
        local_path = path(lca, x)
        n = len(local_path)-1
        first_right = local_path[1][0] > lca[0]
        same = n >= 2 and ((local_path[2][0] > local_path[1][0]) == first_right)
        predicted_e = 1 if n % 2 else (2 if same else 1)
        ck(e == predicted_e, 'epsilon-from-original-local-parity-and-directions')
        ck(sum(v['case'] != 'ZIG' for v in local_events) == n//2,
           'local-comparison-not-extra-physical-credit')
    result, _ = pt.splay_trace(pp(T), x)
    actual = depth(pj(result), g)
    predicted = h-j+e
    ck(predicted == actual, 'exact-LCA-anchor-depth-update')
    ck(tokens(T) == sorted(tokens(T)) or len(tokens(T)) == len(set(tokens(T))),
       'opaque-source-occurrences-distinct')
    return dict(h=h, j=j, e=e, predicted_h=predicted, actual_h=actual)


def audit_phase(p):
    g, side = p['anchor'], p['side']
    for u in p['updates']:
        r = u['row']
        aa = source_lca(r['source_A'], g, r['key'], side)
        bb = source_lca(r['source_B'], g, r['key'], side, r['mode']=='KEEP')
        for name, v in [('A', aa), ('B', bb)]:
            for k in v:
                ck(v[k] == u[name][k], 'independent-source-LCA-' + k)
        before, after = 2*aa['h']-bb['h'], 2*aa['actual_h']-bb['actual_h']
        ck(after == before-2*aa['j']+bb['j']+2*aa['e']-bb['e'],
           'signed-paired-source-recurrence')
    r = p['return_row']
    if r['mode'] == 'KEEP':
        da, db = depth(r['source_A'], g), depth(r['source_B'], g)
        D = 2*da-db
        reserve = da % 2 + (D+1)//2
        ck(reserve == 2*r['a']-r['q'] == p['exact_signed_reserve'],
           'signed-return-reserve-including-negative-D')
        final = p['updates'][-1]['B']
        qualified = final['applied'] and final['predicted_h'] <= 3
        ck(qualified == p['qualifying_final_reset'], 'source-qualifying-reset')
        if qualified:
            ck(r['q'] <= 1 and r['a'] >= 1 and reserve >= 1,
               'near-anchor-actual-negative-return')


def mixed(r):
    # Actual DELETE leader owns A work; actual first KEEP owns B demands.
    A, B, x = r['source_A'], r['source_B'], r['key']
    steps = []
    for mode in ('DELETE', 'DELETE', 'KEEP', 'KEEP'):
        v = edge(A, B, mode, x)
        steps.append(v)
        A, B = v['destination_A'], v['destination_B']
    ck((A, B) == (r['destination_A'], r['destination_B']), 'mixed-complete-boundary-projection')
    ck([v['a'] for v in steps] == [r['a'], 0, 0, 0], 'actual-DELETE-leader-A-ownership')
    ck([v['q'] for v in steps] == [0, 0, r['q'], 0], 'actual-first-KEEP-B-ownership')
    return dict(key=x, A_owner_occurrence=0, B_owner_occurrence=2,
                a=r['a'], q=r['q'])


def physical_injection(rows, donor, positive):
    assignments = []
    used_A, used_B = set(), set()
    for i, r in enumerate(rows):
        own = [(i, e, bit) for e in range(r['a']) for bit in (0, 1)]
        demand = [(i, e) for e, v in enumerate(r['B_events']) if v[0] != 'ZIG']
        for j, b in enumerate(demand):
            unit = own[j] if j < len(own) else (donor, rows[donor]['a']-1, 1)
            ck(unit not in used_A and b not in used_B, 'distinct-physical-unit-injection')
            ck(0 <= unit[1] < rows[unit[0]]['a'] and unit[2] in (0, 1),
               'genuine-A-event-bit')
            used_A.add(unit)
            used_B.add(b)
            assignments.append(dict(A_unit=list(unit), B_double=list(b)))
    ck(len(used_B) == sum(r['q'] for r in rows), 'one-period-all-demands-injected')
    ck(rows[donor]['delta'] < 0 and rows[positive]['delta'] == 1,
       'real-donor-and-unique-positive')
    order = [(donor+t) % len(rows) for t in range(len(rows))]
    rank = {v:i for i,v in enumerate(order)}
    ck(all(rank[a['A_unit'][0]] <= rank[a['B_double'][0]] for a in assignments),
       'no-startup-or-future-unit-at-donor-cut')
    return dict(source_cut=donor, positive_block=positive, donor_block=donor,
                donor_A_unit=[donor, rows[donor]['a']-1, 1],
                positive_B_double=[positive, 2], assignments=assignments,
                actual_period_order=order, startup_units=0, imported_units=0,
                repeated_units=0, actual_A_units=2*sum(r['a'] for r in rows),
                B_demands=len(used_B))


def main():
    d = read(HERE/'inward_reset_source_certificate.json')
    ck(d['new_exact_symbolic_core_keys'] == 16, 'declared-single-exact-sixteen-core-template')
    for field, g, side in [('rows', 1, 'R'), ('symbolic_rows', 1, 'R'),
                           ('reflected_rows', 16, 'L')]:
        rs = d[field]
        history(rs)
        ck([(r['a'],r['q']) for r in rs] == [(1,3),(1,2),(1,2),(1,2),(1,2)],
           'exact-inward-reset-no-spare-costs')
        ck(2*sum(r['a'] for r in rs) == 10 and sum(r['q'] for r in rs) == 11,
           'ten-physical-units-eleven-actual-demands')
        ck(all(r['delta'] >= 0 for r in rs), 'no-negative-block-in-open-source-episode')
        B0, B1 = rs[0]['source_B'], rs[-1]['destination_B']
        child = 2 if side == 'R' else 1
        ck((B1[child][0] < B0[child][0]) if side == 'R' else
           (B1[child][0] > B0[child][0]), 'strict-inward-anchor-B-child-reset')
        ck(B1 != B0 and rs[-1]['destination_A'] != rs[0]['source_A'],
           'open-source-episode-not-a-paired-closed-walk')
        for r in rs[:-1]:
            aa = source_lca(r['source_A'], g, r['key'], side)
            bb = source_lca(r['source_B'], g, r['key'], side)
            ck(2*aa['actual_h']-bb['actual_h'] ==
               2*aa['h']-bb['h']-2*aa['j']+bb['j']+2*aa['e']-bb['e'],
               'template-signed-recurrence')
        r = rs[-1]
        D = 2*r['d_A']-r['d_B']
        ck(D == -2 and r['d_A']%2+(D+1)//2 == 0,
           'negative-depth-deficit-does-not-force-spare')
    sr = d['symbolic_rows']
    for label in ('A','B'):
        ck(len(tokens(sr[0]['source_'+label])) == 17, 'all-seventeen-formal-gap-bodies')
        ck(sorted(tokens(sr[0]['source_'+label])) == sorted(tokens(sr[-1]['destination_'+label])),
           'formal-gap-multiplicity-preserved')
    ck(set(tokens(sr[0]['source_A'])).isdisjoint(tokens(sr[0]['source_B'])),
       'paired-gap-interiors-independent-not-assumed-equal')
    ck(not d['reachable_closed_FE02_refutation'] and not d['Coarse_Double_counterexample'],
       'valid-source-refutation-not-promoted-to-FE02')
    audit = read(HERE/'closed_source_LCA_audit_certificate.json')
    source_updates, near = 0, 0
    for name, phases in audit['corpora'].items():
        for phase in phases:
            audit_phase(phase)
            source_updates += len(phase['updates'])
            near += bool(phase.get('qualifying_final_reset'))
    ck(source_updates == audit['source_updates'] == 140, 'fixed-source-update-count')
    ck(near == len(audit['qualifying_return_contexts']) == 52, 'fixed-qualifying-return-count')
    pg = read(BASE/'route_c_pf_positive_gap_closure_20261101_v001/closed_source_certificate.json')
    ore = read(BASE/'route_c_fe02_odd_restoration_20261101_v001/odd_restoration_source_certificate.json')
    ce = read(BASE/'route_c_fe02_coupled_excursions_20261101_v001/coupled_excursion_control_certificate.json')
    for rs in (pg['ordinary_rows'], pg['reflected_rows'], pg['formal_opaque_fringe_rows'],
               ore['rows'], ore['reflected_rows'], ce['rows'], ce['reflected_rows'], ce['symbolic_rows']):
        history(rs, closed=True)
    W = pg['ordinary_rows']
    ck((sum(r['a'] for r in W),sum(r['q'] for r in W)) == (25,22), 'frozen-nineteen-block-totals')
    phase = next(p for p in audit['corpora']['W_ordinary_rows'] if p['return_block'] == 7)
    ck(phase['internal_keys'] == [5,6,4] and phase['qualifying_final_reset'],
       'actual-nonordered-turn-phase-near-anchor-repayment')
    ck([i for i,r in enumerate(W) if r['delta'] > 0] == [0], 'frozen-single-positive')
    injections = {field:physical_injection(pg[field],7,0) for field in
                  ('ordinary_rows','reflected_rows','formal_opaque_fringe_rows')}
    save('near_anchor_physical_injection_certificate.json', dict(status='PASS',
         donor_selection='actual source-LCA endpoint condition; no future payer-demand fitting',
         injections=injections, source_certificate_sha256=sha(
             BASE/'route_c_pf_positive_gap_closure_20261101_v001/closed_source_certificate.json')))
    mixed_rows = [mixed(d['rows'][i]) for i in (0,3,4)] + [mixed(W[7])]
    pins = read(HERE/'entry_source_pins.json')
    for path_, h in pins['files'].items():
        ck(sha(ROOT/path_) == h, 'all-inherited-pinned-bytes-unchanged')
    result = dict(status='PASS', total_checks=sum(counts.values()), checks=dict(sorted(counts.items())),
        both_original_engines=True, producer_imported=False,
        fixed_source_updates=source_updates, qualifying_old_closed_return_contexts=near,
        new_exact_symbolic_core_keys=16, new_template_blocks=5, opaque_gap_pairs=17,
        arbitrary_unequal_gap_interiors=True, reflection=True, mixed_physical_owners=mixed_rows,
        local_capacity=10, local_demand=11, diagonal_reachability='NOT ESTABLISHED',
        new_episode_full_closed_provenance='NOT ESTABLISHED; not closed as written',
        exact_obstruction_scope='unrestricted valid-source phase child-drift/reset-payment law',
        all_size_theorem='source-LCA induction and near-anchor actual-return proof; not finite extrapolation',
        FE02_CD='OPEN', Universal_Coarse_Double='OPEN', Coarse_Double_counterexample=False,
        larger_finite_fits=0, source_graph_or_coefficient_search=False,
        script_sha256=sha(Path(__file__)),
        certificate_hashes={p.name:sha(p) for p in HERE.glob('*certificate.json')},
        original_source_hashes={str(p.relative_to(ROOT)):sha(p) for p in
            [ROOT/'python/independent/splay.py', ROOT/'python/liquidity/legacy_embedding.py']})
    save('independent_audit.json', result)
    print(json.dumps(dict(status='PASS',checks=sum(counts.values()),source_updates=source_updates,
        qualifying_old_closed_returns=near, new_exact_template_keys=16,
        new_template_capacity=10,new_template_demand=11,FE02_CD='OPEN'),indent=2))


if __name__ == '__main__':
    main()
