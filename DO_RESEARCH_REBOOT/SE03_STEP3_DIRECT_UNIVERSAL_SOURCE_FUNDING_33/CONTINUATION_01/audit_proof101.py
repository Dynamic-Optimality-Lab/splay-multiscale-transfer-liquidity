"""Lossless modal-B representation. Mutate a loaded COPY, never frozen data.
Packed presence masks are compressed source-column data, not additional live
pair-state records. At every stage explicit coefficient records<=old count.
"""
import json,pickle,time,sys,hashlib,collections
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    raw=(B/'native10_debt_03.pkl').read_bytes();pin=hashlib.sha256(raw).hexdigest();receipt=json.loads((B/'native10_complete_independent_audit.json').read_text());assert pin==receipt['input_sha256'];L=pickle.loads(raw)['level'];del raw;original=len(L);Z=json.loads((B/'native10_source_actions.json').read_text());N=len(Z['trees']);roots=[t[0] for t in Z['trees']];mir=Z['mirror'];rootcounts=collections.Counter(roots);offset={g:roots.index(g) for g in range(1,11)};hist=[[0]*4 for _ in range(N)];present=[0]*N
    for code,d in L.items():
        a,b=divmod(code,N);g=roots[b];assert g==roots[a] and g<=5;hist[b][d]+=1;present[b]|=1<<(a-offset[g])
    mode=[0]*N;expected=0
    for b,g in enumerate(roots):
        if g>5:continue
        hist[b][0]=rootcounts[g]-sum(hist[b]);m=max(range(4),key=lambda d:(hist[b][d],-d));mode[b]=mode[mir[b]]=m;expected+=rootcounts[g]-hist[b][m]
    assert expected<=original
    for code in list(L):
        d=L[code];m=mode[code%N]
        if d==m:del L[code]
        else:L[code]=d-m
    zero_overrides=0
    for b,g in enumerate(roots):
        if g>5 or mode[b]==0:continue
        absent=((1<<rootcounts[g])-1)^present[b]
        while absent:
            bit=absent&-absent;local=bit.bit_length()-1;absent-=bit;code=(offset[g]+local)*N+b;assert code not in L;L[code]=-mode[b];zero_overrides+=1
    assert len(L)==expected<=original
    data={'status':'EXACT_MODAL_B_COEFFICIENT_REPRESENTATION_CANDIDATE','N':N,'base':mode,'residual':L,'original_nonzero_states':original,'old_sha256':pin,'lookup':'D10(a,b)=base[b]+residual.get(canon(a,b),0)','zero_override_count':zero_overrides,'mode_tie_break':'lowest value'}
    with (B/'native10_B_modal_factored_debt.pkl').open('xb') as f:pickle.dump(data,f,protocol=5)
    out('native10_B_modal_factoring_candidate.json',{'status':data['status'],'original_nonzero_states':original,'residual_states_including_zero_overrides':len(L),'zero_override_count':zero_overrides,'explicit_state_record_peak':original,'source_queries':0,'source_engine_calls':0,'old_sha256':pin,'factored_sha256':hashlib.sha256((B/'native10_B_modal_factored_debt.pkl').read_bytes()).hexdigest(),'principal_U33':'OPEN'});print(json.dumps({'status':'MODAL_B_FACTORED','old':original,'new':len(L),'zero_overrides':zero_overrides,'source_queries':0}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof101_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
