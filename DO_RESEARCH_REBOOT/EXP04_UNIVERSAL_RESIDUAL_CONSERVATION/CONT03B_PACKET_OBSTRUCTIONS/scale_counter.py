from campaign3b import *
from private_scaling import construct as base_source
from cohort_repeat_attack import run
from new_payments import intern_original_states


if __name__=='__main__':
    meter=Meter('scaled_counter_control');pool=intern_original_states();d=11
    base=base_source(4,stride=d);first=4*d;outside=8*d;aux=13*d+1;x=13*d+3
    piece=[['D',outside],['K',first],['K',outside],['D',aux],['D',x],['K',outside],['K',x]]
    s={k:v for k,v in base.items() if k not in ('A','Q_B','trace_hash','closing_A','closing_B')}
    s.update(name='C3B_counter_d11',family='parametric_fenced_cohort_repeat',
        operations=base['operations'][:646]+piece+base['operations'][646:],packet_target_operations=[646,649,653],
        parametric_family={'d':d,'legal_domain':'odd d>=3','physical_population':'64d+1',
            'primary_private_target':'4d','outside_cohort_target':'8d','A_helper':'13d+1','second_target':'13d+3',
            'universal_claim':'Legal operations and exact paired restoration only; original Pi counterexample status is verified per instance.'})
    r,z=run(s);write('SCALED_SOURCE.json',s);write('SCALED_RESULT.json',z)
    print('scaled d11 N',len(r.keys),'A',r.A,'Rstar',len(z['original_R_star']),
        'C repeats',len(z['ordered_accounting']['first_use_E_C']['repeat_original_gaps']),
        'old periodic funded',z['ordered_accounting']['positive_old_periodic_certificate'] is not None,flush=True)
    meter.success=True
