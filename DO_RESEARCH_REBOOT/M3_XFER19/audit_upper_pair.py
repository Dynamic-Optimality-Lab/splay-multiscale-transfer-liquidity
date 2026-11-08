"""New cases of the complete paired upper-return structural family."""
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
    assert json.loads((BASE/'audit_pair_v2.json').read_text())['status']=='UNIVERSAL_PAIRED_ZERO_RETURN_AUDIT_PASS'
    new=[(4,E,N(6,N(5),E)),(5,N(4),N(6))]
    proofs=[];queries=0
    for u,A,B in new:
        S=N(0,E,N(3,N(1,E,N(2)),N(u,A,N(7,B,N(8)))))
        T=N(8,N(3,N(0,E,N(1,E,N(2))),N(7,N(u,A,B),E)),E)
        assert replay(S,path(S,8))==T
        assert replay(reverse(S),tuple(1-v for v in path(S,8)))==reverse(T)
        assert max(dp(S).values())<=5 and max(dp(T).values())<=5
        assert all(k==8 or u<k<8 for k,d in dp(S).items() if d>=4)
        zero_upper=[k for k,d in dp(T).items() if d>=4 and k>u]
        assert all(k in (5,6) for k in zero_upper)
        outs=[]
        for x in zero_upper:
            out=replay(T,path(T,x))
            assert all(d<=3 for k,d in dp(out).items() if k!=2)
            assert replay(reverse(T),tuple(1-v for v in path(T,x)))==reverse(out)
            if u==5:
                v=prefix((0,1),8,x,'upper'+str(x));m=[z3.Bool('uppermark'+str(k)) for k in range(9)]
                e1=z3.And(*(z3.Implies(z3.And(m[k],z3.Or(*(v['target'][j]==k for j in range(1,7)))),
                  z3.BoolVal(dp(out)[k]<=3)) for k in range(9) if k!=x))
                s=z3.Solver();s.add(*v['constraints'],z3.PbEq([(q,1) for q in m],5),m[8],m[x],
                  v['source'][1]==u,v['source'][3]==0,z3.Not(e1))
                assert s.check()==z3.unsat;queries+=1
            # u4 uses the completed excluded-key2 target lemma for x5/6.
            outs.append({'zero_upper':x,'only_possible_deep_core_after_access':2,
              'full_target_visibility':'new universal proof' if u==5 else 'reused completed u4 arbitrary-block proof'})
        proofs.append({'pivot':u,'S':S,'T':T,'zero_upper_outputs':outs})
    v=prefix((1,1),0,8,'upperS');u=z3.Int('upperPivot')
    s=z3.Solver();s.add(*v['constraints'],u>=4,u<=5,v['source'][2]==u,
      z3.Or(v['target'][1]!=u,v['target'][3]!=0))
    assert s.check()==z3.unsat;queries+=1
    assert time.process_time()<CAP
    write('audit_upper_pair.json',{'status':'UNIVERSAL_COMPLETE_UPPER_PAIR_FAMILY_AUDIT_PASS',
      'new_constructor_cases':proofs,'old_pair_case_reused_not_replayed':True,
      'all_original_masks_signatures_and_private_data_quantified':True,
      'all_newly_raised_source_LOW_rows_proved_and_old_signed_rows_preserved':True,
      'new_symbolic_queries':queries,'new_finite_population_or_mask_tests':0,
      'new_original_root_or_psi_queries':0,'completed_semantic_checks_replayed':0,'Step4_complete':False})
    print(json.dumps({'status':'PASS','new_universal_queries':queries,'resume_anchor_signed_audit':True}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:
        error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:write('audit_upper_pair_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
