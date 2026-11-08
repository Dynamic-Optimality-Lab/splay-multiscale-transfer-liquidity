"""Independent event-cost-graded checker of all natural source paths."""
import functools,hashlib,json,pickle,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1]
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tup(t):return None if t is None else (t[0],tup(t[1]),tup(t[2]))
def main():
    m=read(F/'active_a9_model.json');native=read(B/'native10_source_actions.json')
    assert sha(B/'native10_source_actions.json')==m['native_cache_sha256']
    for p,h in m['input_sha256'].items():assert sha(F/p)==h
    @functools.lru_cache(None)
    def cat(lo,hi):
        if lo>hi:return (None,)
        return tuple((k,l,r) for k in range(lo,hi+1) for l in cat(lo,k-1) for r in cat(k+1,hi))
    assert len(m['A_trees'])==4862 and set(map(tup,m['A_trees']))==set(cat(1,9))
    ids=m['A_native10_indices'];loc={v:i for i,v in enumerate(ids)}
    for a,orig in enumerate(ids):
        for k in range(9):
            assert m['A_destination'][a][k]==loc[native['destination'][orig][k]]
            assert m['A_H'][a][k]==native['H'][orig][k]
    ba=read(F/'full_B_actions.json');va=read(F/'independent_full_B_actions_audit.json')
    assert va['input_sha256']['full_B_actions.json']==sha(F/'full_B_actions.json')
    expected={(s,row['destination'],2*j+1,row['q']) for s,rows in enumerate(ba['actions']) for j,row in enumerate(rows) if row['admissible'] and s!=row['destination']}
    assert expected=={(e['source'],e['target'],e['key'],e['q']) for e in m['B_edges']}
    with (F/'active_a9_02.pkl').open('rb') as f:z=pickle.load(f)
    assert z['status']=='COMPLETE' and not z['pending'] and z['cycle'] is None and z['model_sha256']==sha(F/'active_a9_model.json')
    import numpy as np
    K=max(v for d in z['level'] for v in d.values());C=(K+7)//2
    roots=np.array(m['A_roots']);mr=m['mark_ranks'];classes=[np.flatnonzero(roots==mr[(r-1)//2]) for r in m['B_roots']]
    ah=np.array(m['A_H']);ad=np.array(m['A_destination']);groups={}
    for h in range(1,C):
        a,k=np.nonzero(ah==h);groups[h]=(a,ad[a,k])
    by=[[] for _ in range(m['B_count'])]
    for e in m['B_edges']:by[e['source']].append((e['target'],e['q']))
    checks=0;mn=1000
    for b,aa in enumerate(classes):
        dp=[np.full(4862,-1000000,dtype=np.int32) for _ in range(C)]
        dp[0][aa]=[z['level'][b].get(int(a),0) for a in aa]
        for c in range(1,C):
            for h in range(1,c+1):
                src,dst=groups[h];np.maximum.at(dp[c],dst,dp[c-h][src]-2*h)
        best=np.maximum.reduce(dp)
        for bt,q in by[b]:
            ta=classes[bt];lv=np.array([z['level'][bt].get(int(a),0) for a in ta])
            margin=lv-best[ta]-q;v=int(margin.min());assert v>=0,(b,bt,v)
            mn=min(mn,v);checks+=len(ta)
        if b%100==0:assert time.process_time()-START<CAP-2
    assert K==4 and C==5 and K+2*C==14
    report={'status':'PASS_TWO_ANONYMOUS_EXACT_SOURCE_CLASS','mark_ranks':mr,'helper_ranks':[2,4],
      'A_all_shapes':4862,'B_all_maximal_core_states':3876,'B_all_admissible_genuine_edges':13184,
      'implicit_synchronized_domain':sum(map(len,classes)),'live_positive_potential_cells':z['nonzero_states'],
      'D_width':K,'natural_c_cap':C,'Bank25_working_bound':14,'endpoint_inequalities':checks,'minimum_margin':mn,
      'source_queries':0,'source_engine_calls':0,'source_lengths':'all finite, including arbitrary repeated/shared helpers',
      'scope':'r7 core13, two active anonymous A nodes at ranks 2 and 4 or reflected ranks; arbitrary rigid private BSTs',
      'JR35':'OPEN','all_two_anonymous_orders':False,'all_supports':False,
      'verification':'event-cost graded source paths, independent of heap and packed path-length producer; accepted source caches; same agent not external/formal review',
      'input_sha256':{'active_a9_model.json':sha(F/'active_a9_model.json'),'active_a9_02.pkl':sha(F/'active_a9_02.pkl'),
        'independent_full_B_actions_audit.json':sha(F/'independent_full_B_actions_audit.json')}}
    with (F/'independent_active_a9_audit.json').open('x',encoding='utf-8') as f:json.dump(report,f,indent=2)
    print(json.dumps({k:v for k,v in report.items() if k!='input_sha256'}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_verify102_exit.json').open('x',encoding='utf-8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
