"""Independent exact quadratic-dual audit; closed realization remains separate."""
import json,time,sys,hashlib,importlib.util,fractions
from pathlib import Path
B=Path(__file__).resolve().parent;F=fractions.Fraction
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    import numpy as np
    sp=importlib.util.spec_from_file_location('independent_dual_set_features33',B/'audit_verify23.py');M=importlib.util.module_from_spec(sp);sp.loader.exec_module(M);exact=json.loads((B/'diagonal_zero_quadratic_exact_dual.json').read_text());assert all(hashlib.sha256((B/n).read_bytes()).hexdigest()==v for n,v in exact['input_sha256'].items());native=json.loads((B/'native10_source_actions.json').read_text());trees=native['trees'];template=np.load(B/'nonlinear_feature_projected_graph.npz')['source_records'];vines=np.load(B/'diagonal_zero_vine_full_arrays.npz')['source_records'];spec=json.loads((B/'diagonal_zero_source_spec.json').read_text());src=json.loads((B/'uniform_feature_dual_source_certificate.json').read_text());histories=src['witnesses']+[json.loads((B/'native10_width2_source_countercertificate.json').read_text())];num=json.loads((B/'diagonal_zero_dual_numeric_checkpoint.json').read_text());weighted=[F(0)]*135;price=F(0);total=F(0);counts={'template':0,'already_closed_source_corpus':0,'complete_A_vine_adversary':0};audit_records=[]
    def compare(v):return [v[0]-v[1],v[2]-v[3],v[4]-v[5],v[6]-v[7],10-v[8],10-v[9],v[0]+v[1]+20-2*v[10],v[11],v[2]+v[3]-2*v[12],v[4]+v[5]-2*v[13],v[0]+v[1]+20-2*v[14],v[16],10-v[17],v[18],10-v[19]]
    def basis(A,B):
        v=compare(M.features(A,B));return v+[v[i]*v[j] for i in range(15) for j in range(i,15)]
    oldedges=spec['template_edges'];corpus=spec['accepted_actual_natural_packets_added']
    for i,(e,st) in enumerate(zip(exact['source_edge_ids'],exact['weights'])):
        weight=F(st);assert weight>0;total+=weight
        if oldedges<=e<oldedges+corpus:
            kind='already_closed_source_corpus';origin=spec['extra_source_origins'][e-oldedges];zs=histories[origin['source_number']];rm={r['occurrence']:r for r in zs['rows']};rr=[rm[t] for t in origin['occurrences']];before=fr(rr[0]['before'][:2]);after=fr(rr[-1]['after'][:2]);H=sum(r['a'] for r in rr);Q=sum(r['qF'] for r in rr);source={'origin':origin}
        else:
            kind='template' if e<oldedges else 'complete_A_vine_adversary';a,b,x=map(int,template[e] if e<oldedges else vines[e-oldedges-corpus]);assert trees[a][0]==trees[b][0]!=x;at=native['destination'][a][x-1];bt=native['destination'][b][x-1];before=fr((trees[a],trees[b]));after=fr((trees[at],trees[bt]));H=native['H'][a][x-1];Q=native['Q'][b][x-1];source={'a':a,'b':b,'target':x}
        counts[kind]+=1;bb=basis(*before);aa=basis(*after);delta=[a-b for a,b in zip(aa,bb)];assert delta==[num['exact_integer_equation_matrix'][k][i] for k in range(135)] and 2*H-Q==num['source_prices'][i];weighted=[v+weight*d for v,d in zip(weighted,delta)];price+=weight*(2*H-Q);audit_records.append({'edge':e,'kind':kind,'source':source,'H':H,'Q':Q})
    assert total==1 and not any(weighted) and price==F(exact['weighted_price'])<0
    out('diagonal_zero_dual_independent_algebra_audit.json',{'status':'PASS_EXACT_DUAL_AND_ORIGINAL_PRIMITIVE_INSTANCES_CLOSED_EMBEDDINGS_PENDING','support':len(exact['weights']),'source_categories':counts,'weighted_price':str(price),'all135_weighted_feature_changes_zero':True,'positive_weights_sum_one':True,'source_primitive_cache_reused_not_rerun':True,'new_source_queries':0,'full_original_paired_closed_embedding_for_new_selected_edges':'PENDING producer construction and independent composition audit','universal_family_refutation_promoted':False,'principal_U33':'OPEN','external_or_formal_verification':False,'source_inventory':audit_records,'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('diagonal_zero_quadratic_exact_dual.json','diagonal_zero_dual_numeric_checkpoint.json','native10_source_actions.json','native10_source_independent_audit.json','diagonal_zero_source_spec.json')}});print(json.dumps({'status':'PASS_EXACT_DUAL_SOURCE_PRIMITIVES_CLOSED_BRIDGE_PENDING','support':len(exact['weights']),'categories':counts,'new_source_queries':0}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify27_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
