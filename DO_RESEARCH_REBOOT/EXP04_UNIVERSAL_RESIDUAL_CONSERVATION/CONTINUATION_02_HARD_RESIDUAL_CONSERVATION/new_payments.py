from campaign import *


def actual_payments(r,events):
    gaps=keep_gaps(r);out=[];ancestor_load=Counter()
    for e in events:
        h,j=e['original_parent'];d=r.U[(h,j)];x=r.ops[h-1][1];g=d['g'];a=gaps[h]['A']
        prefix=j<=2*a;ancestor=g in r.boundaries[h-1]['A_path'][:-1];witness=None
        if ancestor:
            # Independent physical relation test: the original rotation whose
            # deleted ancestor relation is g->x, within CURRENT operation h.
            astate=Tree(r.boundaries[h-1]['pre_A'])
            for z in r.events[r.boundaries[h-1]['start_time']:r.boundaries[h-1]['post_A_time']]:
                was=g in astate.path(x)[:-1];astate.rotate(z['pivot'],z['side']);now=g in astate.path(x)[:-1]
                if was and not now:
                    assert z['pivot']==g;witness=z['id'];break
            assert witness is not None
            ancestor_load[tuple(witness)]+=1
        out.append({**e,'old_g':g,'A_gap':a,'prefix_paid':prefix,'current_ancestor_paid':ancestor,
                    'current_ancestry_loss_bit':witness,'upper_B_only':not prefix and not ancestor})
    assert max(ancestor_load.values(),default=0)<=3
    # Direct quota is global independently of which residual is inspected.
    assert sum(min(r.boundaries[h-1]['q'],2*z['A']) for h,z in gaps.items())<=2*r.A
    return {'original_events':out,'prefix_parent_budget':2*r.A,'current_A_bit_maximum_gap_load':max(ancestor_load.values(),default=0),
            'upper_B_only_original_events':[e for e in out if e['upper_B_only']],
            'original_R_next_P_membership':'not inferred from original R_* membership'}


def compact_trace(r,events,file):
    states={};refs={};rows=[]
    for row in r.boundaries:
        z={k:v for k,v in row.items() if k not in ('pre_A','post_A','pre_B','post_B')}
        for key in ('pre_A','post_A','pre_B','post_B'):
            st=row[key]
            if id(st) not in refs:sha=digest(st);refs[id(st)]=sha;states[sha]=st
            z[key+'_state_sha256']=refs[id(st)]
        rows.append(z)
    write(file,{'format':'lossless full original state pool and exact primitive events',
        'source':r.source,'events':r.events,'boundaries':rows,'states':states,'original_R_star':events})


def intern_original_states():
    pool={}
    def state(tree):
        key=(tree.root,tuple((k,*tree.ch[k]) for k in tree.keys))
        if key not in pool:pool[key]={'root':tree.root,'children':{str(k):list(tree.ch[k]) for k in tree.keys}}
        return pool[key]
    Tree.state=state
    return pool


if __name__=='__main__':
    meter=Meter('current_A_payment_and_upper_probe');out=[];sources=[]
    control=next(s for s in json.loads((ROOT/'HELPER_SOURCES.json').read_text()) if 'helper5_' in s['name'])
    r=Replay(control);ev,_,_=original_residual(r);z=actual_payments(r,ev)
    out.append({'source':control['name'],'A':r.A,'Q_B':r.Q,**z})
    write('CURRENT_A_PAYMENT_RESULTS.json',out);del r
    sys.setrecursionlimit(20000);pool=intern_original_states()
    # The p9 full-oracle run exceeded the memory aim and was superseded by
    # the193-key private-ancestor witness. It is opt-in for reproduction,
    # never an automatic continuation after a negative p8 diagnostic.
    cases=(8,9) if '--include-expensive-p9' in sys.argv else (8,)
    for p in cases:
        s=both_oscillations(p,64,64,'bitreverse',right_low=2);s['name']='C02_upper_'+s['name']
        r=Replay(s);ev,_,_=original_residual(r);z=actual_payments(r,ev)
        s.update(A=r.A,Q_B=r.Q,trace_hash=digest(r.events),closing_A=r.a.state(),closing_B=r.b.state())
        sources.append(s);row={'source':s['name'],'A':r.A,'Q_B':r.Q,'population':len(r.keys),
            'independent_original_operations':r.independent_checks,**z}
        raw=periodic_cost([x for tag,x in r.ops if tag=='K'],r.S)
        row['old_raw_periodic_certificate']={**raw,'eligible':raw['B_cyclic']<=10*r.A}
        if z['upper_B_only_original_events']:
            row['trace_file']=f'UPPER_TRACE_p{p}.json';compact_trace(r,ev,row['trace_file'])
            row['upper_parent_certificates']=[{'event':e,'original_U':r.U[tuple(e['original_parent'])],
                'A_path':r.boundaries[e['consumer']-1]['A_path'],'B_path':r.boundaries[e['consumer']-1]['B_path']}
                 for e in z['upper_B_only_original_events']]
        out.append(row);write('UPPER_SOURCES.json',sources);write('CURRENT_A_PAYMENT_RESULTS.json',out)
        print(s['name'],'R*',len(ev),'upper B-only',len(z['upper_B_only_original_events']),
              'raw periodic covered',row['old_raw_periodic_certificate']['eligible'],flush=True)
        if z['upper_B_only_original_events']:break
        del r;pool.clear()
    meter.success=True;meter.details['new_original_sources']=len(sources)
