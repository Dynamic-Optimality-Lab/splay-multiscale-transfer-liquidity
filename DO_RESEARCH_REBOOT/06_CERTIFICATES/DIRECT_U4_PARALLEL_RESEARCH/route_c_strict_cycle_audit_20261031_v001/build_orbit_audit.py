"""Generate a standalone fixed-orbit auditor; preserve earlier scripts as text."""
from pathlib import Path
HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'route_c_first_intervention_ceiling_20261031_v001'
prior=(OLD/'audit_first_intervention.py').read_text(encoding='utf-8')
source=prior[:prior.index('    oldcert=json.loads(')]
source=source.replace('route_c_unbounded_depth_charging_20261031_v001','route_c_first_intervention_ceiling_20261031_v001')
source=source.replace('"""Single first-intervention frame ceiling; fixed old source corpus, no fit."""',
  '"""One fixed thirteen-key KEEP generator, exact pair orbit, no adaptive fitting."""')
source+='''
    def fixed_orbit(name,initial,n,prefix,word):
        a=b=initial;setup=[]
        for k,(mode,x) in enumerate(prefix):a,b,r0=step(a,b,mode,x,-k-1);setup.append(r0)
        start_a,start_b=a,b
        boundaries=[dict(completed_laps=0,request_count=0,A=raw(a),B=raw(b))]
        seen={(a,b):0};allstates={(a,b):0};rows=[];repeat_records=[]
        reason='lap_limit';cycle_start=None;cycle_end=None;sync_at=None;completed=0
        for lap in range(64):
            for mode,x in word:
                a,b,r0=step(a,b,mode,x,len(rows));rows.append(r0)
                if (a,b) in allstates:repeat_records.append([allstates[(a,b)],len(rows)])
                else:allstates[(a,b)]=len(rows)
                if a==b:reason='diagonal_synchronization';sync_at=len(rows)-1;break
            if sync_at is not None:break
            completed=lap+1
            boundaries.append(dict(completed_laps=completed,request_count=len(rows),A=raw(a),B=raw(b)))
            if (a,b) in seen:
                reason='repeated_boundary_pair';cycle_start=seen[(a,b)]*len(word);cycle_end=len(rows);break
            seen[(a,b)]=completed
        extracted=None
        if reason=='repeated_boundary_pair':
            cyc=[dict(r0,occurrence=k) for k,r0 in enumerate(rows[cycle_start:cycle_end])]
            assert cyc[-1]['destination_A']==cyc[0]['source_A'] and cyc[-1]['destination_B']==cyc[0]['source_B']
            bs=blocks(cyc);fresh=[scan(cyc,bs,c) for c in range(len(bs))];coarse=[scan(cyc,bs,c,False) for c in range(len(bs))]
            good=[t for t in fresh if t['accepted']];oldgood=[t for t in coarse if t['accepted']]
            assert {t['cut'] for t in oldgood}<={t['cut'] for t in good}
            E=sum(max(b0['delta'],0) for b0 in bs);CD=sum(2*b0['a'] for b0 in bs if not b0['has_KEEP'])
            if E<=CD:assert oldgood
            extracted=dict(source_start_index=cycle_start,source_end_index=cycle_end,period_laps=(cycle_end-cycle_start)//len(word),
              full_replay=cyc,blocks=bs,E=E,C_D=CD,old_UD_trials=[compact(t) for t in coarse],FI_trials=[compact(t) for t in fresh],
              old_UD_accepted_cuts=[t['cut'] for t in oldgood],FI_accepted_cuts=[t['cut'] for t in good],
              selected_FI_ledger=good[0] if good else None,strict_FI_not_UD=bool(good) and not oldgood,
              A=sum(r0['a'] for r0 in cyc),Q_B=sum(r0['q'] for r0 in cyc),Z_B=sum(r0['z'] for r0 in cyc),
              actual_pair_closure=True)
        if reason=='diagonal_synchronization':
            assert a==b and not repeat_records
        return dict(name=name,n=n,initial_diagonal=raw(initial),setup_prefix=prefix,setup_replay=setup,
          orbit_initial_A=raw(start_a),orbit_initial_B=raw(start_b),generator=word,lap_cap=64,orbit_replay=rows,
          boundary_records=boundaries,repeat_records=repeat_records,stop_reason=reason,sync_occurrence=sync_at,
          completed_whole_laps=completed,requests_executed=len(rows),final_A=raw(a),final_B=raw(b),extracted_cycle=extracted,
          strict_closed_walk_found=bool(extracted and extracted['strict_FI_not_UD']))
    n=13;initial=s.vine(n);prefix=[['D',13],['D',12]]
    word=[['K',x] for x in [13,11,12,9,10,7,8,5,6,3,4,1,2]]
    normal=fixed_orbit('fixed_descending_pairs',initial,n,prefix,word)
    reflected=fixed_orbit('fixed_descending_pairs_reflection',mirror(initial,n),n,
      [[m,n+1-x] for m,x in prefix],[[m,n+1-x] for m,x in word])
    old=json.loads((OLD/'first_intervention_certificate.json').read_text(encoding='utf-8'))
    barrier_controls=[]
    for prior in old['witnesses']:
        bs=blocks(prior['full_replay']);E=sum(max(b0['delta'],0) for b0 in bs);CD=sum(2*b0['a'] for b0 in bs if not b0['has_KEEP'])
        coarse=[scan(prior['full_replay'],bs,c,False) for c in range(len(bs))]
        assert [compact(t) for t in coarse]==prior['old_UD_trials']
        if E<=CD:assert any(t['accepted'] for t in coarse)
        barrier_controls.append(dict(name=prior['name'],E=E,C_D=CD,delete_dominated=E<=CD,
          old_UD_accepted_cuts=[t['cut'] for t in coarse if t['accepted']],source_word_changed=False))
    found=normal['strict_closed_walk_found'];assert found==reflected['strict_closed_walk_found']
    cert=dict(schema='one-fixed-generator-strict-cycle-audit-v1',date='2026-10-31',witnesses=[normal,reflected],
      delete_budget_controls=barrier_controls,strict_new_closed_walk_coverage=found,finite_fits=0,size_sweeps=0,
      adaptive_word_searches=0,fixed_generator_attempts=1,allocation_optimizer_used=False,
      matching_terminal_line='FROZEN',universal_CD='OPEN',strictness_success_criterion_unchanged=True)
    save('fixed_generator_certificate.json',cert)
    print(json.dumps(dict(preserved_files=len(pins),stage_files=len(stage),strict_new_closed_walk_coverage=found,
      orbits=[dict(name=w['name'],stop=w['stop_reason'],requests=w['requests_executed'],sync=w['sync_occurrence'],
        extracted_cycle_length=w['extracted_cycle'] and len(w['extracted_cycle']['full_replay'])) for w in cert['witnesses']],
      barrier_controls=barrier_controls),indent=2))

if __name__=='__main__':main()
'''
with (HERE/'audit_fixed_generator.py').open('x',encoding='utf-8') as f:f.write(source)
