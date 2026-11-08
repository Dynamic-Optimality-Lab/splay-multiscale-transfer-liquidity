"""Check exact shallow-profile dependence; no source operation invoked."""
import json,time,sys,collections
from pathlib import Path
B=Path(__file__).resolve().parent;CAP=float(sys.argv[1]);START=time.process_time()
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def main():
    cache=json.loads((B/'nine_label_native_action_cache.json').read_text());cert=json.loads((B/'native9_sparse_debt_certificate.json').read_text());T=list(map(fr,cache['trees']));N=len(T);mirror=cert['mirror'];levels=dict(cert['nonzero_debt']);result=[]
    def d(a,b):return levels.get(min(a*N+b,mirror[a]*N+mirror[b]),0)
    def shadow(t,depth):
        if isinstance(t,str):return None
        return (t[0],) if depth==0 else (t[0],shadow(t[1],depth-1),shadow(t[2],depth-1))
    for depth in (1,2):
        groups=collections.defaultdict(list);sig=[]
        for i,t in enumerate(T):v=shadow(t,depth);sig.append(v);groups[v].append(i)
        checks=0;failure=None
        for code,val in levels.items():
            a,b=divmod(code,N)
            for other in groups[sig[a]]:
                checks+=1
                if d(other,b)!=val:failure={'B':b,'A':a,'other_A':other,'debt':val,'other_debt':d(other,b),'signature':sig[a]};break
            if failure:break
            if time.process_time()-START>CAP-2:raise TimeoutError('PROFILE_CAP')
        result.append({'depth':depth,'profile_count':len(groups),'status':'PROFILE_SUFFICIENT_ON_NATIVE9' if failure is None else 'PROFILE_NOT_SUFFICIENT','checks':checks,'failure':failure})
    out('native9_shallow_dependence.json',{'result':result,'source_queries':0,'principal_U33':'OPEN','not_claimed':'no arbitrary private A lift or all-r formula'})
    print(json.dumps({'result':[{k:r[k] for k in ('depth','status','checks')} for r in result]}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof16_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
