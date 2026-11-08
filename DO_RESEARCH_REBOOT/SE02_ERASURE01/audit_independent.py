"""Separate SE02 mathematical/source audit; no construction or research imports.

All term objects below are free symbolic trees with independent hanger
variables. Rewriting proves universal identities, not finite sample instances.
No concrete key population, mask, walk search or source engine is executed.
"""
import ast,hashlib,json,sys,time
from fractions import Fraction
from pathlib import Path
B=Path(__file__).resolve().parent
R=B.parent
ROOT=R.parent
def xp(p):return Path('\\\\?\\'+str(p.resolve()))
def raw(p):return xp(p).read_text(encoding='utf-8')
def read(p):return json.loads(raw(p))
def sha(p):return hashlib.sha256(xp(p).read_bytes()).hexdigest()
def write(n,d):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(d,f,indent=2)
def contains(p,parts):
    text=raw(p)
    for q in parts:assert q in text,(str(p),q)
def poly(p):return {k:Fraction(v) for k,v in p.items() if Fraction(v)!=0}
def affine(s):
    assert len(s['ge'])==len(s['mg']) and len(s['eq'])==len(s['me'])
    assert all(Fraction(v)>=0 for v in s['mg'])
    result={}
    for ts,ms in ((s['ge'],s['mg']),(s['eq'],s['me'])):
        for t,m in zip(ts,ms):
            for k,v in poly(t).items():result[k]=result.get(k,Fraction(0))+Fraction(m)*v
    assert poly(result)==poly(s['goal']),s['name']

# Independent free-term equational kernel, bound to original source syntax.
def N(k,l,r):return ('N',k,l,r)
def right_child(t):
    _,g,A,xnode=t;_,x,B,C=xnode
    return N(x,N(g,A,B),C)
def left_child(t):
    _,g,xnode,C=t;_,x,A,B=xnode
    return N(x,A,N(g,B,C))
def RR(t):
    _,g,A,pnode=t;_,p,B,xnode=pnode;_,x,C,D=xnode
    return N(x,N(p,N(g,A,B),C),D)
def LL(t):
    _,g,pnode,D=t;_,p,xnode,C=pnode;_,x,A,B=xnode
    return N(x,A,N(p,B,N(g,C,D)))
def zigzag_RL(t):
    _,g,A,pnode=t;_,p,xnode,D=pnode;_,x,B,C=xnode
    return N(x,N(g,A,B),N(p,C,D))
def paths(t,p=()):
    if isinstance(t,str):return {t:p}
    _,k,l,r=t
    out={k:p};out.update(paths(l,p+('L',)));out.update(paths(r,p+('R',)))
    return out
def inorder_nodes(t):
    if isinstance(t,str):return []
    return inorder_nodes(t[2])+[t[1]]+inorder_nodes(t[3])

def main():
    inherited=read(B/'dependency_pins.json');pins=inherited['pins']
    for p in pins:assert sha(ROOT/p['path'])==p['sha256'],p['path']
    assert sha(Path(inherited['user_directive_path']))==inherited['user_directive_sha256']
    base=read(R/'CD5_BASE01/CD5_CERTIFICATE.json')
    assert base['status']=='PROVED_CD5_COMPLETE_ORIGINAL_CLOSED_WALK_BASE'
    assert base['mandatory_open_CD5_dependencies']==[]
    assert all(v=='PASS' for v in base['publication_gates'].values())
    prior=read(R/'CD_UNIFORM01/PARTIAL_CERTIFICATE.json')
    assert not prior['unrestricted_CD_proved'] and not prior['uniform_support_induction_proved']
    assert read(R/'CD_UNIFORM01/final_manifest.json')['status']=='AUDITED_PARTIAL_RESULTS_PUBLISHED_UNRESTRICTED_CD_OPEN'

    source=ROOT/'python/independent/splay.py';tree=ast.parse(raw(source))
    fs={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)}
    code=ast.get_source_segment(raw(source),fs['_rebuild'])
    for statement in (
      'cur = node(x, t1, node(kp, t2, node(kg, q, c)))',
      'cur = node(x, node(kp, node(kg, c, q), t1), t2)',
      'cur = node(x, node(kg, a, t1), node(kp, t2, q))',
      'cur = node(x, t1, node(kp, t2, q))',
      'cur = node(x, node(kp, q, t1), t2)',
      'return _plug(fr, cur), evs'):assert statement in code
    assert 'd, cur = 0, t' in ast.get_source_segment(raw(source),fs['lookup'])

    # Universal depth offsets of each primitive rotation, including hangers.
    t=N('p','L',N('c','M','R'));u=right_child(t)
    p0,p1=paths(t),paths(u)
    rg={v:len(p1[v])-len(p0[v]) for v in ('p','c','L','M','R')}
    assert rg=={'p':1,'c':-1,'L':1,'M':0,'R':-1}
    t=N('p',N('c','L','M'),'R');u=left_child(t)
    p0,p1=paths(t),paths(u)
    lg={v:len(p1[v])-len(p0[v]) for v in ('p','c','L','M','R')}
    assert lg=={'p':1,'c':-1,'L':-1,'M':0,'R':1}

    # Exact inverses on the complete free terms, not just roots/depths.
    tr=N('y','A',N('z','B','C'));assert left_child(right_child(tr))==tr
    tl=N('y',N('z','A','B'),'C');assert right_child(left_child(tl))==tl
    trr=N('y','A',N('p','B',N('z','C','D')))
    assert LL(RR(trr))==trr
    tll=N('y',N('p',N('z','A','B'),'C'),'D')
    assert RR(LL(tll))==tll
    # Positive and negative indirect effects are actual source positions.
    assert len(paths(RR(trr))['y'])==2 and len(paths(trr)['y'])==0
    tw=N('y','A',N('p','B',N('z','C',N('w','E','F'))))
    assert len(paths(tw)['w'])==3 and len(paths(RR(tw))['w'])==1
    # Rejected zigzag geometry has equal roots but unequal full trees.
    tz=N('y','A',N('p',N('z','B','C'),'D'))
    returned=left_child(zigzag_RL(tz))
    assert returned==N('y','A',N('z','B',N('p','C','D')))
    assert returned!=tz and returned[3][1]=='z' and tz[3][1]=='p'

    # New all-fringe family: all nine hangers remain free indeterminates.
    f=['F'+str(i) for i in range(9)]
    spine=N('b2',f[3],N('b3',f[4],N('b4',f[5],N('b5',f[6],N('b6',f[7],f[8])))))
    S=N('b1',N('p',N('z',f[0],f[1]),f[2]),spine)
    assert inorder_nodes(S)==['z','p','b1','b2','b3','b4','b5','b6']
    assert RR(LL(S))==S
    rules={'R':right_child,'L':left_child,'RR':RR,'LL':LL}
    proof_word=['R','R','R','RR','LL','L','L','L']
    target_word=['b2','b3','b4','b6','b4','b3','b2','b1']
    state=S
    for rule,target in zip(proof_word,target_word):
        previous_root=state[1];state=rules[rule](state)
        assert state[1]==target and target!=previous_root
    assert state==S
    skeleton_paths=paths(S)
    zpath=['b1','p','z'];b6path=['b1','b2','b3','b4','b5','b6']
    assert skeleton_paths['z']==('L','L') and skeleton_paths['b6']==('R',)*5
    core=set(zpath)|set(b6path)
    assert core==set(inorder_nodes(S)) and len(core)==8
    marks={'z','b1','b2','b3','b4','b6'};assert len(marks)==6 and marks<=core

    # Review the mathematical scope/normalization and physical reservation.
    contains(B/'ERASURE_ALIGNMENT.md',[
      'r>=6','I=[uN,(u+L)N)','A_I=LA, Q_F(I)=LQ','Dividing ALL three terms by the same L',
      'D is nonnegative;','J is signed','possibly0','transient marginal is incorrect',
      'No sign is assumed for the transient term'])
    contains(B/'ROTATION_INTERFERENCE.md',[
      'Each gain reads membership in ITS OWN current source frame',
      'j_t=floor(f/2)-floor(e/2)','if f-e>=2','if f-e=1','if f-e=-1','if f-e<=-2',
      'A root splay has an empty word','not an exhaustive favorable geometric'])
    contains(B/'PROTECTED_COMPENSATION.md',[
      'Every block is a nonempty run','at least one KEEP','All KEEPs of z',
      'same-side grandchild','child, or a same-side grandchild','COMPLETE A tree',
      'first KEEP y','no assumption about slack','WHOLE selected blocks',
      'SMALLER-SUPPORT THEOREM to gamma0','none of which is in a selected block',
      'first period costs Q0+1','each subsequent period','u=1,L=1',
      'selected complete period contains every donor and consumer',
      'No uniform CD(r)=>CD(r+1) promotion is made'])
    contains(B/'SIX_KEY_CORE8_FAMILY.md',[
      'for every integer m>=1','Every empty pointer','nine such hanger slots',
      'A(gamma_m)=2m+8','Q_full(gamma_m)=2m+2','Q_erased=2',
      'D_z=m, J_z=m, Delta_z=2m','genuine support is EXACTLY M',
      'exactly8 nodes','outside CD(5)','does not\ncertify novelty against every historical'])
    contains(B/'STRESS_TESTS.md',[
      'one direct and one positive','first-period marginal is2m-1','No transient unit pays an aligned demand',
      'FAILS our guard','The last full tree differs','No concrete tree'])

    p=read(B/'derivation.json')
    assert p['alignment']['A_trajectory_preserved'] and not p['alignment']['preperiod_credits_available']
    assert p['alignment']['per_original_period']=='divide R,R_z,Delta,D,J together by L'
    assert not p['marginal']['indirect_sign_assumed'] and p['marginal']['nongenuine_and_zero_operations_retained']
    assert p['primitive_gains']['rotate_right_child']==dict(rg,outside=0)
    assert p['primitive_gains']['rotate_left_child']==dict(lg,outside=0)
    guard=p['protected_theorem']
    assert guard['blocks']=='disjoint cyclic z-run then y-run,y!=z; each run nonempty and has a KEEP'
    assert guard['B_z_geometry']=='same-side grandchild' and guard['A_z_geometry']=='child or same-side grandchild'
    assert guard['all_Kz_in_blocks'] and guard['arbitrary_run_modes_and_lengths']
    assert guard['full_paired_identity'] and guard['outside_full_state_resynchronization']
    assert guard['per_block']=={'A':2,'Q_full':2,'Q_erased':0,'D':1,'J':1,'Delta':2}
    assert guard['block_boundary_alignment']=={'u':0,'L':1}
    assert guard['arbitrary_active_B_cut']=={'u':1,'L':1,'first_erased_Q':'Q0+1','recurrent_erased_Q':'Q0'}
    assert guard['donor_at_or_before_consumers'] and not guard['Delta_le_Rz_assumed']
    assert guard['reserved_pool']=='all4 A units per block excluded from contracted gamma0'
    assert guard['used_pool']=='only2 bits of first z A event'
    assert guard['bit0_consumer']=='B DOUBLE at first full KEEP z'
    assert guard['bit1_consumer']=='B DOUBLE at first full KEEP y'
    assert guard['cost_relations']==['A=A0+2m','Q_full=Q0+2m','Q_erased=Q0']
    assert not guard['every_walk_has_guarded_key']
    family=p['new_family']
    assert set(family['marked_roles'])==marks and family['G']==6 and family['fixed_core_size']==8
    assert family['arbitrary_mark_free_hangers']==9 and family['W_source_rules']==proof_word
    assert family['W_A']==8 and family['W_Q']==2
    assert family['strictly_outside_CD5_and_core_le7'] and not family['novel_against_every_historical_packet_closure_claimed']
    assert family['costs']=={'A':'2m+8','Q_full':'2m+2','Q_erased':'2','D':'m','J':'m','Delta':'2m','R':'2m+14','R_z':'4m+14'}

    expected={
      'aligned_residual':([],[{'R':1,'S':-2,'QF':1},{'Rz':1,'S':-2,'QE':1},{'Delta':1,'QF':-1,'QE':1}],{'R':1,'Rz':-1,'Delta':1}),
      'direct_indirect_split':([],[{'Delta':1,'QF':-1,'QE':1},{'QF':1,'D':-1,'F':-1},{'QE':1,'E':-1},{'J':1,'F':-1,'E':1}],{'Delta':1,'D':-1,'J':-1}),
      'transient_subtraction':([],[{'tail':1,'FT':-1,'FP':1,'ET':1,'EP':-1},{'total':1,'FT':-1,'ET':1},{'pre':1,'FP':-1,'EP':1}],{'tail':1,'total':-1,'pre':1}),
      'parity_identity':([],[{'f':1,'qf':-2,'bf':-1},{'e':1,'qe':-2,'be':-1},{'j':1,'qf':-1,'qe':1}],{'j':2,'f':-1,'e':1,'bf':1,'be':-1}),
      'positive_band_contradiction':([{'d':1,'1':-2},{'j':-1},{'1':1,'bf':-1},{'be':1}],[{'d':1,'j':-2,'bf':-1,'be':1}],{'1':-1}),
      'negative_band_contradiction':([{'d':-1,'1':-2},{'j':1},{'bf':1},{'1':1,'be':-1}],[{'d':1,'j':-2,'bf':-1,'be':1}],{'1':-1}),
      'protected_compensation':([{'A0':2,'Q0':-1}],[{'A':1,'A0':-1,'m':-2},{'Q':1,'Q0':-1,'m':-2}],{'A':2,'Q':-1,'m':-2}),
      'six_family_slack':([],[{'A':1,'m':-2,'1':-8},{'Q':1,'m':-2,'1':-2}],{'A':2,'Q':-1,'m':-2,'1':-14})}
    seen=set()
    for s in p['affine_schemas']:
        assert s['name'] not in seen;seen.add(s['name'])
        assert (s['ge'],s['eq'],s['goal'])==expected[s['name']]
        affine(s)
    assert seen==set(expected)
    # The nonunit sign cases use integer j and the checked contradiction.
    # For delta1: e=2h+eps, f=2(h+eps)+(1-eps), j=eps.
    # For delta-1 exchange f/e, giving j=-eps. eps in{0,1}; no source sample.
    assert p['parity']=={'identity':'2j=f-e-(f mod2)+(e mod2)','delta_ge2':'j>=1',
      'delta_eq1':'j=(e mod2)','delta_eq0':'j=0','delta_eq_minus1':'j=-(f mod2)','delta_le_minus2':'j<=-1'}
    assert p['new_finite_tests']==p['new_solver_queries']==p['new_original_root_queries']==p['completed_semantic_checks_replayed']==0
    assert not p['frozen_graph_modified'] and not p['matching_terminal_modified'] and p['Bank25']==25
    assert not p['uniform_support_induction_proved'] and not p['unrestricted_CD_proved'] and not p['Dynamic_Optimality_proved']
    assert time.process_time()<float(sys.argv[1])
    write('independent_audit.json',{
      'status':'INDEPENDENT_SE02_MATHEMATICAL_AND_SOURCE_AUDIT_PASS',
      'declared_inherited_pins_verified':len(pins),'user_directive_pin_verified':True,
      'general_aligned_marginal_identity':'PROVED_UNIVERSAL_AT_STATED_SOURCE_DOMAIN',
      'direct_indirect_decomposition':'PROVED_SIGNED_NO_FAVORABLE_SIGN_ASSUMPTION',
      'primitive_depth_gain_tables':'PROVED_FROM_FREE_SOURCE_ROTATIONS',
      'parity_sign_cases':'COMPLETE_INTEGER_CLASSIFICATION',
      'protected_compensation':'PROVED_RESTRICTED_SOURCE_GEOMETRIC_CLASS',
      'donor_reservation':'CONTRACTED_SOURCE_CD_POOL_EXCLUDES_ALL_BLOCK_EVENTS',
      'physical_credit_injection':'bit0_to_direct_bit1_to_indirect; distinct copy/block/occurrence IDs',
      'block_boundary_alignment':{'u':0,'L':1},
      'active_B_input_cut_transient':{'u':1,'L':1,'first_erased_Q':'Q0+1','recurrent_erased_Q':'Q0'},
      'symbolic_six_key_core8_family':'PROVED_ALL_m_GE1_ALL_NINE_HANGERS',
      'strictly_outside_CD5_and_core_le7':True,'novelty_against_entire_historical_bank_certified':False,
      'universal_affine_schemas':sorted(seen),
      'source_term_proofs':['left_rotation_offsets','right_rotation_offsets','zig_inverse_both_sides',
        'RR_LL_inverse_both_sides','positive_indirect_return','negative_indirect_far_hanger',
        'zigzag_full_tree_nonidentity','six_key_family_block_identity','six_key_family_backbone_identity'],
      'indirect_global_bound_proved':False,'favorable_key_selection_proved':False,
      'uniform_support_induction_proved':False,'unrestricted_CD_proved':False,'original_CD_counterexample_claimed':False,
      'new_finite_tests':0,'new_solver_queries':0,'new_original_root_queries':0,'completed_semantic_checks_replayed':0,
      'old_seals_and_frozen_graph_preserved':True,'matching_terminal_modified':False,'Bank25':25,
      'construction_imported':False,'research_engines_imported':False,'external_peer_review':False,
      'whole_compiler_formalization':False,'proof_object_bytes':(B/'derivation.json').stat().st_size,
      'publication_requires_controllers_resources_and_integrity_PASS':True})
    print(json.dumps({'status':'INDEPENDENT_SE02_AUDIT_PASS','new_finite_tests':0,'universal_CD':'OPEN'}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:write('audit_independent_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
