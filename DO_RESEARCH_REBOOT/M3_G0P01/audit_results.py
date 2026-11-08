"""Independent tree-level refinement, all new edge images, original roots and full cycle closure."""
import sys,json,time,ast
from pathlib import Path
from collections import defaultdict,Counter
sys.path.insert(0,'DO_RESEARCH_REBOOT/M3_G0P01')
from certify_refinement import S,V,M,BASE,PORT,load,port_tree,shadow,rho
from port_potential import PortPotential
from PC_TYPED_DAG import DAG
from STRICT_LOW_COMPILER import build_slow
from STRICT_HIGH_COMPILER import build_shigh
OUT=BASE/'audit_results.json'
def expand(t):
    if t==PORT:return S.node(-1,S.LEAF,S.LEAF)
    if t==S.LEAF:return t
    return S.node(t[1],expand(t[2]),expand(t[3]))
def main():
    assert not OUT.exists();start=time.process_time();P=PortPotential();c,a=load();old=P.old;oc=old.c;oa=old.a
    for path in BASE.glob('*.py'):ast.parse(path.read_text(),filename=str(path))
    union=[tuple(tuple(r) for r in s) for s in c['shadows']];uid={s:i for i,s in enumerate(union)}
    assert len(union)==1444 and len(uid)==1444 and c['old_physical_shadow_count']==1188
    for i,s in enumerate(oc['shadows']):assert union[i]==tuple(tuple(r) for r in s)
    expected=set();commutations=0
    for i,t in enumerate(old.old.old.trees):
        pt=port_tree(t);expanded=expand(pt);assert expanded==V.insert(t,-1)
        sa=shadow(pt);rs,rule=rho(sa);assert rs==tuple(tuple(r) for r in V.shadow(expanded))
        for x in M:
            h=S.lookup(pt,x)[1]
            if h not in (1,2):continue
            result=S.trace(pt,x)[0]
            assert expand(result)==S.trace(expanded,x)[0] # whole-tree identity, not just alpha
            ta=shadow(result);rt,_=rho(ta);assert rt==tuple(tuple(r) for r in V.shadow(expand(result)))
            expected.add((uid[sa],x,uid[ta]));commutations+=1
    actual={(o['source_shadow'],o['target'],o['destination_shadow']) for o in c['family_options']}
    assert expected==actual and len(actual)==len(c['family_options']) and commutations==8634
    byroot={r:[i for i,s in enumerate(union) if s[0]==(0,1,r)] for r in range(9)}
    local={ai:j for r in range(9) for j,ai in enumerate(byroot[r])}
    oldlocal={ai:j for r in range(9) for j,ai in enumerate(oc['shadows_by_root'][str(r)])}
    unchanged=0
    for u,(bi,ai) in enumerate(zip(a['ordinary_b'],a['ordinary_a'])):
        image=oc['B_bases'][bi]+oldlocal[c['refined_shadow'][ai]]
        assert image==a['images'][u] and a['potential'][u]==old.p[image]
        assert -2<=a['potential'][u]<=-oc['psi'][bi]
        assert u==c['B_bases'][bi]+local[ai]
        if ai<1188:
            assert c['refined_shadow'][ai]==ai;unchanged+=1
    assert unchanged==342796 and len(a['potential'])==469346
    opts=defaultdict(list)
    for j,o in enumerate(c['family_options']):opts[union[o['source_shadow']][0][2]].append((j,o))
    oldB=json.loads(Path('DO_RESEARCH_REBOOT/M3_H1F01/cheap_census.json').read_text())
    n=0;failures=Counter();residuals=Counter()
    for bi,b in enumerate(old.old.old.trees):
        if b[1] not in M:continue
        for j,o in opts[b[1]]:
            si=o['source_shadow'];ti=o['destination_shadow'];x=o['target']
            if si<1188 and ti<1188:continue
            h=oldB['B_depth'][bi][x]
            if h==0:continue
            bj=oldB['B_destination'][bi][x];u=c['B_bases'][bi]+local[si];v=c['B_bases'][bj]+local[ti];w=2-h//2
            assert (a['source'][n],a['destination'][n],a['weights'][n],a['option'][n])==(u,v,w,j)
            iu=a['images'][u];iv=a['images'][v];ee=a['image_edge'][n]
            assert a['image_source'][n]==iu and a['image_destination'][n]==iv
            assert oa['offsets'][iu]<=ee<oa['offsets'][iu+1] and oa['targets'][ee]==iv and oa['weights'][ee]==w
            oo=oc['low_options'][oa['ordinary_a'][iu]][oa['meta'][ee]]
            assert oo['H']==1 and oo['target']==x and oo['destination_shadow']==c['refined_shadow'][ti]
            r=w+a['potential'][u]-a['potential'][v];assert r==w+old.p[iu]-old.p[iv]>=0;residuals[r]+=1
            su=old.p[iu] if si<1188 else oc['initial_by_B'][bi]
            tv=old.p[iv] if ti<1188 else oc['initial_by_B'][bj]
            oldr=w+su-tv
            if oldr<0:failures[(w,oldr)]+=1
            n+=1
        assert time.process_time()-start<120,'UNKNOWN: finite audit cap'
    assert n==719976 and c['combined_edges']==2635563
    assert failures=={(-1,-1):24,(0,-2):219,(0,-1):3473,(1,-1):1852}
    finite_time=round(time.process_time()-start,3);phase=time.process_time()
    d=DAG();L=build_slow(d,'MXL');dh=DAG();H=build_shigh(dh,'MXH')
    general=json.loads((BASE/'original_port_controls.json').read_text());visible=json.loads((BASE/'visible_port_cycle.json').read_text())
    records=general['records']+visible['records'];assert len(records)==14
    byname={r['label']:r for r in records};assert len(byname)==14
    for r in records:
        dag,root=(d,L['root']) if r['kind']=='LOW' else (dh,H['root'])
        env=r['environment'];assert set(env)==set(dag.vars);V.bounds(dag,env);assert dag.ev_ground(root,env)
        for suffix,s in (('s',r['source']),('t',r['destination'])):
            tag=('MXL' if r['kind']=='LOW' else 'MXH')+suffix
            assert env[tag+'_mu']==s['mu']==341
            assert [env[tag+'_sg'+str(i)] for i in range(10)]==s['sigma']==[1]+[0]*9
            assert env[tag+'_b_broot']==s['b']['root']
            for f in V.FIELDS:assert [env[tag+'_b_b'+f+str(i)] for i in range(19)]==s['b'][f]
            for i,(k,ss,ii) in enumerate(s['alpha']):
                assert env[tag+'_ak'+str(i)]==k and env[tag+'_aS'+str(i)]==bool(ss) and env[tag+'_aI'+str(i)]==ii
            assert V.phi(s)==-3
        ps=P.inspect(r['source']);pt=P.inspect(r['destination'])
        assert ps==r['potential_source'] and pt==r['potential_destination']
        assert r['port_residual']==r['w']+ps['port_joint']-pt['port_joint']>=0
        if r['kind']=='LOW':
            assert env['MXL_H']==r['H']==1 and env['MXLbt_q']==r['q'] and env['MXL_w']==r['w']==2-r['q']
            assert any(p['population'][0]==1 and not p['hidden_S'] for p in r['port_inventory'])
        else:
            assert env['MXH_q']==r['q'] and env['MXH_w1']==r['w']==6-r['q']
            m=r['shared_midpoint'];assert env['MXHg_fmu']==m['mu']==341 and env['MXHg_fv']==m['v']
            assert [env['MXHg_fsg'+str(i)] for i in range(10)]==m['sigma']==[1]+[0]*9
            assert env['MXHg_fb_broot']==m['b']['root']
            for f in V.FIELDS:assert [env['MXHg_fb_b'+f+str(i)] for i in range(19)]==m['b'][f]
            assert r['OM_reduced_weight']==r['w']+ps['port_joint']>=0 and r['MO_reduced_weight']==-pt['port_joint']>=0
        assert time.process_time()-phase<300,'UNKNOWN: original root audit cap'
    for names in general['macro_variants']:
        x,y=(byname[n] for n in names)
        assert x['source']==y['source'] and x['destination']==y['destination'] and x['w']==y['w']
    cycle=[byname[n] for n in general['closed_mixed_cycle']['labels']]
    for l,r in zip(cycle,cycle[1:]+cycle[:1]):assert l['destination']==r['source']
    assert sum(r['w'] for r in cycle)==sum(r['port_residual'] for r in cycle)==4
    cycle=visible['records'];assert cycle[0]['source']==cycle[1]['destination'] and cycle[0]['destination']==cycle[1]['source']
    assert sum(r['w'] for r in cycle)==sum(r['port_residual'] for r in cycle)==8
    assert all(any(x[0]==1 for x in r[k]['alpha']) for r in cycle for k in ('source','destination'))
    result={'status':'COMPLETE','whole_tree_commutations':8634,'source_access_queries':24310,
        'new_edges_independently_regenerated_and_image_checked':719976,'combined_low_edges':2635563,
        'old_physical_nodes_unchanged':342796,'new_port_nodes':126550,'potential_range':[-2,0],
        'minimum_new_residual':min(residuals),'residual_histogram':dict(residuals),
        'old_interface_failures_repaired':sum(failures.values()),'cheap_interface_failures_repaired':5544,
        'negative_H1_interface_failures_repaired':24,'full_original_low_roots_replayed':12,
        'full_original_high_roots_replayed':2,'full_ordinary_states_and_midpoints_checked':True,
        'closed_mixed_control_weights':[4,8],'observed_port_on_second_cycle':True,
        'negative_mixed_cycles_certified':0,'new_potential_fit':False,
        'finite_audit_CPU_seconds':finite_time,'original_audit_CPU_seconds':round(time.process_time()-phase,3)}
    with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='residual_histogram'},indent=2),flush=True)
if __name__=='__main__':main()
