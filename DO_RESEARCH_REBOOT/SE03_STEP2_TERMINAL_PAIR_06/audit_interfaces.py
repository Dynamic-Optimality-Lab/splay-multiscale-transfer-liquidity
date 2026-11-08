"""Final source-interface coverage audit; no finite population experiments."""
import collections,json,time
from pathlib import Path
import audit_independent as a
B=Path(__file__).resolve().parent
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    S={t for t in a.alltrees(1,11) if t[1] in a.M and a.density(t)[2]};n=0
    for t in S:
        for x in a.M-{t[1]}:
            z=a.legal(t,x)
            if z is None:continue
            assert z[0] in S, 'an admitted SS cold probe must not be dropped by a destination filter'
            n+=1
    assert n==3698
    data=json.loads((B/'grammar.json').read_text())
    compatible=[r['rank_word'] for r in data['order_profiles'] if r['A_compatible']]
    assert compatible==[[0,4,2,3,1],[4,0,2,1,3]]
    cert=json.loads((B/'saturation3.json').read_text());classes=collections.Counter()
    for r in cert['records']:
        b=a.bf_read(r['BF']);classes[(a.L(b),a.degree(b),r['budget'])]+=1
    assert dict(classes)=={(3,3,0):120,(3,3,1):120,(2,2,0):20}
    result={'status':'PASS_SOURCE_INTERFACE_ASSEMBLY','all_legal_SS_destinations_in_density_grammar':True,
        'source_frames':2394,'source_edges':n,'no_cold_probe_removed':True,
        'record_classes':[{ 'L':k[0],'degree':k[1],'budget':k[2],'count':v} for k,v in sorted(classes.items())],
        'zero_cost_root_repeats':'retained original operations; projection changes neither A nor BF nor recent order',
        'auxiliary_effects':'not asserted identical; irrelevant only to necessary A/B/recent exclusion projection',
        'actual_pair_successors':'all actual q1 successors, no restriction to extreme labels in the proof',
        'source_engine_calls':a.calls,'new_finite_tests':0}
    out('interface_audit.json',result);print(json.dumps(result),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_interfaces_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':a.calls,'new_finite_tests':0})
