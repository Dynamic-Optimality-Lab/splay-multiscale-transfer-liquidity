import json,time,hashlib
from pathlib import Path
from certified_source_composer import Composer
B=Path(__file__).resolve().parent
def main():
    c=Composer();f=json.loads((B/'positive_deficit_inventory_source_candidate.json').read_text())['failure'];z=c.compile(f['A'],f['B'],f['DELETE_helper_or_0'],f['KEEP_target']);assert (z['H'],z['Q'])==(1,3) and 2*z['A']>=z['QF'];z.update(status='CLOSED_SOURCE_UNCHANGED_DEFICIT_INVENTORY_REFUTATION_CANDIDATE',inventory_failure=f,new_source_queries=0,new_source_engine_calls=0,source_method='composition of accepted ordinary primitive identities, not fresh kernel replay',principal_U33='OPEN',input_sha256={n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('positive_deficit_inventory_source_candidate.json','native10_source_actions.json','native10_source_independent_audit.json','certified_source_composer.py')})
    with (B/'positive_deficit_inventory_closed_source.json').open('x') as out:json.dump(z,out,indent=2)
    print(json.dumps({k:z[k] for k in ('status','period','natural_packet','H','Q','A','QF')}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_proof56_exit.json').open('x') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
