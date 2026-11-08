"""Bounded DELETE preparation for a singleton NEG2 and one +1 entry."""
import collections,functools,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;OLD=B.parent/'SE03_STEP2_COLD_NEG2_01'
sys.path.insert(0,str(OLD))
from source_model import trace,vine
account={'source_engine_calls':0,'new_finite_tests':0};started=time.process_time();CAP=min(30,float(sys.argv[1])-3)
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
class Bound(Exception):pass
@functools.lru_cache(maxsize=100000)
def move(t,x):
    account['source_engine_calls']+=1
    if account['source_engine_calls']%128==0:
        if time.process_time()-started>=CAP or account['source_engine_calls']>=500000:raise Bound()
    return trace(t,x)
def goal(a):
    if a[0]!=1:return False
    for x in (7,9,1):
        a,p,e=move(a,x)
        if len(e)!=1:return False
    return True
def main():
    R=vine(11);todo=collections.deque([R]);parent={R:None};found=None;why='FINITE_FAMILY_EXHAUSTED';popped=0
    try:
        while todo:
            a=todo.popleft();popped+=1
            if goal(a):
                w=[];u=a
                while parent[u] is not None:u,x=parent[u];w.append(x)
                found={'preparation':w[::-1],'source_A':a,'negative_target':7,'positive_one_target':9,'lowering_target':1}
                why='CANDIDATE_FOUND';break
            for x in (8,10,1,9,7,3,5,11,2,4,6):
                n=move(a,x)[0]
                if n in parent:continue
                if len(parent)>=40000:raise Bound()
                parent[n]=(a,x);todo.append(n)
    except Bound:why='PREDECLARED_LIMIT'
    out('e1_preparation.json',{'status':why,'candidate':found,'states':len(parent),'popped':popped,
        'initial_A':R,'source_closed_embedding_still_required':True,**account})
    print(json.dumps({'status':why,'preparation':None if found is None else found['preparation'],
        'states':len(parent),'popped':popped,**account}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_e1prep_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,**account})
