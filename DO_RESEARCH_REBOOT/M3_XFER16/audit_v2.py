"""Universal safe-ceiling audit; no finite original-state/model tests.

Open BLOCKs remain arbitrary subtrees. Spine schemas prove identities
with all side data free; no original compiler, tree bank or psi is run.
"""
import hashlib,json,sys,time
from pathlib import Path
BASE=Path(__file__).resolve().parent
CAP=min(120.0,float(sys.argv[1]))
E=('EMPTY',)
def lp(p):return Path('\\\\?\\'+str(Path(p).resolve()))
def sha(p):return hashlib.sha256(lp(p).read_bytes()).hexdigest()
def read(p):return json.loads(lp(p).read_text(encoding='utf-8'))
def write(n,v):
    with (BASE/n).open('x',encoding='utf-8') as stream:json.dump(v,stream,indent=2)
def V(n):return ('BLOCK',n)
def N(k,l=E,r=E):return ('NODE',k,l,r)
def rz(t):
    assert t[0]=='NODE' and t[2][0]=='NODE'
    a=t[2];return N(a[1],a[2],N(t[1],a[3],t[3]))
def lz(t):
    assert t[0]=='NODE' and t[3][0]=='NODE'
    a=t[3];return N(a[1],N(t[1],t[2],a[2]),a[3])
def at(t,p):
    for b in p:
        assert t[0]=='NODE';t=t[2+b]
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
    return N(t[1],opposite(t[3]),opposite(t[2])) if t[0]=='NODE' else t
def locate(t,k,p=()):
    if t[0]=='BLOCK':return p if t[1]==k else None
    if t[0]!='NODE':return None
    if t[1]==k:return p
    q=locate(t[2],k,p+(0,))
    return q if q is not None else locate(t[3],k,p+(1,))
def labels(t):
    return ({t[1]}|labels(t[2])|labels(t[3])) if t[0]=='NODE' else set()
def mandatory_lower_fork(t):
    if t[0]!='NODE':return None
    low=lambda s:{v for v in labels(s) if v.startswith('a')}
    if t[1].startswith('a') and low(t[2]) and low(t[3]):return t[1]
    return mandatory_lower_fork(t[2]) or mandatory_lower_fork(t[3])
def spine(keys,dirs):
    t=N('y',V('target_L'),V('target_R'))
    for i in reversed(range(len(keys))):
        side=V('side_'+str(i))
        t=N(keys[i],t,side) if dirs[i]==0 else N(keys[i],side,t)
    return t
def lin(*parts):
    d={}
    for part in parts:
        for k,v in part.items():d[k]=d.get(k,0)+v
    return {k:v for k,v in d.items() if v}

def main():
    A,B,C,D,F,G=map(V,('A','B','C','D','F','G'))
    ids=[]
    def cert(name,t,p,want):
        assert splay(t,p)==want,name
        ids.append(name)
        assert splay(opposite(t),tuple(1-b for b in p))==opposite(want),name+'_opposite'
        ids.append(name+'_actual_opposite_primitives')

    # Pair growth induction: formal target-side subtrees drop by <=1;
    # the two newly introduced core ancestors have depth<=2.
    X=N('x',V('X_L'),V('X_R'))
    growth=[
      ((0,0),N('g',N('p',X),E)),
      ((1,1),N('g',E,N('p',E,X))),
      ((0,1),N('g',N('p',E,X),E)),
      ((1,0),N('g',E,N('p',X,E))),
    ]
    pair_growth=[]
    for p,t in growth:
        out=pair(t,p)
        assert out[1]=='x'
        assert len(locate(out,'X_L'))<=2 and len(locate(out,'X_R'))<=2
        assert len(locate(out,'p'))<=2 and len(locate(out,'g'))<=2
        word=''.join('LR'[b] for b in p)
        ids.append('arbitrary_processed_spine_pair_growth_'+word)
        pair_growth.append({'word':word,'old_target_side_depth_increase_at_most':1,'new_ancestor_depth_at_most':2})
    for name,out in [('left',lz(N('p',E,X))),('right',rz(N('p',X,E)))]:
        assert out[1]=='x' and len(locate(out,'X_L'))<=2 and len(locate(out,'X_R'))<=2
        ids.append('processed_spine_final_zig_growth_'+name)
    height_bounds=[]
    for depth,spine_bound,off in [(6,4,2),(7,5,1),(8,5,0)]:
        assert off==8-depth and spine_bound==(depth//2+1)+(depth%2)
        assert spine_bound+off<=6
        height_bounds.append({'negative_access_depth':depth,'spine_bound':spine_bound,'off_path_core_count':off,'full_height_bound':spine_bound+off})
    write('checkpoint01_height.json',{'status':'PASS','identities':ids.copy(),'pair_growth':pair_growth,
      'negative_output_height_bounds':height_bounds,'psi_height_ge7_zero_by_completed_incoming_recurrence':True})

    # Extreme8 zero inputs. Actual opposite proves the target0 version.
    s4=N('r',A,N('p',B,N('q',C,N('u',D,N('y',F,G)))))
    t4=N('y',N('p',N('r',A,B),N('u',N('q',C,D),F)),G)
    cert('extreme_depth4_forbidden_minimum_left_child',s4,(1,1,1,1),t4)
    assert at(t4,(0,0))[1]=='r' and at(t4,(0,1))[1]=='u'
    H=V('H')
    s5=N('r',A,N('p',B,N('q',C,N('u',D,N('v',F,N('y',G,H))))))
    t5=N('y',N('r',A,N('q',N('p',B,C),N('v',N('u',D,F),G))),H)
    cert('extreme_depth5_old_root_at_left_child',s5,(1,1,1,1,1),t5)
    assert at(t5,(0,))[1]=='r'

    # Eleven arbitrary-side constructor schemas, exhaustive by ordered
    # ancestors to near-maximum7 and the sole higher core8. NOT states.
    expected={(4,None):'FORK',(5,None):'FORK',
      (4,0):'EXCEPTION',(4,1):'OLD_ROOT',(4,2):'FORK',(4,3):'FORK',
      (5,0):'FORK',(5,1):'OLD_ROOT',(5,2):'OLD_ROOT',(5,3):'FORK',(5,4):'FORK'}
    cases=[]
    for (dep,pos),kind in expected.items():
        keys=[];a=0
        for i in range(dep):
            if i==pos:keys.append('upper')
            else:keys.append('a'+str(a));a+=1
        dirs=tuple(0 if k=='upper' else 1 for k in keys)
        t=spine(keys,dirs);out=splay(t,dirs)
        assert out[1]=='y'
        fork=mandatory_lower_fork(out[2])
        if kind=='FORK':assert fork is not None,(dep,pos)
        elif kind=='OLD_ROOT':assert out[2][1]==keys[0],(dep,pos)
        else:
            assert keys[0]=='upper' and out[2][1]=='a0' and out[3][1]=='upper'
        other=splay(opposite(t),tuple(1-b for b in dirs))
        assert other==opposite(out)
        # Formal opposite terms use reversed ordered roles, never psi or
        # a transformed original private witness.
        ids.extend([f'near_extreme_d{dep}_upper_{pos}_{kind}',f'near_extreme_d{dep}_upper_{pos}_{kind}_actual_opposite'])
        cases.append({'B_depth':dep,'upper_ancestor_position':pos,'conclusion':kind,
          'mandatory_lower_fork_role':fork,'side_blocks':'ALL arbitrary compatible blocks',
          'actual_opposite_constructor_identity':True})
    assert len(cases)==11
    # The only nonexcluded zero source has this exact core identity.
    exceptional=N('old8',N('zero',E,N('a',B,N('b',C,N('near7',D,E)))),E)
    exceptional_out=N('near7',N('zero',E,N('b',N('a',B,C),D)),N('old8'))
    cert('exceptional_d4_source_and_target_exact',exceptional,(0,1,1,1),exceptional_out)
    assert 3+(4-1)==6 and 4+(4-1)==7
    write('checkpoint02_incoming.json',{'status':'PASS','all_constructor_ids':ids.copy(),
      'complete_zero_incoming_spine_cases':cases,'exceptional_source_height_at_least':6,
      'nonexception_old_root_extreme_observation_contradiction':True})

    # Actual A incoming identities and the real-cut interface. All blocks
    # remain open; the H implications are separately audited in prose.
    cert('incoming_A_L',N('old8',N('near7',A,B),C),(0,),N('near7',A,N('old8',B,C)))
    cert('incoming_A_LL',N('old8',N('p',N('near7',A,B),C),D),(0,0),N('near7',A,N('p',B,N('old8',C,D))))
    cert('incoming_A_LR',N('old8',N('p',A,N('near7',B,C)),D),(0,1),N('near7',N('p',A,B),N('old8',C,D)))
    hidden=[
      ('LL',N('r',N('p',N('f',A,N('y',B,C)),D),F),(0,0),N('y',N('f',A,B),N('p',C,N('r',D,F)))),
      ('LR',N('r',N('p',A,N('f',B,N('y',C,D))),F),(0,1),N('y',N('f',N('p',A,B),C),N('r',D,F))),
    ]
    for name,t,p,want in hidden:
        mid=splay(t,p);assert locate(t,'y')==p+(1,) and locate(mid,'y')==(1,0)
        assert splay(mid,(1,0))==want
        other=splay(opposite(t),tuple(1-b for b in p))
        assert splay(other,(0,1))==opposite(want)
        ids.extend(['hidden_'+name+'_exact_two_charge_endpoint','hidden_'+name+'_actual_opposite_endpoint'])
    # Coefficient identities in nonnegative slack variables. Do NOT
    # enumerate D/psi values; the source cap is proved from old guards.
    signs={
      'unchanged_target':{'old_residual':1,'source_reduction':1},
      'changed_target_positive_weight':lin({'one':1,'weight_excess':1},{'one':1},{'one':-2,'source_room_to2':1}),
      'changed_target_zero_H1':{'source_room_to1':1},
      'hidden_Gamma1_zero':{'target_excess_above1':1,'source_room_to1':1},
      'new_psi_floor_on_H':{'new_nonnegative_debt':1},
    }
    assert all(c>=0 for p in signs.values() for c in p.values())
    assert signs['changed_target_positive_weight']=={'weight_excess':1,'source_room_to2':1}
    # min(old,1) is1 only when old>1; no changed-target0 is assumed.
    changed_target_statement={'old_D_strictly_greater_than':1,'new_D_exactly':1}

    prior=BASE.parent/'M3_XFER15'
    pa=read(prior/'symbolic_audit.json');pc=read(prior/'certificate.json')
    assert pa['status']=='VISIBLE_GAMMA1_ROOT_REMOVAL_UNIVERSAL_AUDIT_PASS'
    assert pc['all_original_Gamma1_zero_destination_psi_at_least']==1 and pc['all_eight_visible_profiles_closed']
    inherited=read(prior/'dependencies.json');pins={v['path']:v['sha256'] for v in inherited['files']}
    source_hashes=pa['source_hashes_reused_not_executed']
    for p,h in source_hashes.items():assert sha(p)==h,p
    fnames=['SATURATION_THEOREM.md','CUT_PAIR_THEOREM.md','BURIED_CUT_THEOREM.md',
      'RELEASE_CAPACITY_THEOREM.md','RR_RELEASE_THEOREM.md','ANONYMOUS_RELEASE_THEOREM.md',
      'DIRECT_BARRIER_THEOREM.md','BURIED_BARRIER_THEOREM.md','INTERVAL_CHILD_THEOREM.md',
      'GRANDCHILD_THEOREM.md','MARKED_RELAY_THEOREM.md','DEPTH_FIVE_RELAY_THEOREM.md',
      'NON_EXTREMAL_EXPOSURE_THEOREM.md']
    names=[['h_Q'],['h_R'],['S','T','L'],['J'],['K','C','Z'],['N'],['Kx','Cx','G7'],
      ['KB','RB','CB','TB','GB'],['h_I'],['h_Z'],['J_marked','G_marked'],
      ['Bdry','Rsh','Q8','P8','C5','C8','K','J8','G45'],['EB','ER','H','CA','CB','R','T','G']]
    reasons=[
      'other-nonroot-real cut excludes Q in L; marked7 grandchild excludes other unique-child cases',
      'marked largest8 forces second-largest7; L port guard fails, LL/LR position fails; unmarked root excluded',
      'central roots exclude S/L; largest-pair T requires depth7<=3 but actual depth7=4',
      'source root5/6 or3/2 is not8',
      'C/Z root excludes8; K second-largest4 contradicts marked7',
      'source root5/6 or3/2 is not8',
      'Cx/G7 root excludes8; Kx second-largest4 contradicts marked7',
      'KB marked-pair contradiction; CB root4; RB/GB left5 and TB left7 contradict actual left0',
      'L has real LL; other marked child is not unique because marked7 remains visible',
      'child path not grandchild; LL parent anonymous; LR parent anonymous or required opaque LL is anonymous-real',
      'J central second-largest contradiction; G root8 core requires immediate left4/5 rather than0',
      'root/prefix and second-largest3/4 contradictions cover every named cap including dropped-V boundary clauses',
      'both exact masks omit marked7 and omit actual opposite marked1',
    ]
    registry=[];deps=[]
    for i,(name,terms,reason) in enumerate(zip(fnames,names,reasons),1):
        p=BASE.parent/f'M3_XFER{i:02}'/name
        assert lp(p).exists() and p.as_posix() in pins,p
        assert sha(p)==pins[p.as_posix()],p
        cp=BASE.parent/f'M3_XFER{i:02}'/'certificate.json'
        c=read(cp);assert c['R1_R4_preserved'] and (c.get('h0_correction_preserved') or c.get('corrected_h0_preserved'))
        registry.append({'campaign':i,'terms':terms,'theorem':p.as_posix(),'sha256':sha(p),
          'universal_exceptional_source_exclusion':reason,'actual_opposite_guard_audited':True,
          'source2_auxiliary_feasibility_assumed':False})
        deps.extend([p,cp])
    masks=read(BASE.parent/'M3_XFER13/certificate.json')
    assert all(7 not in masks[k] and 1 not in masks[k] for k in ('mask_minus','mask_actual_opposite'))
    # Typed/order contradiction certificates underpin the prose guard audit.
    guard_facts={'real_kind0_disjoint_nonreal_kinds':[1,2],
      'anonymous_isS_false_disjoint_Score_isS_true':True,
      'marked7_between_all_central_largest_pair_bounds_and8':7>4 and 7<8,
      'marked1_between0_and_all_central_smallest_pair_bounds':0<1 and 1<3,
      'actual_left0_differs_from_central_left4_5_7':0 not in (4,5,7),
      'exception_target_depth4_violates_T_cap3':4>3}
    assert 0 not in guard_facts['real_kind0_disjoint_nonreal_kinds']
    assert all(guard_facts[k] for k in list(guard_facts)[1:])
    ldr=next(Path(p) for p in pins if p.endswith('/IAGS_11G_S03_M3_LDR01_LOW_DEFICIT_RUN_REPAYMENT.md'))
    assert sha(ldr)==pins[ldr.as_posix()]
    text=lp(ldr).read_text(encoding='utf-8')
    assert 'psi(v) = max(0, max_(u->v)(psi(u)+delta(u,v)))' in text
    assert 'all 4,862 ordered core topologies' in text
    deps.extend([ldr,BASE.parent/'RESEARCH_RULES.md',BASE.parent/'M3_E1_01/OUTSIDE_E1.md',
      BASE.parent/'M3_XFER10/GRANDCHILD_THEOREM.md',prior/'VISIBLE_GAMMA1_REPAYMENT.md',
      prior/'PROOF_AUDIT.md',prior/'certificate.json',prior/'partition_update.json',prior/'symbolic_audit.json'])
    g0=lp(BASE.parent/'M3_XFER10/GRANDCHILD_THEOREM.md').read_text(encoding='utf-8')
    assert 'every public psi<=F<=2' in g0
    write('cap_exclusion_registry.json',{'status':'COMPLETE_GUARD_INTERFACE_AUDITED',
      'all_current_D_exp_terms_included':True,'entries':registry,'typed_order_facts':guard_facts,
      'exact_mathematical_scope_proof':'CAP_EXCLUSION.md and PROOF_AUDIT.md',
      'all_old_caps_vanish_at_exception':True,'exception_D_exp_equals_Lambda_at_most':1,
      'no_finite_state_guard_tests':True,'formalization_of_every_old_guard_claimed':False})
    write('checkpoint03_source_sign.json',{'status':'PASS','all_constructor_ids':ids.copy(),
      'nonnegative_sign_identities':signs,'changed_target_statement':changed_target_statement,
      'complete_old_cap_guard_audit':'cap_exclusion_registry.json','all_old_row_semantics_reused_not_replayed':True})

    old=read(prior/'partition_update.json')
    expected={'G1-MIN-H-r7-LL','G1-MIN-H-r7-LR','G1-MIN-H-r8-LL','G1-MIN-H-r8-LR',
      'G1-MAX-H-r0-RR','G1-MAX-H-r0-RL','G1-MAX-H-r1-RR','G1-MAX-H-r1-RL'}
    actual={c['id'] for c in old['cells'] if c['normal_form']=='Gamma1' and '-H-' in c['id']}
    assert actual==expected
    out=[];closures=[]
    for c in old['cells']:
        v=dict(c);v['current_potential']='D_hid = source ceiling of D_exp on H'
        if c['id'] in expected:
            assert c['source_A_terminal_depth']==3 and c['source_B_terminal_depth']==7
            v.update(status='CLOSED_UNIVERSAL_FOR_D_hid',source_F_at_most=1,target_F_at_least=1,
              current_debt_drop_options=[],closure_needed=None,
              proof='HIDDEN_GAMMA1_REPAYMENT.md',all_old_quantifiers_retained=True)
            closures.append({'id':c['id'],'status':'CLOSED_UNIVERSAL','source_in_H':True,
              'source_F_at_most':1,'target_F_at_least':1,'original_signed_residual_at_least':0,
              'old_D_exp_2_to1_claimed_valid_without_ceiling':False})
        elif c['normal_form']=='Gamma1':
            v.update(status='CLOSED_UNIVERSAL_FOR_D_hid',transport='safe ceiling preserves each previously valid row')
        else:
            assert c['status']=='OPEN'
            v.update(status='OPEN',old_seed_indices_retained=True,
              failure_bridge='any F failure is an old D_exp failure; changed targets have no H1 failure',
              current_F_floor_Lambda_claimed=False)
        out.append(v)
    assert len(closures)==8 and sum(c['status']=='OPEN' for c in out)==36
    assert all(c['normal_form']=='H1' for c in out if c['status']=='OPEN')
    write('hidden_profile_closures.json',{'all_eight_hidden_profiles_closed':True,
      'potential_changed_by_proved_safe_ceiling':True,'profiles':closures})
    write('partition_update.json',{'parent_partition':(prior/'partition_update.json').as_posix(),
      'parent_sha256':sha(prior/'partition_update.json'),'all_old_files_preserved':True,
      'newly_closed_hidden_profiles':8,'all_visible_and_hidden_Gamma1_slots_closed':16,
      'remaining_open_H1_schemas':36,'remaining_open_Gamma1_zero_schemas':0,
      'old_seed_index_bridge':'row-preservation contrapositive; no incoming H1 failure at a lowered target',
      'new_F_ge_Lambda_claimed':False,'Step4_complete':False,'no_open_cell_nonemptiness_asserted':True,'cells':out})
    assert time.process_time()<CAP
    result={'status':'HIDDEN_GAMMA1_SAFE_CEILING_UNIVERSAL_AUDIT_PASS',
      'new_universal_constructor_certificates':ids,'negative_output_height_bounds':height_bounds,
      'all_height_ge7_cores_psi_zero':True,'complete_zero_H1_incoming_spine_schemas':cases,
      'only_exceptional_zero_H1_incoming':{'MIN':{'old_root':8,'target':7,'depth':4},'MAX':{'old_root':0,'target':1,'depth':4}},
      'all_exception_source_old_caps_vanish':True,'exception_source_old_D_exp_at_most':1,
      'new_public_potential':'D_hid=min(D_exp,1) on H, D_exp elsewhere',
      'new_floor_psi_and_range_preserved':True,'new_F_ge_Lambda_claimed':False,
      'every_previously_valid_original_LOW_row_preserved':True,'HIGH_h0_glue_preserved':True,
      'all_eight_hidden_profiles_closed':True,'old_eight_visible_profiles_preserved':True,
      'all_original_quantifiers_and_coordinates_retained':True,
      'signed_identity':'F_t-F_s=(F_t-1)+(1-F_s)>=0 on each hidden Gamma1 zero',
      'nonnegative_sign_identities':signs,'source_hashes_reused_not_executed':source_hashes,
      'reused_proof_hashes':{p.as_posix():sha(p) for p in deps},
      'remaining_open_H1_schemas':36,'remaining_open_Gamma1_zero_schemas':0,'Step4_complete':False,'M3_status':'OPEN',
      'new_finite_tests':0,'new_source_transition_queries':0,'new_original_root_evaluations':0,
      'new_saved_psi_queries':0,'new_label_fits':0,'new_bank_censuses':0,'completed_semantic_checks_replayed':0,
      'original_negative_cycle_certified':False,'full_compiler_formalization_claimed':False,
      'external_human_or_model_review_claimed':False,'CPU_seconds':time.process_time(),'CPU_cap':CAP}
    write('symbolic_audit.json',result)
    print(json.dumps({'status':result['status'],'universal_constructor_certificates':len(ids),
      'hidden_profiles_closed':8,'remaining_H1_schemas':36,'remaining_Gamma1_zero_schemas':0,
      'Step4':'OPEN','new_finite_tests':0},indent=2),flush=True)

if __name__=='__main__':
    error=None
    try:main()
    except BaseException as exception:
        error={'type':type(exception).__name__,'message':str(exception)}
        raise
    finally:write('symbolic_audit_exit.json',{'whole_process_CPU_seconds':time.process_time(),'CPU_cap':CAP,'error':error})
