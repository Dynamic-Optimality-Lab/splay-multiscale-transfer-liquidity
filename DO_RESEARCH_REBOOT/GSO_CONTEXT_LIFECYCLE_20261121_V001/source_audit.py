"""Complete original-source audit of context lifecycles and literal old U IDs."""
import json
from collections import Counter
import context as C
K=C.K


def encoded(state,keys):
    rank={x:i+1 for i,x in enumerate(keys)};rank[None]=0
    return tuple([rank[state['root']]]+[rank[x] for k in keys for x in state['children'][str(k)]])


def core_measure(a,b):return max(C.size(C.reduce_pair(a,b))-1,0)


def audit(source,selected=None):
    original=K.OLD.replay(source)
    keys=sorted(map(int,source['initial_A']['children']));rank={x:i+1 for i,x in enumerate(keys)}
    a=encoded(source['initial_A'],keys);b=encoded(source['initial_B'],keys);start=(a,b)
    demand_ids={tuple(d['id']) for d in original['demands']};demand_ops={i[0] for i in demand_ids}
    interesting=set(selected or [])|demand_ops
    rows=[];allrows=[];maxcore=0;A=Q=0;u_within5=[];extra=[];gap=0;keep_gaps={}
    for op,(mode,key) in enumerate(source['operations'],1):
        x=rank[key];before=C.size(C.reduce_pair(a,b));pre_roots_differ=a[0]!=b[0]
        aa,da=K.original_splay(a,x);mid=C.size(C.reduce_pair(aa,b))
        if mode=='K':bb,db=K.original_splay(b,x)
        else:bb,db=b,0
        after=C.size(C.reduce_pair(aa,bb));cost=(da+1)//2;q=db//2;A+=cost;Q+=q;gap+=cost
        assert max(mid-1,0)-max(before-1,0)<=da
        if mode=='K':assert after<=mid
        row={'op':op,'mode':mode,'target':key,'a':cost,'q':q,'A_depth':da,'B_depth':db,'before_core':before,'post_A_core':mid,'after_core':after,'kappa_before':max(before-1,0),'kappa_post_A':max(mid-1,0),'kappa_after':max(after-1,0),'pre_roots_differ':pre_roots_differ}
        allrows.append(row);maxcore=max(maxcore,before,after)
        if op in interesting:rows.append(row)
        if mode=='K':keep_gaps[op]=gap;gap=0
        a,b=aa,bb
    # The incoming original KEEP gaps are cyclic; the suffix belongs to the
    # first KEEP, not to a free reaching prefix.
    first=next((op for op,(mode,_) in enumerate(source['operations'],1) if mode=='K'),None)
    if first is not None:keep_gaps[first]+=gap
    assert (a,b)==start and A==original['A'] and Q==original['Q_B']
    lookup={r['op']:r for r in allrows}
    for d in original['demands']:
        r=lookup[d['id'][0]]
        if r['before_core']<=5:u_within5.append(d['id'])
        if d['id'][1]>keep_gaps[d['id'][0]]:extra.append({'id':d['id'],'before_core':r['before_core'],'after_core':r['after_core'],'gap_A':keep_gaps[d['id'][0]]})
    # Inspect the actual original B bits at the interesting occurrences.
    trees={actor:K.OLD.Tree(source['initial_'+actor],original['S']) for actor in ('A','B')};bits=[]
    for op,(mode,x) in enumerate(source['operations'],1):
        K.OLD.plain(trees['A'],x)
        if mode!='K':continue
        tree=trees['B'];step=0
        while tree.parent[x] is not None:
            p=tree.parent[x];g=tree.parent[p];step+=1
            pivots=[x] if g is None else [p,x] if (p<g)==(x<p) else [x,x]
            for bit,y in enumerate(pivots):
                inspect=op in interesting
                if inspect:old=core_measure(encoded(trees['A'].state(),keys),encoded(tree.state(),keys))
                event=tree.rotate(y)
                if inspect:
                    new=core_measure(encoded(trees['A'].state(),keys),encoded(tree.state(),keys))
                    neutral=not any(trees['A'].counts[z]>0 for z in event['born'])
                    assert new<=old
                    if neutral:assert new==old,('neutral core-change conjecture failed',source['name'],op,step,bit,old,new)
                    bits.append({'id':['B',op,step,bit],'promoted':event['p'],'demoted':event['g'],'born_labels':event['born'],'neutral':neutral,'kappa_before':old,'kappa_after':new,'original_U':(op,step) in demand_ids})
    assert all(trees[actor].state()==source['initial_'+actor] for actor in ('A','B'))
    return {'source':source,'A':A,'Q_B':Q,'original_S':original['S'],'original_U':original['demands'],'operations':len(allrows),'rows':rows,'selected_B_bits':bits,'maximum_boundary_core':maxcore,'U_pre_core5':u_within5,'U_beyond_direct_A_gap_prefix':extra,'core5_beyond_direct_prefix':[x for x in extra if x['before_core']<=5],'entire_source_boundary_core5':maxcore<=5,'all_phase_measure_bounds_checked':True,'full_pair_closure':True,'prefix_checked_by_original_replayer':True}


def population():
    result=[]
    for n in (3,4,5,6):result.append((K.load(C.PREVIOUS/'run_001'/f'optimum_cycle_n{n}.json')['source'],None))
    for i in range(3):
        ref=K.load(C.PREVIOUS/'run_001'/f'flow_case_{i}.json')['ref'];result.append((K.SOURCES.canonical(ref),None))
    for q in (1,3,7,17):
        s=K.PARAM.H(3,q);n=len(s['initial_A']['children']);result.append((s,{n+7}))
    return result


def main():
    out=C.HERE/'sources_001';out.mkdir(exist_ok=False);summary=[]
    for i,(s,selected) in enumerate(population()):
        z=audit(s,selected);filename=f'source_{i:02d}.json.gz';C.write(out/filename,z)
        row={'file':filename,'name':s['name'],'keys':len(s['initial_A']['children']),'ops':z['operations'],'A':z['A'],'Q_B':z['Q_B'],'U':len(z['original_U']),'maximum_core':z['maximum_boundary_core'],'U_pre_core5':len(z['U_pre_core5']),'U_beyond_prefix':len(z['U_beyond_direct_A_gap_prefix']),'U_core5_beyond_prefix':len(z['core5_beyond_direct_prefix'])}
        summary.append(row);print(json.dumps(row),flush=True)
    C.write(out/'SUMMARY.json',{'cases':summary,'scope':'Complete original periods and literal original U/Pi, with selected actual bit core measurements. No finite count is a universal coverage proof.'})


if __name__=='__main__':main()
