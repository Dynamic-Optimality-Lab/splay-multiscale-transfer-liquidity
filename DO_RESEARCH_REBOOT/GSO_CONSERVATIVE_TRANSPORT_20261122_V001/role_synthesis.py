"""Inverse six-port synthesis, followed by exact original-source CEGIS.

The symbolic full-profile invariant is deliberately separated from the open
arbitrary-source initialization/preservation theorem.
"""
import sys
import time
import json
import itertools
from collections import Counter
import z3
sys.dont_write_bytecode = True
import transport as T

ROLES = ('external', 'grandparent', 'parent', 'middle2')


def symbolic():
    H = z3.Real('H')
    orders = list(itertools.permutations(ROLES))
    checked = []
    for perm in orders:
        names = ['target', *perm, 'middle1']
        out = {name: z3.If(6*H-1-j*H <= 0, 0,
                          z3.If(6*H-1-j*H >= H, H, 6*H-1-j*H))
               for j, name in enumerate(names)}
        solver = z3.Solver(); solver.add(H >= 1)
        wanted = z3.And(*[out[name] == H for name in names[:-1]],
                        out['middle1'] == H-1,
                        2*out['middle2'] + out['grandparent'] == 3*H,
                        sum(out.values()) == 6*H-1)
        solver.add(z3.Not(wanted))
        assert solver.check() == z3.unsat
        checked.append({'middle_order': list(perm), 'arbitrary_real_H_ge1': True})
    result = {'status': 'PROVED_LOCAL_FULL_PROFILE_TRANSPORT', 'orders': checked,
              'invariant': 'Full carry and full fresh (H,H) profile are preserved at the exact distinct-owner six-port RR/LL template.',
              'retention': 'persistent=H, retired=H-1, so persistent-retired=1 and weighted fresh profile stays3H.',
              'scope': 'One local repeated-role template; no arbitrary-source lower-bound initialization or general funded guard is assumed.',
              'universal_CD': 'OPEN'}
    T.write('SYMBOLIC_RETENTION_CERTIFICATE.json', result)
    return orders


def prepared(z, perm):
    ev = T.B.events(z)
    owner = {x: i for i, block in enumerate(z['blocks']) for x in block}
    by_id = {tuple(s['id']): s for s in z['steps']}
    changed = 0
    for e in ev:
        if e['id'][0] != 'B':
            continue
        s = by_id[tuple(e['id'])]
        if s['type'] not in ('LL', 'RR'):
            continue
        first, second = s['bits']
        roles = {'target': e['target'], 'external': first['grandparent'],
                 'grandparent': first['demoted'], 'parent': second['demoted'],
                 'middle1': first['middle'], 'middle2': second['middle']}
        order = []
        for role in ['target', *perm, 'middle1']:
            key = roles[role]
            if key is not None and owner[key] not in order:
                order.append(owner[key])
        assert set(order) == set(e['scope'])
        e['priority'] = order; changed += 1
    return ev, changed


def fast_cyclic(z, ev, H):
    state = [H] * len(z['blocks'])
    compiled = [(e['a'] or e['k'], e['q'], e['priority'], e['id']) for e in ev]

    def sweep(initial, fail_fast=False):
        stock = initial.copy(); first = None; paid = 0
        for reset, q, scope, identifier in compiled:
            if reset:
                for block in scope:
                    stock[block] = H
            else:
                mass = sum(stock[block] for block in scope)
                if mass < q and first is None:
                    first = identifier
                    if fail_fast:
                        return None, first, paid
                consume = min(mass, q); paid += consume; mass -= consume
                for block in scope:
                    amount = min(H, mass); stock[block] = amount; mass -= amount
        return stock, first, paid

    # Any failure from the full vector already excludes every bounded start.
    # Otherwise iterate the same full clipped period map to its greatest seam.
    for lap in range(len(state)*H + 1):
        new, failure, paid = sweep(state, True)
        if failure:
            return {'passed': False, 'first_failure': failure, 'pass': lap,
                    'reason': 'Monotone upper orbit fails; every funded closed start is dominated by this orbit.'}
        assert all(a <= b for a, b in zip(new, state))
        if new == state:
            assert paid == z['Q_B']
            return {'passed': True, 'greatest_closed_balance': True, 'passes': lap+1}
        state = new
    raise AssertionError('integer descent bound')


def main():
    start = time.perf_counter(); orders = symbolic()
    audit = T.load(T.HERE / 'TEACHER_SUMMARY.json')
    cases = []
    seen = set()
    for row in audit['cases']:
        if row['tag'] in seen:
            continue
        seen.add(row['tag'])
        cert = T.load(T.HERE / row['certificate'])
        path = T.ROOT / cert['trace']['path']
        cases.append((row['tag'], path))
    candidates = {(H, order): [] for H in (5, 8) for order in orders}
    dead = []; attempts = 0
    for tag, path in cases:
        z = T.load(path)
        for key in list(candidates):
            assert time.perf_counter()-start <= 300, 'declared role-synthesis wall budget'
            H, perm = key; ev, changed = prepared(z, perm)
            receipt = fast_cyclic(z, ev, H); attempts += 1
            if receipt['passed']:
                candidates[key].append(tag)
            else:
                dead.append({'H': H, 'middle_order': list(perm), 'eliminating_source': tag,
                             'source': z['source']['name'], 'physical_role_steps': changed, **receipt})
                del candidates[key]
        print(json.dumps({'source': tag, 'surviving_candidate_capacity_pairs': len(candidates),
                          'eliminated': len(dead)}), flush=True)
    survivors = [{'H': H, 'middle_order': list(perm), 'verified_source_tags': passed}
                 for (H, perm), passed in candidates.items()]
    T.write('ROLE_CEGIS_RESULT.json', {'status': 'FINITE_EXACT_ROLE_POLICY_DIAGNOSTIC',
            'candidate_capacity_pairs': 48, 'attempts': attempts, 'sources': len(cases),
            'survivors': survivors, 'eliminated': dead, 'seconds': time.perf_counter()-start,
            'local_retention': 'SYMBOLIC_RETENTION_CERTIFICATE.json',
            'missing': 'A source-uniform lower-bound invariant including initialization and every legal successor.',
            'universal_CD': 'OPEN'})
    if survivors:
        winner = survivors[0]
        T.write('SELECTED_ROLE_POLICY.json', winner | {'status': 'FINITE_SURVIVOR_NOT_UNIVERSAL',
                 'frozen_declaration': 'ROLE_SYNTHESIS_ADMISSION.json'})


if __name__ == '__main__':
    main()
