"""Independent universal term/parity audit; no sampled states or populations."""
import json,sys,time,ast,hashlib
from pathlib import Path
BASE=Path(__file__).resolve().parent;CAP=min(120,float(sys.argv[1]))
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def V(name):return ('var',name)
def N(label,left,right):return ('node',label,left,right)
def right(t):
    assert t[0]=='node' and t[2][0]=='node';p,x=t[1],t[2][1];return N(x,t[2][2],N(p,t[2][3],t[3]))
def left(t):
    assert t[0]=='node' and t[3][0]=='node';p,x=t[1],t[3][1];return N(x,N(p,t[2],t[3][2]),t[3][3])
def splay_LL(t):return right(right(t))
def splay_RR(t):return left(left(t))
def splay_LR(t):return right(N(t[1],left(t[2]),t[3]))
def flip(t):return t if t[0]=='var' else N(t[1],flip(t[3]),flip(t[2]))
def find(t,key):
    if t[0]!='node':return None
    if t[1]==key:return t
    return find(t[2],key) or find(t[3],key)
def path(t,key,p=()):
    if t[0]=='var':return p if t[1]==key else None
    if t[1]==key:return p
    q=path(t[2],key,p+(0,));return q if q is not None else path(t[3],key,p+(1,))
def obs7(t,owner='r'):
    # Exact symbolic interface for the authoritative depth-two reader.
    # A variable's arbitrary real/port/empty/G view depends at most on the
    # static owner label and its one-step child observations. Its maximal
    # remaining path is1 here. This includes both coarse propagation and
    # literal-slot0 fallback without enumerating their concrete values.
    def mark(label):return ('real','anonymous') if label in ('f','u') else ('real','Score',label)
    ownernode=find(t,owner);assert ownernode is not None
    def rootview(n):return ('root_view',n[1],mark(owner)) if n[0]=='var' else mark(n[1])
    ownersig=(mark(owner),rootview(ownernode[2]),rootview(ownernode[3]))
    def at(n,p):
        if n[0]=='var':return ('arbitrary_depth2_view',n[1],p,ownersig)
        if not p:return mark(n[1])
        return at(n[2+p[0]],p[1:])
    return tuple(at(t,p) for p in ((),(0,),(1,),(0,0),(0,1),(1,0),(1,1)))
def lin(**coeff):return {k:v for k,v in coeff.items() if v}
def sub(a,b):
    result=dict(a)
    for k,v in b.items():result[k]=result.get(k,0)-v
    return {k:v for k,v in result.items() if v}
def main():
    start=time.process_time();A,B,C,D,E,U=map(V,('A','B','C','D','E','U'))
    source=N('r',N('f',A,B),N('x',C,D));after=splay_RR(right(source));direct=left(source);assert after==direct
    source_lr=N('r',N('u',A,N('f',B,C)),N('x',D,E));after_lr=splay_RR(splay_LR(source_lr));direct_lr=left(source_lr)
    assert after_lr==N('x',N('r',N('f',N('u',A,B),C),D),E)
    assert direct_lr==N('x',N('r',N('u',A,N('f',B,C)),D),E)
    assert obs7(after_lr)==obs7(direct_lr)
    # Universal right/max dual: reverse constructors, not source witnesses
    # or HIGH sentinel assignments.
    assert obs7(flip(after_lr))==obs7(flip(direct_lr))
    # General minimum-path induction: a newly processed pair increases
    # the relative depth of old-min support U by exactly1; old root g is
    # depth2. A remaining zig puts old root g at depth1.
    pair=N('g',N('p',N('f',A,U),B),C);pair_after=splay_LL(pair)
    assert pair_after==N('f',A,N('p',U,N('g',B,C)))
    assert len(path(pair_after,'U'))-len(path(pair_after,'f')) == len(path(pair,'U'))-len(path(pair,'f'))+1
    assert len(path(pair_after,'g'))==2
    zig=N('g',N('f',A,U),B);zig_after=right(zig)
    assert len(path(zig_after,'U'))-len(path(zig_after,'f')) == len(path(zig,'U'))-len(path(zig,'f'))+1
    assert len(path(zig_after,'g'))==1
    # Base paths: old parent Score0 ends at depth1 for h1 and h2.
    base1=N('z',N('f',A,B),C);base2=N('g',N('z',N('f',A,B),C),D)
    assert len(path(right(base1),'z'))==len(path(splay_LL(base2),'z'))==1
    # Odd-depth B frontier is the same inverse-rotation identity above;
    # arbitrary common bottom pairs are wholly inside source m.right.
    bfront=N('r',N('f',A,B),N('x',C,D));assert splay_RR(right(bfront))==left(bfront)
    # Even depth: after common core-only pairs, x is f.right and P contains
    # minimum r. The final zig leaves P as f.right, contradicting a leaf.
    P,Q=map(V,('P_contains_minimum_r','Q'));even_after=left(N('f',A,N('x',P,Q)))
    assert even_after==N('x',N('f',A,P),Q) and find(even_after,'f')[3]==P
    # Arbitrary integer k: d=2k+1, terminal charges k+1 versus k.
    w2=lin(one=3,k=-1);w1=lin(one=2,k=-1);assert sub(w2,w1)==lin(one=1)
    # Public-fibre maximum obstruction is universal in 0<=q<p<=2,
    # not a numerical test: private edge residuals0, public residual q-p.
    public_residual=sub(lin(q=1),lin(p=1));assert public_residual==lin(q=1,p=-1)
    # Provenance-only source checks: actual theorem uses the certified
    # source semantics, not this AST check as a full compiler formalization.
    sourcepath=BASE.parent/'06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_LOW_COMPILER.py';text=sourcepath.read_text(encoding='utf-8-sig');module=ast.parse(text)
    function=next(n for n in module.body if isinstance(n,ast.FunctionDef) and n.name=='build_slow');body=ast.unparse(function)
    assert 'bd_last' in body and 'd.LE(d.ADD(bt.q, bt.q, 5), bd_last)' in body and 'd.LT(bd_last, d.ADD(d.ADD(bt.q, bt.q, 5), d.const_int(2, 5), 5))' in body
    assert 'for a1, a2 in ((t.b.kl, bs[5].kl)' in body and 'b_tree_valid(d, t.b, bst5, t.sig)' in body
    result={'status':'UNIVERSAL_ERASED_HELPER_REDUCTION_ALGEBRA_AUDIT_PASS','arbitrary_subtree_variables':['A','B','C','D','E','U','P_contains_minimum_r','Q'],'source_L_exact_pointer_identity':True,'source_LR_authoritative_shadow_identity':True,'right_max_dual_shadow_identity':True,'G_alias_owner_children_included_in_shadow_interface':True,'minimum_spine_base_and_induction_step_verified':True,'old_root_depth_parity_verified':True,'odd_B_frontier_exact_identity':True,'even_B_frontier_leaf_contradiction':True,'symbolic_weight_gap':1,'terminal_q_source_dependency_confirmed':True,'endpoint_fresh_bounds_source_dependency_confirmed':True,'source_SHA256':hashlib.sha256(sourcepath.read_bytes()).hexdigest(),'full_source_formalization_claimed':False,'helper_theorem_premises':['0<=public D<=2','all ORIGINAL H1 inequalities','reused original H2/Gamma1 source normal form'],'new_private_inventory_invariance_assumed':False,'public_debt_constructed':False,'public_fibre_max_signed_lift':'NOT_VALID_AS_A_GENERAL_INFERENCE','symbolic_public_max_residual':public_residual,'M3_status':'OPEN','new_finite_population_tests':0,'new_source_transition_queries':0,'new_original_root_evaluations':0,'CPU_seconds':time.process_time()-start,'CPU_cap':CAP}
    assert result['CPU_seconds']<CAP;write(BASE/'symbolic_audit.json',result);print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error={'type':type(e).__name__,'message':str(e)};raise
    finally:write(BASE/'symbolic_audit_exit.json',{'whole_process_CPU_seconds':time.process_time(),'CPU_cap':CAP,'error':error})
