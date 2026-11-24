"""Seal the exact auxiliary result; never infer a residual from a screen.

--verify-only is read-only. Writer mode is for an unsealed reproduction only.
"""
from base3 import *
from physical1 import Edges
from model0 import prefix_check
from gate1 import signature, packets
import gc

MANIFEST = 'M1_CONT03_DELIVERY_MANIFEST.json'
PROOFS = [
    'PRE_EXECUTION.md', 'PACKING_BEFORE.md', 'PROTECTED_REPAIR_BEFORE.md',
    'GATE1_EXACT_REDUCTION.md', 'PACKET_PACKING_REFUTATION.md',
    'SAFE_REPAIR_LEMMAS.md', 'GATE3_PRIMITIVE_HYBRID_LINK.md',
    'HYBRID_EXCLUSION_AUDIT.md', 'GLOBAL_ACCOUNTING.md', 'PROOF_LEDGER.md',
    'FINAL_REPORT.md', 'INDEPENDENT_VERIFICATION.md', 'REPRODUCTION.md',
    'ADMINISTRATIVE_FAILURES.md',
]


def inventory():
    return {p.relative_to(ROOT).as_posix(): hfile(p)
            for p in ROOT.rglob('*') if p.is_file() and p.name != MANIFEST}


def verify_only():
    sealed = load(ROOT / MANIFEST)
    assert inventory() == sealed['files'], 'Delivery inventory or digest mismatch'
    assert preserve() == load(ROOT / 'INPUT_MANIFEST.json')
    assert sealed['principal_result'] == 'E — EXACT AUXILIARY REFUTATION'
    assert sealed['full_M1'] == 'OPEN'
    print('PASS read-only exact delivery, all inherited seals, HEAD and tracked files; '
          f"{len(sealed['files'])} files. Result E; full M1 OPEN.", flush=True)


def verify_physical(s, p):
    """Separate edge/mask recheck of every bit, signed SET, and full boundary."""
    assert digest(s) == p['source_sha256']
    assert p['original_S'] == p['original_genuine_M'] == list(range(1, s['n'] + 1))
    pool = p['state_pool']
    assert pool['all_complete_operation_states_checked_against_immutable_engine']
    assert pool['all_S_carrier_SETS_checked_at_every_actor_boundary']
    assert pool['original_event_sha256'] == digest(p['events'])
    aa, bb = Edges(s['initial_A']), Edges(s['initial_B'])
    initial = aa.code(), bb.code()
    assert len(p['boundaries']) == len(s['operations'])
    ds = {tuple(z['parent']): z for z in p['doubles']}
    byh = defaultdict(list)
    for v, d in ds.items(): byh[v[0]].append((v, d))
    A = Q = bits = splitbits = internals = 0
    extreme = 1 | (1 << (s['n'] - 1))
    forbidden = set(s.get('protected_labels', []))
    for h, (row, (tag, x)) in enumerate(zip(p['boundaries'], s['operations']), 1):
        assert (row['t'], row['tag'], row['x']) == (h, tag, x)
        assert aa.code() == int(pool['states'][row['pre_A_state']], 16)
        assert bb.code() == int(pool['states'][row['pre_B_state']], 16)
        apath = aa.path(x)
        assert apath == row['A_path'] and row['a'] == len(apath) // 2
        expected_abits = len(apath) - 1
        assert row['post_A_time'] - row['start_time'] == expected_abits
        # A's phase does not change B: check pre-B data even when A has no bits.
        if tag == 'K':
            bpath = bb.path(x)
            assert bpath == row['B_path'] and (len(bpath) - 1) // 2 == row['q']
            for v, d in byh[h]: assert bb.m[d['g']] == d['F']
        for t in range(row['start_time'], row['end_time']):
            e = p['events'][t]
            assert e['time'] == t + 1 and e['id'][1] == h
            actor = 'A' if t < row['post_A_time'] else 'B'
            assert e['actor'] == e['id'][0] == actor and e['target'] == x
            tree, other = (aa, bb) if actor == 'A' else (bb, aa)
            before = set(tree.m[1:]) - {0}
            otherlabs = set(other.m[1:]) - {0}
            tree.step(e)
            after = set(tree.m[1:]) - {0}
            lost, created = before - after, after - before
            assert sorted(lost) == e['lost'] and sorted(created) == e['created']
            sign = (sum(v in otherlabs for v in lost) - sum(v in otherlabs for v in created)) if actor == 'A' else (
                sum(v not in otherlabs for v in created) - sum(v not in otherlabs for v in lost))
            assert sign == e['sign'] and tree.m[e['pivot']] == e['demoted_label']
            bits += 1
            if actor == 'A':
                assert not forbidden.intersection(after)
                if s['family'] == 'globally_internal_A_blind_column_fan':
                    assert e['external'] is None
                    assert all(v & extreme for v in after)
                    splitbits += 1
                internals += any(not v & extreme for v in after)
            if t + 1 == row['post_A_time']:
                assert aa.code() == int(pool['states'][row['post_A_state']], 16)
                if tag == 'K':
                    bpath = bb.path(x)
                    assert bpath == row['B_path'] and (len(bpath) - 1) // 2 == row['q']
                    for v, d in byh[h]: assert bb.m[d['g']] == d['F']
        # Zero-depth A phases have no primitive at their boundary.
        assert aa.code() == int(pool['states'][row['post_A_state']], 16)
        assert bb.code() == int(pool['states'][row['post_B_state']], 16)
        assert aa.root == x
        if tag == 'K': assert bb.root == x
        else: assert row['q'] == 0
        A += row['a']; Q += row['q']
    aa.recompute(); bb.recompute()
    assert (aa.code(), bb.code()) == initial
    assert bits == len(p['events'])
    return {'A': A, 'Q_B': Q, 'primitives': bits, 'splitvine_A_bits': splitbits,
            'internal_A_label_snapshots': internals}


def verify_new_sources():
    fresh = []; critical_example = None
    for stem in ('NEW', 'PROTECTED'):
        sources = load(ROOT / f'{stem}_SOURCE_CATALOG.json')
        results = load(ROOT / f'{stem}_RESULTS.json')
        assert len(sources) == len(results) == 6
        for i, (s, row) in enumerate(zip(sources, results)):
            paths = {kind: ROOT / f'{stem}_{kind}_{i:02}.json' for kind in (
                'PHYS', 'FOREST', 'WEIGHTS', 'M1_AUDIT', 'BIRTH', 'ORDERED', 'REDUCTION')}
            p, f, w, an, b, acc, red = (load(paths[k]) for k in paths)
            assert row['source'] == s['name']
            assert digest(s) == row['source_sha256'] == b['source_sha256'] == acc['source_sha256']
            assert prefix_check(s) == row['prefix']
            physical = verify_physical(s, p)
            assert physical['A'] == row['A'] == an['A'] == b['A'] == acc['A']
            assert physical['Q_B'] == row['Q_B'] == an['Q_B'] == b['Q_B']
            assert physical['primitives'] == row['primitives'] == b['original_SET_and_sign_checks']
            if stem == 'NEW': assert physical['splitvine_A_bits'] == row['A_splitvine_primitives_checked']
            else: assert physical['internal_A_label_snapshots'] == row['A_internal_label_snapshots'] > 0
            assert an['primitive_edges_and_all_complete_boundaries_verified']
            assert set(tuple(z['parent']) for z in p['doubles']) == set(tuple(z['parent']) for z in f['vertices']) == set(tuple(z['parent']) for z in w['vertices'])
            assert f['root_donors_injective'] and f['vertex_count'] == row['Q_B']
            assert w['R_overflow'] == 0 and all(z['w'] == 0 for z in w['vertices'])
            r6 = {digest(e['rho']): e for e in b['original_R6']}
            star = acc['native_original_R_star']
            assert star == row['original_R_star'] and len(r6) == row['original_R6']
            for e in star:
                assert digest(e['rho']) in r6
                assert e['original_parent'] == r6[digest(e['rho'])]['parent']
            assigned = acc['disjoint_original_assignments']
            assert {k: len(v) for k, v in assigned.items()} == row['assigned_counts']
            assert assigned['skipped_rank'] == star
            assert all(not v for k, v in assigned.items() if k != 'skipped_rank')
            assert {digest(e['rho']) for e in acc['frozen_skipped_after_carrier_eligible']} == {digest(e['rho']) for e in star}
            assert not acc['C_old'] and not acc['E_old'] and not acc['exact_D'] and not acc['quota_rows']
            assert acc['actual_S_UU'] == 0
            assert acc['raw_periodic_certificate'] == row['raw_periodic_cost'] <= 10 * row['A']
            rebuilt = packets(s, p, b, f, an, acc['exact_D'], star)
            assert rebuilt == red and not red['literal_S_UU'] and red['sum_z_h'] == 0
            assert row['actual_S_UU'] == [] and row['sum_z_h'] == 0
            sig = signature(p, b, f, an)
            critical = sorted(v for v in sig if v[0] == 2)
            assert [list(v) for v in critical] == row['critical']['physical_silent_UU_parents']
            assert len(critical) == row['critical']['N_h'] == s['s'] // 2
            assert row['critical']['A_gap'] == 1 and not row['critical']['actual_D_parents']
            assert row['critical']['z_h'] == 0
            assert len(row['critical']['R6_parents']) >= s['s'] // 4
            assert {tuple(v) for v in row['critical']['R6_parents']} <= set(critical)
            assert {tuple(v) for v in row['critical']['R_star_parents']} <= set(critical)
            ref = {'source': s['name'], 'source_sha256': digest(s), 'source_catalog': f'{stem}_SOURCE_CATALOG.json',
                   'catalog_index': i, 'population': s['n'], 'operations': len(s['operations']),
                   'A': row['A'], 'Q_B': row['Q_B'], 'critical': row['critical'],
                   'original_R6_gaps': len(r6), 'native_R_star_gaps': len(star),
                   'frozen_assignment': 'Every original R_* gap assigned skipped-rank; no later duplicate assignment.',
                   'actual_D': [], 'sum_z_h': 0, 'literal_S_UU': [],
                   'certificates': {k: {'file': q.name, 'sha256': hfile(q)} for k, q in paths.items()},
                   'replay_scope': 'Full original mutable/immutable replay in writer; fresh edge/mask/signed-SET and complete-boundary check at seal.'}
            fresh.append(ref)
            if stem == 'NEW' and i == 1:
                ds = {tuple(z['parent']): z for z in p['doubles']}
                uu = {ast.literal_eval(k): v for k, v in b['U'].items()}
                depths = {tuple(z['vertex']): z for z in an['C_fringe_depths']}
                details = []
                for v in critical:
                    creator = tuple(uu[v]['creator'])
                    details.append({'original_parent': v, 'B_double': ds[v], 'physical_A_distance': depths[v],
                                    'pre_A_target_path': p['boundaries'][1]['A_path'],
                                    'original_U_data': uu[v], 'creator': creator,
                                    'creator_B_double': ds[creator], 'creator_original_U_data': uu[creator],
                                    'literal_R6_gaps': [e for e in b['original_R6'] if e['parent'] == list(v)],
                                    'native_R_star_gaps': [e for e in star if e['original_parent'] == list(v)],
                                    'actual_D_position': None})
                critical_example = {'principal_result': 'E — EXACT AUXILIARY REFUTATION',
                    'refuted_law': 'The exact inherited physical N_h <= 2 a_h',
                    'source': s, 'source_sha256': digest(s), 'complete_certificates': ref['certificates'],
                    'critical_KEEP': 2, 'A_gap': 1, 'physical_N_h': 8,
                    'distinct_current_original_R6_parents': row['critical']['R6_parents'],
                    'distinct_current_native_R_star_parents': row['critical']['R_star_parents'],
                    'parents': details, 'frozen_skipped_rank_records': acc['frozen_skipped_after_carrier_eligible'],
                    'actual_D': [], 'actual_z_h': 0, 'literal_S_UU': [],
                    'parameterized_law': 'For every s>=8 divisible by4, N_h=s/2 at a_h=1; at least s/4 genuine original R6 parents.',
                    'not_refuted': ['Actual z_h=0 universally', 'Aggregate sum z_h=O(A)', 'Four-way frontier including comparison/global A alternatives']}
            del p, f, w, an, b, acc, red, sig
            gc.collect()
    assert len(fresh) == 12 and max(z['population'] for z in fresh) == 134
    assert critical_example and len(critical_example['distinct_current_native_R_star_parents']) == 5
    write('EXACT_PACKING_COUNTEREXAMPLE.json', critical_example)
    return fresh


def verify_controls():
    catalog = load(ROOT / 'CONTROL_REFERENCE_CATALOG.json')
    ranks = load(ROOT / 'LCA_RANK_RESULTS.json')
    assert len(catalog) == len(ranks) == 80
    inherited = []
    for i, (e, r) in enumerate(zip(catalog, ranks)):
        assert r['index'] == i and e['source']['name'] == r['source']
        assert digest(e['source']) == e['source_sha256'] == r['source_sha256']
        assert r['cyclic_signed_q_change'] == 0
        assert r['raw_periodic_cost'] <= 2 * r['real_A_bits'] + r['Lambda_A'] <= 4 * r['A'] + r['Lambda_A']
        if r['Lambda_A'] == 0: assert r['raw_periodic_cost'] <= 3 * r['A']
        assert r['lambda_le_6A_implies_periodic_paid'] == (r['Lambda_A'] <= 6 * r['A'])
        if e['physical']: assert hfile(e['physical']) == e['physical_sha256']
        for k, sha in e.get('sealed_input_hashes', {}).items(): assert hfile(e[k]) == sha
        if e['origin'] == 'C3_NEW': assert r['Lambda_A'] == 0
        if e['origin'] == 'C3_PROTECTED': assert 0 < r['Lambda_A'] <= 6 * r['A']
        if not e['origin'].startswith('C3_'):
            ref = {'source': r['source'], 'source_sha256': r['source_sha256'],
                   'full_source_catalog': 'CONTROL_REFERENCE_CATALOG.json', 'catalog_index': i,
                   'origin': e['origin'], 'original_physical_file': e['physical'],
                   'original_physical_sha256': e['physical_sha256'],
                   'current_check': r['physical_scope'],
                   'prior_predicate_scope': 'Inherited exact original predicates/certificates remain pinned; no new native R_* run inferred from this rank audit.'}
            if e.get('expansion'):
                ref['expansion_files'] = {q: {'path': str(C2 / q), 'sha256': hfile(C2 / q)} for q in (
                    'BOOST_SHORT_PHYS.json', 'BOOST_EVENT_EXPANSION.json', 'expand_events2.py')}
            inherited.append(ref)
    assert len(inherited) == 68
    long = next(z for z in ranks if z['origin'] == 'C2_boost_long')
    assert (long['A'], long['Lambda_A'], long['raw_periodic_cost']) == (314555, 2875227, 3145551)
    return inherited, ranks


def verify_gate1_and_exposure():
    g = load(ROOT / 'GATE1_AUDIT.json')
    assert g['weighted_identity_passed'] and not g['packing_proved'] and not g['positive_S_UU_claimed']
    assert len(g['exact_source_packet_audits']) == 7 and g['D_gaps_total'] == 36
    for r in g['exact_source_packet_audits']:
        assert not r['literal_S_UU'] and r['sum_z_h'] == 0
        assert sum(sum(z['fiber_weights'].values()) for z in r['packets']) == len(r['literal_D_original_rho'])
        for z in r['packets']:
            assert all(1 <= v <= 3 for v in z['fiber_weights'].values())
            assert len(z['Z_h']) == z['z_h'] and z['z_h'] <= z['weighted_S_UU'] <= 3 * z['z_h']
    repairs = load(ROOT / 'FAN_EXPOSURE_REPAIR.json')
    assert len(repairs) == 2
    for e, n in zip(repairs, (8, 16)):
        assert e['entire_B_word_and_all_B_double_shapes_equal'] and len(e['creator_repairs']) == n
        for row in e['creator_repairs']:
            assert row['new_creator_class'] == 'U' and row['exposure_before_B_birth']
            assert row['old_cyclic_kappa'] < row['old_donor_lift'] < row['old_cyclic_Gamma']
    tickets = load(ROOT / 'CONSTRUCTED_PACKET_CLOSURE_TICKETS.json')
    assert len(tickets) == 12
    for e in tickets:
        assert e['tracked_packet_only'] == 2 and e['maximum_parent_load_per_actual_A_StepEv'] == 1
        assert len({tuple(z['future_measured_A_demotion']) for z in e['tickets']}) == len(e['tickets'])
    return {'exact_original_D_sources': 7, 'exact_original_D_gaps': 36,
            'old_fan_creator_repairs': 24, 'constructed_packet_ticket_sources': 12,
            'tickets_universal': False}


def seal():
    assert not (ROOT / MANIFEST).exists(), 'Never overwrite a sealed checkpoint; use a fresh sibling.'
    t0 = time.process_time(); wall0 = time.perf_counter()
    receipt = 'CPU_finalization.json'; i = 2
    while (ROOT / receipt).exists(): receipt = f'CPU_finalization_{i}.json'; i += 1
    success = False
    try:
        assert preserve() == load(ROOT / 'INPUT_MANIFEST.json')
        for name in PROOFS: assert (ROOT / name).is_file(), name
        for q in ROOT.glob('*.py'): ast.parse(q.read_text(encoding='utf-8-sig'), filename=q.name)
        fresh = verify_new_sources()
        inherited, rank_rows = verify_controls()
        gate = verify_gate1_and_exposure()
        assert preserve() == load(ROOT / 'INPUT_MANIFEST.json')
        write('SOURCE_WITNESSES.json', {'fresh_complete_original_sources': fresh,
            'inherited_complete_original_controls': inherited,
            'full_source_words': 'Referenced catalogs contain complete labelled initial trees, actual measured operations and legal excluded prefixes.',
            'long_control_scope': 'Lossless C2 original-event expansion; no new long native Pi/R_* replay claimed.',
            'finite_checks_are_universal_proof': False})
        verification = {'principal_result': 'E — EXACT AUXILIARY REFUTATION', 'full_M1': 'OPEN',
            'exact_inherited_physical_N_h_bound': 'REFUTED',
            'parameterized_local_ratio': 'N_h/a_h=s/2 for every s>=8 divisible by4',
            'actual_posthybrid_survivor_certified': False, 'new_universal_K_UU': None,
            'new_approved_transfer_X': None, 'original_interface_changed': False,
            'fresh_complete_sources': len(fresh), 'fresh_max_population': max(z['population'] for z in fresh),
            'new_rank_law_source_audits': len(rank_rows), 'inherited_rank_law_controls': len(inherited),
            'fresh_all_original_R_star_assigned_frozen_skipped_rank': True,
            'fresh_literal_D_gaps': 0, 'fresh_literal_S_UU_gaps': 0,
            'gate1': gate, 'primitive_rank_hybrid_theorem': 'raw <= 4A + Lambda_A; Lambda_A<=6A eliminates via EXISTING hybrid certificate',
            'unpriced_Lambda_A_is_A_credit': False,
            'first_missing_implication': 'All original F/E_old/G/H/local/quota failures for an actual late sigma parent imply earlier payment or a physical A obligation with absolute global load.',
            'verification_scope': 'Same agent, separate engines/implementations; no external reviewer or formal-kernel certification.',
            'preservation': load(ROOT / 'INPUT_MANIFEST.json')}
        write('FINAL_VERIFICATION.json', verification)
        success = True
    finally:
        write(receipt, {'completed': success, 'cpu_seconds': time.process_time() - t0,
            'wall_seconds': time.perf_counter() - wall0,
            'memory': prev.prev.base0.old.inherited.memory(),
            'scope': 'Seal consistency checks, full new edge/mask/signed SET replay, prefixes, original packet and transitive preservation checks; import time excluded.'})
    receipts = {q.name: load(q) for q in ROOT.glob('CPU_*.json')}
    failed = [n for n, z in receipts.items() if not z['completed']]
    assert failed == ['CPU_gate1_exact_packet_reduction.json'], failed
    cpu = sum(z['cpu_seconds'] for z in receipts.values())
    peak = max(z['memory']['peak_working_set_bytes'] for z in receipts.values())
    assert cpu <= 1200 and peak < 2 * 1024 ** 3
    write('RESOURCE_RECORD.json', {'allocation': {'measured_script_CPU_seconds': 1200,
        'fresh_complete_source_cap': 12, 'fresh_population_cap': 1027,
        'per_process_peak_working_set_aim_bytes': 2 * 1024 ** 3},
        'measured_script_CPU_seconds_total': cpu, 'maximum_measured_process_peak_working_set_bytes': peak,
        'receipts': receipts, 'fresh_complete_sources': 12, 'fresh_max_population': 134,
        'unmetered': ['Module imports before meters', 'Read-only source and schema inspections, including a truncated oversized catalog print',
            'Proof reasoning, prose and patch construction', 'Final JSON/manifest serialization and read-only seal verification'],
        'resource_numbers_are': 'Measured script scope only; not a total wall-time or full reasoning CPU claim.',
        'failed_semantic_or_source_run': False,
        'administrative_failure': 'Original gate1 tuple/list representation comparison; retained and corrected in gate1_v2 with no changed selector.',
        'agents_or_external_reviewers_used': 0, 'installations': 0, 'Git_mutations': 0,
        'historical_writes': 0, 'all_caps_operational_not_mathematical': True})
    write(MANIFEST, {'principal_result': 'E — EXACT AUXILIARY REFUTATION', 'full_M1': 'OPEN',
        'format': 'Exact full relative file inventory with SHA256; excludes only this manifest.',
        'inherited_C2_manifest_sha256': hfile(C2 / 'M1_CONT02_DELIVERY_MANIFEST.json'),
        'files': inventory()})
    print(f'PASS sealed {len(inventory())} files; 12 fresh complete sources; '
          f'{cpu:.3f} measured script CPU seconds. Result E; full M1 OPEN.', flush=True)


if __name__ == '__main__':
    if sys.argv[1:] == ['--verify-only']: verify_only()
    else:
        assert not sys.argv[1:]
        seal()
