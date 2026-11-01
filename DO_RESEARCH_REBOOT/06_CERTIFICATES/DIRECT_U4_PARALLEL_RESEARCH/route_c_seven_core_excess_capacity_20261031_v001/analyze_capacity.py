"""Exact SCC/longest-path excess capacity on the pinned source relation."""
import hashlib
import json
import subprocess
import sys
from collections import Counter, deque
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OLD = HERE.parent / 'route_c_seven_core_return_obstruction_20261031_v001'
STAGE = ROOT / 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'


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
        gate_sha256=sha(HERE / 'EC00_FOUR_RULE_GATE.md')))
    gp = OLD / 'reachable_relation_certificate.json'
    tp = OLD / 'source_transition_table.json'
    ap = OLD / 'independent_audit.json'
    control_path = OLD / 'literal_return_certificate.json'
    graph = json.loads(gp.read_text(encoding='utf-8'))
    audit = json.loads(ap.read_text(encoding='utf-8'))
    control = json.loads(control_path.read_text(encoding='utf-8'))
    assert audit['status'] == control['status'] == 'PASS'
    assert audit['relation_sha256'] == sha(gp) and audit['source_table_sha256'] == sha(tp)
    assert control['source_table_sha256'] == sha(tp) and control['source_audit_sha256'] == sha(ap)
    raw_edges = graph['outgoing_edges']
    n = len(raw_edges)
    assert n == 18450 and sum(len(row) for row in raw_edges) == 109410
    adj = [[(edge[1], max(edge[2], 0), edge[0]) for edge in row] for row in raw_edges]
    rev = [[] for _ in range(n)]
    for u, row in enumerate(adj):
        for v, w, key in row:
            rev[v].append(u)

    # Iterative Kosaraju; recursion depth is not used as an implicit bound.
    seen = [False]*n
    finish = []
    for start in range(n):
        if seen[start]:
            continue
        stack = [(start, False)]
        while stack:
            u, done = stack.pop()
            if done:
                finish.append(u)
                continue
            if seen[u]:
                continue
            seen[u] = True
            stack.append((u, True))
            for v, w, key in reversed(adj[u]):
                if not seen[v]:
                    stack.append((v, False))
    comp = [-1]*n
    members = []
    for start in reversed(finish):
        if comp[start] >= 0:
            continue
        cid = len(members)
        block = []
        comp[start] = cid
        stack = [start]
        while stack:
            u = stack.pop()
            block.append(u)
            for v in rev[u]:
                if comp[v] < 0:
                    comp[v] = cid
                    stack.append(v)
        members.append(block)
    internal_positive = []
    for u, row in enumerate(adj):
        for v, w, key in row:
            if w and comp[u] == comp[v]:
                internal_positive.append([u, key, v, w])

    def route(start, target, component=None):
        queue = deque([start])
        parent = {start: None}
        while queue:
            u = queue.popleft()
            if u == target:
                break
            for v, w, key in adj[u]:
                if component is not None and comp[v] != component:
                    continue
                if v not in parent:
                    parent[v] = (u, key, w)
                    queue.append(v)
        assert target in parent
        path = []
        cursor = target
        while cursor != start:
            u, key, w = parent[cursor]
            path.append([u, key, cursor, w])
            cursor = u
        path.reverse()
        return path

    common = dict(date='2026-10-31', source_relation_sha256=sha(gp), source_table_sha256=sha(tp),
        source_audit_sha256=sha(ap), vertices=n, edges=sum(map(len, adj)),
        component_labels=comp, components=len(members), component_size_histogram=dict(Counter(map(len, members))),
        internal_positive_edges=internal_positive, new_source_engine_calls=0,
        larger_finite_fits=0, new_active_core_sizes=0, matching_terminal_line='FROZEN', universal_CD='OPEN')
    if internal_positive:
        u, key, v, w = internal_positive[0]
        approach = route(0, u)
        back = route(v, u, comp[u])
        loop = [[u, key, v, w]]+back
        assert sum(e[3] for e in loop) > 0
        save('capacity_certificate.json', dict(common, status='UNBOUNDED_CORE_TAIL_EXCESS',
            approach_edges=approach, loop_edges=loop, loop_KEEP_word=[e[1] for e in loop],
            loop_positive_excess=sum(e[3] for e in loop),
            actual_two_reset_high_J_return='OPEN; not inferred from loop repetition'))
        print(json.dumps(dict(status='UNBOUNDED_CORE_TAIL_EXCESS', components=len(members),
            loop_length=len(loop), loop_E=sum(e[3] for e in loop), prior_files=len(pins)), indent=2))
        return

    condensed = [dict() for _ in members]
    indegree = [0]*len(members)
    for u, row in enumerate(adj):
        for v, w, key in row:
            cu, cv = comp[u], comp[v]
            if cu == cv:
                continue
            old = condensed[cu].get(cv)
            if old is None:
                indegree[cv] += 1
            if old is None or w > old[0]:
                condensed[cu][cv] = (w, u, key, v)
    queue = deque(i for i, value in enumerate(indegree) if value == 0)
    order = []
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in condensed[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
    assert len(order) == len(members)
    cp = [0]*len(members)
    best = [None]*len(members)
    for u in reversed(order):
        for v, edge in condensed[u].items():
            score = edge[0]+cp[v]
            if score > cp[u]:
                cp[u] = score
                best[u] = edge
    P = [cp[comp[u]] for u in range(n)]
    for u, row in enumerate(adj):
        assert P[u] >= 0
        for v, w, key in row:
            assert P[u] >= w+P[v]
    bound = P[0]
    closed_lower = control['paired_closed'] and control['E'] == 1+bound
    if closed_lower:
        extension = json.loads((OLD / 'positive_extension_certificate.json').read_text(encoding='utf-8'))
        keys = extension['KEEP_extension']
        path = []
        state = 0
        for key in keys:
            v, w, _ = next(edge for edge in adj[state] if edge[2] == key)
            path.append([state, key, v, w])
            state = v
        assert sum(e[3] for e in path) == bound
        witness_kind = 'inherited exact closed return attains upper bound'
    else:
        path = []
        state = 0
        while P[state] > 0:
            w, u, key, v = best[comp[state]]
            path += route(state, u, comp[state])
            path.append([u, key, v, w])
            state = v
        assert sum(e[3] for e in path) == bound
        witness_kind = 'exact source tail attains finite maximum; no new return assumed'
    assert P[state] == 0
    outcome = 'CORE_ONLY_HIGH_THRESHOLD_IDENTITY_EXCLUDED' if 1+bound <= 4 else 'CORE_EXCESS_CAPACITY_SUFFICIENT_HIGH_J_RETURN_OPEN'
    save('capacity_certificate.json', dict(common, status='FINITE_EXACT_CAPACITY', outcome=outcome,
        potentials=P, component_remaining_bounds=cp, component_topological_order=order,
        potential_value_histogram=dict(Counter(P)), prefix_positive_excess=1,
        maximum_additional_tail_excess=bound, maximum_prefix_plus_tail_excess=1+bound,
        pure_reset_capacity=4, attaining_tail_edges=path, attaining_KEEP_word=[e[1] for e in path],
        attaining_tail_end=state, attaining_tail_positive_excess=sum(e[3] for e in path), witness_kind=witness_kind,
        inherited_closed_return_sha256=sha(control_path) if closed_lower else None,
        closed_return_attains_upper_bound=closed_lower,
        outer_fringe_activation_before_synchronization_necessary_for_E_gt_4=1+bound <= 4,
        requested_unrestricted_identity='OPEN', automatic_successor_launched=False))
    print(json.dumps(dict(status='FINITE_EXACT_CAPACITY', outcome=outcome, components=len(members),
        potential_value_histogram=dict(Counter(P)), maximum_additional_tail_excess=bound,
        maximum_prefix_plus_tail_excess=1+bound, C_D=4, closed_return_attains_upper_bound=closed_lower,
        attaining_word=[e[1] for e in path], prior_files=len(pins), stage_11G_files=len(stage)), indent=2))


if __name__ == '__main__':
    main()
