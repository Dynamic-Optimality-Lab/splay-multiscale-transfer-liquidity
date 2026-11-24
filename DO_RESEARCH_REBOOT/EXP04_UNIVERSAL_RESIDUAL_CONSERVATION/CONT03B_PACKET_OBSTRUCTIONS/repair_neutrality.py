from cohort_repeat_attack import construct,run
from campaign3b import *
from new_payments import intern_original_states
import gc


if __name__=='__main__':
    meter=Meter('repair_neutrality');pool=intern_original_states();sources=[];results=[]
    base=json.loads((C2/'PRIVATE_ANCESTOR_SOURCES.json').read_text())[0]
    for helper in (40,34,46,58):
        s=construct(base,646,[24,60],f'C3B_repair_A_{helper}')
        assert s['operations'][649]==['D',60]
        s['operations']=s['operations'][:649]+[['D',helper]]+s['operations'][649:]
        s['packet_target_operations']=[646,649,653];s['actual_auxiliary_DELETE']=helper
        r,z=run(s)
        sourceall=[p for p in r.pairs if p['rho'][0]==653]
        z['second_hit_pair_classes']=[{'rho':p['rho'],'class':p['class'],'parent':p['parent'],
            'old_g':r.doubles[tuple(p['parent'])]['g'],'parent_signs':r.doubles[tuple(p['parent'])]['signs']} for p in sourceall]
        sources.append(s);results.append(z);write('NEUTRALITY_SOURCES.json',sources);write('NEUTRALITY_RESULTS.json',results)
        unpaid=z['ordered_accounting']['first_use_E_C']['repeat_original_gaps']
        print(s['name'],'Rstar',len(z['original_R_star']),'C',len(z['ordered_accounting']['C_after_frozen_and_prefix']),
            'C repeats',len(unpaid),'second g52 signs',r.doubles.get((653,3),{}).get('signs'),flush=True)
        del r;pool.clear();gc.collect()
        if z.get('unpaid_C_demands'):break
    meter.success=True;meter.details['new_original_sources']=len(sources)
