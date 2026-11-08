"""Adversarial exact test of the frozen quadratic formula on ACCEPTED sources."""
import json,time,hashlib,fractions
from pathlib import Path
B=Path(__file__).resolve().parent;F=fractions.Fraction
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def load_features():
    # Reuse independently checked SET-based feature specification, not a splay run.
    import importlib.util,sys
    old=sys.argv[:];sys.argv=[sys.argv[0],'20','0'];sp=importlib.util.spec_from_file_location('accepted_set_features33',B/'audit_verify23.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);sys.argv=old;return m.features
def main():
    features=load_features();candidate=json.loads((B/'quadratic_feature_result_02.json').read_text());assert candidate['status']=='FINITE_QUADRATIC_SOURCE_CANDIDATE_NOT_UNIVERSAL';coeff=[F(str(v)) for v in candidate['coefficients_unscaled']];source=json.loads((B/'uniform_feature_dual_source_certificate.json').read_text());audit=json.loads((B/'uniform_feature_dual_independent_audit.json').read_text());assert hashlib.sha256((B/'uniform_feature_dual_source_certificate.json').read_bytes()).hexdigest()==audit['input_sha256']['uniform_feature_dual_source_certificate.json'];sources=[('dual_'+str(i),z) for i,z in enumerate(source['witnesses'])];old=json.loads((B/'native10_width2_source_countercertificate.json').read_text());sources.append(('range_three_source',old));checked=0;failures=[]
    def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
    def basis(v):return v+[v[i]*v[j] for i in range(20) for j in range(i,20)]
    for name,z in sources:
        rows=z['rows'];ends=[i for i,r in enumerate(rows) if r['genuine_F']]
        for j,end in enumerate(ends):
            p=ends[j-1];rr=rows[p+1:end+1] if p<end else rows[p+1:]+rows[:end+1];before=basis(features(*fr(rr[0]['before'][:2])));after=basis(features(*fr(rr[-1]['after'][:2])));H=sum(r['a'] for r in rr);Q=sum(r['qF'] for r in rr);delta=sum(c*(v-u) for c,u,v in zip(coeff,before,after));margin=2*H-Q+delta;checked+=1
            if margin<0:failures.append({'source':name,'occurrences':[r['occurrence'] for r in rr],'H':H,'Q':Q,'price':2*H-Q,'debt_change':str(delta),'exact_margin':str(margin),'margin_float':float(margin),'feature_before':before[:20],'feature_after':after[:20],'is_actual_natural_packet':True,'source_audit':'uniform_feature_dual_independent_audit.json' if name!='range_three_source' else 'native10_width3_lower_independent_audit.json'})
    failures.sort(key=lambda z:F(z['exact_margin']));result={'status':'FROZEN_QUADRATIC_FORMULA_SOURCE_REFUTED' if failures else 'NO_ACCEPTED_CORPUS_FAILURE_NOT_UNIVERSAL_PROOF','checked_actual_natural_packets':checked,'negative_packets':len(failures),'failures':failures,'formula_exact_rational_interpretation':[str(c) for c in coeff],'scope':'only this fitted formula, NOT the entire degree-two family','new_source_queries':0,'accepted_source_replay_not_repeated':True,'principal_U33':'OPEN','input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('quadratic_feature_result_02.json','uniform_feature_dual_source_certificate.json','uniform_feature_dual_independent_audit.json','native10_width2_source_countercertificate.json')}};out('quadratic_formula_actual_source_test.json',result);print(json.dumps({'status':result['status'],'checked_packets':checked,'failures':len(failures),'strongest':failures[0] if failures else None}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof40_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
