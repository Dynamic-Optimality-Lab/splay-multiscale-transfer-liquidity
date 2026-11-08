"""Remaining first-gap predecessor-projection H2 mismatch: old LRR with left1.
Actual LRRR, one anonymous first-gap node under anchor1.right.
"""
import json,pickle,time,sys,hashlib
from pathlib import Path
from interior_projection_source_tools import *
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    Z=json.loads((B/'native10_source_actions.json').read_text());S=Lift(Z);T=S.T;N=len(T);mir=Z['mirror'];file=B/'native10_B_modal_factored_debt.pkl';raw=file.read_bytes();check=json.loads((B/'native10_modal_oracle_independent_audit.json').read_text());assert hashlib.sha256(raw).hexdigest()==check['input_sha256'][file.name];d=pickle.loads(raw);L=d['residual'];base=d['base'];del raw,d
    def debt(a,b):return base[b]+L.get(min(a*N+b,mir[a]*N+mir[b]),0)
    byroot={g:[b for b,t in enumerate(T) if t[0]==g] for g in range(1,11)};failure=None;shapes=couplings=0
    for a,t in enumerate(T):
        g,left,E=t
        if not isnode(left) or left[0]==1 or not isnode(left[2]) or not isnode(left[2][2]):continue
        one,A,uTerm=left;u,BB,xTerm=uTerm;x,C,D=xTerm;private=2*one+1;As=(2*g,(2*one,scale(A),(private,'private_left',scale(uTerm))),scale(E));At,h=S.access(As,2*x);assert h==2;ps=projections(As,private);pt=projections(At,private);assert len(ps)==len(pt)==1 and S.idx[ps[0]]==a;pa=S.idx[pt[0]];assert T[pa]==(x,(one,A,(u,BB,C)),(g,D,E));shapes+=1
        for b in byroot[g]:
            q=Z['Q'][b][x-1];w=4-q;ds=debt(a,b)
            if w>=ds:continue
            bt=Z['destination'][b][x-1];dt=debt(pa,bt);couplings+=1
            if w+dt-ds<0:
                failure={'source_A':As,'actual_A_target':At,'private_key':private,'source_B_core_index':b,'B_target_core_index':bt,'target_actual_key':2*x,'H':2,'Q':q,'price':w,'old_source_A_index':a,'old_projected_target_index':pa,'source_value_multiset':[ds],'target_value_multiset':[dt],'D_source':ds,'D_target':dt,'signed_margin':w+dt-ds,'scope':'unique contraction at both endpoints; refutes retaining the old D10 on all new unary states'};break
        if failure:break
        if time.process_time()-START>CAP-2:raise TimeoutError('LRRR_SOURCE_CAP')
    result={'status':'UNIQUE_PROJECTION_COMPATIBILITY_REFUTATION_CANDIDATE' if failure else 'COMPLETE_NONMINIMUM_LEFT_LRRR_PROJECTION_CASES_PASS','candidate':failure,'source_A_shapes':shapes,'potentially_constraining_couplings':couplings,'source_identity_instantiations':S.calls,'source_queries':0,'source_engine_calls':0,'source_geometry':'old rootg leftanchor a>1 rightu rightx; insert p in gap(a,a+1) aboveu; actual LRRR; both projections unique','principal_U33':'OPEN'};out('general_LRRR_unique_projection_candidate.json',result);print(json.dumps({k:v for k,v in result.items() if k!='candidate'}));print(json.dumps({k:v for k,v in failure.items() if k not in ('source_A','actual_A_target')} if failure else {}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof113_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
