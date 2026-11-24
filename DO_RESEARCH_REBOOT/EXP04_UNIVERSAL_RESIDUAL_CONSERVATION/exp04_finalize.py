from exp04_core import *


def load(name):return json.loads((ROOT/name).read_text())


def correct_continuity(p):
    h=p['history'];loss=p['last_A_loss'];hi=p['original_parent_certificate']['post_A']
    if loss is None:return None
    state=h['initial_relation']['B']
    for e in h['changes']:
        if e['id'][0]=='B' and e['time']<=loss['time']:state=e['present_after']
    lo=loss['unrolled_time'];T=loss['time']-lo if lo<0 else None
    for e in h['changes']:
        if e['id'][0]!='B':continue
        when=e['time']-(T if T and e['time']>hi else 0)
        if lo<when<=hi and not e['present_after']:state=False
    return state


def add_boundary_data(s,row):
    a=Tree(s['initial_A']);b=Tree(s['initial_B']);S=set(row['S'])
    bits={k:1<<i for i,k in enumerate(a.keys) if k in S};equal=[];ps=[]
    for tag,x in s['operations']:
        Replay.plain_splay(a,x)
        if tag=='K':Replay.plain_splay(b,x)
        equal.append(a.root==b.root and a.ch==b.ch)
        ps.append(len((set(b.labels(bits).values())-{0})-set(a.labels(bits).values())))
    assert a.state()==s['initial_A'] and b.state()==s['initial_B']
    row['equality_boundaries']=[i+1 for i,v in enumerate(equal) if v]
    run=longest=0
    for v in equal+equal:
        run=0 if v else run+1;longest=max(longest,min(run,len(equal)))
    row['longest_no_equality_operations']=longest;row['Psi_after_operations']=ps
    initial=psi_state(s['initial_A'],s['initial_B'],bits);n=len(ps);episodes=[];cur=None
    if n and not any(v==0 for v in ps):episodes=[{'id':0,'operations':list(range(1,n+1)),'kind':'persistent_positive_Psi'}]
    elif n:
        start=0 if initial==0 else next(i+1 for i,v in enumerate(ps) if v==0)%n
        for delta in range(n):
            i=(start+delta)%n
            if cur is None:
                if ps[i]==0:continue
                cur={'id':len(episodes),'operations':[],'kind':'between_actual_Psi_zero_boundaries'}
            cur['operations'].append(i+1)
            if ps[i]==0:episodes.append(cur);cur=None
        assert cur is None
    for ep in episodes:
        ts=set(ep['operations']);steps=[e for e in row['A_StepEv'] if e[1] in ts];ep.update(A_StepEv=steps,A=len(steps))
    row['Psi_episodes']=episodes


if __name__=='__main__':
    meter=Meter('EXP04_finalize')
    archive=load('EXP04_SOURCE_WITNESSES.json');oldrows=load('EXP04_RESIDUAL_INVENTORY.json')['inherited_sources']
    files=[('EXP04_NEW_SOURCE_CHECKPOINT.json','EXP04_NEW_RESULTS.json','EXP04_NEW_LIFECYCLES.json'),
        ('EXP04_ADVERSARIAL_SOURCES.json','EXP04_ADVERSARIAL_RESULTS.json','EXP04_ADVERSARIAL_LIFECYCLES.json'),
        ('EXP04_SPARSE_SOURCES.json','EXP04_SPARSE_RESULTS.json','EXP04_SPARSE_LIFECYCLES.json'),
        ('EXP04_FINAL_CYCLE_SOURCES.json','EXP04_FINAL_CYCLE_RESULTS.json','EXP04_FINAL_CYCLE_LIFECYCLES.json')]
    sources=[];newrows=[];lifecycles=[]
    for sf,rf,lf in files:
        z=load(sf);sources+=z['sources'] if isinstance(z,dict) else z
        newrows+=load(rf);lifecycles+=load(lf)
    assert len(sources)==120 and len(newrows)==120
    archive['new_sources']=sources;write('EXP04_SOURCE_WITNESSES.json',archive)
    oldsources={s['name']:s for s in archive['inherited_sources']}
    for row in oldrows:
        row['family']=oldsources[row['source']].get('family','inherited')
        if 'Psi_episodes' not in row:add_boundary_data(oldsources[row['source']],row)
    previous=json.loads((PREV/'EXP03_CAUSAL_EPISODE_RESULTS.json').read_text())
    for row in previous['inherited_sources']+previous['new_sources']:
        ids={tuple(e['original_parent']) for e in row['remaining_after_restart']}
        if not ids:continue
        ps=[]
        for p in row['original_parents']:
            if tuple(p['original_parent']) not in ids:continue
            ps.append({'original_parent':p['original_parent'],'type':p['type'],'g':p['g'],'target':p['target'],
                'history':p['ancestry_history'],'last_A_loss':p['last_A_loss'],'original_parent_certificate':p['original_parent_certificate'],
                'A_path':p['original_A_path'],'B_path':p['original_B_path']})
        lifecycles.append({'source':row['source'],'parents':ps,'maximum_load':row['last_loss_selector']['maximum_primitive_load'],
            'undefined':row['last_loss_selector']['undefined_parents'],'last_loss_loads':row['last_loss_selector']['loads']})
    changes=0;counterexamples=[];own=[]
    for row in lifecycles:
        for p in row['parents']:
            corrected=correct_continuity(p)
            if p.get('B_continuous_from_last_A_loss')!=corrected and 'B_continuous_from_last_A_loss' in p:changes+=1
            p['B_continuous_from_last_A_loss']=corrected
            p['g_is_A_ancestor_pre_A']=p['g'] in p['A_path'][:-1]
            p['g_is_A_ancestor_post_A']=False
            if corrected is False:counterexamples.append({'source':row['source'],'parent':p['original_parent']})
            if p['g_is_A_ancestor_pre_A']:own.append({'source':row['source'],'parent':p['original_parent']})
    write('EXP04_PHYSICAL_LIFECYCLES.json',{'sources':lifecycles,'continuity_measurement':'B must be present at the last A loss AND have no intervening B loss before post-A at consumption.',
        'corrected_preliminary_boolean_records':changes,'noncontinuous_histories':counterexamples,'own_access_grandparents':own})
    mono={s['source']:s for s in load('EXP04_MONOTONE_RESULTS.json')+load('EXP04_ADVERSARIAL_MONOTONE.json')}
    for row in load('EXP04_SPARSE_RESULTS.json')+load('EXP04_FINAL_CYCLE_RESULTS.json'):mono[row['source']]=row['following_classes']
    density={s['source']:s for s in load('EXP04_FINAL_CYCLE_DENSITY.json')}
    totals=Counter();families=defaultdict(Counter);allrows=oldrows+newrows
    for row in allrows:
        zero={digest(e['rho']) for e in row.get('new_comparison',{}).get('paid',[])}
        mm=mono.get(row['source'],{});mp={digest(e['rho']) for e in mm.get('monotone_comparison',{}).get('paid',[])}
        cp={digest(e['rho']) for e in mm.get('rank_certificate_paid',[])}
        dp={digest(e['rho']) for e in density.get(row['source'],{}).get('paid',[])}
        assignments=[];remaining=[]
        for e in row['events']:
            h=digest(e['rho']);kind='zero_two_direction' if h in zero else 'gappy_monotone' if h in mp else 'cycle_rank_certificate' if h in cp else 'actual_density_window' if h in dp else 'unpaid'
            assignments.append({'rho':e['rho'],'original_parent':e['original_parent'],'original_type':e['type'],'EXP04_class':kind});totals[kind]+=1
            if kind=='unpaid':remaining.append(e)
        row.update(EXP04_assignments=assignments,EXP04_remaining=remaining,EXP04_paid=len(assignments)-len(remaining))
        fam=families[row.get('family','inherited')];fam['sources']+=1;fam['R_star']+=row['R_star'];fam['remaining']+=len(remaining)
        fam['A']+=row['A'];fam['Q_B']+=row['Q_B']
    write('EXP04_RESIDUAL_INVENTORY.json',{'definition':'Literal original EXP-03 R_*; original types preserved; four new classes are successively subtracted.',
        'inherited_sources':oldrows,'new_sources':newrows,'assignment_totals':dict(totals),
        'universal_endpoint':'Q_B <= (35+48 C_seq+99 C_DF)A + R_next; universal R_next coverage OPEN'})
    # Correct imported report-only bound labels from the early in-flight
    # monotone run. Physical frames/costs/assignments are unchanged.
    for z in mono.values():
        for system in z.get('monotone_comparison',{}).get('systems',[]):
            system['bound']='R_system <=18 C_DF A; gappy monotone dynamic-finger theorem'
    write('EXP04_MONOTONE_CERTIFICATES.json',list(mono.values()))
    write('EXP04_ANCESTRY_DISCREPANCY_EXPERIMENTS.json',{'last_A_loss_maximum_observed_load':max(s['maximum_load'] for s in lifecycles),
        'undefined_last_A_losses':sum(s['undefined'] for s in lifecycles),'noncontinuous_B_histories':counterexamples,
        'own_access_grandparent_examples':own,'complete_lifecycles':'EXP04_PHYSICAL_LIFECYCLES.json',
        'edge_boundary_data':['EXP04_EDGE_BOUNDARY_EXPERIMENTS.json','EXP04_NEW_EDGE_AUDIT.json','EXP04_ADVERSARIAL_EDGES.json'],
        'qualifications':'Observed load is not a universal theorem. Raw ancestry mass remains refuted; edge-boundary A variation is bounded but neutral B decreases obstruct telescoping payment.'})
    write('EXP04_GLOBAL_CONGESTION_EXPERIMENTS.json',{'source_count':len(allrows),'per_system_absolute_budgets':{
        'zero2':'12 C_seq A; each original A transition witness load <=2',
        'two_monotone_strategies_both_directions':'72 C_DF A; each transition witness load <=4',
        'whole_cycle_L_le_2A':'15 C_DF A; source-level scalar reuse explicitly added',
        'actual_density':'12 C_DF A; original A span StepEv disjoint, load <=1'},
        'original_occurrence_assignment_totals':dict(totals),'new_universal_completeness':'OPEN',
        'counterexample_to_earlier_union':'composed_p4_alternating_inside_m256: A932,Q732,R_star1; no monotone representative, L/A3995/932>2; later paid by actual density window'})
    table=['# EXP-04 full new-source measurements','','Finite exact records; no table proves all-source coverage.','',
        '| Source | n | ops | M | A | Q_B | R_* | parents | zero2 | remaining | longest no equality |',
        '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for row in newrows:
        table.append(f"| {row['source']} | {row['population']} | {row['operations']} | {len(row['genuine_KEEP_support'])} | {row['A']} | {row['Q_B']} | {row['R_star']} | {row['parents']['parent_count']} | {len(row['new_comparison']['paid'])} | {len(row['EXP04_remaining'])} | {row['longest_no_equality_operations']} |")
    (ROOT/'EXP04_FULL_MEASUREMENTS.md').write_text('\n'.join(table)+'\n',encoding='utf-8')
    summary={'canonical_sources':len(allrows),'inherited_sources':len(oldrows),'new_sources':len(newrows),
        'original_operations':sum(row['operations'] for row in allrows),'new_original_operations':sum(row['operations'] for row in newrows),
        'R_star':sum(row['R_star'] for row in allrows),'inherited_R_star':sum(row['R_star'] for row in oldrows),'new_R_star':sum(row['R_star'] for row in newrows),
        'assignment_totals':dict(totals),'R_next_finite':sum(len(row['EXP04_remaining']) for row in allrows),
        'new_types':dict(Counter(e['type'] for row in newrows for e in row['events'])),
        'maximum_population':max(row['population'] for row in allrows),'maximum_new_operations':max(row['operations'] for row in newrows),
        'new_no_complete_equality_sources':sum(not row['equality_boundaries'] for row in newrows),
        'noncontinuous_B_histories':len(counterexamples),'own_access_grandparent_parents':len(own),
        'families':{k:dict(v) for k,v in families.items()},'universal_verdict':'OPEN; finite covered corpus does not establish completeness'}
    write('EXP04_SUMMARY.json',summary)
    cycles=[
        (1,'carrier-SET zero cuts and separately budgeted directions','PROVED restricted quantitative class; inherited120->107'),
        (2,'missing KEEP ranks and protected unequal fringes','REFUTED completeness of EXP-03/zero2 restart; new G and no-equality controls'),
        (3,'physical edge-boundary conservation','PROVED A Lipschitz3 per real rotation; REFUTED neutral B decrease and paid-only negative variation'),
        (4,'gappy monotone comparisons via dynamic finger','PROVED restricted72 C_DF A class; covers inherited strict residual finitely'),
        (5,'whole-cycle rank-travel certificate','PROVED restricted15 C_DF A class; universal rank budget REFUTED by extreme oscillations'),
        (6,'compose scrambled continuation and cheap oscillation; local density windows','REFUTED earlier union completeness; PROVED new12 C_DF A class on actual spans'),
        (7,'warmed sparse leaf/core cycles and private keys','FINITE EXACT; no undefined last-loss residual found; not an impossibility theorem'),
        (8,'continuous B ancestry from last A loss','REFUTED EXACT at scramble_p5_dyadic parent400,2; B loses then recreates82->116'),
        (9,'A-depth-weighted access-lemma potential, local reweighting','REFUTED PARAMETRICALLY: one original A rotation raises Phi by more than n/2; exact rational checks through513'),
        (10,'same potential, aggregate signed A drift','REFUTED PARAMETRICALLY: first B drop Omega(n^2) forces signed A drift Omega(n^2), while the complete source has A=O(n)')]
    write('EXP04_EXPERIMENT_LOG.json',{'cycles':[{'cycle':i,'candidate':c,'result':result,
        'next':'Continue on the first unsupported source-uniform completeness/congestion implication; do not promote finite coverage.'} for i,c,result in cycles],
        'rejected_construction':'EXP04_REJECTED_FRINGE_v001.json; core-start mismatch fixed with real prefix KEEP2; failed measured stage preserved',
        'measurement_correction':'B-continuity now checks presence at the A-loss instant as well as subsequent B losses. Final unified lifecycles supersede preliminary optimistic booleans.',
        'execution_state':'resumable campaign checkpoint; universal target remains open'})
    meter.success=True;meter.details.update(summary);print(json.dumps(summary,indent=2),flush=True)
