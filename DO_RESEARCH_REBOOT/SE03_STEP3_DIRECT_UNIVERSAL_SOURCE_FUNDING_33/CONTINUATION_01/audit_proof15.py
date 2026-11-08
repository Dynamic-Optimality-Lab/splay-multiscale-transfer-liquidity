"""Publish sparse source certificate and a source-exact unary repair map.
No accepted artifact is overwritten. All actual donor identities are explicit.
"""
import json,pickle,time,sys,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    with (B/'sparse_nine_01.pkl').open('rb') as f:s=pickle.load(f)
    assert not s['queue'] and max(s['level'].values())==2
    out('native9_sparse_debt_certificate.json',{'status':'PRODUCER_COMPLETE_NATIVE_NINE_ANCHOR_SOURCE_CERTIFICATE','number_of_anchors':9,'native_tree_count':4862,'code':'A_tree_index*4862+B_tree_index; choose minimum of code and reflected code','mirror':s['mirror'],'nonzero_debt':sorted(s['level'].items()),'all_other_coefficients':0,'width':2,'LOW':'H1 andH2 exact ordinary macro syntax','HIGH':'H>=3, all synchronized destination A trees, margin by width2 and Q<=4','c':'min(H,3) actual prefix events','working_bank_bound':8,'source_cache_sha256':hashlib.sha256((B/'nine_label_native_action_cache.json').read_bytes()).hexdigest(),'scope':'a FIXED ordered set of9 possible A operands, every KEEP within it, arbitrary unaccessed ordered gap BSTs','arbitrary_anonymous_A_operands':False,'principal_U33':'OPEN'})
    physical=json.loads((B/'unary_projection_source_countercertificate.json').read_text());cache=json.loads((B/'nine_label_native_action_cache.json').read_text())
    def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
    T=list(map(fr,cache['trees']));idx={v:i for i,v in enumerate(T)}
    src=idx[fr(physical['projected_A_before'])];a=b=src
    native=[('D',3),('D',1),('D',4),('K',3),('K',1),('D',2),('D',1),('D',4),('D',3),('D',2),('D',1)]
    native += [('K',x) for x in list(range(2,10))+list(range(8,0,-1))]
    refs=[1,3,4,4,5,6,7,8,8,9,10]+list(range(11,27));rows=[];pairmap={};demmap={};gadget=[[(1,1)],[(3,1)],[(4,1),(4,2)],[(2,1)],[(5,1)],[(6,1)],[(7,1)],[(8,1),(8,2)],[(6,2)],[(9,1)],[(10,1)]]
    for nt,((mode,x),pt) in enumerate(zip(native,refs),1):
        before=(a,b);aa=cache['H'][a][x-1];a=cache['destination'][a][x-1];q=0
        if mode=='K':q=cache['Q'][b][x-1];b=cache['destination'][b][x-1]
        events=gadget[nt-1] if nt<=11 else [(pt,j) for j in range(1,aa+1)];assert len(events)==aa
        for j,ev in enumerate(events,1):
            for bit in (0,1):pairmap[(nt,j,bit)]=ev+(bit,)
        for k in range(1,q+1):demmap[nt,k]=(pt,k)
        rows.append({'occurrence':nt,'mode':mode,'target':x,'physical_boundary_reference':pt,'before_indices':before,'after_indices':(a,b),'a':aa,'q':q})
    assert a==b==src and sum(r['a'] for r in rows)==29
    U={(r['occurrence'],j,v) for r in physical['rows'] for j in range(1,r['a']+1) for v in (0,1)};V={(r['occurrence'],j,v) for r in rows for j in range(1,r['a']+1) for v in (0,1)}
    assert set(pairmap)==V and len(set(pairmap.values()))==len(V) and set(pairmap.values())<=U
    assert U-set(pairmap.values())=={(9,2,0),(9,2,1)}
    # Both native and physical full natural h0 only have two actual demands.
    native_h0={(4,1):(1,1,0),(5,1):(5,1,0)};physical_h0={(4,1):(1,1,0),(5,1):(5,1,0)}
    assert all(pairmap[u]==physical_h0[demmap[d]] for d,u in native_h0.items())
    out('unary_projection_physical_repair_map.json',{'status':'PRODUCER_COMPLETE_UNIFORM_FAMILY_REPAIR','native_initial':T[src],'native_word':native,'native_rows':rows,'bit_map':[{'native':v,'physical':u} for v,u in sorted(pairmap.items())],'demand_map':[{'native':d,'physical':p} for d,p in sorted(demmap.items())],'unused_original_bits':sorted(U-set(pairmap.values())),'native_A':29,'original_A':30,'same_B_demands':2,'original_h0_preserved':True,'repair_reservations':[{'event':(2,1),'used_at_native_occurrence':4},{'event':(6,2),'used_at_native_occurrence':9}],'additional_held_bits':2,'scope':'uniform right-vine/one-anonymous-key returning family, arbitrary disjoint finite repetitions and reflected gap substitutions','general_lift':False,'principal_U33':'OPEN'})
    print(json.dumps({'status':'TWO_PRODUCER_CERTIFICATES_EXPORTED','native9_coefficients':len(s['level']),'width':2,'native9_working_bound':8,'repair_native_A':29,'repair_original_A':30,'all_original_h0_preserved':True}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof15_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
