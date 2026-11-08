"""Construct the small universal composition proof object, without a solver."""
import json,sys,time
from pathlib import Path
BASE=Path(__file__).resolve().parent
R=BASE.parent
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(n,d):
    with (BASE/n).open('x',encoding='utf-8') as f:json.dump(d,f,indent=2)
def cert(name,ge,eq,mg,me,target):
    return {'name':name,'nonnegative_premises':ge,'equality_zero_premises':eq,
            'nonnegative_multipliers':mg,'equality_multipliers':me,'conclusion_nonnegative':target}
def main():
    m=read(R/'M3_XFER21/M3_CERTIFICATE.json')
    assert m['M3_complete'] and m['missing_obligations']==0
    assert m['pointwise_theorem']=='EVERY original edge satisfies w(s,t)>=W(t)-W(s)'
    f=R/'06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP04_UNIVERSAL_CERTIFICATION'
    assert read(f/'S04_UNIVERSAL_DEPENDENCY_GRAPH.json')['mandatory_open']==[]
    obj={
      'status':'COMPOSITION_PROOF_OBJECT_AWAITING_INDEPENDENT_AUDIT',
      'theorem':'forall W in W_5^9: Q_B(W) <= 2 A(W)',
      'domain':{'genuine_KEEP_keys':5,'marked_core_nodes':9,'legal_masks':126,'gap_slots':10,
        'signatures':'all original admissible ten-component saturated signatures',
        'fringe':'arbitrary admissible','word_lengths':'arbitrary finite',
        'closure':'exact labeled paired A/B tree closure',
        'KEEP_DELETE':True,'zero_cost':True,'nongenuine_KEEP':True,'E3_E4':True,
        'primitive_and_nonprimitive':True,'reachability_filter':False,'new_support_or_population_bound':False},
      'graph':{'region':'G_star = G_AF','ordinary_coordinates':147,'midpoint_coordinates':127,
        'weights':m['weights'],'all_raw_fields_retained':True,'SAME_full_midpoint':True,
        'independent_private_witnesses':True,'HIGH_v_free':True,'MM':'FALSE'},
      'potential':{'ordinary':m['ordinary_potential'],'midpoint':m['midpoint_potential'],
        'debt_equation':m['ordinary_debt_equation'],'debt_range':m['debt_range'],
        'chi8':m['chi8'],'original_h0':m['corrected_h0'],'fixed_current_public_state_only':True},
      'quantifiers':{
        'simulation':'forall W in W_5^9 exists P in G_AF: closed(P) and w(P)<=2A(W)-Q_B(W)',
        'edge_sign':'forall original edges (u,v): w(u,v)>=Phi(v)-Phi(u)',
        'walk_sign':'forall finite P in G_star: w(P)>=Phi(end(P))-Phi(start(P))',
        'cycle_sign':'forall closed P in G_star: w(P)>=0',
        'conclusion':'forall W in W_5^9: Q_B(W)<=2A(W)'},
      'dependencies':[
        {'id':'11F','uses':[],'kind':'imported_closed_simulation_and_upper_bound'},
        {'id':'coverage','uses':[],'kind':'imported_G_star_equals_G_AF'},
        {'id':'pointwise','uses':[],'kind':'imported_sealed_XFER21_all_original_edges'},
        {'id':'walk_sign','uses':['pointwise'],'kind':'length_induction'},
        {'id':'Step03','uses':['walk_sign'],'kind':'full_endpoint_equality'},
        {'id':'RestrictedCD','uses':['11F','coverage','Step03'],'kind':'existential_elimination_and_inequality'}],
      'linear_certificates':[
        cert('low_macro_upper_direction',[],[{'H':2,'q':-1,'w':-1}],[],[1],{'H':2,'q':-1,'w':-1}),
        cert('high_macro_upper_direction',[{'H':1,'1':-3}],[{'w':1,'q':1,'1':-6}],[2],[-1],{'H':2,'q':-1,'w':-1}),
        cert('walk_base',[],[{'S':1},{'end':1,'start':-1}],[],[1,-1],{'S':1,'end':-1,'start':1}),
        cert('walk_induction',[{'S':1,'mid':-1,'start':1},{'w':1,'end':-1,'mid':1}],[],[1,1],[],{'S':1,'w':1,'end':-1,'start':1}),
        cert('closed_walk',[{'S':1,'end':-1,'start':1}],[{'end':1,'start':-1}],[1],[1],{'S':1}),
        cert('terminal_composition',[{'S':1},{'A':2,'Q':-1,'S':-1}],[],[1,1],[],{'A':2,'Q':-1})],
      'no_new_finite_tests':True,'new_SMT_queries':0,'new_original_root_queries':0,
      'completed_semantic_checks_replayed':0,'unrestricted_CD_proved':False,
      'Dynamic_Optimality_proved':False,'Bank25':25}
    assert time.process_time()<float(sys.argv[1])
    write('composition.json',obj)
    print(json.dumps({'status':'COMPOSITION_OBJECT_WRITTEN','new_finite_tests':0,'new_solver_queries':0}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:write('audit_compose_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
