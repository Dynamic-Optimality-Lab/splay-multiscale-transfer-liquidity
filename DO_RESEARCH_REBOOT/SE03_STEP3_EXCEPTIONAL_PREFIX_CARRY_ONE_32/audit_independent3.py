"""Zero-query independent arithmetic bridge for the new restricted proofs.
No original/source tree query, new source relation or splay execution.
The bounded debt/excess coordinate checks use already-proved exact ranges;
they do not sample source populations or prove the source inductions.
"""
import json,time,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    casesN=casesH=0
    for start in (1,2):
        for end in range(4):
            for E in range(5):
                if end-E<=1:
                    assert start-end+E>=0;casesN+=1
            assert start-end+4-1>=1;casesN+=1
            for Q in range(1,7):
                for excess_beyond_ancestors in range(5):
                    M=6-min(Q,2)+excess_beyond_ancestors-end
                    assert M>=1 and start-1+M>=1;casesH+=1
    new=json.loads((B/'transient13_independent_audit.json').read_text());assert new['intermediate_debt']==2 and not new['terminal_counterexample']
    old=json.loads((B/'static_independent_audit.json').read_text());assert old['status'].startswith('PASS_')
    names=['SS_SOURCE_BOUNDARY_COMPLETION.md','HIGH_RETURN_CARRY_THEOREM.md','DISTINGUISHED_7_SOURCE_PERSISTENCE.md',
           'OPEN_CHART_AND_TERMINAL_INTERFACES.md','PRE_ACTIVATION_CARRY_THEOREM.md','UPPER_ONLY_BARRIER.md']
    out('restricted_proof_arithmetic_audit.json',{'status':'PASS_RESTRICTED_BOUND_RANGE_ARITHMETIC','new_source_queries':0,
        'no9_exact_range_cells':casesN,'HIGH_return_exact_range_cells':casesH,
        'no9_result':'D_out<=1 subject to proved local grammar/source and root-bound bridge',
        'immediate9_HIGH_return_result':'D_out=0 subject to proved complete q5-packet and local table bridge',
        'source_inductions_formal_or_kernel_audit':False,'external_audit':False,'principal_FR32_CARRY1':'OPEN',
        'metadata_pins_do_not_prove_source_induction':True,
        'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in names}})
    print(json.dumps({'status':'RESTRICTED_PROOF_ARITHMETIC_PASS','source_queries':0,'principal_CARRY1':'OPEN'}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_independent3_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0,'source_queries':0})
