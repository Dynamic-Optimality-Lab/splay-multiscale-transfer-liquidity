"""Independent completeness, commuting/image audit and full original-relation verification."""
import sys,json,time,ast
from pathlib import Path
from functools import lru_cache
from collections import Counter,defaultdict
sys.path.insert(0,'DO_RESEARCH_REBOOT/M3_S3P01')
from certify_core3_v2 import BASE,M,S,V,hide,expand,shadow,load,fringe_rho,load_previous
from core3_potential import Core3Potential
from PC_TYPED_DAG import DAG
from STRICT_LOW_COMPILER import build_slow
from STRICT_HIGH_COMPILER import build_shigh
OUT=BASE/'audit_results.json'
@lru_cache(None)
def key_trees(keys):
    if not keys:return (S.LEAF,)
    return tuple(S.node(k,l,r) for i,k in enumerate(keys) for l in key_trees(keys[:i]) for r in key_trees(keys[i+1:]))
def leaf(t,x):
    while t[1]!=x:t=t[2] if x<t[1] else t[3]
    return t[2:]==(S.LEAF,S.LEAF)
def rewrite(a):
    b=[tuple(r) for r in a]
    if b[0]==(0,1,2) and b[2]==(0,1,4) and b[5]==(1,0,0):b[5]=(0,1,3)
    elif b[0]==(0,1,4) and b[1]==(0,1,2) and b[4]==(1,0,0):b[4]=(0,1,3)
    return fringe_rho(b)[0]
def main():
    assert not OUT.exists();start=time.process_time();P=Core3Potential();J=P.physical;c,a=load();pc,pa=load_previous()
    for path in BASE.glob('*.py'):ast.parse(path.read_text(),filename=str(path))
    full=[V.from_serial(t) for t in J.c['A_trees']];single={t for t in full if leaf(t,3)}
    both={t for t in single if leaf(t,-1)}
    constructed_single={V.insert(t,3) for t in key_trees(tuple(k for k in range(-1,9) if k!=3))}
    constructed_both={V.insert(V.insert(t,-1),3) for t in key_trees(tuple(k for k in range(9) if k!=3))}
    assert len(single)==4862 and single==constructed_single
    assert len(both)==1430 and both==constructed_both
    union=[tuple(tuple(r) for r in s) for s in c['shadows']];uid={s:i for i,s in enumerate(union)}
    assert len(union)==len(uid)==1498
    physical=[tuple(tuple(r) for r in s) for s in J.c['shadows']];pid={s:i for i,s in enumerate(physical)}
    for i,s in enumerate(pc['shadows']):assert union[i]==tuple(tuple(r) for r in s)
    for i,s in enumerate(union):assert rewrite(s)==physical[c['refined_shadow'][i]]
    assert all(s[0] in ((0,1,2),(0,1,4)) for s in union[1444:])
    expected_options=set();expected_commute={};sourcequeries=0
    for tid,t in enumerate(full):
        if t not in single:continue
        modes=[(3,)]+([(-1,3)] if t in both else [])
        for hidden in modes:
            pt=hide(t,hidden);assert expand(pt)==t;sa=shadow(pt);rs=rewrite(sa)
            assert rs==tuple(tuple(r) for r in V.shadow(t))
            def check(H,x,result,fp):
                assert expand(result)==fp
                ta=shadow(result);rt=rewrite(ta);assert rt==tuple(tuple(r) for r in V.shadow(fp))
                expected_options.add((uid[sa],H,x,uid[ta]))
                expected_commute[(tid,hidden,H,x)]=(uid[sa],uid[ta])
            for x in M:
                sourcequeries+=1;found,h=S.lookup(pt,x)
                if found and h in (1,2):check(1,x,S.trace(pt,x)[0],S.trace(t,x)[0])
            if -1 not in hidden:
                found,h0=S.lookup(pt,-1)
                if found and h0 in (1,2):
                    pre=S.trace(pt,-1)[0];fp=S.trace(t,-1)[0];assert expand(pre)==fp
                    for x in M:
                        sourcequeries+=1;found,h=S.lookup(pre,x)
                        if found and h in (1,2):check(2,x,S.trace(pre,x)[0],S.trace(fp,x)[0])
    cert=json.loads((BASE/'core3_certificate.json').read_text())
    assert sourcequeries==cert['source_access_queries']==43615
    assert len(expected_commute)==len(cert['commutation_rows'])==14845
    for r in cert['commutation_rows']:
        assert expected_commute[(r['A_tree'],tuple(r['hidden_leaves']),r['H'],r['target'])]==(r['source_shadow'],r['destination_shadow'])
    actual={(o['source_shadow'],o['H'],o['target'],o['destination_shadow']) for o in c['family_options']}
    assert actual==expected_options and len(actual)==len(c['family_options'])
    local={ai:j for r in range(9) for j,ai in enumerate(c['shadows_by_root'][str(r)])}
    oldlocal={ai:j for r in range(9) for j,ai in enumerate(J.c['shadows_by_root'][str(r)])}
    for u,(bi,ai) in enumerate(zip(a['ordinary_b'],a['ordinary_a'])):
        image=J.c['B_bases'][bi]+oldlocal[c['refined_shadow'][ai]]
        assert a['images'][u]==image and a['potential'][u]==J.p[image]
        assert -2<=a['potential'][u]<=-J.c['psi'][bi]
        assert u==c['B_bases'][bi]+local[ai]
    assert len(a['potential'])==481562
    for u,(bi,ai) in enumerate(zip(pa['ordinary_b'],pa['ordinary_a'])):
        v=c['B_bases'][bi]+local[ai]
        assert a['potential'][v]==pa['potential'][u] and a['images'][v]==pa['images'][u]
    bt=J.old.old.trees;bdest=[];bdepth=[];h2={}
    from fringe_kernel import gap_leaf,erase
    for bi,t in enumerate(bt):
        bdest.append([J.old.old.ids[S.trace(t,x)[0]] for x in range(9)])
        bdepth.append([S.lookup(t,x)[1] for x in range(9)])
        if t[1] in M:
            pre=S.trace(V.insert(t,-1),-1)[0]
            for x in M:
                end=S.trace(pre,x)[0]
                if gap_leaf(end):h2[(bi,x)]=(J.old.old.ids[erase(end)],S.lookup(pre,x)[1]//2)
    opts=defaultdict(list)
    for j,o in enumerate(c['family_options']):
        root=union[o['source_shadow']][0]
        if root[0]==0 and root[1]:opts[root[2]].append((j,o))
    n=0;residuals=Counter();failures=Counter();Hcounts=Counter()
    for bi,b in enumerate(bt):
        if b[1] not in M:continue
        for j,o in opts[b[1]]:
            si=o['source_shadow'];ti=o['destination_shadow'];x=o['target'];H=o['H']
            if si<1444 and ti<1444:continue
            if H==1:
                h=bdepth[bi][x]
                if h==0:continue
                bj=bdest[bi][x];q=h//2
            else:
                assert -1 not in o['hidden_leaves']
                result=h2.get((bi,x))
                if result is None:continue
                bj,q=result
            u=c['B_bases'][bi]+local[si];v=c['B_bases'][bj]+local[ti];w=2*H-q
            assert (a['source'][n],a['destination'][n],a['weights'][n],a['option'][n])==(u,v,w,j)
            iu=a['images'][u];iv=a['images'][v];ee=a['image_edge'][n]
            assert (a['image_source'][n],a['image_destination'][n])==(iu,iv)
            assert J.a['offsets'][iu]<=ee<J.a['offsets'][iu+1] and J.a['targets'][ee]==iv and J.a['weights'][ee]==w
            oo=J.c['low_options'][J.a['ordinary_a'][iu]][J.a['meta'][ee]]
            assert oo['H']==H and oo['target']==x and oo['destination_shadow']==c['refined_shadow'][ti]
            r=w+a['potential'][u]-a['potential'][v];assert r==w+J.p[iu]-J.p[iv]>=0
            residuals[r]+=1;Hcounts[H]+=1
            su=J.p[iu] if si<1444 else J.c['initial_by_B'][bi]
            tv=J.p[iv] if ti<1444 else J.c['initial_by_B'][bj]
            if w+su-tv<0:failures[(H,w,w+su-tv)]+=1
            n+=1
        assert time.process_time()-start<120,'UNKNOWN: finite audit cap'
    assert n==239010 and c['combined_edges']==2874573
    assert failures=={(1,-1,-1):131,(1,0,-2):744,(1,0,-1):3863,(1,1,-1):1884}
    finite_time=round(time.process_time()-start,3);phase=time.process_time()
    positive=json.loads((BASE/'original_core3_controls.json').read_text())
    negative=json.loads((BASE/'wrong_inventory_controls.json').read_text())
    records=positive['records'];assert len(records)==17
    d=DAG();L=build_slow(d,'MXL');dh=DAG();HIGH=build_shigh(dh,'MXH')
    assert len(d.nodes)==1400081 and len(dh.nodes)==53455
    names={r['label']:r for r in records};assert len(names)==17
    for r in records:
        dag,root=(d,L['root']) if r['kind']=='LOW' else (dh,HIGH['root'])
        env=r['environment'];assert set(env)==set(dag.vars);V.bounds(dag,env);assert dag.ev_ground(root,env)
        for suffix,s in (('s',r['source']),('t',r['destination'])):
            tag=('MXL' if r['kind']=='LOW' else 'MXH')+suffix
            assert env[tag+'_mu']==s['mu']==341 and [env[tag+'_sg'+str(i)] for i in range(10)]==s['sigma']==[1]+[0]*9
            assert env[tag+'_b_broot']==s['b']['root']
            for f in V.FIELDS:assert [env[tag+'_b_b'+f+str(i)] for i in range(19)]==s['b'][f]
            for i,(k,ss,ii) in enumerate(s['alpha']):
                assert env[tag+'_ak'+str(i)]==k and env[tag+'_aS'+str(i)]==bool(ss) and env[tag+'_aI'+str(i)]==ii
            assert V.phi(s)==-3
        ps=P.inspect(r['source']);pt=P.inspect(r['destination'])
        assert ps==r['potential_source'] and pt==r['potential_destination']
        assert r['core3_residual']==r['w']+ps['core3_joint']-pt['core3_joint']>=0
        if r['kind']=='LOW':
            assert env['MXL_H']==r['H'] and env['MXLbt_q']==r['q'] and env['MXL_w']==r['w']==2*r['H']-r['q']
            inv=r['port_inventory'];has3=False
            for p in inv:
                slot=p['slot'];side=p['side']
                assert p['hidden_S']==[k for k in range(9) if env[f'MXLv_hs{slot}_{side}_{k}']]
                assert p['population']==[env[f'MXLv_z{k}_{slot}_{side}'] for k in range(10)]
                if p['hidden_S']==[3] and p['population']==[0]*10:
                    assert p['lower']==4 and p['upper']==5;has3=True
            assert has3
            assert not any(env[f'MXLw_p{i}'] and env[f'MXLw_isS{i}'] and env[f'MXLw_sidx{i}']==3 for i in range(127))
        else:
            m=r['shared_midpoint'];assert env['MXHg_fmu']==m['mu']==341 and env['MXHg_fv']==m['v']
            assert [env['MXHg_fsg'+str(i)] for i in range(10)]==m['sigma']==[1]+[0]*9
            assert env['MXHg_fb_broot']==m['b']['root']
            for f in V.FIELDS:assert [env['MXHg_fb_b'+f+str(i)] for i in range(19)]==m['b'][f]
            assert env['MXH_q']==r['q'] and env['MXH_w1']==r['w']==6-r['q']
            assert r['OM_reduced_weight']==r['w']+ps['core3_joint']>=0 and r['MO_reduced_weight']==-pt['core3_joint']>=0
        assert time.process_time()-phase<300,'UNKNOWN: original audit cap'
    for r in negative['records']:
        env=r['environment'];assert set(env)==set(d.vars);V.bounds(d,env);assert not d.ev_ground(L['root'],env)
        base=names[r['base_control']]['environment']
        assert {key for key in env if env[key]!=base[key]}=={r['mutated_field']}
        assert r['mutated_field'].startswith('MXLv_')
    for l,r in positive['macro_variants']:
        l=names[l];r=names[r];assert l['source']==r['source'] and l['destination']==r['destination'] and l['H']==r['H'] and l['w']==r['w']
    cycle=[names[label] for label in positive['closed_mixed_cycle']['labels']]
    assert cycle[0]['source']==cycle[1]['destination'] and cycle[0]['destination']==cycle[1]['source']
    assert sum(r['w'] for r in cycle)==sum(r['core3_residual'] for r in cycle)==8
    assert 'S3_RL' in cycle[0]['potential_source']['core3_rule'] and 'G0_' in cycle[0]['potential_source']['core3_rule']
    assert 'S3_LR' in cycle[0]['potential_destination']['core3_rule']
    result={'status':'COMPLETE','single_S3_leaf_A10_trees':4862,'both_leaf_A10_trees':1430,
        'independent_insertion_completeness_checked':True,'source_access_queries':sourcequeries,
        'whole_tree_commutations':14845,'new_edges_regenerated_and_old_images_checked':239010,
        'new_H1_edges':Hcounts[1],'new_H2_edges':Hcounts[2],'combined_low_edges':2874573,
        'old_G0P01_states_unchanged':469346,'new_port_states':12216,'new_port_shadow_classes':54,
        'potential_range':[-2,0],'minimum_new_residual':min(residuals),'old_extension_failures_repaired':sum(failures.values()),
        'cheap_H1_failures_repaired':744+3863+1884,'negative_H1_failures_repaired':131,
        'original_low_roots_accepted':16,'original_high_roots_accepted':1,'wrong_inventory_roots_rejected':4,
        'full_state_fields_and_midpoint_checked':True,'opaque_S3_inventory_verified':True,
        'whole_macro_variants':4,'closed_mixed_cycle_weight':8,'both_ports_and_orientations_on_cycle':True,
        'new_label_fit':False,'negative_mixed_cycles_certified':0,
        'finite_audit_CPU_seconds':finite_time,'original_audit_CPU_seconds':round(time.process_time()-phase,3)}
    with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':main()
