"""Streaming independent proof of the exact modal-B oracle, including all zeros.
No simultaneous materialization of the 1.77m old states and new override table.
"""
import json,pickle,re,time,sys,hashlib,collections
from pathlib import Path
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    file=B/'native10_B_modal_factored_debt.pkl';blob=file.read_bytes();filepin=hashlib.sha256(blob).hexdigest();z=pickle.loads(blob);del blob;R=z['residual'];mode=z['base'];Z=json.loads((B/'native10_source_actions.json').read_text());N=len(Z['trees']);roots=[t[0] for t in Z['trees']];counts=collections.Counter(roots);mir=Z['mirror'];data=(B/'native10_credit_certificate.json').read_bytes();oldpin=re.search(rb'"checked_input_pickle_sha256":"([0-9a-f]+)"',data).group(1).decode();assert oldpin==z['old_sha256'];start=data.index(b'"nonzero_debt":[')+len(b'"nonzero_debt":[');end=data.index(b'],"omitted_debt"',start);hist=[[0]*4 for _ in range(N)];last=-1;seen=overrides_seen=0
    for match in re.finditer(rb'\[(\d+),([123])\]',data[start:end]):
        code,d=map(int,match.groups());assert code>last;last=code;a,b=divmod(code,N);assert roots[a]==roots[b]<=5;assert mode[b]+R.get(code,0)==d;seen+=1;hist[b][d]+=1
        if code in R:overrides_seen+=1
    assert seen==1769616==z['original_nonzero_states'];zero_override=[0]*N;positive_overrides=0
    for code,delta in R.items():
        a,b=divmod(code,N);assert 0<=a<N and 0<=b<N and roots[a]==roots[b]<=5 and code<mir[a]*N+mir[b] and delta!=0;d=mode[b]+delta;assert 0<=d<=3
        if d:positive_overrides+=1
        else:zero_override[b]+=1
    assert positive_overrides==overrides_seen;expected=0
    for b,g in enumerate(roots):
        assert mode[b]==mode[mir[b]]
        if g>5:continue
        hist[b][0]=counts[g]-sum(hist[b]);assert hist[b][0]>=0
        chosen=max(range(4),key=lambda d:(hist[b][d],-d));assert mode[b]==chosen
        if chosen>0:assert zero_override[b]==hist[b][0]
        else:assert zero_override[b]==0
        expected+=counts[g]-hist[b][chosen]
    assert len(R)==expected==1013185 and sum(zero_override)==475429;assert time.process_time()-START<CAP-1
    out('native10_modal_oracle_independent_audit.json',{'status':'PASS_LOSSLESS_COMPLETE_MODAL_B_DEBT_REPRESENTATION','old_nonzero_coefficients_streamed':seen,'new_explicit_override_states':len(R),'includes_original_zero_override_states':sum(zero_override),'all_old_positive_states_verified':True,'all_old_omitted_zero_states_verified':'exact per-column missing counts and explicit zero coverage when baseline is positive; otherwise zero default, with no spurious positive override','source_semantics_or_coefficients_changed':False,'original_state_record_peak_during_producer':1769616,'independent_audit_state_records':'only the new1,013,185 overrides plus small B-column counters; old positive coefficients streamed from immutable bytes','lookup':'base[b]+override.get(canonical(a,b),0), signed overrides allowed','source_queries':0,'source_engine_calls':0,'external_or_formal_proof_assistant_verification':False,'old_checked_pickle_sha256':oldpin,'input_sha256':{file.name:filepin,'native10_credit_certificate.json':hashlib.sha256(data).hexdigest(),'native10_source_actions.json':hashlib.sha256((B/'native10_source_actions.json').read_bytes()).hexdigest()},'principal_U33':'OPEN'});print(json.dumps({'status':'PASS_EXACT_MODAL_B_ORACLE','old':seen,'new':len(R),'zero_overrides':sum(zero_override),'source_queries':0}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify47_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
