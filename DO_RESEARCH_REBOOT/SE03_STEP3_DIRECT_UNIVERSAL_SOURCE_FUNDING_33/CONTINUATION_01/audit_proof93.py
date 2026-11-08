"""Derive exact old B-specific envelopes; no old sign checks repeated."""
import json,pickle,hashlib,time,sys,collections
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    native=json.loads((B/'native10_source_actions.json').read_text());roots=[t[0] for t in native['trees']];N=len(roots);mir=native['mirror'];raw=(B/'native10_debt_03.pkl').read_bytes();receipt=json.loads((B/'native10_complete_independent_audit.json').read_text());pin=hashlib.sha256(raw).hexdigest();assert pin==receipt['input_sha256'];level=pickle.loads(raw)['level'];del raw;hist=[collections.Counter() for _ in roots];counts=collections.Counter(roots)
    for code,d in level.items():
        a,b=divmod(code,N);assert roots[a]==roots[b] and b!=mir[b];hist[b][d]+=1;hist[mir[b]][d]+=1
    low=[];high=[];spectra=[]
    for b,v in enumerate(hist):
        assert sum(v.values())<=counts[roots[b]];missing=sum(v.values())<counts[roots[b]];low.append(0 if missing else min(v));high.append(max(v,default=0));spectra.append(sorted(set(v)|({0} if missing else set())))
    out('native10_B_specific_envelopes.json',{'status':'EXACT_OLD_COEFFICIENT_ENVELOPES_DERIVED','low':low,'high':high,'value_spectra':spectra,'basis_pickle_sha256':pin,'complete_HIGH_audit_reused':'native10_complete_independent_audit.json','source_queries':0,'source_engine_calls':0,'not_new_source_sign_checks':True});print(json.dumps({'status':'B_SPECIFIC_ENVELOPES_DERIVED','trees':N,'nonzero_lower_bounds':sum(v>0 for v in low),'old_HIGH_checks_reused':151164}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof93_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
