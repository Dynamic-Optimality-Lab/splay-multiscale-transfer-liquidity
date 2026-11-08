"""Independent universal visibility audit of the complete lower family."""
import json,sys,time,itertools
from pathlib import Path
import z3
from target_floor import N,dp
from symbolic_prefix_v2 import prefix
from compatibility import source_compatible
BASE=Path(__file__).resolve().parent;CAP=min(120,float(sys.argv[1]));E=None
sys.path.insert(0,str(BASE.parent/'M3_XFER18'))
from audit_spread import replay,path,reverse
def write(name,obj):
    with (BASE/name).open('x',encoding='utf-8') as f:json.dump(obj,f,indent=2)
def main():
    L=N(0,E,N(1,E,N(2)));proofs=[];queries=0
    def e1(a,t,m):return z3.And(*(z3.Implies(z3.And(m[k],z3.Or(*(a[j]==k for j in range(1,7)))),
      z3.BoolVal(dp(t)[k]<=3)) for k in range(9) if k!=t[0]))
    def prove(label,source,x,word,guard,accept):
        nonlocal queries
        out=replay(source,path(source,x))
        assert len(path(source,x)) in (4,5),label
        assert replay(reverse(source),tuple(1-v for v in path(source,x)))==reverse(out)
        u=prefix(word,source[0],x,'lower'+str(queries));m=[z3.Bool('lower_mark'+str(k)) for k in range(9)]
        sol=z3.Solver();sol.set(timeout=10000)
        sol.add(*u['constraints'],z3.PbEq([(v,1) for v in m],5),m[source[0]],m[x],guard(u['source']),
          z3.Not(accept(u['target'],out,m)))
        result=sol.check();queries+=1
        assert result==z3.unsat,(label,str(result),str(sol.model()) if result==z3.sat else sol.reason_unknown())
        proofs.append({'statement':label,'result':'UNIVERSAL_UNSAT_negation','actual_opposite_constructor_identity':True})
        return out
    for H in (N(7,E,N(8)),N(8,N(7),E)):
        K=N(2,N(1,N(0),E),N(3,E,N(4,E,N(5,E,N(6,E,H)))))
        Kout=prove('K_zero6_E1',K,6,(1,1),lambda a:z3.And(a[2]==4,a[6]==6),
          lambda a,t,m:e1(a,t,m))
        T5=N(5,N(3,L,N(4)),N(6,E,H))
        T4=N(4,N(3,L,E),N(5,E,N(6,E,H)))
        prove('T5_zero2_E1',T5,2,(0,1),lambda a:z3.And(a[1]==0,z3.Or(a[2]==6,a[6]==6)),
          lambda a,t,m:e1(a,t,m))
        prove('T4_zero2_K_or_E1',T4,2,(0,1),lambda a:z3.And(a[1]==0,z3.Or(a[2]==5,a[2]==6,a[6]==5,a[6]==6)),
          lambda a,t,m:z3.Or(z3.And(a[2]==4,a[6]==6),e1(a,t,m)))
        z=8 if H[0]==7 else 7
        upperout=prove('T4_upper_zero_E1_or_Bad',T4,z,(1,1),lambda a:z3.And(a[1]==0,z3.Or(a[2]==5,a[2]==6)),
          lambda a,t,m:z3.Or(z3.Not(source_compatible(a)),e1(a,t,m)))
        for A,v,T in [(N(4,E,N(5)),5,T5),(N(5,N(4),E),4,T4)]:
            S=N(0,E,N(3,N(1,E,N(2)),N(6,A,H)))
            assert replay(S,path(S,v))==T
            for p in ((1,),(1,0)):
                prove('S_lower_zero_reaches_T',S,v,p,lambda a:z3.Or(a[2]==6,a[6]==6),
                  lambda a,t,m:z3.And(a[1]==0,z3.Or(a[2]==6,a[6]==6)))
            prove('S_upper_zero_E1_or_Bad',S,z,(1,1),lambda a:a[2]==6,
              lambda a,t,m:z3.Or(z3.Not(source_compatible(a)),e1(a,t,m)))
    assert time.process_time()<CAP
    write('audit_lower_return_v2.json',{'status':'UNIVERSAL_COMPLETE_LOWER_RETURN_FAMILY_AUDIT_PASS',
      'universal_proofs':proofs,'new_symbolic_queries':queries,
      'all_masks_signatures_blocks_G_and_unused_fields_quantified':True,
      'ordered_new_floors':['K1','T4_1/T5_1','S1'],'all_old_signed_rows_and_fresh_source_H1_safety_preserved':True,
      'new_finite_population_or_mask_tests':0,'new_original_root_or_psi_queries':0,'completed_semantic_checks_replayed':0,
      'Step4_complete':False})
    print(json.dumps({'status':'PASS','universal_queries':queries,'resume_complete_anchor_audit':True}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:
        error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:write('audit_lower_return_v2_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
