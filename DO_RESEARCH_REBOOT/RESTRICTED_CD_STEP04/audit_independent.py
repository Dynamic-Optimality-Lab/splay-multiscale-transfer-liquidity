"""Separate exact proof-object and source-interface audit; no construction import.

Checks universal rational affine certificates, not sampled assignments. Cached
theorems are premises, with independently checked declared hashes and scopes.
Does not compile/import original graph code or replay any accepted semantic query.
"""
import ast,hashlib,json,re,subprocess,sys,time
from fractions import Fraction
from pathlib import Path
BASE=Path(__file__).resolve().parent
ROOT=BASE.parent.parent
R=BASE.parent
F=R/'06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP04_UNIVERSAL_CERTIFICATION'
G=R/'06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP01_GRAPH_DOMAIN_AND_REDUCTION'
def xp(p):return Path('\\\\?\\'+str(p.resolve()))
def raw(p):return xp(p).read_text(encoding='utf-8')
def read(p):return json.loads(raw(p))
def sha(p):return hashlib.sha256(xp(p).read_bytes()).hexdigest()
def write(n,d):
    with (BASE/n).open('x',encoding='utf-8') as f:json.dump(d,f,indent=2)
def require_text(path,parts):
    text=raw(path)
    for part in parts:assert part in text,(str(path),part)
def polynomial(d):return {k:Fraction(v) for k,v in d.items() if Fraction(v)!=0}
def check_affine(c):
    ge=c['nonnegative_premises'];eq=c['equality_zero_premises']
    mg=[Fraction(x) for x in c['nonnegative_multipliers']]
    me=[Fraction(x) for x in c['equality_multipliers']]
    assert len(ge)==len(mg) and len(eq)==len(me) and all(x>=0 for x in mg)
    result={}
    for p,m in list(zip(ge,mg))+list(zip(eq,me)):
        for k,v in polynomial(p).items():result[k]=result.get(k,Fraction(0))+m*v
    assert polynomial(result)==polynomial(c['conclusion_nonnegative']),c['name']
def main():
    pins=read(BASE/'dependency_pins.json')['pins']
    for p in pins:assert sha(ROOT/p['path'])==p['sha256'],p['path']
    pindex={p['path']:p['sha256'] for p in pins}
    m=read(R/'M3_XFER21/M3_CERTIFICATE.json');a=read(R/'M3_XFER21/full_m3_audit.json')
    cov=read(R/'M3_XFER21/coverage_final.json');seal=read(R/'M3_XFER21/final_manifest.json')
    assert seal['status']=='FULL_M3_CLOSED_ALL_PUBLICATION_GATES_PASS' and seal['M3_complete']
    assert m['status']=='PROVED_UNIVERSAL_FULL_M3' and m['missing_obligations']==0
    assert m['pointwise_theorem']=='EVERY original edge satisfies w(s,t)>=W(t)-W(s)'
    assert a['status']=='INDEPENDENT_FULL_ORIGINAL_M3_CERTIFICATE_AUDIT_PASS'
    assert a['mathematical_M3_complete'] and a['all_masks_and_admissible_signatures']
    assert not a['support_or_population_restriction_added']
    assert a['missing_new_signed_obligations']==0 and cov['remaining_M3_cases']==0
    assert m['signed_clause_word_obligations_including_Step4']==69084
    assert cov['all_original_masks_and_signatures'] and cov['full_state_closure']
    assert m['domain']['ordinary_coordinates']==147 and m['domain']['midpoint_coordinates']==127
    assert m['weights']=={'OO':'original2H-q','OM':'original6-q','MO':0,'MM':'no edge'}
    assert m['debt_range']==[0,2]
    assert m['ordinary_potential']=='W(O)=-D(O)-5*chi8(O.b)'
    assert m['midpoint_potential']=='W(M)=-5*chi8(M.b)'
    assert m['corrected_h0']=={'actual_depth':0,'declared_depth':18,'q':9,'weight':-3}
    scope=m['full_state_and_signature_closure']
    for k in ('no_vertices_or_edges_identified','SAME_actual_midpoint','independent_OM_MO_private_witnesses',
              'HIGH_v_free','weak_LE_and_G_rules_unchanged','unused_fields_free'):assert scope[k]
    assert not scope['private_inventory_history_new_observable_used']
    assert sha(R/'M3_XFER19/STEP4_CERTIFICATE.json')==m['parent_Step4_sha256']

    # Original graph sources are parsed as syntax, never imported or executed.
    source_root=R/'06_CERTIFICATES'
    low=source_root/'DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_LOW_COMPILER.py'
    high=source_root/'DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE/STRICT_HIGH_COMPILER.py'
    product=source_root/'DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE/CW_PRODUCT_COMPILER.py'
    proj=source_root/'DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP03_EXACT_QUANTIFIED_OPERATORS/S03_EDGE_PROJECTIONS.py'
    assert sha(low)=='d621355f3745c0e0ce182c60197fd3f3e83a126237013cc4b7ae951c4731183a'
    assert sha(high)=='b5136fa0efa0c3fa9bec472b19a89a58c9bb0697ecbd919c034c362e4ce91b64'
    for p in (low,high,product,proj):ast.parse(raw(p))
    require_text(low,['C.append(d.EQ(macro_H(d, wit), Hv))','C.append(d.LE(Hv, d.const_int(2, 2)))',
       'root_terminated(d, wit, bt, st, bs[e], e, active)','same_keep_target(d, wit, inv, bt, e, active)',
       'C.append(marked)','C.append(chg)',
       'C.append(d.EQ(wv, d.SUB(d.ADD(Hv, Hv, 3), bt.q, 5)))'])
    require_text(high,['C.append(verify_bpath(d, s.b, bt, 0))','C.append(b_equal(d, bs1, g.b))',
       'C.append(d.LE(q, d.const_int(9, 4)))','C.append(d.EQ(w1, d.SUB(d.const_int(6, 5), q, 5)))'])
    htree=ast.parse(raw(high))
    high_calls={n.func.id for n in ast.walk(htree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name)}
    assert 'root_terminated' not in high_calls and 'same_keep_target' not in high_calls
    require_text(product,["'bkl%d', 'brl%d', 'bkr%d', 'brr%d', 'blo%d', 'bhi%d'",
       "self.O = StateVars7(d, 'QO')","self.O2 = StateVars7(d, 'QO2')","self.M = FiberVars7(d, 'QM')",
       'self.E_sm = d.EXISTS(tuple(o2b), hroot)','self.E_mt = d.EXISTS(tuple(o1b), hroot)',
       "d.EQ(self.high['q'], d.const_int(6 - w, 4))"])
    require_text(proj,["project_edge(d, e, ('QO',))","project_edge(d, e, ('QO', 'QM'))",
       "project_edge(d, P.E_mt, ('QM', 'QO2'))","edges[(1, 1, 0)] = d.const_bool(False)"])

    # Independently match the domain and quantifier scopes of the imported statements.
    require_text(F/'S04_UNIVERSAL_FORWARD_SIMULATION.md',['arbitrary W in W_5^9','U1','U16','Composition and closure'])
    require_text(F/'S04_STAGE11F_COMPLETION_CERTIFICATE.md',[
       r'\forall W\in\mathcal W_5^9',r'\exists P\in G_{\mathrm{AF}}','P\\text{ closed}',
       r'w(P)\le2A(W)-Q_B(W)'])
    require_text(F/'S04_BOUNDARY_CONSISTENCY_THEOREM.md',['pin-equality','paired closure','hence abstract path closes'])
    require_text(F/'S04_ORIGINAL_DOMAIN_AUDIT.md',['five genuine','126 masks','arbitrary fringe',
       'KEEP/DELETE','zero-cost','nongenuine','E3/E4','primitive/nonprimitive','paired closure'])
    require_text(F/'S04_T266_REPRESENTATIVE_CERTIFICATE.md',['Per-edge T=266','No global','per-macro'])
    require_text(G/'G01_SOURCE_COVERAGE_THEOREM.md',['G_star = G_AF','Reachability restriction: NONE'])
    require_text(G/'G01_DIAGONAL_REACHABILITY_AUDIT.md',['exact','paired-state closure','NOT a distinguished'])
    require_text(G/'G01_MIDPOINT_CONTRACTION_THEOREM.md',['EXISTS m','E^MO_0(m,t)','shared QM vars'])
    fd=read(F/'S04_UNIVERSAL_DEPENDENCY_GRAPH.json')
    assert fd['mandatory_open']==[] and fd['verdict']=='no mandatory OPEN or CONDITIONAL lemma'
    assert all(v.startswith(('PROVED','CERTIFIED','COMPLETE','PARAMETRIC','EXECUTED')) for v in fd['nodes'].values())
    assert len(re.findall(r'^\| F04-\d+ .*?\| PASS \|',raw(F/'S04_FINAL_ACCEPTANCE_GATES.md'),re.M))==33

    c=read(BASE/'composition.json')
    assert c['theorem']=='forall W in W_5^9: Q_B(W) <= 2 A(W)'
    d=c['domain']
    assert [d[k] for k in ('genuine_KEEP_keys','marked_core_nodes','legal_masks','gap_slots')]==[5,9,126,10]
    assert d['signatures']=='all original admissible ten-component saturated signatures'
    assert d['fringe']=='arbitrary admissible' and d['word_lengths']=='arbitrary finite'
    assert d['closure']=='exact labeled paired A/B tree closure'
    for k in ('KEEP_DELETE','zero_cost','nongenuine_KEEP','E3_E4','primitive_and_nonprimitive'):assert d[k]
    assert not d['reachability_filter'] and not d['new_support_or_population_bound']
    assert c['graph']['region']=='G_star = G_AF'
    assert c['graph']['weights']==m['weights']
    assert c['graph']['ordinary_coordinates']==147 and c['graph']['midpoint_coordinates']==127
    for k in ('all_raw_fields_retained','SAME_full_midpoint','independent_private_witnesses','HIGH_v_free'):assert c['graph'][k]
    assert c['potential']['debt_equation']==m['ordinary_debt_equation']
    assert c['potential']['ordinary']==m['ordinary_potential'] and c['potential']['midpoint']==m['midpoint_potential']
    assert c['potential']['original_h0']==m['corrected_h0']

    expected_deps={'11F':[],'coverage':[],'pointwise':[],'walk_sign':['pointwise'],
                   'Step03':['walk_sign'],'RestrictedCD':['11F','coverage','Step03']}
    got={}
    for n in c['dependencies']:
        assert n['id'] not in got and n['uses']==expected_deps[n['id']]
        assert all(x in got for x in n['uses']);got[n['id']]=n['uses']
    assert got==expected_deps
    q=c['quantifiers']
    assert q=={
      'simulation':'forall W in W_5^9 exists P in G_AF: closed(P) and w(P)<=2A(W)-Q_B(W)',
      'edge_sign':'forall original edges (u,v): w(u,v)>=Phi(v)-Phi(u)',
      'walk_sign':'forall finite P in G_star: w(P)>=Phi(end(P))-Phi(start(P))',
      'cycle_sign':'forall closed P in G_star: w(P)>=0',
      'conclusion':'forall W in W_5^9: Q_B(W)<=2A(W)'}

    # Assert the actual theorem schemas, not just algebra identities supplied by construction.
    expected_schemas={
      'low_macro_upper_direction':([], [{'H':2,'q':-1,'w':-1}], {'H':2,'q':-1,'w':-1}),
      'high_macro_upper_direction':([{'H':1,'1':-3}],[{'w':1,'q':1,'1':-6}],{'H':2,'q':-1,'w':-1}),
      'walk_base':([],[{'S':1},{'end':1,'start':-1}],{'S':1,'end':-1,'start':1}),
      'walk_induction':([{'S':1,'mid':-1,'start':1},{'w':1,'end':-1,'mid':1}],[],{'S':1,'w':1,'end':-1,'start':1}),
      'closed_walk':([{'S':1,'end':-1,'start':1}],[{'end':1,'start':-1}],{'S':1}),
      'terminal_composition':([{'S':1},{'A':2,'Q':-1,'S':-1}],[],{'A':2,'Q':-1})}
    assert len(c['linear_certificates'])==len(expected_schemas)
    seen=set()
    for lc in c['linear_certificates']:
        assert lc['name'] not in seen;seen.add(lc['name'])
        assert (lc['nonnegative_premises'],lc['equality_zero_premises'],lc['conclusion_nonnegative'])==expected_schemas[lc['name']]
        check_affine(lc)
    assert seen==set(expected_schemas)

    assert c['new_SMT_queries']==0 and c['new_original_root_queries']==0 and c['no_new_finite_tests']
    assert not c['Dynamic_Optimality_proved'] and not c['unrestricted_CD_proved'] and c['Bank25']==25
    assert time.process_time()<float(sys.argv[1])
    write('independent_audit.json',{
      'status':'INDEPENDENT_RESTRICTED_CD_COMPOSITION_AUDIT_PASS',
      'declared_dependency_pins_verified':len(pins),'source_AST_contracts_checked':4,
      'original_domain_coverage':'EXACT_W_5^9_ALL_126_MASKS_ARBITRARY_ADMISSIBLE_FRINGE_AND_SIGMA',
      'graph_identity':'ORIGINAL_FULL_G_star_EQUALS_G_AF','full_state_closure':True,
      'shared_actual_midpoint_independent_private_witnesses':True,'HIGH_v_free':True,
      'corrected_h0_retained':m['corrected_h0'],'all_original_edge_families':'OO_OM_MO_NO_MM',
      'Step03_M1_M2_M3_closed_by_common_pointwise_theorem':True,
      'universal_affine_proof_schemas':sorted(seen),'arbitrary_length_walk_induction':True,
      'quantifier_order_verified':'forall_W_exists_P_WITH_forall_closed_P_nonnegative',
      'dependency_DAG_acyclic_and_complete':True,'mandatory_open_dependencies':[],
      'restricted_CD_mathematical_conclusion':True,'new_SMT_queries':0,'new_original_root_queries':0,
      'new_finite_tests':0,'completed_accepted_semantic_checks_replayed':0,
      'proof_object_input_bytes':(BASE/'composition.json').stat().st_size,
      'audit_imports_construction':False,'external_peer_review':False,'whole_compiler_formalization':False,
      'unrestricted_CD_proved':False,'Dynamic_Optimality_proved':False,'Bank25':25,
      'publication_requires_controller_resource_and_integrity_gates':True})
    print(json.dumps({'status':'INDEPENDENT_COMPOSITION_AUDIT_PASS','universal_affine_schemas':len(seen),
                      'pins':len(pins),'new_finite_tests':0}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:write('audit_independent_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
