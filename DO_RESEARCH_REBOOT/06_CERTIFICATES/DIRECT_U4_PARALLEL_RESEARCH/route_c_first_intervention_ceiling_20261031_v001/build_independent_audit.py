"""Write a standalone pointer/source-frame verifier with exclusive creation."""
from pathlib import Path
HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'route_c_unbounded_depth_charging_20261031_v001'
old=(OLD/'independent_verify.py').read_text(encoding='utf-8')
prefix=old[:old.index('    def fact(')]
prefix=prefix.replace("cp=HERE/'arbitrary_key_certificate.json'","cp=HERE/'first_intervention_certificate.json'")
prefix=prefix.replace('route_c_split_shallow_charging_20261031_v001/split_shallow_certificate.json',
  'route_c_unbounded_depth_charging_20261031_v001/arbitrary_key_certificate.json')
base=old[old.index('    def fact('):old.index('    def independent_pass(')].replace('def fact(','def coarse_fact(',1)
scan=old[old.index('    def independent_pass('):old.index('    def compact(')]
scan=scan.replace('def independent_pass(rows,bs,cut,shallow_only=False):','def independent_pass(rows,bs,cut,refined=True):')
scan=scan.replace("facts=[fact(rows,bs,i,j) for i in history if not shallow_only or b['key'] in shallow(rows,bs,i)]",
  "facts=[fact(rows,bs,i,j,refined) for i in history]")
scan=scan.replace("eligible=[i for i in history if cursor[i]<bs[i]['delta'] and (not shallow_only or b['key'] in shallow(rows,bs,i))]",
  "eligible=[i for i in history if cursor[i]<bs[i]['delta']]")
assert 'shallow_only' not in scan
extra='''
    def search_path(t,key):
        out=[]
        while t is not None:
            out.append(t[0])
            if key==t[0]:return out
            t=t[1] if key<t[0] else t[2]
        raise AssertionError('present source path')
    def subtree(t,key):
        while t is not None:
            if t[0]==key:return t
            t=t[1] if key<t[0] else t[2]
        raise AssertionError('operation site ancestor present')
    def envelope(t,x,y,source_events):
        px,py=search_path(t,x),search_path(t,y);d=len(px)-1;h=len(py)-1
        same=0
        for ax,ay in zip(px,py):
            if ax!=ay:break
            same+=1
        ops=[]
        ck(len(source_events)==(d+1)//2,'complete pointer-source operation list')
        for index,event in enumerate(source_events):
            zig=event[0]=='ZIG';top=0 if zig else d-2*(index+1)
            ck(zig==(index==len(source_events)-1 and d%2==1),'only final zig')
            ops.append(dict(case=event[0],site_depth=top,grandparent=px[top],parent=None if zig else px[top+1]))
        if d==0:role='root_noop';entry=None;mu=outer=matched=0;cap=h
        elif x==y:role='accessed';entry=None;mu=outer=matched=0;cap=0
        else:
            # Choose entry by subtree membership, independently of the producer's LCA test.
            entry=next(index for index,op in enumerate(ops) if y in inorder(subtree(t,op['grandparent'])))
            op=ops[entry]
            if op['case']=='ZIG':role='zig_root' if y==op['grandparent'] else 'zig_fringe';mu=1
            elif y==op['parent']:role='parent';mu=0
            else:role='grandparent' if y==op['grandparent'] else 'fringe';mu=2
            following=[op['case'] for op in ops[entry+1:] if op['case']!='ZIG']
            outer=len(following);matched=sum(case==('LL' if y<x else 'RR') for case in following)
            cap=h+mu-outer-matched
        return dict(source_depth=h,access_depth=d,lca_depth=same-1,operations=ops,entry_operation=entry,
          entry_role=role,first_gain_allowance=mu,outer_doubles=outer,matching_outer_doubles=matched,
          target_side='equal' if y==x else ('left' if y<x else 'right'),upper_depth=min(h+2,max(0,cap)))
    def fact(rows,bs,i,j,refined=True):
        f=coarse_fact(rows,bs,i,j)
        if not refined:return f
        first=None;profile=None;actual_first=None;c=f['ceiling'];changes=f['intervening_B_occurrences']
        if changes:
            first=changes[0];r=rows[first];y=bs[j]['key']
            ck(r['source_B']==rows[bs[i]['B_active_access']]['destination_B'],'no hidden B change before first intervention')
            profile=envelope(r['source_B'],r['key'],y,r['B_events'])
            actual_first=depth(r['destination_B'],y);ck(actual_first<=profile['upper_depth'],'universal frame upper bound at actual first source event')
            c=profile['upper_depth']//2+len(changes)-1 if bs[j]['has_KEEP'] else 0
        ck(bs[j]['q']<=c<=f['ceiling'],'refined own-work ceiling sound and pointwise no larger')
        f.update(coarse_ceiling=f['ceiling'],ceiling=c,first_intervention=first,first_frame_profile=profile,
          actual_first_post_depth_for_verification=actual_first)
        return f
'''
tail='''
    def compact(t):
        return dict(cut=t['cut'],accepted=t['accepted'],unpaid=t['unpaid'],unpaid_excess=t['unpaid_excess'],
          transfers=[[p['payer_occurrence'],v['anchor_occurrence'],v['demand_start'],v['demand_end'],v['credit_start'],v['credit_end']]
            for p in t['pools'] for v in p['loans']])
    totals=dict(rows=0,prefix=0,trees=0,cuts=0,accepted=0,rejected=0,selected=0,alternatives=0,old_successes=0,old_alternatives=0)
    summary=[];expected_matrix=[];roles=set();entry_cases=set();outer_cases=set();loose=0;strictly_improved=0
    literal=([['K',13],['K',11],['K',12],['K',2],['D',3],['D',2]]+[['K',k] for k in range(3,14)]+
      [['K',k] for k in range(1,14)]+[['K',k] for k in range(12,0,-1)]+[['D',13],['D',12]])
    ck(len(cert['witnesses'])==len(old['witnesses'])==12,'same fixed corpus; no new source word')
    for wi,(w,prior) in enumerate(zip(cert['witnesses'],old['witnesses'])):
        n=w['n'];rows=w['full_replay'];initial=w['initial_diagonal']
        ck(initial==(vine(n) if wi%2==0 else mirror(vine(n),n)),'exact diagonal vine and reflection')
        ck(w['word']==prior['word'] and w['prefix']==prior['prefix'] and rows==prior['full_replay'] and
          w['prefix_replay']==prior['prefix_replay'],'every old source word, event and state preserved')
        trees=[initial,w['cycle_initial_A'],w['cycle_initial_B']]
        for r in w['prefix_replay']+rows:trees.extend(r[k] for k in ('source_A','source_B','destination_A','destination_B'))
        for t in trees:ck(inorder(t)==list(range(1,n+1)),'strict BST and complete source key set');totals['trees']+=1
        ck([r['occurrence'] for r in rows]==list(range(len(rows))) and
          [r['occurrence'] for r in w['prefix_replay']]==[-i-1 for i in range(len(w['prefix']))],'single cycle and separate prefix provenance')
        a,b=replay(initial,initial,w['prefix'],w['prefix_replay']);ck((a,b)==(w['cycle_initial_A'],w['cycle_initial_B']),'diagonal reachability')
        aa,bb=replay(a,b,w['word'],rows);ck((aa,bb)==(a,b) and w['actual_pair_closure'],'actual paired source closure')
        bs=blocks(rows);ck(bs==w['blocks']==prior['blocks'],'independent maximal blocks')
        ck(len(w['cut_trials'])==len(w['old_UD_trials'])==len(bs),'all cuts, not only successful cuts')
        good=[];oldgood=[];chosen=None;oldchosen=None;alternative=oldalt=0
        for cut in range(len(bs)):
            fresh=independent_pass(rows,bs,cut);coarse=independent_pass(rows,bs,cut,False)
            ck(compact(fresh)==w['cut_trials'][cut] and compact(coarse)==w['old_UD_trials'][cut]==prior['cut_trials'][cut],
              'every transfer and rejected residual in each complete one-period cut')
            # Same source histories mean each new reservation is no larger, even when debts differ.
            ck(len(fresh['pools'])==len(coarse['pools']),'same actual payer pools')
            for fp,cp0 in zip(fresh['pools'],coarse['pools']):
                ck(fp['block']==cp0['block'] and fp['source_history']==cp0['source_history'] and
                  fp['reservation']<=cp0['reservation'],'pointwise reserve dominance with retained paid facts')
            if fresh['accepted']:
                good.append(cut);alternative+=len(fresh['credit_assignments']);totals['accepted']+=1
                if chosen is None:chosen=fresh
            else:totals['rejected']+=1
            if coarse['accepted']:
                oldgood.append(cut);oldalt+=len(coarse['credit_assignments']);ck(fresh['accepted'],'all old successful cuts preserved')
                if oldchosen is None:oldchosen=coarse
            totals['cuts']+=1
        ck(good==w['accepted_cuts'] and oldgood==w['old_UD_accepted_cuts']==prior['accepted_cuts'],'cut membership lists and old coverage')
        ck(chosen==w['selected_ledger'] and oldchosen==prior['selected_ledger'] and chosen['cut']==w['chosen_cut'],'full selected fresh/old certificates')
        ck(alternative==w['alternative_assignment_checks'] and oldalt==w['old_UD_alternative_assignment_checks']==prior['alternative_assignment_checks'],
          'separate full budgets for every alternative successful cut')
        A,Q,Z=sum(r['a'] for r in rows),sum(r['q'] for r in rows),sum(r['z'] for r in rows)
        ck((A,Q,Z,2*A-Q)==(w['A'],w['Q_B'],w['Z_B'],w['weight'])==
          (prior['A'],prior['Q_B'],prior['Z_B'],prior['weight']) and chosen['unused_credit_count']==2*A-Q,'all totals unchanged and conserved')
        if wi<2:
            expected=literal if wi==0 else [[m,14-x] for m,x in literal]
            ck(w['word']==expected and chosen['cut']==0 and len(rows)==44,'literal gate word and reflection')
            paying=[pool for pool in chosen['pools'] if pool['loans']]
            ck([(pool['payer_occurrence'],[(v['anchor_occurrence'],v['demand_start'],v['demand_end']) for v in pool['loans']]) for pool in paying]==
              [(1,[(0,0,3)]),(2,[(0,3,4)])],'all excess paid within first three blocks; no DELETE loan')
            payer=next(pool for pool in chosen['pools'] if pool['payer_occurrence']==2)
            cp0=next(pool for pool in oldchosen['pools'] if pool['payer_occurrence']==2)
            f=payer['facts'][0];profile=f['first_frame_profile']
            ck((f['h'],f['k'],f['coarse_ceiling'],f['ceiling'],profile['first_gain_allowance'],profile['outer_doubles'],
              profile['matching_outer_doubles'],profile['upper_depth'])==(6,1,4,1,0,2,2,2),'parent and two matching outer doubles')
            ck(profile['entry_role']=='parent' and (cp0['reservation'],payer['reservation'],payer['own_q'],payer['capacity'])==(2,1,1,2),
              'one reserved unit recovered from the same physical pool')
            ck(cp0['balances_after']==[[0,1]] and payer['balances_after']==[[0,0]],'strictly earlier repayment, not claimed new closed cycle')
            control=next(pool for pool in chosen['pools'] if pool['payer_occurrence']==3)
            ck(control['ceiling']==control['reservation']==2 and control['own_q']==1,'coarse later propagation remains non-oracle')
            span_claims=[v for v in chosen['credit_assignments'] if v['demand'][0] in (0,1,2)]
            ck(len(span_claims)==10 and len({tuple(v['credit']) for v in span_claims})==10 and
              all(v['credit'][0] in (0,1,2) for v in span_claims),'self-contained span injection with no external unit')
            expected_span=dict(indices=[0,1,2],A=5,Q_B=10,coarse_unpaid_after=1,refined_unpaid_after=0,
              recovered_pool_occurrence=2,recovered_units=1,old_ceiling=4,new_ceiling=1,old_reservation=2,new_reservation=1,
              credit_assignments=span_claims,uses_DELETE_credit=False,claims_new_closed_cycle_coverage=False)
            ck(w['span_comparison']==expected_span and good==[0]+list(range(3,44)),'exact prefix result and honest two rejected cuts')
        else:ck(w['span_comparison'] is None,'no undeclared strict local witness')
        for r in w['prefix_replay']+rows:
            if r['mode']!='K':continue
            for y in range(1,n+1):
                profile=envelope(r['source_B'],r['key'],y,r['B_events']);actual=depth(r['destination_B'],y)
                ck(actual<=profile['upper_depth']<=profile['source_depth']+2,'local envelope source matrix is an upper bound')
                roles.add(profile['entry_role'])
                if profile['entry_operation'] is not None:
                    entry_cases.add(profile['operations'][profile['entry_operation']]['case'])
                    outer_cases.update(op['case'] for op in profile['operations'][profile['entry_operation']+1:] if op['case']!='ZIG')
                loose+=profile['upper_depth']>actual;strictly_improved+=profile['upper_depth']<profile['source_depth']+2
                expected_matrix.append(dict(witness=wi,occurrence=r['occurrence'],tracked_key=y,profile=profile,actual_post_depth=actual))
        totals['rows']+=len(rows);totals['prefix']+=len(w['prefix_replay']);totals['selected']+=len(chosen['credit_assignments'])
        totals['alternatives']+=alternative;totals['old_successes']+=len(oldgood);totals['old_alternatives']+=oldalt
        summary.append(dict(name=w['name'],accepted_cuts=len(good),old_UD_accepted_cuts=len(oldgood),
          span_repayment_improved=wi<2,A=A,Q_B=Q,Z_B=Z,weight=2*A-Q))
    ck(cert['local_envelope_matrix']==expected_matrix,'all declared actual B-access/key rows independently reconstructed')
    for i in range(0,len(cert['witnesses']),2):
        w,r=cert['witnesses'][i:i+2];n=w['n']
        ck(r['initial_diagonal']==mirror(w['initial_diagonal'],n) and r['word']==[[m,n+1-x] for m,x in w['word']],'reflected source words')
        for a,b in zip(w['full_replay'],r['full_replay']):
            ck(all(b[k]==mirror(a[k],n) for k in ('source_A','source_B','destination_A','destination_B')),'both orientations, every source endpoint')
    ck(cert['finite_fits']==cert['size_sweeps']==cert['new_source_words']==cert['word_searches']==cert['source_graph_searches']==0 and
      not cert['allocation_optimizer_used'] and not cert['actual_payer_q_used_as_reservation_oracle'] and
      not cert['full_exact_depth_propagation_used'] and cert['matching_terminal_line']=='FROZEN' and
      cert['strict_closed_walk_class_enlargement']=='NOT ESTABLISHED','scope, exact-oracle boundary and honest class claim')
    ck(loose>0 and {'LL','RR','LR','RL','ZIG'}<=entry_cases and {'LL','RR','LR','RL'}<=outer_cases,'loose envelopes and all source orientations corroborated')
    result=dict(status='PASS',date='2026-10-31',complete_cycle_source_rows=totals['rows'],complete_diagonal_prefix_rows=totals['prefix'],
      pointer_source_accesses=calls,strict_BST_tree_occurrences_validated=totals['trees'],block_cut_trials_verified=totals['cuts'],
      accepted_trial_ledgers=totals['accepted'],rejected_trials_with_unpaid_debt=totals['rejected'],selected_ledger_credit_assignments=totals['selected'],
      alternative_ledger_assignment_checks=totals['alternatives'],prior_successful_UD_cuts_preserved=totals['old_successes'],
      old_UD_alternative_assignment_checks=totals['old_alternatives'],old_source_words_preserved=12,new_source_words=0,
      source_envelope_matrix_rows=len(expected_matrix),loose_envelope_rows=loose,rows_improving_uniform_plus_two=strictly_improved,
      entry_roles_observed=sorted(roles),entry_cases_observed=sorted(entry_cases),outer_double_cases_observed=sorted(outer_cases),
      no_credit_reuse=True,one_reservation_per_pool=True,no_second_lap_or_external_span_credit=True,
      prefix_A=5,prefix_Q_B=10,prefix_old_unpaid=1,prefix_new_unpaid=0,recovered_payer_units=1,
      first_frame_envelope='PROVED—UNIVERSAL, analytic FI01',charging_corollary='PROVED—RESTRICTED DOMAIN',
      strict_span_repayment='PROVED—RESTRICTED DOMAIN',strict_closed_walk_class_enlargement='NOT ESTABLISHED',universal_CD='OPEN',
      matching_terminal_line='FROZEN',producer_imported=False,old_recognizers_executed=False,
      independent_entry_detection='original source subtree membership; producer uses LCA depth',
      actual_payer_q_used_as_reservation_oracle=False,full_exact_depth_propagation_used=False,finite_fits=0,size_sweeps=0,
      witnesses=summary,certificate_sha256=hashlib.sha256(cp.read_bytes()).hexdigest())
    with (HERE/'independent_audit.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2,ensure_ascii=False);f.write('\\n')
    print(json.dumps(result,indent=2,ensure_ascii=False))

if __name__=='__main__':main()
'''
source=prefix+base+extra+scan+tail
source=source.replace('"""Pointer-source arbitrary-depth audit; no producer or old recognizer imports."""',
  '"""Pointer replay and independent source-frame entry/credit verification."""')
with (HERE/'independent_verify.py').open('x',encoding='utf-8') as f:f.write(source)
