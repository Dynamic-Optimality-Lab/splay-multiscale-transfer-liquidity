"""Independent source-time receipt: own units plus ONE carried spare.
Select the full packet cut before the chosen positive packet, then
transport BOTH demand/donor IDs through every fixed-period cut.
"""
import json,time
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    receipts=json.loads((B/'physical_receipts2.json').read_text());reports=[]
    for f in receipts['families']:
        rows={r['occurrence']:r for r in f['rows']};mm=f['macros'];start=f['seed_spare_macro']
        seed=tuple(f['seed_spare']);r=tuple(f['R']);paid={};carry=None;maximum=0;newtime=0;source_times={}
        for j in range(len(mm)):
            m=mm[(start+j)%len(mm)];own=[]
            for t in m['occurrences']:
                newtime+=1;source_times[t]=newtime
                # At an original KEEP, A replay is before B replay.
                for k in range(1,rows[t]['a']+1):
                    for b in (0,1):
                        u=(t,k,b)
                        if len(own)<min(m['Q'],2*m['H']):own.append(u)
                        elif u==seed:
                            assert carry is None;carry=u
                        maximum=max(maximum,len(own)+int(carry is not None))
                # The only positive full B-demand batch is the terminal one.
                for k in range(1,rows[t]['qF']+1):
                    d=(t,k)
                    if d==r:
                        assert carry is not None;paid[d]=carry;carry=None
                    else:
                        assert own;paid[d]=own.pop(0)
            assert not own
        assert carry is None and len(source_times)==len(rows)
        expected={tuple(v['demand']):tuple(v['unit']) for v in f['independent_h']};assert paid==expected
        assert all(source_times[u[0]]<=source_times[d[0]] for d,u in paid.items())
        assert maximum<=4
        for delta in range(len(rows)):
            tau=lambda t:t if t>delta else t+len(rows)
            mapped={(tau(d[0]),d[1]):(tau(u[0]),u[1],u[2]) for d,u in paid.items()}
            assert len(set(mapped.values()))==len(mapped)
            assert all(delta<t<=delta+len(rows) for t,j,b in mapped.values())
        reports.append({'reflected':f['reflected'],'source_cut_before_macro':start,
            'max_working_units':maximum,'one_carried_unit':True,'native_source_time_valid_at_this_cut':True,
            'fixed_aux_cut_transport':'both endpoints, no old assignment or source unit duplicated',
            'demand_count':len(paid)})
    out('source_stream_audit.json',{'status':'PASS_CAUSAL_INDEPENDENT_FULL_RECEIPT_AND_LEGAL_TRANSPORT',
        'reports':reports,'universal_working_bound':4,
        'bound_reason':'one carried bit plus at most Q<=3 selected own bits; all other actual bits remain reserve',
        'final_owner_exchange':'block/cyclic receipt on fixed I, no native chronology asserted for its relocated endpoint',
        'source_engine_calls':0,'new_finite_tests':2})
    print(json.dumps({'status':'PASS','reports':reports}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_stream_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0,'new_finite_tests':2})
