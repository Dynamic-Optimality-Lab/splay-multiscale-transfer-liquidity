"""Literal free-term identities and annotations of PINNED CACHED traces only."""
import collections
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

def clusters(tree, S):
    found = set()
    def visit(node):
        if node is None:
            return frozenset()
        label = visit(node[1]) | visit(node[2]) | ({node[0]} if node[0] in S else set())
        if label:
            found.add(label)
        return label
    visit(tree)
    return found

def descendants(node, S):
    if node is None:
        return set()
    return descendants(node[1], S) | descendants(node[2], S) | ({node[0]} if node[0] in S else set())

def lca(tree, keys):
    lo, hi = min(keys), max(keys)
    while tree is not None:
        if hi < tree[0]:
            tree = tree[1]
        elif lo > tree[0]:
            tree = tree[2]
        else:
            return tree
    raise AssertionError('keys not in cached physical tree')

def depth(tree, key):
    n = 0
    while tree[0] != key:
        tree = tree[1] if key < tree[0] else tree[2]
        n += 1
    return n

def free_term_identities():
    # Hangers are uninterpreted atoms. These are universal substitution
    # identities, not splaying actual or searched source trees.
    def node(k, l, r):
        return (k, l, r)
    g, p, x = 'g', 'p', 'x'
    a, b, c, d = ('T0', 'T1', 'T2', 'T3')
    cases = {
        'LL': (node(g, node(p, node(x, a, b), c), d),
               [('', 'R'), ('', 'R')],
               node(p, node(x, a, b), node(g, c, d)),
               node(x, a, node(p, b, node(g, c, d)))),
        'RR': (node(g, a, node(p, b, node(x, c, d))),
               [('', 'L'), ('', 'L')],
               node(p, node(g, a, b), node(x, c, d)),
               node(x, node(p, node(g, a, b), c), d)),
        'LR': (node(g, node(p, a, node(x, b, c)), d),
               [('L', 'L'), ('', 'R')],
               node(g, node(x, node(p, a, b), c), d),
               node(x, node(p, a, b), node(g, c, d))),
        'RL': (node(g, a, node(p, node(x, b, c), d)),
               [('R', 'R'), ('', 'L')],
               node(g, a, node(x, b, node(p, c, d))),
               node(x, node(g, a, b), node(p, c, d))),
    }
    expected = {
        'LL': [('px', (0, 1, 2), 'g', (2, 3)), ('x', (0, 1), 'pg', (1, 2, 3))],
        'RR': [('px', (1, 2, 3), 'g', (0, 1)), ('x', (2, 3), 'gp', (0, 1, 2))],
        'LR': [('x', (1, 2), 'p', (0, 1)), ('px', (0, 1, 2), 'g', (2, 3))],
        'RL': [('x', (1, 2), 'p', (2, 3)), ('px', (1, 2, 3), 'g', (0, 1))],
    }
    def label(term):
        if isinstance(term, str):
            return {term.replace('T', 'U')}
        return {term[0]} | label(term[1]) | label(term[2])
    def rotate(term, direction):
        k, l, r = term
        if direction == 'R':
            promoted, inner, middle = l
            out = node(promoted, inner, node(k, middle, r))
            return out, label(l), label(out[2])
        promoted, middle, outer = r
        out = node(promoted, node(k, l, middle), outer)
        return out, label(r), label(out[1])
    def at(term, path, direction):
        if not path:
            return rotate(term, direction)
        slot = 1 if path[0] == 'L' else 2
        child, old, new = at(term[slot], path[1:], direction)
        out = list(term)
        out[slot] = child
        return tuple(out), old, new
    rows = []
    for name, (before, operations, mid, after) in cases.items():
        state, ports = before, []
        for j, (path, direction) in enumerate(operations):
            state, old, new = at(state, path, direction)
            key_i, ui, key_j, uj = expected[name][j]
            assert old == set(key_i) | {'U' + str(i) for i in ui}
            assert new == set(key_j) | {'U' + str(i) for i in uj}
            assert state == (mid if j == 0 else after)
            ports.append(dict(removed=sorted(old), created=sorted(new)))
        rows.append(dict(pattern=name, before=before, intermediate=mid, after=after, ports=ports))
    # Exact R,G return, with completely opaque arbitrary private hangers.
    U = node('G', 'A', node('C', node('x', 'B0', 'B1'), node('R', 'D', 'E')))
    term, _, _ = at(U, '', 'L')
    term, _, _ = at(term, '', 'L')
    after_R = node('R', node('C', node('G', 'A', node('x', 'B0', 'B1')), 'D'), 'E')
    assert term == after_R
    term, _, _ = at(term, '', 'R')
    term, _, _ = at(term, '', 'R')
    assert term == U
    term, _, _ = at(U, 'R', 'R')
    term, _, _ = at(term, '', 'L')
    assert term == node('x', node('G', 'A', 'B0'), node('C', 'B1', node('R', 'D', 'E')))
    return dict(four_frames=rows, exact_return=dict(before=U, after_R=after_R, after_RG=U, future_x=term),
                interpretation='free-term rotation identities, no original-source engine calls')

def make_vine(data):
    r = data['r']
    S = set(range(1, r + 1))
    fine = []
    for row in data['rows']:
        for kind, events in [('A', row['A_events']), ('B', row['BF_events'])]:
            di = 0
            for event in events:
                isdouble = len(event['rotations']) == 2
                if kind == 'B' and isdouble:
                    di += 1
                for rot in event['rotations']:
                    before = (clusters(row['BF_before'], S) - clusters(rot['before'], S)) if kind == 'A' else (clusters(rot['before'], S) - clusters(row['A_after'], S))
                    after = (clusters(row['BF_before'], S) - clusters(rot['after'], S)) if kind == 'A' else (clusters(rot['after'], S) - clusters(row['A_after'], S))
                    fine.append(dict(index=len(fine), kind=kind, t=row['t'], access_key=row['key'],
                                     event_j=event['j'], rotation_bit=rot['bit'], pattern=event['pattern'],
                                     unit=(row['t'], event['j'], rot['bit']) if kind == 'A' else None,
                                     demand=(row['t'], di) if kind == 'B' and isdouble else None,
                                     before_missing=sorted(map(sorted, before)), after_missing=sorted(map(sorted, after)),
                                     removed=sorted(map(sorted, before - after)), added=sorted(map(sorted, after - before))))
    return dict(source='VINE8', S=sorted(S), fine_steps=fine), data['rows']

def main():
    step1 = read(S1 / 'release_completion_controls.json')
    accepted1 = read(S1 / 'independent_release_audit.json')
    accepted = read(N / 'independent_audit.json')
    assert accepted1['status'] == 'PASS_STEP1_INDEPENDENT_CACHED_AND_EXACT_INVENTORY_CHECK'
    assert sha(S1 / 'release_completion_controls.json') == accepted1['input_sha256'][str(S1 / 'release_completion_controls.json')]
    for name in ('lifetime_controls.json', 'exact_challenge_sources.json', 'LIFETIME_NORMAL_FORM.md', 'ROOT_ENTRY_LEMMA.md'):
        assert sha(N / name) == accepted['input_sha256'][str(N / name)]
    inputs = [N / name for name in ('lifetime_controls.json', 'exact_challenge_sources.json', 'independent_audit.json',
                                   'LIFETIME_NORMAL_FORM.md', 'ROOT_ENTRY_LEMMA.md', 'ZIG_RELEASE_COMPLEMENT_THEOREM.md')]
    inputs += [S1 / name for name in ('release_completion_controls.json', 'independent_release_audit.json',
                                     'STEP1_PC35_RELEASE_COMPLETION.md', 'STEP1_EXACT_RESIDUAL_IDENTITY.md')]
    inputs += [F / name for name in ('STEP2_EXACT_SOURCE_GEOMETRY.md', 'STEP2_INTERACTION_THEOREM.md', 'derive_source_geometry.py')]
    lifetime = read(N / 'lifetime_controls.json')
    controls = []
    for data in lifetime['controls']:
        path = Path(data['source_path'])
        assert sha(path) == read(C / 'CONTINUATION_04/independent_core_sector_neutral.json')['input_sha256'][str(path)]
        controls.append((data, read(path)['period_rows']))
        inputs.append(path)
    controls.append(make_vine(read(N / 'exact_challenge_sources.json')['vine_family_control']))
    reports = []
    for data, rows in controls:
        name, S, fine = data['source'], set(data['S']), data['fine_steps']
        prior = next(r for r in step1['controls'] if r['source'] == name)
        residual = {tuple(d) for a in prior['accesses'] for d in a['residual_demands']}
        g1 = {tuple(p['unit']): tuple(p['demand']) for p in prior['g1']}
        rowby = {row['t']: row for row in rows}
        ainfo = {}
        for row in rows:
            for ev in row.get('A_events', []):
                for rot in ev['rotations']:
                    ainfo[(row['t'], ev['j'], rot['bit'])] = (row, ev, rot)
        ports, geometry = [], []
        for demand in sorted(residual):
            steps = [s for s in fine if s['kind'] == 'B' and s['demand'] and tuple(s['demand']) == demand]
            assert len(steps) == 2 and all(len(s['added']) == len(s['removed']) == 1 for s in steps)
            x = rowby[demand[0]]['key']
            A = rowby[demand[0]]['A_after']
            assert A[0] == x
            I1, I2 = (set(s['removed'][0]) for s in steps)
            J1, J2 = (set(s['added'][0]) for s in steps)
            W = I2 | J2
            pattern = steps[0]['pattern']
            assert (I2 < I1) if pattern in ('LL', 'RR') else (I1 < I2)
            details = []
            for J in (J1, J2):
                v = lca(A, J)
                blockers = descendants(v, S) - J
                assert blockers and frozenset(J) not in clusters(A, S)
                details.append(dict(created=sorted(J), A_LCA=v[0], blockers=sorted(blockers)))
            if pattern in ('LL', 'RR'):
                assert J1 < J2
                side = {z for z in W if (z > x if pattern == 'LL' else z < x)}
                assert J2 == side
                assert all(z > max(W) if pattern == 'LL' else z < min(W) for z in details[1]['blockers'])
            else:
                assert {frozenset(J1), frozenset(J2)} == {frozenset(z for z in W if z < x), frozenset(z for z in W if z > x)}
                for det in details:
                    assert all(z < min(W) if max(det['created']) < x else z > max(W) for z in det['blockers'])
            geometry.append(dict(demand=demand, pattern=pattern, W=sorted(W), removed=[sorted(I1), sorted(I2)], created=details))
            for s in steps:
                i, I = s['index'], frozenset(s['removed'][0])
                addition = None
                for offset in range(1, len(fine) + 1):
                    j = (i - offset) % len(fine)
                    if I in map(frozenset, fine[j]['added']):
                        addition = j
                        break
                assert addition is not None
                distance = (i - addition) % len(fine)
                assert distance > 0
                assert all(I in map(frozenset, fine[(addition + k) % len(fine)]['before_missing']) for k in range(1, distance + 1))
                origin = fine[addition]
                if origin['kind'] == 'A':
                    witness, typ = origin, 'A_ADDITION'
                else:
                    witness, typ = None, 'ROOT_ENTRY'
                    assert origin['access_key'] not in I
                    for k in range(1, distance):
                        candidate = fine[(addition + k) % len(fine)]
                        if candidate['kind'] == 'A':
                            row, ev, rot = ainfo[tuple(candidate['unit'])]
                            if rot['before'][0] not in I and rot['after'][0] in I:
                                witness = candidate
                                break
                    assert witness is not None
                beta = tuple(witness['unit'])
                row, ev, rot = ainfo[beta]
                ports.append(dict(demand=demand, B_rotation=s['index'], label=sorted(I), addition_fine_index=addition,
                                  witness_fine_index=witness['index'], witness_type=typ, beta=beta,
                                  root_before=rot['before'][0], root_after=rot['after'][0],
                                  wrapped_label_run=addition >= i))
        assert len(ports) == 2 * len(residual)
        assert len({(tuple(p['beta']), tuple(p['label'])) for p in ports}) == len(ports)
        groups = []
        for beta in sorted({tuple(p['beta']) for p in ports}):
            attached = [p for p in ports if tuple(p['beta']) == beta]
            row, ev, rot = ainfo[beta]
            u, v = rot['before'][0], rot['after'][0]
            labels = [set(p['label']) for p in attached]
            if u != v and v in S:
                chain = [K for K in clusters(row['BF_before'], S) if K != S and v in K and u not in K]
                assert all(frozenset(K) in chain for K in labels)
                ordered = sorted(labels, key=len)
                assert all(a < b for a, b in zip(ordered, ordered[1:]))
                bound = len(chain)
                B = row['BF_before']
                expected = depth(B, v) - depth(B, lca(B, {u, v})[0]) if u in S else depth(B, v)
                assert bound == expected
                mode = 'S_ROOT_PROMOTION_CHAIN'
            else:
                assert len(attached) <= 1 and all(p['witness_type'] == 'A_ADDITION' for p in attached)
                bound, mode = 1, 'SINGLETON'
            assert len(attached) <= bound
            if u != v:
                assert ev['j'] == max(e['j'] for e in row['A_events'])
            wf = next(s for s in fine if s['kind'] == 'A' and tuple(s['unit']) == beta)
            change = len(wf['after_missing']) - len(wf['before_missing'])
            if change <= 0:
                assert beta not in g1
            groups.append(dict(beta=beta, source_root_change=[u, v], mode=mode, tag_count=len(attached), bound=bound,
                               labels=sorted([sorted(k) for k in labels], key=len), Psi_change=change,
                               frozen_g1_owner=g1.get(beta), raw_free=beta not in g1))
        events = []
        for t, j in sorted({tuple(p['beta'])[:2] for p in ports}):
            event_groups = [g for g in groups if tuple(g['beta'])[:2] == (t, j)]
            events.append(dict(event=[t, j], tag_count=sum(g['tag_count'] for g in event_groups),
                               actual_units=[dict(bit=[t, j, b], frozen_g1_owner=g1.get((t, j, b))) for b in (0, 1)]))
        assert sum(g['tag_count'] for g in groups) == sum(e['tag_count'] for e in events) == len(ports)
        reports.append(dict(source=name, residual=len(residual), ports=ports, double_geometry=geometry,
                            rotation_groups=groups, event_groups=events,
                            max_rotation_load=max([g['tag_count'] for g in groups], default=0),
                            max_event_load=max([e['tag_count'] for e in events], default=0),
                            old_assignments_modified=False))
        assert time.process_time() - START < CAP - 1
    result = dict(status='PASS_STEP2_LITERAL_IDENTITIES_AND_CACHED_GEOMETRY',
                  free_term_proofs=free_term_identities(), controls=reports,
                  source_queries=0, source_engine_calls=0,
                  universal_proof='written symbolic four-frame/LCA/canonical-tag/chain theorems',
                  no_new_matching_or_potential=True,
                  input_sha256={str(p): sha(p) for p in dict.fromkeys(inputs)})
    with (F / 'source_geometry_controls.json').open('x', encoding='utf-8') as out:
        json.dump(result, out, indent=2)
    print(json.dumps(dict(status=result['status'], controls=[dict(source=r['source'], residual=r['residual'], ports=len(r['ports']),
                     witnesses=len(r['rotation_groups']), max_rotation_load=r['max_rotation_load'], max_event_load=r['max_event_load']) for r in reports],
                     source_queries=0, source_engine_calls=0)))

if __name__ == '__main__':
    main()
