"""Close the strongest currently refuted censored-profile class, k=2."""
import json,time,hashlib
from pathlib import Path
from source_edge_resolver import Resolver
from certified_source_composer import Composer
B=Path(__file__).resolve().parent
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    import numpy as np
    k=2;graph=np.load(B/'root_clipped2_deficit_profile_graph.npz');sol=json.loads((B/'root_clipped2_deficit_profile_result_01.json').read_text());cycle=sol['cycle_edges'];assert cycle and sol['cycle_weight']<0;resolver=Resolver();composer=Composer();records=[];price=0
    def profile(a,b):return [max(q-2*h,-k) for h,q in zip(composer.H[a],composer.Q[b])]
    def code(root,p):return 10*sum((v+k)*(k+3)**i for i,v in enumerate(p))+root-1
    for i,e in enumerate(cycle):
        origin=int(graph['source_records'][e,0]);r=resolver.resolve(origin);assert r['kind']!='corpus';s=composer.compile(r['A'],r['B'],r['DELETE_helper_or_0'],r['KEEP_target']);assert (s['H'],s['Q'])==(r['H'],r['Q']) and 2*s['A']>=s['QF'];ps=profile(r['A'],r['B']);pt=profile(r['A_after'],r['B_after']);gs=composer.root[r['A']];gt=composer.root[r['A_after']];assert code(gs,ps)==int(graph['keys'][graph['src'][e],0]) and code(gt,pt)==int(graph['keys'][graph['dst'][e],0]);assert int(graph['dst'][e])==int(graph['src'][cycle[(i+1)%len(cycle)]]);price+=r['price'];records.append({'projected_edge':e,'source':r,'root_before':gs,'root_after':gt,'capped_profile_before':ps,'capped_profile_after':pt,'closed_history':s})
    assert price==-2;out('root_clipped2_source_countercertificate.json',{'status':'SOURCE_REALIZED_ROOT_CAPPED_DEFICIT_K2_REFUTATION_CANDIDATE','negative_cutoff':k,'cycle_price':price,'cycle_edges':records,'scope':'ANY fixed F(shared current marked root,ordered max(delta_i,-2)) at native-ten support; any c_e<=H_e on these unchanged natural packets','all_smaller_cutoffs_implied':'clip at-k for k=0,1 is a function of the k=2 profile','not_an_actual_full_state_cycle':True,'no_Coarse_Double_counterexample':True,'new_source_queries':0,'principal_U33':'OPEN','independent_audit':'PENDING','input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('root_clipped2_deficit_profile_graph.npz','root_clipped2_deficit_profile_result_01.json','certified_source_composer.py','native10_source_independent_audit.json')}});print(json.dumps({'status':'ROOT_CAPPED_K2_SOURCE_CYCLE_COMPOSED','distinct_histories':len(records),'cycle_price':price,'terminal_A_zero_cases':sum(r['source']['DELETE_helper_or_0']==r['source']['KEEP_target'] for r in records)}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof76_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
