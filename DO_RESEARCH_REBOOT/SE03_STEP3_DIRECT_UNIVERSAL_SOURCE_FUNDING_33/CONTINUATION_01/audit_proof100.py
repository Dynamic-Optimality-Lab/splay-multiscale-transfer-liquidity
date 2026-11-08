"""Lossless B-floor factoring of the immutable native-ten certificate.
Transforms a loaded copy IN PLACE; original file and coefficients stay frozen.
"""
import json,pickle,time,sys,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    old=B/'native10_debt_03.pkl';raw=old.read_bytes();pin=hashlib.sha256(raw).hexdigest();receipt=json.loads((B/'native10_complete_independent_audit.json').read_text());assert pin==receipt['input_sha256'];L=pickle.loads(raw)['level'];del raw;original=len(L);Z=json.loads((B/'native10_source_actions.json').read_text());N=len(Z['trees']);mir=Z['mirror'];envelopes=B/'native10_B_specific_envelopes.json';E=json.loads(envelopes.read_text());check=json.loads((B/'native10_B_envelopes_independent_audit.json').read_text());assert check['input_sha256']['native10_B_specific_envelopes.json']==hashlib.sha256(envelopes.read_bytes()).hexdigest();base=E['low'];assert all(base[b]==base[mir[b]] for b in range(N))
    for code in list(L):
        b=code%N;d=L[code];assert d>=base[b]
        if d==base[b]:del L[code]
        else:L[code]=d-base[b]
    record={'status':'LOSSLESS_OLD_DEBT_B_FLOOR_FACTOR_CANDIDATE','base':base,'residual':L,'N':N,'old_coefficient_count':original,'old_sha256':pin,'envelope_sha256':hashlib.sha256(envelopes.read_bytes()).hexdigest(),'state_code':'same accepted simultaneous-reflection canonical code','semantics':'D10(a,b)=base[b]+residual.get(canon(a,b),0) on all synchronized states'}
    with (B/'native10_B_floor_factored_debt.pkl').open('xb') as f:pickle.dump(record,f,protocol=5)
    out('native10_B_floor_factoring_candidate.json',{'status':record['status'],'original_nonzero_states':original,'residual_nonzero_states':len(L),'factored_B_values':N,'maximum_unique_loaded_coefficient_states':original,'no_original_semantics_or_coefficients_changed':True,'source_queries':0,'source_engine_calls':0,'old_sha256':pin,'factored_file_sha256':hashlib.sha256((B/'native10_B_floor_factored_debt.pkl').read_bytes()).hexdigest(),'all_missing_states_argument':'Any B with positive base has no missing compatible A by the independently checked exact envelope counts. All other omitted states have base=residual=0.','principal_U33':'OPEN'});print(json.dumps({'status':'B_FLOOR_FACTORED','original':original,'residual':len(L),'source_queries':0}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof100_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
