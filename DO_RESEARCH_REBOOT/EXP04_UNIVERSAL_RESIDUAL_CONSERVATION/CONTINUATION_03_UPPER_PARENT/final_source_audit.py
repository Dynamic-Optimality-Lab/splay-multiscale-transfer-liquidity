from delivery3_support import *
from independent_path_audit import check
from fast_physics import path_hull
from new_payments import intern_original_states
from accounting import audit
import gc


if __name__=='__main__':
    meter=Meter('all_sources_final');out=[];extra=[];sources,rows,_=collect();pool=intern_original_states()
    for s in sources:
        z=check(s);M={x for tag,x in s['operations'] if tag=='K'}
        assert path_hull(Tree(s['initial_B']),M)==set(int(k) for k in s['initial_B']['children'])
        z['S_is_entire_full_physical_population']=True;out.append(z)
        write('ALL_NEW_SOURCE_VERIFICATION.json',out)
        if s['name'] in ('C03_private_p4_d3_c4','C03_private_p5_d3_c1'):
            r=Replay(s);star,_,_=original_residual(r);assert star==rows[s['name']]['original_R_star']
            extra.append(audit(r,star));write('EXTRA_ORDERED_ACCOUNTING.json',extra)
            del r;pool.clear();gc.collect()
        print('PASS complete source',s['name'],flush=True)
    meter.success=True;meter.details.update(new_complete_sources=len(out),extra_ordered_original_audits=len(extra))
