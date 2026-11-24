from fast_physics import *


def trees(lo,hi):
    if lo>hi:return [None]
    return [(k,l,r) for k in range(lo,hi+1) for l in trees(lo,k-1) for r in trees(k+1,hi)]


def state(t):
    ch={}
    def rec(z):
        if z is None:return None
        k,l,r=z;ch[str(k)]=[rec(l),rec(r)];return k
    return {'root':rec(t),'children':ch}


def spines(t):
    ans=set()
    for side in (0,1):
        k=t.root
        while k:ans.add(k);k=(t.r if side else t.l)[k]
    return ans


if __name__=='__main__':
    meter=Meter('structural_and_small_return_checks');checks=0
    for n in range(1,7):
        for t in trees(1,n):
            st=state(t);original=FullTree(st)
            for x in range(1,n+1):
                path=original.path(x)
                if len(path)>3:continue
                b=FullTree(st);old=spines(b);b.splay(x,b,'A');new=spines(b)
                zigzag=len(path)==3 and (path[1]>path[0])!=(x>path[1])
                assert new==old|{x} if zigzag else new==old
                if len(path)==2:
                    b.splay(st['root'],b,'A');assert b.state()==st
                checks+=1
    s={'name':'C02_missing_root_coupling_control','initial_A':{'root':3,'children':{'1':[None,None],'2':[1,None],'3':[2,None]}},
        'operations':[['D',1],['K',1],['K',3]],'reaching_prefix':[]}
    s['initial_B']=s['initial_A'];r=Replay(s)
    localA=sum(b['a'] for b in r.boundaries[1:]);localQ=sum(b['q'] for b in r.boundaries[1:])
    assert r.closed and r.A==2 and r.Q==2 and localA==1 and localQ==2
    assert r.boundaries[1]['pre_B']==r.boundaries[-1]['post_B']
    assert r.boundaries[1]['pre_A']['root']!=r.boundaries[1]['pre_B']['root']
    write('ROOT_COUPLING_COUNTEREXAMPLE.json',{'source':s,'A':r.A,'Q_B':r.Q,'local_operations':[2,3],
        'local_A':localA,'local_Q_B':localQ,'full_original_events':r.events,'full_original_boundaries':r.boundaries,
        'pointwise_uncoupled_b2_bound_refuted':True,'coupled_extension_operations':[1,2,3],
        'independent_original_operations':r.independent_checks})
    rootchecks=0
    for start in range(3):
        for length in range(1,4):
            ids=[(start+j)%3 for j in range(length)];bs=[r.boundaries[i] for i in ids]
            if bs[0]['pre_B']!=bs[-1]['post_B']:continue
            M={b['x'] for b in bs if b['tag']=='K' and len(b['B_path'])>1}
            A=sum(b['a'] for b in bs);Q=sum(b['q'] for b in bs)
            if M and bs[0]['pre_A']['root']==bs[0]['pre_B']['root']:
                J=path_hull(Tree(bs[0]['pre_B']),M)
                assert len(J)<=2*len(M)-1 and Q<=(len(M)-1)*A;rootchecks+=1
    write('STRUCTURAL_VERIFICATION.json',{'root_zig_and_spine_cases':checks,'B_return_root_coupled_cyclic_checks':rootchecks,
        'scope':'Finite independent sanity checks; universal validity is the analytic proof in PROOF_LEDGER.md.',
        'full_original_root_coupling_counterexample_verified':True})
    print('PASS',checks,'root zig/spine cases and complete source boundary control',flush=True);meter.success=True
