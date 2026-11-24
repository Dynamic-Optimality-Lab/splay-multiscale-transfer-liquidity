"""Bounded exact original-source transport audit, declared in ADMISSION.json."""
import sys
import time
import json
from pathlib import Path
sys.dont_write_bytecode = True
import transport as T


def sources():
    for i in range(18):
        path = T.TRACE / f'run_001/trace_{i:02d}.json.gz'
        yield 'legacy_%02d' % i, path, T.load(path), 'Previously sealed full original-event/Pi audit.'
    for tag, relative in [('H9q5', 'scaling_001/trace_08.json.gz'),
                           ('H7q44', 'counter_001/W_H1_complete_trace.json.gz')]:
        path = T.PREV / relative; z = T.load(path)
        yield tag, path, z, 'Previous bank checkpoint independently checked full original carrier/Pi.'
        mirrored = T.F.compile_source(T.F.mirror(z['source']))
        T.write(f'inputs/mirror_{tag}.json.gz', mirrored)
        yield 'mirror_' + tag, T.HERE / f'inputs/mirror_{tag}.json.gz', mirrored, 'Complete reflected original physical source; no new Pi claim.'
    # Additional scales are selected before observing the new teacher output.
    for index in (3, 5, 7, 14, 16, 20):
        path = T.PREV / f'scaling_001/trace_{index:02d}.json.gz'
        yield 'scale_%02d' % index, path, T.load(path), 'Sealed complete physical source; no new Pi claim.'


def main():
    start = time.perf_counter(); rows = []; pins = []; rotations = 0; count = 0
    for tag, path, z, scope in sources():
        count += 1; assert count <= 36
        rotations += z.get('real_rotations', sum(len(s['bits']) for s in z['steps']))
        assert rotations <= 1000000
        pins.append(T.pin(path))
        T.write(f'inputs/{tag}_vouchers.json.gz', T.vouchers(z))
        for H in (1, 2, 5, 8):
            assert time.perf_counter() - start <= 300, 'declared wall budget'
            cert = T.solve(z, H)
            cert['trace'] = pins[-1]
            cert['physical_verification_scope'] = scope
            artifact = f'run_001/{tag}_H{H}.json.gz'
            T.write(artifact, cert)
            row = {'tag': tag, 'source': z['source']['name'], 'H': H,
                   'keys': sum(map(len, z['blocks'])), 'A': z['A'], 'Q_B': z['Q_B'],
                   'paid': cert['paid'], 'shortfall': cert['demand'] - cert['paid'],
                   'nodes': cert['nodes'], 'edges': cert['edges'], 'certificate': artifact}
            rows.append(row); print(json.dumps(row), flush=True)
    T.write('PINNED_AUDIT_TRACES.json', pins)
    T.write('TEACHER_SUMMARY.json', {'cases': rows, 'sources': count, 'physical_rotations': rotations,
                                   'seconds': time.perf_counter() - start,
                                   'scope': 'Exact source-specific free conservative transfers. No arbitrary-source feasibility premise or policy.',
                                   'universal_CD': 'OPEN'})


if __name__ == '__main__':
    main()
