from fast_physics import *
import random


def common_dilated(active_n,stride=1):
    assert stride%2==1
    n=1+(active_n-1)*stride;active=[1+i*stride for i in range(active_n)]
    left={'root':n,'children':{str(k):[k-1 if k>1 else None,None] for k in range(1,n+1)}}
    t=FullTree(left);other=FullTree(left)
    for x in active[-2::-1]:t.splay(x,other,'A')
    st=t.state();T=Tree(st)
    assert all(set(T.path(x))<=set(active) for x in active)
    return st,active


def warm_cycle(diag,prep,word,max_warm=24):
    a=FullTree(diag);b=FullTree(diag)
    for tag,x in prep:
        a.splay(x,b,'A')
        if tag=='K':b.splay(x,a,'B')
    seen={};states=[]
    for j in range(max_warm+1):
        key=(a.code,b.code)
        if key in seen:
            start=seen[key];aa,bb=states[start]
            return {'initial_A':aa,'initial_B':bb,'reaching_prefix':prep+word*start,
                    'V':word*(j-start),'warmup_copies':start,'cycle_copies':j-start}
        seen[key]=j;states.append((a.state(),b.state()))
        for tag,x in word:
            a.splay(x,b,'A')
            if tag=='K':b.splay(x,a,'B')
    return None


def build_source(name,active_n,stride,prep,word,copies=64):
    diag,active=common_dilated(active_n,stride);n=len(diag['children'])
    phi=lambda w:[[tag,1+(x-1)*stride] for tag,x in w]
    cycle=warm_cycle(diag,phi(prep),phi(word))
    if cycle is None:return None
    restore=ops('K',range(1,n+1))+ops('K',active[-2::-1])+cycle['reaching_prefix']
    return {'name':name,'family':'dilated_exact_warmed_cycle_plus_full_support_restoration',
            'diagonal_initial':diag,'initial_A':cycle['initial_A'],'initial_B':cycle['initial_B'],
            'reaching_prefix':cycle['reaching_prefix'],'operations':cycle['V']*copies+restore,
            'V':cycle['V'],'restoration':restore,'copies':copies,'active_n':active_n,'stride':stride,
            'warmup_copies':cycle['warmup_copies'],'cycle_copies':cycle['cycle_copies'],
            'full_support_reason':'restoration visits every key increasingly and then the active minimum after maximum',
            'reachability':'explicit original prep and warm word from saved complete common diagonal; prefix excluded'}


def patterns(n):
    even=list(range(2,n,2));allk=list(range(1,n+1))
    def alternating(xs):
        out=[];lo=0;hi=len(xs)-1
        while lo<=hi:
            out.append(xs[lo]);lo+=1
            if lo<=hi:out.append(xs[hi]);hi-=1
        return out
    def bitreverse(xs):
        width=n.bit_length();return sorted(xs,key=lambda x:int(f'{x:0{width}b}'[::-1],2))
    for targets in (even,even[::2],allk):
        for xs in (targets,targets[::-1],alternating(targets),bitreverse(targets)):
            for prep in ([['D',n//2]],[['D',n//2],['D',2],['D',n//2]],ops('D',range(1,n+1)),
                         [['D',x] for x in (3,n-2,n//2,1,n)]):
                yield prep,ops('K',xs)
    rng=random.Random(20261110+n)
    for trial in range(48):
        pool=even if trial%2 else even[::2]
        xs=[]
        for j in range(2*len(pool)):
            if trial%3==0:xs.append(pool[j//2%len(pool)] if j%2==0 else pool[-1-j//2%len(pool)])
            else:xs.append(rng.choice(pool))
        word=[]
        for x in xs:
            if rng.random()<0.035:word.append(['D',rng.randrange(1,n+1)])
            word.append(['K',x])
        prep=ops('D',[rng.randrange(1,n+1) for _ in range(4)])
        yield prep,word


if __name__=='__main__':
    meter=Meter('active_cycle_screen');rows=[];shortlist=[]
    # These are original closed active cycles used to screen a larger full-
    # support construction. No Pi/R6/R_next classification is inferred here.
    for n in (17,65,257):
        diag,_=common_dilated(n,1)
        for k,(prep,word) in enumerate(patterns(n)):
            cyc=warm_cycle(diag,prep,word)
            if cyc is None:
                rows.append({'active_n':n,'pattern':k,'status':'no paired return found in warm limit'});continue
            s={'name':f'active_n{n}_p{k}','initial_A':cyc['initial_A'],'initial_B':cyc['initial_B'],'operations':cyc['V']}
            r=physical_replay(s)
            H=skeleton_cost(r,variant='H');G=skeleton_cost(r,variant='G')
            row={'active_n':n,'pattern':k,'A_V':r['A'],'Q_V':r['Q_B'],'V_length':len(cyc['V']),
                 'H':{a:b for a,b in H.items() if a!='retained_original_operations'},
                 'G':{a:b for a,b in G.items() if a!='retained_original_operations'},
                 'prep':prep,'word':word,'reaching_prefix':cyc['reaching_prefix'],
                 'status':'complete paired active-cycle physical screen; S assumed full for future restored source'}
            rows.append(row)
            if H['guard_count']:
                shortlist.append(row)
                print('candidate',n,k,'A',r['A'],'Q',r['Q_B'],'Hguards',H['guard_count'],
                      'local cyclic',H['B_cyclic'],'J',H['J_size'],flush=True)
            if k%12==0:write('ACTIVE_CYCLE_SCREEN.json',rows);write('ACTIVE_SHORTLIST.json',shortlist)
            del r
        print('finished active_n',n,'shortlist',len(shortlist),flush=True)
    write('ACTIVE_CYCLE_SCREEN.json',rows);write('ACTIVE_SHORTLIST.json',shortlist)
    meter.success=True;meter.details.update(trials=len(rows),shortlist=len(shortlist),
        qualification='No screened active cycle has been declared an original R_next^P escape')
