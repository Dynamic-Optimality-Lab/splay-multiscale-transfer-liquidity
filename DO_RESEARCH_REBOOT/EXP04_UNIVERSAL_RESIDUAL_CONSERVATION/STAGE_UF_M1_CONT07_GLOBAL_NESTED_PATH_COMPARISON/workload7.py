from base7 import *
from catalog7 import known_inputs,accounting
from cohortc import decode_state
from physical1 import Edges
from exp01_oracle import Tree,Replay
from model0 import to_tuple
from independent import splay as ind

def span(u,v,N):
    return list(range(u[0],v[0])) if u[0]<v[0] else list(range(u[0],N))+list(range(v[0]))

def full_component(st,g):return Edges(st).component(g)

def canonical_edges(s,p,acc):
    ds={tuple(d['parent']):d for d in p['doubles']};groups=defaultdict(list);cols=defaultdict(list)
    for e in acc['C_old']:groups[tuple(e['original_parent'])].append(e)
    for v in sorted(groups):cols[ds[v]['g']].append(v)
    E={digest(z['rho']) for z in acc['E_old']};out=[];T=len(p['events'])
    for g,vs in cols.items():
        for i,v in enumerate(vs):
            selected=[digest(z['rho']) in E for z in groups[v]];assert all(selected) or not any(selected)
            if all(selected):continue
            u=vs[i-1];lo=p['boundaries'][u[0]-1]['end_time'];hi=p['boundaries'][v[0]-1]['post_A_time']
            ts=list(range(lo,hi)) if u[0]<v[0] else list(range(lo,T))+list(range(hi))
            events=[p['events'][t] for t in ts];assert not any(e['actor']=='A' and (e['pivot']==g or e['promoted']==g) for e in events)
            promos=[e for e in events if e['actor']=='B' and e['promoted']==g]
            out.append({'u':u,'v':v,'old_g':g,'PF':not promos,'mediating_promotions':[e['id'] for e in promos],
                'original_C_old_rhos':groups[v],'A_reset_epoch_exists':any(e['actor']=='A' and e['pivot']==g for e in p['events'])})
    return out

def paths_from_edges(edges):
    free=[z for z in edges if z['PF']];nxt={tuple(z['u']):tuple(z['v']) for z in free};assert len(nxt)==len(free)
    prevs={tuple(z['v']):tuple(z['u']) for z in free};assert len(prevs)==len(free)
    heads=sorted(set(nxt)-set(prevs));out=[];used=set()
    for u in heads:
        path=[u]
        while path[-1] in nxt:
            v=nxt[path[-1]];assert v not in path;used.add((path[-1],v));path.append(v)
        out.append(path)
    assert len(used)==len(free),'Forbidden all-PF cycle or missing edge'
    return out

def merged_replay(p,rows,ds,u,v,g,hits):
    initial=decode_state(p,rows[u[0]-1]['post_B_state']);shadow=Tree(initial);immutable=to_tuple(initial)
    failures=[];matches=[];Q=0;traces=[]
    for h,x in hits:
        pre=shadow.state();actual_pre=decode_state(p,rows[h-1]['pre_B_state']);actual_post=decode_state(p,rows[h-1]['post_B_state'])
        equal_before=full_component(pre,g)==full_component(actual_pre,g);path=shadow.path(x)
        original=next((w for w,d in ds.items() if w[0]==h and d['g']==g),None)
        if original is not None:
            distance=len(path)-1-path.index(g) if g in path else None
            match=distance is not None and distance>=2 and distance%2==0
            matches.append({'original_parent':original,'matched_old_g':match,'shadow_double_j':distance//2 if match else None})
        immutable,ev=ind.trace(immutable,x);Replay.plain_splay(shadow,x);post=shadow.state();assert to_tuple(post)==immutable
        q=sum(e[0]!='ZIG' for e in ev);Q+=q
        equal_after=full_component(post,g)==full_component(actual_post,g)
        traces.append({'operation':h,'target':x,'shadow_pre_sha256':digest(pre),'shadow_post_sha256':digest(post),'q':q,'full_g_equal_before':equal_before,'full_g_equal_after':equal_after})
        if (not equal_before or not equal_after) and not failures:
            failures.append({'operation':h,'target':x,'original_inside_parent_double':[d for w,d in ds.items() if w[0]==h and d['p']==g],
                'shadow_pre_path':path,'original_pre_path':rows[h-1]['B_path'],
                'actual_pre_B':actual_pre,'actual_post_B':actual_post,'shadow_pre_B':pre,'shadow_post_B':post,
                'full_g_equal_before':equal_before,'full_g_equal_after':equal_after})
    return {'retained_inside_hits':hits,'shadow_Q':Q,'traces':traces,'original_old_g_matches':matches,
        'full_g_component_failure':failures,'all_original_old_g_matched':all(z['matched_old_g'] for z in matches)}

def path_workload(s,p,path,verify_sides=True):
    rows=p['boundaries'];N=len(rows);u,v=path[0],path[-1];ds={tuple(d['parent']):d for d in p['doubles']};g=ds[u]['g']
    assert all(ds[w]['g']==g for w in path);initial_sid=rows[u[0]-1]['post_B_state'];initial=decode_state(p,initial_sid);tree=Edges(initial)
    stem=tree.path(g);component_keys=tree.m[g];sides=[[],[]];hits=[];all_ids=[]
    for pos in span(u,v,N):
        row=rows[pos]
        if row['tag']!='K':continue
        pre=Edges(decode_state(p,row['pre_B_state']));x=row['x']
        if pre.m[g]&(1<<(x-1)):
            assert x!=g;sides[int(x>g)].append([row['t'],x]);hits.append([row['t'],x])
            ids=[e['id'] for e in p['events'][row['post_A_time']:row['end_time']] if e['pivot']==g]
            assert len(ids)==1;all_ids+=ids
        assert not any(e['actor']=='B' and e['promoted']==g for e in p['events'][row['post_A_time']:row['end_time']])
    domains=[];interiors=[];local_domains=[];matched=[];Q=[];original_side_states=[]
    for side,hs in enumerate(sides):
        xs=[x for h,x in hs];assert xs==sorted(set(xs),reverse=bool(side))
        J=set()
        for x in xs:J.update(tree.path(x))
        if not xs:domains.append([]);interiors.append([]);local_domains.append([]);Q.append(0);matched.append([]);continue
        assert set(stem)<=J;I=J-set(stem);assert I<=set(k for k in range(1,tree.n+1) if component_keys&(1<<(k-1)))
        domains.append(sorted(J));interiors.append(sorted(I));local_domains.append(sorted(I|{g}))
        shadow=Tree(initial);immutable=to_tuple(initial);qtotal=0;ms=[]
        for h,x in hs:
            pre=shadow.state();path_shadow=shadow.path(x)
            original=next((w for w,d in ds.items() if w[0]==h and d['g']==g),None)
            if original is not None:
                distance=len(path_shadow)-1-path_shadow.index(g);assert distance==2*original[1]
                ms.append(list(original))
            immutable,ev=ind.trace(immutable,x);Replay.plain_splay(shadow,x);assert to_tuple(shadow.state())==immutable
            qtotal+=sum(e[0]!='ZIG' for e in ev)
        Q.append(qtotal);matched.append(ms)
    nonempty=sum(bool(x) for x in sides);M=sum(map(len,domains));Mint=sum(map(len,interiors));Mstem=nonempty*len(stem);Mhit=len(hits)
    assert M==Mint+Mstem and Mint>=Mhit
    merged=merged_replay(p,rows,ds,u,v,g,hits)
    later=list(path[1:])
    for w in later:assert list(w) in matched[int(ds[w]['target']>g)]
    return {'path':path,'old_g':g,'original_initial_B_state':initial_sid,'original_initial_B_sha256':digest(initial),
        'root_to_g_stem':stem,'left_inside_hits':sides[0],'right_inside_hits':sides[1],
        'full_initial_domains':domains,'inside_domain_parts':interiors,'component_rooted_domains':local_domains,
        'M_PF':M,'M_stem':Mstem,'M_inside':Mint,'M_hit':Mhit,'M_support_padding':Mint-Mhit,
        'component_rooted_workload':Mint+nonempty,'matched_original_doubles':matched,'Q_two_sided_separate':Q,
        'unique_original_inside_pivot_bits':all_ids,'merged_inside_shadow':merged,
        'scope':'Maximal ORIGINAL C_old PF path before H/quota. Comparison costs are not source A credit.'}

if __name__=='__main__':
    unsealed();m=Meter('exact_inherited_path_workloads');entries=known_inputs();out=[]
    summaries={z['source_sha256']:z for z in load(C5/'PHYSICAL_RENEWAL_RESULTS_FINAL.json')}
    summaries.update({digest(s):load(C6/f'FRESH_RESULT_{i:02}.json') for i,s in enumerate(load(C6/'FRESH_SOURCE_CATALOG.json'))})
    expected={z['source_sha256']:z for z in load(C5/'CANONICAL_REDUCTION_INVENTORY.json')['source_records']}
    expected.update({digest(s):load(C6/f'FRESH_RENEWAL_{i:02}.json') for i,s in enumerate(load(C6/'FRESH_SOURCE_CATALOG.json'))})
    for i,e in enumerate(entries):
        s=e['source'];acc=accounting(e);meta=summaries[digest(s)];A=meta['A'];edges=[];paths=[];details=[]
        if acc['C_old']:
            p=load(e['physical']);assert digest(s)==p['source_sha256'];edges=canonical_edges(s,p,acc)
            assert {(tuple(z['u']),tuple(z['v'])) for z in edges}=={(tuple(z['earlier_parent']),tuple(z['later_parent'])) for z in expected[digest(s)]['canonical_renewals']}
            paths=paths_from_edges(edges);details=[path_workload(s,p,path) for path in paths];del p
        assert len(edges)==expected[digest(s)]['canonical_renewals_count']
        row={'source':s['name'],'source_sha256':digest(s),'origin':e['origin'],'A':A,'Q_B':meta['Q_B'],'physical':e['physical'],
            'C_old_gaps':len(acc['C_old']),'E_old_gaps':len(acc['E_old']),'canonical_edges':edges,'maximal_PF_paths':details,
            'M_PF':sum(z['M_PF'] for z in details),'M_stem':sum(z['M_stem'] for z in details),'M_inside':sum(z['M_inside'] for z in details),
            'merged_component_failures':sum(bool(z['merged_inside_shadow']['full_g_component_failure']) for z in details),
            'actual_S_PF':[],'actual_S_PM':[],'actual_residual_scope':'Inherited positive periodic/cheap quota exclusion, not inferred from path counts.'}
        out.append(row);write('INHERITED_PATH_WORKLOADS.json',out);gc.collect()
        print('PASS workload',i,s['name'],'paths',len(paths),'M',row['M_PF'],'A',A,'merge failures',row['merged_component_failures'],flush=True)
    write('EXACT_ACCOUNTING_INPUTS.json',entries);m.info.update(complete_original_accounting_sources=len(out));m.ok=True
