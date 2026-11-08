"""Actual B prefix from the diagonal right vine for the selected falsifier word."""
import collections,hashlib,json,pickle,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;B=F.parents[1]/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    p=F/'eight_core_B_source_01.pkl'
    with p.open('rb') as f:z=pickle.load(f)
    c=F/'eight_core_B_cycles.json';cycle=json.loads(c.read_text())['cycles'][0];trees=z['trees'];edges=z['rows'];idx={t:i for i,t in enumerate(trees)}
    vine=None
    for k in range(15,0,-1):vine=(k,None,vine)
    root=idx[vine];target=cycle['edges'][0][0];out=[[] for _ in trees]
    for j,e in enumerate(edges):out[e[0]].append(j)
    pred={root:None};todo=collections.deque([root])
    while todo:
        a=todo.popleft()
        for j in out[a]:
            b=edges[j][1]
            if b not in pred:pred[b]=j;todo.append(b)
    path=[];v=target
    if target in pred:
        while pred[v] is not None:
            j=pred[v];path.append(j);v=edges[j][0]
        path=path[::-1]
        state=root
        for j in path:assert edges[j][0]==state;state=edges[j][1]
        assert state==target
    result={'status':'PRODUCER_ACTUAL_SOURCE_REACH_PREFIX' if target in pred else 'SELECTED_INITIAL_B_REACHABILITY_NOT_ESTABLISHED',
      'right_vine_state':root,'cycle_initial_B_state':target,'reachable_states':len(pred),'static_states':len(trees),
      'prefix_edge_ids':path,'prefix_edges':[edges[j] for j in path],
      'source_bridge':'Start A=BF=BE at right vine15; prefix literal all KEEP, so A=BF after it; then canonical actual A-only Gamma to any tested full A source. True paired closure of a positive cycle still required.',
      'source_queries':0,'source_engine_calls':0,'JR35':'OPEN','independent_replay_pending_for_any_root_candidate':True,
      'input_sha256':{str(p):sha(p),str(c):sha(c),str(F/'derive_eight_core_source_reach_prefix.py'):sha(F/'derive_eight_core_source_reach_prefix.py')}}
    with (F/'eight_core_B_source_reach_prefix.json').open('x',encoding='utf8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k not in ('prefix_edges','input_sha256')}),flush=True)
    assert target in pred and time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_proof295_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
