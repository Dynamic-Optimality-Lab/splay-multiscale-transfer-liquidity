from exp04_core import *
import subprocess


if __name__=='__main__':
    meter=Meter('EXP04_inheritance')
    delivery=json.loads((PREV/'EXP03_DELIVERY_MANIFEST.json').read_text())
    for p,h in delivery['files'].items():assert file_hash(PREV/p)==h,p
    archive=json.loads((PREV/'EXP03_SOURCE_WITNESSES.json').read_text())
    sources=archive['inherited_sources']+archive['new_sources']
    data=json.loads((PREV/'EXP03_CAUSAL_EPISODE_RESULTS.json').read_text())
    oldby={s['source']:s for s in data['inherited_sources']+data['new_sources']}
    # Keep full historical words in a separate archive namespace; no edits.
    write('EXP04_SOURCE_WITNESSES.json',{'inherited_sources':sources,'new_sources':[]})
    write('EXP04_INPUT_MANIFEST.json',{'EXP03_files':delivery['files'],'HEAD':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
        'branch':subprocess.check_output(['git','branch','--show-current'],text=True).strip()})
    rows=[];checks=0
    for i,s in enumerate(sources):
        r=Replay(s);assert digest(r.events)==s['trace_hash']
        events=oldby.get(s['name'],{}).get('remaining_after_restart',[])
        for e in events:
            pair=next(p for p in r.pairs if p['rho']==e['rho'])
            assert pair['class']=='R6' and pair['parent']==e['original_parent']
        if events:
            row=metrics(r,events)
        else:
            row={'source':s['name'],'A':r.A,'Q_B':r.Q,'R_star':0,'events':[],'remaining':[],
                'trace_hash':digest(r.events),'population':len(r.keys),'operations':len(r.ops),'genuine_KEEP_support':sorted(r.M),
                'S':sorted(r.S),'I':sorted(r.I),'A_StepEv':[e['id'] for e in r.events if e['actor']=='A' and e['id'][3]==0],
                'B_doubles':[[t,j,d['g']] for (t,j),d in r.doubles.items()],
                'ratios':{'R_star_over_A':'0' if r.A else None,'Q_over_A':str(Fraction(r.Q,r.A)) if r.A else None},
                'complete_paired_closure':r.closed,'independent_original_operations':r.independent_checks}
        rows.append(row);checks+=r.independent_checks
        print(i+1,s['name'],'R*',len(events),'newpaid',len(events)-len(row['remaining']),flush=True)
        if i%20==19:write('EXP04_INHERITANCE_CHECKPOINT.json',{'completed':i+1,'sources':rows})
        del r
    assert len(sources)==260 and checks==121755 and sum(r['R_star'] for r in rows)==120
    write('EXP04_RESIDUAL_INVENTORY.json',{'inherited_sources':rows,'new_sources':[]})
    write('EXP04_EXPERIMENT_LOG.json',{'cycles':[{'cycle':1,'mechanism':'actual carrier-SET zero boundaries, separately budgeted orientations',
        'status':'finite audit complete; symbolic theorem recorded separately','old_R_star':120,
        'new_paid':sum(r['R_star']-len(r['remaining']) for r in rows),'remaining':sum(len(r['remaining']) for r in rows)}]})
    meter.details.update(sources=260,independent_original_operations=checks);meter.success=True
