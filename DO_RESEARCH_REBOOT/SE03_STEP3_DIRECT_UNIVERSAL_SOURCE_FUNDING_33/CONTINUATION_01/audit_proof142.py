"""Emit the prepared-family static construction at the audited actual control."""
import json,time,sys,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    S=json.loads((B/'core13_framed_activation_closed_source.json').read_text());M=json.loads((B/'framed_core13_full_matching.json').read_text())
    inverse={tuple(r['unit']):tuple(r['demand']) for r in M['full_pairs']};own={tuple(r['unit']):tuple(r['demand']) for r in M['natural_h0']};events=[];emitted=[];released=[]
    for row in S['period_rows']:
        for j in range(1,row['H']+1):
            units=[(row['absolute_t'],j,b) for b in (0,1)];actions=[]
            for u in units:
                if u in inverse:actions.append({'unit':u,'action':'emit_h0' if u in own else 'emit_seed','demand':inverse[u]});emitted.append({'demand':inverse[u],'unit':u})
                else:actions.append({'unit':u,'action':'release'});released.append(u)
            events.append({'occurrence':row['absolute_t'],'event_index':j,'buffer_before':0,'buffer_after_admit':2,'actions':actions,'buffer_after_resolve':0})
    assert len(emitted)==36 and len(released)==282 and len(events)==159 and time.process_time()-START<CAP-1
    out('prepared_frame_static_schedule.json',{'status':'EXPLICIT_PREPARED_CORE13_STATIC_BANK2_SCHEDULE','period':S['period'],'events':events,'full_pairs':emitted,'released_units':released,'working_peak':2,'all_event_boundaries_empty':True,'storage_contract':'original independent-h static within predecessor/critical blocks, not all-time endpoint storage','source_queries':0,'source_engine_calls':0,'principal_U33':'OPEN','input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('PREPARED_FRAME_STATIC_BANK25.md','core13_framed_activation_closed_source.json','framed_core13_full_matching.json','framed_family_repayment_independent_audit.json')}})
    print(json.dumps({'status':'PREPARED_STATIC_BANK2_SCHEDULE_EMITTED','events':159,'pairs':36,'released_units':282,'source_queries':0}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof142_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
