"""Sharp unary-RR minimum-contraction coefficient obligation, all old A shapes.
No new actual source engine: accepted term identities only.
"""
import json,time,sys,pickle,hashlib,collections
from pathlib import Path
from interior_projection_source_tools import *
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    Z=json.loads((B/'native10_source_actions.json').read_text());S=Lift(Z);T=S.T;N=len(T);mir=Z['mirror'];R=json.loads((B/'native10_complete_independent_audit.json').read_text());raw=(B/'native10_debt_03.pkl').read_bytes();assert hashlib.sha256(raw).hexdigest()==R['input_sha256'];level=pickle.loads(raw)['level'];del raw
    def debt(a,b):return level.get(min(a*N+b,mir[a]*N+mir[b]),0)
    motifs={};groups=collections.defaultdict(list)
    for a,t in enumerate(T):
        g,A,R=t
        if not isnode(R):continue
        x,C,D=R
        if not isnode(C):continue # no extra contractions, old source law directly applies
        private=2*g+1;As=(2*g,scale(A),(private,'new_gap',scale(R)));At,h=S.access(As,2*x);assert h==1;pts=tuple(S.idx[v] for v in projections(At,private));motifs[a]=(x,private,As,At,pts);groups[g,x].append(a)
    examined=0;failure=None;stage='positive_coefficients';complete=False
    def inspect(a,b,ds):
        nonlocal examined,failure
        x,private,As,At,pts=motifs[a];q=Z['Q'][b][x-1];w=2-q
        if w>=ds:return
        bt=Z['destination'][b][x-1];dt=min(debt(v,bt) for v in pts);examined+=1
        if w+dt-ds<0:failure={'candidate':'min_over_all_BST_anchor_contractions','private_key':private,'source_A':As,'source_B_core_index':b,'target_anchor':x,'target_actual_key':2*x,'actual_A_target':At,'H':1,'Q':q,'price':w,'D_source':ds,'D_target':dt,'signed_margin':w+dt-ds,'all_source_projection_indices':[a],'all_target_projection_indices':pts,'all_source_projection_debts':[ds],'all_target_projection_debts':[debt(v,bt) for v in pts],'B_target_core_index':bt}
    for j,(code,ds) in enumerate(level.items()):
        a,b=divmod(code,N)
        for aa,bb in ((a,b),(mir[a],mir[b])):
            if aa in motifs:inspect(aa,bb,ds)
            if failure:break
        if failure:break
        if j%32768==0 and time.process_time()-START>CAP-3:break
    else:
        stage='negative_zero_sources'
        for b,t in enumerate(T):
            for x,q in enumerate(Z['Q'][b],1):
                if q<3:continue
                for a in groups[t[0],x]:
                    if debt(a,b)==0:inspect(a,b,0)
                    if failure:break
                if failure:break
            if failure:break
            if b%256==0 and time.process_time()-START>CAP-3:break
        else:complete=True
    result={'status':'MIN_CONTRACTION_UNARY_RR_RULE_REFUTED' if failure else 'COMPLETE_UNARY_RR_MINIMUM_COEFFICIENT_PROPERTY' if complete else 'PARTIAL_UNARY_RR_MINIMUM_COEFFICIENT_CHECK','failure':failure,'stage':stage,'old_A_motifs':len(motifs),'potentially_constraining_couplings':examined,'accepted_source_identity_instantiations':S.calls,'source_queries':0,'source_engine_calls':0,'all_source_populations':'not claimed by a partial coefficient check','principal_U33':'OPEN'};out('interior_unary_RR_minimum_property.json',result);print(json.dumps({k:v for k,v in result.items() if k!='failure'}));print(json.dumps({k:v for k,v in failure.items() if k not in ('source_A','actual_A_target')} if failure else {}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof85_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
