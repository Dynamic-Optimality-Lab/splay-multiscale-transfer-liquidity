from campaign3 import *
from verify_checkpoint import tuple_rotate
from bisect import bisect_right


def data(tree,bits):
    labels={};edges=set();todo=[(tree,False)]
    while todo:
        z,done=todo.pop()
        if z[0]=='leaf':continue
        _,k,l,rr=z
        if not done:todo.extend([(z,True),(l,False),(rr,False)]);continue
        labels[k]=bits.get(k,0)|(labels[l[1]] if l[0]=='node' else 0)|(labels[rr[1]] if rr[0]=='node' else 0)
        if l[0]=='node':edges.add((k,l[1],0))
        if rr[0]=='node':edges.add((k,rr[1],1))
    return set(labels.values())-{0},edges,labels


def check(r):
    a=r.as_tuple(Tree(r.source['initial_A']));b=r.as_tuple(Tree(r.source['initial_B']))
    aset,_,_=data(a,r.bits);bset,_,_=data(b,r.bits)
    present={lab:0 for lab in aset};intervals=defaultdict(list)
    creates=defaultdict(list);losses=defaultdict(list)
    for ev in r.events:
        actor=ev['actor'];tree=a if actor=='A' else b;before=aset if actor=='A' else bset
        before2,edges,labs=data(tree,r.bits);assert before2==before
        if actor=='B' and ev['id'][3]==0 and ev['case']!='ZIG':
            cur=tree;path=[]
            while cur[0]=='node':
                path.append(cur[1])
                if cur[1]==ev['target']:break
                cur=cur[2] if ev['target']<cur[1] else cur[3]
            g,p,x=path[-3:];d=r.doubles[tuple(ev['id'][1:3])]
            assert (d['g'],d['F'],d['case'])==(g,labs[g],('R' if p>g else 'L')+('R' if x>p else 'L'))
        newtree=tuple_rotate(r.ind,tree,ev['pivot'],ev['side'])
        after,newedges,newlabs=data(newtree,r.bits)
        lost=before-after;born=after-before
        assert sorted(lost)==ev['lost'] and sorted(born)==ev['created']
        assert sorted(edges-newedges)==list(map(tuple,ev['deleted']))
        assert sorted(newedges-edges)==list(map(tuple,ev['added']))
        if actor=='A':
            assert len(lost&bset)-len(born&bset)==ev['sign']
            for lab in lost:intervals[lab].append((present.pop(lab),ev['time']-1))
            for lab in born:assert lab not in present;present[lab]=ev['time']
            a=newtree;aset=after
        else:
            assert len(after-aset)-len(before-aset)==ev['sign']
            for lab in lost:losses[lab].append(ev['time'])
            for lab in born:creates[lab].append(ev['time'])
            b=newtree;bset=after
            if ev['case']!='ZIG':
                d=r.doubles[tuple(ev['id'][1:3])]
                if d['nu']==ev['time']:assert d['J']==newlabs[ev['pivot']]
    assert a==r.as_tuple(Tree(r.source['initial_A'])) and b==r.as_tuple(Tree(r.source['initial_B']))
    for lab,start in present.items():intervals[lab].append((start,r.T))
    starts={lab:[a for a,b in ss] for lab,ss in intervals.items()}
    def line(lab,lo,hi):
        if lab not in starts:return False
        i=bisect_right(starts[lab],hi)-1
        return i>=0 and intervals[lab][i][1]>=lo
    def any_A(lab,lo,hi):
        assert 0<=hi-lo<=r.T
        end=lo%r.T+(hi-lo);lo%=r.T
        return line(lab,lo,min(end,r.T)) or (end>=r.T and line(lab,0,end-r.T))
    def prev(times,before):return max(t+((before-1-t)//r.T)*r.T for t in times)
    us={}
    for key,d in r.doubles.items():
        if d['signs']!=[0,0] or d['F']&r.extremes:continue
        post=r.boundaries[key[0]-1]['post_A_time'];gamma=prev(creates[d['F']],post+1);kappa=prev(losses[d['F']],gamma)
        if any_A(d['F'],kappa,post):continue
        h=next((key[0]+dt-1)%len(r.ops)+1 for dt in range(1,len(r.ops)+1)
               if r.ops[(key[0]+dt-1)%len(r.ops)][0]=='K' and r.bits.get(r.ops[(key[0]+dt-1)%len(r.ops)][1],0)&d['J'])
        hit=r.boundaries[h-1]['post_A_time']+(r.T if h<=key[0] else 0)
        z={'Gamma':gamma,'kappa':kappa,'post_A':post,'h':h,'hit_time':hit,'exposed':any_A(d['J'],d['nu'],hit)}
        assert all(d[k]==v for k,v in z.items());us[str(key)]=z
    assert set(us)=={str(k) for k in r.U}
    return {'source':r.source['name'],'complete_immutable_primitive_rotations':r.T,
        'full_SET_edge_sign_frame_checks':True,'independently_reconstructed_all_original_U':us,
        'A_presence_interval_count':sum(len(v) for v in intervals.values()),
        'qualification':'All full primitive SET/Pi/U predicates independently rebuilt using exact carrier-presence intervals. Higher original first-hit cohort and residual selectors remain the pinned implementations.'}


if __name__=='__main__':
    meter=Meter('large_Pi_and_accounting')
    from new_payments import intern_original_states
    from accounting import audit
    pool=intern_original_states()
    s=next(s for s in json.loads((ROOT/'SCALING_SOURCES.json').read_text()) if s['p']==6)
    r=Replay(s);star,_,_=original_residual(r)
    old=next(z for z in json.loads((ROOT/'SCALING_RESULTS.json').read_text()) if z['source']==s['name'])
    assert star==old['original_R_star'] and digest(r.events)==s['trace_hash']
    z=check(r);write('LARGE_INDEPENDENT_PI.json',z)
    a=audit(r,star);write('LARGE_ORDERED_ACCOUNTING.json',a)
    print('PASS full independent Pi/U',r.T,'bits;',len(r.U),'U; strict new post-frozen/prefix',
          len(a['strict_new_E_C_minus_own']),'old periodic funded',a['positive_old_periodic_certificate'] is not None,flush=True)
    meter.success=True
