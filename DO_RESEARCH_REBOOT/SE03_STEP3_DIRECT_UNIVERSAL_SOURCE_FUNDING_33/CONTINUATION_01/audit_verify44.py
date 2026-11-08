"""Independent coefficient-export check of derived B envelopes, no sign rerun."""
import json,time,sys,hashlib,collections
from pathlib import Path
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    Z=json.loads((B/'native10_source_actions.json').read_text());E=json.loads((B/'native10_credit_certificate.json').read_text());N=len(Z['trees']);mir=Z['mirror'];count=[0]*N;low=[4]*N;high=[0]*N;bits=[0]*N;rootcounts=collections.Counter(t[0] for t in Z['trees'])
    for code,d in E['nonzero_debt']:
        a,b=divmod(code,N)
        for bb in (b,mir[b]):count[bb]+=1;low[bb]=min(low[bb],d);high[bb]=max(high[bb],d);bits[bb]|=1<<d
    for b,t in enumerate(Z['trees']):
        if count[b]<rootcounts[t[0]]:low[b]=0;bits[b]|=1
        assert count[b]<=rootcounts[t[0]]
    actual=json.loads((B/'native10_B_specific_envelopes.json').read_text());assert actual['low']==low and actual['high']==high and actual['value_spectra']==[[v for v in range(4) if bits[b]>>v&1] for b in range(N)];assert E['checked_input_pickle_sha256']==actual['basis_pickle_sha256'];assert time.process_time()-START<CAP-1
    out('native10_B_envelopes_independent_audit.json',{'status':'PASS_EXACT_B_SPECIFIC_COEFFICIENT_ENVELOPES','old_HIGH_sign_audit_reused_without_repetition':151164,'B_shapes':N,'positive_lower_bounds':sum(d>0 for d in low),'source_queries':0,'source_engine_calls':0,'not_a_new_full_source_sign_certificate':True,'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('native10_B_specific_envelopes.json','native10_credit_certificate.json','native10_complete_independent_audit.json')},'principal_U33':'OPEN'});print(json.dumps({'status':'PASS_B_SPECIFIC_ENVELOPES','B_shapes':N,'old_HIGH_rechecked':False,'source_queries':0}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify44_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
