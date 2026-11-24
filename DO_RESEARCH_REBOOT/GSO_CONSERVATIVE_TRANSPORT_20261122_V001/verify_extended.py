"""Independent frozen-policy and held-out physical/cut verification.

Uses the independent current checker, not any producer, policy implementation
or optimizer. Original full cyclic Pi is bound to sealed old receipts where
an exact counterexample to the proposed entry condition is reported.
"""
import sys
import json
import hashlib
import time
from pathlib import Path
from collections import Counter
sys.dont_write_bytecode = True
import verify as V
HERE = V.HERE; ROOT = V.ROOT


def tape(z):
    owner = {x: i for i, block in enumerate(z['blocks']) for x in block}
    out = []
    for op in z['operations']:
        if op['k']:
            out.append({'id': ['K', op['id']], 'a': 0, 'q': 0, 'k': 1, 'scope': [owner[op['target']]]})
        for s in z['steps'][op['steps'][0]:op['steps'][1]]:
            out.append({key: s[key] for key in ('id', 'a', 'q', 'k', 'scope')})
    return out


def replay(z, events, choice, saved=None):
    H = choice['H']; owner = {x: i for i, block in enumerate(z['blocks']) for x in block}
    steps = {tuple(s['id']): s for s in z['steps']}; prepared = []
    for e in events:
        target = z['operations'][e['id'][1]-1]['target']; block = owner[target]
        order = [block] + [i for i in sorted(e['scope']) if i != block]
        role_keys = None
        if e['id'][0] == 'B':
            s = steps[tuple(e['id'])]
            if s['type'] in ('LL', 'RR'):
                one, two = s['bits']
                role_keys = {'target': target, 'external': one['grandparent'],
                             'grandparent': one['demoted'], 'parent': two['demoted'],
                             'middle1': one['middle'], 'middle2': two['middle']}
                order = []
                for name in ['target', *choice['middle_order'], 'middle1']:
                    key = role_keys[name]
                    if key is not None and owner[key] not in order:
                        order.append(owner[key])
        assert set(order) == set(e['scope']) and order[0] == block
        prepared.append((e, order, role_keys))

    def run(initial, record=False):
        bank = initial.copy(); paid = issued = 0; rows = []; entries = []; failures = []
        packet_op = None; debt = 0; packet_start = None; net_rows = []
        peak = {'maximum_deficit': 0, 'start_id': None, 'end_id': None, 'terms': []}
        for j, (e, order, roles) in enumerate(prepared):
            before = [bank[i] for i in order]; mass = sum(before)
            if roles and len(order) == 6:
                stocks = {name: bank[owner[key]] for name, key in roles.items()}
                if stocks['external'] < 1 or stocks['grandparent'] < 1:
                    entries.append({'id': e['id'], 'target': z['operations'][e['id'][1]-1]['target'],
                                    'type': steps[tuple(e['id'])]['type'], 'role_keys': roles,
                                    'role_stocks': stocks, 'pooled_credit': mass,
                                    'funded_original_double': mass >= 1})
            if e['a'] or e['k']:
                after = [H]*len(order); issue = sum(after)-mass; consume = 0
                assert 0 <= issue <= (8*H if e['a'] else H)
            else:
                consume = min(mass, e['q']); issue = 0; remaining = mass-consume
                after = [min(H, max(0, remaining-lane*H)) for lane in range(len(order))]
            for block, value in zip(order, after): bank[block] = value
            assert sum(after)-mass == issue-consume
            if record and e['id'][0] == 'B':
                if packet_op != e['id'][1]:
                    packet_op = e['id'][1]; debt = 0; packet_start = None; net_rows = []
                    assert before[0] == H, 'once-per-genuine-KEEP reserve before B'
                other_credit = mass-before[0]
                net = e['q']-other_credit
                new_debt = max(0, debt+net)
                if debt == 0 and new_debt > 0:
                    packet_start = len(net_rows)
                net_rows.append({'id': e['id'], 'q': e['q'], 'other_credit': other_credit,
                                 'net_demand': net})
                if consume == e['q']:
                    assert H-after[0] == new_debt <= H
                if new_debt > peak['maximum_deficit']:
                    assert packet_start is not None
                    terms = net_rows[packet_start:].copy()
                    assert sum(item['net_demand'] for item in terms) == new_debt
                    peak = {'maximum_deficit': new_debt, 'start_id': terms[0]['id'],
                            'end_id': terms[-1]['id'], 'terms': terms}
                if new_debt == 0:
                    packet_start = None
                debt = new_debt
            if consume != e['q']:
                failures.append(e['id'])
            if record:
                rows.append({'event': j, 'id': e['id'], 'priority': order,
                             'before': before, 'after': after, 'issued': issue,
                             'paid': consume, 'unpaid': e['q']-consume})
            paid += consume; issued += issue
        return bank, paid, issued, rows, entries, failures, peak

    state = [H]*len(z['blocks']); passes = []
    for lap in range(len(state)*H+1):
        new, paid, issued, _, _, failures, _ = run(state)
        assert all(x <= y for x, y in zip(new, state))
        passes.append({'pass': lap, 'mass_before': sum(state), 'mass_after': sum(new),
                       'unpaid': z['Q_B']-paid})
        if new == state: break
        assert sum(new) < sum(state); state = new
    else: raise AssertionError('integer descending rank violated')
    final, paid, issued, rows, entries, failures, peak = run(state, True)
    assert final == state and paid == issued and paid == z['Q_B'] and not failures
    if saved is not None:
        assert saved['initial_greatest_fixed_point'] == state
        assert saved['period_passes'] == passes and saved['rows'] == rows
        assert saved['paid'] == saved['issued'] == paid and saved['failures'] == []
    return {'paid': paid, 'H': H, 'greatest_closed_balance_checked': True,
            'passes': len(passes), 'local_entry_failures': entries, 'packet_peak': peak}


def main():
    start = time.perf_counter(); old = V.read(HERE/'INDEPENDENT_VERIFICATION.json')
    assert old['passed']; chosen = V.read(HERE/'SELECTED_ROLE_POLICY.json')
    teacher = V.read(HERE/'TEACHER_SUMMARY.json'); holdouts = V.read(HERE/'HOLDOUT_SUMMARY.json')
    cases = []; total = Counter(old['totals']); unique = {}
    for row in teacher['cases']:
        unique.setdefault(row['tag'], row)
    old_scopes = {row['tag']: row for row in old['sources']}
    obstruction = None
    old_checkpoint = HERE.parent/'GSO_PHYSICAL_BANK_RULE_20261122_V001'
    original = V.read(old_checkpoint/'counter_001/H8_original_events.json.gz')
    original_U = {tuple(row['id']): row for row in original['original_U']}
    for tag, row in unique.items():
        certificate = V.read(HERE/row['certificate']); path = ROOT/certificate['trace']['path']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == certificate['trace']['sha256']
        z = V.read(path); assert tag in old_scopes
        result = replay(z, tape(z), chosen)
        if tag == 'H9q5':
            assert z['source'] == original['source']
            # Find a literal original U, not just a paid or ineligible event.
            for entry in result['local_entry_failures']:
                if tuple(entry['id'][1:]) in original_U:
                    obstruction = {'status': 'REFUTED_EXACT_ENTRY_CONJECTURE',
                        'conjecture': 'ENTRY_CONJECTURE_ADMISSION.json',
                        'selected_policy': chosen, 'trace': certificate['trace'], **entry,
                        'original_U_receipt': original_U[tuple(entry['id'][1:])],
                        'cyclic_Pi_binding': 'Previous sealed INDEPENDENT_VERIFICATION.json fully checked this original source and every literal U occurrence.',
                        'scope': 'The universal two-positive-fresh-banks entry condition is false. This funded event does not refute the policy or Universal CD.'}
                    break
        result['local_entry_failures_count'] = len(result.pop('local_entry_failures'))
        cases.append({'tag': tag, 'source': z['source']['name'], **result})
    new_sources = []
    for row in holdouts['cases']:
        z = V.read(HERE/row['trace']); events, stats = V.physical(z)
        total.update({key: stats[key] for key in ('operations', 'real_rotations')})
        free = V.read(HERE/row['free_certificate'])
        assert hashlib.sha256((HERE/row['trace']).read_bytes()).hexdigest() == free['trace']['sha256']
        V.certificate(z, events, free)
        V.voucher_check(z, V.read(HERE/f'holdouts/{row["tag"]}_vouchers.json.gz'))
        policy = V.read(HERE/row['role_certificate']); result = replay(z, events, chosen, policy)
        result['local_entry_failures_count'] = len(result.pop('local_entry_failures'))
        cases.append({'tag': row['tag'], 'source': z['source']['name'], **result})
        new_sources.append({'tag': row['tag'], **stats})
    out = {'passed': True, 'selected_policy_sources': len(cases),
           'independent_physical_sources_total': old['physical_sources']+len(new_sources),
           'independent_free_flow_cut_certificates': old['capacity_certificates']+len(new_sources),
           'physical_totals': dict(total), 'selected_policy_original_Q_paid': sum(c['paid'] for c in cases),
           'cases': cases, 'new_immutable_physical_sources': new_sources,
           'entry_conjecture_refuted_on_original_U': obstruction is not None,
           'seconds': time.perf_counter()-start, 'universal_CD': 'OPEN',
           'scope': 'Independent full physical original replay and exact flow/cut certificates on36 complete sources; independent greatest-closed-policy replay on all36. Full cyclic Pi reused from sealed matching sources only.'}
    if not (HERE/'FINAL_MANIFEST.json').exists():
        (HERE/'EXTENDED_INDEPENDENT_VERIFICATION.json').write_text(json.dumps(out, indent=2), encoding='utf-8')
        if obstruction:
            (HERE/'ENTRY_INVARIANT_OBSTRUCTION.json').write_text(json.dumps(obstruction, indent=2), encoding='utf-8')
    print(json.dumps({key: out[key] for key in ('passed', 'selected_policy_sources', 'independent_physical_sources_total', 'independent_free_flow_cut_certificates', 'physical_totals', 'entry_conjecture_refuted_on_original_U', 'seconds')}))


if __name__ == '__main__':
    main()
