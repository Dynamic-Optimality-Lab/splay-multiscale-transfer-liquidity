"""Attempt a fixed-FULL-B final control for the root-aware multiset obstruction."""
import json,time,sys,pickle,hashlib
from pathlib import Path
from interior_projection_source_tools import *
B=Path(__file__).resolve().parent
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    Z=json.loads((B/'native10_source_actions.json').read_text());S=Lift(Z);T=S.T;N=len(T);mir=Z['mirror'];r=json.loads((B/'native10_complete_independent_audit.json').read_text());raw=(B/'native10_debt_03.pkl').read_bytes();assert hashlib.sha256(raw).hexdigest()==r['input_sha256'];L=pickle.loads(raw)['level'];debt=lambda a,b:L.get(min(a*N+b,mir[a]*N+mir[b]),0);e2=json.loads((B/'root_aware_contraction_second_closed_source.json').read_text())['candidate'];b=e2['B_target_core_index'];assert T[b][0]==3;bt=Z['destination'][b][0];q=Z['Q'][b][0];failure=None;count=0
    for t in T:
        g,left,R=t
        if g!=3 or left!=(1,'F0',(2,'F1','F2')):continue
        As=(6,(3,(2,'A','B'),(4,'C','D')),scale(R));At,h=S.access(As,2);assert h==1;ps=tuple(S.idx[p] for p in projections(As,3));pt=tuple(S.idx[p] for p in projections(At,3));src=sorted(debt(a,b) for a in ps);dst=sorted(debt(a,bt) for a in pt);count+=1
        if src==[0,2] and dst==[0] and q==1:
            failure={'source_A':As,'actual_A_target':At,'private_key':3,'source_B_core_index':b,'B_target_core_index':bt,'target_actual_key':2,'H':1,'Q':q,'price':1,'source_value_multiset':src,'target_value_multiset':dst,'source_projection_indices':ps,'target_projection_indices':pt,'source_value_mask':5,'target_value_mask':1,'source_mask':37,'target_mask':1};break
    out('full_B_contraction_multiset_final_control_candidate.json',{'status':'FIXED_FULL_B_MULTISET_FINAL_CONTROL_FOUND' if failure else 'NO_CONTROL_IN_THE_COMPLETE_429_RIGHT_TAIL_DOMAIN','candidate':failure,'right_tail_shapes_inspected':count,'accepted_source_identity_instantiations':S.calls,'source_queries':0,'source_engine_calls':0,'principal_U33':'OPEN'});print(json.dumps({'status':'FOUND' if failure else 'NO_CONTROL','shapes':count,'B_source':b,'B_target':bt,'Q':q,'candidate_source_projection_indices':failure['source_projection_indices'] if failure else None}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof90_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
