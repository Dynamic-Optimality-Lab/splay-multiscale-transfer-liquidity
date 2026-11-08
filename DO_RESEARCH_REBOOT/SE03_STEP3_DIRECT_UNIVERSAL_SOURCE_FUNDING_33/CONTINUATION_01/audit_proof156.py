"""The retirement control also defeats every <=2-event ordinary comparison."""
import hashlib,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    Z=json.loads((B/'native10_source_actions.json').read_text());e=json.loads((B/'single_private_retirement_preimage_candidate.json').read_text())['candidate'];rows=[];x=e['target_actual_key']//2;target=e['target_contraction_index']
    for a in e['source_contraction_indices']:
        for helper in [None]+list(range(1,11)):
            mid=a if helper is None else Z['destination'][a][helper-1];h=0 if helper is None else Z['H'][a][helper-1];dest=Z['destination'][mid][x-1];h+=Z['H'][mid][x-1]
            rows.append({'old_source':a,'optional_DELETE_proxy':helper,'terminal_KEEP':x,'ordinary_H':h,'old_destination':dest,'matches_target':dest==target})
    assert len(rows)==22 and not any(r['ordinary_H']<=2 and r['matches_target'] for r in rows)
    assert time.process_time()-START<CAP-1
    out('retirement_two_event_comparison_certificate.json',{'status':'NO_TWO_EVENT_OLD_COMPARISON_FOR_EXACT_RETIREMENT_CONTROL','old_sources':e['source_contraction_indices'],'unique_old_target':target,'all_comparisons':rows,'exhaustiveness':'With total H<=2 there are at most two positive accesses; the final root is x. Zero repeats can be removed for calculation only, so the possibilities are direct x or one arbitrary old DELETE proxy then x. All original operations remain in the actual source word.','not_a_CD_counterexample':True,'source_queries':0,'source_engine_calls':0,'principal_U33':'OPEN','input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('single_private_retirement_preimage_candidate.json','retirement_preimage_closed_source.json','native10_source_actions.json')}})
    print(json.dumps({'status':'NO_TWO_EVENT_OLD_COMPARISON','cases':22,'ordinary_target':target,'principal_U33':'OPEN'}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof156_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
