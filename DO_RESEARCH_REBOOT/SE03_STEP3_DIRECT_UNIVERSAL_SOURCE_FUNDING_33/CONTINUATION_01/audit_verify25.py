"""Complete independent diagonal feature reconstruction for verify24's margin."""
import json,time,hashlib,fractions
from pathlib import Path
B=Path(__file__).resolve().parent;F=fractions.Fraction
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    z=json.loads((B/'quadratic_formula_actual_source_test.json').read_text());old=json.loads((B/'quadratic_formula_independent_refutation.json').read_text());assert all(hashlib.sha256((B/n).read_bytes()).hexdigest()==v for n,v in old['input_sha256'].items());source=json.loads((B/'uniform_feature_dual_source_certificate.json').read_text());fail=z['failures'][0];s=source['witnesses'][int(fail['source'].split('_')[1])];row=next(r for r in s['rows'] if r['occurrence']==fail['occurrences'][0])
    def diag(tree):
        depths=[];sizes=[]
        def visit(t,d):
            if isinstance(t,str):return 0
            k,l,r=t;n=1+visit(l,d+1)+visit(r,d+1);depths.append(d);sizes.append(n);return n
        n=visit(tree,0);ranks=[v.bit_length()-1 for v in sizes];D=sum(depths);DD=sum(v*v for v in depths);S=sum(sizes);SS=sum(v*v for v in sizes);R=sum(ranks);RR=sum(v*v for v in ranks);return [D,D,DD,DD,SS,SS,R,R,n,n,S,0,DD,SS,S,RR,0,n,0,n]
    before=diag(row['before'][0]);after=diag(row['after'][0]);assert before==fail['feature_before'] and after==fail['feature_after'];qb=lambda v:v+[v[i]*v[j] for i in range(20) for j in range(i,20)];margin=F(2*row['a']-row['qF'])+sum(F(c)*(a-b) for c,a,b in zip(z['formula_exact_rational_interpretation'],qb(after),qb(before)));assert margin==F(fail['exact_margin'])<0
    out('quadratic_formula_complete_independent_refutation.json',{'status':'PASS_SOURCE_FEATURES_AND_EXACT_QUADRATIC_MARGIN','source_packet':fail['occurrences'],'exact_margin':str(margin),'original_source_reused_by_accepted_hash':True,'new_independent_diagonal_feature_reconstruction':True,'prior_verify24':'exact arithmetic receipt; completed here by independent feature reconstruction','new_source_queries':0,'only_specific_formula_refuted':True,'principal_U33':'OPEN','input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('quadratic_formula_actual_source_test.json','quadratic_formula_independent_refutation.json','uniform_feature_dual_source_certificate.json')}});print(json.dumps({'status':'PASS_COMPLETE_QUADRATIC_CANDIDATE_REFUTATION','exact_margin':str(margin)}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify25_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
