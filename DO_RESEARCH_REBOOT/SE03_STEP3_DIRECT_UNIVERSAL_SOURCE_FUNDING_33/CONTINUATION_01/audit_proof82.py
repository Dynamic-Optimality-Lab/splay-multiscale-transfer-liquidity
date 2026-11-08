"""Falsify naive min/max anchor-contraction debts at an interior A ancestor.
Uses accepted ten-node primitives by an off-path rigid-leaf identity, no oracle.
"""
import json,time,sys,hashlib,pickle,collections
from pathlib import Path
from interior_projection_source_tools import *
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    native=json.loads((B/'native10_source_actions.json').read_text());S=Lift(native);T=S.T;N=len(T);mirror=native['mirror'];receipt=json.loads((B/'native10_complete_independent_audit.json').read_text());raw=(B/'native10_debt_03.pkl').read_bytes();assert hashlib.sha256(raw).hexdigest()==receipt['input_sha256'];level=pickle.loads(raw)['level'];del raw
    def debt(a,b):return level.get(min(a*N+b,mirror[a]*N+mirror[b]),0)
    byroot=collections.defaultdict(list)
    for b,t in enumerate(T):byroot[t[0]].append(b)
    failures={};examined=0;shapes=0
    for a,t in enumerate(T):
        g,A,R=t
        if not isnode(R) or not isnode(R[1]):continue
        z=2*g+1;As=(2*g,scale(A),(z,'z_gap',scale(R)));created,h=S.access(As,2*R[0]);assert h==1;assert isnode(S.sub(created,z)[1]) and isnode(S.sub(created,z)[2]);shapes+=1
        source_projs=tuple(S.idx[v] for v in projections(created,z));root=created[0]//2
        for target in known(created):
            if target==z or target==created[0] or len(path(created,target))>2:continue
            At,ha=S.access(created,target);assert ha==1;target_projs=tuple(S.idx[v] for v in projections(At,z));x=target//2
            for b in byroot[root]:
                q=native['Q'][b][x-1];w=2-q;bt=native['destination'][b][x-1];src=[debt(v,b) for v in source_projs];dst=[debt(v,bt) for v in target_projs];examined+=1
                for name,f in (('min',min),('max',max)):
                    if name not in failures and w+f(dst)-f(src)<0:
                        failures[name]={'candidate':name+'_over_all_BST_anchor_contractions','private_key':z,'source_A':created,'source_B_core_index':b,'target_anchor':x,'target_actual_key':target,'actual_A_target':At,'H':1,'Q':q,'price':w,'D_source':f(src),'D_target':f(dst),'signed_margin':w+f(dst)-f(src),'all_source_projection_indices':source_projs,'all_target_projection_indices':target_projs,'all_source_projection_debts':src,'all_target_projection_debts':dst,'B_target_core_index':bt,'source_validity':'common-initial closed-B A-realization theorem applies; explicit original source word PENDING'}
                if len(failures)==2:break
            if len(failures)==2:break
        if len(failures)==2:break
        if time.process_time()-START>CAP-3:break
    result={'status':'BOTH_MIN_MAX_CONTRACTION_CANDIDATES_FAIL' if len(failures)==2 else 'PARTIAL_TARGETED_CONTRACTION_FALSIFICATION','failures':failures,'states_inspected':shapes,'coefficient_couplings_inspected':examined,'accepted_primitive_rigid_leaf_instantiations':S.calls,'source_queries':0,'source_engine_calls':0,'primary_U33':'OPEN','no_original_CD_counterexample_claim':True,'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('native10_source_actions.json','native10_debt_03.pkl','native10_complete_independent_audit.json')}}
    out('interior_contraction_potential_source_candidates.json',result);print(json.dumps({'status':result['status'],'states':shapes,'couplings':examined,'primitive_instances':S.calls,'failure_summaries':[{k:v for k,v in f.items() if k in ('candidate','private_key','source_B_core_index','target_anchor','H','Q','D_source','D_target','signed_margin')} for f in failures.values()]}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof82_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
