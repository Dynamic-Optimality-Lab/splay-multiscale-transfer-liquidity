"""Exact inverse-one-event test for the minimum-contraction debt, no oracle."""
import json,time,sys,pickle,hashlib
from pathlib import Path
from interior_projection_source_tools import *
from audit_verify35 import rotate
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def paths(t,depth=2):
    r=[]
    def walk(t,p):
        if not isnode(t) or len(p)>depth:return
        if p:r.append(p)
        walk(t[1],p+[1]);walk(t[2],p+[2])
    walk(t,[]);return r
def main():
    old=json.loads((B/'interior_contraction_potential_source_candidates.json').read_text())['failures']['max'];target=fr(old['source_A']);private=old['private_key'];x=target[0];native=json.loads((B/'native10_source_actions.json').read_text());S=Lift(native);T=S.T;N=len(T);mir=native['mirror'];raw=(B/'native10_debt_03.pkl').read_bytes();R=json.loads((B/'native10_complete_independent_audit.json').read_text());assert hashlib.sha256(raw).hexdigest()==R['input_sha256'];level=pickle.loads(raw)['level'];del raw
    def debt(a,b):return level.get(min(a*N+b,mir[a]*N+mir[b]),0)
    candidates={rotate(target,p) for p in paths(target)}
    for t in list(candidates):candidates.update(rotate(t,p) for p in paths(t))
    incoming=[]
    for t in candidates:
        if t[0]==private or len(path(t,x))>2:continue
        dest,h=S.access(t,x)
        if h==1 and normalize(dest)==normalize(target):incoming.append(t)
    failure=None;checks=0;target_projs=tuple(S.idx[t] for t in projections(target,private));X=x//2
    for t in incoming:
        source_projs=tuple(S.idx[a] for a in projections(t,private));g=t[0]//2
        for b,Bs in enumerate(T):
            q=native['Q'][b][X-1]
            if Bs[0]!=g or q<3:continue
            bt=native['destination'][b][X-1];src=[debt(a,b) for a in source_projs];dst=[debt(a,bt) for a in target_projs];checks+=1;ds=min(src);dt=min(dst);w=2-q
            if w+dt-ds<0:
                failure={'candidate':'min_over_all_BST_anchor_contractions','private_key':private,'source_A':t,'source_B_core_index':b,'target_anchor':X,'target_actual_key':x,'actual_A_target':target,'H':1,'Q':q,'price':w,'D_source':ds,'D_target':dt,'signed_margin':w+dt-ds,'all_source_projection_indices':source_projs,'all_target_projection_indices':target_projs,'all_source_projection_debts':src,'all_target_projection_debts':dst,'B_target_core_index':bt,'source_validity':'source-exact local identity, common-initial closed-B realization applies; explicit source word PENDING'};break
        if failure:break
    result={'status':'MINIMUM_CONTRACTION_POTENTIAL_FAILS' if failure else 'NO_FAILURE_AT_THIS_INVERSE_DOMAIN','failure':failure,'inverse_one_event_A_preimages':len(incoming),'candidate_B_couplings':checks,'accepted_primitive_rigid_leaf_instantiations':S.calls,'source_queries':0,'source_engine_calls':0,'primary_U33':'OPEN','no_original_CD_counterexample_claim':True};out('interior_min_contraction_incoming_candidate.json',result);print(json.dumps({k:v for k,v in result.items() if k!='failure'}));print(json.dumps({k:v for k,v in failure.items() if k not in ('source_A','actual_A_target')} if failure else {}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof83_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
