"""Falsify source-geometric joins at the second gap using exact old identities."""
import json,pickle,time,sys,hashlib,collections
from pathlib import Path
from interior_projection_source_tools import *
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    Z=json.loads((B/'native10_source_actions.json').read_text());S=Lift(Z);N=len(S.T);mir=Z['mirror'];raw=(B/'native10_B_modal_factored_debt.pkl').read_bytes();pin=json.loads((B/'native10_modal_oracle_independent_audit.json').read_text());assert hashlib.sha256(raw).hexdigest()==pin['input_sha256']['native10_B_modal_factored_debt.pkl'];O=pickle.loads(raw);del raw
    debt=lambda a,b:O['base'][b]+O['residual'].get(min(a*N+b,mir[a]*N+mir[b]),0)
    prior=json.loads((B/'second_gap_join_candidates_raw.json').read_text());gap=2;p=5;failures=prior['candidate_failures'];comparisons=collections.Counter();cursor=0;groups=collections.defaultdict(list)
    for b,t in enumerate(S.T):groups[t[0]].append(b)
    def split(t):
        if not isnode(t):return 'E','E'
        if t[0]<p:L,R=split(t[2]);return (t[0],t[1],L),R
        L,R=split(t[1]);return L,(t[0],R,t[2])
    def join(L,R,kind):
        if not isnode(L):return R
        if not isnode(R):return L
        if kind=='predecessor':choose=True
        elif kind=='nearest_root':choose=abs(L[0]-p)<=abs(R[0]-p)
        else:choose=len(known(L))<=len(known(R))
        return (L[0],L[1],join(L[2],R,kind)) if choose else (R[0],join(L,R[1],kind),R[2])
    def project(t,kind):
        if not isnode(t):return t
        L,R=project(t[1],kind),project(t[2],kind)
        return join(L,R,kind) if t[0]==p else (t[0],L,R)
    order=sorted(range(prior['old_A_cursor'],N),key=lambda a:(S.T[a][0] not in (4,5,6,7,8),abs(S.T[a][0]-6),a))
    for pos,ai in enumerate(order):
        old=S.T[ai]
        if time.process_time()-START>CAP-2:break
        g=old[0];a=scale(old);d=2 if 2*g<p else 1;U=a[d];left,right=split(U);priv=(p,left,right);As=(a[0],priv,a[2]) if d==1 else (a[0],a[1],priv)
        for side in (left,right):
            if not isnode(side):continue
            x=side[0];At,h=S.access(As,x);assert h==1
            Bs=sorted(groups[g],key=lambda b:(-Z['Q'][b][x//2-1],b))
            for kind in ('predecessor','nearest_root','smaller_side'):
                if kind in failures:continue
                src=normalize(project(As,kind),{2*k:k for k in range(1,11)});dst=normalize(project(At,kind),{2*k:k for k in range(1,11)});sa=S.idx[src];ta=S.idx[dst]
                for b in Bs:
                    q=Z['Q'][b][x//2-1];ds=debt(sa,b);w=2-q;comparisons[kind]+=1
                    if w>=ds:continue
                    bt=Z['destination'][b][x//2-1];dt=debt(ta,bt)
                    if w+dt-ds<0:
                        failures[kind]={'source_A':As,'actual_A_target':At,'private_key':p,'source_B_core_index':b,'B_target_core_index':bt,'target_actual_key':x,'H':h,'Q':q,'price':w,'projection_rule':kind,'old_source_A_index':sa,'old_projected_target_index':ta,'D_source':ds,'D_target':dt,'signed_margin':w+dt-ds};break
        cursor=pos+1
        if len(failures)==3:break
    z={'status':'ALL_THREE_SECOND_GAP_JOIN_CANDIDATES_REFUTED_RAW' if len(failures)==3 else 'SECOND_GAP_GEOMETRIC_JOIN_DISCOVERY_OPEN','gap':gap,'candidate_failures':failures,'old_A_cursor':cursor,'old_A_total':N,'B_couplings':dict(comparisons),'source_identity_instantiations':S.calls,'source_queries':0,'source_engine_calls':0,'explicit_closed_source_embedding':'PENDING','principal_U33':'OPEN'};out('second_gap_join_candidates_continuation.json',z);out('second_gap_join_work_01.json',{'A_order':order,'next_pos':cursor,'failures':failures,'initial_checked_A_prefix':prior['old_A_cursor']});print(json.dumps({k:v for k,v in z.items() if k!='candidate_failures'}));print(json.dumps({k:{f:e[f] for f in ('source_B_core_index','target_actual_key','H','Q','D_source','D_target','signed_margin')} for k,e in failures.items()}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof111_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
