"""Read-only provenance/dimension audit; does not rerun symbolic reductions."""
import ast
import hashlib
import json
import os
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from certify_dirty import cases


def native(path):
    path = Path(path).absolute()
    return Path(chr(92) * 2 + '?' + chr(92) + str(path)) if os.name == 'nt' else path


def digest(path):
    return hashlib.sha256(native(path).read_bytes()).hexdigest()


def read(name):
    return json.loads((HERE / name).read_text(encoding='utf-8'))


def main():
    parsed = []
    for path in sorted(HERE.glob('*.py')):
        ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
        parsed.append(path.name)

    proof = read('proof_certificate.json')
    assert proof['status'] == 'COMPLETE' and proof['failures'] == []
    assert (proof['cases'], proof['right_cases'], proof['left_cases']) == (6300, 2555, 3745)
    assert proof['production_DAG_nodes'] == 14600 and proof['cpu_seconds'] < 300
    expected = list(cases())
    assert len(expected) == len(proof['rows']) == 6300
    family_counts = Counter()
    for (meta, source, period, word), row in zip(expected, proof['rows']):
        assert len(period) == len(word)
        assert {k: row[k] for k in meta} == meta
        assert set(row) == set(meta) | {'forced_final_root_claim_verified', 'pins_sha256'}
        assert row['forced_final_root_claim_verified'] is True
        pins = {**source, 'T_bT0': meta['target'], 'T_bd0': meta['d']}
        for k in range(meta['d'] + 1):
            pins[f'T_bp0_{k}'] = period[k % len(period)]
        for k in range(meta['d']):
            pins[f'T_bdir0_{k}'] = word[k % len(word)]
        assert hashlib.sha256(json.dumps(pins, sort_keys=True).encode()).hexdigest() == row['pins_sha256']
        family_counts[meta['family']] += 1
    assert family_counts == {'RIGHT_SELF': 2555, 'LEFT_SUCCESSOR': 3745}

    for name, count, family in (('diagnostic.json', 2555, 'RIGHT_SELF'),
                                ('left_diagnostic.json', 3745, 'LEFT_SUCCESSOR')):
        data = read(name)
        assert data['status'] == 'COMPLETE' and data['cases'] == count
        assert data['root_claim_cases'] == count and data['unresolved_count'] == 0
        assert data['unresolved'] == [] and data['cpu_seconds'] < 120
        rows = [r for r in proof['rows'] if r['family'] == family]
        assert len(data['rows']) == len(rows)
        for diag, row in zip(data['rows'], rows):
            for k in ('h', 'bits', 'd'):
                assert diag[k] == row[k]
            if family == 'LEFT_SUCCESSOR':
                for k in ('s', 'zero_mode', 'target', 'claimant'):
                    assert diag[k] == row[k]
                assert diag['root'] == row['target'] and diag['root_claims']
            else:
                assert diag['kind'] == 'ROOT_CLAIM' and diag['claims']
    probe = read('left_successor_probe.json')
    assert probe['status'] == 'COMPLETE' and probe['cases'] == len(probe['rows']) == 40
    assert probe['valid_negative_edges'] == 0 and probe['edges'] == []

    static = read('static_partition.json')
    assert static['status'] == 'COMPLETE' and static['cpu_seconds'] < 120
    for k, v in {'core_trees': 4862, 'single_phantom_source_models': 48620,
                 'target_queries': 437580, 'compatible_queries': 43758,
                 'rejected_queries': 393822, 'original_verify_bpath_checks': 6916}.items():
        assert static[k] == v
    assert static['families'] == {'RIGHT_SELF': 24310, 'LEFT_SUCCESSOR': 19448}
    assert static['compatible_queries'] + static['rejected_queries'] == static['target_queries']
    assert len(static['positive_control_sources']) == 14

    controls = read('full_high_controls.json')
    assert controls['status'] == 'COMPLETE' and controls['cpu_seconds'] < 120
    assert controls['queries'] == len(controls['records']) == 39
    assert controls['valid_edges'] == 21 and controls['rejected_negative_candidates'] == 18
    assert controls['potential_violations'] == 0
    for r in controls['records']:
        assert r['source_valid'] and r['path_valid']
        assert r['high_root'] == r['expected']
        assert r['q'] == r['d'] // 2 and r['w'] == 6 - r['q']
        for field, name in (('source', 'phi_source'), ('destination', 'phi_destination')):
            m = r[field]
            assert r[name] == -3 * int(m['kr'][8] == 0 and m['rr'][8] == 19)
        if r['high_root']:
            assert r['potential_checked'] and r['reduced_cost'] >= 0
            assert r['reduced_cost'] == r['w'] - (r['phi_destination'] - r['phi_source'])
        else:
            assert r['forced_final_root_claims'] and r['d'] >= 14
    boundaries = [r for r in controls['records'] if r['label'].startswith('potential_boundary_clean_h0')]
    assert len(boundaries) == 2
    for r in boundaries:
        assert r['source']['root'] == r['destination']['root'] == 8
        assert r['w'] == -3 and r['phi_source'] == 0 and r['phi_destination'] == -3

    checked_hashes = 0
    manifest_path = HERE / 'manifest.json'
    if manifest_path.exists():
        manifest = read('manifest.json')
        for collection in ('files', 'frozen_dependencies', 'baseline_preservation'):
            for row in manifest[collection]:
                assert digest(ROOT / row['path']) == row['sha256'], row['path']
                checked_hashes += 1
    print(json.dumps({'status': 'PASS', 'symbolic_rows_audited': 6300,
                      'right_rows': family_counts['RIGHT_SELF'],
                      'left_rows': family_counts['LEFT_SUCCESSOR'],
                      'controls_audited': 39, 'python_files_parsed': len(parsed),
                      'manifest_hashes_checked': checked_hashes,
                      'note': 'Provenance audit; symbolic reductions are certified by the completed production-DAG run.'}))


if __name__ == '__main__':
    main()
