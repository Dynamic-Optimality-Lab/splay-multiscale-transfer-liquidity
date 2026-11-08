"""Dedicated common-excess/blocker case on actual certified source IDs.
The lock placement is an adversarial logical fixture, not invented fE.
"""
import importlib.util,json,time
from pathlib import Path
from single_slot_allocator import independent_full,extend_one
B=Path(__file__).resolve().parent
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def pack(m):return [{'demand':d,'unit':u} for d,u in sorted(m.items())]
def main():
    f=json.loads((B/'physical_receipts2.json').read_text())['families'][0]
    build=independent_full(f['rows']);r=build['R'];h0=build['h0'];D,U=build['D'],build['U']
    # Prefix-ordinal common set at the critical actual occurrence, including r.
    C={d for d in D if d[0]==r[0]};p=min(D-C)
    l={d:h0[d] for d in C-{r}};l[r]=h0[p]
    spec=importlib.util.spec_from_file_location('partial10',B.parent/'SE03_STEP2_FULL_FUNDING_CLOSURE_10/physical_exchange.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    prior=m.exchange(D,U,l,h0)
    assert prior['uncovered']=={p} and prior['blocked'][p]['owner']==r
    a=prior['allocation'];ex=extend_one(D,U,a,build['h'])
    assert ex['missing']==p and p!=r and ex['unit'] not in set(a.values())
    assert len(ex['path'])==2 and all(ex['allocation'][d]==u for d,u in a.items())
    out('blocked_common_case.json',{'status':'PASS_BLOCKED_OTHER_ROOT_WITH_COMMON_EXCESS_ANCHOR',
        'fixture_scope':'logical injective common lock placement on actual source IDs; not a numerical sealed fE or source-realizability claim',
        'common_locks':pack(l),'original_partial_a':pack(a),'Pstar':p,'R':r,'actual_anchor':prior['blocked'][p]['owner'],
        'extension_path':ex['path'],'new_unit':ex['unit'],'final':pack(ex['allocation']),
        'all_previously_paid_values_fixed':True,'new_finite_tests':1,'source_engine_calls':0})
    print(json.dumps({'status':'PASS_BLOCKED_COMMON_ANCHOR_CASE','Pstar':p,'R':r,'path':ex['path']}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_blocked_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0,'new_finite_tests':1})
