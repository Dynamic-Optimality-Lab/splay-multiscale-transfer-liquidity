from campaign3 import *
from inherited_epoch_audit import A_pivots
from independent_path_audit import check


def geometry(s,demands,gmap):
    A,pivots=A_pivots(s);a=Tree(s['initial_A']);wanted=defaultdict(list)
    steps=defaultdict(list)
    for bits in pivots.values():
        for t,bit in bits:
            if bit[3]==0:steps[t].append(bit)
    keeps=[h for h,(tag,x) in enumerate(s['operations'],1) if tag=='K']
    previous={h:keeps[i-1] for i,h in enumerate(keeps)};endpoint_loads=Counter()
    for d in demands:wanted[d['consumer']].append(d)
    records=[];fringe=[];loads_bits=Counter();endpoint_ops=Counter()
    for h,(tag,x) in enumerate(s['operations'],1):
        px=a.path(x)
        for d in wanted[h]:
            parent=tuple(d['original_parent']);g=gmap[parent];pg=a.path(g)
            common=0
            while common<min(len(pg),len(px)) and pg[common]==px[common]:common+=1
            own=g in px[:-1];delta=0 if own else len(pg)-common
            attachment=pg[common-1] if not own else None
            record={'event':d,'old_g':g,'pre_A_target_path':px,'pre_A_g_path':pg,
                'own_path':own,'off_path_depth':delta,'immediate_fringe_root':not own and delta==1}
            if record['immediate_fringe_root']:
                fringe.append(d)
                if attachment!=x:
                    bit=next(bit for t,bit in pivots[attachment] if t==h)
                    loads_bits[bit]+=1;record['actual_A_bit_witness']=bit
                else:
                    endpoint_ops[h]+=1;prev=previous[h];T=len(s['operations'])
                    ts=[(prev+k-1)%T+1 for k in range(1,(h-prev)%T+1 if (h-prev)%T else T+1)]
                    witnesses=[bit for t in ts for bit in sorted(steps[t])]
                    assert witnesses
                    witness=witnesses[0];endpoint_loads[witness]+=1
                    record['actual_A_StepEv_bit0_witness']=witness
                    record['payment_part']='two target-child roots; actual incoming KEEP-gap StepEv'
            records.append(record)
        Replay.plain_splay(a,x)
    assert a.state()==s['initial_A']
    assert max(loads_bits.values(),default=0)<=3 and max(endpoint_ops.values(),default=0)<=6
    assert max(endpoint_loads.values(),default=0)<=6
    assert len(fringe)<=12*A
    return {'source':s['name'],'A':A,'records':records,'fringe_paid_original_gaps':fringe,
        'strict_attachment_A_bit_maximum_gap_load':max(loads_bits.values(),default=0),
        'endpoint_gap_maximum_gap_load':max(endpoint_ops.values(),default=0)}


def subtree(a,g):
    todo=[g];out={}
    while todo:
        k=todo.pop();out[k]=tuple(a.ch[k]);todo.extend(c for c in a.ch[k] if c is not None)
    return out


def packet_check():
    t=json.loads((ROOT/'OBSTRUCTION_FULL_TRACE.json').read_text())
    c=json.loads((ROOT/'EPOCH_OBSTRUCTION_CERTIFICATE.json').read_text())
    p=c['original_packet'];anchor=tuple(p['actual_A_demotion_bit']);g=p['old_g']
    events=t['events'];T=len(events);bt={}
    for e in events:
        if e['actor']=='B':bt.setdefault(tuple(e['id'][1:3]),e['time'])
    at=next(e['time'] for e in events if tuple(e['id'])==anchor)
    parents=[tuple(p['selected_first_parent'])]+[tuple(z) for z in p['remaining_original_parents']]
    times={bt[q] if bt[q]>at else bt[q]+T:q for q in parents};last=max(times)
    a=Tree(t['source']['initial_A']);fixed=None;observations=[]
    for lap in range(2):
        for ev in events:
            tm=lap*T+ev['time']
            if ev['actor']=='A':a.rotate(ev['pivot'],ev['side'])
            if tm==at:fixed=subtree(a,g)
            if fixed is not None and at<=tm<=last:assert subtree(a,g)==fixed
            if tm in times:
                parent=times[tm];x=t['source']['operations'][parent[0]-1][1]
                assert x<min(fixed) or x>max(fixed)
                observations.append({'parent':parent,'target':x,'fixed_A_subtree_keys':sorted(fixed),
                    'target_outside_fixed_A_subtree_interval':True})
        assert a.state()==t['source']['initial_A']
    return {'source':t['source']['name'],'actual_A_demotion_anchor':anchor,
        'complete_A_subtree_rigid_at_every_primitive_through_last_parent':True,
        'observations':observations,'repeat_parent':[179,2],
        'qualification':'R6-level packet obstruction, not an R_upper escape.'}


if __name__=='__main__':
    meter=Meter('scoped_class_verification')
    sources=json.loads((ROOT/'SCALING_SOURCES.json').read_text());results=json.loads((ROOT/'SCALING_RESULTS.json').read_text())
    out=[];geoms=[]
    for s,z in zip(sources,results):
        out.append(check(s));write('NEW_SOURCE_PHYSICS.json',out)
        if not z['original_Pi_classification']:continue
        gmap={}
        for p in z['first_use_payment']['packets']:
            for parent in [p['selected_first_parent']]+p['remaining_original_parents']:gmap[tuple(parent)]=p['old_g']
        assert len(gmap)==len({tuple(d['original_parent']) for d in z['original_R_star']})
        geoms.append(geometry(s,z['original_R_star'],gmap))
    t=json.loads((ROOT/'LARGE_UPPER_TRACE.json').read_text())
    for d in results[2]['original_R_star']:
        h,j=d['original_parent'];g=next(p['old_g'] for p in results[2]['first_use_payment']['packets']
            if list(d['original_parent'])==p['selected_first_parent'] or list(d['original_parent']) in p['remaining_original_parents'])
        path=t['boundaries'][h-1]['B_path'];assert path[-1-2*j]==g
    packet=packet_check();write('RIGID_PACKET_VERIFICATION.json',packet)
    write('FRINGE_GEOMETRY_VERIFICATION.json',geoms)
    print('PASS 4 new complete physical sources; original parent distances; exact rigid repeated-use packet; fringe budget checks',flush=True)
    meter.success=True
