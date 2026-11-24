"""Independent primitive edge-list updater, chain and physical flux audit.

No splay rotation engine is called by this module. Input primitives are
validated through their literal deleted/added edges and complete states.
"""
from base1 import *
from bisect import bisect_left

class Edges:
    def __init__(self,st):
        self.n=len(st['children']);self.root=st['root']
        self.c=[[0,0]]+[[z or 0 for z in st['children'][str(k)]] for k in range(1,self.n+1)]
        self.p=[0]*(self.n+1);self.m=[0]*(self.n+1)
        for k in range(1,self.n+1):
            for x in self.c[k]:
                if x:self.p[x]=k
        self.recompute()
    def recompute(self):
        stack=[(self.root,False)];seen=set();new=[0]*(self.n+1)
        while stack:
            k,done=stack.pop()
            if not k:continue
            if done:
                l,r=self.c[k];new[k]=(1<<(k-1))|new[l]|new[r]
            else:
                assert k not in seen;seen.add(k);stack.append((k,True))
                stack.extend((z,False) for z in self.c[k] if z)
        assert len(seen)==self.n and new[self.root]==(1<<self.n)-1
        if any(self.m):assert new==self.m
        self.m=new
    def path(self,x):
        out=[];k=self.root
        while k:
            out.append(k)
            if k==x:return out
            k=self.c[k][int(x>k)]
        raise AssertionError('target missing')
    def code(self):
        b=(self.n+1).bit_length();z=self.root<<(2*self.n*b)
        for k in range(1,self.n+1):
            l,r=self.c[k];z|=l<<((2*k-2)*b);z|=r<<((2*k-1)*b)
        return z
    def step(self,e):
        u,v,side=e['pivot'],e['promoted'],e['side']
        assert self.c[u][side]==v
        c=self.p[u];middle=self.c[v][1-side]
        assert (c or None)==e['external'] and (middle or None)==e['middle']
        expected_del={(u,v,side)};expected_add={(v,u,1-side)}
        if c:
            slot=int(self.c[c][1]==u);assert self.c[c][slot]==u
            expected_del.add((c,u,slot));expected_add.add((c,v,slot))
        if middle:expected_del.add((v,middle,1-side));expected_add.add((u,middle,side))
        assert set(map(tuple,e['deleted']))==expected_del
        assert set(map(tuple,e['added']))==expected_add
        for a,b,s in e['deleted']:
            assert self.c[a][s]==b;self.c[a][s]=0;self.p[b]=0
        for a,b,s in e['added']:
            assert self.c[a][s]==0;self.c[a][s]=b;self.p[b]=a
        if not c:self.root=v;assert self.p[v]==0
        l,r=self.c[u];self.m[u]=(1<<(u-1))|self.m[l]|self.m[r]
        l,r=self.c[v];self.m[v]=(1<<(v-1))|self.m[l]|self.m[r]
    def component(self,g):
        out=[];stack=[g]
        while stack:
            k=stack.pop();l,r=self.c[k];out.append((k,l,r))
            if l:stack.append(l)
            if r:stack.append(r)
        return sorted(out)

def between(lo,hi,T):
    if hi<lo:hi+=T
    return [(t%T) for t in range(lo,hi)] if T else []

def analyze(s,phys,forest,weights):
    a,b=Edges(s['initial_A']),Edges(s['initial_B']);a0,b0=a.code(),b.code()
    core=sum(1<<(k-1) for k in phys['original_S'])
    evs=phys['events'];N=len(s['operations']);T=len(evs)
    ds={tuple(z['parent']):z for z in phys['doubles']}
    verts={tuple(z['parent']):z for z in forest['vertices']}
    ws={tuple(z['parent']):z['w'] for z in weights['vertices']}
    assert set(ds)==set(verts)==set(ws)
    flux=[];tot=Counter();Ag={};shapes={};fringe={};donors={};gain_events=defaultdict(list);loss_events=defaultdict(list)
    phi=0;initial_phi=sum(((b.m[k]&core)&~a.m[k]).bit_count() for k in range(1,a.n+1));phi=initial_phi
    byh=defaultdict(list)
    for v in sorted(ds):byh[v[0]].append(v)
    real_A_ids={tuple(e['id']):e for e in evs if e['actor']=='A'}
    for row,(tag,x) in zip(phys['boundaries'],s['operations']):
        h=row['t'];assert (row['tag'],row['x'])==(tag,x)
        assert a.code()==int(phys['state_pool']['states'][row['pre_A_state']],16)
        assert b.code()==int(phys['state_pool']['states'][row['pre_B_state']],16)
        assert a.path(x)==row['A_path']
        path=set(row['A_path'])
        for v in byh[h]:
            if verts[v]['type']!='C':continue
            g=ds[v]['g'];assert g not in path
            z=g;depth=0
            while z not in path:z=a.p[z];depth+=1;assert z
            fringe[v]={'distance':depth,'attachment':z,'kind':'target' if z==x else 'strict_ancestor'}
        for k in range(row['start_time'],row['end_time']):
            e=evs[k];assert e['time']==k+1
            actor=e['actor'];tree,other=(a,b) if actor=='A' else (b,a)
            assert (k<row['post_A_time'])==(actor=='A')
            u,v=e['pivot'],e['promoted'];old_u,old_v=tree.m[u],tree.m[v]
            pair_before=sum(((b.m[z]&core)&~a.m[z]).bit_count() for z in (u,v))
            indicator_before=sum(bool((b.m[z]&core)&~a.m[z]) for z in (u,v))
            old_g_indicator=bool((b.m[u]&core)&~a.m[u])
            tree.step(e);new_u,new_v=tree.m[u],tree.m[v]
            lost=old_u&~new_u;gained=new_v&~old_v
            assert new_u&~old_u==0 and old_v&~new_v==0
            if actor=='A':
                plus=(lost&b.m[u]&core).bit_count();minus=(gained&b.m[v]&core).bit_count()
                tot['A_created_atoms']+=plus;tot['A_destroyed_atoms']+=minus;delta=plus-minus
                tot['A_signed_flux']+=delta;tot['A_positive_flux']+=max(0,delta)
            else:
                plus=(gained&core&~a.m[v]).bit_count();minus=(lost&core&~a.m[u]).bit_count();delta=plus-minus
                assert minus>=1 # the current target is lost at this pivot and absent from its A subtree
                assert lost&(1<<(x-1)) and not a.m[u]&(1<<(x-1))
                tot['B_gain_atoms']+=plus;tot['B_loss_atoms']+=minus
                if v==x:assert plus==0
                else:assert e['case'] in ('LL','RR') and e['id'][3]==0
                gain_events[v].append({'time':k+1,'id':e['id'],'keys':gained&core,'target':x})
                loss_events[u].append({'time':k+1,'id':e['id'],'keys':lost&core})
            pair_after=sum(((b.m[z]&core)&~a.m[z]).bit_count() for z in (u,v))
            indicator_after=sum(bool((b.m[z]&core)&~a.m[z]) for z in (u,v))
            assert pair_after-pair_before==delta
            phi+=delta
            assert phi>=0
            flux.append({'id':e['id'],'time':k+1,'created_atoms':plus,'destroyed_atoms':minus,'delta_Phi':delta,
                'delta_indicator':indicator_after-indicator_before,'pivot_indicator_before':old_g_indicator,
                'pivot_indicator_after':bool((b.m[u]&core)&~a.m[u])})
            if k+1==row['post_A_time']:
                for parent in byh[h]:
                    g=ds[parent]['g'];Ag[parent]=a.m[g];shapes[parent]=a.component(g)
        # Handles zero-cost A access and zero-bit operations as well.
        for parent in byh[h]:
            g=ds[parent]['g'];Ag.setdefault(parent,a.m[g]);shapes.setdefault(parent,a.component(g))
        a.recompute();b.recompute()
        assert a.code()==int(phys['state_pool']['states'][row['post_A_state']],16)
        assert b.code()==int(phys['state_pool']['states'][row['post_B_state']],16)
        assert phi==sum(((b.m[z]&core)&~a.m[z]).bit_count() for z in range(1,a.n+1))
    assert (a.code(),b.code())==(a0,b0) and phi==initial_phi
    assert tot['B_loss_atoms']==tot['B_gain_atoms']+tot['A_signed_flux']
    Q=len(ds);Z=sum(e['actor']=='B' and e['case']=='ZIG' for e in evs)
    assert 2*Q+Z<=tot['B_loss_atoms']
    C=[v for v in sorted(verts) if verts[v]['type']=='C'];Cchild={}
    chains=[];lives=[];life_ids=set();indicator_failures=[]
    for v in C:
        u=tuple(verts[v]['predecessor']);assert u not in Cchild;Cchild[u]=v
        g=ds[v]['g'];assert ds[u]['g']==g
        assert Ag[u]==Ag[v] and shapes[u]==shapes[v]
        lo=phys['boundaries'][u[0]-1]['end_time'];hi=phys['boundaries'][v[0]-1]['post_A_time']
        for k in between(lo,hi,T):
            e=evs[k]
            if e['actor']=='A':assert e['pivot']!=g and e['promoted']!=g
            else:assert e['promoted']!=g
        length=(v[0]-u[0])%N
        assert length>0
        for j in range(1,length+1):
            _,target=s['operations'][(u[0]-1+j)%N];assert not Ag[u]&(1<<(target-1))
        x=ds[u]['target'];bit=0 if ds[u]['case'] in ('LL','RR') else 1
        t=ds[u]['events'][bit];close=evs[t-1]
        assert close['pivot']==g and close['id']==['B',u[0],u[1],bit]
        assert flux[t-1]['pivot_indicator_before'] and flux[t-1]['pivot_indicator_after']
        indicator_failures.append({'C_child':v,'predecessor':u,'old_g':g,'bit':close['id'],
            'pivot_indicator_before':True,'pivot_indicator_after':True,'weight':ws[v]})
        gains=[e for e in gain_events[g] if e['keys']&(1<<(x-1))]
        losses=[e for e in loss_events[g] if e['keys']&(1<<(x-1))]
        assert gains and losses
        before=[e for e in gains if e['time']<t];opener=before[-1] if before else gains[-1]
        distance=(t-opener['time'])%T;assert distance>0
        assert all(not (0<(e['time']-opener['time'])%T<distance) for e in losses)
        life=(tuple(opener['id']),g,x,tuple(close['id']));assert life not in life_ids;life_ids.add(life)
        lives.append({'C_child':v,'predecessor':u,'g':g,'retired_target':x,'original_opening_bit':opener['id'],
            'opening_kind':'target' if opener['target']==g else 'non_target',
            'original_closing_bit':close['id'],'opening_gain_capacity':opener['keys'].bit_count(),
            'original_weight':ws[v]})
    for head in sorted(verts):
        if verts[head]['type']=='C':continue
        chain=[head]
        while chain[-1] in Cchild:chain.append(Cchild[chain[-1]])
        g=ds[head]['g'];xs=[ds[v]['target'] for v in chain]
        assert len(xs)==len(set(xs))
        left=[x for x in xs if x<g];right=[x for x in xs if x>g]
        assert left==sorted(left) and right==sorted(right,reverse=True)
        assert all(Ag[v]==Ag[head] and shapes[v]==shapes[head] for v in chain)
        chains.append({'head':head,'head_type':verts[head]['type'],'g':g,'vertices':chain,'targets':xs,
            'A_component_keys_mask':Ag[head],'A_component_shape':shapes[head],
            'C_count':len(chain)-1,'original_R_C_weight':sum(ws[v] for v in chain[1:])})
    assert sum(z['C_count'] for z in chains)==len(C)
    assert sum(len(z['vertices']) for z in chains)==len(verts)
    # Independently construct the bounded-fringe map for all physical C vertices.
    gs={}
    ks=[j for j,(tag,x) in enumerate(s['operations']) if tag=='K']
    for j,i in enumerate(ks):
        prev=ks[j-1];length=(i-prev)%N or N
        hs=[(prev+k)%N+1 for k in range(1,length+1)]
        units=[]
        for h in hs:
            units+=sorted({tuple(e['id'][:3]) for e in evs[phys['boundaries'][h-1]['start_time']:phys['boundaries'][h-1]['post_A_time']]})
        assert len(units)==sum(phys['boundaries'][h-1]['a'] for h in hs)
        gs[i+1]=units
    radius_results=[]
    for radius in (1,2,3):
        mapping=[];unit_load=Counter();bit_load=Counter();target_load=Counter();wload=Counter()
        for v in C:
            z=fringe[v]
            if z['distance']>radius:continue
            h=v[0]
            if z['kind']=='strict_ancestor':
                bit=next(tuple(e['id']) for e in evs[phys['boundaries'][h-1]['start_time']:phys['boundaries'][h-1]['post_A_time']] if e['pivot']==z['attachment'])
                bit_load[bit]+=1;unit=bit[:3]
            else:
                assert gs[h];unit=gs[h][0];bit=None;target_load[unit]+=1
            unit_load[unit]+=1;wload[unit]+=ws[v]
            mapping.append({'vertex':v,'distance':z['distance'],'attachment':z['attachment'],'role':z['kind'],
                'actual_A_bit':bit,'actual_A_StepEv':unit,'original_gap_weight':ws[v]})
        width=(1<<radius)-1
        assert max(bit_load.values(),default=0)<=width
        assert max(target_load.values(),default=0)<=2*width
        assert max(unit_load.values(),default=0)<=4*width
        A=sum(z['a'] for z in phys['boundaries'])
        assert len(mapping)<=4*width*A and sum(wload.values())<=12*width*A
        radius_results.append({'radius':radius,'global_gap_coefficient':12*width,'selected_physical_C_parents':len(mapping),
            'selected_original_gap_weight':sum(wload.values()),'maximum_parent_load_per_actual_A_StepEv':max(unit_load.values(),default=0),
            'mapping':mapping})
    packet=defaultdict(list)
    for z in lives:packet[tuple(z['original_opening_bit'])].append(z)
    restoration_packets=[{'opening_bit':bit,'kind':zs[0]['opening_kind'],'physical_C_ticket_count':len(zs),
        'gain_capacity':zs[0]['opening_gain_capacity'],'original_gap_weight':sum(z['original_weight'] for z in zs),
        'C_children':[z['C_child'] for z in zs]} for bit,zs in sorted(packet.items())]
    assert all(z['physical_C_ticket_count']<=z['gain_capacity'] for z in restoration_packets)
    return {'source':s['name'],'A':sum(z['a'] for z in phys['boundaries']),'Q_B':Q,'Z_B':Z,
        'primitive_edges_and_all_complete_boundaries_verified':True,'flux_totals':dict(tot),'primitive_flux':flux,
        'C_parent_count':len(C),'maximal_C_chains':chains,'maximum_C_chain_edges':max((z['C_count'] for z in chains),default=0),
        'C_fringe_depths':[{'vertex':v,**fringe[v],'original_gap_weight':ws[v]} for v in C],
        'exact_B_ancestry_lifetimes':lives,'restoration_packets':restoration_packets,
        'saturated_column_counterexamples':indicator_failures,'bounded_fringe_payments':radius_results,
        'actual_R_C':sum(ws[v] for v in C),'actual_R_P':sum(ws[v] for v in verts if verts[v]['type']=='P')}
