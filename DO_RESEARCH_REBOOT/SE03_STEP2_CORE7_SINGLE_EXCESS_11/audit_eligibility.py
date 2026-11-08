"""Old successful-path stability under one-edge completion, exact common set.
This checks the LICENSED original C exchange equals old a plus one endpoint.
"""
import collections,importlib.util,itertools,json,time
from pathlib import Path
from single_slot_allocator import extend_one
B=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('partial10_license',B.parent/'SE03_STEP2_FULL_FUNDING_CLOSURE_10/physical_exchange.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def allmaps(D,U):
    for k in range(len(D)+1):
        for ds in itertools.combinations(D,k):
            for us in itertools.permutations(U,k):yield dict(zip(ds,us))
def main():
    D=(0,1,2);U={0,1,2,3};locks=list(allmaps(D,tuple(sorted(U))));count=0;branches=collections.Counter()
    for hu in itertools.permutations(sorted(U),len(D)):
        h=dict(zip(D,hu))
        for r in D:
            h0={d:u for d,u in h.items() if d!=r}
            assert h[r] not in set(h0.values())
            for l in locks:
                prior=m.exchange(D,U,l,h0);licensed=m.exchange(D,U,l,h)
                extension=extend_one(D,U,prior['allocation'],h)
                assert licensed['total'] and not licensed['blocked']
                assert licensed['allocation']==extension['allocation']
                assert all(licensed['allocation'][d]==u for d,u in prior['allocation'].items())
                oldpaths={v['root']:v for v in prior['paths']}
                newpaths={v['root']:v for v in licensed['paths']}
                for p,v in oldpaths.items():assert newpaths[p]==v
                missing=prior['uncovered']
                if not missing:branches['empty']+=1
                else:
                    p=next(iter(missing));branches['p_equals_r' if p==r else 'blocked_other_at_common_r']+=1
                    assert newpaths[p]['terminal_unit']==extension['unit']
                count+=1
    assert count==5256 and all(branches[k]>0 for k in ('empty','p_equals_r','blocked_other_at_common_r'))
    out('eligibility_exchange_audit.json',{'status':'PASS_EXACT_INHERITED_COMMON_EXCHANGE_AND_ALL_OLD_PATHS_STABLE',
        'cases':count,'branches':dict(branches),'exact_common_set_preserved':True,
        'all_old_successful_paths_identical':True,'licensed_full_exchange_equals_one_pair_extension':True,
        'universal_proof':'old successful h0/l paths avoid r; h equals h0 there; complete exchange disjointness preserves all endpoints',
        'scope':'actual supplied fE common claims, no invented auxiliary execution or enlarged eligibility policy',
        'test_scope':'small injective-map regressions; universal source proof is path stability, not extrapolation',
        'new_finite_tests':count,'source_engine_calls':0})
    print(json.dumps({'status':'PASS_EXACT_ELIGIBILITY_RECEIPT','cases':count,'branches':dict(branches)}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_eligibility_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0,'new_finite_tests':5256})
