"""Capped source-symbolic obstruction assembly and exact parent-status reconstruction."""
import hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;C=F.parent;P=C.parent
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def put(n,z):
    with (F/n).open('x',encoding='utf-8') as f:json.dump(z,f,indent=2)
def main():
    # The new obstruction relies on accepted SOURCE realization, not abstract A states.
    paths=[B/'UNIFORM_A_REALIZATION_OVER_CLOSED_B.md',
      B/'SOURCE_JOINT_REPAIR_03/SOURCE_ONLY_B_BOUND.md',
      C/'CONTINUATION_02/ANCHORED_FAMILY_COMPLETE_FUNDING.md',
      C/'CONTINUATION_02/DESCENDING_SWEEP_RETURN.md',
      C/'CONTINUATION_01/SYMBOLIC_B_CLOSURE.md']
    deps={str(p.relative_to(P)):sha(p) for p in paths}
    # Polynomial coefficients of 2*(2r+2)-(6r-6), all r, no finite sampling.
    m=(2,2);q=(6,-6);margin=tuple(2*a-b for a,b in zip(m,q));assert margin==(-2,10)
    cert={'status':'B_CHART_ONLY_NATURAL_MACRO_ARCHITECTURE_REFUTED_BY_SOURCE_DERIVATION',
      'r_min':6,'genuine_count_polynomial':m,'B_cost_polynomial':q,
      'forced_cycle_margin_polynomial':margin,
      'local_H1_edges':'each edge separately realized in an original reachable paired-closed source',
      'same_all_H1_source_claimed':False,'B_side_context_condition':'finite and invariant under A-only DELETE',
      'D_range':'any finite real state values; no width bound used',
      'other_packetizations_refuted':False,'A_dependent_potentials_refuted':False,
      'UCF35_refuted':False,'Coarse_Double_counterexample':False,
      'source_queries':0,'source_engine_calls':0,'input_sha256':deps}
    put('B_chart_only_source_obstruction.json',cert)
    # Live source release uses the exact AF family, not a newly sampled BST.
    forward=[v for x in range(3,12,2) for v in (1,x)]
    reverse=[v for x in range(9,2,-2) for v in (1,x)]+[1]
    assert len(forward)+len(reverse)+1==20
    release={'status':'SOURCE_EXACT_SYMBOLIC_E2A_COUNTEREXAMPLE_TO_GLOBAL_L2',
      'r':7,'physical_keys':list(range(1,14)),'genuine_marks':list(range(1,14,2)),
      'source_word':['KEEP13','DELETE1','DELETE Gamma_low',{'KEEP':forward},{'KEEP':reverse},'DELETE Gamma_reset'],
      'source_family':'AF35; same transformation definitions, every operation retained',
      'target':3,'H':1,'Q':2,'old_marked_path':[1,13,3],
      'old_path_ancestor_degrees':[1,5],'old_target_degree':0,
      'new_degrees':{'3':2,'13':4,'1':0},'L2_source':3,'L2_target':2,
      'physical_price':0,'signed_margin':-1,'whole_B_Q':38,
      'paired_closure':'AF35 symbolic proof, full transformations not numerically expanded',
      'whole_source_full_comparison':'AF35 complete independent h, working2',
      'full_numeric_replay':False,'UCF35_refuted':False,
      'source_queries':0,'source_engine_calls':0,'input_sha256':deps}
    put('live_degree_release_countercertificate.json',release)
    boxes=[
      dict(id='UCF35',status='OPEN',target='complete original source-licensed frozen-owner funding for all legitimate r>=7 inputs',
        conditions='original source, actual I,fE,a0,Gamma, Bank25 and all caps',
        inheritance='C14 transfer/base; C15 exchange; immutable SI34; C35-II reductions',
        children=['A_SENSITIVE_CREDIT35','GAMMA_COMPLETENESS35'],
        ambiguities=['uniform source repayment','coverage/release of independently live additional Gamma restrictions'],
        bridge='full source h plus original compatibility gives actual owner extension',
        measure='exact witness factorization; no claimed descent to a solved leaf',
        falsification='one legitimate original input rejecting every licensed complete alternative'),
      dict(id='A_SENSITIVE_CREDIT35',status='OPEN',target='source-simple credit retaining actual A information',
        conditions='all supports/core sizes, private populations and source lengths',
        inheritance='SC35,DL35,OR35,BC35',children=['R7_EXCEPTION_REPAYMENT35','OTHER_CORES_AND_SUPPORTS35'],
        ambiguities=['joint distinct repayment on live low-run exceptions','uniform beyond the source-restricted class'],
        bridge='SC35 reconstructs all closed histories from credited source-simple leaves',
        measure='SC35 genuine-macro descent where applicable; OR35 is fixed-run representation only',
        falsification='complete original-source all-alternative countercertificate'),
      dict(id='DL35',status='DERIVATION_COMPLETE_INTERFACE_AUDITED',target='degree-layer identity and actual threshold channels',
        conditions='closed maximal full B core',inheritance='all-SS path-to-star',children=[],ambiguities=[],
        bridge='nonnegative actual local margins yield complete original Type B source construction',
        measure='cyclic Boolean threshold alternation',falsification='invalid degree identity or duplicated actual channel bit'),
      dict(id='SE35',status='DERIVATION_COMPLETE_INTERFACE_AUDITED',target='seven-key source complement funded with working10',
        conditions='core13 and no E2a,E2b,E3,E4 packet',inheritance='DL35 and original signed induction',children=['DL35'],ambiguities=[],
        bridge='D=L2,c=min(H,3), exact unit selection contains natural h0',measure='complete integer degree partition',
        falsification='actual complement packet with negative margin or owner-unit selection failure'),
      dict(id='OR35',status='DERIVATION_COMPLETE_GUARDED_INTERFACE_AUDITED',target='fixed anonymous operand set for arbitrarily long H1 runs',
        conditions='entry root marked; contexts and barriers retained',inheritance='ordinary six root-local frames',children=[],ambiguities=[],
        bridge='run replay lifts exactly on the fixed actual context assignment; no sign follows',
        measure='first use of an anonymous operand outside entry P0',falsification='such a first operand despite unchanged child pointers'),
      dict(id='BC35',status='ARCHITECTURE_REFUTED_BY_SOURCE_DERIVATION',target='universal B/chart-only natural-macro debt',
        conditions='universal formula invariant under A-only preparation, fixed natural packetization',
        inheritance='original closed V_r source and accepted arbitrary A realization',children=[],ambiguities=[],
        bridge='forces actual-A dependence or a different genuinely licensed grouping; NOT root refutation',
        measure='sum necessary edge inequalities on a closed B-side period',
        falsification='a flaw in the genuine H1 edge realization or B-side context preservation'),
      dict(id='RG35',status='DERIVATION_COMPLETE_INTERFACE_AUDITED',target='all claim-bound reservations and exact signed charts compose with full h',
        conditions='consistent actual full-claim bindings and licensed E-only retirement; source h already complete',
        inheritance='original frozen exchange, natural safety, actual ordinal identity and transport',children=[],ambiguities=[],
        bridge='covers original common/f6/later binding owners and actual chart differences',
        measure='finite unique-incoming owner paths',falsification='a moved old binding or duplicated/unlicensed terminal'),
      dict(id='GAMMA_COMPLETENESS35',status='OPEN',target='every legitimate additional live Gamma restriction has proved normalization or release',
        conditions='no invented arbitrary forbidden set; no actual restriction dropped',inheritance='RG35',children=['RG35'],
        ambiguities=['general additional live-ledger admissibility/release schema not supplied by inspected contracts'],
        bridge='with source full h closes remaining reservation interface',measure='actual reservation-type cases, not assumed empty',
        falsification='a legitimate reservation that cannot be normalized or released under any full comparison'),
      dict(id='R7_EXCEPTION_REPAYMENT35',status='OPEN',target='joint source repayment for all four live degree exceptions',
        conditions='arbitrary shared/repeated H1 runs in closed core13 source',inheritance='SE35/OR35; live AF35 E2a',children=['SE35','OR35'],
        ambiguities=['actual distinct source donors or valid A-dependent signed correction'],
        bridge='complete core13 credit after original owner/chart compatibility',measure='finite degree partition and guarded run syntax; sign still unproved',
        falsification='genuine complete-source infeasibility, not the already refuted degree-only law'),
      dict(id='OTHER_CORES_AND_SUPPORTS35',status='OPEN',target='all remaining original source core/support classes',
        conditions='full UCF35 quantifiers',inheritance='accepted base and previous uniform restricted source results',children=[],
        ambiguities=['uniform credit outside the stated maximal-core7 analysis'],
        bridge='required with the seven-key class for the original all-source root',measure='no unjustified support descent claimed',
        falsification='original legitimate all-licensed-alternatives counterexample')]
    put('proof_boxes_v4.json',{'version':4,'root':'UCF35','root_status':'OPEN','prior_SI34':'REFUTED_IMMUTABLE',
      'boxes':boxes,'A_UCF35':False,'E_UCF35':False,'all_source_closed':False,
      'new_full_numeric_source_replay':False,'new_source_queries':0})
    print('B_ONLY_SOURCE_OBSTRUCTION_AND_PARENT_OPEN_RECONSTRUCTION',flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_proof178_exit.json').open('x',encoding='utf-8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
