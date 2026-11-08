"""Source-backed difference constraints for ANY nonlinear contraction-debt-set rule.
Singleton sets retain the frozen D10 values; all labels may be real in[0,3].
"""
import json,time,sys,pickle,hashlib,collections
from pathlib import Path
from interior_projection_source_tools import *
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def mask(values):return sum(1<<v for v in set(values))
def main():
    Z=json.loads((B/'native10_source_actions.json').read_text());S=Lift(Z);T=S.T;N=len(T);mir=Z['mirror'];raw=(B/'native10_debt_03.pkl').read_bytes();receipt=json.loads((B/'native10_complete_independent_audit.json').read_text());assert hashlib.sha256(raw).hexdigest()==receipt['input_sha256'];level=pickle.loads(raw)['level'];del raw
    def debt(a,b):return level.get(min(a*N+b,mir[a]*N+mir[b]),0)
    lower={m:(m.bit_length()-1 if m&(m-1)==0 else 0) for m in range(1,16)};upper={m:(m.bit_length()-1 if m&(m-1)==0 else 3) for m in range(1,16)};edges={};derivation=[];bad=None
    def solve():
        nonlocal bad
        labels=lower.copy();trace=[]
        for turn in range(60):
            changed=False
            for key,e in edges.items():
                s,t=e['source_mask'],e['target_mask'];required=labels[s]-e['price']
                if required>labels[t]:
                    trace.append({'edge_key':list(key),'source_label':labels[s],'old_target_label':labels[t],'new_target_label':required});labels[t]=required;changed=True
                    if required>upper[t]:bad={'violated_mask':t,'required':required,'upper_bound':upper[t],'trace':trace,'final_labels':labels};return
            if not changed:return
        raise AssertionError('WIDTH_BOUND_SHOULD_ALREADY_DETECT_ANY_DIVERGENCE')
    def add(e):
        key=e['source_mask'],e['target_mask'];old=edges.get(key)
        if old is None or e['price']<old['price']:edges[key]=e;solve()
    # Independently replayed controls, not inferred abstract edges.
    for file in ('interior_max_contraction_closed_source.json','interior_min_contraction_closed_source.json'):
        c=json.loads((B/file).read_text());e=c['candidate'];add({'source_mask':mask(e['all_source_projection_debts']),'target_mask':mask(e['all_target_projection_debts']),'price':e['price'],'kind':'accepted_closed_control','control_file':file,'source_A':e['source_A'],'actual_A_target':e['actual_A_target'],'private_key':e['private_key'],'source_B_core_index':e['source_B_core_index'],'B_target_core_index':e['B_target_core_index'],'target_actual_key':e['target_actual_key'],'H':e['H'],'Q':e['Q']})
    motifs={};count=0;visited=0
    for j,(code,ds) in enumerate(level.items()):
        a,b=divmod(code,N)
        for aa,bb in ((a,b),(mir[a],mir[b])):
            if aa not in motifs:
                g,A,R=T[aa]
                if not isnode(R) or not isnode(R[1]):motifs[aa]=None
                else:
                    x=R[0];private=2*g+1;As=(2*g,scale(A),(private,'new_gap',scale(R)));At,h=S.access(As,2*x);assert h==1;pts=tuple(S.idx[v] for v in projections(At,private));nexts=[]
                    for y in known(At):
                        if y==private or y==At[0] or len(path(At,y))>2:continue
                        Att,hy=S.access(At,y);assert hy==1;pt2=tuple(S.idx[v] for v in projections(Att,private));nexts.append((y,Att,pt2))
                    motifs[aa]=(x,private,As,At,pts,nexts)
            motif=motifs[aa]
            if motif is None:continue
            x,private,As,At,pts,nexts=motif;bt=Z['destination'][bb][x-1];q=Z['Q'][bb][x-1];dst=[debt(v,bt) for v in pts];target_mask=mask(dst);count+=1
            add({'source_mask':1<<ds,'target_mask':target_mask,'price':2-q,'kind':'source_unary_RR','source_A':As,'actual_A_target':At,'private_key':private,'source_B_core_index':bb,'B_target_core_index':bt,'target_actual_key':2*x,'H':1,'Q':q})
            if bad:break
            for y,Att,pt2 in nexts:
                btt=Z['destination'][bt][y//2-1];qy=Z['Q'][bt][y//2-1];dst2=[debt(v,btt) for v in pt2]
                add({'source_mask':target_mask,'target_mask':mask(dst2),'price':2-qy,'kind':'actual_successor_of_unary_RR','source_A':At,'actual_A_target':Att,'private_key':private,'source_B_core_index':bt,'B_target_core_index':btt,'target_actual_key':y,'H':1,'Q':qy})
                if bad:break
            if bad:break
        visited=j+1
        if bad:break
        if j%2048==0 and time.process_time()-START>CAP-3:break
    result={'status':'ALL_WIDTH_THREE_SINGLETON_COMPATIBLE_DEBT_SET_RULES_REFUTED' if bad else 'NO_REFUTATION_IN_PARTIAL_SOURCE_DOMAIN','bounds':{'lower':lower,'upper':upper},'edges':list(edges.values()),'contradiction':bad,'producer_positive_coefficients_visited':visited,'source_couplings':count,'source_schema_instantiations':S.calls,'source_queries':0,'source_engine_calls':0,'scope':'ANY real function of the set of unchanged D10 values over all anchor contractions, agrees F({d})=d, range[0,3]; not arbitrary source-defined debt','principal_U33':'OPEN'};out('contraction_debt_set_formula_candidate.json',result);print(json.dumps({k:v for k,v in result.items() if k not in ('edges','contradiction')}));print(json.dumps({'edges':len(edges),'contradiction':{k:v for k,v in bad.items() if k not in ('trace','final_labels')} if bad else None,'derivation_steps':len(bad['trace']) if bad else0}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof86_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
