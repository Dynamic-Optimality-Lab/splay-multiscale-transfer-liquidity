"""Final exact novelty/claim audit; no replay of accepted source-term checks."""
import json,sys,time
from fractions import Fraction
from pathlib import Path
B=Path(__file__).resolve().parent
def read(n):return json.loads((B/n).read_text())
def write(n,d):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(d,f,indent=2)
def add(terms,multipliers):
    out={}
    for t,m in zip(terms,multipliers):
        for k,v in t.items():out[k]=out.get(k,Fraction(0))+Fraction(m)*v
    return {k:v for k,v in out.items() if v}
def main():
    a=read('repeat_gap_independent_audit.json')
    assert a['status']=='INDEPENDENT_SE02_REPEAT_GAP_AUDIT_PASS'
    assert a['proper_paired_closed_subwalks']==0
    assert a['direct_and_indirect_marginal']=='1+1 per B-return pulse'
    # Pure universally quantified count identity: no original source executed.
    ge={'CE':2,'QE':-1}
    eqC={'C':1,'CE':-1,'m':-2};eqQ={'Q':1,'QE':-1,'m':-2}
    assert add([ge,eqC,eqQ],[1,2,-1])=={'C':2,'Q':-1,'m':-2}
    geA={'A':1,'C':-1}
    assert add([ge,eqC,eqQ,geA],[1,2,-1,2])=={'A':2,'Q':-1,'m':-2}
    text=' '.join((B/'B_COMPOSITION_AUDIT.md').read_text().split())
    for part in ('B-closed two-key','C_full=C_E+2m','known B-compositional closure',
                 'genuinely new original CD coverage','NOT established','does not invalidate the restricted law'):
        assert part in text,part
    assert time.process_time()<float(sys.argv[1])
    write('scope_audit.json',{
      'status':'FINAL_SCOPE_AUDIT_PASS_GENUINE_NEW_COVERAGE_NOT_ESTABLISHED',
      'restricted_credit_law_valid':True,'paired_simple_family_valid':True,
      'return_pulse_class_in_completed_B_only_compositional_closure':True,
      'strict_raw_predicate_domain_separation':True,
      'genuinely_new_CD_coverage_established':False,
      'new_source_explicit_credit_certificate':'restricted repeat-gap reservation; not an uncovered global CD case',
      'uniform_support_induction_proved':False,'unrestricted_CD_proved':False,
      'additional_universal_affine_count_proofs':2,'accepted_source_checks_replayed':0,
      'new_finite_tests':0,'new_solver_queries':0,'Bank25':25})
    print(json.dumps({'status':'FINAL_SCOPE_AUDIT_PASS','genuinely_new_CD_coverage':False,'universal_CD':'OPEN'}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:write('audit_scope_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
