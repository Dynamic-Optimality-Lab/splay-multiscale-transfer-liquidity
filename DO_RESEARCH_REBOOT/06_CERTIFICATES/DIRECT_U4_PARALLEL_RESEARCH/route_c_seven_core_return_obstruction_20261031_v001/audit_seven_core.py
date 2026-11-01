"""Complete seven-core source table and every reachable post-prefix KEEP pair."""
import hashlib
import importlib.util
import json
import subprocess
import sys
from collections import Counter
from functools import lru_cache
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OLD = HERE.parent / 'route_c_recurrent_excess_gate_audit_20261031_v001'
STAGE = ROOT / 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'
PAIR_BOUND = 40569


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(name, value):
    with (HERE / name).open('x', encoding='utf-8') as f:
        json.dump(value, f, indent=2, ensure_ascii=False)
        f.write('\n')


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def main():
    inherited = json.loads((OLD / 'entry_source_pins.json').read_text(encoding='utf-8'))
    pins = dict(inherited['files'])
    for rel, h in pins.items():
        assert sha(ROOT / rel) == h, rel
    for p in HERE.parent.rglob('*'):
        if p.is_file() and HERE not in p.parents:
            pins[p.relative_to(ROOT).as_posix()] = sha(p)
    stage = {p.relative_to(STAGE).as_posix(): sha(p) for p in STAGE.rglob('*') if p.is_file()}
    assert stage == inherited['stage_files'] and len(stage) == 125
    assert not git('status', '--porcelain=v1', '--untracked-files=no')
    assert (git('rev-parse', 'HEAD'), git('branch', '--show-current')) == (inherited['head'], inherited['branch'])
    save('entry_source_pins.json', dict(date='2026-10-31', head=inherited['head'], branch=inherited['branch'],
        tracked_status='', files=pins, stage_files=stage, inherited_pins=len(inherited['files']),
        gate_sha256=sha(HERE / 'KC00_FOUR_RULE_GATE.md')))
    spec = importlib.util.spec_from_file_location('tuple_source', ROOT / 'python/independent/splay.py')
    s = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(s)
    L = s.LEAF
    calls = 0

    def raw(t):
        return None if t == L else [t[1], raw(t[2]), raw(t[3])]

    def mirror(t):
        return L if t == L else s.node(14-t[1], mirror(t[3]), mirror(t[2]))

    def mirror_events(events):
        cm = {'LL': 'RR', 'RR': 'LL', 'LR': 'RL', 'RL': 'LR', 'ZIG': 'ZIG'}
        om = {'L': 'R', 'R': 'L', '-': '-'}
        return [[cm[e[0]], 14-e[2], 14-e[1], om[e[3]]] for e in events]

    def access(t, key):
        nonlocal calls
        assert s.inorder(t) == list(range(1, 14))
        found, d = s.lookup(t, key)
        assert found
        dest, ev = s.trace(t, key)
        q, z = sum(e[0] != 'ZIG' for e in ev), sum(e[0] == 'ZIG' for e in ev)
        assert (q, z, len(ev)) == (d//2, d%2, (d+1)//2)
        assert s.inorder(dest) == list(range(1, 14))
        calls += 1
        return dest, d, ev, q, z

    @lru_cache(None)
    def all_trees(lo, hi):
        if lo > hi:
            return (L,)
        return tuple(s.node(root, left, right) for root in range(lo, hi+1)
            for left in all_trees(lo, root-1) for right in all_trees(root+1, hi))

    cores = list(all_trees(1, 7))
    core_ids = {t: i for i, t in enumerate(cores)}
    assert len(cores) == len(core_ids) == 429
    roots = Counter(t[1] for t in cores)
    assert [roots[r] for r in range(1, 8)] == [132, 42, 28, 25, 28, 42, 132]
    assert sum(v*v for v in roots.values()) == PAIR_BOUND
    F = L
    for key in range(13, 7, -1):
        F = s.node(key, L, F)

    def embed(t):
        if t == L:
            return L
        return s.node(t[1], embed(t[2]), F if t[1] == 7 else embed(t[3]))

    def project(t):
        if t == L:
            return L
        assert 1 <= t[1] <= 7
        if t[1] == 7:
            assert t[3] == F, 'entire upper fringe preserved at core7.right'
            return s.node(7, project(t[2]), L)
        return s.node(t[1], project(t[2]), project(t[3]))

    transitions = []
    for tree_id, core in enumerate(cores):
        source = embed(core)
        for key in range(1, 8):
            dest, d, ev, q, z = access(source, key)
            mdest, md, mev, mq, mz = access(mirror(source), 14-key)
            assert mdest == mirror(dest) and (md, mq, mz) == (d, q, z)
            assert [list(e) for e in mev] == mirror_events(ev)
            target = core_ids[project(dest)]
            assert dest == embed(cores[target])
            transitions.append(dict(source=tree_id, key=key, target=target, depth=d,
                a=len(ev), q=q, z=z, events=ev, mirror_key=14-key, mirror_events=mev))
    assert len(transitions) == 3003 and calls == 6006

    initial = s.vine(13)
    A = B = initial
    mA = mB = mirror(initial)
    prefix_rows, mirrored_prefix = [], []
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
        row = dict(occurrence=occurrence, mode=mode, key=key, source_A=raw(preA), source_B=raw(preB),
            destination_A=raw(A), destination_B=raw(B), d_A=da, a=len(ea), A_events=ea,
            d_B=db, q=q, z=z, B_events=eb)
        mr = dict(occurrence=occurrence, mode=mode, key=14-key, source_A=raw(mpreA), source_B=raw(mpreB),
            destination_A=raw(mA), destination_B=raw(mB), d_A=mda, a=len(mea), A_events=mea,
            d_B=mdb, q=mq, z=mz, B_events=meb)
        assert mA == mirror(A) and mB == mirror(B) and mda == da and (mq, mz) == (q, z)
        assert [list(e) for e in mea] == mirror_events(ea) and [list(e) for e in meb] == mirror_events(eb)
        prefix_rows.append(row)
        mirrored_prefix.append(mr)
    assert calls == 6014 and [r['a'] for r in prefix_rows] == [1, 1, 1]
    assert prefix_rows[-1]['q'] == 3
    seed = (core_ids[project(A)], core_ids[project(B)])
    assert cores[seed[0]][1] == cores[seed[1]][1] == 7
    save('source_transition_table.json', dict(schema='complete-seven-core-source-table-v1', date='2026-10-31',
        core_keys=list(range(1, 8)), fixed_embedding_keys=list(range(1, 14)), fringe=raw(F),
        cores=[raw(t) for t in cores], roots_by_rank=[roots[r] for r in range(1, 8)],
        same_root_pair_bound=PAIR_BOUND, transitions=transitions,
        prefix_rows=prefix_rows, mirrored_prefix_rows=mirrored_prefix,
        seed_pair_ids=list(seed), tuple_source_calls=calls, table_rows=3003,
        all_core_source_contexts=True, outer_fringe_preserved=True))

    pair_ids = [seed]
    where = {seed: 0}
    predecessors = [[-1, 0]]
    edges = []
    positive_edges = []
    at = 0
    max_delta = None
    while at < len(pair_ids):
        aid, bid = pair_ids[at]
        root = cores[aid][1]
        assert cores[bid][1] == root
        row_edges = []
        if aid != bid:
            for key in range(1, 8):
                if key == root:
                    continue
                ar = transitions[7*aid+key-1]
                br = transitions[7*bid+key-1]
                delta = br['q']-2*ar['a']
                assert ar['a'] >= 1
                target_pair = (ar['target'], br['target'])
                if target_pair not in where:
                    where[target_pair] = len(pair_ids)
                    pair_ids.append(target_pair)
                    predecessors.append([at, key])
                    assert len(pair_ids) <= PAIR_BOUND
                target = where[target_pair]
                row_edges.append([key, target, delta])
                max_delta = delta if max_delta is None else max(max_delta, delta)
                if delta > 0:
                    positive_edges.append(dict(source=at, key=key, target=target, a=ar['a'], q=br['q'], delta=delta))
        edges.append(row_edges)
        at += 1
    assert at == len(pair_ids) == len(edges) == len(predecessors)
    diagonal_count = sum(a == b for a, b in pair_ids)
    edge_count = sum(len(v) for v in edges)
    assert edge_count == 6*(len(pair_ids)-diagonal_count)
    outcome = 'NO_FURTHER_CORE_EXCESS_PROVED' if not positive_edges else 'NO_FURTHER_EXCESS_CLAIM_REFUTED'
    if positive_edges:
        edge = positive_edges[0]
        keys = [edge['key']]
        cursor = edge['source']
        while cursor != 0:
            parent, key = predecessors[cursor]
            keys.append(key)
            cursor = parent
        keys.reverse()
        pa, pb = seed
        replay = []
        total = 1
        for i, key in enumerate(keys):
            ar = transitions[7*pa+key-1]
            br = transitions[7*pb+key-1]
            delta = br['q']-2*ar['a']
            replay.append(dict(occurrence=i, key=key, source_A=raw(embed(cores[pa])),
                source_B=raw(embed(cores[pb])), destination_A=raw(embed(cores[ar['target']])),
                destination_B=raw(embed(cores[br['target']])), a=ar['a'], q=br['q'],
                A_events=ar['events'], B_events=br['events'], delta=delta))
            total += max(delta, 0)
            pa, pb = ar['target'], br['target']
        save('positive_extension_certificate.json', dict(KEEP_extension=keys, replay=replay,
            prefix_plus_tail_positive_excess=total, closed_cycle_claimed=False,
            G_B_cycle=None, J_B_cycle=None, requested_identity='OPEN'))
    save('reachable_relation_certificate.json', dict(schema='all-core-KEEP-reachable-pairs-v1', date='2026-10-31',
        source_table_sha256=sha(HERE / 'source_transition_table.json'), seed_pair_ids=list(seed),
        pair_ids=pair_ids, predecessors=predecessors, outgoing_edges=edges,
        states=len(pair_ids), non_diagonal_states=len(pair_ids)-diagonal_count,
        absorbing_diagonal_states=diagonal_count, edges=edge_count, proved_pair_bound=PAIR_BOUND,
        queue_exhausted=True, state_cap_used=False, max_delta=max_delta, positive_edges=positive_edges,
        outcome=outcome, root_noops='omitted exact zero-cost self-loops',
        diagonal_absorption='all future common KEEPs are equal-tree and nonpositive',
        prefix_positive_excess=1, prefix_pure_capacity=4,
        core_only_return_E_upper_bound=1 if not positive_edges else None,
        core_only_requested_identity='EXCLUDED' if not positive_edges else 'OPEN',
        outer_fringe_queries_before_synchronization='NOT CLASSIFIED',
        cycle_G_B=None, cycle_J_B=None, new_finite_key_sizes=0, finite_fits=0,
        matching_terminal_line='FROZEN', universal_CD='OPEN', automatic_successor_launched=False))
    print(json.dumps(dict(outcome=outcome, core_trees=429, transition_rows=3003, source_calls=calls,
        reachable_states=len(pair_ids), non_diagonal_states=len(pair_ids)-diagonal_count,
        absorbing_diagonal_states=diagonal_count, edges=edge_count, max_delta=max_delta,
        positive_edges=len(positive_edges), preserved_files=len(pins), stage_11G_files=len(stage)), indent=2))


if __name__ == '__main__':
    main()
