from campaign3 import *
from bisect import bisect_right


def epoch_payment(events,demands,parent_g):
    """Actual primitive A-demotions; one earliest original parent per epoch.

    events are the original full physical event stream. All demands retain
    original occurrence IDs. Different gaps with the same parent are one
    parent when selecting first use, with up to3 original slots afterward.
    """
    pivots=defaultdict(list);parents=defaultdict(list)
    for e in events:
        if e['actor']=='A':pivots[e['pivot']].append((e['time'],tuple(e['id'])))
    btime={}
    for e in events:
        if e['actor']=='B':btime.setdefault(tuple(e['id'][1:3]),e['time'])
    for d in demands:parents[tuple(d['original_parent'])].append(d)
    groups=defaultdict(list);no_pivot=[]
    for parent,ds in parents.items():
        assert len(ds)<=3
        g=parent_g[parent];ts=pivots[g];t=btime[parent]
        if not ts:no_pivot.append({'parent':parent,'old_g':g,'demands':ds});continue
        i=bisect_right([a for a,b in ts],t)-1
        # Negative index chooses the previous cyclic lap's last demotion.
        groups[ts[i][1]].append({'parent':parent,'old_g':g,'time':t,
            'lifted_time':t if t>ts[i][0] else t+len(events),'demands':ds})
    selected=[];repeat=[];packets=[]
    for bit,ps in sorted(groups.items()):
        ps.sort(key=lambda p:p['lifted_time']);first=ps[0]
        selected+=first['demands']
        for p in ps[1:]:repeat+=p['demands']
        packets.append({'actual_A_demotion_bit':bit,'old_g':first['old_g'],
            'selected_first_parent':first['parent'],'first_original_gaps':[d['rho'] for d in first['demands']],
            'remaining_original_parents':[p['parent'] for p in ps[1:]],
            'remaining_original_gaps':[d['rho'] for p in ps[1:] for d in p['demands']],
            'original_parent_count':len(ps),'original_gap_count':sum(len(p['demands']) for p in ps)})
    chosen={digest(d['rho']) for d in selected}
    assert len(chosen)==len(selected) and len(selected)<=3*len(pivots_as_bits(events))
    assert len(selected)+len(repeat)+sum(len(p['demands']) for p in no_pivot)==len(demands)
    return {'selected_original_gaps':selected,'repeat_original_gaps':repeat,
        'A_demotion_free_key_original_gaps':[d for p in no_pivot for d in p['demands']],
        'packets':packets,'maximum_selected_original_gap_load_per_A_bit':max((len(p['first_original_gaps']) for p in packets),default=0),
        'maximum_unrestricted_parent_uses_per_A_epoch':max((p['original_parent_count'] for p in packets),default=0),
        'partition_verified':True}


def pivots_as_bits(events):return [e for e in events if e['actor']=='A']


def from_replay(r,demands):
    z=epoch_payment(r.events,demands,{tuple(d['original_parent']):r.U[tuple(d['original_parent'])]['g'] for d in demands})
    paid={digest(d['rho']) for d in z['selected_original_gaps']}
    own=[d for d in demands if r.U[tuple(d['original_parent'])]['g'] in r.boundaries[d['consumer']-1]['A_path'][:-1]]
    assert all(digest(d['rho']) in paid for d in own)
    z['current_pre_A_path_class_contained']=True
    z['strictly_new_relative_to_own_path']=[d for d in z['selected_original_gaps'] if d not in own]
    z['A']=r.A;assert len(z['selected_original_gaps'])<=6*r.A
    return z
