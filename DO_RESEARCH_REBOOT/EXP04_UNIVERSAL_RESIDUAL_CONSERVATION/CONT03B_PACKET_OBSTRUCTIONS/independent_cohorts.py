from campaign3b import *
from independent_Pi3 import data


def presence_masks(r):
    aset,_,_=data(r.as_tuple(Tree(r.source['initial_A'])),r.bits)
    opened={lab:0 for lab in aset};masks=defaultdict(int)
    for ev in r.events:
        if ev['actor']!='A':continue
        t=ev['time']
        for lab in ev['lost']:
            lo=opened.pop(lab);masks[lab]|=((1<<(t-lo))-1)<<lo
        for lab in ev['created']:assert lab not in opened;opened[lab]=t
    for lab,lo in opened.items():masks[lab]|=((1<<(r.T-lo))-1)<<lo
    def any_A(lab,lo,hi):
        assert 0<=hi-lo<=r.T
        bits=masks[lab];doubled=bits|(bits<<r.T)
        return bool((doubled>>(lo%r.T))&((1<<(hi-lo+1))-1))
    return any_A


def eligible(r,domain):
    domain=set(domain)
    if len(domain)<2:return set()
    keeps=[(h,x) for h,(tag,x) in enumerate(r.ops,1) if tag=='K']
    cut=next((k for k,(h,x) in enumerate(keeps) if x!=keeps[k-1][1]),None)
    if cut is None:return set()
    ordered=keeps[cut:]+keeps[:cut];blocks=[]
    for h,x in ordered:
        if not blocks or blocks[-1][0]!=x:blocks.append((x,[]))
        blocks[-1][1].append(h)
    ranked={x:i for i,x in enumerate(sorted(domain))};out=set();L=len(blocks)
    for start,(x,hs) in enumerate(blocks):
        for direction,anchor in ((1,min(domain)),(-1,max(domain))):
            if x!=anchor:continue
            run=[start];rank=ranked[x]
            for k in range(1,L):
                nxt=(start+k)%L;y=blocks[nxt][0]
                if y not in ranked or ranked[y]!=rank+direction:break
                run.append(nxt);rank+=direction
            if len(run)<(len(domain)+1)//2+1:continue
            st=r.as_tuple(Tree(r.boundaries[hs[0]-1]['pre_B']));_,edges,_=data(st,r.bits)
            par={v:u for u,v,side in edges}
            if domain!=r.S and any(par.get(v) is not None and par[v] not in domain for v in domain):continue
            out.update(h for k in run for h in blocks[k][1])
    return out


def verify(r):
    any_A=presence_masks(r);groups=defaultdict(list)
    for key,d in r.U.items():groups[d['h']].append(key)
    for h,ks in groups.items():
        ks.sort(key=lambda k:r.U[k]['J'].bit_count())
        for a,b in zip(ks,ks[1:]):assert r.U[a]['J']!=r.U[b]['J'] and r.U[a]['J']&r.U[b]['J']==r.U[a]['J']
    _,_,initial_labs=data(r.as_tuple(Tree(r.source['initial_B'])),r.bits)
    I={k for k,v in initial_labs.items() if k in r.S and v&~r.bits[k]}
    assert I==r.I
    S_paid=eligible(r,r.S);I_paid=eligible(r,I)
    assert S_paid==r.eligible_S and I_paid==r.eligible_I
    out=[]
    for h,ks in groups.items():
        st=r.as_tuple(Tree(r.boundaries[h-1]['pre_B']));_,edges,labs=data(st,r.bits);par={v:u for u,v,side in edges}
        for left,right in zip(ks,ks[1:]):
            aa,bb=r.U[left],r.U[right];path=[aa['g']]
            while path[-1]!=bb['g']:path.append(par[path[-1]])
            path.reverse();pedges={(u,v,int(v>u)) for u,v in zip(path,path[1:])}
            row=r.boundaries[h-1]
            beta=next(ev for ev in r.events[row['post_A_time']:row['end_time']] if pedges.intersection(map(tuple,ev['deleted'])))
            parent=tuple(beta['id'][1:3]);pd=r.doubles[parent]
            sep=any(any_A(labs[k],bb['nu'],bb['hit_time']) for k in path[1:-1])
            if aa['exposed'] or bb['exposed']:cls='E_ctl'
            elif sep:cls='R_sep'
            elif beta['sign']==-1:cls='R_dec'
            elif pd['signs']!=[0,0]:cls='R_mix'
            elif parent not in r.U:cls='R_out'
            elif len(groups[r.U[parent]['h']])==1:cls='T'
            elif h in S_paid:cls='R_scan'
            elif h in I_paid:cls='R_fringe'
            else:cls='R6'
            out.append({'rho':[h,list(left),list(right)],'parent':list(parent),'class':cls,'beta':beta['id'],
                'path':path,'beta_sign':beta['sign'],'path_edges':sorted(pedges),
                'intermediate_labels':[r.label_keys(labs[k]) for k in path[1:-1]]})
    actual={digest(p['rho']):p for p in r.pairs};assert len(out)==len(actual)
    for p in out:
        original=actual[digest(p['rho'])]
        assert all(p[k]==original[k] for k in p),(p,original)
    return {'independently_recomputed_all_original_pairs':out,'cohort_count':len(groups),
        'independent_S_and_I_scan_eligibility_matches':True,
        'scope':'Uses independently primitive-verified U/frame fields; independently rebuilds cohort adjacency, first physical edge deletion, separator exposure, renewal and R6 classes. Higher EXP02/03/04 paid-class selectors remain pinned.'}
