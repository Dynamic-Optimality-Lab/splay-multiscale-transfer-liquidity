"""A second comparison system, restarted only at actual A/B equality cuts."""
from exp03_episodes import *


def restart_windows(r,episodes):
    windows=[];used_ops=set();slots=set();direction=orientation(r)
    for ep in episodes:
        bs=[]
        for t in ep['operations']:
            row=r.boundaries[t-1]
            if row['tag']!='K':continue
            if not bs or bs[-1]['x']!=row['x']:bs.append({'x':row['x'],'ts':[]})
            bs[-1]['ts'].append(t)
        i=0
        while i<len(bs):
            w=inherited_distortion.shadow_candidate(r,bs,i,direction,len(bs)-i)
            if w is None:i+=1;continue
            assert not used_ops.intersection(w['operations']);used_ops.update(w['operations'])
            rb=[]
            for t in w['retained']:
                x=r.ops[t-1][1]
                if not rb or rb[-1]['x']!=x:rb.append({'x':x,'ts':[]})
                rb[-1]['ts'].append(t)
            witnesses=[]
            for a,b in zip(rb,rb[1:]):
                event=A_gap(r,a['ts'][-1],b['ts'][0]);slot=tuple(event[1:3])
                assert slot not in slots;slots.add(slot)
                assert event in ep['A_StepEv']
                witnesses.append(event)
            w.update(episode=ep['id'],original_A_transition_witnesses=witnesses)
            windows.append(w);i+=w['block_span']
    assert sum(w['domain_size'] for w in windows)<=2*len(slots)<=2*r.A
    return windows


def restart_analysis(r,unhandled,episodes):
    windows=restart_windows(r,episodes);matched=[];destinations={};diagnostics=[]
    by_t=defaultdict(list)
    for e in unhandled:by_t[e['consumer']].append(e)
    for wi,w in enumerate(windows):
        shadow=Tree(w['initial_B']);shadow_q=0;accesses=[];independent_shadow=r.as_tuple(shadow)
        for t in w['retained']:
            before=shadow.state();x=r.ops[t-1][1]
            assert set(shadow.path(x))<=set(w['J'])
            Replay.plain_splay(shadow,x)
            independent_shadow,ind_events=r.ind.trace(independent_shadow,x)
            assert independent_shadow==r.as_tuple(shadow)
            frames=list(frame_records(before,x,shadow.state()).values());shadow_q+=len(frames)
            assert sum(e[0]!='ZIG' for e in ind_events)==len(frames)
            if t in by_t:
                accesses.append({'operation':t,'actual_path':r.boundaries[t-1]['B_path'],
                    'shadow_path':Tree(before).path(x),'shadow_frames':frames})
            for e in by_t[t]:
                parent=tuple(e['original_parent']);g=r.U[parent]['g']
                ms=[f for f in frames if f['g']==g];assert len(ms)<=1
                if not ms:continue
                dst=(wi,t,ms[0]['j'])
                assert dst not in destinations or destinations[dst]==parent
                destinations[dst]=parent
                matched.append({'rho':e['rho'],'type':e['type'],'original_parent':list(parent),
                    'old_grandparent':g,'shadow_double':list(dst)})
        diagnostics.append({**w,'shadow_Q':shadow_q,'demand_accesses':accesses,'independently_checked_shadow_accesses':len(w['retained'])})
    return {'fixed_original_orientation':orientation(r),'windows':diagnostics,
        'sum_J':sum(w['domain_size'] for w in windows),'original_A_transition_count':sum(len(w['original_A_transition_witnesses']) for w in windows),
        'paid_original_gaps':matched,'paid_gap_count':len(matched),
        'paid_parent_count':len({tuple(m['original_parent']) for m in matched}),
        'bound':'R_restart <= 3 sum Q_shadow <= 3 C_seq sum |J| <= 6 C_seq A'}


if __name__=='__main__':
    meter=Meter('restart_pilot_v002')
    archive=json.loads((ROOT/'EXP03_SOURCE_WITNESSES.json').read_text())
    names={s['source'] for s in json.loads((ROOT/'EXP03_UNHANDLED_PARENT_INVENTORY.json').read_text())['sources_with_unhandled_parents']}
    result=[]
    for s in archive['inherited_sources']:
        if s['name'] not in names:continue
        r=Replay(s);c=current_classification(r);eps=actual_mismatch_episodes(r)
        restart=restart_analysis(r,c['unhandled'],eps)
        z={'source':s['name'],'actual_mismatch_episodes':eps,'restart':restart}
        result.append(z)
        print(s['name'],'episodes',len(eps),'paid',restart['paid_gap_count'],'of',len(c['unhandled']),flush=True)
    write('EXP03_RESTART_PILOT.json',result);meter.success=True;meter.details['sources']=len(result)
