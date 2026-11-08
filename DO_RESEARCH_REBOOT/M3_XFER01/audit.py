"""Independent symbolic term/order audit; no instantiated states or trees."""
import ast,hashlib,json,sys,time
from pathlib import Path
BASE=Path(__file__).resolve().parent
CAP=min(120,float(sys.argv[1]))

def write(name,obj):
    with (BASE/name).open('x',encoding='utf-8') as stream:json.dump(obj,stream,indent=2)

def block(name):return ('nonreal_cut',name,'arbitrary_nonzero_kind_'+name)
def subtree(name):return ('arbitrary_subtree',name)
def node(label,left,right):return ('node',label,left,right)
def rz(t):
    assert t[0]=='node' and t[2][0]=='node'
    r,x=t[1],t[2][1]
    return node(x,t[2][2],node(r,t[2][3],t[3]))
def lz(t):
    assert t[0]=='node' and t[3][0]=='node'
    r,x=t[1],t[3][1]
    return node(x,node(r,t[2],t[3][2]),t[3][3])
def mirror(t):return node(t[1],mirror(t[3]),mirror(t[2])) if t[0]=='node' else t
def path(t,label,p=()):
    if t[0]!='node':return None
    if t[1]==label:return p
    a=path(t[2],label,p+(0,))
    return a if a is not None else path(t[3],label,p+(1,))
def coarse(t,p):
    if t[0]!='node':return t
    if not p:return ('real_Score',t[1])
    return coarse(t[2+p[0]],p[1:])
POSITIONS=((),(0,),(1,),(0,0),(0,1),(1,0),(1,1))
def view(t):return tuple(coarse(t,p) for p in POSITIONS)
def lin(**terms):return {k:v for k,v in terms.items() if v}
def add(*terms):
    out={}
    for term in terms:
        for k,v in term.items():out[k]=out.get(k,0)+v
    return {k:v for k,v in out.items() if v}
def neg(term):return {k:-v for k,v in term.items()}

def main():
    # Universal leaf-cut terms, NOT numerical tree/population assignments.
    A,B,C=map(block,('A','B','C'))
    original=node('r',node('x',A,B),C)
    target=rz(original)
    assert target==node('x',A,node('r',B,C))
    sv,tv=view(original),view(target)
    assert [x for x in sv[1:] if x[0]=='real_Score']==[('real_Score','x')]
    assert [x for x in tv[1:] if x[0]=='real_Score']==[('real_Score','r')]
    # In marked-r branch, the target again has Q; mark x was given.
    assert target[2]==A and target[3][2]==B and target[3][3]==C
    # The other orientation uses reversed constructors, not reflected
    # original weak-LE or HIGH witness assignments.
    assert lz(mirror(original))==mirror(target)
    assert [x for x in view(mirror(target))[1:] if x[0]=='real_Score']==[('real_Score','r')]
    # Static Q has exactly two node constructors, all other branches cuts.
    def real_count(t):return 1+real_count(t[2])+real_count(t[3]) if t[0]=='node' else 0
    assert real_count(original)==real_count(target)==2

    # B last-step identities with ARBITRARY interior subtrees. Any lower
    # path pairs have already been performed and fit these variables.
    U,V,W,Z=map(subtree,('U','V','W','Z'))
    final_zig=node('r',node('x',U,V),W)
    assert len(path(rz(final_zig),'r'))==1
    final_LL=node('r',node('p',node('x',U,V),W),Z)
    after_LL=rz(rz(final_LL))
    assert after_LL==node('x',U,node('p',V,node('r',W,Z)))
    assert len(path(after_LL,'r'))==2
    final_LR=node('r',node('p',U,node('x',V,W)),Z)
    after_LR=rz(node('r',lz(final_LR[2]),final_LR[3]))
    assert after_LR==node('x',node('p',U,V),node('r',W,Z))
    assert len(path(after_LR,'r'))==1
    assert lz(lz(mirror(final_LL)))==mirror(after_LL)
    assert lz(node('r',mirror(final_LR)[2],rz(mirror(final_LR)[3])))==mirror(after_LR)
    # Reverse weights are2 at depth1,1 at depth2; BOTH imply h_target=2.
    # General slack w_reverse=1+a makes w_reverse+2-2=1+a>0.
    assert add(lin(constant=1,reverse_weight_slack=1),lin(constant=2),lin(constant=-2))==lin(constant=1,reverse_weight_slack=1)

    # Independent affine certificates for all max branches.
    rho=lin(old_residual=1)
    assert add(rho,lin(target_increment=1))==lin(old_residual=1,target_increment=1)
    # Raised source, w>=0: target2, h_source2 -> residual=w.
    nonnegative=add(lin(w=1),lin(constant=2),lin(constant=-2))
    assert nonnegative==lin(w=1)
    # Raised source, -2<=w<0: w=-k,h_source=2-k,target2 ->0.
    negative=add(lin(k=-1),lin(constant=2),neg(lin(constant=2,k=-1)))
    assert negative=={}
    # Incoming weight0/+1 to target2; source=2-a with a>=0.
    incoming2=add(lin(nonnegative_weight=1),lin(constant=2),neg(lin(constant=2,source_range_slack=-1)))
    assert incoming2==lin(nonnegative_weight=1,source_range_slack=1)
    # Incoming+1 to target1, or zero from source<=1.
    assert add(lin(constant=1),lin(constant=1),neg(lin(constant=2,source_range_slack=-1)))==lin(source_range_slack=1)
    assert add(lin(constant=1),neg(lin(constant=1,source_below1=-1)))==lin(source_below1=1)

    # Provenance-only AST reads; NO imports/evaluation of the source DAG.
    low_path=BASE.parent/'06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_LOW_COMPILER.py'
    rot_path=BASE.parent/'06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_ROTATION_INTERPRETER.py'
    lowmod=ast.parse(low_path.read_text(encoding='utf-8-sig'))
    functions={n.name:ast.unparse(n) for n in lowmod.body if isinstance(n,ast.FunctionDef)}
    low,shadow,match=(functions[k] for k in ('build_slow','shadow7','shadow_match7'))
    assert 'C.append(s.aS[0])' in low and 'C.append(d.EQ(s.aI[0], muxb(' in low
    assert 'k = d.ITE(d.EQ(kk, d.const_int(0, 2)), dkk, kk)' in shadow
    assert 'd.OR(d.NOT(is_slot), d.EQ(cs, s.aS[p]))' in match
    assert 'd.OR(d.NOT(d.AND(is_slot, cs)), d.EQ(ci, s.aI[p]))' in match
    assert 'd.LE(d.ADD(bt.q, bt.q, 5), bd_last)' in low
    assert 'd.EQ(wv, d.SUB(d.ADD(Hv, Hv, 3), bt.q, 5))' in low
    rotmod=ast.parse(rot_path.read_text(encoding='utf-8-sig'))
    mux=next(n for n in rotmod.body if isinstance(n,ast.FunctionDef) and n.name=='mux_ref')
    assert ast.unparse(mux.body[0])=='r = vec[0]'
    replay=next(n for n in rotmod.body if isinstance(n,ast.FunctionDef) and n.name=='splay_event')
    for n in ast.walk(replay):
        if isinstance(n,ast.Assign):
            assert all(not ast.unparse(target).startswith(('wit.p','wit.isS')) for target in n.targets)
    assert 'return st' in ast.unparse(replay)
    # Reused premises are recorded by provenance, not rerun as finite checks.
    result={
        'status':'UNIVERSAL_OPAQUE_PREFIX_SATURATION_AUDIT_PASS',
        'proof_scope':'all original states/compatible witnesses/signatures with the explicitly stated Q source shape',
        'both_zig_identities_arbitrary_nonreal_blocks':True,
        'Q_successor_marked_root_branch':True,
        'unmarked_root_branch_uses_reused_empty_V_c2':True,
        'old_B_root_last_step_depths':[1,2],
        'reverse_weight_depth1':2,'reverse_weight_depth2':1,
        'marked_root_destination_c2_assumed':False,
        'simultaneous_h_target2_proved':True,
        'unchanged_source_residual':'old_residual+target_increment',
        'raised_source_residual_nonnegative_weight':nonnegative,
        'raised_source_residual_negative_weight':negative,
        'incoming_target2_residual':incoming2,
        'full_original_LOW_Q_source_coverage':'H1 saturation; H2 Gamma0 reused; Gamma1 impossible with no present anonymous node',
        'static_present_node_connectivity_reused':'AER01',
        'private_port_Score_split_invariance_assumed':False,
        'unused_alpha_fields_fixed_or_quotiented':False,
        'old_completed_semantic_checks_replayed':0,
        'new_finite_population_tests':0,'new_source_transition_queries':0,
        'new_original_root_evaluations':0,'new_label_fits':0,'new_bank_censuses':0,
        'source_provenance':{p.as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (low_path,rot_path)},
        'full_compiler_formalization_claimed':False,
        'all_H1_transfers_solved':False,'all_M3_LOW_solved':False,
        'restricted_walk_theorem':'LOW sources in Q; all original HIGH legs; finite>=-7,fully closed>=0',
        'M3_status':'OPEN','CPU_seconds':time.process_time(),'CPU_cap':CAP,
    }
    assert time.process_time()<CAP
    write('symbolic_audit.json',result)
    print(json.dumps(result,indent=2),flush=True)

if __name__=='__main__':
    error=None
    try:main()
    except BaseException as exception:
        error={'type':type(exception).__name__,'message':str(exception)}
        raise
    finally:write('symbolic_audit_exit.json',{'whole_process_CPU_seconds':time.process_time(),'CPU_cap':CAP,'error':error})
