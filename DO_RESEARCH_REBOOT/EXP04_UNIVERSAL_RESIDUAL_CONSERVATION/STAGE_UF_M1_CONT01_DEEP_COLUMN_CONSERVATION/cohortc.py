"""Full original cohort and first-edge classification on independent U data."""
from basec import *
from physical1 import Edges

def decode_state(phys,sid):
    n=phys['state_pool']['n'];w=(n+1).bit_length();mask=(1<<w)-1
    z=int(phys['state_pool']['states'][sid],16)
    return {'root':z>>(2*n*w),'children':{str(k):[
        (z>>((2*k-2)*w))&mask or None,(z>>((2*k-1)*w))&mask or None] for k in range(1,n+1)}}

def scans(s,phys,domain,isolated=False):
    if len(domain)<2:return set()
    keeps=[(i+1,x) for i,(tag,x) in enumerate(s['operations']) if tag=='K']
    cut=next((i for i in range(len(keeps)) if keeps[i][1]!=keeps[i-1][1]),None)
    if cut is None:return set()
    keeps=keeps[cut:]+keeps[:cut];blocks=[]
    for h,x in keeps:
        if not blocks or blocks[-1]['x']!=x:blocks.append({'x':x,'ts':[]})
        blocks[-1]['ts'].append(h)
    ranks={x:i for i,x in enumerate(sorted(domain))};accepted=set()
    for i,bl in enumerate(blocks):
        for direction in (1,-1):
            anchor=min(domain) if direction==1 else max(domain)
            if bl['x']!=anchor:continue
            run=[bl];rank=ranks[anchor]
            for k in range(1,len(blocks)):
                nxt=blocks[(i+k)%len(blocks)]
                if nxt['x'] not in ranks or ranks[nxt['x']]!=rank+direction:break
                rank+=direction;run.append(nxt)
            ok=len(run)>=(len(domain)+1)//2+1
            if ok and isolated:
                row=phys['boundaries'][bl['ts'][0]-1]
                b=Edges(decode_state(phys,row['pre_B_state']))
                hull=set().union(*(b.path(x) for x in domain));ok=hull==set(domain)
            if ok:accepted.update(h for z in run for h in z['ts'])
    return accepted

def classify(s,phys,U,presence):
    ds={tuple(z['parent']):z for z in phys['doubles']};core=sum(1<<(k-1) for k in phys['original_S'])
    b0=Edges(s['initial_B']);I={k for k in phys['original_S'] if (b0.m[k]&core)&~(1<<(k-1))}
    es=scans(s,phys,set(phys['original_S']));ei=scans(s,phys,I,True)
    cohorts=defaultdict(list)
    for p,z in U.items():cohorts[z['h']].append(p)
    pairs=[];states={}
    for h,ps in sorted(cohorts.items()):
        ps.sort(key=lambda p:ds[p]['J'].bit_count())
        if len(ps)<2:continue
        row=phys['boundaries'][h-1];b=Edges(decode_state(phys,row['pre_B_state']))
        for inner,outer in zip(ps,ps[1:]):
            a,z=ds[inner],ds[outer];assert a['J']!=z['J'] and a['J']&~z['J']==0
            path=[a['g']]
            while path[-1]!=z['g']:path.append(b.p[path[-1]]);assert path[-1]
            path.reverse();edges={(u,v,int(v>u)) for u,v in zip(path,path[1:])}
            beta=next(e for e in phys['events'][row['post_A_time']:row['end_time']]
                if edges.intersection(map(tuple,e['deleted'])))
            p=tuple(beta['id'][1:3]);lo=z['events'][0 if z['case'] in ('LL','RR') else 1];hi=U[outer]['hit_time']
            sep=any(presence.any(b.m[k]&core,lo,hi) for k in path[1:-1])
            if U[inner]['exposed'] or U[outer]['exposed']:kind='E_ctl'
            elif sep:kind='R_sep'
            elif beta['sign']==-1:kind='R_dec'
            elif ds[p]['signs']!=[0,0]:kind='R_mix'
            elif p not in U:kind='R_out'
            elif len(cohorts[U[p]['h']])==1:kind='T'
            elif h in es:kind='R_scan'
            elif h in ei:kind='R_fringe'
            else:kind='R6'
            pairs.append({'rho':[h,list(inner),list(outer)],'class':kind,'path':path,
                'intermediate_labels':[[k for k in phys['original_S'] if b.m[v]&(1<<(k-1))] for v in path[1:-1]],
                'beta':beta['id'],'parent':list(p),'beta_sign':beta['sign'],'path_edges':sorted(edges)})
    assert len(pairs)==sum(len(v)-1 for v in cohorts.values())
    counts=Counter(z['class'] for z in pairs)
    return {'original_cohorts':{str(h):v for h,v in sorted(cohorts.items())},'original_pairs':pairs,
        'original_class_counts':dict(counts),'original_R6':[z for z in pairs if z['class']=='R6'],
        'eligible_S_operations':sorted(es),'eligible_I_operations':sorted(ei),'original_I':sorted(I)}
