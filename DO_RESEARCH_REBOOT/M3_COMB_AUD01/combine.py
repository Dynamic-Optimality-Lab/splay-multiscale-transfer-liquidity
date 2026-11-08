"""Assemble the candidate, audit all premises/scopes and refuse a false full PASS."""
import sys,json,time,itertools,hashlib,subprocess
from pathlib import Path
from collections import Counter
from candidate import RestrictedCombinedCertificate
BASE=Path(__file__).resolve().parent;ROOT=BASE.parents[1];R=ROOT/'DO_RESEARCH_REBOOT'

def read(p):return json.loads(p.read_text(encoding='utf-8'))
def raw(p):return Path('\\\\?\\'+str(p.resolve())).read_bytes()
def digest(p):return hashlib.sha256(raw(p)).hexdigest()
def save(p,j):
    with p.open('x',encoding='utf-8') as f:json.dump(j,f,indent=2)

def main():
    start=time.process_time();baseline=read(BASE/'entry_baseline.json')
    for row in baseline:assert digest(ROOT/row['path'])==row['sha256'],row['path']
    finite=[read(BASE/f'finite_gap{g}.json') for g in range(5)]
    assert all(j['status']=='PASS_INDEPENDENT_FINITE_AUDIT' for j in finite)
    assert sum(j['all_stored_edges_checked'] for j in finite)==19174005
    high=read(BASE/'high_source_audit.json');primitive=read(BASE/'primitive_interface_audit.json')
    original=read(BASE/'original_semantics_audit.json')
    assert high['status'].startswith('PASS_') and primitive['status'].startswith('PASS_') and original['status'].startswith('PASS_')
    P=RestrictedCombinedCertificate();residuals=Counter();single_low=single_high=multi_low=multi_high=0
    uncovered=[];fallbacks=Counter();v_not_target=0
    for row in original['records']:
        if not row['accepted']:continue
        s=row['source'];t=row['destination'];support=sum(n>0 for n in s['sigma'])
        if support>1:
            try:P.ordinary(s)
            except ValueError:undefined=True
            else:undefined=False
            assert undefined
            if row['kind']=='LOW':
                multi_low+=1;uncovered.append({'record_file':row['record_file'],'index':row['index'],
                    'sigma':s['sigma'],'mu':s['mu'],'full_original_root_replayed':True,
                    'weight':row['weight'],'candidate_undefined':True,'is_negative_cycle':False})
            else:multi_high+=1
            continue
        si=P.ordinary_J(s);ti=P.ordinary_J(t);ws=P.ordinary(s);wt=P.ordinary(t)
        if row['kind']=='LOW':
            assert si['profile_found'] and ti['profile_found'],(row['label'],si,ti)
            r=row['weight']+ws-wt;assert r>=0;residuals[r]+=1;single_low+=1
        else:
            wm=P.midpoint(row['midpoint']);a=row['weight']+ws-wm;b=wm-wt
            assert a>=0 and b>=0;residuals[a]+=1;residuals[b]+=1;single_high+=1
            v_not_target+=int(row['midpoint']['v']!=t['b']['root'])
            if not si['profile_found']:fallbacks[si['fallback']]+=1
            if not ti['profile_found']:fallbacks[ti['fallback']]+=1
        assert -7<=ws<=0 and -7<=wt<=0
    assert multi_low==2 and multi_high==5 and len(uncovered)==2
    assert single_low+single_high==161
    # Exhaust all region/J-value combinations used in the global proof.
    algebra=0
    for src_chi,dst_chi in [(0,0),(0,1),(1,1)]:
        lower=-3 if (src_chi,dst_chi)==(0,1) else 2
        for j,w in itertools.product((-2,-1,0),range(lower,7)):
            delta=-5*dst_chi-(j-5*src_chi);assert w>=delta;algebra+=1
    for state_chi,j in itertools.product((0,1),(-2,-1,0)):
        assert 0>=j;algebra+=1
    masks=[m for m in range(512) if m.bit_count()==5];assert len(masks)==126
    signatures={(0,)*10}
    for g in range(10):
        for n in range(1,267):signatures.add(tuple(n if j==g else 0 for j in range(10)))
    assert len(signatures)==2661
    sectors=len(signatures)*len(masks);assert sectors==335286
    coverage={
        'status':'FAIL_FULL_M3_COVERAGE_INCOMPLETE',
        'single_gap_signature_vectors':len(signatures),'single_gap_mask_signature_sectors':sectors,
        'closed_cycle_partition':[
            {'domain':'support(sigma)<=1','status':'PROVED_RESTRICTED_DOMAIN','mechanism':'explicit W=J-5*chi8 on O; -5*chi8 on M'},
            {'domain':'support(sigma)>=2 AND D_L<=2*N_H+P_L','status':'PROVED_RESTRICTED_DOMAIN','mechanism':'universal high toll and exact signed sum'},
            {'domain':'support(sigma)>=2 AND N_H>=1 AND D_L>2*N_H+P_L','status':'OPEN','mechanism':None}],
        'both_chi8_regions_in_residual_domain':True,
        'actual_original_low_states_rejected_by_candidate':uncovered,
        'arithmetic_gap_example':{'N_H':1,'P_L':0,'D_L':3,'proved_lower_bound':-1,
                                  'assertion':'illustrates insufficiency of the bound; not an exhibited walk'},
        'negative_original_cycle_certified':False,
        'multi_gap_literal_completion_obstruction':'two equal full original edges have different hidden S allocations; refutes that extension only',
        'no_total_potential_or_alternative_residual_sign_proof_supplied':True}
    save(BASE/'coverage_audit.json',coverage)
    deps=[
        {'id':'SOURCE_LOW','status':'SOURCE_DEFINITION','depends':[],'evidence':'frozen STRICT_LOW_COMPILER and imported interpreters/inventory/repairs'},
        {'id':'SOURCE_HIGH_PRODUCT','status':'SOURCE_DEFINITION','depends':[],'evidence':'frozen STRICT_HIGH_COMPILER, CW_PRODUCT and S03 projections'},
        {'id':'LOW_PRIMITIVES','status':'INDEPENDENT_EXACT_PASS','depends':['SOURCE_LOW'],'evidence':'408 full-field core rotations,3570 max-pair identities'},
        {'id':'LOW_SOURCE_REDUCTION','status':'SOURCE_PROOF_REVIEWED','depends':['SOURCE_LOW','LOW_PRIMITIVES'],
         'evidence':'H1 fusion; Gamma0 terminal debt; Gamma1 two-access form; S-empty ghost erasure; <=3 retained anonymous classification',
         'scope':'single fixed gap; not multiple-positive-gap allocation determinacy; does not assume M1 cycle sign'},
        {'id':'CORE_DEBT','status':'INDEPENDENT_EXACT_PASS','depends':['LOW_PRIMITIVES'],'evidence':'4862 trees,43758 reference accesses,4224 negative edges,acyclic debt maximum2'},
        {'id':'FINITE_LOW_TABLES','status':'INDEPENDENT_EXACT_PASS','depends':['CORE_DEBT'],'evidence':'19174005 rows and all analytic omissions, independently enumerated A profiles'},
        {'id':'HIGH_SOURCE_CLASSIFICATION','status':'SOURCE_PROOF_REVIEWED','depends':['SOURCE_HIGH_PRODUCT'],
         'evidence':'unique core path h<=8; source max-sentinel claimant; incompatible detour fails by entry10; literal0 cases'},
        {'id':'HIGH_TOLL_ABSORPTION','status':'INDEPENDENT_EXACT_PASS_WITH_SOURCE_REDUCTION','depends':['HIGH_SOURCE_CLASSIFICATION'],
         'evidence':'11340 dirty root claims,171 chi8 boundary identities,9 clean final-write identities; endpoint order argument'},
        {'id':'LOW_CHI8_CONSERVATION','status':'SOURCE_PROOF_REVIEWED_AND_PRIMITIVE_PASS','depends':['SOURCE_LOW','LOW_PRIMITIVES'],
         'evidence':'real ordered rotations; gap9 absent preserves core8 right pair; present gap9 excludes chi8 endpoints'},
        {'id':'FIXED_GAP_SHARED_J','status':'PROVED_RESTRICTED_DOMAIN','depends':['LOW_SOURCE_REDUCTION','CORE_DEBT','FINITE_LOW_TABLES'],
         'evidence':'static signature dispatch; actual low boundary maps into table; population remains opaque; mathematical low reflection only'},
        {'id':'GLOBAL_SINGLE_GAP_W','status':'PROVED_RESTRICTED_DOMAIN','depends':['FIXED_GAP_SHARED_J','HIGH_TOLL_ABSORPTION','LOW_CHI8_CONSERVATION','SOURCE_HIGH_PRODUCT'],
         'evidence':'W_O=J-5chi8; W_M=-5chi8; exact inequalities; independent private OM/MO witnesses share actual M'},
        {'id':'ALL_SIGNATURE_BALANCED_CYCLES','status':'PROVED_RESTRICTED_DOMAIN','depends':['HIGH_TOLL_ABSORPTION','LOW_CHI8_CONSERVATION'],
         'evidence':'every closed mixed walk stays in one region; weight>=2N_H+P_L-D_L'},
        {'id':'MULTI_GAP_HARD_DEFICIT','status':'OPEN','depends':[],'evidence':'no supplied total J or direct sign theorem; witness pair blocks literal completion'},
        {'id':'FULL_M3','status':'INCOMPLETE','depends':['GLOBAL_SINGLE_GAP_W','ALL_SIGNATURE_BALANCED_CYCLES','MULTI_GAP_HARD_DEFICIT'],
         'evidence':'a complete partition still contains an OPEN branch'}]
    byid={n['id']:n for n in deps};active=set();done=set();order=[]
    def visit(k):
        assert k in byid and k not in active,('missing or circular dependency',k)
        if k in done:return
        active.add(k)
        for child in byid[k]['depends']:visit(child)
        active.remove(k);done.add(k);order.append(k)
    for k in byid:visit(k)
    save(BASE/'dependency_ledger.json',{'status':'ACYCLIC_WITH_EXPLICIT_OPEN_LEAF','topological_order':order,'nodes':deps,
        'withdrawn_ACL01_initial_promotion_used_as_premise':False,
        'old_B_only_negative_cycle_used_as_original_counterexample':False,
        'inactive_legacy_imports_distinguished_from_mathematical_premises':True,
        'source_reduction_proofs_are_not_finite_sampling_or_machine_formalization':True})
    result={'status':'AUDIT_COMPLETE_FULL_M3_INCOMPLETE','full_M3_certificate_pass':False,
        'restricted_single_gap_certificate_pass':True,'universal_high_toll_audit_pass':True,
        'all_finite_low_edges_independently_verified':sum(j['all_stored_edges_checked'] for j in finite),
        'fresh_original_root_evaluations':original['original_roots_evaluated'],
        'actual_full_state_closed_mixed_walks':len(original['actual_full_state_cycles']),
        'restricted_candidate_original_records_checked':single_low+single_high,
        'accepted_single_gap_low_records':single_low,'accepted_single_gap_high_records':single_high,
        'multi_gap_original_low_records_outside_candidate_domain':multi_low,
        'multi_gap_high_controls_test_universal_high_law':multi_high,
        'high_fiber_labels_independent_of_actual_B_target_examples':v_not_target,
        'low_state_fallbacks_observed':0,'high_boundary_fallbacks':dict(fallbacks),
        'global_glue_algebra_cases':algebra,'residual_histogram':dict(residuals),
        'raw_O_coordinates':147,'raw_M_coordinates':127,
        'global_single_gap_W_range':[-7,0],'no_negative_original_cycle_certified':True,
        'R1_R4_preserved':True,'Bank25':25,'Stage04_authorized_or_run':False,
        'source_proof_review_limit':'not a formal proof assistant verification of every abstract witness',
        'CPU_seconds':round(time.process_time()-start,3)}
    save(BASE/'combined_audit.json',result)
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
