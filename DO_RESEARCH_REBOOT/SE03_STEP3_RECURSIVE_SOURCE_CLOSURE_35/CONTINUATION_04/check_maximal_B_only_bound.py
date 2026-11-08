"""Falsify/probe Q<=2 genuine macros using ALREADY certified actual B edges.

No new source execution. A negative result is a source-route obstruction,
never a CD counterexample: diagonal A=B pays H=Q on these even-depth rows.
"""
import hashlib,json,sys,time
from pathlib import Path
import numpy as np
F=Path(__file__).resolve().parent;B=F.parents[1]/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    p=F/'active_a10_model.json';m=json.loads(p.read_text());rows=m['B_edges'];N=m['B_count'];assert N==3876
    D=np.zeros(N,dtype=np.int32);parent={};witness=None;rounds=0
    def cycle(v):
        seen={};chain=[]
        while v in parent:
            if v in seen:
                ids=chain[seen[v]:];gain=sum(rows[j]['q']-2 for j in ids)
                if gain>0:
                    ids=ids[::-1];actual=[rows[j] for j in ids]
                    assert all(actual[i]['target']==actual[(i+1)%len(actual)]['source'] for i in range(len(actual)))
                    return {'B_edge_ids':ids,'B_edges':actual,'Q':sum(e['q'] for e in actual),'genuine_macros':len(actual),
                      'Q_minus_2_macros':gain,'keys_used':sorted({e['key'] for e in actual})}
                return None
            seen[v]=len(chain);j=parent[v];chain.append(j);v=rows[j]['source']
        return None
    while time.process_time()-START<CAP-3:
        changed=False
        for j,e in enumerate(rows):
            s,t,q=e['source'],e['target'],e['q'];v=int(D[s])+q-2
            if v>int(D[t]):
                D[t]=v;parent[t]=j;changed=True
                if int(D[t])>8:
                    witness=cycle(t)
                    if witness:break
        rounds+=1
        if witness or not changed:break
    out={'status':'B_ONLY_TWO_PER_MACRO_BOUND_REFUTED_ON_LITERAL_CYCLE' if witness else ('PASS_CACHED_MAX7_B_ONLY_SIGNS' if not changed else 'CHECKPOINT'),
      'rounds':rounds,'max_D':int(D.max()),'witness':witness,'source_queries':0,'source_engine_calls':0,'JR35':'OPEN',
      'diagonal_A_cost_if_replayed':'H=Q on each maximal-core same-side even-depth B edge; not a CD violation',
      'source_admissibility':'literal B cycle; verify actual genuine set and full core before universal maximal-core claim',
      'input_sha256':{str(p):sha(p)}}
    with (F/'maximal_B_only_bound_result.json').open('x',encoding='utf8') as f:json.dump(out,f,indent=2)
    print(json.dumps(out),flush=True);assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_proof287_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
