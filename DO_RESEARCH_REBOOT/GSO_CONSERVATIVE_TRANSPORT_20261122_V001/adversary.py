"""Complete held-out nested and arbitrary-shape restoration interleavings."""
import sys
import json
import random
import time
sys.dont_write_bytecode = True
import transport as T
import role_synthesis as S


def source(n, mode):
    initial = {'root': 1, 'children': {str(k): [None, k+1 if k<n else None] for k in range(1, n+1)}}
    operations = []; current = 1

    def access(target, keep=True, adjacent=True):
        nonlocal current
        if adjacent:
            sign = 1 if target >= current else -1
            for key in range(current+sign, target, sign):
                operations.append(['D', key])
        operations.append(['K' if keep else 'D', target]); current = target

    # All global leaves have already participated before the holdout renewals.
    for key in range(1, n+1): access(key)
    for key in range(n-1, 0, -1): access(key)
    depth = (n-1).bit_length()-1
    if mode == 'nested':
        for round_no in range(3):
            for scale in range(depth, 1, -1):
                width = 2**scale
                left = 1 + ((round_no*17 + scale*7) % (n-width))
                right = left+width
                for j in range(scale+1):
                    access(right+1-2**j)
                    if j % 2:
                        access(left+min(2**(j-1), width))
                # Proper local restoration is interleaved with the next scale.
                for key in range(left, min(left+7, right)+1): access(key)
                for key in range(right, max(right-7, left)-1, -1): access(key)
    else:
        rng = random.Random(749+31*n)
        for index in range(1800):
            if index % 7 == 0:
                target = rng.randrange(1, n+1)
            else:
                distance = 2**rng.randrange(depth+1)
                target = min(n, max(1, current + distance*(1 if rng.randrange(2) else -1)))
            access(target, keep=(index % 5 != 1), adjacent=False)
            if index % 23 == 0:
                lo, hi = max(1, target-3), min(n, target+3)
                for key in range(lo, hi+1): access(key, adjacent=False)
                for key in range(hi-1, lo-1, -1): access(key, adjacent=False)
    for key in range(1, n+1): access(key, adjacent=False)
    for key in range(n-1, 0, -1): access(key, adjacent=False)
    return {'name': f'holdout_{mode}_N{n}', 'initial_A': initial, 'initial_B': initial,
            'diagonal': initial, 'prefix': [], 'operations': operations,
            'construction': 'Counted global warmup, held-out nested/arbitrary-shape internal renewals, counted exact paired restoration.',
            'holdout_mode': mode, 'n': n}


def main():
    start = time.perf_counter(); selected = T.load(T.HERE/'SELECTED_ROLE_POLICY.json')
    rows = []; rotations = 0
    for n in (65, 129, 257, 513):
        for mode in ('nested', 'arbitrary_shape'):
            assert time.perf_counter()-start <= 180
            z = T.F.compile_source(source(n, mode)); rotations += z['real_rotations']; assert rotations <= 450000
            tag = f'{mode}_{n}'; path = f'holdouts/{tag}_trace.json.gz'; T.write(path, z)
            ev, changed = S.prepared(z, tuple(selected['middle_order']))
            policy = T.B.cyclic_events(z, ev, selected['H'], True, 'all_original_Q')
            T.write(f'holdouts/{tag}_role_policy.json.gz', policy)
            # Free flow is tested at the SAME candidate capacity.
            free = T.solve(z, selected['H']); free['trace'] = T.pin(T.HERE/path)
            T.write(f'holdouts/{tag}_free_transport.json.gz', free)
            T.write(f'holdouts/{tag}_vouchers.json.gz', T.vouchers(z))
            row = {'tag': tag, 'source': z['source']['name'], 'H': selected['H'],
                   'operations': len(z['operations']), 'real_rotations': z['real_rotations'],
                   'A': z['A'], 'Q_B': z['Q_B'], 'role_paid': policy['paid'],
                   'role_failures': len(policy['failures']), 'first_failed_original_id': policy['failures'][0]['id'] if policy['failures'] else None,
                   'free_paid': free['paid'], 'trace': path,
                   'role_certificate': f'holdouts/{tag}_role_policy.json.gz',
                   'free_certificate': f'holdouts/{tag}_free_transport.json.gz'}
            rows.append(row); print(json.dumps(row), flush=True)
    T.write('HOLDOUT_SUMMARY.json', {'policy_frozen_before_holdouts': selected,
            'cases': rows, 'additional_real_rotations': rotations,
            'seconds': time.perf_counter()-start, 'universal_CD': 'OPEN'})


if __name__ == '__main__':
    main()
