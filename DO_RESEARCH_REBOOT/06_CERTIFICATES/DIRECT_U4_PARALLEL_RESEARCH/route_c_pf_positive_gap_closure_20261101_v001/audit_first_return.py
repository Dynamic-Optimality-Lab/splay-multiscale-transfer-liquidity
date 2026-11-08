"""One gate-fixed first-return audit using the existing source relation only."""
import hashlib
import importlib.util
import json
import subprocess
import sys
from collections import deque
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASE = HERE.parent
PF = BASE / 'route_c_parent_fringe_obstruction_20261101_v001'
KC = BASE / 'route_c_seven_core_return_obstruction_20261031_v001'
EC = BASE / 'route_c_seven_core_excess_capacity_20261031_v001'
STAGE = ROOT / 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'


def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def save(name, value):
    with (HERE / name).open('x', encoding='utf-8') as f:
        json.dump(value, f, indent=2, ensure_ascii=False)
        f.write('\n')


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def main():
    inherited = read(PF / 'entry_source_pins.json')
    pins = dict(inherited['files'])
    for rel, h in pins.items():
        assert sha(ROOT / rel) == h, rel
    for p in BASE.rglob('*'):
        if p.is_file() and HERE not in p.parents:
            pins[p.relative_to(ROOT).as_posix()] = sha(p)
    stage = {p.relative_to(STAGE).as_posix(): sha(p) for p in STAGE.rglob('*') if p.is_file()}
    assert stage == inherited['stage_files'] and len(stage) == 125
    assert git('rev-parse', 'HEAD') == '8c378d49283b3738b18e7175886772a98025e4e9'
    assert git('branch', '--show-current') == 'coarse-double-branch'
    assert git('status', '--porcelain=v1', '--untracked-files=no') == ''
    save('entry_source_pins.json', dict(head=git('rev-parse', 'HEAD'), branch=git('branch', '--show-current'),
        files=pins, stage_files=stage, gate_sha256=sha(HERE / 'PG00_FOUR_RULE_GATE.md'),
        prior_campaign_files=sum(p.is_file() and HERE not in p.parents for p in BASE.rglob('*')),
        matching_terminal='FROZEN'))
    for name, h in read(PF / 'delivery_manifest.json')['files'].items():
        assert sha(PF / name) == h, name
    table = read(KC / 'source_transition_table.json')
    graph = read(KC / 'reachable_relation_certificate.json')
    source_audit = read(KC / 'independent_audit.json')
    assert source_audit['status'] == 'PASS'
    assert source_audit['source_table_sha256'] == sha(KC / 'source_transition_table.json')
    assert source_audit['relation_sha256'] == sha(KC / 'reachable_relation_certificate.json')
    cap = read(EC / 'capacity_certificate.json')
    cores, tt = table['cores'], table['transitions']
    pairs, edges, labels = graph['pair_ids'], graph['outgoing_edges'], cap['component_labels']
    component = {s for s, label in enumerate(labels) if label == labels[4676]}
    assert len(component) == 18232
    spec = importlib.util.spec_from_file_location('inherited_pf_profile', PF / 'find_zero_offer_returns.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    profile = module.profile

    def tr(t, y):
        return tt[7 * t + y - 1]

    def row(s, y):
        ar, br = tr(pairs[s][0], y), tr(pairs[s][1], y)
        edge = next(e for e in edges[s] if e[0] == y)
        assert [ar['target'], br['target']] == pairs[edge[1]]
        return dict(source=s, key=y, target=edge[1], a=ar['a'], q=br['q'], delta=edge[2])

    def cheap(s):
        return [row(s, y) for y, target, delta in edges[s]
                if target in component and delta <= 0 and tr(pairs[s][0], y)['a'] == 1]

    def annotated(r, T, z, k):
        r = dict(r)
        pr = profile(T, z, r['key'])
        ceiling = pr['source_depth'] // 2 if k == 0 else pr['PF_U'] // 2 + k - 1
        C = 2 * r['a']
        assert r['q'] <= ceiling
        r.update(k=k, profile=pr, ceiling=ceiling, capacity=C, offer=C-min(C, ceiling))
        return r

    found = None
    counts = dict(positive_anchors_examined=0, first_payers_examined=0, second_payers_examined=0,
                  third_payers_examined=0, first_returns_examined=0)
    for s in sorted(component):
        if found:
            break
        for y, target, delta in edges[s]:
            ar, br = tr(pairs[s][0], y), tr(pairs[s][1], y)
            if target not in component or (ar['a'], br['q']) != (1, 3):
                continue
            counts['positive_anchors_examined'] += 1
            anchor = row(s, y)
            T = cores[pairs[target][1]]
            for r1 in cheap(target):
                counts['first_payers_examined'] += 1
                z = r1['key']
                p1 = annotated(r1, T, z, 0)
                if p1['offer']:
                    continue
                for r2 in cheap(r1['target']):
                    if r2['key'] == z:
                        continue
                    counts['second_payers_examined'] += 1
                    p2 = annotated(r2, T, z, 1)
                    if p2['offer']:
                        continue
                    for r3 in cheap(r2['target']):
                        if r3['key'] == z:
                            continue
                        counts['third_payers_examined'] += 1
                        p3 = annotated(r3, T, z, 2)
                        if p3['offer']:
                            continue
                        returns = [r for r in cheap(r3['target']) if r['key'] == z]
                        for r4 in returns:
                            counts['first_returns_examined'] += 1
                            p4 = annotated(r4, T, z, 3)
                            assert p4['offer'] == 0
                            found = dict(anchor=anchor, first_key=z, post_anchor_T=T,
                                         payers=[p1,p2,p3,p4])
                            break
                        if found:
                            break
                    if found:
                        break
                if found:
                    break
            if found:
                break
    if found is None:
        save('first_return_obstruction.json', dict(status='NO_PREFIX_IN_PREDECLARED_FIXED_CLASS', counts=counts,
             universal_statement_proved=False, larger_finite_fits=0, source_engine_calls=0))
        print(json.dumps(dict(status='NO_PREFIX_IN_PREDECLARED_FIXED_CLASS', counts=counts)))
        return

    start = found['payers'][-1]['target']
    # One exact saturated-clock reachability classification; no horizon.
    queue = deque([start])
    parents = {start: None}
    positive_exit = None
    while queue and positive_exit is None:
        s = queue.popleft()
        for y, target, delta in edges[s]:
            if target not in component:
                continue
            r = row(s, y)
            if (r['a'], r['q']) == (1, 3):
                positive_exit = r
                break
            if r['a'] == 1 and delta <= 0 and target not in parents:
                parents[target] = [s, y]
                queue.append(target)

    def path_to(parents, target):
        result = []
        at = target
        while parents[at] is not None:
            prev, key = parents[at]
            result.append(row(prev, key))
            at = prev
        return result[::-1]

    extension = path_to(parents, positive_exit['source']) if positive_exit is not None else []
    end = positive_exit['target'] if positive_exit is not None else start
    # Complete source closure in the inherited strongly connected component.
    queue = deque([end])
    back = {end: None}
    initial = found['anchor']['source']
    while queue and initial not in back:
        s = queue.popleft()
        for y, target, delta in edges[s]:
            if target in component and target not in back:
                back[target] = [s, y]
                queue.append(target)
    assert initial in back
    closing = path_to(back, initial)
    word = [found['anchor']] + found['payers'] + extension
    if positive_exit is not None:
        word.append(positive_exit)
    word += closing
    state = initial
    for r in word:
        assert r['source'] == state
        state = r['target']
    assert state == initial

    # Source startup from the inherited seed, never used as recurrent credits.
    startup = []
    state = initial
    while graph['predecessors'][state] is not None:
        previous, key = graph['predecessors'][state]
        startup.append(row(previous, key))
        state = previous
    startup.reverse()
    assert pairs[state] == graph['seed_pair_ids']
    save('first_return_obstruction.json', dict(status='FIRST_RETURN_STOPPING_RULE_REFUTED_EXACT',
        source_table_sha256=sha(KC / 'source_transition_table.json'),
        source_relation_sha256=sha(KC / 'reachable_relation_certificate.json'),
        source_audit_sha256=sha(KC / 'independent_audit.json'),
        counts=counts, selected=found, first_return_off_diagonal=True, debt_at_first_return=1,
        later_positive_exit=positive_exit, zero_offer_extension=extension,
        saturated_clock=3, cost_one_pools_capacity=2,
        saturated_reachability_nodes_examined=len(parents), closure=closing,
        startup_seed_state=state, startup_seed_pair=pairs[state], startup_common_KEEP=startup,
        source_prefix_rows=table['prefix_rows'], closed_rows=word,
        closed_word=[r['key'] for r in word],
        closed_A=sum(r['a'] for r in word), closed_Q=sum(r['q'] for r in word),
        original_eligibility_U4_counterexample=False, CD_counterexample=False,
        larger_finite_fits=0, source_engine_calls=0, new_key_count_sweeps=0,
        unchanged_FI_PF_algorithms=True, matching_terminal='FROZEN'))
    print(json.dumps(dict(status='FIRST_RETURN_STOPPING_RULE_REFUTED_EXACT', counts=counts,
        anchor=found['anchor'], first_key=found['first_key'], payers=[(r['key'],r['a'],r['q'],r['ceiling']) for r in found['payers']],
        later_positive=positive_exit, zero_offer_extension=[r['key'] for r in extension],
        closed_word=[r['key'] for r in word], A=sum(r['a'] for r in word), Q=sum(r['q'] for r in word)),indent=2))


if __name__ == '__main__':
    main()
