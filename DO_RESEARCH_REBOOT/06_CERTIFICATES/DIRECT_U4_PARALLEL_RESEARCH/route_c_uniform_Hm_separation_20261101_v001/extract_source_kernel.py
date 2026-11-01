"""Extract fixed source identities for an all-m proof; no new m replay.

Only P, one already recorded W, and X are inspected in both orientations.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
NI = HERE.parent / 'route_c_nowhere_immediate_residual_20261101_v001'
CA = HERE.parent / 'route_c_102_cut_protocol_audit_20261101_v001'
STAGE = ROOT / 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'


def read(p):
    return json.loads(p.read_text(encoding='utf-8'))


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def save(name, value):
    with (HERE / name).open('x', encoding='utf-8') as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
        f.write('\n')


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def path(tree, key):
    nodes, dirs = [], []
    while tree:
        nodes.append(tree[0])
        if tree[0] == key:
            return nodes, dirs
        side = 'L' if key < tree[0] else 'R'
        dirs.append(side)
        tree = tree[1 if side == 'L' else 2]
    raise AssertionError('present active key')


def depth(tree, key):
    return len(path(tree, key)[1])


def frame_profile(tree, x, y):
    px, dirs = path(tree, x)
    py, _ = path(tree, y)
    h, d, common = len(py)-1, len(dirs), 0
    while common < min(len(px), len(py)) and px[common] == py[common]:
        common += 1
    ops = []
    for t in range(d//2):
        top = d-2*(t+1)
        ops.append(dict(case=''.join(dirs[top:top+2]), site_depth=top,
            grandparent=px[top], parent=px[top+1]))
    if d % 2:
        ops.append(dict(case='ZIG', site_depth=0, grandparent=px[0], parent=None))
    entry = next(i for i, op in enumerate(ops) if op['site_depth'] <= common-1)
    role = 'parent' if y == ops[entry]['parent'] else 'other'
    mu = 0 if role == 'parent' else (1 if ops[entry]['case'] == 'ZIG' else 2)
    later = [op for op in ops[entry+1:] if op['case'] != 'ZIG']
    r = len(later)
    matching = sum(op['case'] == ('LL' if y < x else 'RR') for op in later)
    return dict(h=h, access_depth=d, lca_depth=common-1, operations=ops, entry_operation=entry,
        entry_role=role, mu=mu, outer_doubles=r, matching_outer_doubles=matching,
        U=min(h+2, max(0, h+mu-r-matching)))


def main():
    inherited = read(CA / 'entry_source_pins.json')
    pins = dict(inherited['files'])
    for rel, h in pins.items():
        assert sha(ROOT / rel) == h, rel
    for p in HERE.parent.rglob('*'):
        if p.is_file() and HERE not in p.parents:
            pins[p.relative_to(ROOT).as_posix()] = sha(p)
    stage = {p.relative_to(STAGE).as_posix(): sha(p) for p in STAGE.rglob('*') if p.is_file()}
    assert stage == inherited['stage_files'] and len(stage) == 125
    assert (git('rev-parse', 'HEAD'), git('branch', '--show-current'),
        git('status', '--porcelain=v1', '--untracked-files=no')) == (inherited['head'], inherited['branch'], '')
    save('entry_source_pins.json', dict(date='2026-11-01', files=pins, stage_files=stage,
        head=inherited['head'], branch=inherited['branch'], tracked_status='',
        gate_sha256=sha(HERE / 'UH00_FOUR_RULE_GATE.md')))
    for name, h in read(CA / 'delivery_manifest.json')['files'].items():
        assert sha(CA / name) == h
    old_audit = read(CA / 'independent_audit.json')
    ni_audit = read(NI / 'independent_audit.json')
    assert old_audit['status'] == ni_audit['status'] == 'PASS'
    assert ni_audit['full_source_replays_sha256'] == sha(NI / 'full_source_replays.json')
    identity = read(NI / 'uniform_nowhere_identity.json')
    assert identity['status'] == 'PROVED—RESTRICTED DOMAIN'
    assert identity['paired_closed'] and identity['nowhere_diagonal']
    replay = read(NI / 'full_source_replays.json')
    kernels, matrices, frames = {}, {}, {}
    for orient, field in [('normal', 'cycle'), ('reflected', 'mirrored_cycle')]:
        rows = replay[field]
        kernel = dict(P=rows[:8], W=rows[8:25], X=rows[-9:])
        P, W, X = kernel['P'], kernel['W'], kernel['X']
        assert (len(P), len(W), len(X)) == (8, 17, 9)
        for phase in kernel.values():
            for i, row in enumerate(phase):
                assert row['a'] == (depth(row['source_A'], row['key'])+1)//2
                assert 1 <= row['a'] <= 3 and row['d_A'] <= 6
                assert row['source_A'] != row['source_B'] and row['destination_A'] != row['destination_B']
                if i:
                    assert phase[i-1]['destination_A'] == row['source_A']
                    assert phase[i-1]['destination_B'] == row['source_B']
                if row['mode'] == 'KEEP':
                    assert row['d_B'] > 0
                else:
                    assert row['source_B'] == row['destination_B'] and row['a'] == 1
        for left, right in [(P, W), (W, W), (W, X), (X, P)]:
            assert left[-1]['destination_A'] == right[0]['source_A']
            assert left[-1]['destination_B'] == right[0]['source_B']
            assert left[-1]['key'] != right[0]['key']
        assert [i for i, row in enumerate(W) if row['delta'] > 0] == [9]
        assert all(row['delta'] <= 0 for row in P+X)
        assert (W[9]['a'], W[9]['q'], W[10]['a'], W[10]['q'], W[11]['a'], W[11]['q']) == (1, 3, 1, 2, 1, 1)
        assert sum(row['mode'] == 'KEEP' for row in P) == 6 and len(X) == 9
        anchor_post = W[9]['destination_B']
        matrix = []
        for k, row in enumerate(W[10:17]):
            h = depth(anchor_post, row['key'])
            c, C = h//2+k, 2*row['a']
            assert c >= C and row['q'] <= C
            matrix.append(dict(W_slot=10+k, key=row['key'], a=row['a'], q=row['q'],
                h=h, k=k, UD_ceiling=c, capacity=C, slack=c-C))
        fp = frame_profile(W[10]['source_B'], W[10]['key'], W[11]['key'])
        assert W[10]['source_B'] == anchor_post
        assert [op['case'] for op in fp['operations']] == [e[0] for e in W[10]['B_events']]
        assert (fp['h'], fp['entry_role'], fp['mu'], fp['outer_doubles'], fp['matching_outer_doubles'], fp['U']) == (3, 'parent', 0, 1, 0, 2)
        assert depth(W[10]['destination_B'], W[11]['key']) <= fp['U']
        kernels[orient], matrices[orient], frames[orient] = kernel, matrix, fp
    save('fixed_source_kernel.json', dict(status='SOURCE-EXACT extraction only',
        source_replay_sha256=sha(NI / 'full_source_replays.json'),
        uniform_source_identity_sha256=sha(NI / 'uniform_nowhere_identity.json'),
        inherited_protocol_audit_sha256=sha(CA / 'independent_audit.json'),
        gate_sha256=sha(HERE / 'UH00_FOUR_RULE_GATE.md'), kernels=kernels,
        original_source_ranges=dict(P=[0,7], W=[8,24], X=[93,101]),
        new_m_values_replayed=0, new_source_engine_calls=0, larger_finite_fits=0))
    save('uniform_proof_certificate.json', dict(status='PROVED—RESTRICTED DOMAIN; analytic proof supplied in UH01',
        quantifiers='every integer m>=5, every untouched BST fringe F>7 including empty, both orientations',
        source_kernel_sha256=sha(HERE / 'fixed_source_kernel.json'),
        short_lag_UD_cases=matrices, FI_source_frame=frames,
        active_core_keys=7, maximum_A_depth=6, maximum_KEEP_capacity=6,
        exhaustive_payer_cases=['k>=7 gives cUD>=7>6>=2a',
            '0<=k<=6 is exactly W slots10..16 of same copy'],
        all_KEEP_B_changes=True, phase_B_changes=dict(P=6,W=17,X=9),
        only_positive_phase='W', positive_W_slot=9,
        successive_anchor_B_change_gaps=dict(internal_repeat=17, wrap_through_X_P=32),
        UD_KEEP_lending_impossible=True, UD_total_lendable_DELETE_capacity=4,
        UD_debts='m', UD_final_debt_lower_bound='m-4',
        UD_cut0_final_debt='m', UD_cut2_final_debt='m-4', UD_accepted_cuts=0,
        FI_latest_KEEP5_fact=dict(h=3,k=1,U=2,ceiling=1,capacity=2,own_q=1),
        FI_older_KEEP5_facts='same T and first KEEP4; k>=1, cFI=k>=1',
        FI_immediate_KEEP4_latest_fact=dict(h=4,k=0,ceiling=2,capacity=2,own_q=2),
        FI_immediate_KEEP4_older_facts='k>=17, U(4,4)=0, cFI=k-1>=16',
        FI_local_debt_recurrence=[0,1,1,0],
        positive_occurrence='i_r=17+17r, 0<=r<m',
        symbolic_residual_demand='(0,i_r,2)', symbolic_donor_unit='(0,i_r+2,0,1)',
        total_blocks='17+17m', FI_rejected_cuts='{18+17r,19+17r:0<=r<m}',
        FI_rejected_count='2m', FI_rejected_final_debt=1, FI_accepted_count='17+15m',
        FI_canonical_accepted_cut=0, FI_cut0_distinct_demand_assignments='18+16m',
        FI_DELETE_or_startup_units_used=0, reused_units=0, periods_per_cut=1,
        exact_three_block_supports_disjoint=True, new_m_values_replayed=0,
        new_source_engine_calls=0, larger_finite_fits=0,
        matching_terminal_line='FROZEN', universal_CD='OPEN', automatic_successor_launched=False))
    print(json.dumps(dict(status='SOURCE_KERNEL_AND_UNIFORM_PROOF_IDENTITIES_PASS',
        short_lag_cases=matrices['normal'], source_frame=frames['normal'],
        phase_B_changes=dict(P=6,W=17,X=9), preserved_files=len(pins),
        new_m_values_replayed=0, larger_finite_fits=0), indent=2))


if __name__ == '__main__':
    main()
