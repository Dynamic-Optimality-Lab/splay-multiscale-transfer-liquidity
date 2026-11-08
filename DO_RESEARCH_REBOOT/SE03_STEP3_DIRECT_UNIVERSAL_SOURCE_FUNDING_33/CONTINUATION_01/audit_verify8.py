"""Independent symbolic LOW lift using largest off-path leaf.
No producer lift function and no new splay engine are called.
"""
import json,time,sys,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;CAP=float(sys.argv[1]);START=time.process_time()
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    old=json.loads((B/'nine_label_native_action_cache.json').read_text());new=json.loads((B/'ten_anchor_LOW_source_schemas.json').read_text());assert json.loads((B/'native9_sparse_independent_audit.json').read_text())['status']=='PASS_COMPLETE_NINE_ANCHOR_SOURCE_CERTIFICATE'
    oldT=list(map(fr,old['trees']));ni={t:i for i,t in enumerate(oldT)};T=list(map(fr,new['trees']));idx={t:i for i,t in enumerate(T)};assert len(idx)==16796
    catalan=[1]
    for n in range(1,11):catalan.append(sum(catalan[k]*catalan[n-1-k] for k in range(n)))
    assert len(T)==catalan[10];checks=0
    def valid(t,lo,hi,d,dep,leaves):
        if lo>hi:assert t=='F'+str(hi);return
        k,l,r=t;assert lo<=k<=hi;dep[k]=d
        if isinstance(l,str) and isinstance(r,str):leaves.append(k)
        valid(l,lo,k-1,d+1,dep,leaves);valid(r,k+1,hi,d+1,dep,leaves)
    for i,t in enumerate(T):
        dep={};leaves=[];valid(t,1,10,0,dep,leaves)
        for x in range(1,11):
            h=(dep[x]+1)//2;assert new['H'][i][x-1]==h
            if h==0:assert new['LOW_destination'][i][x-1]==i;continue
            if h>2:assert new['LOW_destination'][i][x-1]==-1;continue
            z=max(v for v in leaves if v!=x);keep=[v for v in range(1,11) if v!=z];rank={v:j+1 for j,v in enumerate(keep)}
            def smaller(v,upper=9):
                if isinstance(v,str) or v[0]==z:return 'F'+str(upper)
                k,l,r=v;k=rank[k];return k,smaller(l,k-1),smaller(r,upper)
            s=ni[smaller(t)];rx=rank[x];assert old['H'][s][rx-1]==h
            payload={}
            for gap in range(10):
                lower=keep[gap-1] if gap else 0;upper=keep[gap] if gap<9 else 11
                payload['F'+str(gap)]=(z,'F'+str(z-1),'F'+str(z)) if lower<z<upper else 'F'+str(lower)
            def bigger(v):return payload[v] if isinstance(v,str) else (keep[v[0]-1],bigger(v[1]),bigger(v[2]))
            expected=bigger(oldT[old['destination'][s][rx-1]]);assert idx[expected]==new['LOW_destination'][i][x-1];checks+=1
        if i%512==0 and time.process_time()-START>CAP-2:raise TimeoutError('INDEPENDENT_SCHEMA_CAP')
    assert checks==new['reused_free_gap_schema_instantiations']==107484
    result={'status':'PASS_COMPLETE_TEN_ANCHOR_LOW_SCHEMA_LIFT','complete_native_shapes':16796,'LOW_schema_instantiations':checks,'distinct_leaf_choice':'producer smallest, checker largest non-target leaf','new_source_queries':0,'new_source_engine_calls':0,'proof_basis':'certified nine-anchor primitives with arbitrary rigid free payloads; off-path substitution commutes with every frame','fresh_semantic_replay_claimed':False,'external_or_formal_verification':False,'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('ten_anchor_LOW_source_schemas.json','OFF_PATH_LEAF_SOURCE_LIFT.md','nine_label_native_action_cache.json')},'principal_U33':'OPEN'}
    out('ten_anchor_schema_independent_audit.json',result);print(json.dumps(result))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify8_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
