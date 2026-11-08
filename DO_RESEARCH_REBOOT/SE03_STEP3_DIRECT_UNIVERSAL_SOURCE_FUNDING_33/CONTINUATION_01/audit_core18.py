"""Exact critical-quartet test for private-maximum pullback of native10 debt.
The generic source proof leaves ONLY zero-slack D3->D0 RR-even jumps.
"""
import json,time,sys,pickle,hashlib,importlib.util
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent.parent;START=time.process_time();CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);queries=0
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    global queries
    z=json.loads((B/'native10_source_actions.json').read_text());T=list(map(fr,z['trees']));N=len(T);idx={t:i for i,t in enumerate(T)};D=z['destination'];Q=z['Q'];mirror=z['mirror'];audit=json.loads((B/'native10_complete_independent_audit.json').read_text());raw=(B/'native10_debt_03.pkl').read_bytes();assert hashlib.sha256(raw).hexdigest()==audit['input_sha256'];saved=pickle.loads(raw);level=saved['level'];assert len(level)==1769616 and not saved['queue'];del raw,saved
    def debt(a,b):return level.get(min(a*N+b,mirror[a]*N+mirror[b]),0)
    IA={};IB={};projected={};Arows=0
    for a,t in enumerate(T):
        for x in range(1,11):
            v=t;path=''
            while v[0]!=x:
                side=1 if x<v[0] else 2;path+='L' if side==1 else 'R';v=v[side]
            if len(path) not in (2,4) or not path.startswith('RR'):continue
            at=D[a][x-1];xx,left,right=T[at];p,gg,C=left;g,A,BB=gg;assert xx==x and g==t[0] and p==t[2][0];pt=idx[(x,(g,A,(p,BB,C)),right)];projected[at]=pt;IA.setdefault(at,[]).append((a,len(path)//2,g));Arows+=1
    for b,t in enumerate(T):
        g=t[0]
        for x in range(g+1,11):
            q=Q[b][x-1]
            if q>=2:IB.setdefault((D[b][x-1],g),[]).append((b,q))
    target_states=examined=0;failure=None
    for code,value in level.items():
        if value!=3:continue
        at,bt=divmod(code,N)
        for aa,bb in {(at,bt),(mirror[at],mirror[bt])}:
            if aa not in IA:continue
            target_states+=1;pt=projected[aa]
            if debt(pt,bb)!=0:continue
            for a,h,g in IA[aa]:
                for b,q in IB.get((bb,g),[]):
                    expected=2*h-q+3
                    if not 0<=expected<=3:continue
                    ds=debt(a,b);examined+=1
                    if ds==expected:failure={'A_source':a,'B_source':b,'target':T[aa][0],'native_A_target':aa,'B_target':bb,'projected_actual_A_target':pt,'native_H':h,'Q':q,'D_source':ds,'D_native_target':3,'D_projected_target':0,'native_margin':0,'actual_H':h+1,'actual_margin':-1};break
                if failure:break
            if failure:break
        if failure:break
        if time.process_time()-START>CAP-3:raise TimeoutError('CRITICAL_QUARTET_CPU')
    result={'status':'PRIVATE_MAX_PULLBACK_CRITICAL_COUNTEREXAMPLE' if failure else 'COMPLETE_CRITICAL_QUARTET_ABSENCE_CERTIFICATE_CANDIDATE','critical_tuples':[[1,2,3,3,0],[1,3,2,3,0],[1,4,1,3,0],[2,4,3,3,0]],'A_RR_even_inverse_rows':Arows,'explicit_D3_target_instances_inspected':target_states,'source_pair_candidates_inspected':examined,'failure':failure,'new_source_queries':0,'principal_U33':'OPEN','only_candidate':'pullback D_new(A,B)=D10(pi_max(A),pi_max(B)); not arbitrary private-ancestor debt formulas'}
    if failure:
        a,b,x=(failure[k] for k in ('A_source','B_source','target'));g,L,R=T[a];As=(g,L,(11,R,'F11'))
        def embed(t):
            if isinstance(t,str):return (11,'F10','F11') if t=='F10' else t
            return t[0],embed(t[1]),embed(t[2])
        Bs=embed(T[b]);sp=importlib.util.spec_from_file_location('private_max_critical_actual33',P/'SE03_STEP2_COLD_NEG2_01/source_model.py');S=importlib.util.module_from_spec(sp);sp.loader.exec_module(S);p0=S.path
        def path(t,k):
            global queries
            if queries>=QCAP:raise TimeoutError('QUERY_CAP')
            queries+=1;return p0(t,k)
        S.path=path;At,pa,ea=S.trace(As,x);Bt,pb,eb=S.trace(Bs,x)
        def suppress(t):
            if isinstance(t,str):return t
            if t[0]==11:assert t[2]=='F11';return suppress(t[1])
            return t[0],suppress(t[1]),suppress(t[2])
        assert len(ea)==failure['actual_H'] and len(pb)//2==failure['Q'] and suppress(At)==T[failure['projected_actual_A_target']] and suppress(Bt)==T[failure['B_target']];assert 2*len(ea)-len(pb)//2+failure['D_projected_target']-failure['D_source']==-1;result.update(actual_A_before=As,actual_B_before=Bs,actual_A_after=At,actual_B_after=Bt,actual_A_path=pa,actual_B_path=pb,actual_A_events=ea,actual_B_events=eb,new_source_queries=queries,source_closed_embedding='uniform A-realization over the closed ten-mark B cycle with private11 in its rigid exterior gap; explicit word construction PENDING')
    out('private_max_pullback_critical_quartet.json',result);print(json.dumps({k:v for k,v in result.items() if k not in ('actual_A_before','actual_B_before','actual_A_after','actual_B_after','actual_A_events','actual_B_events')}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_core18_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':queries})
