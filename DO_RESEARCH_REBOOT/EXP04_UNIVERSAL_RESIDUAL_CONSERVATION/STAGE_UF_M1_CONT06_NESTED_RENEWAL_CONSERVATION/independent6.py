from base6 import *
from physical1 import Edges
from cohortc import decode_state
from residual0 import gap_costs

def full_physical(s,p):
    n=len(s['initial_B']['children']);assert digest(s)==p['source_sha256']
    assert p['original_S']==p['original_genuine_M']==list(range(1,n+1))
    aa,bb=Edges(s['initial_A']),Edges(s['initial_B']);initial=aa.code(),bb.code();A=Q=bits=0
    pool=p['state_pool']['states'];ds={tuple(z['parent']):z for z in p['doubles']};byh=defaultdict(list)
    for v,d in ds.items():byh[v[0]].append((v,d))
    for h,(row,(tag,x)) in enumerate(zip(p['boundaries'],s['operations']),1):
        assert (row['t'],row['tag'],row['x'])==(h,tag,x)
        assert (aa.code(),bb.code())==(int(pool[row['pre_A_state']],16),int(pool[row['pre_B_state']],16))
        path=aa.path(x);assert path==row['A_path'] and row['a']==len(path)//2
        assert row['post_A_time']-row['start_time']==len(path)-1
        if tag=='K':
            bp=bb.path(x);assert bp==row['B_path'] and (len(bp)-1)//2==row['q']
            for v,d in byh[h]:assert bb.m[d['g']]==d['F']
        for i in range(row['start_time'],row['end_time']):
            e=p['events'][i];actor='A' if i<row['post_A_time'] else 'B';tree,other=(aa,bb) if actor=='A' else (bb,aa)
            assert e['time']==i+1 and e['actor']==e['id'][0]==actor and e['id'][1]==h and e['target']==x
            before=set(tree.m[1:]);otherlabs=set(other.m[1:]);tree.step(e);after=set(tree.m[1:]);lost=before-after;made=after-before
            assert sorted(lost)==e['lost'] and sorted(made)==e['created']
            sign=(sum(z in otherlabs for z in lost)-sum(z in otherlabs for z in made)) if actor=='A' else (sum(z not in otherlabs for z in made)-sum(z not in otherlabs for z in lost))
            assert sign==e['sign'] and tree.m[e['pivot']]==e['demoted_label'];bits+=1
        assert (aa.code(),bb.code())==(int(pool[row['post_A_state']],16),int(pool[row['post_B_state']],16))
        assert aa.root==x and (bb.root==x if tag=='K' else row['q']==0)
        A+=row['a'];Q+=row['q']
    assert len(p['boundaries'])==len(s['operations']) and bits==len(p['events'])
    aa.recompute();bb.recompute();assert (aa.code(),bb.code())==initial
    return {'A':A,'Q_B':Q,'primitives':bits,'all_original_edges_signed_SET_and_full_boundaries':True}

def domain_price(p,targets,initial_sid,A):
    tree=Edges(decode_state(p,initial_sid));J=set()
    for x in targets:J.update(tree.path(x))
    xs=[]
    for x in targets:
        if not xs or xs[-1]!=x:xs.append(x)
    rank={x:i for i,x in enumerate(sorted(J))};L=sum(abs(rank[y]-rank[x]).bit_length() for x,y in zip(xs,xs[1:]))
    return {'J':sorted(J),'targets':xs,'L':L,'A':A,'D':len(J)+len(xs)+L}

def local_prices(s,p,geo):
    rows=p['boundaries'];ds=p['doubles'];gs=gap_costs(s,rows);extreme=1|(1<<(len(s['initial_B']['children'])-1));out=[]
    for z in geo:
        loc=z['local_natural_interval']
        if loc is None:continue
        ts=loc['operations'];A=sum(rows[t-1]['a'] for t in ts);start=rows[ts[0]-1]['pre_B_state']
        raw=domain_price(p,[rows[t-1]['x'] for t in ts if rows[t-1]['tag']=='K'],start,A);assert raw==loc['raw']
        checks={}
        for variant in ('G','H'):
            guards={d['parent'][0] for d in ds if d['signs']==[0,0] and not(d['F']&extreme) and (variant=='G' or rows[d['parent'][0]-1]['q']>2*gs[d['parent'][0]])}
            stack=[];positions={start:0}
            for t in ts:
                row=rows[t-1]
                if row['tag']!='K':continue
                sid=row['post_B_state']
                if t in guards:stack.append(t);positions={sid:len(stack)}
                elif sid in positions:
                    stop=positions[sid];assert not set(stack[stop:]+[t])&guards
                    stack=stack[:stop];positions={sid0:j for sid0,j in positions.items() if j<=stop}
                else:stack.append(t);positions[sid]=len(stack)
            price=domain_price(p,[rows[t-1]['x'] for t in stack],start,A)
            assert stack==loc[variant]['retained_KEEP']
            assert sorted(set(ts)&guards)==loc[variant]['protected_operations_in_span']
            assert all(price[k]==loc[variant][k] for k in price)
            checks[variant]={'retained':stack,'protected':sorted(set(ts)&guards),'D':price['D']}
        Aids=[e['id'] for t in ts for e in p['events'][rows[t-1]['start_time']:rows[t-1]['post_A_time']] if e['id'][3]==0]
        assert len(Aids)==A
        out.append({'earlier':z['earlier_parent'],'later':z['later_parent'],'raw':raw,'G_H':checks,'actual_A_StepEv':Aids,
            'threshold_5A':5*A,'independently_checked_natural_price_refutation':min(raw['D'],checks['G']['D'],checks['H']['D'])>5*A})
    return out

def original_predecessors(p,acc,rn):
    ds={tuple(d['parent']):d for d in p['doubles']};groups=defaultdict(list)
    for e in acc['C_old']:groups[tuple(e['original_parent'])].append(e)
    cols=defaultdict(list)
    for v in sorted(groups):cols[ds[v]['g']].append(v)
    T=len(p['events']);reset=defaultdict(list)
    for e in p['events']:
        if e['actor']=='A':reset[e['pivot']].append(e['time'])
    E={digest(e['rho']) for e in acc['E_old']};expected={tuple(z['later_parent']):tuple(z['earlier_parent']) for z in rn['canonical_renewals']};derived={}
    for g,vs in cols.items():
        for i,v in enumerate(vs):
            u=vs[i-1];hi=p['boundaries'][v[0]-1]['post_A_time'];lo=p['boundaries'][u[0]-1]['end_time'];distance=(hi-lo)%T
            assert distance>0
            first=bool(reset[g]) and min((hi-t)%T for t in reset[g])<distance
            assert all(digest(e['rho']) in E for e in groups[v])==first
            if not first:derived[v]=u
    assert derived==expected
    return {'original_C_old_parents':len(groups),'canonical_edges':len(derived),'independent_offline_cyclic_distance_check':True}
