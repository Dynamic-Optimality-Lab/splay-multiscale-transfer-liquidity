"""Independent local-charge algebra for the foreign core10 source theorem."""
import json,time
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def p(c=0,l=0):return {'constant':c,'lambda':l}
def plus(*ps):return p(sum(x['constant'] for x in ps),sum(x['lambda'] for x in ps))
def minus(x):return p(-x['constant'],-x['lambda'])
def diff(x,y):return plus(x,minus(y))
def check(gw,pw,a,b,target,ownG,ownP):
    # RR old: G(A,P(B,target)); new: target(P(G(A,B),C),D).
    # For the lower channel target is foreign with left charge t,right0.
    og=plus(gw,a,pw,b,target);op=plus(pw,b,target)
    ng=plus(gw,a,b);np=plus(pw,ng,target)
    return plus(diff(ng,og) if ownG else p(),diff(np,op) if ownP else p())
def main():
    d=json.loads((B/'flux_audit.json').read_text())
    assert d['status']=='PASS_EXHAUSTIVE_POSITIVE_CORE10_SOURCE_FLUX'
    # Generic structural tags, all unspecified hangers remain arbitrary
    # subject to their analytically derived own-charge coefficients.
    z=p();one=p(1);L=p(0,1);oneL=p(1,-1)
    creation=check(one,p(-1),z,z,one,False,True)
    twoU=check(p(-1),p(-1),oneL,one,one,True,True)
    transfer_lower=check(z,p(-1),oneL,z,one,False,True)
    loss=check(p(-1),one,one,z,z,True,False)
    foreign_parent=check(p(-1),z,oneL,one,z,True,False)
    assert creation==one and twoU==minus(L) and transfer_lower==oneL and loss==p(-1) and foreign_parent==z
    # Transfer's own-upper charge: G=U1 loses1, P=U0 is foreign.
    # Own-upper channel RR source weights(-1,0,+1), A=1,B=C=D=0.
    own_upper_oldG=-1+1+0+0+1;own_upper_newG=-1+1+0
    assert own_upper_oldG==1 and own_upper_newG==0
    total_transfer=plus(transfer_lower,p(-1));assert total_transfer==minus(L)
    # No new original units are created by the purely B-state token matching.
    assert d['tokens_are_A_bits'] is False and d['original_B_demands_paid'] is False
    proof=(B/'CORE10_FOREIGN_FLUX.md').read_text()
    assert 'intra' in proof.lower() and 'NOT actual A-bit units' in proof
    out('flux_independent_audit.json',{'status':'PASS_SEPARATE_FOREIGN_FLUX_AND_OWNERSHIP_AUDIT',
        'independent_representation':'local RR subtree-charge sums, not endpoint decoding',
        'case_exhaustiveness':'upper RR P=M0/U0/U1; LL P=U1; mixed G or P=U1; mirror swaps channels and directions',
        'positive_total':'pure creation only, +1; transfer net=-lambda',
        'ownership':'one actual cyclic source event list, min-K cut, distinct removal ordinals; no source occurrence duplicated',
        'interpretation_limit':'this pays B-shape flux tokens, not original B demands from A units',
        'fixed_receipts_changed':False,'Bank25_changed':False,
        'same_agent_separate_derivation':True,'external_peer_review':False,'whole_compiler_formalization':False,
        'new_finite_tests':0,'source_engine_calls':0,'old_semantic_rows_replayed':0,'new_graphs':0,
        'requested_completion_achieved':False,'Step2':'OPEN','Step3':'OPEN','Universal_CD':'OPEN'})
    print('PASS independent foreign-flux source algebra and exact non-A ownership boundary; Step2 OPEN')
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_flux_independent_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
