"""Certified free-payload instantiation, not a new splay-engine oracle.
All LOW source actions are instances of already audited primitive schemas.
"""
import json,time,sys,functools,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;CAP=float(sys.argv[1]);START=time.process_time()
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def main():
    old=json.loads((B/'nine_label_native_action_cache.json').read_text());nine=list(map(fr,old['trees']));ni={t:i for i,t in enumerate(nine)}
    assert json.loads((B/'native9_sparse_independent_audit.json').read_text())['status']=='PASS_COMPLETE_NINE_ANCHOR_SOURCE_CERTIFICATE'
    @functools.lru_cache(None)
    def grammar(lo,hi):return ('F'+str(hi),) if lo>hi else tuple((k,l,r) for k in range(lo,hi+1) for l in grammar(lo,k-1) for r in grammar(k+1,hi))
    T=grammar(1,10);assert len(T)==16796;index={t:i for i,t in enumerate(T)};H=[];dest=[];lifts=identities=0
    for i,t in enumerate(T):
        depth={};leaves=[]
        def walk(v,d):
            if isinstance(v,str):return
            k,l,r=v;depth[k]=d
            if isinstance(l,str) and isinstance(r,str):leaves.append(k)
            walk(l,d+1);walk(r,d+1)
        walk(t,0);hh=[];dd=[]
        for x in range(1,11):
            h=(depth[x]+1)//2;hh.append(h)
            if h==0:dd.append(i);identities+=1;continue
            if h>2:dd.append(-1);continue
            leaf=min(z for z in leaves if z!=x);keys=[k for k in range(1,11) if k!=leaf];rank={k:j+1 for j,k in enumerate(keys)}
            def reduce(v,lo=1,hi=9):
                if isinstance(v,str) or v[0]==leaf:return 'F'+str(hi)
                k,l,r=v;k=rank[k];return k,reduce(l,lo,k-1),reduce(r,k+1,hi)
            reduced=reduce(t);s=ni[reduced];rx=rank[x];assert old['H'][s][rx-1]==h
            dst=nine[old['destination'][s][rx-1]]
            def inflate(v):
                if isinstance(v,str):
                    gap=int(v[1:]);before=0 if gap==0 else keys[gap-1];after=11 if gap==9 else keys[gap]
                    return (leaf,'F'+str(leaf-1),'F'+str(leaf)) if before<leaf<after else 'F'+str(before)
                k,l,r=v;return keys[k-1],inflate(l),inflate(r)
            target=inflate(dst);dd.append(index[target]);lifts+=1
        H.append(hh);dest.append(dd)
        if i%256==0 and time.process_time()-START>CAP-2:raise TimeoutError('SCHEMA_LIFT_CAP')
    result={'status':'COMPLETE_TEN_ANCHOR_LOW_SOURCE_SCHEMAS','trees':T,'H':H,'LOW_destination':dest,'source_queries':0,'source_engine_calls':0,'reused_free_gap_schema_instantiations':lifts,'root_identities':identities,'fresh_source_semantic_replay':False,'source_base_sha256':hashlib.sha256((B/'nine_label_native_action_cache.json').read_bytes()).hexdigest(),'source_proof':'OFF_PATH_LEAF_SOURCE_LIFT.md','scope':'all ten-anchor primitives with H<=2; HIGH destination intentionally unspecified','principal_U33':'OPEN'}
    out('ten_anchor_LOW_source_schemas.json',result);print(json.dumps({k:result[k] for k in ('status','reused_free_gap_schema_instantiations','root_identities','source_queries')}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof17_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
