"""Pinned graph/ownership analysis only; no source engine or splay calls."""
import hashlib
import json
import sys
import time
from pathlib import Path

F = Path(__file__).resolve().parent
C = F.parent
N = C / 'ND35_COMPLEMENT_08'
S1 = C / 'PC35_RELEASE_COMPLETION_09'
S2 = C / 'DEFICIT_SOURCE_GEOMETRY_10'
CAP = float(sys.argv[1])
START = time.process_time()


def read(p):
    return json.loads(p.read_text(encoding='utf8'))


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def maximum(graph):
    owner, chosen = {}, {}

    def augment(d, seen):
        for u in sorted(graph[d]):
            if u in seen:
                continue
            seen.add(u)
            if u not in owner or augment(owner[u], seen):
                owner[u], chosen[d] = d, u
                return True
        return False

    for d in sorted(graph):
        augment(d, set())
    roots = set(graph) - set(chosen)
    reached, units, todo = set(roots), set(), list(roots)
    while todo:
        d = todo.pop()
        for u in graph[d]:
            units.add(u)
            assert u in owner
            if owner[u] not in reached:
                reached.add(owner[u])
                todo.append(owner[u])
    assert units == set().union(*(graph[d] for d in reached)) if reached else not units
    assert len(reached) - len(units) == len(graph) - len(chosen)
    return chosen, dict(demands=sorted(reached), units=sorted(units), deficiency=len(reached) - len(units))


def normalize(h, fixed, D, U):
    assert set(h) == D and len(set(h.values())) == len(D) and set(h.values()) <= U
    assert set(fixed) <= D and len(set(fixed.values())) == len(fixed)
    reverse = {u: d for d, u in fixed.items()}
    result, paths = dict(fixed), []
    for root in sorted(D - set(fixed)):
        d, visited, edges = root, set(), []
        while True:
            assert d not in visited
            visited.add(d)
            u = h[d]
            next_d = reverse.get(u)
            edges.append(dict(demand=d, comparison_unit=u, fixed_owner=next_d))
            if next_d is None:
                break
            d = next_d
        result[root] = u
        paths.append(dict(root=root, terminal=u, edges=edges))
    assert len(set(result.values())) == len(result) and set(result) == D
    assert all(result[d] == u for d, u in fixed.items())
    return result, paths


def main():
    inherited = [N / 'independent_audit.json', S1 / 'independent_release_audit.json', S2 / 'independent_geometry_audit.json']
    receipts = [read(p) for p in inherited]
    pins = [N / 'lifetime_controls.json', N / 'root_entry_graph_controls.json',
            N / 'exact_challenge_sources.json', S1 / 'release_completion_controls.json',
            S2 / 'source_geometry_controls.json']
    for p in pins:
        hashes = [r['input_sha256'][str(p)] for r in receipts if str(p) in r['input_sha256']]
        assert hashes and all(v == sha(p) for v in hashes)
    step1 = read(S1 / 'release_completion_controls.json')
    geometry = read(S2 / 'source_geometry_controls.json')
    graphs = read(N / 'root_entry_graph_controls.json')
    life = read(N / 'lifetime_controls.json')
    reports, inputs = [], inherited + pins
    for source in life['controls']:
        name = source['source']
        old = next(r for r in graphs['controls'] if r['source'] == name)
        one = next(r for r in step1['controls'] if r['source'] == name)
        two = next(r for r in geometry['controls'] if r['source'] == name)
        path = Path(source['source_path'])
        inputs.append(path)
        original = read(path)
        U, D = set(map(tuple, source['U'])), set(map(tuple, source['D']))
        fixed = {tuple(a['demand']): tuple(a['unit']) for a in one['g1']}
        h = {tuple(a['demand']): tuple(a['unit']) for a in old['matching']}
        G = {tuple(a['demand']): set(map(tuple, a['units'])) for a in old['graph']}
        residual, free = D - set(fixed), U - set(fixed.values())
        assert len(residual) == one['residual'] and len(free) == one['remaining_raw_units']
        sub = {d: G[d] & free for d in residual}
        chosen, cut = maximum(sub)
        canonical = {d: set() for d in residual}
        for p in two['ports']:
            t, j, b = p['beta']
            canonical[tuple(p['demand'])].update((t, j, bit) for bit in (0, 1))
        assert all(us <= U for us in canonical.values())
        cf = {d: us & free for d, us in canonical.items()}
        cchosen, ccut = maximum(cf)
        normalized, paths = normalize(h, fixed, D, U)
        assert all(h[d] in G[d] for d in D)
        A, Q = len(U) // 2, len(D)
        assert len(free) - len(residual) == 2 * A - Q
        reports.append(dict(source=name, source_path=str(path), source_sha256=sha(path),
                            source_period_t=[original['period_rows'][0]['t'], original['period_rows'][-1]['t']],
                            source_word=[dict(t=r['t'], key=r['key'], keep=r.get('keep', r.get('kind')), H=r['a'], Q=r['qF'])
                                         for r in original['period_rows']],
                            A=A, Q=Q, fixed_count=len(fixed), residual_count=len(residual), raw_free_count=len(free),
                            residual_demands=sorted(residual),
                            direct_existing_graph_matching_size=len(chosen), direct_cut=cut,
                            direct_residual_edges=[dict(demand=d, units=sorted(us)) for d, us in sorted(sub.items())],
                            canonical_event_matching_size=len(cchosen), canonical_event_cut=ccut,
                            canonical_event_edges=[dict(demand=d, units=sorted(us)) for d, us in sorted(cf.items())],
                            complete_comparison_count=len(h), normalization_paths=paths,
                            normalized_residual_pairs=[dict(demand=d, unit=normalized[d], original_graph_edge=normalized[d] in G[d])
                                                       for d in sorted(residual)],
                            normalized_complete_count=len(normalized), historical_g1_modified=False))
        assert time.process_time() - START < CAP - 1
    # The cached vine has own-funded NATURAL MACROS, including every
    # preceding DELETE. A terminal KEEP can have H=0. The failed v01
    # access-only check is retained, charged, and explicitly corrected.
    vine = read(N / 'exact_challenge_sources.json')['vine_family_control']
    one = next(r for r in step1['controls'] if r['source'] == 'VINE8')
    U, D, h = set(), set(), {}
    rows = vine['rows']
    for row in rows:
        U.update((row['t'], j, b) for j in range(1, row['H'] + 1) for b in (0, 1))
    ends = [i for i, r in enumerate(rows) if r['kind'] == 'K' and r['BF_before'][0] != r['key']]
    for number, end in enumerate(ends):
        units, i = [], (ends[number - 1] + 1) % len(rows)
        while True:
            row = rows[i]
            units.extend((row['t'], j, b) for j in range(1, row['H'] + 1) for b in (0, 1))
            if i == end:
                break
            i = (i + 1) % len(rows)
        target = rows[end]
        assert target['Q'] <= len(units)
        for k in range(1, target['Q'] + 1):
            d = (target['t'], k)
            D.add(d)
            h[d] = units[k - 1]
    fixed = {tuple(a['demand']): tuple(a['unit']) for a in one['g1']}
    normalized, paths = normalize(h, fixed, D, U)
    reports.append(dict(source='VINE8', A=len(U) // 2, Q=len(D), fixed_count=len(fixed), residual_count=len(D) - len(fixed),
                        raw_free_count=len(U) - len(fixed), complete_comparison_count=len(h),
                        normalization_paths=paths, normalized_residual_pairs=[dict(demand=p['root'], unit=p['terminal']) for p in paths],
                        normalized_complete_count=len(normalized), historical_g1_modified=False,
                        scope='one existing cached vine control; arbitrary-even-support own-funding proof inherited separately'))
    out = dict(status='PASS_PINNED_STEP3_COMPARISON_ANALYSIS', controls=reports,
               source_queries=0, source_engine_calls=0, universal_compensation_proved=False,
               graph_failure_scope='only direct residual edges after freezing g1; not raw funding or full joint graph',
               input_sha256={str(p): sha(p) for p in dict.fromkeys(inputs)})
    with (F / 'existing_compensation_controls.json').open('x', encoding='utf8') as f:
        json.dump(out, f, indent=2)
    print(json.dumps(dict(status=out['status'], controls=[{k: r[k] for k in (
        'source', 'Q', 'residual_count', 'raw_free_count', 'direct_existing_graph_matching_size',
        'direct_cut', 'canonical_event_matching_size', 'canonical_event_cut', 'normalized_residual_pairs') if k in r} for r in reports])))


if __name__ == '__main__':
    main()
