"""Generate a standalone tuple auditor exclusively; old auditors are text inputs."""
from pathlib import Path
HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'route_c_unbounded_depth_charging_20261031_v001'
old=(OLD/'audit_arbitrary_keys.py').read_text(encoding='utf-8')
prefix=old[:old.index('    def bound(')].replace('route_c_split_shallow_charging_20261031_v001','route_c_unbounded_depth_charging_20261031_v001')
base=old[old.index('    def bound('):old.index('    def scan(')].replace('def bound(','def coarse_bound(',1)
scan=old[old.index('    def scan('):old.index('    def compact(')]
scan=scan.replace('def scan(rows,bs,cut,shallow=False):','def scan(rows,bs,cut,refined=True):')
scan=scan.replace("facts=[bound(rows,bs,i,j,b['key']) for i in history if not shallow or b['key'] in collar(rows,bs,i)]",
  "facts=[bound(rows,bs,i,j,b['key'],refined) for i in history]")
scan=scan.replace("if not owed or (shallow and b['key'] not in collar(rows,bs,i)):continue","if not owed:continue")
assert 'shallow' not in scan
extra='''
    def path(t,x):
        keys=[];directions=[]
        while t is not None:
            keys.append(t[0])
            if t[0]==x:return keys,directions
            side='L' if x<t[0] else 'R';directions.append(side);t=t[1] if side=='L' else t[2]
        raise AssertionError('present source key')
    def envelope(t,x,y):
        px,dirs=path(t,x);py,_=path(t,y);d=len(dirs);h=len(py)-1
        common=0
        while common<min(len(px),len(py)) and px[common]==py[common]:common+=1
        lca=common-1;ops=[]
        for number in range(d//2):
            top=d-2*(number+1)
            ops.append(dict(case=''.join(dirs[top:top+2]),site_depth=top,grandparent=px[top],parent=px[top+1]))
        if d%2:ops.append(dict(case='ZIG',site_depth=0,grandparent=px[0],parent=None))
        role='root_noop' if d==0 else ('accessed' if x==y else None)
        entry=None;mu=r=m=0;candidate=h
        if role=='accessed':candidate=0
        if role is None:
            entry=next(z for z,op in enumerate(ops) if op['site_depth']<=lca);op=ops[entry]
            if op['case']=='ZIG':role='zig_root' if y==op['grandparent'] else 'zig_fringe';mu=1
            elif y==op['parent']:role='parent';mu=0
            else:role='grandparent' if y==op['grandparent'] else 'fringe';mu=2
            outer=[op for op in ops[entry+1:] if op['case']!='ZIG'];r=len(outer)
            matching='LL' if y<x else 'RR';m=sum(op['case']==matching for op in outer)
            candidate=h+mu-r-m
        U=min(h+2,max(0,candidate))
        return dict(source_depth=h,access_depth=d,lca_depth=lca,operations=ops,entry_operation=entry,
          entry_role=role,first_gain_allowance=mu,outer_doubles=r,matching_outer_doubles=m,
          target_side='equal' if y==x else ('left' if y<x else 'right'),upper_depth=U)
    def bound(rows,bs,i,j,y,refined=True):
        result=coarse_bound(rows,bs,i,j,y)
        if not refined:return result
        active=result['intervening_B_occurrences'];profile=None;first=None;firstactual=None
        c=result['ceiling']
        if active:
            first=active[0];fr=rows[first]
            assert fr['source_B']==rows[bs[i]['B_active_access']]['destination_B']
            profile=envelope(fr['source_B'],fr['key'],y)
            assert [op['case'] for op in profile['operations']]==[e[0] for e in fr['B_events']]
            firstactual=depth(tup(fr['destination_B']),y);assert firstactual<=profile['upper_depth']
            c=profile['upper_depth']//2+len(active)-1 if bs[j]['has_KEEP'] else 0
        assert bs[j]['q']<=c<=result['ceiling']
        result.update(coarse_ceiling=result['ceiling'],ceiling=c,first_intervention=first,
          first_frame_profile=profile,actual_first_post_depth_for_verification=firstactual)
        return result
'''
tail='''
    def compact(t):
        return dict(cut=t['cut'],accepted=t['accepted'],unpaid=t['unpaid'],unpaid_excess=t['unpaid_excess'],
          transfers=[[p['payer_occurrence'],v['anchor_occurrence'],v['demand_start'],v['demand_end'],v['credit_start'],v['credit_end']]
            for p in t['pools'] for v in p['loans']])
    oldcert=json.loads((OLD/'arbitrary_key_certificate.json').read_text(encoding='utf-8'))
    witnesses=[];matrix=[]
    for wi,prior in enumerate(oldcert['witnesses']):
        initial=tup(prior['initial_diagonal']);a=b=initial;pr=[]
        for k,(mode,x) in enumerate(prior['prefix']):a,b,r0=step(a,b,mode,x,-k-1);pr.append(r0)
        ia,ib=a,b;rows=[]
        for k,(mode,x) in enumerate(prior['word']):a,b,r0=step(a,b,mode,x,k);rows.append(r0)
        assert (a,b)==(ia,ib)
        assert json.loads(json.dumps(rows))==prior['full_replay'] and json.loads(json.dumps(pr))==prior['prefix_replay']
        bs=blocks(rows);trials=[scan(rows,bs,cut) for cut in range(len(bs))]
        oldtrials=[scan(rows,bs,cut,False) for cut in range(len(bs))]
        good=[t for t in trials if t['accepted']];oldgood=[t for t in oldtrials if t['accepted']];assert good
        assert [compact(t) for t in oldtrials]==prior['cut_trials']
        assert [t['cut'] for t in oldgood]==prior['accepted_cuts']
        assert set(prior['accepted_cuts'])<={t['cut'] for t in good}
        assert json.loads(json.dumps(oldgood[0]))==prior['selected_ledger']
        chosen=good[0];prefix_comparison=None
        if wi<2:
            assert chosen['cut']==0
            paying=[p for p in chosen['pools'] if p['loans']]
            assert [(p['payer_occurrence'],[(v['anchor_occurrence'],v['demand_end']-v['demand_start']) for v in p['loans']]) for p in paying]==[(1,[(0,3)]),(2,[(0,1)])]
            payer=next(p for p in chosen['pools'] if p['payer_occurrence']==2)
            coarse=next(p for p in oldgood[0]['pools'] if p['payer_occurrence']==2)
            f=payer['facts'][0];profile=f['first_frame_profile']
            assert (f['h'],f['k'],f['coarse_ceiling'],f['ceiling'])==(6,1,4,1)
            assert (profile['entry_role'],profile['first_gain_allowance'],profile['outer_doubles'],profile['matching_outer_doubles'],profile['upper_depth'])==('parent',0,2,2,2)
            assert (coarse['reservation'],payer['reservation'],payer['own_q'],payer['capacity'])==(2,1,1,2)
            assert coarse['balances_after']==[[0,1]] and payer['balances_after']==[[0,0]]
            control=next(p for p in chosen['pools'] if p['payer_occurrence']==3)
            assert control['ceiling']==control['reservation']==2 and control['own_q']==1
            span_assign=[v for v in chosen['credit_assignments'] if v['demand'][0] in (0,1,2)]
            assert len(span_assign)==10 and all(v['credit'][0] in (0,1,2) for v in span_assign)
            prefix_comparison=dict(indices=[0,1,2],A=sum(r['a'] for r in rows[:3]),Q_B=sum(r['q'] for r in rows[:3]),
              coarse_unpaid_after=1,refined_unpaid_after=0,recovered_pool_occurrence=2,recovered_units=1,
              old_ceiling=4,new_ceiling=1,old_reservation=2,new_reservation=1,credit_assignments=span_assign,
              uses_DELETE_credit=False,claims_new_closed_cycle_coverage=False)
            assert (prefix_comparison['A'],prefix_comparison['Q_B'])==(5,10)
        for rr in pr+rows:
            if rr['mode']!='K':continue
            for y in range(1,prior['n']+1):
                profile=envelope(rr['source_B'],rr['key'],y)
                actual=depth(tup(rr['destination_B']),y)
                assert actual<=profile['upper_depth']<=profile['source_depth']+2
                assert [op['case'] for op in profile['operations']]==[e[0] for e in rr['B_events']]
                matrix.append(dict(witness=wi,occurrence=rr['occurrence'],tracked_key=y,profile=profile,actual_post_depth=actual))
        A,Q,Z=sum(r['a'] for r in rows),sum(r['q'] for r in rows),sum(r['z'] for r in rows)
        assert (A,Q,Z,2*A-Q)==(prior['A'],prior['Q_B'],prior['Z_B'],prior['weight'])
        witnesses.append(dict(name=prior['name'],n=prior['n'],initial_diagonal=raw(initial),prefix=prior['prefix'],prefix_replay=pr,
          word=prior['word'],cycle_initial_A=raw(ia),cycle_initial_B=raw(ib),full_replay=rows,blocks=bs,chosen_cut=chosen['cut'],
          selected_ledger=chosen,cut_trials=[compact(t) for t in trials],accepted_cuts=[t['cut'] for t in good],
          old_UD_trials=[compact(t) for t in oldtrials],old_UD_accepted_cuts=prior['accepted_cuts'],
          alternative_assignment_checks=sum(len(t['credit_assignments']) for t in good),
          old_UD_alternative_assignment_checks=sum(len(t['credit_assignments']) for t in oldgood),
          span_comparison=prefix_comparison,A=A,Q_B=Q,Z_B=Z,weight=2*A-Q,actual_pair_closure=True))
    cert=dict(schema='first-intervention-frame-ceiling-v1',date='2026-10-31',witnesses=witnesses,local_envelope_matrix=matrix,
      finite_fits=0,size_sweeps=0,new_source_words=0,word_searches=0,source_graph_searches=0,allocation_optimizer_used=False,
      actual_payer_q_used_as_reservation_oracle=False,full_exact_depth_propagation_used=False,
      matching_terminal_line='FROZEN',universal_CD='OPEN',strict_closed_walk_class_enlargement='NOT ESTABLISHED',
      claimed_strict_advancement='earlier repayment of a reachable three-block source span, without DELETE credit')
    save('first_intervention_certificate.json',cert)
    print(json.dumps(dict(preserved_files=len(pins),stage_files=len(stage),local_envelope_rows=len(matrix),
      witnesses=[dict(name=w['name'],new_cuts=len(w['accepted_cuts']),old_cuts=len(w['old_UD_accepted_cuts']),
        span=w['span_comparison'] and {k:v for k,v in w['span_comparison'].items() if k!='credit_assignments'}) for w in witnesses]),indent=2))

if __name__=='__main__':main()
'''
source=prefix+base+extra+scan+tail
source=source.replace('"""Arbitrary-key split payers from actual post-depths; no search or fit."""',
  '"""Single first-intervention frame ceiling; fixed old source corpus, no fit."""')
with (HERE/'audit_first_intervention.py').open('x',encoding='utf-8') as f:f.write(source)
