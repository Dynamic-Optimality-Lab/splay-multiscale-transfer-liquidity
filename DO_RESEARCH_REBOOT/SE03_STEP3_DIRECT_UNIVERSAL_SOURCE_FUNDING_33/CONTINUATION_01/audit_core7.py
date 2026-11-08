"""Adversarial original-source test of unary projection of the NEW debt.
Starts from actual common states, prepares A by two actual DELETEs, creates
a genuine KEEP boundary, then tries a true H2 packet. Only this candidate
lift is tested; no CD or all-r claim follows from finite passing controls.
"""
import json,time,sys,importlib.util,collections
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent.parent;CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();queries=0
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def main():
    global queries
    c=json.loads((B/'nine_label_native_action_cache.json').read_text());cert=json.loads((B/'native9_sparse_debt_certificate.json').read_text());T=list(map(fr,c['trees']));N=len(T);idx={t:i for i,t in enumerate(T)};mirror=cert['mirror'];level=dict(cert['nonzero_debt']);marks=[1,2]+list(range(4,11));inv={x:i+1 for i,x in enumerate(marks)}
    sp=importlib.util.spec_from_file_location('original_debt_lift33',P/'SE03_STEP2_COLD_NEG2_01/source_model.py');S=importlib.util.module_from_spec(sp);sp.loader.exec_module(S);p0=S.path
    def path(t,x):
        global queries
        if queries>=QCAP or time.process_time()-START>CAP-2:raise TimeoutError('SOURCE_CAP')
        queries+=1;return p0(t,x)
    S.path=path
    def debt(a,b):return level.get(min(a*N+b,mirror[a]*N+mirror[b]),0)
    def physical(t):
        if isinstance(t,str):
            i=int(t[1:]);return (3,'F2','F3') if i==2 else 'F'+str(i if i<2 else i+1)
        return marks[t[0]-1],physical(t[1]),physical(t[2])
    def project(t):
        def prune(v):
            if isinstance(v,str):return None
            k,l,r=v;l=prune(l);r=prune(r)
            if k==3:
                if l is not None and r is not None:raise ValueError('anonymous brancher')
                return l if r is None else r
            return inv[k],l,r
        def gaps(v,lo=1,hi=9):
            if v is None:return 'F'+str(hi)
            k,l,r=v;return k,gaps(l,lo,k-1),gaps(r,k+1,hi)
        return idx[gaps(prune(t))]
    hit=None;trials=0;undefined=0;candidate_sources=0
    for bpre,t in enumerate(T):
        if queries>=min(25000,QCAP-2000) or time.process_time()-START>CAP-5:break
        base=physical(t);ad,_,_=S.trace(base,3)
        for g in (1,9):
            if g==t[0]:continue
            a,_,_=S.trace(ad,marks[g-1]);b=c['destination'][bpre][g-1]
            try:ap=project(a)
            except ValueError:undefined+=1;continue
            ds=debt(ap,b)
            if ds==0:continue
            candidate_sources+=1;depth={};anc={}
            def walk(v,d,p):
                if isinstance(v,str):return
                k,l,r=v;depth[k]=d;anc[k]=p;walk(l,d+1,p+[k]);walk(r,d+1,p+[k])
            walk(a,0,[])
            for x in range(1,10):
                q=c['Q'][b][x-1];px=marks[x-1]
                if x==g or ds<=4-q or depth[px] not in (3,4) or 3 not in anc[px]:continue
                at,pa,ev=S.trace(a,px);assert len(ev)==2;bt=c['destination'][b][x-1];trials+=1
                try:apt=project(at)
                except ValueError:undefined+=1;continue
                dt=debt(apt,bt);margin=4-q+dt-ds
                if margin<0:hit={'bpre':bpre,'g':g,'x':x,'ds':ds,'dt':dt,'Q':q,'margin':margin,'before_A':a,'after_A':at,'before_A_projection':ap,'after_A_projection':apt,'before_B':b,'after_B':bt};break
            if hit:break
        if hit:break
    witness=None
    if hit:
        r9=next(i for i,t in enumerate(T) if t==S.vine(9))
        def bfs(s,t):
            parent={s:None};queue=collections.deque([s])
            while queue and t not in parent:
                v=queue.popleft()
                for x in range(9):
                    u=c['destination'][v][x]
                    if u not in parent:parent[u]=(v,x+1);queue.append(u)
            assert t in parent;word=[];v=t
            while v!=s:v,x=parent[v];word.append(x)
            return list(reversed(word))
        toR=bfs(hit['after_B'],r9);toBase=bfs(r9,hit['bpre']);tour=list(range(2,10))+list(range(8,0,-1));reset=list(range(1,11))+list(range(9,0,-1))
        word=[('D',3),('D',marks[hit['g']-1]),('K',marks[hit['g']-1]),('K',marks[hit['x']-1])]+[('K',marks[x-1]) for x in toR+tour+toBase]+[('D',x) for x in reset+[4,2,1]]+[('D',marks[x-1]) for x in toBase]
        initial=physical(T[hit['bpre']]);a=b=initial;rows=[]
        for k,(mode,x) in enumerate(word,1):
            before=(a,b);a,pa,ea=S.trace(a,x);pb='';eb=[]
            if mode=='K':b,pb,eb=S.trace(b,x)
            rows.append({'occurrence':k,'mode':mode,'target':x,'before':before,'after':(a,b),'A_path':pa,'BF_path':pb,'A_events':ea,'BF_events':eb,'a':len(ea),'qF':len(pb)//2,'genuine_F':mode=='K' and before[1][0]!=x})
        assert a==b==initial and rows[2]['genuine_F'] and rows[3]['genuine_F'] and rows[3]['a']==2 and rows[3]['qF']==hit['Q']
        assert {r['target'] for r in rows if r['genuine_F']}==set(marks)
        assert project(rows[3]['before'][0])==hit['before_A_projection'] and project(rows[3]['after'][0])==hit['after_A_projection']
        witness={'status':'SOURCE_EXACT_PROJECTED_NATIVE9_DEBT_REFUTED','initial_diagonal':initial,'word':word,'rows':rows,'marks':marks,'critical_occurrence':4,'critical_preceding_genuine_boundary':3,'H':2,'Q':hit['Q'],'D_source':hit['ds'],'D_target':hit['dt'],'signed_margin':hit['margin'],'details':hit,'source_period':[1,len(word)],'actual_A':sum(r['a'] for r in rows),'actual_Q':sum(r['qF'] for r in rows),'paired_closed':True,'refuted_claim':'new sparse native9 debt lifts by unary suppression of an active anonymous A ancestor','original_native9_certificate_invalidated':False,'actual_CD_refutation':False,'principal_U33':'OPEN'}
        assert 2*witness['actual_A']>=witness['actual_Q']
        out('native9_unary_debt_lift_countercertificate.json',witness)
    result={'status':witness['status'] if witness else 'NO_FAILURE_IN_BOUNDED_EXTREME_ROOT_CONTROLS','source_queries':queries,'actual_H2_trials':trials,'positive_debt_sources':candidate_sources,'undefined_branching_projections':undefined,'source_models_examined_through_B_index':bpre,'principal_U33':'OPEN','positive_universal_claim':False}
    out('native9_unary_debt_lift_search.json',result);print(json.dumps(result))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_core7_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':queries})
