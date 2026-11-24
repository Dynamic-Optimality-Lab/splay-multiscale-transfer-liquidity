"""Exact diagnostic implementation of cyclic last-gain accounting.

Uses original IDs. An arbitrary diagnostic pool is never named the frozen D.
"""
from stage5 import *
from collections import defaultdict, Counter
Tree=inherited.Tree

def lifted(items,lo,hi,T):
    out=[]
    for t,obj in items:
        u=t+((lo-t)//T+1)*T
        if u<=hi:out.append((u,obj))
    return sorted(out,key=lambda z:z[0])

def audit(r,parents,mode='gain',prefix_payment=False,protected_paid_ops=()):
    assert mode in ('gain','promotion')
    groups=defaultdict(list)
    for p in sorted(set(map(tuple,parents))):groups[r.doubles[p]['g']].append(p)
    if not groups:return {'rows':[],'counts':{},'parent_count':0,'bounded_count':0}
    T=r.T; changes=defaultdict(list);dem=defaultdict(list)
    b=Tree(r.source['initial_B']);bl=b.labels(r.bits)
    for e in r.events:
        u=e['pivot'];v=e['promoted'];t=e['time']
        if e['actor']=='A':
            if u in groups:dem[u].append((t,e))
        else:
            b.rotate(u,e['side']);new=b.labels(r.bits)
            for g in {u,v}.intersection(groups):
                if bl[g]!=new[g]:changes[g].append((t,(bl[g],new[g],e)))
            bl=new
    def acquired(lab,lo,hi):
        xs=lifted([(t,t) for t,on in r.a_changes[lab] if on],lo,hi,T)
        return r.events[(xs[-1][0]-1)%T] if xs else None
    gaps=inherited.keep_gaps(r) if prefix_payment else {}
    protected_paid_ops=set(protected_paid_ops)
    rows=[];chosen_A={key:set() for key in ['A_reset','frame_exposed','parent_output_exposed']}
    restorers=set()
    for g,ps in sorted(groups.items()):
        for i,p in enumerate(ps):
            prev=ps[i-1];x=r.ops[p[0]-1][1];bit=r.bits[x]
            lo=r.boundaries[prev[0]-1]['end_time'];hi=r.boundaries[p[0]-1]['post_A_time']
            if hi<lo:lo-=T
            assert 0<=hi-lo<T
            z={'parent':p,'previous_same_column':prev,'grandparent':g,'target':x,
               'after_previous_B_unrolled_time':lo,'through_pre_B_unrolled_time':hi}
            resets=lifted(dem[g],lo,hi,T)
            if resets:
                e=resets[-1][1];role='A_reset';z['A_bit']=e['id']
                assert tuple(e['id']) not in chosen_A[role];chosen_A[role].add(tuple(e['id']))
            else:
                initial=Tree(r.boundaries[prev[0]-1]['post_B']).labels(r.bits)[g]
                hist=lifted(changes[g],lo,hi,T)
                assert (hist[-1][1][1] if hist else initial)&bit
                gains=[(t,e) for t,(u,v,e) in hist if not (u&bit) and (v&bit)]
                candidates=gains if mode=='gain' else [(t,e) for t,(u,v,e) in hist if e['promoted']==g]
                if not candidates:
                    assert initial&bit and all(v&bit for t,(u,v,e) in hist)
                    role='continuous_retention'
                else:
                    rt,e=candidates[-1];rid=tuple(e['id'][1:3]);d=r.doubles[rid]
                    assert e['id'][3]==0 and e['promoted']==g and e['target']!=g
                    assert d['case'] in ('LL','RR') and rid not in restorers;restorers.add(rid)
                    z.update(restorer=rid,selected_B_bit=e['id'],selected_unrolled_time=rt,
                             actual_gain_for_this_target=any(t==rt for t,_ in gains))
                    if prefix_payment and rid[1]<=2*gaps[rid[0]]['A']:
                        role='restorer_prefix'
                    elif rid[0] in protected_paid_ops:
                        role='restorer_old_hybrid_protected'
                    elif d['signs']!=[0,0]:
                        role='nonneutral_restorer'
                    else:
                        F=d['F'];post=r.boundaries[rid[0]-1]['post_A_time']
                        assert F!=sum(r.bits.values())
                        gamma=r.previous(r.b_creates[F],post+1);kap=r.previous(r.b_losses[F],gamma)
                        assert not r.present(F,kap) and not r.present(F,post)
                        head=acquired(F,kap,post)
                        if head:
                            role='frame_exposed'
                        else:
                            second=r.events[d['events'][1]-1];P=second['demoted_label']
                            assert second['pivot']==g and P in second['created']
                            birth=second['time'];assert not r.present(P,birth)
                            loss=min(t+((birth-t)//T+1)*T for t in r.b_losses[P])
                            head=acquired(P,birth,loss)
                            role='parent_output_exposed' if head else 'silent_restoration'
                            if head:assert head['sign']<=0
                        if head:
                            z['A_bit']=head['id'];assert tuple(head['id']) not in chosen_A[role]
                            chosen_A[role].add(tuple(head['id']))
            z['classification']=role;rows.append(z)
    counts=Counter(z['classification'] for z in rows);R_A=sum(e['actor']=='A' for e in r.events)
    P=sum(e['actor']=='A' and e['sign']==1 for e in r.events)
    N=sum(e['actor']=='A' and e['sign']==-1 for e in r.events)
    D=sum(e['actor']=='B' and e['sign']==-1 for e in r.events)
    assert D==P-N
    bounded=sum(counts[k] for k in ['A_reset','frame_exposed','parent_output_exposed','nonneutral_restorer'])
    assert counts['nonneutral_restorer']<=D
    assert counts['parent_output_exposed']<=R_A-P
    assert counts['nonneutral_restorer']+counts['parent_output_exposed']<=R_A
    assert bounded<=3*R_A<=6*r.A
    assert counts['restorer_prefix']<=2*r.A
    return {'rows':rows,'counts':dict(counts),'parent_count':len(rows),'bounded_count':bounded,
        'selector':mode,'restorer_prefix_active':prefix_payment,
        'additional_prefix_paid_count':counts['restorer_prefix'],
        'additional_protected_paid_count':counts['restorer_old_hybrid_protected'],
        'real_A_bits':R_A,'A_positive':P,'A_negative':N,'B_decreases':D,
        'distinct_selected_B_restorers':len(restorers)}
