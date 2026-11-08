"""Independent original-event-cost graded check; capped resumable intervals."""
import hashlib,json,pickle,sys,time
from pathlib import Path
import numpy as np
F=Path(__file__).resolve().parent;P=F.parents[1]
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time();PHASE=sys.argv[3];BATCH=int(sys.argv[4])
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    m=read(F/'active_a10_model.json');native=read(B/'native10_source_actions.json')
    assert m['native_cache_sha256']==sha(B/'native10_source_actions.json')
    assert m['A_destination']==native['destination'] and m['A_H']==native['H']
    assert m['A_roots']==[t[0] for t in native['trees']] and len(m['A_roots'])==16796
    for p,h in m['input_sha256'].items():assert sha(F/p)==h
    ba=read(F/'full_B_actions.json');va=read(F/'independent_full_B_actions_audit.json')
    assert va['input_sha256']['full_B_actions.json']==sha(F/'full_B_actions.json')
    expected={(s,row['destination'],2*j+1,row['q']) for s,rows in enumerate(ba['actions']) for j,row in enumerate(rows) if row['admissible'] and s!=row['destination']}
    assert expected=={(e['source'],e['target'],e['key'],e['q']) for e in m['B_edges']}
    path=None
    for p in sorted(F.glob('active_a10_[0-9][0-9].json')):
        if read(p)['status']=='COMPLETE':path=p.with_suffix('.pkl')
    assert path is not None
    with path.open('rb') as f:z=pickle.load(f)
    assert z['status']=='COMPLETE' and not z['pending'] and z['cycle'] is None and z['model_sha256']==sha(F/'active_a10_model.json')
    if BATCH>1:
        prev=read(F/f'independent_active_a10_part{BATCH-1:02d}.json')
        assert prev['status']=='CHECKPOINT' and prev['input_sha256'][path.name]==sha(path)
        start=prev['next_B_column'];checks=prev['endpoint_inequalities']
    else:start=0;checks=0
    ids={id(row):row for row in z['level']};cells=sum(map(len,ids.values()))
    assert cells+16796+3876+len(z['parent'])<2000000
    K=max(v for row in ids.values() for v in row.values());C=(K+7)//2
    roots=np.array(m['A_roots']);mr=m['mark_ranks'];classes=[np.flatnonzero(roots==mr[(r-1)//2]) for r in m['B_roots']]
    for b,row in enumerate(z['level']):
        assert all(roots[a]==mr[(m['B_roots'][b]-1)//2] and 0<v<=K for a,v in row.items())
    ah=np.array(m['A_H']);ad=np.array(m['A_destination']);groups={}
    for h in range(1,C):
        a,k=np.nonzero(ah==h);groups[h]=(a,ad[a,k])
    by=[[] for _ in range(m['B_count'])]
    for e in m['B_edges']:by[e['source']].append((e['target'],e['q']))
    end=start
    for b in range(start,3876):
        aa=classes[b];dp=[np.full(16796,-1000000,dtype=np.int32) for _ in range(C)]
        dp[0][aa]=[z['level'][b].get(int(a),0) for a in aa]
        for c in range(1,C):
            for h in range(1,c+1):
                src,dst=groups[h];np.maximum.at(dp[c],dst,dp[c-h][src]-2*h)
        best=np.maximum.reduce(dp)
        for bt,q in by[b]:
            ta=classes[bt];lv=np.array([z['level'][bt].get(int(a),0) for a in ta]);margin=lv-best[ta]-q
            assert margin.min()>=0,(b,bt,int(margin.min()));checks+=len(ta)
        end=b+1
        if time.process_time()-START>CAP-4:break
    assert K==4 and C==5 and K+2*C==14
    r={'status':'PASS' if end==3876 else 'CHECKPOINT','checked_B_interval':[start,end],'next_B_column':end,
       'endpoint_inequalities':checks,'D_width':K,'natural_c_cap':C,'Bank25_working_bound':14,
       'A_all_shapes':16796,'B_all_maximal_states':3876,'B_all_admissible_genuine_edges':13184,
       'unique_live_profile_cells':cells,'actual_source_state_identifications':0,
       'source_queries':0,'source_engine_calls':0,'JR35':'OPEN',
       'scope':'seven marks, B core13, A anonymous ranks 2,4,6 and reflection, arbitrary finite helpers and rigid private BSTs',
       'verification':'independent total-event-cost graded paths; producer uses packed path-length and shared profiles; same agent, not external/formal review',
       'input_sha256':{'active_a10_model.json':sha(F/'active_a10_model.json'),path.name:sha(path),
        'independent_full_B_actions_audit.json':sha(F/'independent_full_B_actions_audit.json')}}
    with (F/f'independent_active_a10_part{BATCH:02d}.json').open('x',encoding='utf-8') as f:json.dump(r,f,indent=2)
    print(json.dumps({k:v for k,v in r.items() if k!='input_sha256'}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/f'audit_{PHASE}_exit.json').open('x',encoding='utf-8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
