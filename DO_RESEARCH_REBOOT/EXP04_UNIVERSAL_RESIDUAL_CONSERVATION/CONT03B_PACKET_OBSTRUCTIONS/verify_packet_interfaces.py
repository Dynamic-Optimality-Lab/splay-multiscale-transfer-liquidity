from delivery_support3b import *
from packet_payments import test
from fast_physics import physical_replay


if __name__=='__main__':
    meter=Meter('packet_interfaces');sources,rows,_=collect();out=[]
    for s in sources:
        row=rows[s['name']]
        if not row.get('original_Pi_classification',row.get('full_original_Pi_classification',False)):continue
        a=row['ordered_accounting'];star=row['original_R_star'];f=physical_replay(s)
        F={digest(e['rho']) for key in ('1_frozen_carrier','2_frozen_skipped_rank') for e in a['ordered_original_assignments'][key]}
        E={digest(e['rho']) for e in a['first_use_E_C']['selected_original_gaps']}
        H={digest(e['rho']) for e in star if f['rows'][e['consumer']-1]['q']>2*f['rows'][e['consumer']-1]['A_gap']}
        assert a['positive_old_periodic_certificate']['eligible_periodic']
        D=[e for e in star if digest(e['rho']) not in F|E|H];q=test(s,D)
        selected={digest(rho) for z in q['selected_parent_allocations'] for rho in z['original_gaps']}
        P={digest(e['rho']) for e in a['ordered_original_assignments']['3_original_B_prefix']}
        assert P-(F|E|H)<=selected
        assert not q['literal_overflow']
        out.append({'source':s['name'],'generic_pre_hybrid_C_payment':test(s,a['C_after_frozen_and_prefix']),
            'P3_D_after_F_E_H':D,'P3_quota_payment':q,'old_prefix_containment_verified':True,
            'qualification':'Exact finite implementation checks; source-uniform budgets are the analytic P1-P3 proofs.'})
    assert len(out)==13
    write('PACKET_INTERFACE_VERIFICATION.json',out)
    print('PASS13 exact original-demand packet interfaces; old prefix containment and real StepEv donors; no universal fit inferred',flush=True)
    meter.success=True
