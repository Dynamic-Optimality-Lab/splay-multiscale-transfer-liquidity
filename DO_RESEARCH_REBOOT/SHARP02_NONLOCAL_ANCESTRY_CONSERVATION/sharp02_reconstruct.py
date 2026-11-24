"""Reproduce all inherited sources and exact all-recreation graphs, read-only."""
from sharp02_common import *
from sharp02_graph import graph_data,solve
from sharp01_validate import validate

with Run('stage0_reconstruction_v001',limit=180) as run:
    idx=read(OLD/'SHARP01_GAP_LEDGER.json')['ledgers'];saved=read(OLD/'SHARP01_PHYSICAL_INCIDENCE.json')['sources']
    episodes=read(OLD/'SHARP01_ANCESTOR_EPISODES.json')
    witnesses=read(OLD/'SHARP01_SOURCE_WITNESSES.json')['sources'];results=[];ops=0
    for num,(item,src,oldgraph) in enumerate(zip(idx,witnesses,saved)):
        assert item['name']==src['name']==oldgraph['source'] and sha(OLD/item['path'])==item['sha256']
        l=read(OLD/item['path']);ops+=validate(src,l);data=graph_data(l)
        result=solve(data['weights'],data['adj'],data['free'])
        assert result['unmatched']==0
        assert result['flow']==oldgraph['rules']['unit_A_recreation']['flow']
        old_units=oldgraph['units']
        # Resource indexes differ because SHARP-02 also names reserved units.
        old_ids={tuple(u['id']) for u in old_units.values()}
        if data['weights']:assert old_ids=={tuple(u['id']) for u in data['free'].values()}
        models={}
        for mode,(ww,aa) in data['token_models'].items():models[mode]=solve(ww,aa,data['free'],tight=False)
        row={'name':src['name'],'summary':l['summary'],'broad':result,'token_models':models}
        if src['name'].startswith('C15_'):
            byid={tuple(u['id']):j for j,u in data['free'].items()}
            firstold=oldgraph['rules']['unit_first_A_recreation']
            firstadj={i:{byid[tuple(old_units[str(j)]['id'])] for j in js} for i,js in firstold['edges'].items()}
            rr=solve(data['weights'],firstadj,data['free'])
            assert rr['flow']==firstold['flow'] and rr['unmatched']==firstold['demand']-firstold['flow']
            row['first_recreation_reproduction']=rr
        results.append(row)
        if num%10==0:
            write(BASE/'SHARP02_RECONSTRUCTION.checkpoint.json',{'rows':results,'operations_verified':ops})
            run.check(sources_verified=num+1,operations_verified=ops)
    write(BASE/'SHARP02_RECONSTRUCTION.json',{'sources':results,'operations_verified':ops,'episode_source_count':len(episodes['sources']),
        'level':'same agent; byte-pinned pointer ledger versus separate immutable operation replay and newly implemented grouped integral flows'})
    run.check(sources_verified=len(results),operations_verified=ops)
    print(json.dumps({'sources':len(results),'operations':ops,'broad_failures':sum(z['broad']['unmatched']>0 for z in results),
         'token_failures':{mode:sum(z['token_models'][mode]['unmatched']>0 for z in results) for mode in ('outermost','innermost','extra_double')}}))
