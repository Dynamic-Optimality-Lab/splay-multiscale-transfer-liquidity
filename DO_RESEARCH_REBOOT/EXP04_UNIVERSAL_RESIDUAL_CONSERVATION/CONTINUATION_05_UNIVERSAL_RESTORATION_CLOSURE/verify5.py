from stage5 import *
from fast_physics import physical_replay,decode
from independent_Pi3 import check as check_pi
from independent_cohorts import verify as check_cohorts
from ledger5 import audit
from forest5 import forest
import exp02_distortion,exp02_frame_bridge,exp03_core,exp04_core
# Primary selectors write diagnostics only inside the new research folder.
for mod in [exp02_distortion,exp02_frame_bridge,exp03_core,exp04_core]:mod.ROOT=ROOT

def opposite_geometry(s,f):
    a,b=f['rows'][:2];x,y=s['critical_targets'];k=s['k']
    first={g for typ,p,g,sgn in a['B_steps'] if g is not None}
    second={g for typ,p,g,sgn in b['B_steps'] if g is not None}
    common=sorted(first&second);assert len(common)==k//2 and first==set(range(1,k+1))
    assert all(c in ('LR','RL') for c,p,g,sgn in a['B_steps'])
    assert all(c=='RR' for c,p,g,sgn in b['B_steps'] if g in common)
    assert (a['a'],b['a'])==(1,1)
    st=decode(a['B_code'],2*k+2);B=inherited.Tree(st)
    path=B.path(y);assert path==[x]+list(range(1,k+1))+[y]
    # No B operation intervenes; this very full tree is the next pre-B state.
    assert set(common)<=set(path[:-1])
    first_ids={g:[1,j] for j,(c,p,g,s) in enumerate(a['B_steps'],1) if g in common}
    second_ids={g:[2,j] for j,(c,p,g,s) in enumerate(b['B_steps'],1) if g in common}
    return {'first_operation':1,'second_operation':2,'first_target':x,'second_target':y,
        'first_opposite_grandparents':sorted(first),'reused_grandparents':common,
        'reused_count':len(common),'actual_A_gap_StepEv':1,'B_ancestry_gains_between_B_phases':0,
        'next_pre_B_path':path,'complete_first_post_B_tree':st,
        'common_forest_edges':[{'old_g':g,'predecessor':first_ids[g],'successor':second_ids[g]}
                               for g in common],
        'only_A_StepEv_in_all_these_causal_spans':['A',2,1],
        'minimum_local_causal_span_congestion':len(common),
        'candidate_violated':'At least k-1 intervening B gains when k old grandparents are reused at one later KEEP, for all orientations.'}

def mass_geometry(r,s):
    keys=set(s['private_actual_marked_keys']);assert keys<=r.M
    out=[]
    for h in s['critical_operation_indices']:
        d=r.doubles[h,2];first=r.events[d['events'][0]-1];second=r.events[d['events'][1]-1]
        assert d['g']==18 and d['case']=='LL' and d['signs']==[0,0]
        assert first['promoted']==10==second['pivot']
        assert len(first['lost'])==1
        gains=set(r.label_keys(d['F']&~first['lost'][0]))
        assert keys<=gains<=set(r.label_keys(second['demoted_label']))
        after=inherited.Tree(r.boundaries[h-1]['post_B']);assert keys<=set(r.label_keys(after.labels(r.bits)[10]))
        if h>s['body_length']:assert (h,2) in r.U
        out.append({'original_parent':[h,2],'gain_bit':first['id'],'promoted_key':10,
                    'persistent_marked_gain_keys':sorted(gains),'added_private_gain_keys':sorted(keys),
                    'original_U':(h,2) in r.U,'neutral_signs':d['signs']})
    return {'critical_restorations':out,'counted_gain_mass_lower_bound':s['m']*s['m'],
        'counted_class':'Persistent genuine-marked descendant gains, first bit of fully neutral same-side doubles whose original frame is in U, using only interior body copies.',
        'gains_not_required_to_be_used_by_a_future_overflow_parent':True}

if __name__=='__main__':
    meter=Meter('verify');out=[];ledgers=[];forests=[]
    for s in load(ROOT/'SOURCE_WITNESSES.json'):
        f=physical_replay(s);name=s['name']
        z={'source':name,'source_sha256':digest(s),'full_original_Pi':False}
        if s['family']=='opposite_retained_columns':z.update(opposite_geometry(s,f))
        if len(s['initial_B']['children'])<100:
            r=inherited.Replay(s);assert (r.A,r.Q)==(s['A'],s['Q_B'])
            assert r.S==r.M==set(range(1,len(s['initial_B']['children'])+1))
            cp=check_pi(r);co=check_cohorts(r)
            star,_,_=inherited.original_residual(r)
            z.update(full_original_Pi=True,original_R_star=star,original_R6=r.counts['R6'],
                original_U=len(r.U),original_event_sha256=digest(r.events),
                immutable_primitive_check=cp,independent_cohort_R6_check=co)
            ft=forest(r);forests.append({'source':name,**ft})
            if s['family']=='opposite_retained_columns':
                ids=[p for p in r.doubles if p[0] in (1,2)]
                z['diagnostic_pool_scope']='All physical doubles at the two critical KEEPs only, not D.'
            elif s['family']=='marked_neutral_persistent_gain_mass':
                z.update(mass_geometry(r,s));ids=list(r.doubles)
                z['diagnostic_pool_scope']='All original physical B doubles, not D.'
            elif s['family']=='one_column_strict_containment_chain':
                k=s['k'];ids=[(t,1) for t in range(1,k+1)]
                assert all(r.doubles[p]['g']==1 for p in ids)
                ftby={tuple(z['parent']):z for z in ft['rows']}
                for t in range(2,k+1):
                    assert ftby[t,1]['predecessor']==(t-1,1)
                    assert ftby[t,1]['kind']=='no_promotion_same_column'
                z['verified_long_strict_chain']=ids
                z['diagnostic_pool_scope']='First physical B double of each of the k critical KEEPs, not D.'
            else:
                ids=[(1,1),(4,5)]
                assert r.doubles[1,1]['g']==r.doubles[4,5]['g']==10
                assert r.doubles[2,3]['signs']==r.doubles[4,5]['signs']==[0,0]
                q=audit(r,ids,mode='promotion',prefix_payment=True)
                row=next(z for z in q['rows'] if z['parent']==(4,5))
                assert row['restorer']==(2,3) and row['actual_gain_for_this_target']
                assert row['classification'] not in ('A_reset','restorer_prefix','nonneutral_restorer')
                z['critical_restorer_diagnostic']=row
                z['restorer_and_consumer_in_U']=[(2,3) in r.U,(4,5) in r.U]
                z['critical_restorer_original_U']=r.U.get((2,3))
                z['critical_consumer_original_U']=r.U.get((4,5))
                z['critical_source_boundaries']=r.boundaries[:4]
                z['critical_primitive_events']=r.events[:r.boundaries[3]['end_time']]
                z['diagnostic_pool_scope']='Two selected physical old-grandparent 10 parents, not D.'
            ledgers.append({'source':name,'pool_scope':z['diagnostic_pool_scope'],**audit(r,ids)})
        out.append(z);write('INDEPENDENT_RESULTS.json',out);write('CYCLIC_GAIN_LEDGER.json',ledgers)
        write('LAST_PROMOTION_FORESTS.json',forests)
        print('PASS',name,'Pi',z['full_original_Pi'],flush=True)
    meter.success=True
