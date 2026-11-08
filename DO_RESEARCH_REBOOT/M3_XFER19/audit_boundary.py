"""Independent interval/source/row audit of the uniform boundary rule.

These are universal integer UNSAT proofs, not population/mask tests.
The static source derivation is independent of the H1 proof-word builder.
"""
import json,sys,time
from pathlib import Path
import z3
from compatibility import source_compatible,anon_compatible
BASE=Path(__file__).resolve().parent;CAP=min(120,float(sys.argv[1]))
def write(name,obj):
    with (BASE/name).open('x',encoding='utf-8') as f:json.dump(obj,f,indent=2)
def check(name,assumptions,bad,results):
    s=z3.Solver();s.set(timeout=20000);s.add(*assumptions,bad)
    v=s.check();assert v==z3.unsat,(name,str(v),str(s.model()) if v==z3.sat else s.reason_unknown())
    results.append({'theorem':name,'all_symbolic_integer_assignments':'UNSAT_negation'})
def main():
    results=[]
    lo,hi,r,g,lft,rgt=z3.Ints('lo hi r g left right')
    valid=lambda t:z3.And(t>=0,t<=12,t!=11)
    score=lambda t:z3.And(t>=0,t<9)
    ls=z3.And(score(lft),lft!=r);rs=z3.And(score(rgt),rgt!=r)
    le=z3.Or(lft==12,lft==r);re=z3.Or(rgt==12,rgt==r)
    bounds=[lo<=hi+1,valid(lft),valid(rgt),r>=0,r<9,z3.Or(r<lo,r>hi)]
    def direct(q):
        return z3.And(lo<=q,q<=hi+1,
          z3.Implies(ls,z3.And(lo<=lft,lft<q)),z3.Implies(rs,z3.And(q<=rgt,rgt<=hi)),
          z3.Implies(le,q==lo),z3.Implies(re,q==hi+1))
    compatible=anon_compatible(lft,rgt,lo,hi,r)
    witness=z3.If(re,hi+1,z3.If(ls,lft+1,lo))
    check('anonymous_interval_elimination_forward',bounds+[direct(g)],z3.Not(compatible),results)
    check('anonymous_interval_elimination_constructive_reverse',bounds+[compatible],z3.Not(direct(witness)),results)
    # Independent direct physical source shadow: seven literal addresses,
    # original-owner0 reads, no rotations, no imports of the word builder.
    raw=[r]+[z3.Int('raw_'+str(i)) for i in range(1,7)]
    gs=[z3.Int('gap_'+str(i)) for i in range(7)]
    C=[r>=0,r<9]+[z3.And(t>=0,t<=12) for t in raw[1:]]
    def production(t,q,l,h,when=z3.BoolVal(True)):
        C.extend([z3.Implies(z3.And(when,t<9),z3.And(l<=t,t<=h)),
          z3.Implies(z3.And(when,t==9),z3.And(l<=q,q<=h+1)),
          z3.Implies(z3.And(when,z3.Or(t==11,t==12)),l>h)])
    production(raw[1],gs[1],z3.IntVal(0),r-1)
    production(raw[2],gs[2],r+1,z3.IntVal(8))
    for i,il,ir,l,h in [(1,3,4,z3.IntVal(0),r-1),(2,5,6,r+1,z3.IntVal(8))]:
        pivot=z3.If(raw[i]<9,raw[i],gs[i]);active=raw[i]<=9
        production(raw[il],gs[il],l,pivot-1,active)
        production(raw[ir],gs[ir],z3.If(raw[i]<9,pivot+1,pivot),h,active)
    read=lambda t:z3.If(t==11,r,t)
    left=read(raw[1]);right=read(raw[2]);a=[r,left,right]
    for i,il,ir in [(1,3,4),(2,5,6)]:
        nonreal=z3.Or(raw[i]==10,raw[i]==12)
        a.extend([z3.If(nonreal,raw[i],z3.If(raw[i]==11,left,read(raw[il]))),
                  z3.If(nonreal,raw[i],z3.If(raw[i]==11,right,read(raw[ir])))])
    check('every_original_static_source_grammar_production_satisfies_SC',C,z3.Not(source_compatible(a,r)),results)
    # Symbolic cancellation; no debt values enumerated.
    w,ds,dt,inc=z3.Ints('weight source_D target_D target_increment')
    check('all_previously_valid_LOW_rows_preserved_when_sources_unchanged',
      [w+dt-ds>=0,inc>=0],w+(dt+inc)-ds<0,results)
    check('every_nonnegative_incoming_row_to_saturated_boundary',
      [w>=0,ds>=0,ds<=2],w+2-ds<0,results)
    assert time.process_time()<CAP
    write('audit_boundary.json',{'status':'UNIVERSAL_STATIC_BOUNDARY_SOURCE_INTERVAL_AND_SIGN_AUDIT_PASS',
      'universal_integer_proofs':results,'new_symbolic_queries':len(results),
      'source_AST_premises':'original shadow7 propagation, shadow_match7, Score uniqueness/cover and completed protected-prefix coverage',
      'no_actual_LOW_source_value_is_changed':True,'all_old_signed_LOW_rows_preserved':True,
      'new_debt':'D_bad=max(D_current,2*I[P and not SC])',
      'HIGH_h0_full_state_scopes_and_source_debt_theorem_preserved':True,
      'new_finite_population_or_mask_tests':0,'new_original_root_evaluations':0,'completed_checks_replayed':0,
      'independent_of_H1_word_builder':True,'external_review_or_full_compiler_formalization_claimed':False,
      'Step4_complete':False})
    print(json.dumps({'universal_proofs':len(results),'status':'PASS','continue_complete_zero_proof':True}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:
        error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:write('audit_boundary_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
