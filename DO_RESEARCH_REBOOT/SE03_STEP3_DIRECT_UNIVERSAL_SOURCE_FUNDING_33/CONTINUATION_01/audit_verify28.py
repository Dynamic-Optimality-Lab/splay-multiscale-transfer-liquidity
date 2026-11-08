"""Independent composition audit using already certified primitive identities.
No previous ordinary-splay primitive audit is repeated; this is proof reuse.
"""
import json,time,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    path=B/'diagonal_zero_dual_closed_source_compositions.json';z=json.loads(path.read_text());assert z['status']=='COMPLETE_CLOSED_SOURCE_COMPOSITION_AUDIT_PENDING' and z['completed']==z['required']==136;assert all(hashlib.sha256((B/n).read_bytes()).hexdigest()==v for n,v in z['input_sha256'].items());old=json.loads((B/'native10_source_independent_audit.json').read_text());native=json.loads((B/'native10_source_actions.json').read_text());assert hashlib.sha256((B/'native10_source_actions.json').read_bytes()).hexdigest()==old['input_sha256'] and old['status']=='PASS_COMPLETE_NATIVE10_SOURCE_ACTIONS';T=native['trees'];D=native['destination'];H=native['H'];Q=native['Q'];algebra=json.loads((B/'diagonal_zero_dual_independent_algebra_audit.json').read_text());assert algebra['status']=='PASS_EXACT_DUAL_AND_ORIGINAL_PRIMITIVE_INSTANCES_CLOSED_EMBEDDINGS_PENDING';actual=already=lookups=0;CDmargins=[];sources=[]
    for item in z['records']:
        if item.get('reused_existing_closed_source'):
            assert item['kind']=='already_closed_source_corpus';already+=1;continue
        word=item['word'];bpre=item['initial_diagonal_index'];state=[bpre]*3;lru=[];elru=[];rows={r[0]:r for r in item['rows']};start_chart=None;start_tree=None;seen=[]
        for copy in range(item['u']+item['L']):
            for local,(mode,x) in enumerate(word,1):
                t=copy*len(word)+local
                if t==item['period'][0]:start_chart=(lru[:],elru[:]);start_tree=state[:]
                before=state[:];state[0]=D[state[0]][x-1];h=H[before[0]][x-1];q=qe=0;lookups+=1
                if mode=='K':
                    state[1]=D[state[1]][x-1];q=Q[before[1]][x-1];lookups+=1
                    if x in lru:lru.remove(x)
                    lru.insert(0,x)
                    if x!=10:
                        state[2]=D[state[2]][x-1];qe=Q[before[2]][x-1];lookups+=1
                        if x in elru:elru.remove(x)
                        elru.insert(0,x)
                if t in rows:
                    row=[t,mode,x]+before+state[:]+[h,q,qe];assert row==rows[t];seen.append(t)
        assert seen==list(rows) and state==start_tree and (lru,elru)==start_chart;genuine={r[2] for r in item['rows'] if r[1]=='K' and T[r[4]][0]!=r[2]};assert genuine==set(range(1,11));occ=item['selected_natural_occurrence'];hit=rows[occ];prev=rows[occ-1];assert prev[1]=='K' and T[prev[4]][0]!=prev[2] and hit[1]=='K' and T[hit[4]][0]!=hit[2];assert hit[3]==item['source']['a'] and hit[4]==item['source']['b'] and hit[2]==item['source']['target'] and (hit[9],hit[10])==(item['H'],item['Q']);assert T[hit[3]][0]==T[hit[4]][0];margin=2*sum(r[9] for r in item['rows'])-sum(r[10] for r in item['rows']);assert margin>=0;CDmargins.append(margin);actual+=1;sources.append({'edge':item['edge'],'period':item['period'],'selected_natural_occurrence':occ,'H':item['H'],'Q':item['Q'],'CD_margin':margin})
    assert actual==133 and already==3 and algebra['support']==136 and algebra['all135_weighted_feature_changes_zero'] and algebra['positive_weights_sum_one'];out('diagonal_zero_quadratic_family_independent_refutation.json',{'status':'PASS_SOURCE_EXACT_DIAGONAL_ZERO_QUADRATIC_FAMILY_REFUTATION','scope':'ALL real linear/quadratic coefficients on the15 specified diagonal-zero comparisons at native-ten support, on every genuine natural packet; not other invariants or regrouping','new_closed_source_compositions_checked':actual,'existing_accepted_closed_sources_reused':already,'total_dual_packets':136,'exact_weighted_price':algebra['weighted_price'],'all_source_periods_and_actual_recent_charts_closed':True,'all_ten_keys_genuinely_KEEP':True,'all_new_periods_CD_safe':True,'primitive_identity_instantiations_checked':lookups,'new_source_engine_calls':0,'new_source_queries':0,'verification_method':'independent word/absolute-ID/chart/cost composition checker over immutable previously independently verified complete source primitive identities; no new ordinary-splay kernel run claimed','principal_U33':'OPEN','external_or_formal_verification':False,'new_source_inventory':sources,'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('diagonal_zero_dual_closed_source_compositions.json','diagonal_zero_dual_independent_algebra_audit.json','diagonal_zero_quadratic_exact_dual.json','native10_source_independent_audit.json','native10_source_actions.json')}});print(json.dumps({'status':'PASS_SOURCE_EXACT_QUADRATIC_COMPARISON_FAMILY_REFUTATION','new_closed_histories':actual,'accepted_histories_reused':already,'primitive_instances_checked':lookups,'new_source_queries':0,'principal_U33':'OPEN'}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify28_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
