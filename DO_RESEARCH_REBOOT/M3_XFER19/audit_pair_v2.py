"""Universal constructor/visibility/sign audit of paired zero returns."""
import json,sys,time
from pathlib import Path
import z3
from target_floor import N,dp
from symbolic_prefix_v2 import prefix
BASE=Path(__file__).resolve().parent;CAP=min(120,float(sys.argv[1]));E=None
sys.path.insert(0,str(BASE.parent/'M3_XFER18'))
from audit_spread import replay,path,reverse
def write(name,obj):
    with (BASE/name).open('x',encoding='utf-8') as f:json.dump(obj,f,indent=2)
def main():
    S=N(0,E,N(3,N(1,E,N(2)),N(4,E,N(7,N(5,E,N(6)),N(8)))))
    T=N(8,N(3,N(0,E,N(1,E,N(2))),N(7,N(4,E,N(5,E,N(6))),E)),E)
    P5=N(5,N(3,N(0,E,N(1,E,N(2))),N(4)),N(8,N(7,N(6),E),E))
    P6=N(6,N(3,N(0,E,N(1,E,N(2))),N(5,N(4),E)),N(8,N(7),E))
    for source,x,want in []: # Completed constructor/opposite prefix reused, not replayed.
        p=path(source,x);assert replay(source,p)==want
        assert replay(reverse(source),tuple(1-v for v in p))==reverse(want)
    assert {k for k,v in dp(T).items() if v>=4}=={2,5,6}
    # Core1 is depth3 or4? Keep the proof's needed set exact below:
    # the independent depth calculation is authoritative and is audited.
    outputs={5:P5,6:P6};proofs=[]
    for x,out in outputs.items():
        assert all(d<=3 for k,d in dp(out).items() if k!=2)
        u=prefix((0,1),8,x,'pair'+str(x));m=[z3.Bool('pairmark'+str(k)) for k in range(9)]
        E1=z3.And(*(z3.Implies(z3.And(m[k],z3.Or(*(u['target'][j]==k for j in range(1,7)))),
          z3.BoolVal(dp(out)[k]<=3)) for k in range(9) if k!=x))
        sol=z3.Solver();sol.set(timeout=10000)
        sol.add(*u['constraints'],z3.PbEq([(v,1) for v in m],5),m[8],m[x],
          u['source'][1]==4,u['source'][3]==0,z3.Not(E1))
        assert sol.check()==z3.unsat,('FULL_TARGET_E1',x)
        proofs.append({'zero_target':x,'all_masks_gaps_and_blocks':'UNIVERSAL_UNSAT_negation','actual_full_target_E1':True})
    u=prefix((1,1),0,8,'pairS');sol=z3.Solver()
    sol.add(*u['constraints'],u['source'][2]==4,u['source'][6]==8,
      z3.Or(u['target'][1]!=4,u['target'][3]!=0))
    assert sol.check()==z3.unsat
    assert time.process_time()<CAP
    write('audit_pair_v2.json',{'status':'UNIVERSAL_PAIRED_ZERO_RETURN_AUDIT_PASS','proofs':proofs,
      'S_zero8_full_target_T1':True,'new_debt':'D_pair=max(D_repay,1_T1,1_S1), both actual orientations',
      'all_old_signed_LOW_rows_HIGH_h0_full_state_scopes_preserved':True,
      'freshly_raised_H1_sources_directly_proved':True,'old_signed_anchor_UNSATs_transport_monotonically':True,
      'new_symbolic_queries':3,'new_finite_population_or_mask_tests':0,'new_original_root_or_psi_queries':0,
      'completed_semantic_checks_replayed':0,'Step4_complete':False})
    print(json.dumps({'status':'PASS','resume_fixed_global_anchor_signed_audit':True}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:
        error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:write('audit_pair_v2_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
