from campaign import *


if __name__=='__main__':
    meter=Meter('inherited_original_local_payment_audit')
    inv=json.loads((PARENT/'EXP04_RESIDUAL_INVENTORY.json').read_text())
    archive=json.loads((PARENT/'EXP04_SOURCE_WITNESSES.json').read_text())
    sources={s['name']:s for s in archive['inherited_sources']+archive['new_sources']};out=[]
    for row in inv['inherited_sources']+inv['new_sources']:
        if not row['events']:continue
        s=sources[row['source']];a=Tree(s['initial_A']);wanted={e['consumer'] for e in row['events']}
        paths={};prefix=[0]
        for t,(tag,x) in enumerate(s['operations'],1):
            path=a.path(x)
            if t in wanted:paths[t]=path
            prefix.append(prefix[-1]+len(path)//2);Replay.plain_splay(a,x)
        assert prefix[-1]==row['A'] and a.state()==s['initial_A']
        ks=[i+1 for i,(tag,x) in enumerate(s['operations']) if tag=='K'];before={h:ks[i-1] for i,h in enumerate(ks)}
        gmap={(t,j):g for t,j,g in row['B_doubles']};records=[]
        for e in row['events']:
            h,j=e['original_parent'];prev=before[h]
            agap=prefix[h]-prefix[prev] if prev<h else prefix[-1]-prefix[prev]+prefix[h]
            g=gmap[h,j];assert agap>=1
            records.append({**e,'old_g':g,'A_gap':agap,'current_pre_A_path':paths[h],
                            'prefix_paid':j<=2*agap,'current_ancestor_paid':g in paths[h][:-1],
                            'upper_B_only':j>2*agap and g not in paths[h][:-1]})
        out.append({'source':row['source'],'A':row['A'],'original_events':records,
                    'qualification':'Pinned original R_* membership; fresh original A-only cost/root/path replay, not a new Pi classification.'})
    write('INHERITED_LOCAL_PAYMENT_AUDIT.json',{'sources':out,
        'upper_B_only_original_events':[{'source':r['source'],**e} for r in out for e in r['original_events'] if e['upper_B_only']],
        'finite_audit_is_not_a_universal_theorem':True})
    print('audited',sum(len(r['original_events']) for r in out),'pinned original gaps; upper B-only',
          sum(e['upper_B_only'] for r in out for e in r['original_events']),flush=True)
    meter.success=True
