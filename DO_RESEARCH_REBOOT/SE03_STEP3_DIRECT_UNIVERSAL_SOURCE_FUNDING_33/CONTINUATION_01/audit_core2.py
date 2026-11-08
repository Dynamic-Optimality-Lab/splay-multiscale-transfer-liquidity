"""Complete nine-label ordinary actions, reusing accepted source rows.
This supplies exact native transitions for source-normal-form investigation,
not a finite-population proof of universal funding.
"""
import json,time,sys,functools,importlib.util,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent.parent;CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();queries=0
def rd(p):return json.loads(p.read_text())
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def out(n,v):
    with (B/n).open('x') as f:json.dump(v,f,indent=2)
def main():
    global queries
    @functools.lru_cache(None)
    def trees(lo,hi):
        return ('F'+str(hi),) if lo>hi else tuple((k,l,r) for k in range(lo,hi+1) for l in trees(lo,k-1) for r in trees(k+1,hi))
    T=trees(1,9);assert len(T)==4862;index={t:i for i,t in enumerate(T)};known={};pins={}
    for p in sorted((P/'SE03_STEP2_UNARY_A_LIFT_14').glob('branch_core9_mask*.json')):
        z=rd(p);tt=list(map(fr,z['BF_trees']));mapped=[index[t] for t in tt]
        for s,t,x,q in z['BF_relation']:
            key=(mapped[s],x);value=(mapped[t],q)
            assert key not in known or known[key]==value;known[key]=value
        pins[p.name]=hashlib.sha256(p.read_bytes()).hexdigest()
    reused=len(known);identities=0
    for s,t in enumerate(T):
        k=(s,t[0]);assert k not in known or known[k]==(s,0)
        if k not in known:identities+=1;known[k]=(s,0)
    sp=importlib.util.spec_from_file_location('native_nine33',P/'SE03_STEP2_COLD_NEG2_01/source_model.py');S=importlib.util.module_from_spec(sp);sp.loader.exec_module(S);path0=S.path
    def path(t,x):
        global queries
        if queries>=QCAP or time.process_time()-START>CAP-3:raise TimeoutError('NINE_CACHE_RESERVE')
        queries+=1;return path0(t,x)
    S.path=path
    fresh=[]
    for s,t in enumerate(T):
        for x in range(1,10):
            if (s,x) not in known:
                dst,pa,ev=S.trace(t,x);known[s,x]=(index[dst],len(pa)//2);fresh.append([s,x,index[dst],len(pa)//2])
    # Static syntax depth annotation uses no new original source operation.
    dst=[];hh=[];qq=[]
    for s,t in enumerate(T):
        depth={}
        def walk(v,d):
            if isinstance(v,str):return
            depth[v[0]]=d;walk(v[1],d+1);walk(v[2],d+1)
        walk(t,0);ds=[];hs=[];qs=[]
        for x in range(1,10):
            dest,q=known[s,x];assert q==depth[x]//2
            ds.append(dest);hs.append((depth[x]+1)//2);qs.append(q)
        dst.append(ds);hh.append(hs);qq.append(qs)
    assert len(known)==4862*9
    out('nine_label_native_action_cache.json',{'status':'COMPLETE_EXACT_NINE_LABEL_ACTIONS','trees':T,'destination':dst,'H':hh,'Q':qq,
        'reused_accepted_genuine_rows':reused,'source_identity_rows':identities,'new_source_rows':fresh,'new_source_queries':queries,
        'reused_certificate_sha256':pins,'claim':'exact action cache only; no all-r proof or negative source cycle inferred'})
    print(json.dumps({'status':'COMPLETE_EXACT_NINE_LABEL_ACTIONS','trees':len(T),'reused':reused,'identity':identities,'new_source_queries':queries}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_core2_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':queries})
