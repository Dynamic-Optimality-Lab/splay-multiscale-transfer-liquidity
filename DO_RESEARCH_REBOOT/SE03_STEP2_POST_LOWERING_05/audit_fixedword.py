"""Bounded joint A feasibility for a fixed source-exact complete-return candidate."""
import collections,functools,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;OLD=B.parent/'SE03_STEP2_COLD_NEG2_01'
sys.path.insert(0,str(OLD))
from source_model import trace,vine,replay,charts,core,labels
started=time.process_time();CAP=min(30,float(sys.argv[1])-3)
account={'source_engine_calls':0,'new_finite_tests':0};targets=(7,1,3,5,1,11)
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
class Bound(Exception):pass
@functools.lru_cache(maxsize=100000)
def move(t,x):
    account['source_engine_calls']+=1
    if account['source_engine_calls']%128==0:
        if time.process_time()-started>=CAP or account['source_engine_calls']>=500000:raise Bound()
    return trace(t,x)
def good(a):
    if a[0]!=1:return False
    for x in targets:
        a,p,e=move(a,x)
        if len(e)!=1:return False
    return True
def main():
    R=vine(11);todo=collections.deque([R]);parent={R:None};found=None;why='FINITE_PREPARATION_FAMILY_EXHAUSTED';popped=0
    try:
        while todo:
            a=todo.popleft();popped+=1
            if good(a):
                w=[];u=a
                while parent[u] is not None:u,x=parent[u];w.append(x)
                found={'preparation':w[::-1],'source_A':a};why='SOURCE_A_CANDIDATE_FOUND';break
            for x in (10,1,7,9,11,3,5,2,4,6,8):
                n=move(a,x)[0]
                if n in parent:continue
                if len(parent)>=40000:raise Bound()
                parent[n]=(a,x);todo.append(n)
    except Bound:why='PREDECLARED_FINITE_LIMIT'
    # Exact physical BF word is checked even when A preparation is absent.
    warm=[9,1,3,5,3,1,11,1,3,5,9,11,9,5,3,1];b=R;bdata=[]
    for x in warm:b=move(b,x)[0]
    for x in targets:
        old=b;b,p,e=move(b,x);bdata.append({'key':x,'before':old,'after':b,'path':p,'Q':len(e)})
    assert [r['Q'] for r in bdata]==[4,1,2,2,2,4]
    assert all(all(q['kind']=='DOUBLE' and q['case'] in ('LL','RR') for q in move(r['before'],r['key'])[2]) for r in bdata)
    out('fixedword_search.json',{'status':why,'candidate':found,'initial_A':R,'source_root':1,
        'target_word':targets,'desired_A_events':[1]*6,'B_source_warmup':warm,'B_rows':bdata,
        'states':len(parent),'popped':popped,'remaining_queue':len(todo),
        'finite_scope':'actual eleven-key DELETE preparations; no arbitrary-inventory exclusion from this search',**account})
    print(json.dumps({'status':why,'preparation':None if found is None else found['preparation'],
        'states':len(parent),'popped':popped,'B_Q':[r['Q'] for r in bdata],**account}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_fixedword_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,**account})
