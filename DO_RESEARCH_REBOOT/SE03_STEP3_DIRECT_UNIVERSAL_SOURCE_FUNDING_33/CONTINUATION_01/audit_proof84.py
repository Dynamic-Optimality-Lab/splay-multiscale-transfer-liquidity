"""Symbolic diagonal-target construction against minimum-contraction debt."""
import json,time,sys,pickle,hashlib
from pathlib import Path
from interior_projection_source_tools import *
B=Path(__file__).resolve().parent
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def remove_min(t):
    assert isnode(t)
    return t[2] if not isnode(t[1]) else (t[0],remove_min(t[1]),t[2])
def main():
    native=json.loads((B/'native10_source_actions.json').read_text());S=Lift(native);T=S.T;N=len(T);mir=native['mirror'];v=0;assert known(T[v])==list(range(1,11)) and all((not isnode(S.sub(T[v],k)[1])) for k in range(1,11));target=10;bt=native['destination'][v][9];q=native['Q'][v][9];assert q==4;tt=T[bt];assert tt[0]==10 and not isnode(tt[2]);C=remove_min(tt[1]);private=3;As=(2,'A',(private,'B',(20,scale(C),'C')));At,h=S.access(As,20);assert h==1;source_projs=tuple(S.idx[p] for p in projections(As,private));target_projs=tuple(S.idx[p] for p in projections(At,private));assert bt in target_projs
    R=json.loads((B/'native10_complete_independent_audit.json').read_text());raw=(B/'native10_debt_03.pkl').read_bytes();assert hashlib.sha256(raw).hexdigest()==R['input_sha256'];L=pickle.loads(raw)['level'];debt=lambda a,b:L.get(min(a*N+b,mir[a]*N+mir[b]),0);src=[debt(a,v) for a in source_projs];dst=[debt(a,bt) for a in target_projs];assert debt(bt,bt)==0 and min(dst)==0;ds=min(src);margin=2-q-ds;assert margin<0
    failure={'candidate':'min_over_all_BST_anchor_contractions','private_key':private,'source_A':As,'source_B_core_index':v,'target_anchor':10,'target_actual_key':20,'actual_A_target':At,'H':1,'Q':q,'price':2-q,'D_source':ds,'D_target':0,'signed_margin':margin,'all_source_projection_indices':source_projs,'all_target_projection_indices':target_projs,'all_source_projection_debts':src,'all_target_projection_debts':dst,'diagonal_target_projection':bt,'B_target_core_index':bt,'source_validity':'exact source identity; original closed word construction next'}
    result={'status':'MINIMUM_CONTRACTION_RULE_REFUTED_BY_DIAGONAL_TARGET_PACKET','failure':failure,'parametric_scope':'n>=7 anchors; full B ascending vine, target n, private z between1 and2, C obtained by contracting minimum1 in S_n(vine).left; any nonnegative old debt with diagonal0 fails minimum-contraction pullback','accepted_primitive_identity_instantiations':S.calls,'source_queries':0,'source_engine_calls':0,'principal_U33':'OPEN'};out('interior_min_contraction_diagonal_candidate.json',result);print(json.dumps({k:v for k,v in failure.items() if k not in ('source_A','actual_A_target')}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof84_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
