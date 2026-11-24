"""Independent original SET/Pi and whole-frame birth reconstruction.

Uses M1's edge-list physical updater, not the primary oracle's SET/Pi
implementation. No historical module writer is invoked.
"""
from basec import *
from physical1 import Edges
from bisect import bisect_left,bisect_right

def previous(times,before,T):
    assert times and T
    q,r=divmod(before-1,T);i=bisect_right(times,r)-1
    return times[i]+q*T if i>=0 else times[-1]+(q-1)*T

class Presence:
    def __init__(self,initial,changes,T):
        self.initial=initial;self.changes=changes;self.T=T
        self.times={lab:[t for t,on in cs] for lab,cs in changes.items()}
        self.creates={lab:[t for t,on in cs if on] for lab,cs in changes.items()}
    def at(self,lab,t):
        ts=self.times.get(lab,[]);i=bisect_right(ts,t%self.T)-1
        return self.changes[lab][i][1] if i>=0 else lab in self.initial
    def first_creation(self,lab,lo):
        ts=self.creates.get(lab,[])
        if not ts:return None
        q,r=divmod(lo,self.T);i=bisect_right(ts,r)
        return ts[i]+q*self.T if i<len(ts) else ts[0]+(q+1)*self.T
    def any(self,lab,lo,hi):
        assert 0<=hi-lo<=self.T
        if self.at(lab,lo):return True
        t=self.first_creation(lab,lo);return t is not None and t<=hi

def reconstruct(s,phys,forest,m1audit,known_star=None,weights=None):
    a,b=Edges(s['initial_A']),Edges(s['initial_B']);a0,b0=a.code(),b.code()
    S=phys['original_S'];core=sum(1<<(k-1) for k in S);exts=[S[0],S[-1]] if S else []
    extremes=sum(1<<(k-1) for k in set(exts));T=len(phys['events']);evs=phys['events'];N=len(s['operations'])
    ac=Counter(z&core for z in a.m[1:] if z&core);bc=Counter(z&core for z in b.m[1:] if z&core)
    initialA=set(ac);achanges=defaultdict(list);bcreates=defaultdict(list);blosses=defaultdict(list)
    totals=Counter();ext={q:Counter() for q in set(exts)};extrows=[];extdelta={}
    ds={tuple(z['parent']):z for z in phys['doubles']};V={tuple(z['parent']):z for z in forest['vertices']}
    depth={tuple(z['vertex']):z['distance'] for z in m1audit['C_fringe_depths']}
    RA=sum(e['actor']=='A' for e in evs)
    KB=sum(row['tag']=='K' and len(row['B_path'])>1 for row in phys['boundaries'])
    for row in phys['boundaries']:
        assert a.code()==int(phys['state_pool']['states'][row['pre_A_state']],16)
        assert b.code()==int(phys['state_pool']['states'][row['pre_B_state']],16)
        for k in range(row['start_time'],row['end_time']):
            e=evs[k];actor=e['actor'];tree,other,ct,ot=(a,b,ac,bc) if actor=='A' else (b,a,bc,ac)
            u,v=e['pivot'],e['promoted'];ou,ov=tree.m[u],tree.m[v]
            old=[ou&core,ov&core];tree.step(e);nu,nv=tree.m[u],tree.m[v]
            new=[nu&core,nv&core];labs=set(old+new)-{0};pre={z for z in labs if ct[z]}
            for z in old:
                if z:ct[z]-=1
            for z in new:
                if z:ct[z]+=1
            assert all(ct[z]>=0 for z in labs)
            post={z for z in labs if ct[z]};lost=pre-post;created=post-pre
            assert len(lost)<=1 and len(created)<=1
            assert sorted(lost)==e['lost'] and sorted(created)==e['created']
            sign=(sum(ot[z]>0 for z in lost)-sum(ot[z]>0 for z in created)) if actor=='A' else (
                sum(ot[z]==0 for z in created)-sum(ot[z]==0 for z in lost))
            assert sign==e['sign']
            if actor=='A':
                totals['PA']+=sign==1;totals['NA']+=sign==-1
                for z in lost:achanges[z].append((k+1,False))
                for z in created:achanges[z].append((k+1,True))
            else:
                assert len(lost)==len(created)==1 and sign<=0
                assert next(iter(created))==(nu&core)
                totals['DB']+=sign==-1
                for z in lost:blosses[z].append(k+1)
                for z in created:bcreates[z].append(k+1)
            lost_nodes=ou&~nu;gain_nodes=nv&~ov
            for q,counts in ext.items():
                bit=1<<(q-1)
                if actor=='A':
                    plus=bool(lost_nodes&bit and b.m[u]&bit);minus=bool(gain_nodes&bit and b.m[v]&bit)
                    counts['A_flux']+=int(plus)-int(minus)
                else:
                    plus=bool(gain_nodes&bit and not a.m[v]&bit);minus=bool(lost_nodes&bit and not a.m[u]&bit)
                    counts['B_plus']+=plus;counts['B_minus']+=minus
                    if plus:assert v!=e['target'] and e['case'] in ('LL','RR') and e['id'][3]==0
                    if v==e['target']:assert not plus
                    extrows.append({'extreme':q,'bit':e['id'],'plus':int(plus),'minus':int(minus)})
                    extdelta[q,tuple(e['id'])]=(int(plus),int(minus))
        a.recompute();b.recompute()
        assert a.code()==int(phys['state_pool']['states'][row['post_A_state']],16)
        assert b.code()==int(phys['state_pool']['states'][row['post_B_state']],16)
    assert (a.code(),b.code())==(a0,b0) and set(z for z,n in ac.items() if n)==initialA
    assert totals['DB']==totals['PA']-totals['NA']<=RA
    assert KB<=sum(r['a'] for r in phys['boundaries'])
    for q,counts in ext.items():
        assert counts['B_minus']==counts['B_plus']+counts['A_flux']
        assert counts['A_flux']<=RA
        byh=Counter(row['bit'][1] for row in extrows if row['extreme']==q and row['plus'])
        assert max(byh.values(),default=0)<=1 and counts['B_plus']<=KB
    boundary_records=[]
    for q in set(exts):
        bit=1<<(q-1);away=Counter();losses=[]
        for p,d in ds.items():
            if not d['F']&bit:continue
            toward=(d['target']<d['g']) if q==S[0] else (d['target']>d['g'])
            if toward:
                j=0 if d['case'] in ('LL','RR') else 1;t=d['events'][j];e=evs[t-1]
                assert e['pivot']==d['g']
                assert extdelta[q,tuple(e['id'])][1]==1
                losses.append(p)
            else:away[p[0]]+=1
        assert max(away.values(),default=0)<=1
        assert len(losses)<=ext[q]['B_minus'] and sum(away.values())<=KB
        assert len(losses)+sum(away.values())<=RA+2*KB
        boundary_records.append({'extreme':q,'toward_double_count':len(losses),'away_double_count':sum(away.values()),
            'max_away_doubles_per_KEEP':max(away.values(),default=0),'flow':dict(ext[q])})
    presence=Presence(initialA,achanges,T)
    U={};classes={};exposure_donors=set();output_births={}
    for p,d in sorted(ds.items()):
        if d['signs']!=[0,0]:classes[p]={'class':'nonneutral'};continue
        if d['F']&extremes:classes[p]={'class':'boundary'};continue
        post=phys['boundaries'][p[0]-1]['post_A_time']
        gam=previous(bcreates[d['F']],post+1,T);kap=previous(blosses[d['F']],gam,T)
        assert 0<post-kap<=T and not presence.at(d['F'],kap) and not presence.at(d['F'],post)
        expose=presence.any(d['F'],kap,post)
        if expose:
            donor=presence.first_creation(d['F'],kap);assert donor is not None and donor<=post
            original_time=(donor-1)%T+1;assert original_time not in exposure_donors;exposure_donors.add(original_time)
            assert evs[original_time-1]['actor']=='A' and d['F'] in evs[original_time-1]['created']
            classes[p]={'class':'whole_frame_exposed','A_donor':evs[original_time-1]['id'],'Gamma':gam,'kappa':kap};continue
        t=gam%T or T;creator=evs[t-1]
        assert creator['actor']=='B' and creator['pivot']==d['g'] and creator['case']!='ZIG'
        assert creator['sign']==0 and d['F'] in creator['created']
        cp=tuple(creator['id'][1:3]);cd=ds[cp]
        if creator['pivot']==cd['g']:
            kind='grandparent';assert d['F']==cd['J']
        else:
            kind='parent';assert creator['pivot']==cd['p'] and d['F']==cd['P_output']
        assert d['F']&~cd['F']==0 and d['F']!=cd['F']
        # First physical entry of that exact output is this consuming access.
        first=None
        for dt in range(1,N+1):
            h=(cp[0]+dt-1)%N+1;tag,x=s['operations'][h-1]
            if tag=='K' and d['F']&(1<<(x-1)):first=h;break
        assert first==p[0]
        U[p]={'Gamma':gam,'kappa':kap,'post_A':post,'creator':cp,'creator_bit':creator['id'],'output_kind':kind}
        classes[p]={'class':'U'};output_births[p]=creator
    counts=Counter(z['class'] for z in classes.values())
    A=sum(z['a'] for z in phys['boundaries'])
    assert counts['nonneutral']<=totals['DB']<=RA
    assert counts['whole_frame_exposed']<=RA
    assert counts['boundary']<=2*RA+4*KB
    assert len(ds)-len(U)<=4*RA+4*KB<=12*A
    # Finish original first-hit/exposure metadata for direct comparison to old certificates.
    for p,ud in U.items():
        d=ds[p];found=None
        for dt in range(1,N+1):
            h=(p[0]+dt-1)%N+1;tag,x=s['operations'][h-1]
            if tag=='K' and d['J']&(1<<(x-1)):
                hi=phys['boundaries'][h-1]['post_A_time']+(T if h<=p[0] else 0);found=(h,hi);break
        assert found is not None;h,hi=found;nu=d['events'][0 if d['case'] in ('LL','RR') else 1]
        ud.update(h=h,hit_time=hi,exposed=presence.any(d['J'],nu,hi))
    from cohortc import classify
    cohorts=classify(s,phys,U,presence)
    r6by=defaultdict(list)
    for z in cohorts['original_R6']:r6by[tuple(z['parent'])].append(z)
    crows=[];successors=defaultdict(list);allbirths=Counter();deep_orig=[]
    wm={tuple(z['parent']):z['w'] for z in weights['vertices']} if weights is not None else None
    starby=defaultdict(list)
    for rho in known_star or []:starby[tuple(rho['original_parent'])].append(rho)
    for p,ud in sorted(U.items()):
        cp=ud['creator'];allbirths[tuple(ud['creator_bit'])]+=1
        assert allbirths[tuple(ud['creator_bit'])]<=1
        if V[p]['type']!='C':continue
        if ud['output_kind']=='grandparent':assert cp==tuple(V[p]['predecessor'])
        else:assert ds[cp]['case'] in ('LR','RL') and ud['creator_bit'][3]==0
        status='UU' if cp in U else 'paid_nonU_creator'
        row={'consumer':p,'old_g':ds[p]['g'],'distance':depth[p],'Gamma':ud['Gamma'],
            'creator':cp,'birth_bit':ud['creator_bit'],'output_kind':ud['output_kind'],
            'creator_class':classes[cp]['class'],'status':status,
            'actual_deep_gap_weight':(wm[p] if depth[p]>2 else 0) if wm is not None else None,
            'original_R6_gaps':r6by[p],
            'known_original_R_star_gaps':starby[p]}
        crows.append(row);successors[cp].append(row)
        if starby[p] and depth[p]>2:deep_orig.append(row)
    for cp,zs in successors.items():
        assert len(zs)<=2
        if len(zs)==2:
            assert ds[cp]['case'] in ('LR','RL')
            f1,f2=(ds[tuple(v['consumer'])]['F'] for v in zs);assert not f1&f2
    all_nonU_children=sum(ud['creator'] not in U for ud in U.values())
    assert all_nonU_children<=2*(len(ds)-len(U))<=24*A
    return {'source':s['name'],'source_sha256':digest(s),'A':A,'Q_B':len(ds),'real_A_bits':RA,'genuine_B_accesses':KB,
        **cohorts,
        'original_SET_and_sign_checks':len(evs),'sign_inventory':dict(totals),'extreme_flows':boundary_records,
        'double_partition_counts':dict(counts),'nonU_double_bound':12*A,'all_nonU_U_children':all_nonU_children,
        'U':{str(p):v for p,v in U.items()},'double_classes':{str(p):v for p,v in classes.items()},
        'C_U_births':crows,'deep_original_R_star_C_births':deep_orig,
        'nonU_creator_children_gap_capacity':3*all_nonU_children,'global_gap_capacity_bound':72*A,
        'all_physical_C':sum(v['type']=='C' for v in V.values()),'all_U_C':len(crows),
        'all_deep_U_C':sum(z['distance']>2 for z in crows),
        'nonU_deep_U_C':sum(z['distance']>2 and z['status']=='paid_nonU_creator' for z in crows),
        'known_original_R_star_C_gaps':sum(len(z['known_original_R_star_gaps']) for z in crows) if known_star is not None else None,
        'known_original_R_star_scope':'Archived exact membership' if known_star is not None else 'NOT_CLASSIFIED; no assertion of emptiness',
        'actual_R_C':sum(wm[p] for p in V if V[p]['type']=='C') if wm is not None else None,
        'actual_R_C_deep':sum(wm[p] for p in V if V[p]['type']=='C' and depth[p]>2) if wm is not None else None,
        'actual_weight_scope':'Literal supplied original weight records' if wm is not None else 'NOT_CLASSIFIED'}
