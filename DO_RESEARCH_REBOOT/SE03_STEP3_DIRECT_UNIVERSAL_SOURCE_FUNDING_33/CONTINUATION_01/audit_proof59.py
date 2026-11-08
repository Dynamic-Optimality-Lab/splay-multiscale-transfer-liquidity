import json,time,hashlib
from pathlib import Path
from certified_source_composer import Composer
from source_edge_resolver import Resolver
B=Path(__file__).resolve().parent
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    import numpy as np
    graph=np.load(B/'ordered_deficit_profile_graph.npz');sol=json.loads((B/'ordered_deficit_profile_result_01.json').read_text());cycle=sol['cycle_edges'];assert cycle and sol['cycle_weight']<0;resolver=Resolver();composer=Composer();records=[];sumw=0
    def profile(a,b):return [max(0,q-2*h) for h,q in zip(composer.H[a],composer.Q[b])]
    for i,e in enumerate(cycle):
        global_edge=int(graph['source_records'][e,0]);r=resolver.resolve(global_edge);assert r['kind']!='corpus';w=composer.compile(r['A'],r['B'],r['DELETE_helper_or_0'],r['KEEP_target']);assert (w['H'],w['Q'])==(r['H'],r['Q']) and 2*w['A']>=w['QF'];before=profile(r['A'],r['B']);after=profile(r['A_after'],r['B_after']);src=int(graph['keys'][graph['src'][e],0]);dst=int(graph['keys'][graph['dst'][e],0]);assert sum(v*3**k for k,v in enumerate(before))==src and sum(v*3**k for k,v in enumerate(after))==dst and r['price']==int(graph['w'][e]);records.append({'projected_cycle_edge':e,'source':r,'ordered_profile_before':before,'ordered_profile_after':after,'closed_history':w});sumw+=r['price'];assert int(graph['dst'][e])==int(graph['src'][cycle[(i+1)%len(cycle)]])
    assert sumw==-1;result={'status':'DEFICIT_PROFILE_CANDIDATE_SOURCE_COUNTERCERTIFICATES','anonymous_inventory_source':'positive_deficit_inventory_closed_source.json','ordered_profile_cycle':records,'cycle_price':sumw,'only_refuted_candidates':'ANY fixed debt determined solely by anonymous positive deficit inventory, or by its COMPLETE ordered per-mark positive profile','not_a_joined_actual_source_cycle':True,'not_a_CD_counterexample':True,'new_source_queries':0,'source_verification':'accepted primitive compositions; independent fresh source replay still pending','principal_U33':'OPEN','input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('positive_deficit_inventory_closed_source.json','ordered_deficit_profile_graph.npz','ordered_deficit_profile_result_01.json','native10_source_independent_audit.json','source_edge_resolver.py')}};out('deficit_profile_source_countercertificates.json',result);print(json.dumps({'status':result['status'],'ordered_cycle_edges':len(records),'price':sumw,'packets':[{'H':r['source']['H'],'Q':r['source']['Q'],'word_length':len(r['closed_history']['word']),'profile_before':r['ordered_profile_before'],'profile_after':r['ordered_profile_after']} for r in records]}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof59_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
