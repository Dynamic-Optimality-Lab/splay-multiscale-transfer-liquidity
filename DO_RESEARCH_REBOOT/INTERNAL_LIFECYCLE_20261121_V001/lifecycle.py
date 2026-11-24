"""Complete original internal-renewal sources and physical birth-run accounting.

No old artifact is written. Mutable rotations are checked against the frozen
tuple splay after each access. Full Pi membership is reconstructed, not inferred
from a post-A neutral flag. This producer is not the universal proof.
"""
from __future__ import annotations
import bisect
import importlib.util
import json
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

sys.dont_write_bytecode = True
sys.setrecursionlimit(30000)
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
spec = importlib.util.spec_from_file_location("old_readonly_core", ROOT / "DO_RESEARCH_REBOOT/H3Q_ANALYSIS_20261120_V001/replay.py")
OLD = importlib.util.module_from_spec(spec)
spec.loader.exec_module(OLD)
REF = OLD.REF
START = time.process_time()
TOTAL_ROTATIONS = 0


def vine(n):
    t = None
    for k in range(n, 0, -1):
        t = (k, None, t)
    return t


def decorate(t, n):
    """E: old nodes doubled; every null gap filled with its full new subtree."""
    def rec(v, lo, hi):
        if v is None:
            assert hi == lo + 1
            if lo == n:
                return (2*n+1, None, (2*n+2, None, (2*n+3, None, None)))
            return (2*hi-1, None, None)
        k, left, right = v
        return (2*k, rec(left, lo, k), rec(right, k, hi))
    return rec(t, 0, n+1)


def initial(r, d):
    t, n = vine(r), r
    for _ in range(d):
        t = decorate(t, n)
        n = 2*n + 3
    return t, n


def mirror(t, n):
    return None if t is None else (n+1-t[0], mirror(t[2], n), mirror(t[1], n))


def builder(r, d):
    """Actual KEEP word from the full physical right vine to E^d(vine_r)."""
    if d == 0:
        return []
    n = (1 << (d-1)) * (r+3) - 3
    out = [2*n+1]
    for k in range(1, n+1):
        out.extend(range(2*k, 1, -2))
    out.extend(2*x for x in builder(r, d-1))
    return out


def source(p, q, d, m, mode="I", reflected=False, helpers=False):
    r = (1 << (p+1))*(q+1)+1
    assert r % 4 == 1 and d >= 1 and m >= 2 and mode in ("I", "J")
    t, n = initial(r, d)
    scale = 1 << d
    kept = {r+1-(1 << j) for j in range(p+1)}
    inner = [("prep", "D", x) for x in range(2, r+1)]
    inner += [("critical", "K" if x in kept else "D", x) for x in range(r, 0, -1)]
    if mode == "I":
        inner += [("restore_up", "K", x) for x in range(1, r+1)]
        inner += [("restore_down", "K", x) for x in range(r-1, 0, -1)]
    else:
        inner += [("restore_prep", "D", x) for x in range(2, r+1)]
        inner += [("restore_down", "K", x) for x in range(r, 0, -1)]
    assert len(inner) == 4*r-2
    word = []
    for copy in range(1, m+1):
        for phase, flag, x in inner:
            word.append((f"{mode}{copy}:{phase}", flag, scale*x))
            if helpers and phase == 'critical' and flag == 'K':
                word.extend([(f"{mode}{copy}:helper", 'D', 1),
                             (f"{mode}{copy}:helper", 'D', n)])
    outer = list(range(1, n+1)) + list(range(n-1, 0, -1)) + builder(r, d)
    word += [("outer", "K", x) for x in outer]
    if reflected:
        t = mirror(t, n)
        word = [(phase, flag, n+1-x) for phase, flag, x in word]
    return {"p": p, "q": q, "d": d, "m": m, "mode": mode, "reflected": reflected, "helpers": helpers,
            "r": r, "n": n, "initial": t, "prefix": [], "word": word}


class Tree(OLD.Tree):
    def __init__(self, t, n):
        super().__init__(n)
        self.labels.clear()
        self.left = [0]*(n+1)
        self.right = [0]*(n+1)
        self.parent = [0]*(n+1)
        def visit(v, parent):
            if v is None:
                return 0
            k, left, right = v
            self.parent[k] = parent
            self.left[k] = visit(left, k)
            self.right[k] = visit(right, k)
            self.update(k)
            self.labels.add((self.lo[k], self.hi[k]))
            return k
        self.root = visit(t, 0)
        self.validate()


def frozen(t):
    return REF.LEAF if t is None else REF.node(t[0], frozen(t[1]), frozen(t[2]))


def mersenne(lab):
    c = lab[1]-lab[0]+1
    return c >= 3 and not (c & (c+1))


def overlaps(runs, kap, end, period):
    return any(start+shift*period <= end and stop+shift*period > kap
               for start, stop in runs for shift in (-2, -1, 0, 1, 2))


def run(s, save=False):
    global TOTAL_ROTATIONS
    assert not (HERE / "FINAL_MANIFEST.json").exists(), "Sealed run: use a new directory"
    n, r, d = s['n'], s['r'], s['d']
    A, B = Tree(s['initial'], n), Tree(s['initial'], n)
    init = A.tuple()
    refs = {"A": init, "B": init}
    events, rows, demands = [], [], []
    births, deaths = defaultdict(list), defaultdict(list)
    presence = {lab: 0 for lab in A.labels}
    runs = defaultdict(list)
    clock = 0
    phi = 0

    def primitive(actor, tree, x, op, step, bit, typ, target):
        nonlocal clock, phi
        global TOTAL_ROTATIONS
        clock += 1
        fixed = B if actor == 'A' else A
        old = (tree.lo[x], tree.hi[x])
        old_match = old in fixed.labels
        demoted, grand, direction, removed, created = tree.rotate(x)
        new_match = created in fixed.labels
        if actor == 'A':
            psi_delta = int(old_match)-int(new_match)
            delta = int(mersenne(created) and new_match)-int(mersenne(removed) and old_match)
            assert -1 <= delta <= 1
            runs[removed].append((presence.pop(removed), clock))
            presence[created] = clock
        else:
            psi_delta = int(not new_match)-int(not old_match)
            delta = int(mersenne(removed) and not old_match)-int(mersenne(created) and not new_match)
            assert psi_delta in (-1, 0)
            assert removed[0] <= target <= removed[1]
            assert not created[0] <= target <= created[1]
        e = {'id': [actor, op, step, bit], 'clock': clock, 'type': typ, 'target': target,
             'promoted': x, 'demoted': demoted, 'external': grand, 'direction': direction,
             'removed': removed, 'created': created, 'psi_delta': psi_delta,
             'phi_before': phi, 'phi_delta': delta, 'phi_after': phi+delta}
        phi += delta
        if actor == 'B':
            births[created].append((clock, len(events)))
            deaths[removed].append((clock, len(events)))
        events.append(e)
        TOTAL_ROTATIONS += 1
        assert TOTAL_ROTATIONS <= 200000 and time.process_time()-START <= 240
        return e

    def splay(actor, tree, target, op, postA):
        step = 0
        while tree.parent[target]:
            step += 1
            pr = tree.parent[target]
            gp = tree.parent[pr]
            if not gp:
                primitive(actor, tree, target, op, step, 0, 'ZIG', target)
            else:
                frame = (tree.lo[gp], tree.hi[gp])
                a = 'L' if tree.left[gp] == pr else 'R'
                b = 'L' if tree.left[pr] == target else 'R'
                typ = a+b
                e0 = primitive(actor, tree, pr if a == b else target, op, step, 0, typ, target)
                e1 = primitive(actor, tree, target, op, step, 1, typ, target)
                if actor == 'B':
                    demands.append({'id': [op, step], 'type': typ, 'frame': frame,
                                    'neutral': e0['psi_delta'] == e1['psi_delta'] == 0,
                                    'interior': frame[0] > 1 and frame[1] < n, 'postA_clock': postA})
        return step

    for op, (phase, mode, target) in enumerate(s['word'], 1):
        clock += 1
        phi0 = phi
        preB_initial = B.tuple() == init
        before = len(events)
        adepth = A.depth(target)
        astep = splay('A', A, target, op, None)
        refs['A'], fr = REF.trace(refs['A'], target)
        assert refs['A'] == A.tuple() and astep == len(fr) == (adepth+1)//2
        clock += 1
        postA = clock
        phia = phi
        mid = len(events)
        bdepth = B.depth(target) if mode == 'K' else 0
        if mode == 'K':
            bstep = splay('B', B, target, op, postA)
            refs['B'], fr = REF.trace(refs['B'], target)
            assert refs['B'] == B.tuple() and bstep == len(fr) == (bdepth+1)//2
        clock += 1
        row = {'id': op, 'phase': phase, 'mode': mode, 'target': target,
               'a': astep, 'a_depth': adepth, 'q_B': bdepth//2, 'z_B': bdepth%2,
               'preB_initial': preB_initial, 'postA_clock': postA, 'end_clock': clock,
               'phi_start': phi0, 'phi_postA': phia, 'phi_postB': phi,
               'A_phi_delta': phia-phi0, 'B_phi_delta': phi-phia,
               'A_rotations': mid-before, 'B_rotations': len(events)-mid}
        rows.append(row)
        if not s.get('helpers') and not s.get('altered_restore') and phase != 'outer' and (op % (4*r-2)) == 0:
            assert A.tuple() == B.tuple() == init
        if mode == 'K':
            assert phi == -sum(mersenne(lab) for lab in B.labels-A.labels)
    assert A.tuple() == B.tuple() == init and phi == 0
    for lab, begin in presence.items():
        runs[lab].append((begin, clock+1))
    # The period ends just before next period's first pre-A marker.
    period = clock
    for lab in presence:
        runs[lab][-1] = (runs[lab][-1][0], period)
    for demand in demands:
        demand['U_int'] = False
        if not demand['neutral'] or not demand['interior']:
            continue
        lab, end = tuple(demand['frame']), demand['postA_clock']
        bc = [a for a, _ in births[lab]]
        dc = [a for a, _ in deaths[lab]]
        assert bc and dc
        j = bisect.bisect_left(bc, end)-1
        gamma, ge = births[lab][j]
        glap = 0 if j >= 0 else -1
        gamma += glap*period
        k = bisect.bisect_left(dc, gamma % period)-1
        kap, ke = deaths[lab][k]
        klap = glap + (0 if k >= 0 else -1)
        kap += klap*period
        assert kap < gamma < end
        absent = not overlaps(runs[lab], kap, end, period)
        demand.update(Gamma=events[ge]['id'], Gamma_lap=glap,
                      kappa=events[ke]['id'], kappa_lap=klap,
                      kappa_clock=kap, Gamma_clock=gamma, full_Pi_A_absent=absent, U_int=absent)

    # Actual next nontrivial B targets, independent of author-supplied phase names.
    keep = [row for row in rows if row['mode'] == 'K']
    nontriv = [row for row in keep if row['q_B'] or row['z_B']]
    keepops = [row['id'] for row in keep]
    keep_by_key = defaultdict(list)
    for row in keep:
        keep_by_key[row['target']].append(row['id'])
    def payment(hit):
        j = bisect.bisect_left(keepops, hit)-1
        previous = keepops[j]
        if j < 0:
            previous -= len(rows)
        for unwrapped in range(previous+1, hit+1):
            actual = (unwrapped-1) % len(rows)+1
            if rows[actual-1]['a']:
                return ['A', actual, 1, 0]
        raise AssertionError('Nontrivial B KEEP has no real A gap work')
    def retire(event):
        lo, hi = event['created']
        op = event['id'][1]
        candidates = []
        for key in range(lo, hi+1):
            a = keep_by_key[key]
            if a:
                j = bisect.bisect_right(a, op)
                candidates.append(a[j] if j < len(a) else a[0]+len(rows))
        assert candidates
        hit_unwrapped = min(candidates)
        hit = (hit_unwrapped-1) % len(rows)+1
        dies = deaths[tuple(event['created'])]
        j = bisect.bisect_right([c for c, _ in dies], event['clock'])
        death = events[dies[j if j < len(dies) else 0][1]]
        assert death['id'][1] == hit
        return hit, payment(hit)
    c = (1 << (d+1))-1
    layer_births = []
    layer_load = Counter()
    for event in events:
        if event['id'][0] == 'B' and event['created'][1]-event['created'][0]+1 == c:
            hit, pay = retire(event)
            layer_births.append({'birth': event['id'], 'label': event['created'], 'first_hit': hit, 'A_payment': pay})
            layer_load[tuple(pay)] += 1
    assert max(layer_load.values(), default=0) <= 1
    lookup = {tuple(e['id']): e for e in events}
    packets = []
    scale = 1 << d
    physical = lambda key: n+1-scale*key if s['reflected'] else scale*key
    for index, row in enumerate(nontriv):
        if not row['preB_initial'] or row['target'] != physical(r):
            continue
        pmax = 0
        for j in range(1, r.bit_length()):
            if (r-1) % (1 << (j+1)) or (r-1)//(1 << (j+1))-1 < 1:
                break
            if index+j >= len(nontriv) or nontriv[index+j]['target'] != physical(r+1-(1 << j)):
                break
            pmax = j
        if not pmax:
            continue
        p = pmax
        q = (r-1)//(1 << (p+1))-1
        critops = [z['id'] for z in nontriv[index:index+p+1]]
        seedlist = []
        xp = r+1-(1 << p)
        for g in range(1, xp, 2):
            eid = ('B', row['id'], (r-g)//2, 0)
            e = lookup[eid]
            lo, hi = scale*(g-1)+1, scale*(g+1)-1
            lab = (n+1-hi, n+1-lo) if s['reflected'] else (lo, hi)
            assert tuple(e['created']) == lab and hi-lo+1 == c
            hit, pay = retire(e)
            assert all(not lab[0] <= rows[z-1]['target'] <= lab[1] for z in critops)
            seedlist.append({'birth': list(eid), 'label': lab, 'first_hit': hit, 'A_payment': pay})
        seeds = (1 << (p-1))*(2*q+1)+1
        critical_bound = ((1 << p)-1)*(q+1)-p
        assert len(seedlist) == seeds and 3*critical_bound < 4*seeds and 3*r < 8*seeds
        dcrit = [x['id'] for x in demands if x['U_int'] and x['id'][0] in critops]
        assert len(dcrit) <= critical_bound
        assert sum(rows[z-1]['q_B'] for z in critops) == r-q-2
        after = index+p+1
        candidates = [('I', list(range(1, r+1))+list(range(r-1, 0, -1))), ('J', list(range(r, 0, -1)))]
        restore = []
        cert = None
        for name, pattern in candidates:
            seq = nontriv[after:after+len(pattern)]
            if len(seq) == len(pattern) and [x['target'] for x in seq] == [physical(k) for k in pattern]:
                cert, restore = name, [x['id'] for x in seq]
                break
        dlife = [x['id'] for x in demands if x['U_int'] and x['id'][0] in critops+restore]
        qrestore = sum(rows[z-1]['q_B'] for z in restore)
        packets.append({'initial_KEEP': row['id'], 'p': p, 'q': q, 'seeds': seedlist,
                        'critical_operations': critops, 'critical_bound': critical_bound,
                        'critical_U_ids': dcrit, 'restoration_mode': cert,
                        'restoration_operations': restore, 'restoration_Q': qrestore,
                        'lifecycle_U_ids': dlife})
    assert len(packets) == s['m']
    # Capacity two for critical U, assigned only once using literal original IDs.
    owner = {}
    critical_map = []
    critical_load = Counter()
    for packet in sorted(packets, key=lambda x: x['initial_KEEP']):
        for i, demand in enumerate(z for z in packet['critical_U_ids'] if tuple(z) not in owner):
            ticket = packet['seeds'][i//2]
            owner[tuple(demand)] = packet['initial_KEEP']
            critical_map.append({'demand': demand, 'birth': ticket['birth'], 'A_payment': ticket['A_payment']})
            critical_load[tuple(ticket['A_payment'])] += 1
    assert max(critical_load.values(), default=0) <= 2
    covered = {tuple(z) for packet in packets for z in packet['lifecycle_U_ids']}
    all_u = {tuple(z['id']) for z in demands if z['U_int']}
    if not s.get('helpers') and not s.get('altered_restore'):
        assert covered == all_u
    for copy in range(1, s['m']+1):
        a = sum(row['a'] for row in rows if row['phase'].startswith(f"{s['mode']}{copy}:"))
        if not s.get('helpers') and not s.get('altered_restore'):
            assert a == 4*(r-1)
    life_owner, life_map, life_load = {}, [], Counter()
    for packet in sorted(packets, key=lambda x: x['initial_KEEP']):
        eligible = [z for z in packet['lifecycle_U_ids'] if tuple(z) not in life_owner]
        capacity = (len(eligible)+len(packet['seeds'])-1)//len(packet['seeds'])
        packet['finite_lifecycle_capacity'] = capacity
        for i, demand in enumerate(eligible):
            ticket = packet['seeds'][i//capacity]
            life_owner[tuple(demand)] = packet['initial_KEEP']
            life_map.append({'demand': demand, 'birth': ticket['birth'], 'A_payment': ticket['A_payment']})
            life_load[tuple(ticket['A_payment'])] += 1
    inner_births = [e for e in events if e['id'][0] == 'B' and rows[e['id'][1]-1]['phase'] != 'outer']
    assert all(e['created'][1]-e['created'][0]+1 >= c for e in inner_births)
    if not s.get('helpers') and not s.get('altered_restore'):
        assert not any(z['U_int'] for z in demands if rows[z['id'][0]-1]['phase'] == 'outer')
    totals = {key: sum(row[key] for row in rows) for key in ['a', 'q_B', 'z_B', 'A_rotations', 'B_rotations']}
    totals.update(U_int=len(all_u), critical_U=len(owner), lifecycle_U=len(covered), literal_complement_U=len(all_u-covered), c=c, packets=len(packets),
                  seed_births=sum(len(x['seeds']) for x in packets), fixed_layer_births=len(layer_births),
                  max_critical_A_load=max(critical_load.values(), default=0),
                  max_finite_lifecycle_A_load=max(life_load.values(), default=0),
                  min_inner_birth_size=min((e['created'][1]-e['created'][0]+1 for e in inner_births), default=0),
                  inner_leaf_births=0, operations=len(rows), real_rotations=len(events))
    probes = []
    if s['mode'] == 'I' and not s.get('helpers'):
        for copy in range(1, s['m']+1):
            op = (copy-1)*(4*r-2)+2*r+2
            row = rows[op-1]
            k = bisect.bisect_left(keepops, op)-1
            g = sum(rows[t-1]['a'] for t in range(keepops[k]+1, op+1))
            probes.append({'operation': op, 'target': row['target'], 'B_phi_delta': row['B_phi_delta'],
                           'A_gap': g, 'a': row['a'], 'u': sum(x['U_int'] for x in demands if x['id'][0] == op),
                           'B_decreases': -sum(e['psi_delta'] for e in events if e['id'][0] == 'B' and e['id'][1] == op),
                           'nontrivial_KEEP': 1})
    name = f"{s['mode']}_p{s['p']}_q{s['q']}_d{d}_m{s['m']}"+('_mirror' if s['reflected'] else '')+('_helpers' if s.get('helpers') else '')+('_altered_restore' if s.get('altered_restore') else '')
    result = {'name': name, 'parameters': {k: v for k, v in s.items() if k not in ('word', 'initial')},
              'totals': totals, 'packets': packets, 'potential_probes': probes,
              'full_pair_closure': True, 'full_original_Pi_audited': True,
              'fixed_layer_global_injection_verified': True}
    if save:
        witness = {'source': s, 'rows': rows, 'real_rotations': events,
                   'all_B_double_records': demands, 'packets': packets,
                   'critical_charge_map': critical_map, 'fixed_layer_birth_runs': layer_births,
                   'lifecycle_charge_map': life_map,
                   'result': result, 'period_clock': period}
        (HERE/(name+'_complete_witness.json')).write_text(json.dumps(witness, separators=(',', ':')), encoding='utf-8')
    print(json.dumps({'name': name, **totals, 'probes': probes}), flush=True)
    return result


def main():
    # Deliberately bounded: full sources, repeated copies, depth, alternative
    # restoration, reflection, large-support Mersenne recharge.
    cases = [(1,1,1,3,'I',False), (1,1,1,3,'J',False),
             (1,1,2,3,'I',False), (1,1,2,3,'J',False),
             (1,1,3,2,'J',False), (1,1,2,2,'J',True),
             (3,1,1,2,'J',False), (2,5,1,2,'I',False),
             (3,5,1,2,'I',False), (2,5,1,2,'J',False)]
    results = [run(source(*case), save=True) for case in cases]
    out = {'passed': True, 'sources': results, 'cpu_seconds': time.process_time()-START,
           'real_rotations': TOTAL_ROTATIONS,
           'scope':'Finite original-event audit; symbolic proof is in linked Notion manuscript.'}
    (HERE/'COMPLETE_SOURCE_AUDIT.json').write_text(json.dumps(out, indent=2), encoding='utf-8')
    print(json.dumps({'passed': True, 'sources': len(results), 'rotations': TOTAL_ROTATIONS, 'cpu_seconds': out['cpu_seconds']}))


if __name__ == '__main__':
    main()
