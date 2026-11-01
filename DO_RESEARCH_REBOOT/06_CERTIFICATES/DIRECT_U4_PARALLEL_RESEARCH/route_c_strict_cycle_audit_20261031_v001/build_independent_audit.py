"""Create a standalone pointer verifier for the fixed failed generator and barrier."""
from pathlib import Path
HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'route_c_first_intervention_ceiling_20261031_v001'
prior=(OLD/'independent_verify.py').read_text(encoding='utf-8')
source=prior[:prior.index('    def search_path(')]
source=source.replace("cp=HERE/'first_intervention_certificate.json'","cp=HERE/'fixed_generator_certificate.json'")
source=source.replace('route_c_unbounded_depth_charging_20261031_v001/arbitrary_key_certificate.json',
  'route_c_first_intervention_ceiling_20261031_v001/first_intervention_certificate.json')
scan=prior[prior.index('    def independent_pass('):prior.index('    def compact(')]
scan=scan.replace('def independent_pass(rows,bs,cut,refined=True):','def ud_pass(rows,bs,cut):')
scan=scan.replace("facts=[fact(rows,bs,i,j,refined) for i in history]","facts=[coarse_fact(rows,bs,i,j) for i in history]")
source+=scan
source+='''
    def compact(t):
        return dict(cut=t['cut'],accepted=t['accepted'],unpaid=t['unpaid'],unpaid_excess=t['unpaid_excess'],
          transfers=[[p['payer_occurrence'],v['anchor_occurrence'],v['demand_start'],v['demand_end'],v['credit_start'],v['credit_end']]
            for p in t['pools'] for v in p['loans']])
    def delete_only_map(rows,bs):
        values=[b['delta'] if b['delta']>0 else (-2*b['a'] if not b['has_KEEP'] else 0) for b in bs]
        cumulative=[0]
        for v in values:cumulative.append(cumulative[-1]+v)
        total=cumulative[-1];ck(total<=0,'delete-only sufficient budget')
        cut=min(range(len(cumulative)),key=lambda j:cumulative[j])%len(bs)
        order=[(cut+j)%len(bs) for j in range(len(bs))];rotated=[values[j] for j in order]
        ck(all(sum(rotated[j:])<=0 for j in range(len(rotated))),'correct MINIMUM cut makes every suffix nonpositive')
        credits={i:[[b['leader'],e,bit] for e in range(b['a']) for bit in (0,1)] for i,b in enumerate(bs)}
        demands={i:[[t,e] for t in b['indices'] for e,ev in enumerate(rows[t]['B_events']) if ev[0]!='ZIG'] for i,b in enumerate(bs)}
        allD={tuple(d) for ds in demands.values() for d in ds};allC={tuple(c) for cs in credits.values() for c in cs}
        claims=[];usedD=set();usedC=set();pending=[];paid={};pool_visits=[]
        def claim(d,c,kind):
            dd,cc=tuple(d),tuple(c)
            ck(dd in allD and cc in allC and dd not in usedD and cc not in usedC,'one actual unit and demand; no reuse')
            usedD.add(dd);usedC.add(cc);claims.append(dict(demand=d,credit=c,kind=kind))
        debt=0;queue_history=[]
        for j in order:
            b=bs[j];capacity=2*b['a']
            if b['delta']>0:
                for d,c in zip(demands[j][:capacity],credits[j]):claim(d,c,'positive_local')
                pending.append(j);paid[j]=0;debt+=b['delta']
            elif b['has_KEEP']:
                for d,c in zip(demands[j],credits[j]):claim(d,c,'KEEP_local_only')
            else:
                ck(b['q']==0,'pure DELETE block has no own B work')
                offset=0
                for i in pending:
                    left=bs[i]['delta']-paid[i];amount=min(left,capacity-offset)
                    if not amount:continue
                    for z in range(amount):claim(demands[i][2*bs[i]['a']+paid[i]+z],credits[j][offset+z],'DELETE_only_transfer')
                    paid[i]+=amount;offset+=amount;debt-=amount
                    if offset==capacity:break
                pool_visits.append(dict(block=j,used=offset,retired=capacity-offset))
            queue_history.append(debt)
        ck(debt==0 and usedD==allD,'closed-walk deletion budget supplies every residual')
        ck(len(pool_visits)==len({v['block'] for v in pool_visits}),'each DELETE pool visited once')
        return dict(cut=cut,E=sum(max(b['delta'],0) for b in bs),C_D=sum(2*b['a'] for b in bs if not b['has_KEEP']),
          cumulative_sums=cumulative,rotated_values=rotated,queue_history=queue_history,credit_assignments=claims,pool_visits=pool_visits,
          unused_credit_count=len(allC)-len(usedC),no_reuse=True)
    valid_trees=0;orbit_rows=0;setup_rows=0;orbit_summary=[]
    canonical=[['K',x] for x in [13,11,12,9,10,7,8,5,6,3,4,1,2]]
    ck(len(cert['witnesses'])==2,'one fixed word and reflection only')
    for wi,w in enumerate(cert['witnesses']):
        n=w['n'];ck(n==13 and w['lap_cap']==64,'fixed original size and predeclared cap')
        initial=vine(13) if wi==0 else mirror(vine(13),13)
        expected_word=canonical if wi==0 else [[m,14-x] for m,x in canonical]
        expected_setup=[['D',13],['D',12]] if wi==0 else [['D',1],['D',2]]
        ck(w['initial_diagonal']==initial and w['generator']==expected_word and w['setup_prefix']==expected_setup,'literal gated source construction')
        rows=w['orbit_replay'];ck(len(rows)==10 and w['requests_executed']==10,'stopped at tenth request, no new word tried')
        trees=[initial,w['orbit_initial_A'],w['orbit_initial_B']]
        for r in w['setup_replay']+rows:trees.extend(r[k] for k in ('source_A','source_B','destination_A','destination_B'))
        for t in trees:ck(inorder(t)==list(range(1,14)),'exact source BST and fixed keys');valid_trees+=1
        a,b=replay(initial,initial,w['setup_prefix'],w['setup_replay']);ck((a,b)==(w['orbit_initial_A'],w['orbit_initial_B']),'reachable non-diagonal seed')
        ck(a!=b,'seed not already synchronized')
        pairs=[(a,b)];sync=None
        for i,r in enumerate(rows):
            ck(r['occurrence']==i,'actual orbit request identity')
            a,b=replay(a,b,[w['generator'][i]],[r]);ck((a,b) not in pairs,'no transient repeated paired state')
            pairs.append((a,b))
            if a==b:
                ck(sync is None,'stops at first equality');sync=i
        ck(sync==9==w['sync_occurrence'] and a==b and (a,b)==(w['final_A'],w['final_B']),'first exact paired synchronization at K3/reflected K11')
        ck(w['stop_reason']=='diagonal_synchronization' and w['extracted_cycle'] is None and not w['strict_closed_walk_found'],'failure honestly recorded, synchronization not called closure')
        ck(w['completed_whole_laps']==0 and w['repeat_records']==[] and w['boundary_records']==[
          dict(completed_laps=0,request_count=0,A=w['orbit_initial_A'],B=w['orbit_initial_B'])],'no unexecuted boundary/lap budget claimed')
        orbit_rows+=len(rows);setup_rows+=len(w['setup_replay'])
        orbit_summary.append(dict(name=w['name'],sync_occurrence=9,sync_key=rows[-1]['key'],requests=10,
          transient_A=sum(r['a'] for r in rows),transient_Q_B=sum(r['q'] for r in rows),
          transient_positive_occurrences=[r['occurrence'] for r in rows if r['delta']>0],new_closed_candidate=False))
    normal,reflected=cert['witnesses']
    for a,b in zip(normal['orbit_replay'],reflected['orbit_replay']):
        ck(all(b[k]==mirror(a[k],13) for k in ('source_A','source_B','destination_A','destination_B')),'mirrored full source states')
    baseline_rows=baseline_prefix=cuts=successes=alternatives=selected=0;delete_maps=[]
    ck(len(cert['delete_budget_controls'])==len(old['witnesses'])==12,'fixed prior control corpus')
    for w,saved in zip(old['witnesses'],cert['delete_budget_controls']):
        n=w['n'];rows=w['full_replay'];initial=w['initial_diagonal']
        trees=[initial,w['cycle_initial_A'],w['cycle_initial_B']]
        for r in w['prefix_replay']+rows:trees.extend(r[k] for k in ('source_A','source_B','destination_A','destination_B'))
        for t in trees:ck(inorder(t)==list(range(1,n+1)),'baseline raw BST provenance');valid_trees+=1
        a,b=replay(initial,initial,w['prefix'],w['prefix_replay']);ck((a,b)==(w['cycle_initial_A'],w['cycle_initial_B']),'baseline reachability')
        aa,bb=replay(a,b,w['word'],rows);ck((aa,bb)==(a,b),'baseline actual paired closure')
        bs=blocks(rows);ck(bs==w['blocks'],'baseline exact source blocks')
        E=sum(max(b0['delta'],0) for b0 in bs);CD=sum(2*b0['a'] for b0 in bs if not b0['has_KEEP'])
        good=[];chosen=None
        for cut in range(len(bs)):
            t=ud_pass(rows,bs,cut);ck(compact(t)==w['old_UD_trials'][cut],'all old UD cut transfers/residuals unchanged')
            if t['accepted']:
                good.append(cut);alternatives+=len(t['credit_assignments'])
                if chosen is None:chosen=t
            cuts+=1
        ck(saved==dict(name=w['name'],E=E,C_D=CD,delete_dominated=E<=CD,old_UD_accepted_cuts=good,source_word_changed=False),'source-derived barrier values')
        ck(E<=CD and good,'all listed prior cycles belong to the deletion-budget sufficient class')
        dmap=delete_only_map(rows,bs);ck(dmap['cut'] in good,'explicit minimum cut is also old-UD accepted')
        ck(len(dmap['credit_assignments'])==w['Q_B'] and dmap['unused_credit_count']==w['weight'],'DELETE-only accounting and all own KEEP work')
        delete_maps.append(dict(name=w['name'],**dmap));successes+=len(good);selected+=len(chosen['credit_assignments'])
        baseline_rows+=len(rows);baseline_prefix+=len(w['prefix_replay'])
    ck(not cert['strict_new_closed_walk_coverage'] and cert['strictness_success_criterion_unchanged'],'strictness target not redefined after failure')
    ck(cert['finite_fits']==cert['size_sweeps']==cert['adaptive_word_searches']==0 and cert['fixed_generator_attempts']==1 and
      not cert['allocation_optimizer_used'] and cert['matching_terminal_line']=='FROZEN','scope and freeze')
    with (HERE/'delete_budget_certificates.json').open('x',encoding='utf-8') as f:json.dump(delete_maps,f,indent=2,ensure_ascii=False);f.write('\\n')
    result=dict(status='PASS',date='2026-10-31',strict_new_closed_walk_coverage='NOT ESTABLISHED',
      fixed_generator='REFUTED—EXACT as a strictness witness: synchronization after ten KEEPs',
      new_orbit_source_rows=orbit_rows,new_setup_rows=setup_rows,baseline_cycle_source_rows=baseline_rows,
      baseline_prefix_rows=baseline_prefix,pointer_source_accesses=calls,strict_BST_tree_occurrences_validated=valid_trees,
      baseline_UD_cuts_verified=cuts,baseline_UD_successes=successes,baseline_UD_alternative_assignment_checks=alternatives,
      baseline_UD_selected_assignments=selected,DELETE_only_assignment_checks=sum(len(v['credit_assignments']) for v in delete_maps),
      DELETE_only_cut_direction='minimum cumulative sum; CW00A corrects original draft',
      new_closed_candidates_extracted=0,new_UD_FI_cycle_cut_trials=0,new_closed_cycle_assignments=0,
      no_credit_reuse=True,no_prefix_or_second_lap_credit=True,old_FI_cut_statuses_preserved_by_pins_not_reexecuted=True,
      original_source_words_preserved=12,fixed_generator_attempts=1,adaptive_word_searches=0,size_sweeps=0,finite_fits=0,
      producer_imported=False,old_recognizers_executed=False,matching_terminal_line='FROZEN',universal_CD='OPEN',
      source_generator_orbits=orbit_summary,certificate_sha256=hashlib.sha256(cp.read_bytes()).hexdigest())
    with (HERE/'independent_audit.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2,ensure_ascii=False);f.write('\\n')
    print(json.dumps(result,indent=2,ensure_ascii=False))

if __name__=='__main__':main()
'''
source=source.replace('"""Pointer replay and independent source-frame entry/credit verification."""',
  '"""Independent pointer proof of synchronization and DELETE-budget unit certification."""')
with (HERE/'independent_verify.py').open('x',encoding='utf-8') as f:f.write(source)
