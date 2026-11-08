"""Does the source-exact H2 counterfamily also defeat EVERY debt selector?"""
import functools,hashlib,json,pickle,sys,time
from pathlib import Path
from interior_projection_source_tools import *
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
@functools.lru_cache(None)
def trees(lo,hi):
    if lo>hi:return ('E',)
    return tuple((2*k,L,R) for k in range(lo,hi+1) for L in trees(lo,k-1) for R in trees(k+1,hi))
def main():
    Z=json.loads((B/'native10_source_actions.json').read_text());S=Lift(Z);N=len(S.T);mir=Z['mirror'];O=pickle.loads((B/'native10_B_modal_factored_debt.pkl').read_bytes());E=json.loads((B/'native10_B_specific_envelopes.json').read_text());groups={g:[b for b,t in enumerate(S.T) if t[0]==g] for g in range(1,11)}
    def D(a,b):return O['base'][b]+O['residual'].get(min(a*N+b,mir[a]*N+mir[b]),0)
    bad=None;shapes=couplings=0;maxdef=None;worst=None
    for g in range(6,11):
        c=g-1
        for W in trees(4,g-3):
            for R in trees(g+1,10):
                As=(2*g,(2*(g-1),(2*(g-2),(5,(4,(2,'E','E'),'E'),(6,'E',W)),'E'),'E'),R);At,H=S.access(As,4);assert H==2;pi=tuple(S.idx[t] for t in projections(As,5));pt=tuple(S.idx[t] for t in projections(At,5));assert len(pi)==2 and len(pt)==1;shapes+=1
                for b in groups[g]:
                    q=Z['Q'][b][1];bt=Z['destination'][b][1];w=4-q;ds=[D(a,b) for a in pi];dt=D(pt[0],bt);deficit=min(ds)-w-dt;couplings+=1
                    if maxdef is None or deficit>maxdef:maxdef=deficit;worst={'source_B':b,'target_B':bt,'H':2,'Q':q,'price':w,'source_debts':ds,'target_debt':dt,'source_B_floor':E['low'][b],'old_source_indices':pi,'old_target_index':pt[0]}
                    if deficit>0:
                        bad={'source_A':As,'actual_A_target':At,'private_key':5,'source_B_core_index':b,'B_target_core_index':bt,'target_actual_key':4,'H':2,'Q':q,'price':w,'DELETE_helper':None,'operation_word':[['K',4]],'source_contraction_indices':pi,'target_contraction_indices':pt,'all_source_contraction_debts':ds,'D_target':dt,'minimum_source_debt':min(ds),'signed_margin_upper_bound':-deficit,'source_required_B_floor':E['low'][b]};break
                if bad:break
                if time.process_time()-START>CAP-3:raise TimeoutError('RETIREMENT_FAMILY_PROBE_CAP')
            if bad:break
        if bad:break
    out('retirement_depth4_debt_selector_candidate.json',{'status':'ALL_CONTRACTION_RANGE_DEBT_SELECTORS_RAW_REFUTATION' if bad else 'RETIREMENT_FAMILY_DEBT_SELECTOR_DISCOVERY_NO_COUNTER','candidate':bad,'source_shapes':shapes,'source_couplings':couplings,'maximum_minimum_selector_deficit':maxdef,'worst_case':worst,'known_fixed_ten_family_complete':bad is None,'not_a_universal_proof':True,'source_identity_instantiations':S.calls,'source_queries':0,'source_engine_calls':0,'principal_U33':'OPEN'})
    print(json.dumps({'status':'RETIREMENT_DEPTH4_SIGN_PROBE','counter':None if bad is None else {k:bad[k] for k in ('source_B_core_index','H','Q','price','all_source_contraction_debts','D_target','signed_margin_upper_bound')},'source_shapes':shapes,'source_couplings':couplings,'maximum_deficit':maxdef}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof159_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
