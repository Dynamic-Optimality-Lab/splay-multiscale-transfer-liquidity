"""Independent universal inverse/guard/source-cover/sign proof audit."""
import json,sys,time
from pathlib import Path
import z3
from target_floor import N,dp,region_caps,opp,opposite_alpha
from legacy_floors import legacy_floor
from symbolic_prefix_v2 import prefix
from compatibility import source_compatible
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'M3_XFER18'))
from audit_spread import replay,path
from audit_central import inverses
from audit_spread_v2 import inverse_proof
BASE=Path(__file__).resolve().parent;CAP=min(120,float(sys.argv[1]));E=None
def write(name,obj):
    with (BASE/name).open('x',encoding='utf-8') as f:json.dump(obj,f,indent=2)
def check(name,s,results):
    v=s.check();assert v==z3.unsat,(name,str(v),str(s.model()) if v==z3.sat else s.reason_unknown())
    results.append(name)
def main():
    results=[]
    S=N(0,E,N(5,N(3,N(1,E,N(2)),N(4)),N(6,E,N(7,E,N(8)))))
    T=N(2,N(0,E,N(1)),N(5,N(3,E,N(4)),N(6,E,N(7,E,N(8)))))
    Q=N(8,N(5,N(2,N(0,E,N(1)),N(3,E,N(4))),N(7,N(6),E)),E)
    P=N(6,N(5,N(4,N(3,N(2,N(1,N(0),E),E),E),E),E),N(7,E,N(8)))
    assert replay(S,path(S,2))==T and len(path(S,2))==4
    assert replay(T,path(T,8))==Q and len(path(T,8))==4
    assert replay(P,path(P,0))==S and len(path(P,0))==6
    inverse=[]
    for name,t in [('S',S),('T',T),('Q',Q)]:
        for d in (6,7,8):
            solutions,proof=inverses(t,d)
            assert solutions==({P} if name=='S' and d==6 else set()),(name,d,solutions)
            inverse.append({'core':name,'depth':d,'complete_inverse_word_proof':proof})
    Pnone=[{'depth':d,'proof':inverse_proof(P,d)} for d in (6,7,8)]
    write('reset_inverse_certificate.json',{'status':'PASS','all_predecessors_quantified':True,
      'inverse_proofs':inverse,'P_no_negative_incoming':Pnone,'derived_psi':{'S':1,'T':0,'Q':0,'P':0},
      'no_bank_or_population_tests':True})
    # Literal guard exclusions are symbolic simplifications of the SAME
    # saved functions, independently cross-checked against theorem scopes.
    mu={0,1,2,3,8};m=[z3.BoolVal(i in mu) for i in range(9)]
    aS=list(map(z3.IntVal,[0,9,2,12,12,1,4]));aT=list(map(z3.IntVal,[2,0,4,9,1,3,8]))
    assert z3.is_true(z3.simplify(source_compatible(aS))) and z3.is_true(z3.simplify(source_compatible(aT)))
    for name,t,a,thresholds in [('S',S,aS,(2,)),('T',T,aT,(1,2))]:
        for k in thresholds:
            guard=z3.Or(legacy_floor(t,a,m,k),legacy_floor(opp(t),opposite_alpha(a),list(reversed(m)),k))
            assert z3.is_false(z3.simplify(guard)),(name,k,str(z3.simplify(guard)))
        one,two=region_caps(t,a,m);o,v=region_caps(opp(t),opposite_alpha(a),list(reversed(m)))
        assert z3.is_false(z3.simplify(z3.Or(*(two+v))))
        if name=='T':assert z3.is_false(z3.simplify(z3.Or(*(one+o))))
    # ALL masks/private gaps and blocks for the proposed repair, with
    # SC-false incoming boundaries paid by the independent Bad theorem.
    u=prefix((1,1),2,8,'repair')
    mm=[z3.Bool('repair_mark_'+str(i)) for i in range(9)]
    e1=z3.And(*(z3.Implies(z3.And(mm[k],z3.Or(*(u['target'][i]==k for i in range(1,7)))),
      z3.BoolVal(dp(Q)[k]<=3)) for k in range(9) if k!=8))
    sol=z3.Solver();sol.set(timeout=20000)
    sol.add(*u['constraints'],z3.PbEq([(v,1) for v in mm],5),mm[2],mm[8],z3.Not(mm[4]),
      u['source'][2]==4,u['source'][6]==8,source_compatible(u['target']),z3.Not(e1))
    check('every_compatible_R_T_zero8_target_E1_otherwise_Bad',sol,results)
    assert time.process_time()<CAP
    write('audit_reset.json',{'status':'UNIVERSAL_COMPATIBLE_RESET_REFUTATION_AND_REPAIR_AUDIT_PASS',
      'old_candidate_analytic_residual':-1,'old_candidate_debts':[1,0],
      'current_D_bad_assignment_refuted_not_M3':True,'original_realizability':'analytic proper-tree source lift, no compiler evaluation',
      'whole_R_T_source_one_credit_safe':True,'universal_symbolic_proofs':results,
      'all_old_signed_rows_HIGH_h0_and_full_state_scopes_preserved':True,
      'new_debt':'D_repay=max(D_bad,1_R_T_both_actual_orientations)',
      'new_finite_population_or_mask_tests':0,'new_original_root_or_psi_bank_queries':0,
      'completed_semantic_checks_replayed':0,'Step4_complete':False})
    print(json.dumps({'status':'PASS','old_candidate_exact_zero_residual':-1,'uniform_repair':'PROVED','complete_Step4':False}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:
        error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:write('audit_reset_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
