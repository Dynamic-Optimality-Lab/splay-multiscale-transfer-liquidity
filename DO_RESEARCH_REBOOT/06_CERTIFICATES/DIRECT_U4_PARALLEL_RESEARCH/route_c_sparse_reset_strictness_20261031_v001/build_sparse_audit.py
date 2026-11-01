"""Generate the one-reset source classification auditor with exclusive creation."""
from pathlib import Path
HERE=Path(__file__).resolve().parent
FI=HERE.parent/'route_c_first_intervention_ceiling_20261031_v001'
old=(FI/'audit_first_intervention.py').read_text(encoding='utf-8')
source=old[:old.index('    oldcert=json.loads(')]
source=source.replace('route_c_unbounded_depth_charging_20261031_v001','route_c_strict_cycle_audit_20261031_v001')
source=source.replace('"""Single first-intervention frame ceiling; fixed old source corpus, no fit."""',
  '"""Exact finite one-reset classification at the fixed thirteen-key size."""')
source+='''
    skeleton=[13,11,12,9,10,7,8,5,6,3,4,1,2]
    initial=s.vine(13);setup_word=[['D',13],['D',12]];a0=b0=initial;setup=[]
    for k,(mode,x) in enumerate(setup_word):a0,b0,r0=step(a0,b0,mode,x,-k-1);setup.append(r0)
    def digest_pair(a,b):
        return hashlib.sha256(json.dumps([a,b],separators=(',',':')).encode('utf-8')).hexdigest()
    def compact_row(r0):
        d={k:v for k,v in r0.items() if k not in ('source_A','source_B','destination_A','destination_B')}
        d['source_pair_sha256']=digest_pair(r0['source_A'],r0['source_B'])
        d['destination_pair_sha256']=digest_pair(r0['destination_A'],r0['destination_B'])
        return d
    def orbit(gap,target):
        word=[]
        for pos,key in enumerate(skeleton):
            word.append(['K',key])
            if pos==gap:word.append(['D',target])
        a,b=a0,b0;seen={(a,b):0};rows=[]
        boundaries=[dict(lap=0,A=raw(a),B=raw(b))];start=end=None
        for lap in range(1,65):
            for mode,x in word:
                a,b,r0=step(a,b,mode,x,len(rows));rows.append(r0)
                if mode=='D':
                    assert r0['a']>=1 and r0['destination_A'][0]==target
                    assert r0['destination_B'][0]==skeleton[gap] and r0['destination_A'][0]!=r0['destination_B'][0]
                    if gap==2 and target==13:assert r0['a']==1
            boundaries.append(dict(lap=lap,A=raw(a),B=raw(b)))
            if (a,b) in seen:start=14*seen[(a,b)];end=len(rows);break
            seen[(a,b)]=lap
        meta=None;test=None;full=None
        if start is None:outcome='OPEN_LAP_CAP'
        else:
            cycle=[dict(r0,occurrence=k) for k,r0 in enumerate(rows[start:end])]
            assert cycle[-1]['destination_A']==cycle[0]['source_A'] and cycle[-1]['destination_B']==cycle[0]['source_B']
            bs=blocks(cycle);E=sum(max(v['delta'],0) for v in bs);CD=sum(2*v['a'] for v in bs if not v['has_KEEP'])
            diagonal=[r0['occurrence'] for r0 in cycle if r0['source_A']==r0['source_B']]
            meta=dict(transient_laps=start//14,period_laps=(end-start)//14,cycle_length=len(cycle),E=E,C_D=CD,
              A=sum(r0['a'] for r0 in cycle),Q_B=sum(r0['q'] for r0 in cycle),Z_B=sum(r0['z'] for r0 in cycle),
              diagonal_source_occurrences=diagonal,reset_costs=[r0['a'] for r0 in cycle if r0['mode']=='D'],actual_pair_closure=True)
            if diagonal:outcome='DIAGONAL_IN_CYCLE'
            elif E<=CD:outcome='DELETE_DOMINATED'
            else:
                coarse=[scan(cycle,bs,cut,False) for cut in range(len(bs))]
                fresh=[scan(cycle,bs,cut,True) for cut in range(len(bs))]
                oldgood=[v for v in coarse if v['accepted']];good=[v for v in fresh if v['accepted']]
                assert {v['cut'] for v in oldgood}<={v['cut'] for v in good}
                test=dict(old_UD_trials=[compact(v) for v in coarse],FI_trials=[compact(v) for v in fresh],
                  old_UD_accepted_cuts=[v['cut'] for v in oldgood],FI_accepted_cuts=[v['cut'] for v in good],
                  selected_FI_ledger=good[0] if good else None,
                  FI_alternative_assignment_checks=sum(len(v['credit_assignments']) for v in good),
                  UD_alternative_assignment_checks=sum(len(v['credit_assignments']) for v in oldgood))
                outcome='UD_ACCEPTS' if oldgood else ('STRICT_FOUND' if good else 'FI_REJECTS')
                if outcome=='STRICT_FOUND':full=dict(full_orbit_replay=rows,full_cycle_replay=cycle,
                  full_reachability_replay=setup+rows[:start],cycle_blocks=bs)
        case=dict(gap=gap,target=target,word=word,lap_cap=64,boundaries=boundaries,
          orbit_replay=[compact_row(r0) for r0 in rows],cycle=meta,comparison=test,outcome=outcome)
        return case,full
    cases=[];strict=None;shared_B={};counts={}
    for gap in range(2,13):
        for target in range(1,14):
            if target in (skeleton[gap],skeleton[(gap+1)%13]):continue
            case,full=orbit(gap,target);cases.append(case)
            for boundary in case['boundaries']:
                lap=boundary['lap']
                if lap in shared_B:assert shared_B[lap]==boundary['B']
                else:shared_B[lap]=boundary['B']
            counts[case['outcome']]=counts.get(case['outcome'],0)+1
            if len(cases)%16==0 or case['comparison'] is not None:
                print(json.dumps(dict(processed=len(cases),gap=gap,target=target,outcome=case['outcome'],counts=counts)),flush=True)
            if full is not None:
                strict=dict(case_index=len(cases)-1,**full);break
        if strict is not None:break
    cert=dict(schema='fixed-thirteen-key-single-reset-classification-v1',date='2026-10-31',skeleton=skeleton,
      initial_diagonal=raw(initial),setup_prefix=setup_word,setup_replay=setup,orbit_initial_A=raw(a0),orbit_initial_B=raw(b0),
      declared_parameter_count=121,cases=cases,shared_B_boundary_states=shared_B,outcome_counts=counts,strict_witness=strict,
      strict_new_closed_walk_coverage=bool(strict),parameter_order='gap 2..12, target 1..13, exclude adjacent KEEP targets',
      stopped_at_first_strict_witness=bool(strict),all_declared_cases_examined=len(cases)==121,
      all_examined_orbits_closed=all(v['outcome']!='OPEN_LAP_CAP' for v in cases),
      finite_fits=0,size_sweeps=0,adaptive_generator_changes=0,lap_cap=64,matching_terminal_line='FROZEN',universal_CD='OPEN',
      old_UD_FI_rules_changed=False,actual_payer_q_used_as_reservation_oracle=False)
    save('sparse_reset_certificate.json',cert)
    print(json.dumps(dict(preserved_files=len(pins),stage_files=len(stage),processed=len(cases),outcomes=counts,
      strict_new_closed_walk_coverage=bool(strict),strict_case=strict and {k:cases[strict['case_index']][k] for k in ('gap','target','cycle')}),indent=2))

if __name__=='__main__':main()
'''
with (HERE/'audit_sparse_resets.py').open('x',encoding='utf-8') as f:f.write(source)
