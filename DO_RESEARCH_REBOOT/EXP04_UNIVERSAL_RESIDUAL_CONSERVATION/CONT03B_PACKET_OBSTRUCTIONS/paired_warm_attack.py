from warm_untouched import make,physical_screen,audit_general
from campaign3b import *
from new_payments import compact_trace
import gc


if __name__=='__main__':
    meter=Meter('paired_warm_attack');sources=[];results=[];failed=[];full=0
    for n in (49,97):
        for seed in range(1,49):
            s,fail=make(n,seed,96,mode='pairs')
            if fail:failed.append(fail);continue
            z=physical_screen(s);s.update(A=z['A'],Q_B=z['Q_B']);sources.append(s)
            row={'source':s['name'],'population':n,**z,'full_original_Pi_classification':False}
            if z['targeted_upper_candidates'] and full<24:
                r=Replay(s);star,_,_=original_residual(r);a=audit_general(r,star);full+=1
                row.update(full_original_Pi_classification=True,original_R_star=star,ordered_accounting=a,
                    original_R6_count=r.counts['R6'],all_original_pair_classes=dict(r.counts),
                    independent_original_operations=r.independent_checks)
                s.update(trace_hash=digest(r.events),closing_A=r.a.state(),closing_B=r.b.state())
                unpaid=a['epoch_unpaid_original_C']
                if unpaid:compact_trace(r,star,'PAIRED_COUNTEREXAMPLE_TRACE.json');row['trace_file']='PAIRED_COUNTEREXAMPLE_TRACE.json'
                print(s['name'],'S',len(r.S),'unmarked candidates',len(z['targeted_upper_candidates']),
                      'R6',r.counts['R6'],'Rstar',len(star),'C',len(a['C_after_frozen_and_prefix']),
                      'epoch-unpaid',len(unpaid),flush=True)
                del r;gc.collect()
            results.append(row);write('PAIR_SOURCES.json',sources);write('PAIR_RESULTS.json',results)
            write('PAIR_INCOMPLETE_PROTOTYPES.json',failed)
            if row.get('ordered_accounting',{}).get('epoch_unpaid_original_C'):
                meter.success=True;meter.details.update(complete_sources=len(sources),full_original_oracles=full);sys.exit(0)
            if full>=24:break
        if full>=24:break
    meter.success=True;meter.details.update(complete_sources=len(sources),full_original_oracles=full)
