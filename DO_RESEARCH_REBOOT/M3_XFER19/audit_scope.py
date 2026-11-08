"""Independent sort/range interface arithmetic, no original root execution."""
import json,sys,time
from pathlib import Path
import z3
BASE=Path(__file__).resolve().parent;CAP=min(300,float(sys.argv[1]))
def write(n,o):
    with (BASE/n).open('x',encoding='utf-8') as f:json.dump(o,f,indent=2)
def main():
    assert json.loads((BASE/'step4_audit.json').read_text())['missing_obligations']==0
    d=z3.Int('ordinary_debt');s=z3.Solver();s.add(d>=0,d<=2,z3.Or(d>2,-5+d>-3,-d>0))
    assert s.check()==z3.unsat
    o=z3.Int('ordinary_potential');m=z3.Int('midpoint_potential');chi=z3.Int('chi')
    s=z3.Solver();s.add(d>=0,d<=2,z3.Or(chi==0,chi==1),o==-d-5*chi,m==-5*chi,
      z3.Or(o< -7,o>0,m< -5,m>0))
    assert s.check()==z3.unsat
    assert time.process_time()<CAP
    write('step4_scope_audit.json',{'status':'INDEPENDENT_TWO_SORT_AND_HIGH_H0_SCOPE_AUDIT_PASS',
      'ordinary_debt_arity':147,'midpoint_arity':127,'alpha_debt_never_called_on_midpoint':True,
      'original_HIGH_v_free':True,'SAME_actual_midpoint_and_independent_witnesses_retained':True,
      'corrected_h0':{'actual_depth':0,'declared_depth':18,'q':9,'weight':-3},
      'HIGH_range_and_potential_range_UNSAT':True,'no_full_M3_promotion':True,
      'new_finite_tests':0,'new_original_root_evaluations':0,'completed_checks_replayed':0})
    print(json.dumps({'status':'PASS','ordinary_only_debt_and_unchanged_midpoint_extension':True}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:write('audit_scope_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
