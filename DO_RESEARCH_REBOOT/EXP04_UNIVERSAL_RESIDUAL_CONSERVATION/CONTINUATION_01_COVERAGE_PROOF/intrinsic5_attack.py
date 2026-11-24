from core import *
from all_intervals import all_intervals_through,materialize
from return_normalization import guarded_skeleton
from gap_payment import keep_gaps,hard_guarded


if __name__=='__main__':
    meter=Meter('CONT01_intrinsic5_hard_consumer');out=[];sources=[]
    # Lossless sharing of repeated COMPLETE immutable snapshots. Tree() copies
    # every child list before mutations; no caller mutates a state() snapshot.
    pool={}
    def shared_complete_state(tree):
        key=(tree.root,tuple((k,*tree.ch[k]) for k in tree.keys))
        if key not in pool:pool[key]={'root':tree.root,'children':{str(k):list(tree.ch[k]) for k in tree.keys}}
        return pool[key]
    Tree.state=shared_complete_state
    s=both_oscillations(7,2048,2048,'bitreverse',right_low=2)
    r=Replay(s);ev,_,_=original_residual(r);r.original_R_star=ev
    gaps=keep_gaps(r);norm=guarded_skeleton(r,list(range(1,len(r.ops)+1)))
    hnorm=hard_guarded(r,list(range(1,len(r.ops)+1)),gaps)
    row={'source':s['name'],'A':r.A,'Q_B':r.Q,'R_star':ev,
         'normalized':norm,'hard_normalized':hnorm,'independent_operations':r.independent_checks,
         'residual_KEEP_paths':[{'consumer':e['consumer'],
             'A_path':r.boundaries[e['consumer']-1]['A_path'],
             'B_path':r.boundaries[e['consumer']-1]['B_path'],
             'KEEP_gap':gaps[e['consumer']]} for e in ev]}
    s.update(A=r.A,Q_B=r.Q,trace_hash=digest(r.events),closing_A=r.a.state(),closing_B=r.b.state())
    sources.append(s);write('INTRINSIC5_SOURCES.json',sources)
    print(s['name'],'A',r.A,'Q',r.Q,'R*',len(ev),'D_G',norm['D'],'D_H',hnorm['D'],flush=True)
    # Interval eligibility is an operation predicate, not a gap predicate.
    # Several original gaps can share one consumer; audit it only once.
    representatives={e['consumer']:e for e in ev}
    # One targeted consumer audit. Other consumers are all retained by the
    # independently checked full-period guarded payment; do not repeat an
    # unrelated all-cuts search before making the source checkpoint durable.
    for e in list(representatives.values())[:1]:
        h=e['consumer'];z=all_intervals_through(r,h,stop_at=5)
        z.update(consumer=h,rho=e['rho'])
        if z['feasible'][5]:z['feasible'][5]=materialize(r,z['feasible'][5])
        row.setdefault('interval_audits',[]).append(z)
        print('consumer',h,'q',gaps[h]['Q_at_KEEP'],'gapA',gaps[h]['A'],
              'raw5 funded',bool(z['feasible'][5]),'exhaustive',z['exhaustive'],
              'min ratio',str(Fraction(z['best']['D'],z['best']['A'])),flush=True)
    row['trace_file']=f'TRACE_COMPACT_{digest(s["name"])[:12]}.json'
    states={};refs={};boundaries=[]
    for b in r.boundaries:
        bb={k:v for k,v in b.items() if k not in ('pre_A','pre_B','post_A','post_B')}
        for k in ('pre_A','pre_B','post_A','post_B'):
            st=b[k]
            if id(st) not in refs:
                sha=digest(st);refs[id(st)]=sha;states[sha]=st
            bb[k+'_state_sha256']=refs[id(st)]
        boundaries.append(bb)
    write(row['trace_file'],{'format':'lossless full-state-pool plus boundary references',
        'source':s,'events':r.events,'states':states,'boundaries':boundaries,'R_star':ev})
    row['shared_complete_states']=len(pool)
    write('INTRINSIC5_RESULTS.json',row);meter.success=True;meter.details['sources']=1
