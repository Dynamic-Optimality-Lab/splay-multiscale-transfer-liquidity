from base6 import *
from physical1 import Edges
from cohortc import decode_state

# These are the original frozen functions, used without changing their code.
sys.path.insert(0,str(BASE/'CONTINUATION_01_COVERAGE_PROOF'))
import core as interval_core
import return_normalization as norm
import gap_payment as hard
assert Path(interval_core.__file__).resolve().parent==BASE/'CONTINUATION_01_COVERAGE_PROOF'

def costs(r,u,v):
    N=len(r.ops);start=u[0]%N;end=v[0]-1
    assert start<=end # Fresh tests are within one original period.
    ts=list(range(start+1,end+2));initial=r.boundaries[start]['pre_B']
    raw=interval_core.interval_cost(r.boundaries,initial,start,end)
    G=norm.guarded_skeleton(r,ts);H=hard.hard_guarded(r,ts)
    return {'operations':ts,'A_original':raw['A'],'threshold_5A':5*raw['A'],
        'raw':raw,'G':G,'H':H,'all_three_natural_interval_prices_exceed_5A':min(raw['D'],G['D'],H['D'])>5*raw['A']}

def renewal_geometry(s,p,rn,r):
    ds={tuple(z['parent']):z for z in p['doubles']};out=[];T=len(p['events'])
    for z in rn['canonical_renewals']:
        u,v=tuple(z['earlier_parent']),tuple(z['later_parent']);g=z['old_g']
        lo=p['boundaries'][u[0]-1]['end_time'];hi=p['boundaries'][v[0]-1]['post_A_time']
        off=z['earlier_lap_offset'];span=list(range(lo,hi)) if off==0 else list(range(lo,T))+list(range(hi))
        Aevents=[p['events'][i] for i in span if p['events'][i]['actor']=='A']
        Bpromos=[p['events'][i] for i in span if p['events'][i]['actor']=='B' and p['events'][i]['promoted']==g]
        assert not any(e['pivot']==g or e['promoted']==g for e in Aevents)
        F=Edges(decode_state(p,p['boundaries'][v[0]-1]['pre_B_state'])).m[g]
        Ju=Edges(decode_state(p,p['boundaries'][u[0]-1]['post_B_state'])).m[g]
        Fu=Edges(decode_state(p,p['boundaries'][u[0]-1]['pre_B_state'])).m[g]
        au=Edges(decode_state(p,p['boundaries'][u[0]-1]['post_A_state'])).component(g)
        av=Edges(decode_state(p,p['boundaries'][v[0]-1]['post_A_state'])).component(g)
        assert au==av
        pf=not Bpromos
        if pf:assert F&~Ju==0 and Ju&~Fu==0 and Ju!=Fu
        later_rhos=z['later_original_C_old_rhos']
        assert later_rhos and all(list(v)==list(e['original_parent']) for e in r.original_R_star if e['rho'] in later_rhos)
        local=costs(r,u,v) if off==0 and u[0]<v[0] else None
        out.append({**z,'promotion_free':pf,'intervening_B_promotion_ids':[e['id'] for e in Bpromos],
            'full_F_u':Fu,'full_J_u':Ju,'full_F_v':F,'equality_F_v_J_u':F==Ju,
            'full_A_component_sha256':digest(au),'local_natural_interval':local,
            'scope':'Canonical ORIGINAL C_old renewal before hybrid/quota; actual residual tracked separately.'})
    return out
