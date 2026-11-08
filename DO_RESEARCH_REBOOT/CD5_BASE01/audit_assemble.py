"""Assemble a universal case proof object; no solver or instance enumeration."""
import json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent
R=B.parent
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(n,d):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(d,f,indent=2)
def affine(name,ge,eq,mg,me,goal):
    return {'name':name,'ge':ge,'eq':eq,'ge_multipliers':mg,'eq_multipliers':me,'goal':goal}
def main():
    restricted=read(R/'RESTRICTED_CD_STEP04/RESTRICTED_CD_CERTIFICATE.json')
    assert restricted['Step04_closed'] and restricted['mandatory_open_dependencies']==[]
    o={
      'status':'ASSEMBLED_AWAITING_SEPARATE_AUDIT',
      'theorem':'forall original reachable fully closed gamma: |G(gamma)|<=5 implies Q_B(gamma)<=2A(gamma)',
      'domain':{'finite_ordered_key_set':'arbitrary','ambient_size':'arbitrary',
        'word_length':'arbitrary finite','reachability':'from some common-tree diagonal',
        'cycle_start_must_be_diagonal':False,'closure':'both full labeled trees',
        'genuine_KEEP_support_max':5,'KEEP_DELETE':True,'all_requests_present':True,
        'DELETE_freezes_B_and_removes_no_key':True,'DELETE_support_unrestricted':True,
        'zero_cost_and_nongenuine_KEEP':True,'primitive_and_nonprimitive':True,
        'fringe_and_relabeling':'arbitrary original admissible','new_population_or_mask_restriction':False},
      'costs':{'depth':'edge depth; root0','A':'sum ceil(d_A/2)',
               'Q_B':'sum floor(d_B/2) on KEEP; DELETE0','LT_cost_substituted':False},
      'normalization':{'G_empty':'all B charges zero',
        'G_nonempty':'M_KEEP=G by cyclic latest-genuine-root provenance',
        'nongenuine_KEEP_A_cost_retained':True,'cyclic_seam_uses_full_B_closure':True},
      'geometry':{'definition':'C_M(B)=union of root-to-mark paths',
        'marked_step':'C_M(B_next) subset C_M(B)',
        'closed_walk':'one fixed full labeled core S',
        'visited_mark_bound':'|S|<=2|M|-1','five_key_core_interval':[5,9],
        'whole_walk_branches':['core<=8 throughout','core=9 throughout'],
        'old_label_swap_claim_used':False},
      'partition':{'domain':[0,5],'integer':True,'branches':[
        {'interval':[0,0],'leaf':'zero'},
        {'interval':[1,3],'leaf':'RT2'},
        {'interval':[4,4],'leaf':'K4'},
        {'interval':[5,5],'leaf':'five_split'}],
        'five_split':{'domain':[5,9],'integer':True,'branches':[
          {'interval':[5,8],'leaf':'K5_LOW'},{'interval':[9,9],'leaf':'K5_CORE9'}]}},
      'leaf_conclusions':{k:'Q_B<=2A' for k in ('zero','RT2','K4','K5_LOW','K5_CORE9')},
      'dependencies':[
        {'id':'physical_semantics','uses':[]},
        {'id':'RT2','uses':[]},{'id':'K4','uses':[]},{'id':'K5_LOW','uses':[]},{'id':'K5_CORE9','uses':[]},
        {'id':'support_normalization','uses':['physical_semantics']},
        {'id':'core_geometry','uses':['physical_semantics','K4']},
        {'id':'CD5','uses':['support_normalization','core_geometry','RT2','K4','K5_LOW','K5_CORE9']}],
      'affine_proof_schemas':[
        affine('zero_G', [{'A':1}],[{'Q':1}],[2],[-1],{'A':2,'Q':-1}),
        affine('charge_chain',[{'Ck':2,'Q':-1},{'Cx':1,'Ck':-1},{'A':1,'Cx':-1}],[],[1,2,2],[],{'A':2,'Q':-1}),
        affine('visited_core_base',[],[{'v':1,'1':-1},{'c':1,'1':-1}],[],[2,-1],{'v':2,'c':-1,'1':-1}),
        affine('visited_core_new_mark',[{'v':2,'c':-1,'1':-1},{'c':1,'1':2,'next_c':-1}],
               [{'next_v':1,'v':-1,'1':-1}],[1,1],[2],{'next_v':2,'next_c':-1,'1':-1}),
        affine('visited_core_revisit',[{'v':2,'c':-1,'1':-1},{'c':1,'next_c':-1}],
               [{'next_v':1,'v':-1}],[1,1],[2],{'next_v':2,'next_c':-1,'1':-1}),
        affine('five_core_upper',[{'k':2,'c':-1,'1':-1}],[{'k':1,'1':-5}],[1],[-2],{'1':9,'c':-1})],
      'new_finite_tests':0,'new_solver_queries':0,'new_original_root_queries':0,
      'completed_semantic_checks_replayed':0,'whole_walk_leaf_selection':True,
      'mixes_leaf_potentials_or_weights':False,'unrestricted_CD_proved':False,
      'Dynamic_Optimality_proved':False,'Bank25':25}
    assert time.process_time()<float(sys.argv[1])
    write('assembly.json',o)
    print(json.dumps({'status':'CD5_CASE_PROOF_ASSEMBLED','new_finite_tests':0,'new_solver_queries':0}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:write('audit_assemble_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
