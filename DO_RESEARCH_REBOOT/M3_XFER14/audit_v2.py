"""Universal term/linear-algebra/coverage audit. NO finite model tests.

BLOCK leaves are universally quantified. Only proof-index labels are
generated. No original compiler, state, DAG, source root or psi is run.
"""
import hashlib,json,sys,time
from pathlib import Path
BASE=Path(__file__).resolve().parent
CAP=min(120.0,float(sys.argv[1]))
EMPTY=('EMPTY',)

def write(name,obj):
    with (BASE/name).open('x',encoding='utf-8') as stream:json.dump(obj,stream,indent=2)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def V(n):return ('BLOCK',n)
def N(k,l=EMPTY,r=EMPTY):return ('NODE',k,l,r)
def rz(t):
    assert t[0]=='NODE' and t[2][0]=='NODE'
    a=t[2];return N(a[1],a[2],N(t[1],a[3],t[3]))
def lz(t):
    assert t[0]=='NODE' and t[3][0]=='NODE'
    a=t[3];return N(a[1],N(t[1],t[2],a[2]),a[3])
def at(t,p):
    for d in p:
        assert t[0]=='NODE';t=t[2+d]
    return t
def put(t,p,v):
    if not p:return v
    return N(t[1],put(t[2],p[1:],v),t[3]) if p[0]==0 else N(t[1],t[2],put(t[3],p[1:],v))
def pair(t,p):
    if p==(0,0):return rz(rz(t))
    if p==(1,1):return lz(lz(t))
    if p==(0,1):return rz(N(t[1],lz(t[2]),t[3]))
    assert p==(1,0);return lz(N(t[1],t[2],rz(t[3])))
def splay(t,p):
    while len(p)>=2:
        pre=p[:-2];t=put(t,pre,pair(at(t,pre),p[-2:]));p=pre
    return (rz(t) if p==(0,) else lz(t)) if p else t
def opposite(t):
    # Identity in the opposite constructor direction; not a private-state
    # or numerical-potential reflection.
    return N(t[1],opposite(t[3]),opposite(t[2])) if t[0]=='NODE' else t
def path(t,k,p=()):
    if t[0]!='NODE':return None
    if t[1]==k:return p
    q=path(t[2],k,p+(0,))
    return q if q is not None else path(t[3],k,p+(1,))
def depth(t,k):
    p=path(t,k);assert p is not None;return len(p)
def lin(*parts):
    out={}
    for part in parts:
        for key,value in part.items():out[key]=out.get(key,0)+value
    return {k:v for k,v in out.items() if v}

def main():
    A,B,C,D,E,F,G,T,R=map(V,('A','B','C','D','E','F','G','T','R'))
    identities=[]
    def cert(name,source,p,expected):
        assert splay(source,p)==expected,name
        identities.append(name)
        assert splay(opposite(source),tuple(1-d for d in p))==opposite(expected),name+'_opposite'
        identities.append(name+'_actual_opposite_primitives')

    # The variable labels are distinct actual core roles, not assigned
    # numerical states. All side terms remain free.
    s4=N('r',N('p',N('q',N('u',N('extreme',A,B),C),D),E),F)
    t4=N('extreme',A,N('p',N('u',B,N('q',C,D)),N('r',E,F)))
    cert('H1_extreme_depth4_mandatory_fork',s4,(0,0,0,0),t4)
    assert at(t4,(1,0))[1]=='u' and at(t4,(1,1))[1]=='r'
    s5=N('r',N('p',N('q',N('u',N('v',N('extreme',A,B),C),D),E),F),G)
    t5=N('extreme',A,N('r',N('q',N('v',B,N('u',C,D)),N('p',E,F)),G))
    cert('H1_extreme_depth5_mandatory_fork',s5,(0,0,0,0,0),t5)
    assert at(t5,(1,0,0))[1]=='v' and at(t5,(1,0,1))[1]=='p'

    # Expanded B h=2. The helper is an actual proxy leaf. Other proxies
    # are contained in the arbitrary T/R blocks; only core counts are used.
    bsource=N('r',N('extreme',N('helper'),T),R)
    btarget=N('helper',EMPTY,N('extreme',EMPTY,N('r',T,R)))
    cert('Gamma1_helper_B_depth2_exact',bsource,(0,0),btarget)
    assert depth(bsource,'helper')==2 and depth(btarget,'extreme')==1 and depth(btarget,'r')==2
    # Last-zig parent identity for any odd terminal depth after bottom pairs.
    cert('Gamma1_last_zig_parent',N('helper',EMPTY,N('terminal',A,B)),(1,),
         N('terminal',N('helper',EMPTY,A),B))

    # Complete A helper words at the minimum end and opposite end.
    helper_terms=[
      ('L',N('r',N('f',A,B),C),(0,),N('f',A,N('r',B,C))),
      ('LL',N('r',N('p',N('f',A,B),C),D),(0,0),N('f',A,N('p',B,N('r',C,D)))),
      ('LR',N('r',N('p',A,N('f',B,C)),D),(0,1),N('f',N('p',A,B),N('r',C,D))),
    ]
    for name,s,p,t in helper_terms:cert('minimum_helper_A_'+name,s,p,t)

    hidden=[
      ('LL',N('r',N('p',N('f',A,N('y',B,C)),D),E),(0,0),
        N('y',N('f',A,B),N('p',C,N('r',D,E)))),
      ('LR',N('r',N('p',A,N('f',B,N('y',C,D))),E),(0,1),
        N('y',N('f',N('p',A,B),C),N('r',D,E))),
    ]
    hidden_depths=[]
    for name,s,p,t in hidden:
        mid=splay(s,p)
        assert depth(s,'f')==2 and depth(s,'y')==3 and path(mid,'y')==(1,0)
        assert splay(mid,(1,0))==t,name
        os=opposite(s);op=tuple(1-d for d in p);om=splay(os,op)
        assert depth(os,'y')==3 and path(om,'y')==(0,1)
        assert splay(om,(0,1))==opposite(t)
        identities.extend(['hidden_two_charge_'+name,'hidden_two_charge_'+name+'_actual_opposite_primitives'])
        hidden_depths.append({'minimum_helper':name,'minimum_source_terminal_path':''.join('LR'[d] for d in path(s,'y')),
          'maximum_helper':''.join('LR'[d] for d in op),'maximum_source_terminal_path':''.join('LR'[d] for d in path(os,'y')),
          'original_A_depth':3,'post_helper_A_depth':2,'negative_H1_source_cap1_claimed':False})

    # Opposite-side visible terminal block. For LL it is too deep, for
    # L/LR it can be charge1-eligible only at its block root (old R).
    opposing=[
      ('L',N('r',N('f',A,B),N('y',C,D)),(0,),2),
      ('LL',N('r',N('p',N('f',A,B),C),N('y',D,E)),(0,0),3),
      ('LR',N('r',N('p',A,N('f',B,C)),N('y',D,E)),(0,1),2),
    ]
    for name,s,p,expected_depth in opposing:
        assert path(s,'y')==(1,)
        assert depth(splay(s,p),'y')==expected_depth
        assert depth(splay(opposite(s),tuple(1-d for d in p)),'y')==expected_depth

    # Algebraic certificates, rather than checking assigned D/psi values.
    # Each dictionary variable denotes a nonnegative quantity.
    slacks={
      'Gamma1_h1_zero_parallel_negative':lin({'parallel_negative_residual':1},{'one':1}),
      'zero_source0':{'target_debt':1},
      'zero_target2':{'source_room_to2':1},
      'zero_equal1':lin({'one':1},{'one':-1}),
      'negative_H1_source_upper1':lin({'parallel_target_room_to2':1,'negative_residual':1}),
      'seed_max_both_terms_below_target':{'source_to_target_room':1},
    }
    assert all(v>=0 for poly in slacks.values() for v in poly.values())
    assert slacks['zero_equal1']=={}
    # Root counts derived from arbitrary-subtree core populations. Roots
    # outside frontier have POSITIVE slack below terminal8, with no census.
    count_certificates={
      'MIN_T_bound':{'root_coefficient':1,'constant':1},
      'MIN_R_bound':{'root_coefficient':-1,'constant':10},
      'MAX_L_bound':{'root_coefficient':1,'constant':2},
      'MAX_T_bound':{'root_coefficient':-1,'constant':9},
      'MIN_central_T_8minusBound':lin({'constant':8},{'constant':-1,'root':-1}),
      'MIN_central_R_8minusBound':lin({'constant':8},{'constant':-10,'root':1}),
      'MAX_central_L_8minusBound':lin({'constant':8},{'constant':-2,'root':-1}),
      'MAX_central_T_8minusBound':lin({'constant':8},{'constant':-9,'root':1}),
    }
    assert count_certificates['MIN_central_T_8minusBound']=={'constant':7,'root':-1}
    assert count_certificates['MIN_central_R_8minusBound']=={'constant':-2,'root':1}
    assert count_certificates['MAX_central_L_8minusBound']=={'constant':6,'root':-1}
    assert count_certificates['MAX_central_T_8minusBound']=={'constant':-1,'root':1}
    count_certificates['MIN_central_T_positive_slack']={'one':1,'room_below6':1}
    count_certificates['MIN_central_R_positive_slack']={'one':1,'room_above3':1}
    count_certificates['MAX_central_L_positive_slack']={'one':1,'room_below5':1}
    count_certificates['MAX_central_T_positive_slack']={'one':1,'room_above2':1}
    assert all(value>=0 for name,expr in count_certificates.items() if name.endswith('positive_slack') for value in expr.values())
    # Under MIN r in[3,6], both 7-r and r-2 >=1.
    # Under MAX r in[2,5], both 6-r and r-1 >=1.
    # Solving each affine bound>=8 gives the frontier directly.

    # Reuse compiled original semantics by hashes, without executing them.
    old9=BASE.parent/'M3_XFER09/symbolic_audit.json'
    old12=BASE.parent/'M3_XFER12/symbolic_audit.json'
    reader=json.loads(old9.read_text())
    assert reader['status']=='INTERVAL_CHILD_UNIVERSAL_SYMBOLIC_AUDIT_PASS'
    prev=json.loads(old12.read_text())
    assert prev['status']=='DEPTH_FIVE_CENTRAL_RELAY_UNIVERSAL_SYMBOLIC_AUDIT_PASS'
    source_hashes={**reader['source_hashes'],**prev['new_AST_source_hashes']}
    for p,h in source_hashes.items():assert digest(Path(p))==h,p

    filenames=['SATURATION_THEOREM.md','CUT_PAIR_THEOREM.md','BURIED_CUT_THEOREM.md',
      'RELEASE_CAPACITY_THEOREM.md','RR_RELEASE_THEOREM.md','ANONYMOUS_RELEASE_THEOREM.md',
      'DIRECT_BARRIER_THEOREM.md','BURIED_BARRIER_THEOREM.md','INTERVAL_CHILD_THEOREM.md',
      'GRANDCHILD_THEOREM.md','MARKED_RELAY_THEOREM.md','DEPTH_FIVE_RELAY_THEOREM.md',
      'NON_EXTREMAL_EXPOSURE_THEOREM.md']
    preservation_keys={2:'each_previously_valid_original_LOW_inequality_preserved',
      3:'each_previously_valid_LOW_inequality_preserved',
      4:'each_previously_valid_original_LOW_inequality_preserved'}
    preservation_keys.update({i:'each_previously_valid_original_LOW_row_preserved' for i in range(5,11)})
    preservation_keys.update({i:'each_previously_valid_LOW_row_preserved_by_each_operation' for i in range(11,14)})
    scopes=[
      'Q source rows; incoming only under stated debt/target-cap qualifications',
      'R source rows; incoming only under stated qualifications',
      'T/L cut source rows and protected incoming exactly as stated',
      'release-capacity J source rows and protected incoming exactly as stated',
      'Z source rows; auxiliary K/C rows only under their stated stage/source-credit conditions',
      'N source rows; all auxiliary/protected rows under their exact hypotheses',
      'G7 source rows; auxiliary one-credit rows only under their stage/source-credit conditions',
      'GB source rows; complete S zero frontier; auxiliary rows retain stage/source-credit conditions',
      'interval I source rows and protected incoming exactly as stated',
      'unmarked-ancestor Z source rows and protected incoming exactly as stated',
      'marked-relay J/G source rows; one-credit auxiliaries retain source-credit conditions',
      'depth-five named main source regions at cap2; auxiliaries retain source-credit conditions',
      'T/G source rows; H/CA/CB/R newly-raised-source1 rows; EB/ER no actual source changes; qualified incoming only',
    ]
    registry=[];lineage=[];reused_paths=[old9,old12]
    for i,(fn,scope) in enumerate(zip(filenames,scopes),1):
        d=BASE.parent/f'M3_XFER{i:02}'
        cp=d/'certificate.json';c=json.loads(cp.read_text())
        assert c['R1_R4_preserved'] and (c.get('h0_correction_preserved') or c.get('corrected_h0_preserved'))
        if i==1:assert 'preserves each previously valid H1 inequality' in c['original_H1_augmentation']
        else:assert c[preservation_keys[i]],(i,preservation_keys[i])
        if i==8:assert c['Gamma1_weight0_or_plus1_implies_helper_initial_B_depth_at_most']==2
        if i==13:assert not c['all_already_debt2_auxiliary_sources_claimed_solved']
        p=d/fn;assert p.exists()
        registry.append({'id':f'OLD_XFER{i:02}','theorem':p.as_posix(),'sha256':digest(p),
          'membership':'ALL hypotheses of the cited row theorem, including its stages/source-credit qualification',
          'scope_index':scope,'propagated_to':'unchanged current D_exp through individually row-preserving later operations',
          'different_potential_signature_assignments_imported':False})
        lineage.append({'campaign':i,'individual_H1_preservation':True,'certificate':cp.as_posix(),'sha256':digest(cp)})
        reused_paths.extend([p,cp])
    for name in ('M3_E1_01/OUTSIDE_E1.md','M3_E1_01/E1_THEOREM.md','M3_E1_01/certificate.json',
      'M3_EXPOSURE02/HELPER_REDUCTION.md','M3_EXPOSURE02/certificate.json','M3_XFER08/PROOF_AUDIT.md'):
        p=BASE.parent/name;assert p.exists();reused_paths.append(p)

    cells=[]
    for label,ps,lt,drops in [('S10',1,0,[[1,0],[2,0],[2,1]]),('S20',2,0,[[2,0],[2,1]]),('S21',2,1,[[2,1]])]:
        for bd in (4,5):
            for ap in ('L','R','LL','LR','RL','RR'):
                cells.append({'id':f'H1-{label}-B{bd}-{ap}','normal_form':'H1','status':'OPEN',
                  'psi_source':ps,'Lambda_target':lt,'B_depth':bd,'actual_A_word':ap,
                  'source_core_height_at_most':7 if ps==1 else 5,'target_core_height_at_most':7,
                  'c_source_strictly_below_psi_source':True,'current_debt_drop_options':drops,
                  'remaining_quantifiers':'ALL original masks, cores, parent/root mark/types, exposures, G/raw fields, sigma and compatible independent private witnesses',
                  'closure_needed':'exclude this original-constraint debt-drop formula, or give a source-valid exact row refuting current D_exp',
                  'nonemptiness_asserted':False})
    visible=[('MIN',1,'above_root',6,'R'),('MIN',2,'above_root',6,'R'),
      ('MIN',7,'between_extreme_root',7,'actual_depth1_or2'),('MIN',8,'between_extreme_root',7,'actual_depth1_or2'),
      ('MAX',6,'below_root',6,'L'),('MAX',7,'below_root',6,'L'),
      ('MAX',0,'between_root_extreme',7,'actual_depth1_or2'),('MAX',1,'between_root_extreme',7,'actual_depth1_or2')]
    for side,root,ts,bd,ap in visible:
        cells.append({'id':f'G1-{side}-V-r{root}','normal_form':'Gamma1','status':'OPEN',
          'helper_side':side,'source_core_root':root,'terminal_side':ts,'source_B_terminal_depth':bd,
          'source_A_terminal':ap,'helper_source_B_depth':2,'preterminal_B_depth':8,
          'initial_helper_Score_support':'bearing','source_D_at_most':1,'current_debt_drop_options':[[1,0]],
          'closure_needed':'prove destination D>=1 whenever source D=1 on the entire original profile',
          'nonemptiness_asserted':False})
    for side,roots,helpers,child in [('MIN',(7,8),('LL','LR'),'right'),('MAX',(0,1),('RR','RL'),'left')]:
        for root in roots:
            for helper in helpers:
                cells.append({'id':f'G1-{side}-H-r{root}-{helper}','normal_form':'Gamma1','status':'OPEN',
                  'helper_side':side,'source_core_root':root,'actual_A_helper':helper,
                  'source_A_terminal':helper+('R' if child=='right' else 'L'),'source_A_terminal_depth':3,
                  'terminal_is_helpers_child':child,'source_B_terminal_depth':7,'helper_source_B_depth':2,
                  'preterminal_B_depth':8,'initial_helper_Score_support':'bearing',
                  'source_D_at_most':2,'current_debt_drop_options':[[1,0],[2,0],[2,1]],
                  'closure_needed':'prove signed debt preservation on entire original hidden-terminal profile',
                  'nonemptiness_asserted':False})
    assert len(cells)==52 and len({c['id'] for c in cells})==52
    assert sum(c['normal_form']=='H1' for c in cells)==36
    assert sum(c['normal_form']=='Gamma1' for c in cells)==16
    assert all(c['status']=='OPEN' and not c['nonemptiness_asserted'] for c in cells)
    # This list is an index of universal formulas, NOT a state enumeration
    # or finite test whose success could establish their inequalities.
    partition={'definition':'ZERO_PARTITION.md','exhaustive_case_definition':True,
      'public_edge_disjointness':'project normalized witnessed cases, then subtract all earlier projections',
      'priority_closed':['exact old theorem scopes K','Gamma0 global floor','H1 seed-safe',
        'H1 target-height8 impossible','Gamma1 helper-depth>=3 impossible','Gamma1 terminal-depth9 impossible',
        'Gamma1 helper-depth1 strict signed residual>=1','Gamma1 depth2 Score-empty impossible',
        'Gamma1 depth2 central-root/wrong-side impossible','elementary integer-range signs'],
      'number_of_residual_schematic_slots':52,'all_residual_cells_closed':False,
      'no_cell_nonemptiness_asserted':True,'new_finite_tests':0,'Step4_complete':False,'cells':cells}
    write('proof_registry.json',{'fixed_potential':'D_exp from Transfer13, unchanged',
      'rule':'membership retains ALL original theorem hypotheses; no blanket source2 auxiliary claim',
      'registry':registry,'signature_certificates_using_other_potentials_retained_but_not_imported':True})
    write('partition.json',partition)
    assert time.process_time()<CAP
    result={'status':'ZERO_FRONTIER_UNIVERSAL_SYMBOLIC_AUDIT_PASS',
      'universal_constructor_identities':identities,'hidden_terminal_depth_derivations':hidden_depths,
      'nonnegative_residual_algebra':slacks,'arbitrary_subtree_core_count_certificates':count_certificates,
      'source_hashes_reused_not_executed':source_hashes,'individual_H1_preservation_lineage':lineage,
      'reused_proof_hashes':{p.as_posix():digest(p) for p in reused_paths},
      'Gamma1_helper_depth1_zero_global_signed_residual_at_least':1,
      'Gamma1_zero_terminal_depth_exact':8,'Gamma1_residual_helper_depth_exact':2,
      'Gamma1_residual_initial_Score_support':'bearing','H1_zero_target_core_height_at_most':7,
      'H1_possible_failure_seed_pairs':[[1,0],[2,0],[2,1]],
      'visible_Gamma1_source_cap':1,'hidden_Gamma1_source_cap_below2_claimed':False,
      'target_floor_inferred_from_upper_capacity':False,'all_original_quantifiers_retained':True,
      'partition_exhaustive_case_definition':True,'residual_schematic_slots':52,
      'residual_cells_closed':False,'Step4_complete':False,'M3_status':'OPEN',
      'current_potential_changed':False,'new_finite_tests':0,'new_source_transition_queries':0,
      'new_original_root_evaluations':0,'new_saved_psi_queries':0,'new_label_fits':0,'new_bank_censuses':0,
      'completed_semantic_checks_replayed':0,'original_negative_cycle_certified':False,
      'full_compiler_formalization_claimed':False,'external_human_or_model_review_claimed':False,
      'CPU_seconds':time.process_time(),'CPU_cap':CAP}
    write('symbolic_audit.json',result)
    print(json.dumps({'status':result['status'],'universal_identities':len(identities),
      'residual_schematic_slots':52,'Step4_complete':False,'new_finite_tests':0},indent=2),flush=True)

if __name__=='__main__':
    error=None
    try:main()
    except BaseException as exception:
        error={'type':type(exception).__name__,'message':str(exception)}
        raise
    finally:write('symbolic_audit_exit.json',{'whole_process_CPU_seconds':time.process_time(),'CPU_cap':CAP,'error':error})
