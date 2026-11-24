from compulsory_core import *
from itertools import product


if __name__=='__main__':
    meter=Meter('compulsory_core_exhaustive_model_check');families=cuts=0
    for T in range(1,7):
        for prefix in product(range(3),repeat=T-1):
            states=list(prefix)+( [0] )
            for mask in range(1<<T):
                rows=[{'tag':'K','x':i+1,'B_code':states[i],
                       'guard_H':bool(mask>>i&1),'guard_G':bool(mask>>i&1) or i%2==0} for i in range(T)]
                f={'rows':rows};z=compulsory(f);mandatory=set(z['mandatory_original_KEEP'])
                erasable=set()
                for start in range(T):
                    old=states[(start-1)%T]
                    for length in range(1,T+1):
                        ids=[(start+j)%T for j in range(length)]
                        if any(rows[i]['guard_H'] for i in ids):continue
                        if states[ids[-1]]==old:erasable.update(i+1 for i in ids)
                assert mandatory==set(range(1,T+1))-erasable
                for cut in range(T):
                    for variant in ('H','G'):
                        ids=skeleton_indices(f,cut,variant);retained={i+1 for i in ids}
                        assert mandatory<=retained
                        actual=periodic_cost([rows[i]['x'] for i in ids],set(range(1,T+1)))
                        assert actual['B_cyclic']>=z['cyclic_cost_lower_bound']
                    cuts+=1
                families+=1
    c=json.loads((ROOT/'COMPULSORY_RETURN_CORE_CERTIFICATE.json').read_text())
    r=json.loads((ROOT/'ADAPTIVE_LIFT_RESULTS.json').read_text())
    best=min(r['variants'],key=lambda z:z['B_cyclic'])
    assert best['B_cyclic']==c['cyclic_cost_lower_bound']
    write('PERIODIC_OPTIMUM_CERTIFICATE.json',{'source':r['source'],'A':r['A'],
        'minimum_over_all_permitted_full_period_cuts_and_raw_G_H_variants':best['B_cyclic'],
        'cut1_variant_attaining_lower_bound':best['variant'],'proof':'compulsory target subsequence gives a cut-independent lower bound; the named actual comparison attains it',
        'eligible_periodic':best['B_cyclic']<=10*r['A'],'original_R_next_P_empty_by_inherited_periodic_theorem':True,
        'qualification':'No original Pi enumeration for this large screened source; the universal inherited payment theorem makes enumeration unnecessary for rejecting this alleged escape.'})
    write('COMPULSORY_MODEL_VERIFICATION.json',{'cyclic_guarded_state_models':families,'cuts_checked':cuts,
        'state_alphabet':3,'maximum_period':6,'brute_force_all_guard_free_return_arcs_match_linear_union':True,
        'mandatory_points_retained_by_every_G_H_cut':True,'cyclic_metric_lower_bound_verified':True,
        'scope':'Finite implementation verification; source-uniform proof is separate C2.'})
    print('PASS',families,'state/guard models and',cuts,'cuts',flush=True);meter.success=True
