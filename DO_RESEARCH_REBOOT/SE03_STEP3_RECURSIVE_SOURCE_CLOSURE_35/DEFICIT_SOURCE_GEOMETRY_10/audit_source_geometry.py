"""Separate cached proof checker: forward label-runs, physical ancestor paths.

Never import the producer or invoke an ordinary-splay/source engine.
"""
import bisect
import hashlib
import json
import sys
import time
from pathlib import Path

F = Path(__file__).resolve().parent
C = F.parent
N = C / 'ND35_COMPLEMENT_08'
S1 = C / 'PC35_RELEASE_COMPLETION_09'
CAP = float(sys.argv[1])
START = time.process_time()

def read(p):
    return json.loads(p.read_text(encoding='utf-8'))

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def index_tree(tree, S):
    # Physical paths and iterative postorder; no producer's LCA or recursion.
    paths, below, jobs = {}, {}, [(tree, (), False)]
    while jobs:
        v, ancestors, finish = jobs.pop()
        if v is None:
            continue
        key = v[0]
        if finish:
            below[key] = (below[v[1][0]] if v[1] else set()) | (below[v[2][0]] if v[2] else set()) | ({key} if key in S else set())
        else:
            paths[key] = ancestors + (key,)
            jobs += [(v, ancestors, True), (v[2], paths[key], False), (v[1], paths[key], False)]
    return paths, below

def common_ancestor(paths, K):
    strings = [paths[k] for k in K]
    prefix = []
    for position in zip(*strings):
        if len(set(position)) != 1:
            break
        prefix.append(position[0])
    return prefix[-1]

def symbolic_promotions(term, vertices):
    # Free constructor variables are opaque leaves. Only named branch
    # vertices are promoted; this is algebra, not an evaluated source W.
    children, parents = {}, {}
    def collect(t, parent=None):
        key = t[0] if isinstance(t, (tuple, list)) else t
        parents[key] = parent
        if isinstance(t, (tuple, list)):
            children[key] = [collect(t[1], key), collect(t[2], key)]
        else:
            children[key] = None
        return key
    root = collect(term)
    def emit(key):
        return key if children[key] is None else [key, emit(children[key][0]), emit(children[key][1])]
    results = []
    for v in vertices:
        p = parents[v]
        a = parents[p]
        side = children[p].index(v)
        middle = children[v][1 - side]
        children[p][side] = middle
        parents[middle] = p
        children[v][1 - side] = p
        parents[p] = v
        parents[v] = a
        if a is None:
            root = v
        else:
            children[a][children[a].index(p)] = v
        results.append(emit(root))
    return results

def vine_trace(data):
    S, trace = set(range(1, data['r'] + 1)), []
    def labels(t):
        return {frozenset(k) for k in index_tree(t, S)[1].values() if k}
    for r in data['rows']:
        for phase, events in [('A', r['A_events']), ('B', r['BF_events'])]:
            k = 0
            for ev in events:
                double = len(ev['rotations']) == 2
                if phase == 'B' and double:
                    k += 1
                for z in ev['rotations']:
                    old = labels(r['BF_before']) - labels(z['before']) if phase == 'A' else labels(z['before']) - labels(r['A_after'])
                    new = labels(r['BF_before']) - labels(z['after']) if phase == 'A' else labels(z['after']) - labels(r['A_after'])
                    trace.append(dict(index=len(trace), kind=phase, t=r['t'], access_key=r['key'], event_j=ev['j'],
                                      pattern=ev['pattern'], unit=[r['t'], ev['j'], z['bit']] if phase == 'A' else None,
                                      demand=[r['t'], k] if phase == 'B' and double else None,
                                      before_missing=sorted(map(sorted, old)), after_missing=sorted(map(sorted, new)),
                                      removed=sorted(map(sorted, old-new)), added=sorted(map(sorted, new-old))))
    return S, trace, data['rows']

def main():
    target = F / 'source_geometry_controls.json'
    result = read(target)
    for name, expected in result['input_sha256'].items():
        assert sha(Path(name)) == expected
    step1 = read(S1 / 'release_completion_controls.json')
    algebra = result['free_term_proofs']
    for row in algebra['four_frames']:
        operations = ['p', 'x'] if row['pattern'] in ('LL', 'RR') else ['x', 'x']
        assert symbolic_promotions(row['before'], operations) == [row['intermediate'], row['after']]
    ret = algebra['exact_return']
    rr = symbolic_promotions(ret['before'], ['C', 'R'])[-1]
    assert rr == ret['after_R']
    assert symbolic_promotions(rr, ['C', 'G'])[-1] == ret['before'] == ret['after_RG']
    assert symbolic_promotions(ret['before'], ['x', 'x'])[-1] == ret['future_x']
    inherited = read(N / 'lifetime_controls.json')
    sources = {r['source']: (set(r['S']), r['fine_steps'], read(Path(r['source_path']))['period_rows']) for r in inherited['controls']}
    sources['VINE8'] = vine_trace(read(N / 'exact_challenge_sources.json')['vine_family_control'])
    summaries = []
    for control in result['controls']:
        name = control['source']
        S, trace, rows = sources[name]
        rowby = {r['t']: r for r in rows}
        frozen = next(r for r in step1['controls'] if r['source'] == name)
        residual = {tuple(d) for a in frozen['accesses'] for d in a['residual_demands']}
        assert len(residual) == control['residual']
        owners = {tuple(p['unit']): tuple(p['demand']) for p in frozen['g1']}
        rotations = {(r['t'], e['j'], z['bit']): (r, e, z)
                     for r in rows for e in r.get('A_events', []) for z in e['rotations']}
        # Check the ENTIRE B path-removal identity from original cached traces.
        for r in rows:
            x = r['key']
            paths, below = index_tree(r['BF_before'], S)
            bsteps = [s for s in trace if s['kind'] == 'B' and s['t'] == r['t']]
            expected = {frozenset(k) for k in below.values() if x in k and k != S} if r['kind'] == 'K' else set()
            removed = [frozenset(s['removed'][0]) for s in bsteps]
            assert len(removed) == len(set(removed)) and set(removed) == expected
            if bsteps:
                assert len(removed) == len(paths[x]) - 1
        ports = control['ports']
        assert {tuple(p['demand']) for p in ports} == residual
        assert len(ports) == 2 * len(residual)
        assert len({p['B_rotation'] for p in ports}) == len(ports)
        assert len({(tuple(p['beta']), tuple(p['label'])) for p in ports}) == len(ports)
        # Forward cyclic addition->next-removal pairing, independent of
        # producer's backward latest-addition search.
        run_origins = {}
        for I in {frozenset(p['label']) for p in ports}:
            births = [s['index'] for s in trace if I in map(frozenset, s['added'])]
            deaths = [s['index'] for s in trace if I in map(frozenset, s['removed'])]
            assert births and len(births) == len(deaths)
            for j in births:
                dest = deaths[bisect.bisect_right(deaths, j) % len(deaths)]
                assert (dest, I) not in run_origins
                run_origins[(dest, I)] = j
        for port in ports:
            i, I = port['B_rotation'], frozenset(port['label'])
            assert trace[i]['removed'] == [sorted(I)]
            j = run_origins[(i, I)]
            assert j == port['addition_fine_index']
            delta = (i-j) % len(trace)
            middle = [trace[(j+k) % len(trace)] for k in range(1, delta)]
            if trace[j]['kind'] == 'A':
                beta, typ = trace[j], 'A_ADDITION'
            else:
                eligible = []
                for s in middle:
                    if s['kind'] == 'A':
                        r, e, z = rotations[tuple(s['unit'])]
                        if z['before'][0] not in I and z['after'][0] in I:
                            eligible.append(s)
                assert eligible
                beta, typ = eligible[0], 'ROOT_ENTRY'
            assert beta['index'] == port['witness_fine_index']
            assert beta['unit'] == port['beta'] and typ == port['witness_type']
        for geo in control['double_geometry']:
            d = tuple(geo['demand'])
            local = [s for s in trace if s['kind'] == 'B' and s['demand'] and tuple(s['demand']) == d]
            assert len(local) == 2 and all(s['pattern'] == geo['pattern'] for s in local)
            assert [s['removed'][0] for s in local] == geo['removed']
            paths, below = index_tree(rowby[d[0]]['A_after'], S)
            for n, det in enumerate(geo['created']):
                J = set(local[n]['added'][0])
                assert sorted(J) == det['created']
                v = common_ancestor(paths, J)
                assert det['A_LCA'] == v and det['blockers'] == sorted(below[v] - J)
                assert det['blockers']
        for group in control['rotation_groups']:
            beta = tuple(group['beta'])
            attached = [p for p in ports if tuple(p['beta']) == beta]
            r, e, z = rotations[beta]
            u, v = z['before'][0], z['after'][0]
            assert len(attached) == group['tag_count'] and group['source_root_change'] == [u, v]
            if u != v and v in S:
                paths, below = index_tree(r['BF_before'], S)
                K = {frozenset(below[k]) for k in paths[v][1:] if u not in below[k]}
                assert {frozenset(p['label']) for p in attached} <= K
                assert group['mode'] == 'S_ROOT_PROMOTION_CHAIN' and len(K) == group['bound']
                assert e['j'] == max(ev['j'] for ev in r['A_events'])
            else:
                assert len(attached) <= 1 and group['mode'] == 'SINGLETON'
            assert tuple(group['frozen_g1_owner']) == owners[beta] if beta in owners else group['frozen_g1_owner'] is None
            assert group['raw_free'] == (beta not in owners)
            if group['Psi_change'] <= 0:
                assert beta not in owners
        for event in control['event_groups']:
            t, j = event['event']
            assert [b['bit'] for b in event['actual_units']] == [[t, j, 0], [t, j, 1]]
            assert event['tag_count'] == sum(tuple(p['beta'])[:2] == (t, j) for p in ports)
        summaries.append(dict(source=name, residual=len(residual), incidences=len(ports),
                              distinct_A_rotations=len(control['rotation_groups']),
                              max_rotation_load=control['max_rotation_load']))
        assert time.process_time() - START < CAP - 1
    accepted = read(N / 'independent_audit.json')
    ccr = next(r for r in accepted['component_checks'] if r['source'] == 'CCR')
    assert ccr['B_only_neutral_cycles'] == 7
    report = dict(status='PASS_STEP2_INDEPENDENT_FORWARD_RUNS_PATHS_AND_LITERAL_TERMS',
                  controls=summaries, reused_CCR_B_only_cycles=7,
                  identity_scope='all four free-term frames and arbitrary-hanger exact R,G return',
                  universal_proof='written literal/LCA/tag injectivity/laminarity proofs; finite checks do not establish quantifiers',
                  source_queries=0, source_engine_calls=0, no_matching_constructed=True,
                  frozen_assignments_modified=False, same_agent_distinct_implementation=True,
                  external_or_formal_review=False,
                  input_sha256={str(p): sha(p) for p in (target, F / 'audit_source_geometry.py', S1 / 'release_completion_controls.json', N / 'independent_audit.json')})
    with (F / 'independent_geometry_audit.json').open('x', encoding='utf-8') as out:
        json.dump(report, out, indent=2)
    print(json.dumps(report | {'input_sha256': 'recorded in artifact'}))
    assert time.process_time() - START < CAP - 1

if __name__ == '__main__':
    main()
