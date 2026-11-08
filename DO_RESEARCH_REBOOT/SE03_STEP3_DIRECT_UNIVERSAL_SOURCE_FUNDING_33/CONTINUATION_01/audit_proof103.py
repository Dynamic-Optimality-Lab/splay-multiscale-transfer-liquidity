"""Attack the stronger UNIQUE-projection interior-unary source law.
Actual RLRL path, old RLL path; both endpoint anchor projections unique.
"""
import json,pickle,time,sys,hashlib
from pathlib import Path
from interior_projection_source_tools import *
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    Z=json.loads((B/'native10_source_actions.json').read_text());S=Lift(Z);T=S.T;N=len(T);mir=Z['mirror'];file=B/'native10_B_modal_factored_debt.pkl';raw=file.read_bytes();check=json.loads((B/'native10_modal_oracle_independent_audit.json').read_text());assert hashlib.sha256(raw).hexdigest()==check['input_sha256'][file.name];p=pickle.loads(raw);L=p['residual'];base=p['base'];del raw,p
    def debt(a,b):return base[b]+L.get(min(a*N+b,mir[a]*N+mir[b]),0)
    Bcandidates=[b for b,t in enumerate(T) if t[0]==1 and Z['Q'][b][1]>=2];shapes=0;couplings=0;failure=None
    for a,t in enumerate(T):
        if t[0]!=1 or len(path(t,2))!=3:continue
        one,A,right=t;u,vterm,E=right
        if not isnode(vterm):continue
        v,two,D=vterm
        if not isnode(two) or two[0]!=2:continue
        x,BB,C=two;As=(2,scale(A),(2*u,(3,'private_left',scale(vterm)),scale(E)));At,h=S.access(As,4);assert h==2;ps=projections(As,3);pt=projections(At,3);assert len(ps)==len(pt)==1 and S.idx[ps[0]]==a;pa=S.idx[pt[0]];expected=(2,(1,A,BB),(u,(v,C,D),E));assert S.T[pa]==expected;shapes+=1
        for b in Bcandidates:
            q=Z['Q'][b][1];ds=debt(a,b);w=4-q
            if w>=ds:continue
            bt=Z['destination'][b][1];dt=debt(pa,bt);couplings+=1
            if w+dt-ds<0:
                failure={'source_A':As,'actual_A_target':At,'private_key':3,'source_B_core_index':b,'B_target_core_index':bt,'target_actual_key':4,'H':2,'Q':q,'price':w,'old_source_A_index':a,'old_projected_target_index':pa,'source_value_multiset':[ds],'target_value_multiset':[dt],'D_source':ds,'D_target':dt,'signed_margin':w+dt-ds,'candidate_scope':'ANY extension that retains the old D10 value whenever the anchor contraction is unique, even with full B and full projected-tree identities'};break
        if failure:break
        if time.process_time()-START>CAP-2:raise TimeoutError('UNARY_SOURCE_TEST_CAP')
    result={'status':'UNIQUE_PROJECTION_COMPATIBILITY_REFUTATION_CANDIDATE' if failure else 'COMPLETE_RLRL_UNIQUE_PROJECTION_CASE_PASSES_OLD_SIGN_LAW','candidate':failure,'source_A_shapes':shapes,'B_source_shapes':len(Bcandidates),'potentially_constraining_couplings':couplings,'source_identity_instantiations':S.calls,'source_queries':0,'source_engine_calls':0,'source_geometry':'insert private p between anchor1 and2 under the left child of the root1 right child; target anchor2; actual RLRL H2 projects a rotation on the old RLL target','principal_U33':'OPEN'};out('interior_RLRL_unique_projection_candidate.json',result);print(json.dumps({k:v for k,v in result.items() if k!='candidate'}));print(json.dumps({k:v for k,v in failure.items() if k not in ('source_A','actual_A_target')} if failure else {}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof103_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
