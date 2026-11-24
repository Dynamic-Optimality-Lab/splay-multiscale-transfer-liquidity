from base6 import *
from catalog5 import data
from cohortc import decode_state
from model0 import to_tuple
from exp01_oracle import Tree,Replay
from independent import splay as ind

def side_component(st,g,side):
    root=st['children'][str(g)][side];out=[];stack=[root] if root is not None else []
    while stack:
        k=stack.pop();l,r=st['children'][str(k)];out.append([k,l,r])
        if l is not None:stack.append(l)
        if r is not None:stack.append(r)
    return [root,sorted(out)]

def keys_component(st,g):
    stack=[g];out=set()
    while stack:
        k=stack.pop();out.add(k);stack.extend(x for x in st['children'][str(k)] if x is not None)
    return out

def edge(e,z,p,rows,ds):
    s=e['source'];u,v=tuple(z['earlier']),tuple(z['later']);g=z['old_g'];N=len(rows)
    span=list(range(u[0],v[0])) if u[0]<v[0] else list(range(u[0],N))+list(range(v[0]))
    initial=decode_state(p,rows[u[0]-1]['post_B_state']);sh=[Tree(initial),Tree(initial)]
    immutable=[to_tuple(initial),to_tuple(initial)];hits=[[],[]];matched=[[],[]];cost=Counter();last=[None,None]
    for pos in span:
        row=rows[pos]
        if row['tag']!='K':continue
        pre=decode_state(p,row['pre_B_state']);post=decode_state(p,row['post_B_state']);x=row['x']
        inside=x in keys_component(pre,g)
        assert x!=g or not inside # Such a hit would promote g; tested PF intervals exclude it.
        for side in (0,1):
            assert side_component(sh[side].state(),g,side)==side_component(pre,g,side)
            if inside and int(x>g)==side:
                if last[side] is not None:assert (x>last[side]) if side==0 else (x<last[side])
                last[side]=x;hits[side].append([row['t'],x])
                for w,d in ds.items():
                    if w[0]!=row['t'] or d['g']!=g:continue
                    path=sh[side].path(x);distance=len(path)-1-path.index(g)
                    assert distance==2*w[1] and path[-2*w[1]]==d['p']
                    matched[side].append(list(w))
                immutable[side],ev=ind.trace(immutable[side],x)
                Replay.plain_splay(sh[side],x);assert to_tuple(sh[side].state())==immutable[side]
                cost[side]+=sum(t[0]!='ZIG' for t in ev)
            assert side_component(sh[side].state(),g,side)==side_component(post,g,side)
    side=int(ds[v]['target']>g);assert list(v) in matched[side]
    return {'earlier':u,'later':v,'old_g':g,'operations_checked':len(span),
        'left_original_inside_hits':hits[0],'right_original_inside_hits':hits[1],
        'matched_original_g_doubles':matched,'shadow_Q':dict(cost),
        'active_side_full_child_pointer_equality':True,'independent_immutable_shadow_checks':True}

if __name__=='__main__':
    assert not (ROOT/'M1_CONT06_DELIVERY_MANIFEST.json').exists(),'Sealed stage.'
    mode=sys.argv[1] if len(sys.argv)>1 else 'all';assert mode in ('all','--historical-only','--fresh-only')
    m=Meter('one_sided_hit_shadow_'+mode.strip('-'));refs=load(C5/'ALL_CONTROL_REFERENCES_FINAL.json')
    old={z['source']:z for z in load(C5/'PHYSICAL_RENEWAL_RESULTS_FINAL.json')}
    out=load(ROOT/'ONE_SIDED_SHADOW_RESULTS.json') if mode=='--fresh-only' else []
    skipped=load(ROOT/'ONE_SIDED_SHADOW_SCOPE.json')['skipped_optional_long_expansions'] if mode=='--fresh-only' else []
    for e in (refs if mode!='--fresh-only' else []):
        selected=[z for z in old[e['source']['name']]['transition_examples'] if z['transition']=='promotion_free']
        if not selected:continue
        if e.get('expansion') or e.get('new_expansion'):
            skipped.append({'source':e['source']['name'],'reason':'Lossless large-source expansion remains sealed; optional shadow test not re-expanded.','stored_PF_examples':len(selected)});continue
        p,rows,events,ds,vs,gs,A=data(e);zs=[]
        for z in selected:zs.append(edge(e,z,p,rows,ds))
        out.append({'source':e['source']['name'],'source_sha256':digest(e['source']),'origin':e['origin'],'tested_stored_PF_intervals':zs})
        write('ONE_SIDED_SHADOW_RESULTS.json',out);gc.collect()
    for i,s in (enumerate(load(ROOT/'FRESH_SOURCE_CATALOG.json')) if mode!='--historical-only' else []):
        p=load(ROOT/f'FRESH_PHYS_{i:02}.json');ds={tuple(d['parent']):d for d in p['doubles']};zs=[]
        for z in load(ROOT/f'FRESH_NESTED_{i:02}.json'):
            if z['promotion_free']:zs.append(edge({'source':s},{'earlier':z['earlier_parent'],'later':z['later_parent'],'old_g':z['old_g']},p,p['boundaries'],ds))
        out.append({'source':s['name'],'source_sha256':digest(s),'origin':'C6_fresh','tested_canonical_original_C_old_intervals':zs})
        write('ONE_SIDED_SHADOW_RESULTS.json',out);gc.collect()
    write('ONE_SIDED_SHADOW_SCOPE.json',{'skipped_optional_long_expansions':skipped,'historical_input_complete_sources':len(refs),
        'tested_sources':len(out),'fresh_pending':mode=='--historical-only','intervals':sum(len(z.get('tested_stored_PF_intervals',z.get('tested_canonical_original_C_old_intervals',[]))) for z in out),
        'scope':'Every stored PF example of the sealed C5 physical audit except explicitly skipped long expansions, plus every fresh canonical C_old PF edge; NOT all historical PF transitions.'})
    m.info['tested_sources']=len(out);m.ok=True;print('PASS one-sided exact active-subtree and old-g matching',len(out),'sources',flush=True)
