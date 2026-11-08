"""Explicit full donor receipts for the NEW specified free-gap families.
Not a universal six-key allocator. The family gap repair is source-derived;
unknown arbitrary-history availability remains explicitly unproved.
"""
import json,time
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    data=json.loads((B/'deficient_source_schemas.json').read_text());cert=[]
    for fam in data['families']:
        units=[];demands=[]
        for row in fam['rows']:
            units += [(row['occurrence'],j,b) for j in range(1,row['a']+1) for b in (0,1)]
            demands += [(row['occurrence'],j) for j in range(1,row['qF']+1)]
        packets=fam['packets'];h={};bad=[];spare={};packet_units={};packet_demands={}
        for i,packet in enumerate(packets):
            uu=[u for t in packet['occurrences'] for u in units if u[0]==t]
            dd=[d for t in packet['occurrences'] for d in demands if d[0]==t]
            packet_units[i]=uu;packet_demands[i]=dd
            if len(dd)>len(uu):bad.append(i)
            else:
                h.update(zip(dd,uu));spare[i]=uu[len(dd):]
        repairs=[]
        for i in bad:
            uu=packet_units[i];dd=packet_demands[i];h.update(zip(dd,uu))
            unpaid=dd[len(uu):];prev=(i-1)%len(packets)
            assert prev in spare and len(spare[prev])>=len(unpaid)
            borrowed=spare[prev][-len(unpaid):];spare[prev]=spare[prev][:-len(unpaid)]
            h.update(zip(unpaid,borrowed))
            repairs.append({'bad_packet':i,'previous_actual_packet':prev,'demands':unpaid,'actual_donors':borrowed,
                'previous_H':packets[prev]['H'],'previous_Q':packets[prev]['Q'],
                'previous_source_occurrences':packets[prev]['occurrences']})
        assert set(h)==set(demands) and len(set(h.values()))==len(demands)
        assert set(h.values())<=set(units)
        cert.append({'name':fam['name'],'core':fam['core'],'period_length':len(fam['word']),
            'full_demands':demands,'all_A_units':units,'full_allocation':[{'demand':d,'unit':u} for d,u in sorted(h.items())],
            'surplus_units':sorted(set(units)-set(h.values())),'repairs':repairs,
            'ownership':'independent full map h, not a claim these units are free under fixed fE',
            'transport':'relative labels; replicate distinct original copies then biject BOTH endpoint IDs into the actual aligned Step1 period'})
    out('family_funding_receipts.json',{'status':'COMPLETE_ONLY_FOR_SIX_NEW_SPECIFIED_SOURCE_FAMILIES',
        'families':cert,'full_CD6':'OPEN','universal_nearest_predecessor_rule':'NOT_PROVED',
        'fixed_fE_preservation':'uniform exchange theorem applies IF an actual fixed map on the same interval is supplied; no numerical sealed fE invented'})
    print(json.dumps({'status':'PASS_RESTRICTED_SOURCE_RECEIPTS','families':len(cert),
        'repairs':sum(len(v['repairs']) for v in cert),'physically_funded_demands':sum(len(v['full_demands']) for v in cert)}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_funding_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0,'new_finite_tests':0})
