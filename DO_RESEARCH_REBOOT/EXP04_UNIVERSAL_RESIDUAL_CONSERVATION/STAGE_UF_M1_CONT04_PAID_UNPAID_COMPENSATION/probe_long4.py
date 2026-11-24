from base4 import *
from fast_physics import physical_replay,skeleton_cost
from physical1 import Edges
from rank_audit3 import audit as rank_audit
from corridor_audit4 import stream_audit
from gate1 import signature

def expanded(short,rule):
    copies=rule['copies_in_long'];lo,hi=rule['template_primitive_slice_zero_based'];assert (lo,hi)==(0,4)
    for c in range(copies):
        for e in short['events'][lo:hi]:
            z={**e,'id':list(e['id']),'time':e['time']+4*c};z['id'][1]+=2*c;yield z
    for e in short['events'][hi:]:
        z={**e,'id':list(e['id']),'time':e['time']+4*(copies-1)};z['id'][1]+=2*(copies-1);yield z

def expanded_boundaries(short,rule):
    copies=rule['copies_in_long']
    for c in range(copies):
        for row in short['boundaries'][:2]:
            z={**row,'t':row['t']+2*c}
            for k in ('start_time','post_A_time','end_time'):z[k]+=4*c
            yield z
    for row in short['boundaries'][2:]:
        z={**row,'t':row['t']+2*(copies-1)}
        for k in ('start_time','post_A_time','end_time'):z[k]+=4*(copies-1)
        yield z

if __name__=='__main__':
    m=Meter('raw_negative_wide_probe');short=load(ROOT/'PROBE_SHORT_SOURCE.json');row=load(ROOT/'PROBE_SHORT_RESULTS.json')
    p=load(ROOT/'PROBE_SHORT_PHYS.json');n=short['n'];b=(n-1).bit_length();assert b==10
    extra=(10*row['A']-row['raw_periodic_cost'])//(2*(b-9))+1;copies=extra+1;delta=2*extra
    s=copy.deepcopy(short);s['name']=short['name'].replace('_T1',f'_T{copies}');s['replication']=copies
    s['operations']=[['K',x] for c in range(copies) for x in (n,1)]+short['operations'][2:]
    s['creator_operation']+=delta;s['critical_operation']+=delta
    s['original_B_KEEP_mapping']=[[j,h+delta] for j,h in short['original_B_KEEP_mapping']]
    s.update(short_source_sha256=digest(short),expected_A=row['A']+delta,
        expected_raw_periodic_cost=row['raw_periodic_cost']+2*(1+b)*extra)
    write('PROBE_LONG_SOURCE.json',s)
    assert len(p['events'][:4])==4 and all(e['case']=='ZIG' for e in p['events'][:4])
    first,last=p['boundaries'][:2]
    assert first['pre_A_state']==last['post_A_state'] and first['pre_B_state']==last['post_B_state']
    extremes=1|(1<<(n-1))
    assert all(lab&extremes for e in p['events'][:4] for lab in e['lost']+e['created'])
    rule={'short_source_sha256':digest(short),'long_source_sha256':digest(s),'copies_in_long':copies,
        'template_original_operations':[1,2],'template_primitive_slice_zero_based':[0,4],
        'template_events':p['events'][:4],
        'event_rule':'Repeat first four actual zig bits with operation+=2c,time+=4c; suffix operation+=2(T-1),time+=4(T-1). Other fields identical.',
        'boundary_rule':'Repeat first two complete boundary rows with matching shifts; suffix has same full state-pool indices.',
        'B_double_rule':'Every original B double belongs to suffix: shift parent/operation IDs by2(T-1), its event times by4(T-1). No new double.',
        'Pi_U_R6_invariance':'Loop bits lose/create only extreme-touching labels; all internal SET memberships, birth/loss/first-hit order and full original cohort adjacency are unchanged under literal ID/time lift. Extreme jumps add no consecutive-rank scan.',
        'full_state_template_identity_verified':True,'full_long_native_R_star_rerun':False}
    write('PROBE_EVENT_EXPANSION.json',rule)
    # Reconstruct BOTH full physical trees at every expanded operation boundary.
    a,bt=Edges(s['initial_A']),Edges(s['initial_B']);a0,bt0=a.code(),bt.code();ev=iter(expanded(p,rule));count=0
    for boundary,(tag,x) in zip(expanded_boundaries(p,rule),s['operations']):
        assert boundary['tag']==tag and boundary['x']==x
        for tree,key in ((a,'pre_A_state'),(bt,'pre_B_state')):assert tree.code()==int(p['state_pool']['states'][boundary[key]],16)
        for t in range(boundary['start_time'],boundary['end_time']):
            e=next(ev);count+=1;assert e['time']==count and e['id'][1]==boundary['t'] and e['target']==x
            (a if e['actor']=='A' else bt).step(e)
        for tree,key in ((a,'post_A_state'),(bt,'post_B_state')):assert tree.code()==int(p['state_pool']['states'][boundary[key]],16)
    assert next(ev,None) is None and (a.code(),bt.code())==(a0,bt0)
    fast=physical_replay(s,collect_A=True);assert fast['A']==s['expected_A'] and fast['Q_B']==row['Q_B']
    xs=[x for tag,x in s['operations'] if tag=='K'];raw=sum((x!=xs[j-1])+abs(x-xs[j-1]).bit_length() for j,x in enumerate(xs))
    assert raw==s['expected_raw_periodic_cost']>10*fast['A']
    norms=[skeleton_cost(fast,variant=v) for v in ('G','H')]
    assert all(z['eligible_periodic'] for z in norms)
    assert all(not any(h<=2*copies for h in z['retained_original_operations']) for z in norms)
    assert [z['B_cyclic'] for z in norms]==[z['B_cyclic'] for z in row['G_H_periodic_certificates']]
    states=[];index={};fr=[]
    for z in fast['rows']:
        q={k:v for k,v in z.items() if k not in ('A_code','B_code')}
        for k in ('A','B'):
            code=z[k+'_code']
            if code not in index:index[code]=len(states);states.append(format(code,'x'))
            q[k+'_state']=index[code]
        fr.append(q)
    write('PROBE_LONG_FULL_STATES.json',{'n':n,'states':states,'rows':fr,
        'all_expanded_A_B_boundaries_equal_short_state_pool':True,'full_long_word_incremental_replay':True,
        'independent_scope':'Full independent short tuple replay plus fresh edge/mask expansion and separate incremental FullTree whole-word replay.'})
    rank=rank_audit(s,p['original_S'],expanded(p,rule));assert rank['Lambda_A']>6*rank['A']
    write('PROBE_LONG_RANK.json',rank)
    ds=[{**d,'parent':[d['parent'][0]+delta,d['parent'][1]]} for d in p['doubles']]
    gs={z['t']:z['A_gap'] for z in fast['rows'] if z['tag']=='K'}
    short_sig=signature(p,load(ROOT/'PROBE_SHORT_BIRTH.json'),load(ROOT/'PROBE_SHORT_FOREST.json'),load(ROOT/'PROBE_SHORT_M1_AUDIT.json'))
    sig={(v[0]+delta,v[1]) for v in short_sig}
    corridor=stream_audit(s,gs,ds,lambda:expanded(p,rule),fast['A'],sig)
    write('PROBE_LONG_CORRIDOR.json',corridor)
    critical=row['critical'];h=s['critical_operation'];selected={tuple(z['parent']) for z in corridor['E_phys']}
    late={(h,v[1]) for v in critical['sigma_parents'] if v[1]>2*gs[h]};assert late<=selected
    result={'source':s['name'],'source_sha256':digest(s),'replication':copies,'A':fast['A'],'Q_B':fast['Q_B'],
        'operations':len(s['operations']),'original_primitives':count,'raw_periodic_cost':raw,'raw_minus_10A':raw-10*fast['A'],
        'raw_periodic_eligible':False,'Lambda_A':rank['Lambda_A'],'G_H_periodic_certificates':norms,
        'critical':{'h':h,'A_gap':gs[h],'N_h':critical['N_h'],'R6_parents':[[h,v[1]] for v in critical['R6_parents']],
            'late_sigma_E_phys_parents':sorted(late)},
        'original_R_star':None,'full_long_native_Pi_R_star_rerun':False,
        'original_U_R6_scope':'Exact internal SET/first-hit/scan insertion law from full independently/native-classified short source; all literal original IDs decoded.',
        'actual_S_UU':0,'exact_zero_reason':'Positive ORIGINAL G and H periodic certificates plus cheap packet quota. No unrun R_* set is treated as empty.',
        'exact_D_scope':'No literal full D enumeration claimed; source-wide existing periodic theorem excludes every noncheap residual.'}
    write('PROBE_LONG_RESULTS.json',result);m.info.update(fresh_complete_sources=1,long_operations=len(s['operations']));m.ok=True
    print('PASS raw-negative wide probe, N',critical['N_h'],'A',fast['A'],'raw',raw,'10A',10*fast['A'],
        'G/H',[z['B_cyclic'] for z in norms],'S_UU0 by existing certificates',flush=True)
