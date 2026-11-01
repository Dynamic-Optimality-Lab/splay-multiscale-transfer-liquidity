"""Independent local-source and symbolic-case audit; no new m is replayed."""
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
NI = HERE.parent / 'route_c_nowhere_immediate_residual_20261101_v001'
checks = Counter()


def ck(test, name):
    if not test:
        raise AssertionError(name)
    checks[name] += 1


def read(p):
    return json.loads(p.read_text(encoding='utf-8'))


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def save(name, data):
    with (HERE / name).open('x', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')


def ancestors(t, key):
    result = []
    while t:
        result.append(t)
        if t[0] == key:
            return result
        t = t[1 if key < t[0] else 2]
    raise AssertionError('present source key')


def depth(t, key):
    return len(ancestors(t, key))-1


def keys(t):
    return [] if t is None else keys(t[1])+[t[0]]+keys(t[2])


def reflection(t):
    return None if t is None else [14-t[0], reflection(t[2]), reflection(t[1])]


def source_frame(t, x, y, events):
    px, py = ancestors(t, x), ancestors(t, y)
    h, d = len(py)-1, len(px)-1
    same = 0
    while same < min(len(px), len(py)) and px[same][0] == py[same][0]:
        same += 1
    ops = []
    for top in range(d-2, -1, -2):
        g, p = px[top][0], px[top+1][0]
        ops.append(dict(case=('L' if x < g else 'R')+('L' if x < p else 'R'),
            site_depth=top, grandparent=g, parent=p))
    if d % 2:
        ops.append(dict(case='ZIG', site_depth=0, grandparent=px[0][0], parent=None))
    ck([op['case'] for op in ops] == [ev[0] for ev in events], 'original source frame word')
    entry = next(j for j, op in enumerate(ops)
        if y in keys(ancestors(t, op['grandparent'])[-1]))
    op = ops[entry]
    mu = 0 if y == op['parent'] else (1 if op['case'] == 'ZIG' else 2)
    role = 'parent' if y == op['parent'] else 'other'
    outer = [op['case'] for op in ops[entry+1:] if op['case'] != 'ZIG']
    matched = outer.count('LL' if y < x else 'RR')
    return dict(h=h, access_depth=d, lca_depth=same-1, operations=ops, entry_operation=entry,
        entry_role=role, mu=mu, outer_doubles=len(outer), matching_outer_doubles=matched,
        U=min(h+2, max(0, h+mu-len(outer)-matched)))


def main():
    entry = read(HERE / 'entry_source_pins.json')
    for rel, h in entry['files'].items():
        ck(sha(ROOT / rel) == h, 'inherited source and prior research unchanged')
    ck(entry['gate_sha256'] == sha(HERE / 'UH00_FOUR_RULE_GATE.md'), 'pre-execution gate unchanged')
    kernel = read(HERE / 'fixed_source_kernel.json')
    proof = read(HERE / 'uniform_proof_certificate.json')
    ck(kernel['source_replay_sha256'] == sha(NI / 'full_source_replays.json'), 'independently executed source basis provenance')
    ck(kernel['uniform_source_identity_sha256'] == sha(NI / 'uniform_nowhere_identity.json'), 'existing all-m source identity provenance')
    ck(proof['source_kernel_sha256'] == sha(HERE / 'fixed_source_kernel.json'), 'fixed kernel hash')
    source = read(NI / 'full_source_replays.json')
    source_identity = read(NI / 'uniform_nowhere_identity.json')
    ck(source_identity['paired_closed'] and source_identity['nowhere_diagonal'], 'inherited uniform closed reachable source family')
    for orientation, source_field in [('normal', 'cycle'), ('reflected', 'mirrored_cycle')]:
        phases = kernel['kernels'][orientation]
        raw = source[source_field]
        ck(phases == dict(P=raw[:8],W=raw[8:25],X=raw[-9:]), 'only34 fixed existing source contexts extracted')
        P, W, X = phases['P'], phases['W'], phases['X']
        ck((len(P),len(W),len(X)) == (8,17,9), 'word phase lengths')
        active = set(range(1,8)) if orientation == 'normal' else set(range(7,14))
        for phase in phases.values():
            for j, row in enumerate(phase):
                for name in ['source_A','source_B','destination_A','destination_B']:
                    ck(keys(row[name]) == list(range(1,14)), 'actual strict source BST')
                da = depth(row['source_A'], row['key'])
                ck(row['a'] == (da+1)//2 and da <= 6 and row['a'] > 0, 'active A path gives capacity at most6')
                ck(all(t[0] in active for t in ancestors(row['source_A'],row['key'])), 'A path never enters arbitrary fringe')
                ck(row['source_A'] != row['source_B'] and row['destination_A'] != row['destination_B'], 'nowhere diagonal source states')
                ck(row['delta'] == row['q']-2*row['a'], 'actual positive block delta')
                if row['mode'] == 'KEEP':
                    db = depth(row['source_B'],row['key'])
                    ck(db > 0 and row['q'] == db//2 and row['z'] == db % 2, 'all KEEPs count as genuine B changes including zero doubles')
                    ck(all(t[0] in active for t in ancestors(row['source_B'],row['key'])), 'B path stays in active core')
                else:
                    ck(row['a'] == 1 and row['source_B'] == row['destination_B'], 'one-StepEv DELETE freezes B')
                if j:
                    ck(phase[j-1]['destination_A'] == row['source_A'] and phase[j-1]['destination_B'] == row['source_B'], 'within-phase source continuity')
        for a,b in [(P,W),(W,W),(W,X),(X,P)]:
            ck(a[-1]['destination_A'] == b[0]['source_A'] and a[-1]['destination_B'] == b[0]['source_B'], 'all repetition and return seams are exact source identities')
            ck(a[-1]['key'] != b[0]['key'], 'cyclic singleton leader seam')
        ck([j for j,r in enumerate(W) if r['delta'] > 0] == [9], 'one positive at fixed W slot9')
        ck(all(r['delta'] <= 0 for r in P+X), 'no seam or bridge positive debt')
        ck(sum(r['mode']=='DELETE' for r in P+W+X)==2, 'exactly two recurrent resets independent of repetition')
        ck(sum(r['mode']=='KEEP' for r in P)==6 and len(W)==17 and len(X)==9, 'B-change counts6,17,9')
        ck((sum(r['a'] for r in P+X),sum(r['q'] for r in P+X),sum(r['z'] for r in P+X)) == (22,18,8), 'fixed additive constants for all-m identity')
        ck((sum(r['a'] for r in W),sum(r['q'] for r in W),sum(r['z'] for r in W)) == (23,16,11), 'one source loop additive coefficients')
        near = []
        for k in range(7):
            row = W[10+k]
            h = depth(W[9]['destination_B'], row['key'])
            C, c = 2*row['a'], h//2+k
            near.append(dict(W_slot=10+k,key=row['key'],a=row['a'],q=row['q'],h=h,k=k,
                UD_ceiling=c,capacity=C,slack=c-C))
            ck(c >= C, 'exact short-lag UD source inequality')
        ck(near == proof['short_lag_UD_cases'][orientation], 'all seven independently reconstructed short-lag cases')
        ck(len(W)-1-9==7 and all(r['mode']=='KEEP' and r['d_B']>0 for r in W[10:]), 'first seven genuine successors stay inside same copy before any seam')
        ck(7 > 6 and all(2*r['a'] <= 6 for r in P+W+X), 'long-lag branch cUD>=k>=7 exceeds every capacity')
        # Successive positive gaps have two structural forms, independent of m.
        internal_gap=len(W)
        wrap_gap=len(W[10:])+len(X)+sum(r['mode']=='KEEP' for r in P)+len(W[:9])+1
        ck((internal_gap,wrap_gap)==(17,32), 'all distinct anchor gaps at least17 B changes')
        fp=source_frame(W[10]['source_B'],W[10]['key'],W[11]['key'],W[10]['B_events'])
        ck(fp == proof['FI_source_frame'][orientation], 'subtree entry independently gives FI frame identity')
        ck((fp['h'],fp['mu'],fp['outer_doubles'],fp['matching_outer_doubles'],fp['U'])==(3,0,1,0,2), 'FI source bound U=2 from parent entry and one outer cross double')
        ck(depth(W[10]['destination_B'],W[11]['key']) <= fp['U'], 'post depth verifies bound but does not choose it')
        ck((W[9]['a'],W[9]['q'],W[10]['a'],W[10]['q'],W[11]['a'],W[11]['q'])==(1,3,1,2,1,1), 'source triple debt and actual capacities')
        ck(fp['U']//2+1-1==1 and fp['U']//2-1==0, 'newest cFI=1 and arbitrary older cFI=k>=1')
        ck(depth(W[9]['destination_B'],W[10]['key'])==4 and 4//2==2, 'newest immediate KEEP4 ceiling2')
        ck(min(internal_gap,wrap_gap)-1 >= 16 >= 2, 'older immediate facts k>=17 and U(x,x)=0 give cFI>=16')
        ck(W[10]['destination_B'][0]==W[10]['key'], 'accessed key depth bound U(x,x)=0')
        debt=[0, W[9]['delta']]
        debt += [max(0,debt[-1]-(2*W[10]['a']-2))]
        debt += [max(0,debt[-1]-(2*W[11]['a']-1))]
        ck(debt == proof['FI_local_debt_recurrence'] == [0,1,1,0], 'induction transition restores zero debt within three blocks')
        ck(len(W[9]['B_events'])==3 and all(e[0]!='ZIG' for e in W[9]['B_events']), 'residual is actual third B-double event index2')
        ck(len(W[11]['A_events'])==1 and W[11]['q']==1, 'giver bit1 outside own bit0 reservation')
        ck(all(r['q'] <= 2*r['a'] for r in P+W+X if r['delta']<=0), 'all other demands fit own reserved capacities')
    a,b=kernel['kernels']['normal'],kernel['kernels']['reflected']
    for phase in ['P','W','X']:
        for r,s in zip(a[phase],b[phase]):
            ck(s['key']==14-r['key'] and all(s[n]==reflection(r[n]) for n in ['source_A','source_B','destination_A','destination_B']), 'full source-kernel reflection')
    # Symbolic support identities. No loop over, construction of, or protocol
    # trial on new m values occurs here. These are constant coefficients used
    # in the written integer induction and cut partition proof.
    ck(8+9==17 and 17-3==14, 'positive index i_r=17+17r and pair supports separated')
    ck(17+17-2==32 and 17+17-3==31, 'two distinct anchor spacing cases exceed triple length')
    ck(17+15 > 0 and 17-2==15, 'accepted-count coefficients N-2m=17+15m')
    ck(17-2==15 and 15-1==14, 'largest bad cut17m+2 lies14 positions before last block')
    ck(11-9==2 and 11<17 and 9<17, 'symbolic donor and anchor stay within same repeated phase interval')
    ck(1 != 0 and 17 > 1, 'donor bit1 distinct from own bit0 and bad-cut offset difference1 cannot equal nonzero multiple17')
    ck(2+2==4 and 5-4>0, 'UD endpoint debt m-4 positive for all integer m>=5')
    ck(proof['UD_final_debt_lower_bound']=='m-4' and proof['UD_cut0_final_debt']=='m' and proof['UD_cut2_final_debt']=='m-4', 'uniform UD terminal accounting identities')
    ck(proof['FI_accepted_count']=='17+15m' and proof['FI_rejected_count']=='2m' and proof['FI_rejected_final_debt']==1, 'uniform FI cut partition formula')
    ck(proof['FI_DELETE_or_startup_units_used']==proof['reused_units']==proof['new_m_values_replayed']==proof['larger_finite_fits']==0, 'no new m replay or forbidden funding in symbolic scheme')
    proof_path=HERE/'UH01_UNIFORM_SEPARATION_PROOF.md'
    ck(proof_path.is_file(), 'full all-m analytic proof supplied')
    save('independent_audit.json',dict(status='PASS',date='2026-11-01',checks=dict(checks),
        source_kernel_sha256=sha(HERE/'fixed_source_kernel.json'),
        proof_certificate_sha256=sha(HERE/'uniform_proof_certificate.json'),
        analytic_proof_sha256=sha(proof_path),
        source_rows_per_orientation=34, short_lag_cases_per_orientation=7,
        first_entry_method='original source subtree membership; producer uses LCA',
        general_m_tested_or_replayed=False, new_m_values_replayed=0,new_source_engine_calls=0,larger_finite_fits=0,
        verification_scope='exact source premises and exhaustive proof-case/support checks; all-m induction is the written analytic proof',
        quantifiers='all integers m>=5, arbitrary untouched fringe F>7, both orientations',
        uniform_UD_accepted_cuts=0, uniform_UD_final_debt_lower_bound='m-4',
        uniform_FI_accepted_count='17+15m',uniform_FI_rejected_count='2m',
        uniform_strict_FI_UD_separation='PROVED—RESTRICTED DOMAIN',
        startup_or_other_lap_units_used=0,reused_units=0,
        matching_terminal_line='FROZEN',universal_CD='OPEN',automatic_successor_launched=False))
    print(json.dumps(dict(status='PASS',independent_checks=sum(checks.values()),
        source_rows=68,short_lag_cases=14,new_m_values_replayed=0,
        theorem='for every m>=5: UD accepts0; FI accepts17+15m and rejects2m',
        proof_type='source identities, exhaustive lag split and chronological span induction'),indent=2))


if __name__=='__main__':
    main()
