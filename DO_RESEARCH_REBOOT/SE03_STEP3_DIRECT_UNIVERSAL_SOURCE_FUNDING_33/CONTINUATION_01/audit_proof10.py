"""Prepare a state-defined native9 debt candidate from complete implicit
source graph. No universal/support/private-A lifting is presumed."""
import json,pickle,time,sys,collections
from pathlib import Path
B=Path(__file__).resolve().parent;CAP=float(sys.argv[1]);START=time.process_time()
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    z=json.loads((B/'nine_label_native_action_cache.json').read_text());N=len(z['trees']);D=z['destination'];T=z['trees']
    with (B/'pair9_reflect_03.pkl').open('rb') as f:s=pickle.load(f)
    assert not s['queue'];a,b=divmod(s['nodes'][0],N);assert a==b;single={a};todo=collections.deque([a])
    while todo:
        v=todo.popleft()
        for t in D[v]:
            if t not in single:single.add(t);todo.append(t)
    roots=collections.Counter(T[v][0] for v in single);product=sum(v*v for v in roots.values());mirror=s['mirror'];fixed=sum(1 for a in single for b in single if T[a][0]==T[b][0] and mirror[a]==a and mirror[b]==b)
    upper=(product+fixed)//2;assert upper>=len(s['nodes'])
    # Only canonical pair states are retained; old shortest-path labels and
    # reaching trees remain immutable in the original checkpoint.
    state={'nodes':s['nodes'],'index':s['index'],'mirror':mirror,'debt':bytearray(len(s['nodes'])),'queue':collections.deque(range(len(s['nodes']))),'inside':bytearray([1])*len(s['nodes']),'parent':[-1]*len(s['nodes']),'parent_op':[None]*len(s['nodes']),'checks':0,'updates':0,'single':single,'native_product_closed':upper==len(s['nodes'])}
    with (B/'pair9_debt_00.pkl').open('xb') as f:pickle.dump(state,f,pickle.HIGHEST_PROTOCOL)
    result={'status':'NATIVE_NINE_DEBT_CANDIDATE_PREPARED','single_tree_reachable':len(single),'single_root_counts':dict(roots),'synchronized_pair_product_mod_reflection':upper,'source_graph_nodes':len(s['nodes']),'native_product_closed':state['native_product_closed'],'source_queries':0,'principal_U33':'OPEN','not_claimed':'no arbitrary support or anonymous A ancestor lifting'}
    out('pair9_native_product.json',result);print(json.dumps(result))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof10_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
