"""Distinct exact checking of pinned neighborhoods and path certificates.

No producer import, source engine, new tree generation, or splay replay.
"""
import hashlib
import itertools
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


def matching_and_cut_check(graph, expected_size, cut):
    # Independent exhaustive Hall-deficiency identity, at most 9 demands
    # in this PINNED corpus. This is not a universal proof by enumeration.
    demands = sorted(graph)
    assert len(demands) <= 9
    worst = 0
    for mask in itertools.product((0, 1), repeat=len(demands)):
        subset = [d for d, yes in zip(demands, mask) if yes]
        neighbors = set().union(*(graph[d] for d in subset))
        worst = max(worst, len(subset) - len(neighbors))
    exact = set(map(tuple, cut['demands']))
    assert exact <= set(demands)
    neighbors = set().union(*(graph[d] for d in exact))
    assert neighbors == set(map(tuple, cut['units']))
    assert len(exact) - len(neighbors) == cut['deficiency'] == worst
    assert expected_size == len(demands) - worst


def main():
    p = F / 'existing_compensation_controls.json'
    producer = read(p)
    assert producer['source_queries'] == producer['source_engine_calls'] == 0
    for path, value in producer['input_sha256'].items():
        assert sha(Path(path)) == value
    accepted = read(N / 'independent_audit.json')
    for path in (N / 'root_entry_graph_controls.json', N / 'lifetime_controls.json', N / 'exact_challenge_sources.json'):
        assert sha(path) == accepted['input_sha256'][str(path)]
    graphs = read(N / 'root_entry_graph_controls.json')
    life = read(N / 'lifetime_controls.json')
    geometry = read(S2 / 'source_geometry_controls.json')
    one = read(S1 / 'release_completion_controls.json')
    checked, inputs = [], [p, F / 'check_existing_compensation_v02.py', Path(__file__),
                          F / 'STEP3_GLOBAL_COMPENSATION.md', F / 'STEP3_COMPLETE_MATCHING.md']
    for r in producer['controls']:
        name = r['source']
        fixed_row = next(x for x in one['controls'] if x['source'] == name)
        g1 = {tuple(x['demand']): tuple(x['unit']) for x in fixed_row['g1']}
        reverse = {u: d for d, u in g1.items()}
        if name != 'VINE8':
            l = next(x for x in life['controls'] if x['source'] == name)
            original = next(x for x in graphs['controls'] if x['source'] == name)
            D, U = set(map(tuple, l['D'])), set(map(tuple, l['U']))
            h = {tuple(x['demand']): tuple(x['unit']) for x in original['matching']}
            G = {tuple(x['demand']): set(map(tuple, x['units'])) for x in original['graph']}
            path = Path(l['source_path'])
            assert sha(path) == geometry['input_sha256'][str(path)] == r['source_sha256']
            # Accepted source proof/replay is reused at this exact hash.
            rootgraph = {d: G[d] - set(reverse) for d in D - set(g1)}
            matching_and_cut_check(rootgraph, r['direct_existing_graph_matching_size'], r['direct_cut'])
            geo = next(x for x in geometry['controls'] if x['source'] == name)
            canonical = {d: set() for d in D - set(g1)}
            for port in geo['ports']:
                t, j, _ = port['beta']
                canonical[tuple(port['demand'])] |= {(t, j, 0), (t, j, 1)} - set(reverse)
            matching_and_cut_check(canonical, r['canonical_event_matching_size'], r['canonical_event_cut'])
        else:
            vine = read(N / 'exact_challenge_sources.json')['vine_family_control']
            rows = vine['rows']
            U = {(z['t'], j, b) for z in rows for j in range(1, z['H'] + 1) for b in (0, 1)}
            D = {(z['t'], k) for z in rows for k in range(1, z['Q'] + 1)}
            # Independently gather backwards from each genuine terminal.
            h = {}
            for i, z in enumerate(rows):
                if z['kind'] != 'K' or z['BF_before'][0] == z['key']:
                    assert z['Q'] == 0
                    continue
                ids, at = [i], (i - 1) % len(rows)
                while not (rows[at]['kind'] == 'K' and rows[at]['BF_before'][0] != rows[at]['key']):
                    assert at not in ids
                    ids.insert(0, at)
                    at = (at - 1) % len(rows)
                bits = [(rows[a]['t'], j, b) for a in ids for j in range(1, rows[a]['H'] + 1) for b in (0, 1)]
                assert len(bits) >= z['Q']
                for k in range(1, z['Q'] + 1):
                    h[(z['t'], k)] = bits[k - 1]
        assert set(h) == D and len(set(h.values())) == len(D)
        assert set(h.values()) <= U and set(g1) <= D and set(reverse) <= U
        Fset, R = D - set(g1), U - set(reverse)
        result, visited_demands, visited_bits = dict(g1), set(), set()
        assert len(r['normalization_paths']) == len(Fset)
        for path in r['normalization_paths']:
            root = tuple(path['root'])
            assert root in Fset and root not in result
            d = root
            for i, edge in enumerate(path['edges']):
                u = tuple(edge['comparison_unit'])
                assert tuple(edge['demand']) == d and u == h[d]
                assert d not in visited_demands and u not in visited_bits
                visited_demands.add(d)
                visited_bits.add(u)
                owner = reverse.get(u)
                assert (None if edge['fixed_owner'] is None else tuple(edge['fixed_owner'])) == owner
                if i + 1 == len(path['edges']):
                    assert owner is None and u == tuple(path['terminal']) and u in R
                else:
                    assert owner is not None
                    d = owner
            result[root] = tuple(path['terminal'])
        assert set(result) == D and len(set(result.values())) == len(D)
        assert all(result[d] == u for d, u in g1.items())
        assert len(R) - len(Fset) == len(U) - len(D)
        assert {tuple(x['demand']): tuple(x['unit']) for x in r['normalized_residual_pairs']} == {d: result[d] for d in Fset}
        checked.append(dict(source=name, Q=len(D), residual=len(Fset), literal_g1_preserved=len(g1),
                            distinct_free_terminals=len(Fset), direct_cut=r.get('direct_cut')))
        assert time.process_time() - START < CAP - 1
    # Coefficient identities for the written m-parameter corollary. The
    # source RR/closure argument is inherited, not established by samples.
    # Each pair means a*m+b, with arbitrary integer m>=4.
    add = lambda p, q: (p[0] + q[0], p[1] + q[1])
    subtract = lambda p, q: (p[0] - q[0], p[1] - q[1])
    B0, B1, B2, Z, local_units = (1, -1), (0, 1), (0, 0), (0, 0), (0, 2)
    assert add(add(B0, B1), B2) == (1, 0)
    assert subtract(B0, add(B2, Z)) == (1, -1)
    local_free = subtract(local_units, (0, 1))
    assert local_free == (0, 1) and subtract(B0, local_free) == (1, -2)
    out = dict(status='PASS_EXACT_PINNED_CUTS_AND_G1_COMPLETIONS', controls=checked,
               source_queries=0, source_engine_calls=0,
               independent_implementation=True, same_research_agent=True,
               external_or_formal_review=False, universal_funding_proved=False,
               symbolic_corollary='coefficient identities checked; source-uniform proof is the written inherited RR/PC35 argument',
               input_sha256={str(q): sha(q) for q in inputs})
    with (F / 'independent_compensation_audit.json').open('x', encoding='utf8') as output:
        json.dump(out, output, indent=2)
    print(json.dumps(dict(status=out['status'], controls=checked, source_queries=0)))


if __name__ == '__main__':
    main()
