from base4 import *
from physical1 import Edges
from cohortc import decode_state
from exp01_oracle import Tree,Replay

def ids(es):return {digest(e['rho']):e for e in es}
def component(st,g):
    t=Tree(st);todo=[g];out={}
    while todo:
        k=todo.pop();out[str(k)]=t.ch[k]
        todo.extend(x for x in t.ch[k] if x is not None)
    return {'root':g,'children':out}

if __name__=='__main__':
    m=Meter('exact_payment_transition_and_component_coupling');out=[]
    oldcat=load(C3/'NEW_SOURCE_CATALOG.json');oldrows=load(C3/'NEW_RESULTS.json')
    newcat=load(ROOT/'SHARED_SOURCE_CATALOG.json');newrows=load(ROOT/'SHARED_RESULTS.json')
    for oi,ni in ((1,0),(2,1),(3,2)):
        old,new=oldcat[oi],newcat[ni];op=load(C3/f'NEW_PHYS_{oi:02}.json');np=load(ROOT/f'SHARED_PHYS_{ni:02}.json')
        ot=op['boundaries'][2]['end_time'];nt=np['boundaries'][2]['end_time']
        assert op['events'][:ot]==np['events'][:nt]
        for h in range(3):
            a,b=op['boundaries'][h],np['boundaries'][h]
            for key in ('pre_A_state','post_A_state','pre_B_state','post_B_state'):
                assert op['state_pool']['states'][a[key]]==np['state_pool']['states'][b[key]]
        oldg=ids([e for e in oldrows[oi]['original_R_star'] if e['consumer']==2])
        newg=ids(newrows[ni]['critical']['R_star_gaps_outside_F']);common=sorted(oldg.keys()&newg.keys())
        acc=load(ROOT/f'SHARED_ORDERED_{ni:02}.json');assigned={digest(e['rho']):k for k,es in acc['disjoint_original_assignments'].items() for e in es}
        changes=[{'original_rho':newg[k]['rho'],'parent':newg[k]['original_parent'],'old_assignment':'frozen_skipped_rank',
            'new_assignment':assigned[k]} for k in common]
        future=[(h,x) for h,(tag,x) in enumerate(new['operations'],1) if tag=='K' and 2<=x<=new['s']+1]
        ascent=next((future[j-1],future[j]) for j in range(1,len(future)) if future[j][1]>future[j-1][1])
        prevh=ascent[0][0];hh=ascent[1][0]
        donor=next(e for e in np['events'] if e['actor']=='A' and prevh<e['id'][1]<=hh)
        a,bt=Edges(new['initial_A']),Edges(new['initial_B']);states=None
        for e in np['events']:
            if e['id']==donor['id']:
                before={'A':format(a.code(),'x'),'B':format(bt.code(),'x')};a.step(e)
                states={'before':before,'after':{'A':format(a.code(),'x'),'B':format(bt.code(),'x')}};break
            (a if e['actor']=='A' else bt).step(e)
        out.append({'old_source':old['name'],'new_source':new['name'],'old_source_sha256':digest(old),'new_source_sha256':digest(new),
            's':new['s'],'identical_full_original_events_through_Ky':ot,'identical_all_A_B_prefix_boundary_codes':True,
            'same_original_R_star_gaps_switching_F_to_alternative':changes,
            'future_single_g_tour_ascent':ascent,'canonical_first_actual_A_bit_of_ascent':donor,'complete_A_B_codes_at_that_bit':states,
            'candidate_per_bit_load_on_all_F_negative_critical_parents':len(newrows[ni]['critical']['R_star_parents']),
            'candidate_load_on_F_negative_late_critical_parents':len({tuple(e['original_parent']) for e in newrows[ni]['critical']['R_star_gaps_outside_F'] if e['original_parent'][1]>2}),
            'scope':'Finite full-four-system F failures; symbolic unbounded load proved only for the specific original records certificate, not for actual S_UU.'})
        del op,np;gc.collect()
    write('EXACT_PAID_TO_ALTERNATIVE_TRANSITIONS.json',out)
    # An omitted outside request can change the GLOBAL B state/path while the
    # common first-hit component and every lower relevant old-g double match.
    s=load(ROOT/'DEFORM_SOURCE_CATALOG.json')[3];p=load(ROOT/'DEFORM_PHYS_03.json');z=load(ROOT/'DEFORM_R6_MONOTONE_03.json');h=s['critical_operation']
    e=next(q for q in z['paid'] if q['original_parent'][0]==h)
    system=next(q for q in z['systems'] if q['strategy']==e['strategy'] and q['comparison_orientation']==e['orientation'])
    wi,hh,j=e['shadow_double'];w=system['windows'][wi];shadow=Tree(w['initial_B']);before=None
    for t in w['retained']:
        if t==h:before=shadow.state();break
        Replay.plain_splay(shadow,s['operations'][t-1][1])
    actual=decode_state(p,p['boundaries'][h-1]['pre_B_state']);g=e['old_grandparent']
    assert before!=actual and component(before,g)==component(actual,g)
    record={'source':s['name'],'source_sha256':digest(s),'original_parent':e['original_parent'],'rho':e['rho'],
        'frozen_certificate':e,'supporting_window':w,'actual_complete_pre_B':actual,'shadow_complete_pre_B':before,
        'global_states_differ':True,'same_complete_first_hit_component':component(actual,g),
        'actual_target_path':Tree(actual).path(s['operations'][h-1][1]),'shadow_target_path':Tree(before).path(s['operations'][h-1][1]),
        'omitted_KEEPS':w['omitted'],'same_old_g_double_despite_omitted_outside_access':True}
    write('INTACT_COMPONENT_COUPLING_EXAMPLE.json',record)
    # Pin actual supporting A transitions and all four complete states at each
    # such primitive in the38-key original paid window.
    traced=load(ROOT/'PC1_PAID_WINDOW_CERTIFICATES.json')[1];s=oldcat[1];p=load(C3/'NEW_PHYS_01.json')
    selected={tuple(q) for w in traced['supporting_windows'].values() for q in w['original_A_transition_witnesses']}
    a,bt=Edges(s['initial_A']),Edges(s['initial_B']);states=[]
    for e in p['events']:
        before=(a.code(),bt.code()) if tuple(e['id']) in selected else None
        (a if e['actor']=='A' else bt).step(e)
        if before:states.append({'original_A_bit':e,'before':{'A':format(before[0],'x'),'B':format(before[1],'x')},
            'after':{'A':format(a.code(),'x'),'B':format(bt.code(),'x')}})
    assert len(states)==len(selected)
    write('PAID_WINDOW_ORIGINAL_A_STATES_38.json',{'source_sha256':digest(s),'n':s['n'],'complete_state_code_definition':p['state_pool']['code_definition'],'actual_supporting_transitions':states})
    m.ok=True;print('PASS identical-prefix payment transitions, one-ascent sharing, exact outside-component coupling and original supporting A states',flush=True)
