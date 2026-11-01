"""Create a standalone pointer auditor, preserving every earlier file."""
from pathlib import Path

HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'route_c_split_shallow_charging_20261031_v001'
source=(OLD/'independent_verify.py').read_text(encoding='utf-8')

def replace_once(old,new):
    global source
    assert source.count(old)==1,old
    source=source.replace(old,new,1)

replace_once("cp=HERE/'split_shallow_certificate.json'","cp=HERE/'arbitrary_key_certificate.json'")
replace_once('route_c_cross_run_shallow_charging_20261031_v001/cross_run_shallow_certificate.json',
  'route_c_split_shallow_charging_20261031_v001/split_shallow_certificate.json')
replace_once("ck(before<=1 and 1<=h<=3,'actual root/child transport')",
  "ck(before>=0 and h>=0,'actual arbitrary-key post-anchor depth, including zero')")
start=source.index('    def old_pass(');end=source.index('    def independent_pass(',start)
source=source[:start]+source[end:]
replace_once('def independent_pass(rows,bs,cut):','def independent_pass(rows,bs,cut,shallow_only=False):')
replace_once("facts=[fact(rows,bs,i,j) for i in history if b['key'] in shallow(rows,bs,i)]",
  "facts=[fact(rows,bs,i,j) for i in history if not shallow_only or b['key'] in shallow(rows,bs,i)]")
replace_once("eligible=[i for i in history if cursor[i]<bs[i]['delta'] and b['key'] in shallow(rows,bs,i)]",
  "eligible=[i for i in history if cursor[i]<bs[i]['delta'] and (not shallow_only or b['key'] in shallow(rows,bs,i))]")
source=source[:source.index('    totals=dict(')]+'''
    def compact(t):
        return dict(cut=t['cut'],accepted=t['accepted'],unpaid=t['unpaid'],unpaid_excess=t['unpaid_excess'],
          transfers=[[p['payer_occurrence'],v['anchor_occurrence'],v['demand_start'],v['demand_end'],v['credit_start'],v['credit_end']]
            for p in t['pools'] for v in p['loans']])
    totals=dict(rows=0,prefix=0,trees=0,cuts=0,accepted=0,rejected=0,selected=0,alternatives=0,old_successes=0,old_alternatives=0)
    summary=[];zero_height=False;binding_deep=False;discarded_real_spare=False;changed_recipient_allocation=False
    literal=([['K',13],['K',11],['K',12],['K',2],['D',3],['D',2]]+[['K',k] for k in range(3,14)]+
      [['K',k] for k in range(1,14)]+[['K',k] for k in range(12,0,-1)]+[['D',13],['D',12]])
    for wi,w in enumerate(cert['witnesses']):
        strict=wi<2;n=w['n'];rows=w['full_replay'];initial=w['initial_diagonal']
        ck(initial==(vine(n) if wi%2==0 else mirror(vine(n),n)),'fixed exact diagonal source')
        trees=[initial,w['cycle_initial_A'],w['cycle_initial_B']]
        for r in w['prefix_replay']+rows:trees.extend(r[k] for k in ('source_A','source_B','destination_A','destination_B'))
        for t in trees:ck(inorder(t)==list(range(1,n+1)),'strict BST and complete fixed key set');totals['trees']+=1
        ck(w['strict_beyond_shallow']==strict and [r['occurrence'] for r in rows]==list(range(len(rows))),'single-period occurrence budget')
        ck([r['occurrence'] for r in w['prefix_replay']]==[-i-1 for i in range(len(w['prefix']))],'prefix provenance')
        a,b=replay(initial,initial,w['prefix'],w['prefix_replay']);ck((a,b)==(w['cycle_initial_A'],w['cycle_initial_B']),'diagonal reachability')
        aa,bb=replay(a,b,w['word'],rows);ck((aa,bb)==(a,b) and w['actual_pair_closure'],'actual paired closure')
        bs=blocks(rows);ck(bs==w['blocks'],'independent maximal A-root blocks')
        ck(len(w['cut_trials'])==len(w['old_SL_trials'])==len(bs),'all old/new cuts including failures')
        good=[];oldgood=[];chosen=None;alternatives=0;oldalt=0
        for cut in range(len(bs)):
            t=independent_pass(rows,bs,cut);sl=independent_pass(rows,bs,cut,True)
            ck(compact(t)==w['cut_trials'][cut] and compact(sl)==w['old_SL_trials'][cut],'all cut outcomes, transfers and unpaid tails')
            if t['accepted']:
                good.append(cut);alternatives+=len(t['credit_assignments']);totals['accepted']+=1
                if chosen is None:chosen=t
            else:totals['rejected']+=1
            if sl['accepted']:
                oldgood.append(cut);oldalt+=len(sl['credit_assignments']);ck(t['accepted'],'each previously successful shallow cut preserved')
            totals['cuts']+=1
        ck(good==w['accepted_cuts'] and oldgood==w['old_SL_accepted_cuts'] and chosen==w['selected_ledger'],'full selected ledger and membership lists')
        ck(chosen is not None and chosen['cut']==w['chosen_cut'] and alternatives==w['alternative_assignment_checks'] and
          oldalt==w['old_SL_alternative_assignment_checks'],'selected first success and separate alternative budgets')
        A,Q,Z=sum(r['a'] for r in rows),sum(r['q'] for r in rows),sum(r['z'] for r in rows)
        ck((A,Q,Z,2*A-Q)==(w['A'],w['Q_B'],w['Z_B'],w['weight']) and chosen['unused_credit_count']==2*A-Q,'source totals and unused unit conservation')
        ck(w['KEEP_support']==sorted({r['key'] for r in rows if r['mode']=='K'}),'genuine support')
        for pool in chosen['pools']:
            ck(len(pool['facts'])==len(pool['source_history']),'every historical positive fact kept, paid or unpaid, at every key')
            zero_height|=any(f['h']==0 for f in pool['facts'])
        if strict:
            expected_word=literal if wi==0 else [[m,14-x] for m,x in literal]
            expected_prefix=[['D',13],['D',12]] if wi==0 else [['D',1],['D',2]]
            ck(w['word']==expected_word and w['prefix']==expected_prefix and len(rows)==44,'pre-execution literal binding')
            ck([(r['a'],r['q'],r['delta']) for r in rows[:6]]==[(1,6,4),(3,3,-3),(1,1,-1),(1,1,-1),(3,0,-6),(1,0,-2)],'first six costs predetermined')
            ck([i for i,b in enumerate(bs) if b['delta']>0]==[0],'no unnoticed positive supplying old extra facts')
            ck(not oldgood and good==[0]+list(range(5,44)),'all-cut old rejection and four honest new failures')
            paying=[pool for pool in chosen['pools'] if pool['loans']]
            ck([(pool['payer_occurrence'],[(v['anchor_occurrence'],v['demand_start'],v['demand_end']) for v in pool['loans']]) for pool in paying]==
              [(1,[(0,0,3)]),(4,[(0,3,4)])],'one anchor split between distinct deep-key pools')
            deep=paying[0];f=deep['facts'][0]
            ck((f['pre_depth'],f['h'],f['k'],deep['own_q'],deep['capacity'],deep['reservation'])==(10,7,0,3,6,3),'deep KEEP has binding nonzero own-work reservation')
            ck(paying[0]['key'] not in shallow(rows,bs,0) and paying[1]['key'] not in shallow(rows,bs,0),'both actual lenders outside old root/child eligibility')
            ck(deep['loans'][0]['credit_start']==3 and deep['loans'][0]['credit_end']==6,'own prefix and deep loan suffix disjoint')
            p12=next(pool for pool in chosen['pools'] if pool['payer_occurrence']==2)
            p2=next(pool for pool in chosen['pools'] if pool['payer_occurrence']==3)
            ck((p12['ceiling'],p12['reservation'],p12['own_q'])==(4,2,1) and
              (p2['ceiling'],p2['reservation'],p2['own_q'])==(2,2,1),'conservative bounds discard actual spare; no exact-surplus oracle')
            binding_deep=True;discarded_real_spare=True
            ck(rows[16]['destination_A']==rows[16]['destination_B'],'synchronization by KEEP13')
            ck((A,Q,Z,2*A-Q)==(68,35,30,101),'exact new totals')
        else:
            prior=old['witnesses'][wi-2]
            ck(rows==prior['full_replay'] and w['prefix_replay']==prior['prefix_replay'] and w['word']==prior['word'] and w['prefix']==prior['prefix'],
              'all ten prior source words and prefixes unchanged')
            ck(w['old_SL_trials']==prior['cut_trials'] and oldgood==prior['accepted_cuts'] and
              oldalt==prior['alternative_assignment_checks'],'old per-cut transfer certificates unchanged')
            ck((A,Q,Z,2*A-Q)==(prior['A'],prior['Q_B'],prior['Z_B'],prior['weight']),'old totals unchanged')
            changed_recipient_allocation|=chosen['credit_assignments']!=prior['selected_ledger']['credit_assignments']
        totals['rows']+=len(rows);totals['prefix']+=len(w['prefix_replay']);totals['selected']+=len(chosen['credit_assignments'])
        totals['alternatives']+=alternatives;totals['old_successes']+=len(oldgood);totals['old_alternatives']+=oldalt
        summary.append(dict(name=w['name'],A=A,Q_B=Q,Z_B=Z,weight=2*A-Q,accepted_cuts=len(good),old_SL_accepted_cuts=len(oldgood)))
    for i in range(0,len(cert['witnesses']),2):
        w,r=cert['witnesses'][i:i+2];n=w['n']
        ck(r['initial_diagonal']==mirror(w['initial_diagonal'],n) and r['word']==[[m,n+1-x] for m,x in w['word']],'reflected literal')
        for a,b in zip(w['full_replay'],r['full_replay']):
            ck(all(b[k]==mirror(a[k],n) for k in ('source_A','source_B','destination_A','destination_B')),'both orientations at every physical endpoint')
    ck(len(cert['witnesses'])==12 and cert['finite_fits']==cert['size_sweeps']==cert['word_searches']==cert['source_graph_searches']==0 and
      not cert['allocation_optimizer_used'] and not cert['actual_payer_q_used_as_reservation_oracle'] and cert['matching_terminal_line']=='FROZEN','scope and freeze')
    ck(binding_deep and discarded_real_spare and zero_height and changed_recipient_allocation,'load-bearing deep/zero-height/conservative/changed-allocation coverage')
    result=dict(status='PASS',date='2026-10-31',complete_cycle_source_rows=totals['rows'],complete_diagonal_prefix_rows=totals['prefix'],
      pointer_source_accesses=calls,strict_BST_tree_occurrences_validated=totals['trees'],block_cut_trials_verified=totals['cuts'],
      accepted_trial_ledgers=totals['accepted'],rejected_trials_with_unpaid_debt=totals['rejected'],
      selected_ledger_credit_assignments=totals['selected'],alternative_ledger_assignment_checks=totals['alternatives'],
      old_SL_alternative_assignment_checks=totals['old_alternatives'],prior_successful_SL_cuts_preserved=totals['old_successes'],
      old_source_controls_preserved=10,no_credit_reuse=True,all_source_facts_retained_after_payment=True,
      one_reservation_and_retirement_per_pool=True,no_second_lap_or_prefix_credit=True,alternative_ledgers_are_not_combined=True,
      strict_extension_of_SL=True,deep_KEEP_with_nonzero_own_B_work_verified=True,zero_post_height_verified=True,
      total_debt_containment_does_not_assume_identical_recipient_allocations=True,source_reachability_and_pair_closure=True,
      producer_imported=False,old_recognizers_executed=False,actual_payer_q_used_as_reservation_oracle=False,
      allocation_optimizer_used=False,finite_fits=0,size_sweeps=0,restricted_class='PROVED—RESTRICTED DOMAIN',universal_CD='OPEN',
      matching_terminal_line='FROZEN',all_size_result='UD01 source/ledger theorem and UD02 analytic fringe/scan family; not finite extrapolation',
      witnesses=summary,certificate_sha256=hashlib.sha256(cp.read_bytes()).hexdigest())
    with (HERE/'independent_audit.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2,ensure_ascii=False);f.write('\\n')
    print(json.dumps(result,indent=2,ensure_ascii=False))

if __name__=='__main__':main()
'''
source=source.replace('"""Pointer-source audit and independent one-period split-ledger verification."""',
  '"""Pointer-source arbitrary-depth audit; no producer or old recognizer imports."""')
with (HERE/'independent_verify.py').open('x',encoding='utf-8') as f:f.write(source)
