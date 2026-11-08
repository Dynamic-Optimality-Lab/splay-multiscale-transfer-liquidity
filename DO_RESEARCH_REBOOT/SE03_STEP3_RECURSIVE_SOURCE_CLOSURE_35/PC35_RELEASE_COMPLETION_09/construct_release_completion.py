"""Step 1 only: consume pinned cached annotations, never execute a splay."""
import bisect
import collections
import hashlib
import json
import sys
import time
from pathlib import Path

F = Path(__file__).resolve().parent
C = F.parent
OLD = C / 'CONTINUATION_04'
ND = C / 'ND35_COMPLEMENT_08'
START = time.process_time()
CAP = float(sys.argv[1])

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def save(name, obj):
    with (F / name).open('x', encoding='utf-8') as out:
        json.dump(obj, out, indent=2)

def labels(tree):
    result = set()
    def visit(node):
        if node is None:
            return frozenset()
        label = visit(node[1]) | visit(node[2]) | {node[0]}
        result.add(label)
        return label
    visit(tree)
    return result

def main():
    old = read(OLD / 'independent_core_sector_neutral.json')
    accepted = read(ND / 'independent_audit.json')
    pc = read(OLD / 'independent_projected_cluster_theorem.json')
    assert accepted['ZRC35'] == 'PROVED_AT_STATED_UNIFORM_RAW_SCOPE'
    assert old['status'] == 'PASS_CSL_LOCAL_INJECTIONS_AND_NEUTRAL_SOURCE_PARTITIONS'
    assert pc['status'] == 'PASS_PC35_ORIGINAL_PAIRED_CLOSED_CONTROL_AND_AF_PROJECTED_FUNDING'
    pins = [
        (old, OLD / 'NEUTRAL_DOUBLE_SOURCE_DECOMPOSITION.md'),
        (accepted, OLD / 'independent_core_sector_neutral.json'),
        (accepted, ND / 'ND35_UNIVERSAL_AUDIT.md'),
        (accepted, ND / 'ZIG_RELEASE_COMPLEMENT_THEOREM.md'),
        (accepted, ND / 'lifetime_controls.json'),
        (accepted, ND / 'zig_release_complement_controls.json'),
        (accepted, ND / 'exact_challenge_sources.json'),
        (pc, OLD / 'PROJECTED_CLUSTER_ACCESS_THEOREM.md'),
    ]
    for receipt, path in pins:
        assert receipt['input_sha256'][str(path)] == sha(path)
    lifetime = read(ND / 'lifetime_controls.json')
    zrc = read(ND / 'zig_release_complement_controls.json')
    controls = []
    inputs = [path for _, path in pins] + [
        ND / 'independent_audit.json', OLD / 'independent_projected_cluster_theorem.json',
        OLD / 'dependency_manifest_03.json',
        F / 'STEP1_PC35_RELEASE_COMPLETION.md', F / 'STEP1_EXACT_RESIDUAL_IDENTITY.md',
        F / 'construct_release_completion.py',
    ]
    for control in lifetime['controls']:
        prior = next(r for r in old['controls'] if r['source'] == control['source'])
        rows = read(Path(control['source_path']))['period_rows']
        fine = []
        for s in control['fine_steps']:
            f = {k: s[k] for k in ('index', 'kind', 't', 'unit', 'demand', 'pattern', 'slot')}
            f['before'], f['after'] = len(s['before_missing']), len(s['after_missing'])
            fine.append(f)
        controls.append((control['source'], fine, set(map(tuple, control['U'])),
                         set(map(tuple, control['D'])),
                         {row['t']: row['qF'] for row in rows},
                         {p['decrease_source_step']: tuple(p['actual_bit'])
                          for p in prior['cyclic_level_pairings']}))
        inputs.append(Path(control['source_path']))
    vine = read(ND / 'exact_challenge_sources.json')['vine_family_control']
    fine, units, demands, qby = [], set(), set(), {}
    def append(before, after, kind, t, pattern, unit=None, demand=None, slot=None):
        fine.append(dict(index=len(fine), before=before, after=after, kind=kind,
                         t=t, pattern=pattern, unit=unit, demand=demand, slot=slot))
    for row in vine['rows']:
        t = row['t']
        qby[t] = row['Q']
        units.update((t, j, b) for j in range(1, row['H'] + 1) for b in (0, 1))
        demands.update((t, k) for k in range(1, row['Q'] + 1))
        jb = labels(row['BF_before'])
        for event in row['A_events']:
            for rot in event['rotations']:
                before, after = len(jb - labels(rot['before'])), len(jb - labels(rot['after']))
                append(before, after, 'A', t, event['pattern'],
                       unit=(t, event['j'], rot['bit']),
                       slot='A_RELEASE' if after < before else None)
        ja = labels(row['A_after'])
        di = 0
        for event in row['BF_events']:
            double = len(event['pattern']) == 2
            d = (t, di + 1) if double else None
            if double:
                di += 1
            first = True
            for rot in event['rotations']:
                before, after = len(labels(rot['before']) - ja), len(labels(rot['after']) - ja)
                slot = None
                if after < before:
                    slot = 'PAYMENT' if double and first else ('B2_RELEASE' if double else 'BZIG_RELEASE')
                    first = False
                append(before, after, 'B', t, event['pattern'], demand=d, slot=slot)
        assert di == row['Q']
    controls.append(('VINE8', fine, units, demands, qby, None))
    reports = []
    for name, fine, units, demands, qby, inherited_cross in controls:
        assert all(s['index'] == i for i, s in enumerate(fine))
        assert all(a['after'] == b['before'] for a, b in zip(fine, fine[1:]))
        assert fine[-1]['after'] == fine[0]['before']
        levels, cross = collections.defaultdict(list), {}
        for s in fine:
            change = s['after'] - s['before']
            assert change in (-1, 0, 1)
            if change == 1:
                assert s['kind'] == 'A' and tuple(s['unit']) in units
                levels[s['after']].append(s['index'])
        for s in fine:
            if s['after'] == s['before'] - 1:
                ups = levels[s['before']]
                u = ups[bisect.bisect_left(ups, s['index']) - 1]
                cross[s['index']] = tuple(fine[u]['unit'])
        assert len(set(cross.values())) == len(cross)
        if inherited_cross is not None:
            assert cross == inherited_cross  # retain the exact existing lambda
        gz_saved = next(r for r in zrc['controls'] if r['source'] == name)
        gz = {tuple(p['demand']): tuple(p['unit']) for p in gz_saved['g_Z']}
        gp = {tuple(s['demand']): cross[s['index']] for s in fine if s['slot'] == 'PAYMENT'}
        assert all(gz[d] == u for d, u in gp.items())
        g1 = dict(gz)
        access_rows = []
        for t, q in sorted(qby.items()):
            steps = [s for s in fine if s['kind'] == 'B' and s['t'] == t]
            drops = {k: sum(s['before'] - s['after'] for s in steps if s['demand'] and tuple(s['demand']) == (t, k))
                     for k in range(1, q + 1)}
            assert all(v in (0, 1, 2) for v in drops.values())
            b0, b1, b2 = (sum(v == k for v in drops.values()) for k in (0, 1, 2))
            zig = [s for s in steps if s['slot'] == 'BZIG_RELEASE']
            z = len(zig)
            assert z <= 1
            ell = int(q > 0 and drops[q] == 0)
            reserved = zig[0]['index'] if ell else None
            if ell:
                assert z == 1 and gz[(t, q)] == cross[reserved]
            internal = [(t, k) for k in range(1, q) if drops[k] == 0]
            releases = [s for s in steps if s['slot'] in ('B2_RELEASE', 'BZIG_RELEASE') and s['index'] != reserved]
            assert len(releases) == b2 + z - ell
            pairs = []
            for d, s in zip(internal, releases):
                u = cross[s['index']]
                assert d not in g1 and u not in g1.values()
                g1[d] = u
                pairs.append(dict(demand=d, release_fine_index=s['index'], actual_A_bit=u))
            remaining = [d for d in internal if d not in g1]
            dcount, surplus = max(0, b0 - b2 - z), max(0, b2 + z - b0)
            assert len(remaining) == dcount
            assert len(releases) - len(pairs) == surplus
            access_rows.append(dict(t=t, q=q, B0=b0, B1=b1, B2=b2, Z=z, ell=ell,
                                    new_pairs=pairs, residual_demands=remaining, d=dcount, s=surplus))
        pbits = {tuple(s['unit']) for s in fine if s['after'] == s['before'] + 1}
        negative = {cross[s['index']] for s in fine if s['kind'] == 'A' and s['after'] == s['before'] - 1}
        unused = {cross[s['index']] for s in fine if s['slot'] in ('B2_RELEASE', 'BZIG_RELEASE')} - set(g1.values())
        pieces = [units - pbits, negative, unused]
        assert all(not a & b for i, a in enumerate(pieces) for b in pieces[i + 1:])
        free = units - set(g1.values())
        assert set().union(*pieces) == free and len(g1) == len(set(g1.values()))
        assert set(g1) <= demands and set(g1.values()) <= units
        residual = demands - set(g1)
        assert residual == {tuple(d) for r in access_rows for d in r['residual_demands']}
        A, Q, P, N = len(units) // 2, len(demands), len(pbits), len(negative)
        b0, b1, b2, z = (sum(r[k] for r in access_rows) for k in ('B0', 'B1', 'B2', 'Z'))
        assert P == N + b1 + 2 * b2 + z
        assert len(free) == 2 * A - P + N + sum(r['s'] for r in access_rows)
        assert len(free) - len(residual) == 2 * A - Q
        reports.append(dict(source=name, A=A, Q=Q, P=P, N=N, B0=b0, B1=b1, B2=b2, Z=z,
                            old_gplus_preserved=len(gp), old_gZ_preserved=len(gz),
                            new_internal_paid=len(g1) - len(gz), residual=len(residual),
                            remaining_raw_units=len(free), accesses=access_rows,
                            g1=[dict(demand=d, unit=u) for d, u in sorted(g1.items())]))
        assert time.process_time() - START < CAP - 1
    out = dict(status='PASS_STEP1_CACHED_RELEASE_COMPLETION', controls=reports,
               source_queries=0, source_engine_calls=0, old_owner_maps_modified=False,
               universal_proof='written ordered-list and exact-inventory proof, not finite controls',
               input_sha256={str(p): sha(p) for p in dict.fromkeys(inputs)})
    save('release_completion_controls.json', out)
    print(json.dumps(dict(status=out['status'], controls=[{k: r[k] for k in
          ('source', 'B0', 'B2', 'Z', 'old_gZ_preserved', 'new_internal_paid', 'residual', 'remaining_raw_units')}
          for r in reports], source_queries=0)))

if __name__ == '__main__':
    main()
