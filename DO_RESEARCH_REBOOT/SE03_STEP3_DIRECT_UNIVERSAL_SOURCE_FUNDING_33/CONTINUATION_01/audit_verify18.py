"""Full check of the UNCHANGED checkpoint coefficients. Never fixes a debt.
Passing would establish feasibility despite an unfinished producer worklist;
failure records the first exact certificate obligation still violated.
"""
import json,pickle,time,sys,hashlib,collections
from pathlib import Path
B=Path(__file__).resolve().parent;CAP=float(sys.argv[1]);START=time.process_time()
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    source=B/'native10_source_actions.json';Z=json.loads(source.read_text());receipt=json.loads((B/'native10_source_independent_audit.json').read_text());assert receipt['status']=='PASS_COMPLETE_NATIVE10_SOURCE_ACTIONS' and hashlib.sha256(source.read_bytes()).hexdigest()==receipt['input_sha256']
    T=Z['trees'];N=len(T);D=Z['destination'];H=Z['H'];Q=Z['Q'];mirror=Z['mirror'];payload=B/'native10_debt_03.pkl';pin=hashlib.sha256(payload.read_bytes()).hexdigest()
    with payload.open('rb') as f:old=pickle.load(f)
    L=old['level'];producer_pending=len(old['queue']);del old
    assert len(L)<1850000 and max(L.values())==3 and min(L.values())>=1
    def canon(a,b):return min(a*N+b,mirror[a]*N+mirror[b])
    def debt(a,b):return L.get(canon(a,b),0)
    cheap=collections.defaultdict(list);helper=[];direct=[];terminal=[];rootcounts=collections.Counter(t[0] for t in T)
    for a,t in enumerate(T):
        helper.append([(y,D[a][y]) for y in range(10) if H[a][y]==1]);direct.append([(x,D[a][x],H[a][x]) for x in range(10) if 1<=H[a][x]<=2]);terminal.append([(x,D[a][x]) for x in range(10) if H[a][x]==1])
        for x in range(10):
            if H[a][x]==1:cheap[t[0],x].append(a)
    for code,v in L.items():a,b=divmod(code,N);assert 0<=a<N and T[a][0]==T[b][0] and code==canon(a,b)
    negative=positive=0;failure=None
    for b,t in enumerate(T):
        for x in range(10):
            q=Q[b][x]
            if q<3:continue
            for a in cheap[t[0],x]:
                at=D[a][x];bt=D[b][x];ds=debt(a,b);dt=debt(at,bt);margin=2-q+dt-ds;negative+=1
                if margin<0:failure={'kind':'ACTUAL_H1','A':a,'B':b,'target':x+1,'after_A':at,'after_B':bt,'H':1,'Q':q,'D_source':ds,'D_target':dt,'margin':margin};break
            if failure:break
        if failure:break
    if failure is None:
        for j,(code,val) in enumerate(L.items()):
            a,b=divmod(code,N);root=T[b][0]-1
            for x,at,h in direct[a]:
                if x==root:continue
                bt=D[b][x];dt=debt(at,bt);m=2*h-Q[b][x]+dt-val;positive+=1
                if m<0:failure={'kind':'ACTUAL_DIRECT_LOW','A':a,'B':b,'target':x+1,'after_A':at,'after_B':bt,'H':h,'Q':Q[b][x],'D_source':val,'D_target':dt,'margin':m};break
            if failure:break
            for y,at in helper[a]:
                for x,att in terminal[at]:
                    if x==root:continue
                    bt=D[b][x];dt=debt(att,bt);m=4-Q[b][x]+dt-val;positive+=1
                    if m<0:failure={'kind':'ACTUAL_TWO_EVENT','A':a,'B':b,'helper':y+1,'target':x+1,'after_A':att,'after_B':bt,'H':2,'Q':Q[b][x],'D_source':val,'D_target':dt,'margin':m};break
                if failure:break
            if failure:break
            if j%65536==0 and time.process_time()-START>CAP-4:raise TimeoutError('AUDIT_CAP')
    highchecks=0
    if failure is None:
        histogram=[collections.Counter() for _ in T]
        for code,v in L.items():
            a,b=divmod(code,N);assert mirror[b]!=b;histogram[b][v]+=1;histogram[mirror[b]][v]+=1
        maxi=[max(v,default=0) for v in histogram];mini=[min(v) if sum(v.values())==rootcounts[T[b][0]] else 0 for b,v in enumerate(histogram)]
        for b,t in enumerate(T):
            for x in range(10):
                if x==t[0]-1:continue
                bt=D[b][x];margin=6-Q[b][x]+mini[bt]-maxi[b];highchecks+=1
                if margin<0:failure={'kind':'HIGH_ANY_ENDPOINT_CERTIFICATE_OBLIGATION','B':b,'target':x+1,'after_B':bt,'source_max_D':maxi[b],'target_min_D':mini[bt],'price':6-Q[b][x],'margin':margin};break
            if failure:break
    result={'status':'CHECKPOINT_COEFFICIENTS_FAIL_COMPLETE_CERTIFICATE_CHECK' if failure else 'PASS_COMPLETE_NATIVE10_SOURCE_CREDIT_CERTIFICATE','input_checkpoint':'native10_debt_03.pkl','input_sha256':pin,'input_coefficients':len(L),'producer_pending_queue':producer_pending,'coefficients_mutated':False,'independent_solver_or_repair_run':False,'negative_LOW_checked':negative,'positive_source_LOW_checked':positive,'HIGH_envelope_checks':highchecks,'first_failure':failure,'new_source_queries':0,'source_engine_calls':0,'width':3,'working_bank_bound_if_complete':9,'scope':'fixed ten-anchor source backbones and rigid private gaps; not arbitrary support','principal_U33':'OPEN','external_or_formal_verification':False}
    out('native10_complete_independent_audit.json',result);print(json.dumps(result))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify18_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})

