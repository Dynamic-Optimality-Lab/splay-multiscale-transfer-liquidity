"""Independent exhaustive low-cost path inequalities, not producer's heap.

Native/B source actions have prior independent source receipts. This verifies
all natural helpers using a bounded Bellman proof plus the range bound.
"""
import functools,hashlib,json,pickle,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1]
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time();PHASE=sys.argv[3];GAP=int(sys.argv[4])
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tup(t):return None if t is None else (t[0],tup(t[1]),tup(t[2]))
def main():
    m=read(F/'active_a8_model.json');native=read(B/'native10_source_actions.json')
    assert sha(B/'native10_source_actions.json')==m['native_cache_sha256']
    for p,h in m['input_sha256'].items():assert sha(F/p)==h
    ba=read(F/'full_B_actions.json');va=read(F/'independent_full_B_actions_audit.json')
    assert va['input_sha256']['full_B_actions.json']==sha(F/'full_B_actions.json')
    @functools.lru_cache(None)
    def cat(lo,hi):
        if lo>hi:return (None,)
        return tuple((k,l,r) for k in range(lo,hi+1) for l in cat(lo,k-1) for r in cat(k+1,hi))
    assert len(m['A_trees'])==1430 and set(map(tup,m['A_trees']))==set(cat(1,8))
    ids=m['A_native10_indices'];loc={v:i for i,v in enumerate(ids)}
    for a,orig in enumerate(ids):
        for k in range(8):
            assert m['A_destination'][a][k]==loc[native['destination'][orig][k]]
            assert m['A_H'][a][k]==native['H'][orig][k]
    expected={(s,row['destination'],2*j+1,row['q']) for s,rows in enumerate(ba['actions']) for j,row in enumerate(rows) if row['admissible'] and s!=row['destination']}
    assert expected=={(e['source'],e['target'],e['key'],e['q']) for e in m['B_edges']}
    receipt=None;path=None
    for p in sorted(F.glob(f'active_a8_g{GAP}_*.json')):
        r=read(p)
        if r['status']=='COMPLETE':receipt=r;path=p.with_suffix('.pkl')
    assert receipt is not None and receipt['model_sha256']==sha(F/'active_a8_model.json')
    with path.open('rb') as f:z=pickle.load(f)
    assert z['status']=='COMPLETE' and not z['pending'] and z['cycle'] is None
    import numpy as np
    level=np.frombuffer(z['levels'],dtype=np.int32);K=int(level.max());C=(K+7)//2;L=C-1
    mr=[j+1+(j>=GAP) for j in range(7)]
    classes=[np.flatnonzero(np.array(m['A_roots'])==mr[(r-1)//2]) for r in m['B_roots']]
    offsets=[0]
    for c in classes:offsets.append(offsets[-1]+len(c))
    assert offsets==z['offsets'] and offsets[-1]==len(level) and len(level)+1430+3876<2000000
    dest=np.array(m['A_destination'],dtype=np.int64).ravel();cost=2*np.array(m['A_H'],dtype=np.int32)
    by=[[] for _ in range(m['B_count'])]
    for e in m['B_edges']:by[e['source']].append((e['target'],e['q']))
    checks=0;minimum=1000
    for b,aa in enumerate(classes):
        best=np.full(1430,-1000000,dtype=np.int32);best[aa]=level[offsets[b]:offsets[b+1]]
        for _ in range(L):
            prev=best.copy();candidates=(prev[:,None]-cost).ravel()
            np.maximum.at(best,dest,candidates)
        for bt,q in by[b]:
            margin=level[offsets[bt]:offsets[bt+1]]-best[classes[bt]]-q
            mn=int(margin.min());assert mn>=0,(GAP,b,bt,q,mn)
            minimum=min(minimum,mn);checks+=len(margin)
        if b%100==0:assert time.process_time()-START<CAP-2
    assert 2*C-6-K>=0 and K+2*C<=25
    # Low-cost macros H<C have at most C-1 positive operations; repeated
    # root identities do not change their endpoint or cost. Bellman includes
    # all these words. High-H macros use only range, so all lengths covered.
    report={'status':'PASS_UNBOUNDED_HELPER_SOURCE_CREDIT_CLASS','gap':GAP,'reflection_gap':7-GAP,
      'synchronized_states':len(level),'all_B_states':3876,'all_B_genuine_edges':len(m['B_edges']),
      'all_A_shapes':1430,'D_width':K,'natural_c_cap':C,'Bank25_working_bound':K+2*C,
      'low_cost_Bellman_layers':L,'endpoint_inequalities':checks,'minimum_margin':minimum,
      'source_queries':0,'source_engine_calls':0,'helper_length':'arbitrary finite',
      'source_scope':'seven genuine marks, maximal B core13, at most one anonymous A operand over the period; specified helper order and reflection, arbitrary rigid private populations',
      'JR35':'OPEN','universal_all_supports':False,
      'verification':'independent Bellman-layer check, distinct from heap producer; accepted independently checked source-action caches; same agent, not external/formal review',
      'input_sha256':{'active_a8_model.json':sha(F/'active_a8_model.json'),path.name:sha(path),
        'independent_full_B_actions_audit.json':sha(F/'independent_full_B_actions_audit.json')}}
    with (F/f'independent_active_a8_g{GAP}.json').open('x',encoding='utf-8') as f:json.dump(report,f,indent=2)
    print(json.dumps({k:v for k,v in report.items() if k!='input_sha256'}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/f'audit_{PHASE}_exit.json').open('x',encoding='utf-8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
