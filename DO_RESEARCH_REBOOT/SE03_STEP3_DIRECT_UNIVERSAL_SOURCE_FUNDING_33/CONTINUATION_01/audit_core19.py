"""Attack depth-two anonymous-maximum lifting at SAME original H=2 cost."""
import json,time,sys,pickle,hashlib,importlib.util
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent.parent;START=time.process_time();CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);queries=0
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    global queries
    native=json.loads((B/'native10_source_actions.json').read_text());T=list(map(fr,native['trees']));idx={t:i for i,t in enumerate(T)};N=len(T);D=native['destination'];Q=native['Q'];mirror=native['mirror'];receipt=json.loads((B/'native10_complete_independent_audit.json').read_text());raw=(B/'native10_debt_03.pkl').read_bytes();assert hashlib.sha256(raw).hexdigest()==receipt['input_sha256'];saved=pickle.loads(raw);level=saved['level'];del raw,saved;motifs={}
    def debt(a,b):return level.get(min(a*N+b,mirror[a]*N+mirror[b]),0)
    for a,t in enumerate(T):
        g,A,right=t
        if isinstance(right,str):continue
        p,BB,right2=right
        if isinstance(right2,str):continue
        u,ul,ur=right2
        if not isinstance(ur,str):
            x,dd,ee=ur;target=(x,(p,(g,A,BB),(u,ul,dd)),ee);motifs.setdefault(a,[]).append(('RRR',x,idx[target],(g,A,(p,BB,(11,right2,'F11')))))
        if not isinstance(ul,str):
            x,cc,dd=ul;target=(x,(p,(g,A,BB),cc),(u,dd,ur));motifs.setdefault(a,[]).append(('RRL',x,idx[target],(g,A,(p,BB,(11,right2,'F11')))))
    failure=None;examined=0
    for code,v in level.items():
        a,b=divmod(code,N)
        for aa,bb in {(a,b),(mirror[a],mirror[b])}:
            for motif,x,pt,aug in motifs.get(aa,[]):
                q=Q[bb][x-1];w=4-q
                if w>=v:continue
                bt=D[bb][x-1];dp=debt(pt,bt);examined+=1
                if w+dp-v<0:failure={'A_source':aa,'B_source':bb,'target':x,'motif':motif,'actual_A_before':aug,'projected_A_after':pt,'B_target':bt,'actual_H':2,'Q':q,'price':w,'D_source':v,'D_projected_target':dp,'actual_margin':w+dp-v};break
            if failure:break
        if failure:break
        if time.process_time()-START>CAP-3:raise TimeoutError('INTERNAL_LIFT_CPU')
    result={'status':'INTERNAL_MAX_UNARY_PULLBACK_COUNTEREXAMPLE_CANDIDATE' if failure else 'NO_H2_INTERNAL_TWO_MOTIF_PULLBACK_FAILURE_COMPLETE_CERTIFICATE_CANDIDATE','A_source_motifs':sum(map(len,motifs.values())),'source_candidates_inspected':examined,'failure':failure,'new_source_queries':0,'source_scope':'ten genuine marks plus SAME unmarked maximum11; unary private node at A depth2, mark-free rigid B gap10','principal_U33':'OPEN'}
    if failure:
        def embed(t):
            if isinstance(t,str):return (11,'F10','F11') if t=='F10' else t
            return t[0],embed(t[1]),embed(t[2])
        sp=importlib.util.spec_from_file_location('source_internal_unary_max33',P/'SE03_STEP2_COLD_NEG2_01/source_model.py');S=importlib.util.module_from_spec(sp);sp.loader.exec_module(S);p0=S.path
        def path(t,x):
            global queries
            if queries>=QCAP:raise TimeoutError('SOURCE_CAP')
            queries+=1;return p0(t,x)
        S.path=path;As=failure['actual_A_before'];Bs=embed(T[failure['B_source']]);x=failure['target'];At,pa,ea=S.trace(As,x);Bt,pb,eb=S.trace(Bs,x)
        def suppress(t):
            if isinstance(t,str):return t
            if t[0]==11:assert t[2]=='F11';return suppress(t[1])
            return t[0],suppress(t[1]),suppress(t[2])
        assert len(ea)==2 and len(pb)//2==failure['Q'] and suppress(At)==T[failure['projected_A_after']] and suppress(Bt)==T[failure['B_target']];result.update(actual_B_before=Bs,actual_A_after=At,actual_B_after=Bt,actual_A_path=pa,actual_B_path=pb,actual_A_events=ea,actual_B_events=eb,new_source_queries=queries,explicit_closed_word='PENDING; uniform source realization theorem already supplies the mathematical closed-embedding implication')
    out('internal_max_unary_pullback_source_candidate.json',result);print(json.dumps({k:v for k,v in result.items() if k not in ('actual_B_before','actual_A_after','actual_B_after','actual_A_events','actual_B_events','failure')},failure={k:v for k,v in failure.items() if k!='actual_A_before'} if failure else None))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_core19_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':queries})
