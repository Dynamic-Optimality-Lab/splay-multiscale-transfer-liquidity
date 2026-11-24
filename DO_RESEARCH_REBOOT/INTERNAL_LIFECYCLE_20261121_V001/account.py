"""Literal-occurrence lifecycle maps and frozen-potential restoration ledger."""
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    assert not (HERE/'FINAL_MANIFEST.json').exists()
    results, probes = [], []
    for file in sorted(HERE.glob('*_complete_witness.json')):
        w = json.loads(file.read_text(encoding='utf-8'))
        s = w['source']
        owners, mapping, loads, packets = set(), [], Counter(), []
        for packet in sorted(w['packets'], key=lambda p: p['initial_KEEP']):
            demands = [z for z in packet['lifecycle_U_ids'] if tuple(z) not in owners]
            seeds = packet['seeds']
            cap = (len(demands)+len(seeds)-1)//len(seeds)
            for i, dem in enumerate(demands):
                ticket = seeds[i//cap]
                assert tuple(dem) not in owners
                owners.add(tuple(dem))
                mapping.append({'demand': dem, 'packet': packet['initial_KEEP'], 'birth': ticket['birth'], 'A_payment': ticket['A_payment']})
                loads[tuple(ticket['A_payment'])] += 1
            packets.append({'initial_KEEP': packet['initial_KEEP'], 's': len(seeds), 'C': packet['critical_bound'],
                            'critical_U': len(packet['critical_U_ids']), 'restoration_Q': packet['restoration_Q'],
                            'lifecycle_U': len(demands), 'finite_capacity': cap})
        actual_u = {tuple(z['id']) for z in w['all_B_double_records'] if z['U_int']}
        assert owners <= actual_u
        if not s.get('helpers') and not s.get('altered_restore'):
            assert owners == actual_u
        phase = defaultdict(Counter)
        for e in w['real_rotations']:
            ph = w['rows'][e['id'][1]-1]['phase']
            phase[ph][e['id'][0]+'_phi_delta'] += e['phi_delta']
        results.append({'witness': file.name, 'sha256': hashlib.sha256(file.read_bytes()).hexdigest(),
                        'packets': packets, 'literal_lifecycle_U_charge_map': mapping,
                        'covered_U': len(owners), 'literal_complement_U': sorted(actual_u-owners),
                        'maximum_finite_A_load': max(loads.values(), default=0),
                        'phase_potential_ledger': dict(phase)})
        if s['mode'] == 'I' and s['q'] == 5 and s['d'] == 1 and not s.get('helpers'):
            p = s['p']
            for probe in w['result']['potential_probes']:
                assert probe['B_phi_delta'] == p+1 and probe['u'] == (p+1)//2
                assert probe['B_decreases'] == 2+int(p % 2 == 0) and probe['A_gap'] == probe['a'] == 1
                op = probe['operation']
                bevents = [e for e in w['real_rotations'] if e['id'][0] == 'B' and e['id'][1] == op]
                removed_m = [e for e in bevents if e['removed'][1]-e['removed'][0]+1 >= 3 and not ((e['removed'][1]-e['removed'][0]+1) & (e['removed'][1]-e['removed'][0]+2))]
                created_m = [e for e in bevents if e['created'][1]-e['created'][0]+1 >= 3 and not ((e['created'][1]-e['created'][0]+1) & (e['created'][1]-e['created'][0]+2))]
                assert not created_m and len(removed_m) == p+1
                assert sorted(e['removed'][1]-e['removed'][0]+1 for e in removed_m) == [(1 << h)-1 for h in range(2, p+3)]
                probes.append({'witness': file.name, 'p': p, 'n': s['n'], **probe,
                               'removed_Mersenne_original_event_ids': [e['id'] for e in removed_m],
                               'all_original_B_events_in_recharge': bevents})
    (HERE/'LIFECYCLE_MAPS.json').write_text(json.dumps({'sources': results, 'note':'Finite capacities are recorded separately from the theorem constant. The uniform upper bound is proved symbolically.'}, indent=2), encoding='utf-8')
    (HERE/'RESTORATION_RECHARGE.json').write_text(json.dumps({'frozen_quantity':'Phi_M from prior H3q checkpoint, unchanged', 'probes': probes}, indent=2), encoding='utf-8')
    certificate = {
        'status':'PROVED—RESTRICTED DOMAIN; same-agent symbolic proof in Notion, independent exact-event code audit',
        'domain':'Admissible exactly paired-closed original sources with S=M=X and canonical decorated whole-carrier prefixes. Both reflections. Outside this domain the named class is empty; no assertion that the whole original residual lies in it.',
        'parameters':'n=2^d(r+3)-3, d=v2(n+3)-2>=1, r>=9, r=1 mod8, c_d=2^(d+1)-1. p,q>=1 and r=2^(p+1)(q+1)+1.',
        'mechanism':'Every qualified prefix creates s fresh actual B SET labels of cardinality c_d. Distinct starts give distinct birth occurrence IDs. In one source c_d is fixed. Each birth maps injectively through cyclic first hit to an actual cost-one A StepEv in its incoming original KEEP gap.',
        'seed_count':'s=2^(p-1)(2q+1)+1',
        'critical_RR_count':'C=(2^p-1)(q+1)-p',
        'critical_all_double_count':'r-q-2',
        'exact_slack_identities':{'4s-3C':'2^p(q-1)+3q+3p+7>0','8s-3r':'2^(p+1)(q-1)+5>0'},
        'critical_U_theorem':{'quantity':'R_crit = union of literal original U_int IDs in recognized critical prefixes; maximal p selected once per initial KEEP', 'bound':'R_crit <= (4/3)A', 'real_A_map_maximum_load':2,'external_scan_dependency':False},
        'lifecycle_U_theorem':{'quantity':'R_life = R_crit plus literal original U_int IDs in immediate certified I or J restoration words; assign each once to earliest containing initial KEEP', 'bound':'R_life <= ((4+8*C_seq)/3)A <=4*C_seq*A', 'integer_A_load':'ceil((4+8*C_seq)/3), or 4*ceil(C_seq)', 'C_seq':'The inherited classical full sorted-scan B-double constant, absolute and >=1; no new numerical value claimed.'},
        'direct_Q_corollary':{'quantity':'All literal original B doubles in certified prefix+restoration words, deduplicated', 'bound':'Q_packet <= (8/3)(1+C_seq)A <= 6*ceil(C_seq)A', 'complete_I_J_family':'For W=(I_(p,q,d))^m Z_d or (J_(p,q,d))^m Z_d without extra helpers, all U_int is R_life and Q_B(W)<=((8/3)(1+C_seq)+1)A(W). Outer Z_d starts common and is all KEEP; its original Q cost is charged with one additional A load.'},
        'new_scope':'Arbitrary A helper history and arbitrary continuation after critical prefixes; globally composed packet birth-run accounting, deeper ballast, reverse-only restoration. The old literal I reverse-zig injection and its earlier ratio theorem are preserved, not presented as new.',
        'restoration_identity':{'source':'Complete I_(p,5,d=1)^m Z_1, m>=2, choose first forward KEEP6 in copy2, original operation6r', 'for_all':'p>=1', 'Delta_B_Phi_M':'p+1', 'u':'ceil(p/2)', 'd_B':'2+1[p even]', 'incoming_A_gap':1,'explanation':'All p+1 nested old Mersenne labels are unmatched and contain the target; the splay removes them and creates no Mersenne label. Thus the negative mismatch potential recharges linearly in depth during one cheap A gap.'},
        'finite_inventory_obstruction':{'claim':'For any fixed cardinality cutoff c, no fixed multiple of all original B births of sizes<=c plus an m-independent initial inventory controls all U_int in these repeated no-leaf families.', 'construction':'Use r=9,p=q=1, choose d with 2^(d+1)-1>c. Every inner B birth has size at least c_d and each copy after the first contributes a genuine original U_int demand. Only fixed outer Z_d contributes births<=c. Let m grow.', 'not_refuted':'Adaptive one-layer theorem above; it explicitly selects c_d from full carrier size and counts renewed birth IDs.'},
        'literal_complement':'Original U_int IDs outside the recognized canonical whole-carrier prefixes and immediate certified restoration words. Includes arbitrary B restoration traffic, other carrier geometries, and unresolved simultaneous packet scales within a source.',
        'budget_composition':'The critical and lifecycle maps are alternative maps, not added on the same demand. If combined with a previously frozen paid class, apply the new map only to its literal complement and add the proved maximum A load. No UF coefficient is recomputed without the frozen original-ID partition.',
        'not_proved':['Universal U_int=R_life','Source-uniform bound on all arbitrary restoration traffic','Strict enlargement of the frozen actual UF hard paid class','Universal Coarse Double','Dynamic Optimality'],
        'before':'Internal nonleaf witnesses exist; literal I critical reverse-zig map and whole-family bounded ratio already proved. All-scale signed mismatch potential fails at restoration.',
        'after':'New explicit globally bounded packet-to-nonleaf-birth-run A map, including arbitrary A helpers/continuation and certified alternate restoration. A fixed finite-cardinality inventory is insufficient, but one canonical adaptive layer suffices for the named class.',
        'proof_dependency_chain':['Full physical E commutes with every active-target primitive rotation','Dyadic comb induction counts seeds and critical doubles','Cyclic fixed-cardinality first-hit injection into real A gap StepEv','Exact packet size inequalities and original-ID deduplication','Classical full sorted-scan theorem for the optional restoration extension'],
        'graph_edge':'canonical internal-renewal packets -> same-cardinality birth runs -> real original A work. Unresolved complement still feeds the global nested-path/renewal obstruction.'}
    certificate.update(
        proof_url='https://app.notion.com/p/41e6251839be81e58078e7d4ebcb3986',
        exact_assignment_rule='Choose earliest containing original initial-KEEP ID. Sort assigned original demand IDs ascending. Sort packet seeds by increasing base g, equivalently decreasing initial maximum RR-step. Critical map uses two slots per seed. Lifecycle map computes a_P=ceil(D_P/s_P) (zero for no demands) and assigns demand i to seed floor(i/a_P); the uniform proof bounds a_P by ceil((4+8C_seq)/3).',
        domain='For every admissible exactly paired-closed original source with S=M=X, and every ONE fixed eligible depth d chosen for that entire source, the bounds hold uniformly in d. Both reflections. Other carrier geometries and other simultaneous depths stay in the literal complement.',
        parameters='d>=1, r=(n+3)/2^d-3=2^(p+1)(q+1)+1, p,q>=1, c_d=2^(d+1)-1. Freeze one d for all charged packets in W.',
        explicit_source_choice='Enumerate eligible whole-carrier starts over feasible d; select the d of the earliest original initial-KEEP ID, and retain that depth globally. Empty class if none. This is a finite explicit choice. The original frozen carrier-only choice d=v2(n+3)-2, r=1 mod8 is a valid narrower corollary.',
        scope_extension='SCOPE_EXTENSION_01.json records the all-p,q one-depth extension before its new witnesses. No budget is summed across d. All literal I/J families are covered by selecting their construction depth.',
        literal_complement='Original U_int IDs outside recognized critical prefixes and immediate certified I/J restoration words at the one selected depth. Includes arbitrary B restoration even if it uses only active keys, creates no global leaves, and eventually returns to the same full tree. Other simultaneous depths and other carrier geometries are also unresolved.',
        exact_coverage_obstruction={'source':'J_p3_q1_d1_m2_altered_restore_complete_witness.json',
                                   'candidate':'Every active-only no-fresh-leaf internal lifecycle is fully in R_life.',
                                   'change':'Before each full descending restoration insert active KEEP3,31,4,30 (physical6,62,8,60). Preserve all final descending and outer closing work.',
                                   'A':1662,'Q_B':991,'U_int':26,'R_crit_equals_R_life':22,'literal_unpaid_complement':4,
                                   'literal_original_complement_ids':[[110,1],[118,1],[244,1],[252,1]],
                                   'claim_refuted':'Exhaustive coverage by the stated immediate I/J packet grammar.',
                                   'not_refuted':'Aggregate O(A), the fixed-cardinality birth theorem, or the scoped packet charging theorem.'})
    (HERE/'LIFECYCLE_CERTIFICATE.json').write_text(json.dumps(certificate, indent=2), encoding='utf-8')
    print(json.dumps({'sources': len(results), 'potential_recharge_probes': len(probes), 'maps_written': True}))


if __name__ == '__main__':
    main()
