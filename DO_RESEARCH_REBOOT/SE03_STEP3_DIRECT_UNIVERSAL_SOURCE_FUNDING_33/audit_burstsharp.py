"""Independent static strengthening of the accepted source obstruction."""
import json,time,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent
def main():
    z=json.loads((B/'Gamma55_original_source.json').read_text());a=json.loads((B/'endpoint_obstruction_independent_audit.json').read_text())
    assert a['status']=='PASS_GAMMA55_SOURCE_AND_ALL_MATCHING_ENDPOINT_OBSTRUCTION'
    row=next(v for v in z['rows'] if v['occurrence']==333)
    q=len([e for e in row['BF_events'] if e['kind']=='DOUBLE']);qe=len([e for e in row['BE_events'] if e['kind']=='DOUBLE'])
    assert (q,qe)==(54,53)
    # q=p+f, p,f>=0. If both relevant banks are<=25, p+f<=50,
    # contradicting q>50. No matching sample/enumeration is substituted.
    assert q>50 and qe>50 and (q+1)//2==(qe+1)//2==27
    result={'status':'PASS_ALL_MATCHING_B_REPLAY_LOWER_BOUND','full_endpoint_lower_bound':27,'common_endpoint_lower_bound':27,
        'B25_full_feasible':False,'B25_common_feasible':False,'arbitrary_support_formula':['ceil((r-1)/2)','ceil((r-2)/2)'],
        'new_source_queries':0,'original_GateU14_working_contract_refuted':False,
        'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('Gamma55_original_source.json','ENDPOINT_BURST_SHARPENING.md')}}
    with (B/'burst_sharp_independent_audit.json').open('x') as f:json.dump(result,f,indent=2)
    print(json.dumps(result))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_burstsharp_exit.json').open('x') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
