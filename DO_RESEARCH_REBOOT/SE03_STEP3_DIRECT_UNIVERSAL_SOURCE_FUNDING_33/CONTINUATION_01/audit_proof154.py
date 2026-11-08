"""Falsify, if possible, the old B-lower-envelope extension to dirty A.
This is a stronger assumption than unrestricted full-geometry debt.
"""
import hashlib,json,pickle,sys,time
from pathlib import Path
from interior_projection_source_tools import *
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    Z=json.loads((B/'native10_source_actions.json').read_text());S=Lift(Z);N=len(S.T);mir=Z['mirror'];O=pickle.loads((B/'native10_B_modal_factored_debt.pkl').read_bytes());E=json.loads((B/'native10_B_specific_envelopes.json').read_text());pin=json.loads((B/'native10_B_envelopes_independent_audit.json').read_text());assert hashlib.sha256((B/'native10_B_specific_envelopes.json').read_bytes()).hexdigest()==pin['input_sha256']['native10_B_specific_envelopes.json']
    def D(a,b):return O['base'][b]+O['residual'].get(min(a*N+b,mir[a]*N+mir[b]),0)
    with (B/'full_geometry_sparse_work_05.pkl').open('rb') as f:w=pickle.load(f)
    groups={g:[b for b,t in enumerate(S.T) if t[0]==g and E['low'][b]>0] for g in range(1,11)};bad=None;checked=0;ashapes=0;complete=True
    for As in w['A']:
        pp=S.sub(As,5)
        if not isnode(pp[1]) or not isnode(pp[2]):continue
        options=[]
        for x in known(As):
            if x in (5,As[0]) or len(path(As,x))>4:continue
            At,H=S.access(As,x);options.append((x,H,None,At))
        for y in known(As):
            if y==As[0] or len(path(As,y))>2:continue
            mid,H=S.access(As,y);assert H==1
            for x in known(mid):
                if x in (5,mid[0],As[0]) or len(path(mid,x))>2:continue
                At,H=S.access(mid,x);assert H==1;options.append((x,2,y,At))
        ashapes+=1
        for x,H,helper,At in options:
            pt=S.sub(At,5)
            if isnode(pt[1]) and isnode(pt[2]):continue
            targetpi=tuple(S.idx[t] for t in projections(At,5));assert len(targetpi)==1
            for b in groups[As[0]//2]:
                q=Z['Q'][b][x//2-1];price=2*H-q
                if price>=E['low'][b]:continue
                bt=Z['destination'][b][x//2-1];dt=D(targetpi[0],bt);checked+=1
                if price+dt-E['low'][b]<0:
                    bad={'source_A':As,'actual_A_target':At,'private_key':5,'source_B_core_index':b,'B_target_core_index':bt,'target_actual_key':x,'H':H,'Q':q,'price':price,'DELETE_helper':helper,'operation_word':([['D',helper]] if helper is not None else [])+[['K',x]],'source_contraction_indices':tuple(S.idx[t] for t in projections(As,5)),'target_contraction_indices':targetpi,'source_required_B_floor':E['low'][b],'D_target':dt,'signed_margin_upper_bound':price+dt-E['low'][b]};break
            if bad:break
        if bad:break
        if time.process_time()-START>CAP-3:complete=False;break
    out('B_lower_envelope_extension_candidate.json',{'status':'B_LOWER_ENVELOPE_DIRTY_EXTENSION_RAW_COUNTER' if bad else 'B_LOWER_ENVELOPE_DIRTY_EXTENSION_DISCOVERY_OPEN','candidate':bad,'source_A_shapes_considered':ashapes,'relevant_source_couplings':checked,'known_A_prefix_complete':complete and bad is None,'source_identity_instantiations':S.calls,'scope':'J agrees with old debt on unary A and satisfies J(A,B)>=old root-compatible minimum l_B on dirty A; no upper bound assumed','source_queries':0,'source_engine_calls':0,'principal_U33':'OPEN'})
    print(json.dumps({'status':'B_LOWER_ENVELOPE_PROBE','counter':None if bad is None else {k:bad[k] for k in ('H','Q','price','source_B_core_index','source_required_B_floor','D_target','signed_margin_upper_bound')},'A_shapes':ashapes,'couplings':checked,'prefix_complete':complete and bad is None}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof154_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
