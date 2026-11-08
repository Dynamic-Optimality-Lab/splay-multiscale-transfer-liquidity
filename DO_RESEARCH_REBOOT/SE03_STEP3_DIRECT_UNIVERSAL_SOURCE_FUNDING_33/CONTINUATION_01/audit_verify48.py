"""Independent native-target rotation check for the two new H2 coefficient laws.
Stream old positive coefficients, expand reflection, use certified modal lookup.
"""
import json,pickle,re,time,sys,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def node(t):return isinstance(t,tuple)
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    source=B/'native10_source_actions.json';Z=json.loads(source.read_text());receipt=json.loads((B/'native10_source_independent_audit.json').read_text());assert hashlib.sha256(source.read_bytes()).hexdigest()==receipt['input_sha256'];T=list(map(fr,Z['trees']));N=len(T);index={t:i for i,t in enumerate(T)};mir=Z['mirror'];file=B/'native10_B_modal_factored_debt.pkl';raw=file.read_bytes();checked=json.loads((B/'native10_modal_oracle_independent_audit.json').read_text());assert hashlib.sha256(raw).hexdigest()==checked['input_sha256'][file.name];D=pickle.loads(raw);base=D['base'];R=D['residual'];del raw,D
    def debt(a,b):return base[b]+R.get(min(a*N+b,mir[a]*N+mir[b]),0)
    patterns={};shapes={'RLL_MIN_ROOT':0,'LRR_MIN_LEFT':0}
    for a,t in enumerate(T):
        g,L,RR=t
        if g==1 and node(RR) and node(RR[1]) and node(RR[1][1]):
            x=RR[1][1][0];nt=T[Z['destination'][a][x-1]];xx,left,right=nt;v,C,ur=right;u,DD,E=ur;pa=index[(xx,left,(u,(v,C,DD),E))];patterns.setdefault(a,[]).append(('RLL_MIN_ROOT',x,pa));shapes['RLL_MIN_ROOT']+=1
        if node(L) and L[0]==1 and node(L[2]) and node(L[2][2]):
            x=L[2][2][0];nt=T[Z['destination'][a][x-1]];xx,left,right=nt;u,one,C=left;mark,A,BB=one;assert mark==1;pa=index[(xx,(mark,A,(u,BB,C)),right)];patterns.setdefault(a,[]).append(('LRR_MIN_LEFT',x,pa));shapes['LRR_MIN_LEFT']+=1
    assert shapes=={'RLL_MIN_ROOT':2002,'LRR_MIN_LEFT':2002};data=(B/'native10_credit_certificate.json').read_bytes();lo=data.index(b'"nonzero_debt":[')+len(b'"nonzero_debt":[');hi=data.index(b'],"omitted_debt"',lo);cases={'RLL_MIN_ROOT':[],'LRR_MIN_LEFT':[]};source_states=0
    for hit in re.finditer(rb'\[(\d+),([123])\]',data[lo:hi]):
        code,ds=map(int,hit.groups());a,b=divmod(code,N);source_states+=1
        for aa,bb in ((a,b),(mir[a],mir[b])):
            for kind,x,pa in patterns.get(aa,()):
                q=Z['Q'][bb][x-1];w=4-q
                if w>=ds:continue
                bt=Z['destination'][bb][x-1];dt=debt(pa,bt);assert w+dt-ds>=0;cases[kind].append([aa,bb,x,q,ds,pa,bt,dt])
        if source_states%131072==0 and time.process_time()-START>CAP-2:raise TimeoutError('COEFFICIENT_AUDIT_CAP')
    assert source_states==1769616 and len(cases['RLL_MIN_ROOT'])==584 and len(cases['LRR_MIN_LEFT'])==1149
    names=('native10_source_actions.json','native10_modal_oracle_independent_audit.json','native10_credit_certificate.json','interior_RLRL_unique_projection_candidate.json','interior_RLRL_remaining_unique_projection_candidate.json','interior_LRRR_unique_projection_candidate.json','first_gap_predecessor_direct_LOW_normal_forms.json')
    out('first_gap_new_H2_coefficients_independent_audit.json',{'status':'PASS_COMPLETE_FIRST_GAP_RLL_AND_LRR_COEFFICIENT_LAWS','source_shapes':shapes,'constraining_cases':cases,'old_positive_coefficients_streamed':source_states,'implicit_zero_sources':'safe because4-Q>=0 and Dtarget>=0','other_positive_sources':'safe when4-Q>=Dsource; every remaining case listed and checked','counterpart_ordinary_source_matrices':'already completely checked and pinned, no new source oracle','producer_metadata_correction':'proof104 source_geometry string says targetanchor2 although its code and complete1001 new rows treat all remaining targets; logical source classes independently reconstructed here','source_queries':0,'source_engine_calls':0,'principal_U33':'OPEN','external_or_formal_proof_assistant_verification':False,'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in names}});print(json.dumps({'status':'PASS_RLL_LRR_COEFFICIENT_LAWS','source_shapes':shapes,'constraining_cases':{k:len(v) for k,v in cases.items()},'source_queries':0}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify48_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
