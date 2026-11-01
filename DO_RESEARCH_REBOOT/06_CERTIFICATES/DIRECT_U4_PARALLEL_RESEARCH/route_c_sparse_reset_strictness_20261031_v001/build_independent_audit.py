"""Create a separate pointer auditor for the complete single-reset classification."""
from pathlib import Path
HERE=Path(__file__).resolve().parent
PARENT=HERE.parent
FI=PARENT/'route_c_first_intervention_ceiling_20261031_v001'
CW=PARENT/'route_c_strict_cycle_audit_20261031_v001'
prior=(FI/'independent_verify.py').read_text(encoding='utf-8')
source=prior[:prior.index('    totals=dict(')]
source=source.replace("cp=HERE/'first_intervention_certificate.json'","cp=HERE/'sparse_reset_certificate.json'")
source='\n'.join(line for line in source.split('\n') if not line.strip().startswith('old=json.loads('))
cw=(CW/'independent_verify.py').read_text(encoding='utf-8')
source+=cw[cw.index('    def delete_only_map('):cw.index('    valid_trees=0;')]
source+='''
    def digest_pair(a,b):return hashlib.sha256(json.dumps([a,b],separators=(',',':')).encode('utf-8')).hexdigest()
    def compact_row(r):
        v={k:x for k,x in r.items() if k not in ('source_A','source_B','destination_A','destination_B')}
        v.update(source_pair_sha256=digest_pair(r['source_A'],r['source_B']),
          destination_pair_sha256=digest_pair(r['destination_A'],r['destination_B']))
        return v
    def advance(a,b,mode,x,occ):
        aa,ae,da,_,_=access(a,x)
        if mode=='K':bb,be,db,q,z=access(b,x)
        else:bb,be,db,q,z=b,[],None,0,0
        r=dict(occurrence=occ,mode=mode,key=x,source_A=a,source_B=b,destination_A=aa,destination_B=bb,
          d_A=da,d_B=db,a=len(ae),q=q,z=z,A_events=ae,B_events=be,delta=q-2*len(ae))
        return aa,bb,r
    def mirrored_events(es):
        case_map={'LL':'RR','RR':'LL','LR':'RL','RL':'LR','ZIG':'ZIG'}
        orient_map={'L':'R','R':'L','-':'-'}
        return [[case_map[e[0]],14-e[2],14-e[1],orient_map[e[3]]] for e in es]
    def mirrored_row(r):
        out=dict(r,key=14-r['key'],A_events=mirrored_events(r['A_events']),B_events=mirrored_events(r['B_events']))
        for k in ('source_A','source_B','destination_A','destination_B'):out[k]=mirror(r[k],13)
        return out
    valid_trees=0
    def validate_row(r):
        nonlocal valid_trees
        for k in ('source_A','source_B','destination_A','destination_B'):
            ck(inorder(r[k])==list(range(1,14)),'strict raw BST and complete fixed key set');valid_trees+=1
    skeleton=[13,11,12,9,10,7,8,5,6,3,4,1,2]
    expected_parameters=[(g,t) for g in range(2,13) for t in range(1,14) if t not in (skeleton[g],skeleton[(g+1)%13])]
    ck(len(expected_parameters)==121 and cert['declared_parameter_count']==121 and cert['skeleton']==skeleton,'entire gated finite parameter class')
    ck([(v['gap'],v['target']) for v in cert['cases']]==expected_parameters and cert['all_declared_cases_examined'],'no parameter replacement or omitted case')
    initial=vine(13);mirror_initial=mirror(initial,13);valid_trees+=2
    ck(cert['initial_diagonal']==initial and cert['setup_prefix']==[['D',13],['D',12]],'fixed seed and reachability prefix')
    a0=b0=initial;ma0=mb0=mirror_initial
    for i,(mode,x) in enumerate(cert['setup_prefix']):
        a0,b0,r=advance(a0,b0,mode,x,-i-1);ma0,mb0,mr=advance(ma0,mb0,mode,14-x,-i-1)
        ck(r==cert['setup_replay'][i] and mr==mirrored_row(r),'both exact setup orientations')
        validate_row(r);validate_row(mr)
    ck((a0,b0)==(cert['orbit_initial_A'],cert['orbit_initial_B']),'source setup endpoints')
    outcomes={};period_counts={};funding_counts={};shared_B={};maps=[];orbit_rows=0;cycle_rows=0;max_laps=0
    non_diag=0;non_diag_positive=0;UD_units=DELETE_units=0;all_primitive=True
    for ci,case in enumerate(cert['cases']):
        g,t=case['gap'],case['target'];word=[]
        for pos,key in enumerate(skeleton):
            word.append(['K',key])
            if pos==g:word.append(['D',t])
        ck(case['word']==word and case['lap_cap']==64,'literal single-reset generator and cap')
        a,b=a0,b0;ma,mb=ma0,mb0;rows=[];mrows=[]
        seen={json.dumps([a,b],separators=(',',':')):0};start=end=None;boundary_records=[dict(lap=0,A=a,B=b)]
        ck(len(case['orbit_replay'])%14==0,'complete whole-word boundary observation')
        total_laps=len(case['orbit_replay'])//14;ck(1<=total_laps<=64,'predeclared bound')
        for lap in range(1,total_laps+1):
            for mode,x in word:
                occ=len(rows);a,b,r=advance(a,b,mode,x,occ);ma,mb,mr=advance(ma,mb,mode,14-x,occ)
                ck(compact_row(r)==case['orbit_replay'][occ] and mr==mirrored_row(r),'source digests, all costs/events and exact reflected states')
                validate_row(r);validate_row(mr);rows.append(r);mrows.append(mr)
                if mode=='D':
                    ck(r['a']>=1 and a[0]==t and b[0]==skeleton[g] and a[0]!=b[0],'pure positive-cost reset separates roots')
                    if (g,t)==(2,13):ck(r['a']==1,'exact cheap-reset identity')
            boundary_records.append(dict(lap=lap,A=a,B=b))
            if lap in shared_B:ck(shared_B[lap]==b,'B source orbit independent of reset placement')
            else:shared_B[lap]=b
            state=json.dumps([a,b],separators=(',',':'))
            if state in seen:
                ck(lap==total_laps,'first repeated boundary, not a later selected loop')
                start=14*seen[state];end=len(rows);break
            seen[state]=lap
        ck(start is not None and case['cycle'] is not None,'all 121 reached exact recurrence, none capped')
        ck(boundary_records==case['boundaries'],'all stored exact boundary pairs')
        cyc=[dict(r,occurrence=i) for i,r in enumerate(rows[start:end])]
        mcyc=[dict(r,occurrence=i) for i,r in enumerate(mrows[start:end])]
        ck((cyc[-1]['destination_A'],cyc[-1]['destination_B'])==(cyc[0]['source_A'],cyc[0]['source_B']),'actual normal paired closure')
        ck((mcyc[-1]['destination_A'],mcyc[-1]['destination_B'])==(mcyc[0]['source_A'],mcyc[0]['source_B']),'actual reflected paired closure')
        unique={json.dumps([r['source_A'],r['source_B']],separators=(',',':')) for r in cyc}
        ck(len(unique)==len(cyc),'primitive source cycle; no internal pair repeat')
        bs=blocks(cyc);mbs=blocks(mcyc)
        E=sum(max(v['delta'],0) for v in bs);CD=sum(2*v['a'] for v in bs if not v['has_KEEP'])
        diag=[r['occurrence'] for r in cyc if r['source_A']==r['source_B']]
        meta=dict(transient_laps=start//14,period_laps=(end-start)//14,cycle_length=len(cyc),E=E,C_D=CD,
          A=sum(r['a'] for r in cyc),Q_B=sum(r['q'] for r in cyc),Z_B=sum(r['z'] for r in cyc),
          diagonal_source_occurrences=diag,reset_costs=[r['a'] for r in cyc if r['mode']=='D'],actual_pair_closure=True)
        ck(meta==case['cycle'],'source-derived recurrence, non-diagonality, costs and budget')
        ck(len(meta['reset_costs'])==meta['period_laps'] and CD==2*sum(meta['reset_costs']),'one pure DELETE pool per period')
        outcome='DIAGONAL_IN_CYCLE' if diag else ('DELETE_DOMINATED' if E<=CD else 'SURVIVOR')
        ck(E<=CD and outcome==case['outcome'] and case['comparison'] is None,'all cases independently fail the mandatory excess filter')
        # One concrete accepting old-UD cut is sufficient to disprove rejection at every cut.
        dmap=delete_only_map(cyc,bs);mdmap=delete_only_map(mcyc,mbs)
        ud=independent_pass(cyc,bs,dmap['cut'],False);mud=independent_pass(mcyc,mbs,mdmap['cut'],False)
        ck(ud['accepted'] and mud['accepted'] and dmap['cut']==mdmap['cut'],'old UD acceptance in each orientation')
        ck(ud['credit_assignments']==mud['credit_assignments'] and dmap['credit_assignments']==mdmap['credit_assignments'],
          'same distinct event-unit map under reflection, separate resource budgets')
        ck(len(ud['credit_assignments'])==len(dmap['credit_assignments'])==meta['Q_B'],'every B double funded once in either alternative proof')
        UD_units+=2*len(ud['credit_assignments']);DELETE_units+=2*len(dmap['credit_assignments'])
        maps.append(dict(case_index=ci,gap=g,target=t,E=E,C_D=CD,cycle_length=len(cyc),old_UD_accepted_cut=dmap['cut'],
          normal_UD_ledger=ud,normal_DELETE_only_map=dmap,reflected_maps_independently_checked=True,
          mirrored_assignments_equal_normal=True,alternative_budgets_not_combined=True))
        outcomes[outcome]=outcomes.get(outcome,0)+1
        key=(meta['transient_laps'],meta['period_laps']);period_counts[str(key)]=period_counts.get(str(key),0)+1
        key=(E,CD,not diag);funding_counts[str(key)]=funding_counts.get(str(key),0)+1
        if not diag:non_diag+=1;non_diag_positive+=E>0
        orbit_rows+=2*len(rows);cycle_rows+=2*len(cyc);max_laps=max(max_laps,total_laps)
    ck({str(k):v for k,v in shared_B.items()}==cert['shared_B_boundary_states'],'complete shared B recurrence')
    ck(outcomes==cert['outcome_counts']=={'DIAGONAL_IN_CYCLE':90,'DELETE_DOMINATED':31},'complete finite outcome classification')
    ck(cert['all_examined_orbits_closed'] and not cert['strict_new_closed_walk_coverage'] and cert['strict_witness'] is None and
      not cert['stopped_at_first_strict_witness'],'no strictness promotion or capped case hidden')
    ck(cert['finite_fits']==cert['size_sweeps']==cert['adaptive_generator_changes']==0 and
      not cert['old_UD_FI_rules_changed'] and not cert['actual_payer_q_used_as_reservation_oracle'] and
      cert['matching_terminal_line']=='FROZEN','fixed scope and frozen architecture')
    with (HERE/'old_UD_acceptance_certificates.json').open('x',encoding='utf-8') as f:json.dump(maps,f,indent=2,ensure_ascii=False);f.write('\\n')
    result=dict(status='PASS',date='2026-10-31',fixed_key_size=13,fixed_reset_parameter_cases=121,source_orientations_per_case=2,
      complete_exact_orbit_classification=True,cap_limited_cases=0,max_laps_to_first_repeat=max_laps,
      primitive_period_laps_observed=[1,2],new_normal_and_reflected_orbit_rows=orbit_rows,
      normal_and_reflected_recurrent_cycle_rows=cycle_rows,setup_source_rows=4,pointer_source_accesses=calls,
      strict_BST_tree_occurrences_validated=valid_trees,non_diagonal_cycles=non_diag,
      non_diagonal_cycles_with_positive_excess=non_diag_positive,cycles_with_diagonal_state=90,
      cases_satisfying_E_greater_C_D=0,all_cases_old_UD_covered=True,explicit_old_UD_cut_certificates=242,
      old_UD_unit_assignment_checks=UD_units,DELETE_only_unit_assignment_checks=DELETE_units,
      new_survivor_all_cut_comparisons=0,new_FI_only_closed_walks=0,strict_new_closed_walk_coverage='NOT ESTABLISHED',
      no_credit_reuse=True,alternative_maps_and_orientations_have_separate_budgets=True,no_prefix_or_second_lap_credit=True,
      producer_imported=False,old_recognizers_executed=False,finite_fits=0,size_sweeps=0,adaptive_generator_changes=0,
      matching_terminal_line='FROZEN',universal_CD='OPEN',
      period_classification=period_counts,funding_classification=funding_counts,
      certificate_sha256=hashlib.sha256(cp.read_bytes()).hexdigest())
    with (HERE/'independent_audit.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2,ensure_ascii=False);f.write('\\n')
    print(json.dumps(result,indent=2,ensure_ascii=False))

if __name__=='__main__':main()
'''
source=source.replace('"""Pointer replay and independent source-frame entry/credit verification."""',
  '"""Independent pointer classification and exact old-UD certificates for sparse resets."""')
with (HERE/'independent_verify.py').open('x',encoding='utf-8') as f:f.write(source)
