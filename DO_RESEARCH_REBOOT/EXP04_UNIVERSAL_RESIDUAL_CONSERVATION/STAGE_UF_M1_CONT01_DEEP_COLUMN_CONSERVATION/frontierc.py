"""Read-only evidence composition and exact literal frontier classification."""
from basec import *
import ast,gc

def reference_pairs(entry):
    if entry['origin']=='M0' and entry['index']<6:
        z=load(base0.C5/'INDEPENDENT_RESULTS.json')[entry['index']]
        if z.get('full_original_Pi'):
            return z['independent_cohort_R6_check']['independently_recomputed_all_original_pairs']
    if entry['origin']=='M1':
        p=M1/f'NEW_ORIGINAL_PI_{entry["index"]:02}.json'
        if p.exists():return load(p)['independent_cohorts']['independently_recomputed_all_original_pairs']
    return None

def classify(s,birth,phys):
    U={ast.literal_eval(k):v for k,v in birth['U'].items()}
    ds={tuple(z['parent']):z for z in phys['doubles']}
    creates=defaultdict(list)
    for e in phys['events']:
        if e['actor']=='A':
            for z in e['created']:creates[z].append(e['time'])
    T=len(phys['events']);donors={};seen=set()
    for p,u in U.items():
        if not u['exposed']:continue
        d=ds[p];nu=d['events'][0 if d['case'] in ('LL','RR') else 1]
        hits=[t+shift*T for t in creates[d['J']] for shift in (0,1) if nu<t+shift*T<=u['hit_time']]
        assert hits,(p,u)
        t=min(hits);real=(t-1)%T+1
        assert real not in seen;seen.add(real)
        donors[p]=phys['events'][real-1]['id']
    assert len(donors)<=birth['real_A_bits']
    rows=[];by_creator=defaultdict(list)
    for z in birth['C_U_births']:
        if z['distance']<=2:continue
        p=tuple(z['consumer']);r=tuple(z['creator'])
        if r not in U:kind='B0_nonU_creator'
        elif z['output_kind']=='parent' and U[r]['exposed']:
            kind='B1_acquired_sibling';assert ds[r]['case'] in ('LR','RL')
        else:
            kind='silent_UU';assert not U[r]['exposed']
        if z['output_kind']=='grandparent' and r in U:assert not U[r]['exposed']
        rows.append({**z,'new_scope':kind,'sibling_A_donor':donors.get(r),
            'creator_chosen_output_acquired':U[r]['exposed'] if r in U else None})
        by_creator[r].append(rows[-1])
    for r,zs in by_creator.items():
        assert len(zs)<=2
        assert sum(z['new_scope']=='B1_acquired_sibling' for z in zs)<=1
    cnt=Counter(z['new_scope'] for z in rows)
    capacities={k:3*v for k,v in cnt.items()}
    assert capacities.get('B0_nonU_creator',0)<=72*birth['A']
    assert capacities.get('B1_acquired_sibling',0)<=6*birth['A']
    actual=Counter()
    for z in rows:
        if z['actual_deep_gap_weight'] is not None:actual[z['new_scope']]+=z['actual_deep_gap_weight']
    assert sum(actual.values())==birth['actual_R_C_deep']
    return {'source':s['name'],'source_sha256':digest(s),'A':birth['A'],
        'all_deep_U_C_counts':dict(cnt),'three_slot_capacities':capacities,
        'literal_actual_deep_weights':dict(actual),'actual_R_C_deep':birth['actual_R_C_deep'],
        'chosen_output_A_acquisitions':len(donors),
        'chosen_output_original_A_donors':{str(k):v for k,v in donors.items()},'deep_birth_frontier':rows}

if __name__=='__main__':
    meter=Meter('frontier_composition');out=[];refs=[]
    for i,e in enumerate(controls()):
        b=load(ROOT/f'BIRTH_{i:02}.json');ref=reference_pairs(e)
        if ref is not None:
            aa={digest(z['rho']):z for z in ref};bb={digest(z['rho']):z for z in b['original_pairs']}
            assert set(aa)==set(bb)
            for k,z in aa.items():assert digest(z)==digest(bb[k]),(i,k)
            refs.append({'index':i,'source':e['source']['name'],'all_original_pairs':len(aa),'exact_full_fields_match':True})
        out.append({'group':'historical','index':i,**classify(e['source'],b,load(e['physical']))})
        gc.collect()
    for group,cat,stem in (('fresh',load(ROOT/'NEW_SOURCE_CATALOG.json'),'NEW'),
                           ('guarded',load(ROOT/'GUARDED_SOURCES.json'),'GUARDED')):
        for i,s in enumerate(cat):
            out.append({'group':group,'index':i,**classify(s,load(ROOT/f'{stem}_BIRTH_{i:02}.json'),load(ROOT/f'{stem}_PHYS_{i:02}.json'))})
            gc.collect()
    n=load(ROOT/'NATIVE_SELECTOR_RESULTS.json');ob=load(ROOT/'NEW_BIRTH_08.json');star=n[1]['original_R_star']
    assert len(star)==1
    rho=star[0]['rho'];parent=tuple(star[0]['original_parent'])
    b0=next(z for z in ob['C_U_births'] if tuple(z['consumer'])==parent)
    assert b0['distance']==4 and b0['creator_class']=='whole_frame_exposed'
    assert rho==[4680,[68,6],[4676,3]] and parent==(4680,4)
    assert tuple(b0['creator'])==(4673,3)
    proof={'false_candidate':'Every deep original R_star C consumer has an original U frame-creator.',
        'scope':'Original prehybrid R_star, not the prescribed post-hybrid residual.',
        'source':n[1]['source'],'index':8,'source_sha256':digest(load(ROOT/'NEW_SOURCE_CATALOG.json')[8]),
        'rho':rho,'parent':parent,'creator':b0['creator'],'distance':4,'birth':b0,
        'native_original_selector':star[0],'actual_R_C_deep':0,
        'zero_reason':'Existing original periodic certificate plus cheap quota remains active.'}
    write('CREATOR_CLOSURE_COUNTEREXAMPLE.json',proof)
    write('FRONTIER_RESULTS.json',out);write('EXACT_REFERENCE_PAIR_CHECKS.json',refs)
    meter.info.update(complete_sources=len(out),earlier_full_pair_certificates=len(refs));meter.ok=True
    print('PASS frontier',len(out),'sources;',len(refs),'exact earlier pair comparisons; native R_star creator-closure counterexample',flush=True)
