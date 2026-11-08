"""Complete native10 primitive cache, reusing every audited LOW row.
Other off-path-leaf cases lift native9; only512 new Hamiltonian leaves
call the original source engine, and are charged as actual queries.
"""
import json,time,sys,hashlib,importlib.util
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent.parent;CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();queries=0
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,separators=(',',':'))
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def main():
    global queries
    ten=json.loads((B/'ten_anchor_LOW_source_schemas.json').read_text());old=json.loads((B/'nine_label_native_action_cache.json').read_text());T=list(map(fr,ten['trees']));OT=list(map(fr,old['trees']));index={t:i for i,t in enumerate(T)};oi={t:i for i,t in enumerate(OT)};D=[];Q=[];fresh=[];lifted=0
    sp=importlib.util.spec_from_file_location('native10_fresh_Hamiltonian33',P/'SE03_STEP2_COLD_NEG2_01/source_model.py');S=importlib.util.module_from_spec(sp);sp.loader.exec_module(S);p0=S.path
    def path(t,x):
        global queries
        if queries>=QCAP or time.process_time()-START>CAP-2:raise TimeoutError('SOURCE_CAP')
        queries+=1;return p0(t,x)
    S.path=path
    for a,t in enumerate(T):
        dep={};leaves=[]
        def walk(v,d):
            if isinstance(v,str):return
            k,l,r=v;dep[k]=d
            if isinstance(l,str) and isinstance(r,str):leaves.append(k)
            walk(l,d+1);walk(r,d+1)
        walk(t,0);dd=[];qq=[]
        for x in range(1,11):
            q=dep[x]//2;qq.append(q);h=ten['H'][a][x-1]
            if h<=2:dd.append(ten['LOW_destination'][a][x-1]);continue
            choices=[z for z in leaves if z!=x]
            if not choices:
                dst,pa,ev=S.trace(t,x);assert len(pa)==9 and len(ev)==5 and q==4;target=index[dst];fresh.append([a,x,target,q]);dd.append(target);continue
            z=min(choices);keys=[k for k in range(1,11) if k!=z];rank={v:i+1 for i,v in enumerate(keys)}
            def small(v,upper=9):
                if isinstance(v,str) or v[0]==z:return 'F'+str(upper)
                k,l,r=v;k=rank[k];return k,small(l,k-1),small(r,upper)
            s=oi[small(t)];rx=rank[x];assert old['H'][s][rx-1]==h and old['Q'][s][rx-1]==q
            def big(v):
                if isinstance(v,str):
                    gap=int(v[1:]);lo=keys[gap-1] if gap else 0;hi=keys[gap] if gap<9 else 11
                    return (z,'F'+str(z-1),'F'+str(z)) if lo<z<hi else 'F'+str(lo)
                k,l,r=v;return keys[k-1],big(l),big(r)
            dd.append(index[big(OT[old['destination'][s][rx-1]])]);lifted+=1
        D.append(dd);Q.append(qq)
    def reflection(v):return 'F'+str(10-int(v[1:])) if isinstance(v,str) else (11-v[0],reflection(v[2]),reflection(v[1]))
    mirror=[index[reflection(t)] for t in T];assert queries==len(fresh)==512
    result={'status':'COMPLETE_NATIVE10_SOURCE_ACTIONS','trees':T,'H':ten['H'],'Q':Q,'destination':D,'mirror':mirror,'fresh_source_rows':fresh,'new_source_queries':queries,'reused_LOW_schema_rows':ten['reused_free_gap_schema_instantiations'],'reused_root_identities':len(T),'reused_HIGH_free_gap_instances':lifted,'reused_LOW_sha256':hashlib.sha256((B/'ten_anchor_LOW_source_schemas.json').read_bytes()).hexdigest(),'native9_source_sha256':hashlib.sha256((B/'nine_label_native_action_cache.json').read_bytes()).hexdigest(),'principal_U33':'OPEN'}
    out('native10_source_actions.json',result);print(json.dumps({k:result[k] for k in ('status','new_source_queries','reused_HIGH_free_gap_instances')}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_core9_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':queries})
