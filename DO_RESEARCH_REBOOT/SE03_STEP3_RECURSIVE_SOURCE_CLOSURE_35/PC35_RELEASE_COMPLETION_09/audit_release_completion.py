"""Independent cached-data check. Stack pairing; no producer imports or splay calls."""
import hashlib
import json
import sys
import time
from pathlib import Path

F = Path(__file__).resolve().parent
OLD = F.parent / 'CONTINUATION_04'
ND = F.parent / 'ND35_COMPLEMENT_08'
CAP = float(sys.argv[1])
START = time.process_time()

def read(p):
    return json.loads(p.read_text(encoding='utf-8'))

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def subtree_sets(tree):
    # Iterative postorder, separate from producer's recursive label routine.
    done, labels, todo = {}, set(), [(tree, False)]
    while todo:
        node, visited = todo.pop()
        if node is None:
            continue
        if not visited:
            todo += [(node, True), (node[2], False), (node[1], False)]
        else:
            label = done.get(id(node[1]), frozenset()) | done.get(id(node[2]), frozenset()) | {node[0]}
            done[id(node)] = label
            labels.add(label)
    return labels

def main():
    result_path = F / 'release_completion_controls.json'
    result = read(result_path)
    for name, expected in result['input_sha256'].items():
        assert sha(Path(name)) == expected
    prior = read(OLD / 'independent_core_sector_neutral.json')
    zrc = read(ND / 'zig_release_complement_controls.json')
    source_data = read(ND / 'lifetime_controls.json')
    controls = []
    for data in source_data['controls']:
        trace = []
        for s in data['fine_steps']:
            trace.append((len(s['before_missing']), len(s['after_missing']), s['kind'], s['t'],
                          tuple(s['unit']) if s['unit'] else None,
                          tuple(s['demand']) if s['demand'] else None, s['slot'], s['pattern']))
        controls.append((data['source'], trace, set(map(tuple, data['U'])), set(map(tuple, data['D']))))
    vine = read(ND / 'exact_challenge_sources.json')['vine_family_control']
    trace, U, D = [], set(), set()
    for row in vine['rows']:
        t = row['t']
        U |= {(t, j, b) for j in range(1, row['H'] + 1) for b in (0, 1)}
        D |= {(t, k) for k in range(1, row['Q'] + 1)}
        for ev in row['A_events']:
            for rot in ev['rotations']:
                before = len(subtree_sets(row['BF_before']) - subtree_sets(rot['before']))
                after = len(subtree_sets(row['BF_before']) - subtree_sets(rot['after']))
                trace.append((before, after, 'A', t, (t, ev['j'], rot['bit']), None,
                              'A_RELEASE' if after < before else None, ev['pattern']))
        k = 0
        for ev in row['BF_events']:
            double = len(ev['rotations']) == 2
            if double:
                k += 1
            demand = (t, k) if double else None
            paid = False
            for rot in ev['rotations']:
                before = len(subtree_sets(rot['before']) - subtree_sets(row['A_after']))
                after = len(subtree_sets(rot['after']) - subtree_sets(row['A_after']))
                slot = None
                if after < before:
                    slot = ('B2_RELEASE' if paid else 'PAYMENT') if double else 'BZIG_RELEASE'
                    paid = True
                trace.append((before, after, 'B', t, None, demand, slot, ev['pattern']))
    controls.append(('VINE8', trace, U, D))
    summaries = []
    for name, trace, U, D in controls:
        saved = next(r for r in result['controls'] if r['source'] == name)
        minimum_index = min(range(len(trace)), key=lambda i: trace[i][0])
        stack, cross = [], {}
        for offset in range(len(trace)):
            i = (minimum_index + offset) % len(trace)
            before, after, kind, t, unit, demand, slot, pattern = trace[i]
            if after > before:
                assert after == before + 1 and kind == 'A' and unit in U
                stack.append((after, unit))
            elif after < before:
                level, donor = stack.pop()
                assert before == level and after == before - 1
                cross[i] = donor
        assert not stack and len(cross) == len(set(cross.values()))
        gp = {s[5]: cross[i] for i, s in enumerate(trace) if s[6] == 'PAYMENT'}
        gz = {tuple(p['demand']): tuple(p['unit']) for p in
              next(r for r in zrc['controls'] if r['source'] == name)['g_Z']}
        g1 = {tuple(p['demand']): tuple(p['unit']) for p in saved['g1']}
        assert all(g1[d] == u for d, u in gz.items())
        assert all(gz[d] == u for d, u in gp.items())
        expected_new, expected_residual, expected_surplus = {}, set(), set()
        for access in saved['accesses']:
            t, q = access['t'], access['q']
            assert {(t, k) for k in range(1, q + 1)} == {d for d in D if d[0] == t}
            local = [(i, s) for i, s in enumerate(trace) if s[2] == 'B' and s[3] == t]
            changes = {k: sum(s[0] - s[1] for _, s in local if s[5] == (t, k))
                       for k in range(1, q + 1)}
            counts = [sum(v == j for v in changes.values()) for j in range(3)]
            assert counts == [access['B0'], access['B1'], access['B2']]
            zigs = [i for i, s in local if s[6] == 'BZIG_RELEASE']
            ell = int(q > 0 and changes[q] == 0)
            assert (len(zigs), ell) == (access['Z'], access['ell'])
            if ell:
                assert len(zigs) == 1 and gz[(t, q)] == cross[zigs[0]]
            internal = [(t, k) for k in range(1, q) if changes[k] == 0]
            slots = [i for i, s in local if s[6] in ('B2_RELEASE', 'BZIG_RELEASE')
                     and not (ell and i == zigs[0])]
            cut = min(len(internal), len(slots))
            selected = {d: cross[slots[j]] for j, d in enumerate(internal[:cut])}
            assert {tuple(p['demand']): tuple(p['actual_A_bit']) for p in access['new_pairs']} == selected
            expected_new.update(selected)
            expected_residual.update(internal[cut:])
            expected_surplus.update(cross[i] for i in slots[cut:])
            assert access['d'] == len(internal) - cut == max(0, counts[0] - counts[2] - len(zigs))
            assert access['s'] == len(slots) - cut == max(0, counts[2] + len(zigs) - counts[0])
        assert g1 == gz | expected_new
        assert D - set(g1) == expected_residual
        assert len(g1) == len(set(g1.values())) and set(g1.values()) <= U
        positives = {s[4] for s in trace if s[1] > s[0]}
        negatives = {cross[i] for i, s in enumerate(trace) if s[2] == 'A' and s[1] < s[0]}
        remainder = U - set(g1.values())
        assert remainder == (U - positives) | negatives | expected_surplus
        assert len(remainder) == len(U) - len(positives) + len(negatives) + len(expected_surplus)
        assert len(remainder) - len(expected_residual) == len(U) - len(D)
        summaries.append(dict(source=name, preserved=len(gz), new=len(expected_new),
                              residual=len(expected_residual), remainder=len(remainder)))
        assert time.process_time() - START < CAP - 1

    # Exercise a genuine NEW internal payment, using an already accepted source.
    private = next(r for r in prior['controls'] if r['source'] == 'PRIVATE_HELPER')
    source_path = OLD.parent.parent / 'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01/B_full_spectrum_edge_0_closed_source.json'
    assert sha(source_path) == prior['input_sha256'][str(source_path)]
    rows = read(source_path)['period_rows']
    D = {(row['absolute_t'], k) for row in rows for k in range(1, row['QF'] + 1)}
    gp = {tuple(p['demand']): tuple(p['actual_bit']) for p in private['g_plus']}
    neutral = D - set(gp)
    assert neutral == {(169, 2)}
    assert next(row for row in rows if row['absolute_t'] == 169)['QF'] == 3
    # The ONLY neutral is internal, so g_Z=g_plus for this entire control.
    extra = [p for p in private['cyclic_level_pairings']
             if p['slot'] == 'B_DOUBLE_EXTRA_RELEASE' and p['demand'][0] == 169]
    assert len(extra) == 1 and tuple(extra[0]['demand']) == (169, 1)
    donor = tuple(extra[0]['actual_bit'])
    assert donor == (169, 1, 1) and donor not in gp.values()
    assert donor in set(map(tuple, private['analytical_remainder_bits']))
    full = gp | {(169, 2): donor}
    assert set(full) == D and len(set(full.values())) == len(D) == 18
    positive_control = dict(source='PRIVATE_HELPER', demand=[169, 2],
                            B2_double=[169, 1], release_fine_index=extra[0]['decrease_source_step'],
                            original_A_bit=list(donor), preserved=17, new=1, residual=0,
                            scope='cached accepted source; B2 release suffices regardless of terminal zig')
    report = dict(status='PASS_STEP1_INDEPENDENT_CACHED_AND_EXACT_INVENTORY_CHECK',
                  controls=summaries, positive_internal_payment=positive_control,
                  source_queries=0, source_engine_calls=0,
                  old_owner_maps_modified=False, same_agent_distinct_implementation=True,
                  formal_or_external_review=False,
                  universal_status='symbolic proof; controls are finite challenges only',
                  input_sha256={str(p): sha(p) for p in (result_path, F / 'audit_release_completion.py', source_path,
                                                        OLD / 'independent_core_sector_neutral.json')})
    with (F / 'independent_release_audit.json').open('x', encoding='utf-8') as out:
        json.dump(report, out, indent=2)
    print(json.dumps(report | {'input_sha256': 'recorded in artifact'}))
    assert time.process_time() - START < CAP - 1

if __name__ == '__main__':
    main()
