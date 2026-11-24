"""Independent unbounded algebra/credit verifier; no learner import."""
import sys
import json
import z3
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent


def prove(name,assumptions,claim):
    s=z3.Solver();s.add(*assumptions,z3.Not(claim));assert s.check()==z3.unsat,name
    return {'obligation':name,'negation':'UNSAT','domain':'Unbounded integer variables, stated assumptions only.'}


def check(learned):
    assert learned['status']=='PROVED_UNBOUNDED_JOINT_AFFINE_INVARIANTS'
    a,b,c=learned['first'];assert a==1 and 9*a-c==0 and 7*a+b+c==0
    d,e,f,g=learned['second'];assert d==1 and e==-16 and f==16 and 4+e+g==0
    x,P,S,j=z3.Ints('leftSize power privateCount completedDoubles')
    I1=lambda x,P:a*x+b*P+c==0
    I2=lambda S,P,j:d*S+e*P+f*j+g==0
    checks=[prove('initialization',[],z3.And(I1(7,1),I2(4,1,0))),
            prove('joint_preservation',[I1(x,P),I2(S,P,j)],z3.And(I1(2*x+9,2*P),I2(S+x-7,2*P,j+1))),
            prove('physical_support',[I2(S,P,j)],16*(j+1)+1+S==16*P+5),
            prove('nonnegative_padding',[x>=7,S>=4,P>=1,j>=0],z3.And(S+x-7>=4,2*x+9>=7,2*P>=1,j+1>=0))]
    A,B,C,D=z3.Ints('outerLeft parentLeft targetLeft targetRight')
    checks.append(prove('all_hanging_subtree_RR_size_alias',[A==D,B==C],z3.And(1+C+D==1+A+B,2+B+C+D==2+A+B+C)))
    coeff,M,u,v=z3.Ints('trialConstant uniformWeightBound firstWeight secondWeight')
    q=coeff+2*M+1
    checks.append(prove('every_finite_signed_bounded_size_weight_family',[coeff>=0,M>=0,u>=-M,v>=-M],q+1+u+v>coeff))
    q2=coeff+1
    checks.append(prove('every_nonnegative_size_weight_family',[coeff>=0,u>=0,v>=0],q2+1+u+v>coeff))
    drop=z3.Int('historyCreditOrShapeDecrease')
    checks.append(prove('positive_unpaid_cost_must_use_earned_carry',[u>=-M,v>=-M,q+1+u+v-drop<=coeff],drop>=q+1-coeff-2*M))
    G,need,nxt,s,cap=z3.Ints('balance required nextRequired supply capacity')
    checks += [prove('supply_induction',[G>=need,nxt-s<=need,nxt<=cap],z3.If(G+s<=cap,G+s,cap)>=nxt),
               prove('demand_induction',[G>=nxt+s,nxt>=0],z3.And(G>=s,G-s>=nxt)),
               prove('closed_A_excursion_cannot_reduce_global_credit',[s>=0,G<=cap],z3.If(G+s<=cap,G+s,cap)>=G)]
    r=z3.Int('q_plus_one');capacity=z3.If(8*r>=12*r-4,8*r,12*r-4)
    for term in (14*r-12,15*r-28):capacity=z3.If(capacity>=term,capacity,term)
    checks.append(prove('all_q_exact_H_capacity_bounds',[r>=2],z3.And(capacity>=8*r,capacity>=12*r-4,capacity>=14*r-12,capacity>=15*r-28,capacity<=15*r)))
    checks.append(prove('restoration_recharges_without_free_ancestry_credit',[r>=2],capacity-15*r+28+4*(16*r-7)>=capacity))
    # The complete all-q source bridge is the explicit H comb recurrence plus
    # rigid-gap rotation substitution; never label these algebra rows a full
    # original BST formalization or a Universal-CD proof.
    old=HERE.parent/'H3Q_ANALYSIS_20261120_V001/SYMBOLIC_BLOCK_CERTIFICATE.json'
    blocks=json.loads(old.read_text());assert max(r['Q'] for r in blocks['generic_block']['rows'])==3
    assert max(r['Q'] for r in blocks['terminal_block']['rows'])==2
    return {'passed':True,'checks':checks,'learned_invariants_verified':True,
        'parametric_source_bridge':'Original H3q j=2/3 comb, arbitrary rigid gaps, one current A zig, neutral RR aliases and final LR common children.',
        'cardinality_grammar':'Phi_w=-sum_{I in full-X B labels minus A labels} w(|I|), arbitrary bounded signed w or arbitrary nonnegative w.',
        'excluded':'Whole-original-operation cost certificates in this grammar for every finite constant.',
        'persistent_global_banks_excluded':False,'root_scope_restricted':False,
        'new_unrestricted_root_cost_obligations_deleted':0,'universal_CD':'OPEN'}


def main():
    result=check(json.loads((HERE/'LEARNED_INDUCTION.json').read_text()))
    if not (HERE/'FINAL_MANIFEST.json').exists():
        p=HERE/'SYMBOLIC_VERIFICATION.json'
        if p.exists():assert json.loads(p.read_text())==result
        else:p.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({'passed':True,'unbounded_checks':len(result['checks']),'universal_CD':'OPEN'}))


if __name__=='__main__':main()
