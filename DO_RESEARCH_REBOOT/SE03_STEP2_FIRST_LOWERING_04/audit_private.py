"""Bounded actual A preparation search, including a private key outside the B core."""
import collections,functools,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;OLD=B.parent/'SE03_STEP2_COLD_NEG2_01'
sys.path.insert(0,str(OLD))
from source_model import trace,vine
account={'source_engine_calls':0,'new_finite_tests':0};start=time.process_time();CAP=min(40,float(sys.argv[1])-3)
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
class Bound(Exception):pass
@functools.lru_cache(maxsize=100000)
def move(t,x):
    account['source_engine_calls']+=1
    if account['source_engine_calls']%128==0:
        if time.process_time()-start>=CAP or account['source_engine_calls']>=700000:raise Bound()
    return trace(t,x)
def target(a):
    if a[0]!=1:return False
    for x in (11,1,3,5):
        a,p,e=move(a,x)
        if len(e)!=1:return False
    return True
def main():
    initial=vine(12);todo=collections.deque([initial]);parents={initial:None};found=None;popped=0;reason='EXHAUSTED_FINITE_PREPARATION_FAMILY'
    try:
        while todo:
            a=todo.popleft();popped+=1
            if target(a):
                word=[];t=a
                while parents[t] is not None:t,x=parents[t];word.append(x)
                found={'preparation':word[::-1],'source_A':a,'subsequent_actual_targets':[11,1,3,5]};reason='CANDIDATE_FOUND';break
            for x in (12,1,3,5,11,7,9,2,4,6,8,10):
                n=move(a,x)[0]
                if n in parents:continue
                if len(parents)>=50000:raise Bound()
                parents[n]=(a,x);todo.append(n)
    except Bound:reason='PREDECLARED_FINITE_LIMIT'
    out('private_preparation.json',{'status':reason,'candidate':found,'initial':initial,'states':len(parents),
        'popped':popped,'remaining_queue':len(todo),'new_present_private_key':12,'genuine_KEEP_support':[1,3,5,7,9,11],
        'scope':'actual preparation states only; entry candidate requires full-source costs/coldness/closure audit',**account})
    print(json.dumps({'status':reason,'preparation':None if found is None else found['preparation'],
        'states':len(parents),'popped':popped,**account}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_private_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,**account})
