"""Bounded integer-cell proof audit of the uniform ENTRY reduction. No tree
engine, original source query, compiler or finite-population experiment.
The P>=2 tail is proved by its nonnegative base and positive slope1.
"""
import json,time
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    cases=[];negative=[]
    for theta in (0,1,2):
        for price in (0,1,2):
            for upper in (11,13):
                c=2 if price<=1 and (upper==13 or theta==0) else 1
                sigma=2*c-(1 if upper==11 else 2)-int(theta>0);before=price+theta-2;total=before+sigma
                z={'theta':theta,'P_low_cell':('>=2' if price==2 else price),'upper':upper,'source_forced_c_lower_bound':c,
                   'untruncated_before':before,'minimum_upper_sigma':sigma,'minimum_prefix_through_upper':total,'tail_slope':1}
                cases.append(z)
                if total<0:negative.append(z)
                if price==2:assert total>=0 # the entire tail then follows with slope1
    assert len(negative)==1 and negative[0]['theta']==1 and negative[0]['P_low_cell']==0 and negative[0]['upper']==11 and negative[0]['minimum_prefix_through_upper']==-1
    c=json.loads((B/'prefix_first_return_countercertificate_v2.json').read_text());assert c['Sigma_low']==0 and c['D_entry']==1 and c['R_return']==0
    assert c['ledger'][3]['target']==11 and c['ledger'][3]['H']==1 and c['ledger'][3]['sigma_E']==0
    out('entry_compensation_algebra_audit.json',{'status':'PASS_COMPLETE_INTEGER_CELL_ENTRY_REDUCTION','cases':cases,'single_residual_case':negative[0],
        'logical_source_premises':'P_low>=0, theta0..2, source low/right-chain invariance forces c bounds as proved in ENTRY_COMPENSATION_REDUCTION.md',
        'unbounded_tail_proof':'P_low>=2 has slope+1; c>=1, so nonnegative base at2 proves all larger integer prices',
        'role':'complete arithmetic bridge for the entry source theorem, NOT proof of all subsequent return paths or all original source realizability',
        'new_source_queries':0,'FR31_PREFIX_first_return_refuted':True,'FR31_FIX_status':'OPEN'})
    print(json.dumps({'status':'ENTRY_COMPENSATION_ALGEBRA_PASS','integer_cells':len(cases),'residual':negative[0],'source_queries':0}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_algebra_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0,'source_queries':0})
