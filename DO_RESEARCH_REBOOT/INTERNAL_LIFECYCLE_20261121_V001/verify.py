"""Independent immutable-tree verification, without importing the producer.

Recomputes full original real rotations, SETs, potentials, costs, cyclic Pi,
actual birth runs, and A gap representatives. Same-agent code independence,
not external review and not a proof assistant.
"""
import bisect
import json
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

sys.setrecursionlimit(30000)
HERE = Path(__file__).resolve().parent


def insert(t, key):
    if t is None:
        return (key, None, None)
    k, l, r = t
    return (k, insert(l, key), r) if key < k else (k, l, insert(r, key))


def expected_tree(r, d):
    t = None
    for key in range(r, 0, -1):
        t = (key, None, t)
    def scale(v):
        return None if v is None else (2*v[0], scale(v[1]), scale(v[2]))
    n = r
    for _ in range(d):
        t = scale(t)
        for key in list(range(1, 2*n+2, 2))+[2*n+2, 2*n+3]:
            t = insert(t, key)
        n = 2*n+3
    return t, n


def reflected(t, n):
    return None if t is None else (n+1-t[0], reflected(t[2], n), reflected(t[1], n))


def path(t, x):
    out = []
    while t:
        out.append(t)
        if t[0] == x:
            return out
        t = t[1] if x < t[0] else t[2]
    raise AssertionError('missing target')


def turn(t, parent, side):
    k, l, r = t
    if k != parent:
        return (k, turn(l, parent, side), r) if parent < k else (k, l, turn(r, parent, side))
    if side == 'L':
        a, b, c = r
        return (a, (k, l, b), c)
    a, b, c = l
    return (a, b, (k, c, r))


def label_set(t):
    result = set()
    def visit(v):
        if v is None:
            return None
        k, l, r = v
        a, b = visit(l), visit(r)
        lab = (a[0] if a else k, b[1] if b else k)
        result.add(lab)
        return lab
    visit(t)
    return result


def score(a, b):
    return -sum(hi-lo+1 >= 3 and not ((hi-lo+1) & (hi-lo+2)) for lo, hi in b-a)


def tupleize(x):
    return tuple(tupleize(v) for v in x) if isinstance(x, list) else x


def verify(file):
    w = json.loads(file.read_text(encoding='utf-8'))
    s = w['source']
    r, d, n = s['r'], s['d'], s['n']
    assert r == (1 << (s['p']+1))*(s['q']+1)+1 and r % 4 == 1
    assert n == (1 << d)*(r+3)-3 and s['prefix'] == []
    init, nn = expected_tree(r, d)
    assert nn == n
    if s['reflected']:
        init = reflected(init, n)
    assert tupleize(s['initial']) == init
    words = s['word']
    assert {x for _, flag, x in words if flag == 'K'} == set(range(1, n+1))
    trees = {'A': init, 'B': init}
    sets = {k: label_set(v) for k, v in trees.items()}
    initial_A = sets['A'].copy()
    a_changes = defaultdict(list)
    bb, bd = defaultdict(list), defaultdict(list)
    cursor = clock = 0
    saved = w['real_rotations']
    doubles, positive_A = [], defaultdict(list)
    astep_total = qtotal = ztotal = 0
    for op, (_, mode, target) in enumerate(words, 1):
        clock += 1
        assert w['rows'][op-1]['preB_initial'] == (trees['B'] == init)
        postA = None
        asteps = qsteps = zsteps = 0
        before_phi = score(sets['A'], sets['B'])
        for actor in ['A', 'B'] if mode == 'K' else ['A']:
            if actor == 'B':
                clock += 1
                postA = clock
                assert postA == w['rows'][op-1]['postA_clock']
                postA_phi = score(sets['A'], sets['B'])
            tr = path(trees[actor], target)
            depth = len(tr)-1
            if actor == 'A':
                asteps = (depth+1)//2
                astep_total += asteps
            else:
                qsteps, zsteps = depth//2, depth%2
                qtotal += qsteps
                ztotal += zsteps
            step = 0
            while len(tr) > 1:
                step += 1
                if len(tr) == 2:
                    typ, pivots, frame = 'ZIG', [target], None
                else:
                    g, pr, x = tr[-3:]
                    a = 'L' if g[1] is pr else 'R'
                    b = 'L' if pr[1] is x else 'R'
                    typ = a+b
                    pivots = [pr[0], target] if a == b else [target, target]
                    frame = max(label_set(g), key=lambda z: z[1]-z[0])
                changes = []
                for bit, pivot in enumerate(pivots):
                    clock += 1
                    e = saved[cursor]
                    identifier = [actor, op, step, bit]
                    assert e['id'] == identifier and e['clock'] == clock and e['type'] == typ
                    ptr = path(trees[actor], pivot)
                    pr = ptr[-2]
                    direction = 'R' if pr[1] is not None and pr[1][0] == pivot else 'L'
                    assert e['promoted'] == pivot and e['demoted'] == pr[0]
                    assert e['direction'] == ('RIGHT' if direction == 'R' else 'LEFT')
                    psi0 = len(sets['B']-sets['A'])
                    phi0 = score(sets['A'], sets['B'])
                    old = sets[actor]
                    trees[actor] = turn(trees[actor], pr[0], direction)
                    sets[actor] = label_set(trees[actor])
                    lost, born = old-sets[actor], sets[actor]-old
                    assert len(lost) == len(born) == 1
                    lost, born = next(iter(lost)), next(iter(born))
                    assert tuple(e['removed']) == lost and tuple(e['created']) == born
                    phi1 = score(sets['A'], sets['B'])
                    delta = len(sets['B']-sets['A'])-psi0
                    assert (phi0, phi1, phi1-phi0, delta) == (e['phi_before'], e['phi_after'], e['phi_delta'], e['psi_delta'])
                    changes.append(delta)
                    if actor == 'A':
                        assert abs(phi1-phi0) <= 1
                        a_changes[lost].append((clock, False))
                        a_changes[born].append((clock, True))
                        if bit == 0:
                            positive_A[op].append(identifier)
                    else:
                        assert lost[0] <= target <= lost[1] and not born[0] <= target <= born[1]
                        bb[born].append((clock, identifier))
                        bd[lost].append((clock, identifier))
                    cursor += 1
                if actor == 'B' and frame is not None:
                    doubles.append({'id': [op, step], 'frame': frame, 'type': typ,
                                    'neutral': changes == [0, 0], 'interior': frame[0] > 1 and frame[1] < n,
                                    'postA_clock': postA})
                tr = path(trees[actor], target)
        if mode != 'K':
            clock += 1
            postA = clock
            postA_phi = score(sets['A'], sets['B'])
        clock += 1
        row = w['rows'][op-1]
        assert (asteps, qsteps, zsteps) == (row['a'], row['q_B'], row['z_B'])
        assert (before_phi, postA_phi, score(sets['A'], sets['B']), clock) == (row['phi_start'], row['phi_postA'], row['phi_postB'], row['end_clock'])
        assert time.process_time()-START <= 240
    assert cursor == len(saved) and clock == w['period_clock']
    assert trees['A'] == trees['B'] == init
    period = clock
    records = {tuple(x['id']): x for x in w['all_B_double_records']}
    assert len(records) == len(doubles)
    all_u = set()
    for x in doubles:
        rec = records[tuple(x['id'])]
        for key in ('frame', 'type', 'neutral', 'interior', 'postA_clock'):
            assert tupleize(rec[key]) == tupleize(x[key])
        actual_u = False
        if x['neutral'] and x['interior']:
            lab, end = x['frame'], x['postA_clock']
            gamma, gid = max((t+lap*period, ident) for t, ident in bb[lab] for lap in (-1, 0) if t+lap*period < end)
            kap, kid = max((t+lap*period, ident) for t, ident in bd[lab] for lap in (-2, -1, 0) if t+lap*period < gamma)
            assert (gid, kid) == (rec['Gamma'], rec['kappa'])
            assert (gamma, kap) == (rec['Gamma_clock'], rec['kappa_clock'])
            changes = a_changes[lab]
            j = bisect.bisect_right([t for t, _ in changes], kap % period)-1
            present_at_kap = changes[j][1] if j >= 0 else lab in initial_A
            has_birth = any(flag and kap < t+lap*period <= end for t, flag in changes for lap in (-2, -1, 0))
            actual_u = not (present_at_kap or has_birth)
            assert actual_u == rec['full_Pi_A_absent']
        assert actual_u == rec['U_int']
        if actual_u:
            all_u.add(tuple(x['id']))
    keepops = [op for op, (_, mode, _) in enumerate(words, 1) if mode == 'K']
    by_event = {tuple(e['id']): e for e in saved}
    c = (1 << (d+1))-1
    resources = w['fixed_layer_birth_runs']
    expected_births = {tuple(e['id']) for e in saved if e['id'][0] == 'B' and e['created'][1]-e['created'][0]+1 == c}
    assert {tuple(x['birth']) for x in resources} == expected_births
    load = Counter()
    for resource in resources:
        e = by_event[tuple(resource['birth'])]
        assert e['created'] == resource['label']
        lab, birthop = tuple(e['created']), e['id'][1]
        deathclock, deathid = min((t+lap*period, ident) for t, ident in bd[lab] for lap in (0, 1) if t+lap*period > e['clock'])
        hit = deathid[1]
        endop = hit if deathclock < period else hit+len(words)
        first = next(op for op in range(birthop+1, endop+1)
                     if words[(op-1) % len(words)][1] == 'K' and lab[0] <= words[(op-1) % len(words)][2] <= lab[1])
        assert first == endop and hit == resource['first_hit']
        j = bisect.bisect_left(keepops, hit)-1
        previous = keepops[j]-(len(words) if j < 0 else 0)
        payment = next(positive_A[(op-1) % len(words)+1][0] for op in range(previous+1, hit+1) if positive_A[(op-1) % len(words)+1])
        assert resource['A_payment'] == payment and tuple(payment) in by_event
        load[tuple(payment)] += 1
    assert max(load.values(), default=0) <= 1
    birth_index = {tuple(z['birth']): z for z in resources}
    critical_ids, life_ids, seed_ids = set(), set(), set()
    for packet in w['packets']:
        p, q = packet['p'], packet['q']
        seed_count = (1 << (p-1))*(2*q+1)+1
        C = ((1 << p)-1)*(q+1)-p
        assert len(packet['seeds']) == seed_count and 3*C < 4*seed_count and 3*r < 8*seed_count
        row = w['rows'][packet['initial_KEEP']-1]
        assert row['preB_initial'] and packet['initial_KEEP'] in packet['critical_operations']
        nontrivial = [z['id'] for z in w['rows'] if z['q_B'] or z['z_B']]
        index = nontrivial.index(packet['initial_KEEP'])
        assert packet['critical_operations'] == nontrivial[index:index+p+1]
        physical = lambda k: n+1-(1 << d)*k if s['reflected'] else (1 << d)*k
        assert [words[z-1][2] for z in packet['critical_operations']] == [physical(r+1-(1 << j)) for j in range(p+1)]
        if (r-1) % (1 << (p+2)) == 0 and (r-1)//(1 << (p+2))-1 >= 1 and index+p+1 < len(nontrivial):
            assert words[nontrivial[index+p+1]-1][2] != physical(r+1-(1 << (p+1)))
        if packet['restoration_mode']:
            pattern = list(range(1, r+1))+list(range(r-1, 0, -1)) if packet['restoration_mode'] == 'I' else list(range(r, 0, -1))
            assert packet['restoration_operations'] == nontrivial[index+p+1:index+p+1+len(pattern)]
            assert [words[z-1][2] for z in packet['restoration_operations']] == [physical(k) for k in pattern]
        assert sum(w['rows'][op-1]['q_B'] for op in packet['critical_operations']) == r-q-2
        expected_crit = {z for z in all_u if z[0] in packet['critical_operations']}
        expected_life = {z for z in all_u if z[0] in packet['critical_operations']+packet['restoration_operations']}
        assert expected_crit == {tuple(z) for z in packet['critical_U_ids']} and len(expected_crit) <= C
        assert expected_life == {tuple(z) for z in packet['lifecycle_U_ids']}
        for ticket in packet['seeds']:
            bid = tuple(ticket['birth'])
            assert bid not in seed_ids and birth_index[bid] == ticket
            seed_ids.add(bid)
        critical_ids |= expected_crit
        life_ids |= expected_life
    if not s.get('helpers') and not s.get('altered_restore'):
        assert life_ids == all_u
    demand_load = Counter()
    assert {tuple(z['demand']) for z in w['critical_charge_map']} == critical_ids
    expected_map, already = [], set()
    for packet in sorted(w['packets'], key=lambda z:z['initial_KEEP']):
        seeds = sorted(packet['seeds'], key=lambda z:-z['birth'][2])
        assert seeds == packet['seeds']
        assigned = sorted([z for z in packet['critical_U_ids'] if tuple(z) not in already])
        for i, dem in enumerate(assigned):
            already.add(tuple(dem))
            ticket = seeds[i//2]
            expected_map.append({'demand':dem,'birth':ticket['birth'],'A_payment':ticket['A_payment']})
    assert expected_map == w['critical_charge_map']
    for z in w['critical_charge_map']:
        assert z['A_payment'] == birth_index[tuple(z['birth'])]['A_payment']
        demand_load[tuple(z['A_payment'])] += 1
    assert max(demand_load.values(), default=0) <= 2
    accounting = json.loads((HERE/'LIFECYCLE_MAPS.json').read_text(encoding='utf-8'))
    entry = next(z for z in accounting['sources'] if z['witness'] == file.name)
    assert {tuple(z['demand']) for z in entry['literal_lifecycle_U_charge_map']} == life_ids
    assert len(entry['literal_lifecycle_U_charge_map']) == len(life_ids)
    caps = {z['initial_KEEP']: z['finite_capacity'] for z in entry['packets']}
    original_packets = {z['initial_KEEP']: z for z in w['packets']}
    life_load, seed_load = Counter(), Counter()
    for item in entry['literal_lifecycle_U_charge_map']:
        dem, packetid, birth = tuple(item['demand']), item['packet'], tuple(item['birth'])
        choices = [p['initial_KEEP'] for p in w['packets'] if list(dem) in p['lifecycle_U_ids']]
        assert packetid == min(choices)
        assert birth in {tuple(z['birth']) for z in original_packets[packetid]['seeds']}
        assert item['A_payment'] == birth_index[birth]['A_payment']
        life_load[tuple(item['A_payment'])] += 1
        seed_load[(packetid, birth)] += 1
    assert all(count <= caps[packetid] for (packetid, _), count in seed_load.items())
    assert max(life_load.values(), default=0) <= max(caps.values(), default=0)
    assert max(life_load.values(), default=0) == entry['maximum_finite_A_load']
    expected_map, already = [], set()
    for packet in sorted(w['packets'], key=lambda z:z['initial_KEEP']):
        assigned = sorted([z for z in packet['lifecycle_U_ids'] if tuple(z) not in already])
        cap = (len(assigned)+len(packet['seeds'])-1)//len(packet['seeds'])
        assert caps[packet['initial_KEEP']] == cap
        for i, dem in enumerate(assigned):
            already.add(tuple(dem))
            ticket = packet['seeds'][i//cap]
            expected_map.append({'demand':dem,'packet':packet['initial_KEEP'],'birth':ticket['birth'],'A_payment':ticket['A_payment']})
    assert expected_map == entry['literal_lifecycle_U_charge_map']
    assert {tuple(z) for z in entry['literal_complement_U']} == all_u-life_ids
    assert all(e['created'][1]-e['created'][0]+1 >= c for e in saved if e['id'][0] == 'B' and words[e['id'][1]-1][0] != 'outer')
    assert (astep_total, qtotal, ztotal, len(all_u)) == tuple(w['result']['totals'][key] for key in ('a', 'q_B', 'z_B', 'U_int'))
    return {'file': file.name, 'n': n, 'r': r, 'd': d, 'operations': len(words),
            'rotations': cursor, 'A': astep_total, 'Q_B': qtotal, 'U_int': len(all_u),
            'critical_U': len(critical_ids), 'lifecycle_U': len(life_ids),
            'cyclic_Pi_independently_verified': True, 'exact_original_birth_to_A_injection': True,
            'complete_pair_closure': True, 'finite_lifecycle_map_verified': True,
            'literal_complement_U': sorted(all_u-life_ids), 'maximum_finite_lifecycle_A_load': max(life_load.values(), default=0)}


def main():
    results = [verify(file) for file in sorted(HERE.glob('*_complete_witness.json'))]
    out = {'passed': True, 'witnesses': results, 'cpu_seconds': time.process_time()-START,
           'total_operations': sum(x['operations'] for x in results),
           'total_real_rotations': sum(x['rotations'] for x in results),
           'limitations': 'Same-agent independent immutable code; not peer review or proof-assistant certification.'}
    if not (HERE/'FINAL_MANIFEST.json').exists():
        (HERE/'INDEPENDENT_VERIFICATION.json').write_text(json.dumps(out, indent=2), encoding='utf-8')
    print(json.dumps(out, indent=2))


START = time.process_time()
if __name__ == '__main__':
    main()
