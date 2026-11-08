"""Independent exact rational falsifier; original source checks reused by pin."""
import json,time,hashlib,fractions,sys,importlib.util
from pathlib import Path
B=Path(__file__).resolve().parent;F=fractions.Fraction
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    z=json.loads((B/'quadratic_formula_actual_source_test.json').read_text());proof=json.loads((B/'uniform_feature_dual_independent_audit.json').read_text());source=json.loads((B/'uniform_feature_dual_source_certificate.json').read_text());assert hashlib.sha256((B/'uniform_feature_dual_source_certificate.json').read_bytes()).hexdigest()==proof['input_sha256']['uniform_feature_dual_source_certificate.json'];fail=z['failures'][0];s=source['witnesses'][int(fail['source'].split('_')[1])];rows={r['occurrence']:r for r in s['rows']};rr=[rows[t] for t in fail['occurrences']];assert len(rr)==1 and rows[rr[0]['occurrence']-1]['genuine_F'] and rr[0]['genuine_F'];c=[F(v) for v in z['formula_exact_rational_interpretation']];before=fail['feature_before'];after=fail['feature_after'];qb=lambda f:f+[f[i]*f[j] for i in range(20) for j in range(i,20)];assert rr[0]['before'][0]==rr[0]['before'][1] and rr[0]['after'][0]==rr[0]['after'][1];change=sum(v*(b-a) for v,a,b in zip(c,qb(before),qb(after)));margin=2*sum(r['a'] for r in rr)-sum(r['qF'] for r in rr)+change;assert margin==F(fail['exact_margin'])<0
    out('quadratic_formula_independent_refutation.json',{'status':'PASS_EXACT_FROZEN_QUADRATIC_FORMULA_REFUTATION','source':fail['source'],'occurrences':fail['occurrences'],'original_source_verification_reused':True,'H':1,'Q':1,'exact_margin':str(margin),'diagonal_A_equals_B_at_both_boundaries':True,'only_this_formula_refuted':True,'entire_quadratic_family_refuted':False,'new_source_queries':0,'principal_U33':'OPEN','external_or_formal_verification':False,'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('quadratic_formula_actual_source_test.json','uniform_feature_dual_source_certificate.json','uniform_feature_dual_independent_audit.json')}});print(json.dumps({'status':'PASS_EXACT_QUADRATIC_CANDIDATE_REFUTATION','margin':str(margin),'no_source_rerun':True}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify24_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
