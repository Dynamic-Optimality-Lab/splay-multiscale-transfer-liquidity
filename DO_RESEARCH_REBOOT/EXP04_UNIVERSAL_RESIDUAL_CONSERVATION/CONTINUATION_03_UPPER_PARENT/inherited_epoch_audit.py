from campaign3 import *
from bisect import bisect_right


def A_pivots(s):
    tree=Tree(s['initial_A']);pivots=defaultdict(list);A=0
    for h,(tag,x) in enumerate(s['operations'],1):
        j=0
        while tree.par[x] is not None:
            j+=1;p=tree.par[x];g=tree.par[p];side=int(x>p)
            if g is None:rs=[(p,side)]
            else:
                z=int(p>g);rs=[(g,z),(p,side)] if side==z else [(p,side),(g,z)]
            for b,(u,ss) in enumerate(rs):
                pivots[u].append((h,('A',h,j,b)));tree.rotate(u,ss)
        A+=j
    assert tree.state()==s['initial_A']
    return A,pivots


def select(s,demands):
    A,pivots=A_pivots(s);T=len(s['operations']);groups=defaultdict(list);zero=[]
    byparent=defaultdict(list)
    for e in demands:byparent[tuple(e['original_parent'])].append(e)
    for parent,ds in byparent.items():
        h,j=parent;g=ds[0]['old_g'];bits=pivots[g]
        if not bits:zero+=ds;continue
        i=bisect_right([t for t,bit in bits],h)-1
        start,bit=bits[i];lift=h if h>=start else h+T
        groups[bit].append((lift,parent,ds))
    selected=[];repeats=[];packets=[]
    for bit,ps in groups.items():
        ps.sort();selected+=ps[0][2]
        repeats.extend(e for _,_,ds in ps[1:] for e in ds)
        packets.append({'actual_A_demotion_bit':bit,'first_parent':ps[0][1],
                        'later_parents':[p for _,p,ds in ps[1:]],'parent_count':len(ps)})
    assert len(selected)+len(repeats)+len(zero)==len(demands) and len(selected)<=6*A
    return {'A':A,'selected_original_gaps':selected,'repeated_original_gaps':repeats,
            'no_A_pivot_key_original_gaps':zero,'packets':packets}


if __name__=='__main__':
    meter=Meter('inherited_epochs')
    archive=json.loads((PARENT/'EXP04_SOURCE_WITNESSES.json').read_text())
    sources={s['name']:s for s in archive['inherited_sources']+archive['new_sources']}
    controls=json.loads((C2/'INHERITED_LOCAL_PAYMENT_AUDIT.json').read_text())['sources'];out=[]
    for row in controls:
        s=sources[row['source']]
        for pool in ('original_R_star','nonprefix_original_R_star'):
            demands=row['original_events'] if pool=='original_R_star' else [e for e in row['original_events'] if not e['prefix_paid']]
            z=select(s,demands);assert z['A']==row['A']
            out.append({'source':row['source'],'pool':pool,**z})
    write('INHERITED_EPOCH_RESULTS.json',{'records':out,'scope':'Pinned original R_star membership; fresh actual A pivot replay. Carrier/skipped exclusions are not used in these broader diagnostic pools.',
        'source_uniform_exhaustiveness_inferred':False})
    print('PASS',len(controls),'source scopes;',sum(len(z['repeated_original_gaps']) for z in out if z['pool']=='nonprefix_original_R_star'),
          'nonprefix repeat gaps;',sum(len(z['no_A_pivot_key_original_gaps']) for z in out if z['pool']=='nonprefix_original_R_star'),'nonprefix no-pivot gaps',flush=True)
    meter.success=True
