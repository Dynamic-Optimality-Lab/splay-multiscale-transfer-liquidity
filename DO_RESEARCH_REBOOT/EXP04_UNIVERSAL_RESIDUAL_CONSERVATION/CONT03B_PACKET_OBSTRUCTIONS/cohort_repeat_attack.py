from campaign3b import *
from accounting import audit
from new_payments import compact_trace,intern_original_states
from fast_physics import physical_replay
import gc


def construct(base,first,targets,name):
    piece=[];previous=12
    for x in targets:piece += [['D',x],['K',previous],['K',x]];previous=x
    s={k:v for k,v in base.items() if k not in ('A','Q_B','trace_hash','closing_A','closing_B')}
    s.update(name=name,family='cohort_outer_birth_then_even_depth_same_g_repeat',
        operations=base['operations'][:first]+piece+base['operations'][first:],
        packet_target_operations=[first]+[first+3*(k+1) for k in range(len(targets))],
        inserted_packet_targets=targets)
    return s


def run(s):
    f=physical_replay(s);r=Replay(s);star,_,_=original_residual(r);a=audit(r,star)
    s.update(A=r.A,Q_B=r.Q,trace_hash=digest(r.events),closing_A=r.a.state(),closing_B=r.b.state())
    parents={tuple(e['original_parent']) for e in a['C_after_frozen_and_prefix']}
    row={'source':s['name'],'population':len(r.keys),'A':r.A,'Q_B':r.Q,'original_R_star':star,
        'original_Pi_classification':True,'ordered_accounting':a,'independent_original_operations':r.independent_checks,
        'packet_R6_pairs':[p for p in r.pairs if p['class']=='R6' and p['rho'][0] in s['packet_target_operations']],
        'original_C_parent_certificates':[{'parent':list(p),'U':r.U[p],
            'pre_A_path':r.boundaries[p[0]-1]['A_path'],'pre_B_path':r.boundaries[p[0]-1]['B_path'],
            'A_gap':keep_gaps(r)[p[0]]['A']} for p in sorted(parents)],
        'R_upper_escape_claimed':False}
    row['all_original_packet_pairs']=[p for p in r.pairs if p['rho'][0] in s['packet_target_operations']]
    unpaid=a['first_use_E_C']['repeat_original_gaps']+a['first_use_E_C']['A_demotion_free_key_original_gaps']
    if unpaid:
        trace_file=f'PACKET_TRACE_{digest(s["name"])[:10]}.json'
        compact_trace(r,star,trace_file);row['trace_file']=trace_file
        row['unpaid_C_demands']=unpaid
    return r,row


if __name__=='__main__':
    meter=Meter('cohort_repeat_attack');sources=[];results=[];pool=intern_original_states()
    base=json.loads((C2/'PRIVATE_ANCESTOR_SOURCES.json').read_text())[0]
    for x in (60,78,90):
        s=construct(base,646,[24,x],f'C3B_cohort_repeat24_{x}')
        r,z=run(s);sources.append(s);results.append(z)
        write('COHORT_SOURCES.json',sources);write('COHORT_RESULTS.json',results)
        print(s['name'],'Rstar',len(z['original_R_star']),'C',len(z['ordered_accounting']['C_after_frozen_and_prefix']),
            'C repeats',len(z['ordered_accounting']['first_use_E_C']['repeat_original_gaps']),flush=True)
        found=bool(z.get('unpaid_C_demands'));del r;pool.clear();gc.collect()
        if found:break
    meter.success=True;meter.details['new_original_sources']=len(sources)
