"""Audit universal rotation schemas with arbitrary subtree variables; no samples."""
import json,sys,time
from pathlib import Path
BASE=Path(__file__).resolve().parent;CAP=min(120,float(sys.argv[1]))
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def V(x):return ('var',x)
def N(label,left,right):return ('node',label,left,right)
def K(label,left,right):return ('smart',label,left,right)
def C(tree):return ('project',tree)
def normalize(tree):
    op=tree[0]
    if op=='var':return tree
    if op in ('node','smart'):return (op,tree[1],normalize(tree[2]),normalize(tree[3]))
    assert op=='project';child=tree[1]
    if child[0]=='var':return tree
    if child[0]=='project':return normalize(child) # independently proved C-idempotence
    assert child[0] in ('node','smart')
    return K(child[1],normalize(C(child[2])),normalize(C(child[3])))
def retain_on_active_path(tree,kept):
    # A smart constructor can be treated as real ONLY under its named
    # pre-rotation Score-support premise. Post-rotation nodes stay smart.
    if tree[0]=='smart' and tree[1] in kept:
        return N(tree[1],retain_on_active_path(tree[2],kept),retain_on_active_path(tree[3],kept))
    if tree[0] in ('node','smart'):
        return (tree[0],tree[1],retain_on_active_path(tree[2],kept),retain_on_active_path(tree[3],kept))
    return tree
def rotate_right(t):
    assert t[0]=='node' and t[2][0]=='node';p,x=t[1],t[2][1];A,B,D=t[2][2],t[2][3],t[3]
    return N(x,A,N(p,B,D))
def rotate_left(t):
    assert t[0]=='node' and t[3][0]=='node';p,x=t[1],t[3][1];A,B,D=t[2],t[3][2],t[3][3]
    return N(x,N(p,A,B),D)
def main():
    start=time.process_time();A,B,D=map(V,('A','B','C'));schemas=[]
    for name,term,rotate in [('RIGHT',N('p',N('x',A,B),D),rotate_right),('LEFT',N('p',A,N('x',B,D)),rotate_left)]:
        lhs=normalize(C(rotate(term)));before=normalize(C(term));kept=retain_on_active_path(before,{'p','x'});rhs=normalize(C(rotate(kept)))
        assert lhs==rhs
        # Verify that the post-rotation parent remains a conditional smart
        # node: no false premise that it still has Score support is used.
        assert lhs[0]=='smart' and lhs[1]=='x'
        parent=lhs[3] if name=='RIGHT' else lhs[2];assert parent[0]=='smart' and parent[1]=='p'
        schemas.append({'orientation':name,'quantified_subtrees':['A','B','C'],'quantified_node_identities':['p','x'],'preconditions':['p and x Score-bearing before rotation'],'normal_form':lhs,'post_rotation_parent_may_be_erased':True})
    report={'status':'UNIVERSAL_ERASURE_ROTATION_SCHEMAS_SYMBOLICALLY_VERIFIED','method':'equational normalization on arbitrary subtree variables, not population/tree instantiation','schemas':schemas,'primitive_lemma_scope':'private proper-prefix term algebra under Score-support premises','support_preservation_and_idempotence':'structural induction in ERASURE_LEMMA.md','context_and_splay_lift':'path/context induction in ERASURE_LEMMA.md','full_source_formalization_claimed':False,'new_finite_population_tests':0,'new_source_transition_queries':0,'new_original_root_evaluations':0,'certificate_labels_read':False,'shared_state_descent_established':False,'Score_empty_helper_simulation_established':False,'M3_status':'OPEN','CPU_seconds':time.process_time()-start,'CPU_cap':CAP}
    assert report['CPU_seconds']<CAP;write(BASE/'symbolic_audit.json',report);print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error={'type':type(e).__name__,'message':str(e)};raise
    finally:write(BASE/'symbolic_audit_exit.json',{'whole_process_CPU_seconds':time.process_time(),'CPU_cap':CAP,'error':error})
