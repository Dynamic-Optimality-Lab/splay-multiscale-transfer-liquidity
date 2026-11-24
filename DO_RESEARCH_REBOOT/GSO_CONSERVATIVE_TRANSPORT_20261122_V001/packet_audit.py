"""Exact packet monitor for the independently verified frozen policy.

This monitor identifies the still-open physical inequality. It does not turn
the equivalent queue condition into an assumed all-source theorem.
"""
import sys
import json
import hashlib
sys.dont_write_bytecode = True
import verify_extended as E


def main():
    old = E.V.read(E.HERE/'EXTENDED_INDEPENDENT_VERIFICATION.json'); assert old['passed']
    choice = E.V.read(E.HERE/'SELECTED_ROLE_POLICY.json')
    teacher = E.V.read(E.HERE/'TEACHER_SUMMARY.json'); holdouts = E.V.read(E.HERE/'HOLDOUT_SUMMARY.json')
    inputs = {}; out = []
    for row in teacher['cases']:
        if row['tag'] not in inputs:
            cert = E.V.read(E.HERE/row['certificate'])
            path = E.ROOT/cert['trace']['path']
            assert hashlib.sha256(path.read_bytes()).hexdigest() == cert['trace']['sha256']
            inputs[row['tag']] = path
    inputs.update({row['tag']: E.HERE/row['trace'] for row in holdouts['cases']})
    for tag, path in inputs.items():
        z = E.V.read(path); result = E.replay(z, E.tape(z), choice)
        out.append({'tag': tag, 'source': z['source']['name'], **result['packet_peak']})
    result = {'passed': True, 'sources': len(out), 'H': choice['H'],
              'maximum_observed_deficit': max(row['maximum_deficit'] for row in out),
              'cases': out,
              'universal_identity': 'With target reserve t, other touched credit r and original cost q, funded target-first pooling gives D_next=max(0,D+q-r), D=H-t. Every access starts D=0. Thus D is the maximum suffix sum of net demands q-r.',
              'exact_acceptance': 'For every original access, every contiguous B-step packet must have sum(q-r)<=H. This is equivalent to no failed guard for this kernel, not an established arbitrary-source inequality.',
              'sharing_caution': 'r is transferred existing stock, may circulate, and is not new A issuance. The separate global9H A supply bound handles provenance.',
              'first_missing_physical_implication': 'Bound these packet deficits on arbitrary reachable original paired states, including interruptions/reentry, cross rotations, recreated ancestry and all original interleavings.',
              'scope': 'The target-battery identity is universal algebra. The observed maximum is finite evidence only.',
              'universal_CD': 'OPEN'}
    if not (E.HERE/'FINAL_MANIFEST.json').exists():
        (E.HERE/'PACKET_VERIFICATION.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps({key: result[key] for key in ('passed','sources','H','maximum_observed_deficit','universal_CD')}))


if __name__ == '__main__':
    main()
