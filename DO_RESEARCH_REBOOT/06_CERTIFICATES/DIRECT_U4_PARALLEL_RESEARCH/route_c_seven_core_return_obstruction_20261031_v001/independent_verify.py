"""Independent complete pointer table, reachable relation, and positive extension."""
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


def ck(ok, message):
    if not ok:
        raise AssertionError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(name, value):
    with (HERE / name).open('x', encoding='utf-8') as f:
        json.dump(value, f, indent=2, ensure_ascii=False)
        f.write('\n')


def main():
    tp = HERE / 'source_transition_table.json'
    gp = HERE / 'reachable_relation_certificate.json'
    xp = HERE / 'positive_extension_certificate.json'
    table = json.loads(tp.read_text(encoding='utf-8'))
    graph = json.loads(gp.read_text(encoding='utf-8'))
    extension = json.loads(xp.read_text(encoding='utf-8'))
    spec = importlib.util.spec_from_file_location('pointer_source', ROOT / 'python/liquidity/legacy_embedding.py')
    p = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(p)

    def raw(t):
        return None if t is None else [t[0], raw(t[1]), raw(t[2])]

    @lru_cache(None)
    def shapes(keys):
        if not keys:
            return (None,)
        out = []
        for i, key in enumerate(keys):
            for left in shapes(keys[:i]):
                for right in shapes(keys[i+1:]):
                    out.append((key, left, right))
        return tuple(out)

    cores = list(shapes(tuple(range(1, 8))))
    ids = {t: i for i, t in enumerate(cores)}
    ck([raw(t) for t in cores] == table['cores'] and len(cores) == len(ids) == 429, 'complete independently generated Catalan corpus')
    roots = Counter(t[0] for t in cores)
    ck([roots[r] for r in range(1, 8)] == [132, 42, 28, 25, 28, 42, 132] and
        sum(v*v for v in roots.values()) == 40569, 'proved same-root state bound')
    F = None
    for key in range(13, 7, -1):
        F = [key, None, F]

    def embed(t):
        return None if t is None else [t[0], embed(t[1]), F if t[0] == 7 else embed(t[2])]

    def project(t):
        if t is None:
            return None
        ck(1 <= t[0] <= 7, 'core projection never silently drops an active vertex')
        if t[0] == 7:
            ck(t[2] == F, 'complete outer fringe unchanged at core7.right')
            return (7, project(t[1]), None)
        return (t[0], project(t[1]), project(t[2]))

    def ptr(t):
        if t is None:
            return None
        z = p.mknode(t[0], ptr(t[1]), ptr(t[2]))
        for side in ('l', 'r'):
            if z[side] is not None:
                z[side]['p'] = z
        return z

    def unptr(t):
        return None if t is None else [t['k'], unptr(t['l']), unptr(t['r'])]

    def mirror(t):
        return None if t is None else [14-t[0], mirror(t[2]), mirror(t[1])]

    def inorder(t):
        return [] if t is None else inorder(t[1])+[t[0]]+inorder(t[2])

    def depth(t, key):
        d = 0
        while t is not None:
            if t[0] == key:
                return d
            t = t[1] if key < t[0] else t[2]
            d += 1
        raise AssertionError('present source key')

    def mev(events):
        cm = {'LL': 'RR', 'RR': 'LL', 'LR': 'RL', 'RL': 'LR', 'ZIG': 'ZIG'}
        om = {'L': 'R', 'R': 'L', '-': '-'}
        return [[cm[e[0]], 14-e[2], 14-e[1], om[e[3]]] for e in events]

    calls = trees = 0

    def access(t, key):
        nonlocal calls, trees
        ck(inorder(t) == list(range(1, 14)), 'strict input BST and all thirteen keys')
        trees += 1
        d = depth(t, key)
        dest, events = p.splay_trace(ptr(t), key)
        out = unptr(dest)
        ck(inorder(out) == list(range(1, 14)), 'strict output BST and all thirteen keys')
        trees += 1
        ev = [[e['case'], e['lo'], e['hi'], e['orient']] for e in events]
        q, z = sum(e[0] != 'ZIG' for e in ev), sum(e[0] == 'ZIG' for e in ev)
        ck((q, z, len(ev)) == (d//2, d%2, (d+1)//2), 'grouped A and B-double accounting')
        calls += 1
        return out, d, ev, q, z

    transitions = []
    for source_id, core in enumerate(cores):
        source = embed(core)
        for key in range(1, 8):
            dest, d, ev, q, z = access(source, key)
            mdest, md, me, mq, mz = access(mirror(source), 14-key)
            ck((mdest, md, me, mq, mz) == (mirror(dest), d, mev(ev), q, z), 'all reflected source table rows')
            target = ids[project(dest)]
            ck(dest == embed(cores[target]), 'exact thirteen-key embedding is source closed')
            row = dict(source=source_id, key=key, target=target, depth=d, a=len(ev), q=q, z=z,
                events=ev, mirror_key=14-key, mirror_events=me)
            ck(row == table['transitions'][7*source_id+key-1], 'every tuple/pointer core source transition')
            transitions.append(row)
    ck(calls == 6006, 'all3003 normal and3003 mirrored source cases')
    initial = None
    for key in range(13, 0, -1):
        initial = [key, None, initial]
    A = B = initial
    mA = mB = mirror(initial)
    prefix, mprefix = [], []
    for occurrence, (mode, key) in enumerate([('DELETE', 3), ('DELETE', 5), ('KEEP', 7)]):
        preA, preB, mpreA, mpreB = A, B, mA, mB
        A, da, ea, qa, za = access(A, key)
        mA, mda, mea, mqa, mza = access(mA, 14-key)
        if mode == 'KEEP':
            B, db, eb, q, z = access(B, key)
            mB, mdb, meb, mq, mz = access(mB, 14-key)
        else:
            db, eb, q, z = None, [], 0, 0
            mdb, meb, mq, mz = None, [], 0, 0
        row = dict(occurrence=occurrence, mode=mode, key=key, source_A=preA, source_B=preB,
            destination_A=A, destination_B=B, d_A=da, a=len(ea), A_events=ea, d_B=db, q=q, z=z, B_events=eb)
        mr = dict(occurrence=occurrence, mode=mode, key=14-key, source_A=mpreA, source_B=mpreB,
            destination_A=mA, destination_B=mB, d_A=mda, a=len(mea), A_events=mea,
            d_B=mdb, q=mq, z=mz, B_events=meb)
        ck(row == table['prefix_rows'][occurrence] and mr == table['mirrored_prefix_rows'][occurrence],
            'literal normal and mirrored two-reset seed')
        prefix.append(row)
        mprefix.append(mr)
    seed = (ids[project(A)], ids[project(B)])
    ck(list(seed) == graph['seed_pair_ids'] == table['seed_pair_ids'] and calls == 6014,
        'exact source seed binding')

    # Independent depth-first traversal; source producer used a breadth-first queue.
    reached = set()
    stack = [seed]
    while stack:
        a_id, b_id = pair = stack.pop()
        if pair in reached:
            continue
        reached.add(pair)
        ck(cores[a_id][0] == cores[b_id][0], 'common root invariant on complete relation')
        if a_id == b_id:
            continue
        root = cores[a_id][0]
        for key in range(7, 0, -1):
            if key != root:
                ar = transitions[7*a_id+key-1]
                br = transitions[7*b_id+key-1]
                stack.append((ar['target'], br['target']))
    pairs = [tuple(pair) for pair in graph['pair_ids']]
    ck(len(pairs) == len(set(pairs)) and set(pairs) == reached and pairs[0] == seed,
        'independent complete reachable relation, no missing or spurious state')
    ck(len(pairs) <= 40569 and graph['queue_exhausted'] and not graph['state_cap_used'], 'proved bound and no cutoff')
    positive = []
    edges = graph['outgoing_edges']
    max_delta = None
    for state_id, (a_id, b_id) in enumerate(pairs):
        root = cores[a_id][0]
        keys = [] if a_id == b_id else [key for key in range(1, 8) if key != root]
        ck([e[0] for e in edges[state_id]] == keys, 'complete source query choice at each nonabsorbed state')
        for key, target_id, delta in edges[state_id]:
            ar = transitions[7*a_id+key-1]
            br = transitions[7*b_id+key-1]
            ck(pairs[target_id] == (ar['target'], br['target']) and delta == br['q']-2*ar['a'],
                'each graph edge is exactly its two source splays')
            max_delta = delta if max_delta is None else max(max_delta, delta)
            if delta > 0:
                positive.append(dict(source=state_id, key=key, target=target_id, a=ar['a'], q=br['q'], delta=delta))
    ck(positive == graph['positive_edges'] and len(positive) == 324 and max_delta == graph['max_delta'] == 1,
        'all positive source counteredges, exact signs')
    predecessors = graph['predecessors']
    distances = [0]*len(pairs)
    ck(predecessors[0] == [-1, 0], 'seed predecessor')
    for state_id in range(1, len(pairs)):
        parent, key = predecessors[state_id]
        ck(0 <= parent < state_id and any(e[0] == key and e[1] == state_id for e in edges[parent]),
            'each listed state has a valid finite source path from seed')
        distances[state_id] = distances[parent]+1
    for state_id, row in enumerate(edges):
        for key, target_id, delta in row:
            ck(distances[target_id] <= distances[state_id]+1, 'predecessor distances are truly shortest')
    first = positive[0]
    ck(distances[first['source']]+1 == min(distances[e['source']]+1 for e in positive),
        'first positive extension has minimum source-word length')
    tail = [first['key']]
    cursor = first['source']
    while cursor:
        parent, key = predecessors[cursor]
        tail.append(key)
        cursor = parent
    tail.reverse()
    ck(tail == extension['KEEP_extension'] == [6, 5, 3, 7, 1, 4], 'exact shortest positive extension')

    total_excess = 1
    extra_rows, mextra_rows = [], []
    A_seed, B_seed = A, B
    for occurrence, key in enumerate(tail):
        preA, preB, mpreA, mpreB = A, B, mA, mB
        A, da, ea, qa, za = access(A, key)
        B, db, eb, q, z = access(B, key)
        mA, mda, mea, mqa, mza = access(mA, 14-key)
        mB, mdb, meb, mq, mz = access(mB, 14-key)
        delta = q-2*len(ea)
        row = dict(occurrence=occurrence, key=key, source_A=preA, source_B=preB,
            destination_A=A, destination_B=B, a=len(ea), q=q, A_events=ea, B_events=eb, delta=delta)
        ck(row == extension['replay'][occurrence], 'full actual pointer replay of selected amplification word')
        ck((mA, mda, mea, mqa, mza) == (mirror(A), da, mev(ea), qa, za) and
            (mB, mdb, meb, mq, mz) == (mirror(B), db, mev(eb), q, z), 'selected amplification reflected in actual source')
        total_excess += max(delta, 0)
        extra_rows.append(dict(row, d_A=da, d_B=db))
        mextra_rows.append(dict(occurrence=occurrence, key=14-key, source_A=mpreA, source_B=mpreB,
            destination_A=mA, destination_B=mB, a=len(mea), q=mq, A_events=mea, B_events=meb,
            delta=mq-2*len(mea), d_A=mda, d_B=mdb))
    ck(total_excess == extension['prefix_plus_tail_positive_excess'] == 2, 'two actual positive source units, not a maximum claim')
    ck(A != A_seed and B != B_seed and A != initial and B != initial, 'open extension is not a return identity')
    ck(not extension['closed_cycle_claimed'] and extension['G_B_cycle'] is None and extension['J_B_cycle'] is None,
        'no cyclic budget attached to an open word')
    ck(graph['outcome'] == 'NO_FURTHER_EXCESS_CLAIM_REFUTED' and graph['core_only_requested_identity'] == 'OPEN',
        'no false core-only impossibility or fringe activation requirement')
    ck(graph['source_table_sha256'] == sha(tp), 'source graph table binding')
    ck((len(pairs), sum(a == b for a, b in pairs), sum(len(row) for row in edges)) == (18450, 215, 109410),
        'complete exact reachable counts')
    ck(calls == 6038 and trees == 12076, 'complete pointer source and tree audit counts')
    save('verified_amplification_certificate.json', dict(status='PASS', initial_diagonal=initial,
        prefix_rows=prefix, KEEP_extension=tail, extension_rows=extra_rows,
        mirrored_initial_diagonal=mirror(initial), mirrored_prefix_rows=mprefix,
        mirrored_KEEP_extension=[14-key for key in tail], mirrored_extension_rows=mextra_rows,
        two_reset_A_costs=[1, 1], pure_reset_capacity=4, prefix_plus_extension_E=2,
        source_A_total=11, B_doubles_total=11, closed_pair=False,
        cycle_G_B=None, cycle_J_B=None, runtime_source_verified=True,
        cumulative_excess_on_other_graph_paths='NOT BOUNDED BY THIS EXAMPLE'))
    result = dict(status='PASS', date='2026-10-31', source_table_sha256=sha(tp), relation_sha256=sha(gp),
        positive_extension_sha256=sha(xp), core_shapes=429, source_table_rows=3003,
        proved_same_root_pair_bound=40569, reached_states=18450, non_diagonal_states=18235,
        absorbing_diagonal_states=215, complete_nontrivial_source_edges=109410,
        positive_edges=324, max_edge_delta=1, graph_complete=True, arbitrary_horizon_relation_verified=True,
        no_further_excess_claim='REFUTED—EXACT', shortest_positive_tail=tail, tail_length=6,
        prefix_plus_tail_E=2, pure_reset_capacity=4, actual_cycle_or_return='NOT ESTABLISHED',
        cycle_G_B=None, cycle_J_B=None, outer_fringe_activation_necessity='NOT PROVED',
        pointer_source_calls=calls, strict_BST_tree_occurrences=trees,
        larger_finite_fits=0, adaptive_source_classes=0, amplification_cycle_searches=0,
        matching_terminal_line='FROZEN', universal_CD='OPEN', automatic_successor_launched=False)
    save('independent_audit.json', result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
