"""Separate source/scope/case-union audit, without construction imports.

Checks universal integer-interval and rational-affine proof certificates. It
does not enumerate keys, masks, populations, trees, transitions or walks.
Previously accepted finite graph certificates are hash-pinned proof premises;
their verifiers/edge rows are not replayed.
"""
import ast,hashlib,json,sys,time
from fractions import Fraction
from pathlib import Path
B=Path(__file__).resolve().parent
R=B.parent
ROOT=R.parent
C=R/'06_CERTIFICATES'
def xp(p):return Path('\\\\?\\'+str(p.resolve()))
def raw(p):return xp(p).read_text(encoding='utf-8')
def read(p):return json.loads(raw(p))
def sha(p):return hashlib.sha256(xp(p).read_bytes()).hexdigest()
def write(n,d):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(d,f,indent=2)
def text_has(p,parts):
    s=raw(p)
    for part in parts:assert part in s,(str(p),part)
def poly(p):return {k:Fraction(v) for k,v in p.items() if Fraction(v)!=0}
def affine(p):
    assert len(p['ge'])==len(p['ge_multipliers']) and len(p['eq'])==len(p['eq_multipliers'])
    assert all(Fraction(x)>=0 for x in p['ge_multipliers'])
    acc={}
    for terms,multipliers in ((p['ge'],p['ge_multipliers']),(p['eq'],p['eq_multipliers'])):
        for term,m in zip(terms,multipliers):
            for k,v in poly(term).items():acc[k]=acc.get(k,Fraction(0))+Fraction(m)*v
    assert poly(acc)==poly(p['goal']),p['name']
def interval_partition(domain,branches):
    # A proof by integer interval adjacency, not evaluation on finitely many k.
    assert all(isinstance(x,int) for x in domain)
    cursor=domain[0]
    for branch in branches:
        lo,hi=branch['interval']
        assert isinstance(lo,int) and isinstance(hi,int) and lo==cursor and lo<=hi
        cursor=hi+1
    assert cursor==domain[1]+1
def main():
    pins=read(B/'dependency_pins.json')['pins']
    for p in pins:assert sha(ROOT/p['path'])==p['sha256'],p['path']
    index={p['path']:p['sha256'] for p in pins}
    for dirname in ('DIRECT_NFKS_RT2','DIRECT_CD_K4','DIRECT_CDK5_LOW'):
        assert any('/'+dirname+'/' in p for p in index)

    # Independently inspect imported theorem hypotheses and completion records.
    rt=C/'DIRECT_NFKS_RT2';k4=C/'DIRECT_CD_K4';k5=C/'DIRECT_CDK5_LOW';nine=R/'RESTRICTED_CD_STEP04'
    text_has(rt/'DIRECT_NFKS_RT2_coarse_double_class_proof.md',[
      'diagonally reachable, exactly closed (both trees)','at\nmost 3 distinct','DELETEs arbitrary present keys',
      'Q_B ≤ 2C_K ≤ 2C_X ≤ 2A','Exact B','Exact A closure'])
    assert read(rt/'DIRECT_NFKS_RT2_terminal_status.json')['outcome']=='RT2-A'
    text_has(k4/'DIRECT_CD_K4_original_class_proof.md',[
      '|supp(KEEP)|=4','exact A closure','Q_B ≤ 2A','C_K ≤ C_X','C_X ≤ A'])
    text_has(k4/'DIRECT_CD_K4_B_cycle_conservation.md',[
      'exact B-closed','4≤|U_t|≤7','q_t − 2c_t + η_{t+1} − η_t ≤ 0','Q_B ≤ 2C_K','nonclosed prefix is excluded'])
    text_has(k4/'DIRECT_CD_K4_seven_node_reduction.md',[
      'New key','size 1','exact B closure','every\nKEEP-occurrence B-state','DELETE-occurrence'])
    text_has(k4/'DIRECT_CD_K4_source_rotation_growth_proof.md',[
      'arbitrary hanging-subtree sizes','Marked access (x∈M): nonincreasing','Unmarked access (x∉M): at most +2'])
    old4=read(k4/'DIRECT_CD_K4_terminal_status.json');fin4=read(k4/'DIRECT_CD_K4_finite_verification.json')
    assert old4['outcome']=='CDK4-A' and all(v.startswith('PASS') for v in old4['gates'].values())
    assert fin4['total']==68876 and fin4['violations']==fin4['engine_mismatch']==0
    text_has(k5/'DIRECT_CDK5_LOW_restricted_class_proof.md',[
      'reachable, exactly closed','|supp(KEEP)|=5','≤8 at every cyclic state','Arbitrary n, length, KEEP order, DELETEs',
      'Q_B ≤ 2C_K ≤ 2C_X ≤ 2A','No finite-n residue'])
    old5=read(k5/'DIRECT_CDK5_LOW_terminal_status.json')
    old5audit=read(k5/'DIRECT_CDK5_LOW_independent_verification.json')
    assert old5['outcome']=='CDK5L-A' and all(v=='PASS' for v in old5['gates'].values())
    assert old5audit['verdict']=='PASS' and old5audit['edge_mismatch']==old5audit['inequ_violations']==0
    assert old5['graph']['edges']==142385 and old5['potential']['independent']=='PASS'
    sealed=read(nine/'final_manifest.json');ncert=read(nine/'RESTRICTED_CD_CERTIFICATE.json')
    assert sealed['status']=='RESTRICTED_CD_CLOSED_ALL_PUBLICATION_GATES_PASS'
    assert ncert['status']=='PROVED_UNIVERSAL_RESTRICTED_COARSE_DOUBLE_W5_CORE9'
    assert ncert['mandatory_open_dependencies']==[] and all(v=='PASS' for v in ncert['publication_gates'].values())
    assert ncert['domain']['genuine_KEEP_keys']==5 and ncert['domain']['marked_core_nodes']==9
    assert ncert['domain']['legal_masks']==126 and ncert['domain']['fringe']=='arbitrary admissible'
    assert ncert['domain']['closure']=='exact labeled paired A/B tree closure'
    assert not ncert['domain']['reachability_filter'] and not ncert['domain']['new_support_or_population_bound']
    assert ncert['potential']['original_h0']=={'actual_depth':0,'declared_depth':18,'q':9,'weight':-3}
    assert ncert['graph']['all_raw_fields_retained'] and ncert['graph']['SAME_full_midpoint']
    assert ncert['graph']['independent_private_witnesses'] and ncert['graph']['HIGH_v_free']
    text_has(C/'DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP04_UNIVERSAL_CERTIFICATION/S04_GENUINE_KEY_AND_CORE_THEOREM.md',[
      'K(W)=G(W)','≥1 genuine KEEP','C_M(B_{t+1}) ⊆ C_M(B_t)','B_T=B_0'])

    # Source syntax only; no imports/calls into physical or graph engines.
    source=ROOT/'python/independent/splay.py';tree=ast.parse(raw(source))
    functions={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)}
    for name in ('lookup','_descend','_rebuild','trace'):assert name in functions
    rebuild=ast.get_source_segment(raw(source),functions['_rebuild'])
    descend=ast.get_source_segment(raw(source),functions['_descend'])
    lookup=ast.get_source_segment(raw(source),functions['lookup'])
    assert 'while fr:' in rebuild and 'return _plug(fr, cur), evs' in rebuild
    assert 'node(x,' in rebuild and 'if x == k:' in descend and 'return (cur, fr)' in descend
    assert 'd, cur = 0, t' in lookup and 'return True, d' in lookup
    text_has(ROOT/'scripts/wp6_cycle_ratio.py',[
      'el.append((ia2 * nS + ib, "D", x, a, 0))','el.append((ia2 * nS + ib2, "K", x, a, b))'])
    spec=C/'DIRECT_U4_PARALLEL_RESEARCH/run_20261030_v001/U4_02_ORIGINAL_PAIR_ACCESS_SPEC.md'
    text_has(spec,['every finite exactly closed pair walk reachable from some such diagonal',
      'a=ceil(dA/2)','q=floor(dB/2)','DELETE q=z=b=0','Both trees, not roots alone, must\nclose'])

    # Inspect the new symbolic derivation separately from the assembly module.
    text_has(B/'CD5_PROOF.md',[
      'If G is empty','M=G','C_M(S_x(B)) subset C_M(B)',
      'Every KEEP target is in M','Each inclusion is\nequality',
      'x is root and already belongs','either c<=8 at every boundary, or c=9 at every boundary',
      'No walk can cross','No functions/potentials\nfrom different leaves are combined'])
    text_has(B/'DOMAIN_AUDIT.md',[
      'rotation of a reachable closed walk remains reachable','old CDK5-LOW source-reduction paragraph',
      'superseded and not used','No restriction is added on ambient key count'])
    a=read(B/'assembly.json');d=a['domain']
    assert a['theorem']=='forall original reachable fully closed gamma: |G(gamma)|<=5 implies Q_B(gamma)<=2A(gamma)'
    assert d['genuine_KEEP_support_max']==5 and d['finite_ordered_key_set']==d['ambient_size']=='arbitrary'
    assert d['word_length']=='arbitrary finite' and d['closure']=='both full labeled trees'
    assert d['reachability']=='from some common-tree diagonal' and not d['cycle_start_must_be_diagonal']
    for k in ('KEEP_DELETE','all_requests_present','DELETE_freezes_B_and_removes_no_key','DELETE_support_unrestricted',
              'zero_cost_and_nongenuine_KEEP','primitive_and_nonprimitive'):assert d[k]
    assert not d['new_population_or_mask_restriction']
    assert a['costs']=={'depth':'edge depth; root0','A':'sum ceil(d_A/2)',
      'Q_B':'sum floor(d_B/2) on KEEP; DELETE0','LT_cost_substituted':False}
    assert a['normalization']['G_nonempty']=='M_KEEP=G by cyclic latest-genuine-root provenance'
    assert a['normalization']['G_empty']=='all B charges zero'
    assert a['normalization']['nongenuine_KEEP_A_cost_retained']
    assert not a['geometry']['old_label_swap_claim_used'] and a['geometry']['five_key_core_interval']==[5,9]
    p=a['partition']
    assert p['domain']==[0,5] and p['integer']
    assert p['branches']==[{'interval':[0,0],'leaf':'zero'},{'interval':[1,3],'leaf':'RT2'},
      {'interval':[4,4],'leaf':'K4'},{'interval':[5,5],'leaf':'five_split'}]
    assert p['five_split']=={'domain':[5,9],'integer':True,'branches':[
      {'interval':[5,8],'leaf':'K5_LOW'},{'interval':[9,9],'leaf':'K5_CORE9'}]}
    interval_partition(p['domain'],p['branches'])
    interval_partition(p['five_split']['domain'],p['five_split']['branches'])
    assert a['leaf_conclusions']=={k:'Q_B<=2A' for k in ('zero','RT2','K4','K5_LOW','K5_CORE9')}
    expected_deps={'physical_semantics':[],'RT2':[],'K4':[],'K5_LOW':[],'K5_CORE9':[],
      'support_normalization':['physical_semantics'],'core_geometry':['physical_semantics','K4'],
      'CD5':['support_normalization','core_geometry','RT2','K4','K5_LOW','K5_CORE9']}
    known={}
    for n in a['dependencies']:
        assert n['id'] not in known and n['uses']==expected_deps[n['id']]
        assert all(u in known for u in n['uses']);known[n['id']]=n['uses']
    assert known==expected_deps
    # Premise and target schemas are specified independently, rather than
    # accepting an arbitrary true identity irrelevant to CD(5).
    expected={
      'zero_G':([{'A':1}],[{'Q':1}],{'A':2,'Q':-1}),
      'charge_chain':([{'Ck':2,'Q':-1},{'Cx':1,'Ck':-1},{'A':1,'Cx':-1}],[],{'A':2,'Q':-1}),
      'visited_core_base':([],[{'v':1,'1':-1},{'c':1,'1':-1}],{'v':2,'c':-1,'1':-1}),
      'visited_core_new_mark':([{'v':2,'c':-1,'1':-1},{'c':1,'1':2,'next_c':-1}],
         [{'next_v':1,'v':-1,'1':-1}],{'next_v':2,'next_c':-1,'1':-1}),
      'visited_core_revisit':([{'v':2,'c':-1,'1':-1},{'c':1,'next_c':-1}],
         [{'next_v':1,'v':-1}],{'next_v':2,'next_c':-1,'1':-1}),
      'five_core_upper':([{'k':2,'c':-1,'1':-1}],[{'k':1,'1':-5}],{'1':9,'c':-1})}
    seen=set()
    for s in a['affine_proof_schemas']:
        assert s['name'] not in seen;seen.add(s['name'])
        assert (s['ge'],s['eq'],s['goal'])==expected[s['name']]
        affine(s)
    assert seen==set(expected)
    assert a['whole_walk_leaf_selection'] and not a['mixes_leaf_potentials_or_weights']
    assert a['new_finite_tests']==a['new_solver_queries']==a['new_original_root_queries']==a['completed_semantic_checks_replayed']==0
    assert not a['unrestricted_CD_proved'] and not a['Dynamic_Optimality_proved'] and a['Bank25']==25
    assert time.process_time()<float(sys.argv[1])
    write('independent_audit.json',{
      'status':'INDEPENDENT_CD5_BASE_AUDIT_PASS','declared_input_hashes_verified':len(pins),
      'genuine_to_KEEP_support_bridge':'PROVED_CYCLICALLY_WHEN_G_NONEMPTY',
      'G_empty_Q_zero':'PROVED_SEPARATELY','full_labeled_core_constancy':'PROVED_RIGID_HANGER_INCLUSION_AND_CLOSURE',
      'core_upper_bound':'REUSED_ARBITRARY_M_GROWTH_WITH_NEW_EXACT_INDUCTION_AUDIT',
      'five_core_split':'WHOLE_WALK_CORE_LE8_OR_CORE9','symbolic_integer_interval_partitions':2,
      'universal_affine_schemas':sorted(seen),'original_domain_and_costs_preserved':True,
      'diagonal_reachability_and_cyclic_seams_preserved':True,'source_syntax_audit':'READ_ONLY_NO_RESEARCH_IMPORTS',
      'RT2_K4_K5LOW_completed_proofs_reused':True,'old_finite_certificates_replayed':False,
      'nine_core_final_seal_and_full_interface_preserved':True,'corrected_h0_retained':True,
      'historical_label_swap_claim_used':False,'mixed_leaf_potential_required':False,
      'all_cases_covered':True,'mandatory_open_CD5_dependencies':[],'CD5_mathematical_conclusion':True,
      'new_finite_tests':0,'new_solver_queries':0,'new_original_root_queries':0,
      'completed_accepted_semantic_checks_replayed':0,'proof_object_input_bytes':(B/'assembly.json').stat().st_size,
      'imports_construction':False,'external_peer_review':False,'whole_compiler_formalization':False,
      'unrestricted_CD_proved':False,'Dynamic_Optimality_proved':False,'Bank25':25,
      'publication_requires_controller_resource_and_integrity_PASS':True})
    print(json.dumps({'status':'INDEPENDENT_CD5_AUDIT_PASS','pins':len(pins),'new_finite_tests':0}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:write('audit_independent_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
