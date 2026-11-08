"""Convert the existing source prefix to exact sparse/regenerating storage."""
import json,pickle,sys,time
from pathlib import Path
from interior_projection_source_tools import known,isnode
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def pre(t):return () if not isnode(t) else (t[0],)+pre(t[1])+pre(t[2])
def main():
    N=16796
    with (B/'full_geometry_compressed_work_08.pkl').open('rb') as f:w=pickle.load(f)
    bypi={};aliases=0
    for a,pi in w['projections'].items():
        if len(pi)==1:continue
        if pi in bypi:assert pre(w['A'][bypi[pi]])==pre(w['A'][a]);aliases+=1
        else:bypi[pi]=a
    code=[bypi[pi]*N+b for b,pi in w['features']];assert len(set(code))==len(code)
    lower={c:d for c,d in zip(code,w['lower']) if d>0};pred={c:j for c,j in zip(code,w['pred']) if c in lower}
    updates=[]
    for r in w['updates']:
        updates.append({**r,'source_code':None if r['source_feature'] is None else code[r['source_feature']],'target_code':code[r['target_feature']]})
    # Source enumeration/group order is identical to the old generator.
    Z=json.loads((B/'native10_source_actions.json').read_text());groups={k:[] for k in range(1,11)}
    for b,t in enumerate(Z['trees']):groups[t[0]].append(b)
    rank={b:i for bb in groups.values() for i,b in enumerate(bb)};apos,bpos,xpos=w['cursor'];pending=[]
    assert not w['pending'] and w['counter'] is None
    for c in lower:
        a,b=divmod(c,N)
        if a>apos or a==apos and rank[b]>=bpos:pending.append(c)
    sparse={'private':w['private'],'N':N,'A':w['A'],'A_index':w['A_index'],'actions':w['actions'],'actions2':w['actions2'],'projections':w['projections'],'initial_H1_complete_A_count':w['initial_H1_complete_A_count'],'cursor':w['cursor'],'source_couplings':w['source_couplings'],'reused_unary_endpoint_packets':w['reused_unary_endpoint_packets'],'lower':lower,'pred':pred,'updates':updates,'pending':pending,'counter':None,'causal_edges':[],'width3_first_candidate':w['width3_first_candidate'],'conversion_source':'full_geometry_compressed_work_08.pkl','old_mutable_features':len(w['features']),'old_edges':len(w['edges']),'old_positive_labels':len(lower),'profile_geometry_aliases':aliases,'source_generation_complete':False}
    assert time.process_time()-START<CAP-5
    with (B/'full_geometry_sparse_work_00.pkl').open('xb') as f:pickle.dump(sparse,f,protocol=5)
    out('full_geometry_sparse_conversion.json',{'status':'PRODUCER_EXACT_SPARSE_CONVERSION_PENDING_INDEPENDENT_AUDIT','old_mutable_profiles':len(code),'retained_positive_labels':len(lower),'old_stored_edges':len(w['edges']),'stored_edges_now':0,'retained_causal_records':len(updates),'cursor':w['cursor'],'known_A_shapes':len(w['A']),'pending_new_source_rows':len(pending),'profile_geometry_aliases':aliases,'source_couplings_reused':w['source_couplings'],'all_old_values_preserved_including_implicit_zero':True,'outgoing_inequalities':'same original source kernel/action grammar; must be regenerated on every future rise','source_queries':0,'source_engine_calls':0,'principal_U33':'OPEN'})
    print(json.dumps({k:v for k,v in json.loads((B/'full_geometry_sparse_conversion.json').read_text()).items() if k!='outgoing_inequalities'}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof143_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
