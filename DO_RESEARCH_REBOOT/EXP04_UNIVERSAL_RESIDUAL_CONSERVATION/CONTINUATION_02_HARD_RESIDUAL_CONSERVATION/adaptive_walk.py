from fast_physics import *
import random,copy


def clone(t):
    z=object.__new__(FullTree)
    for key,value in t.__dict__.items():setattr(z,key,value.copy() if isinstance(value,(list,set)) else value)
    return z


def shallow(t,maxdepth):
    todo=[(t.root,0)];out=[]
    while todo:
        k,d=todo.pop();out.append((k,d))
        if d<maxdepth:
            if t.l[k]:todo.append((t.l[k],d+1))
            if t.r[k]:todo.append((t.r[k],d+1))
    return out


def make(n,seed,length=6000):
    diag=vine(range(1,n+1));a=FullTree(diag);b=FullTree(diag);rng=random.Random(seed)
    width=n.bit_length();targets=sorted(range(1,n+1),key=lambda x:int(f'{x:0{width}b}'[::-1],2))
    prefix=ops('K',targets);word=list(prefix);seen={b.code}
    for tag,x in prefix:a.splay(x,b,'A');b.splay(x,a,'B');seen.add(b.code)
    body=[];A=Q=0;guards=0;novel=0;emergency=0;Agap=0;bodytargets=[];localstats=[]
    for k in range(length):
        if rng.random()<0.075:
            pool=[x for x,d in shallow(a,2) if x!=a.root]
            x=rng.choice(pool);aa,_,_,_=a.splay(x,b,'A');body.append(['D',x]);A+=aa;Agap+=aa
        candidates=[(x,d) for x,d in shallow(a,4) if x!=b.root]
        rng.shuffle(candidates)
        candidates.sort(key=lambda z:((z[1]+1)//2-0.35*abs(z[0]-b.root).bit_length()))
        chosen=None
        for x,d in candidates:
            bb=clone(b);_,q,_,_=bb.splay(x,bb,'A')
            if q>4 or bb.code in seen:continue
            chosen=(x,bb.code);break
        if chosen is None:
            # One foreign actual access opens a different shallow frontier.
            # The helper's actual cost is always measured, including failures.
            x=rng.randrange(1,n+1);aa,_,_,_=a.splay(x,b,'A');body.append(['D',x]);A+=aa;Agap+=aa;emergency+=1
            if emergency>max(32,length//50):break
            continue
        x,bc=chosen;aa,_,_,_=a.splay(x,b,'A');_,q,G,_=b.splay(x,a,'B')
        assert b.code==bc and bc not in seen;seen.add(bc);novel+=1
        body.append(['K',x]);A+=aa;Q+=q;Agap+=aa
        guards+=G and q>2*Agap
        bodytargets.append(x);localstats.append((aa,q,Agap,G));Agap=0
    raw=periodic_cost(bodytargets,set(range(1,n+1)))
    wideL=sum((abs(x-bodytargets[i-1])*31).bit_length() for i,x in enumerate(bodytargets)) if bodytargets else 0
    source={'name':f'C02_adaptive_n{n}_seed{seed}','family':'adaptive_A_shallow_B_four_double_self_avoiding_body',
        'initial_A':diag,'initial_B':diag,'reaching_prefix':[],
        'operations':prefix+body+ops('K',range(1,n+1))+ops('K',range(n-1,0,-1)),
        'unclosed_active_word':prefix+body,'prefix_length':len(prefix),'seed':seed,
        'body_actual_A':A,'body_actual_Q_B':Q,'body_genuine_KEEP':novel,
        'body_hard_G_guards':guards,'body_raw_cyclic_rank_cost':raw,
        'body_predicted_full_domain_stride31_cost':raw['cyclic_blocks']+wideL,
        'body_no_complete_B_state_revisit':True,'emergency_actual_DELETE':emergency,
        'source_full_Pi_status':'not run: physical candidate screening only'}
    return source


if __name__=='__main__':
    meter=Meter('adaptive_return_free_walk_screen');sources=[];out=[]
    for n,seed in [(129,1),(129,2),(511,1),(511,2)]:
        s=make(n,seed);r=physical_replay(s);G=skeleton_cost(r,variant='G');H=skeleton_cost(r,variant='H')
        s.update(A=r['A'],Q_B=r['Q_B']);sources.append(s)
        row={k:v for k,v in s.items() if k not in ('initial_A','initial_B','operations','unclosed_active_word','reaching_prefix')}
        row.update(G={k:v for k,v in G.items() if k!='retained_original_operations'},
                   H={k:v for k,v in H.items() if k!='retained_original_operations'})
        out.append(row);write('ADAPTIVE_SOURCES.json',sources);write('ADAPTIVE_RESULTS.json',out)
        print(s['name'],'body A',s['body_actual_A'],'K',s['body_genuine_KEEP'],
            'Hguards',s['body_hard_G_guards'],'core cost',s['body_raw_cyclic_rank_cost']['B_cyclic'],
            'predicted wide',s['body_predicted_full_domain_stride31_cost'],
            'retained_H',H['retained_KEEP_count'],'period H cost',H['B_cyclic'],flush=True)
    meter.success=True;meter.details.update(new_small_original_sources=len(sources),
        qualification='Large-support escape not inferred from active prototypes or predicted domain costs')
