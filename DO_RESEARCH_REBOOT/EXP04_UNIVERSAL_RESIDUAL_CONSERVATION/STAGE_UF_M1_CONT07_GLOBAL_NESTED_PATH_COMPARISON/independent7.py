from base7 import *
from physical1 import Edges
from model0 import to_tuple
from exp01_oracle import Tree,Replay
from independent import splay as ind

def full_physical(s,p):
    assert digest(s)==p['source_sha256'];n=len(s['initial_B']['children']);aa,bb=Edges(s['initial_A']),Edges(s['initial_B']);initial=aa.code(),bb.code()
    M=set();last=bb.root
    for tag,x in s['operations']:
        if tag=='K':
            if x!=last:M.add(x)
            last=x
    S=set()
    for x in M:S.update(bb.path(x))
    assert sorted(M)==p['original_genuine_M'] and sorted(S)==p['original_S'];Sbits=sum(1<<(x-1) for x in S)
    ds={tuple(z['parent']):z for z in p['doubles']};pool=p['state_pool']['states'];A=Q=bits=abits=azig=bzig=steps=0;bad=set(s.get('protected_labels',[]))
    assert not bad&{z&Sbits for z in aa.m[1:]}
    def interval(mask):return [(mask&-mask).bit_length(),mask.bit_length()]
    for h,(row,(tag,x)) in enumerate(zip(p['boundaries'],s['operations']),1):
        assert (row['t'],row['tag'],row['x'])==(h,tag,x)
        assert (aa.code(),bb.code())==(int(pool[row['pre_A_state']],16),int(pool[row['pre_B_state']],16))
        ap=aa.path(x);assert ap==row['A_path'] and row['a']==len(ap)//2
        assert row['post_A_time']-row['start_time']==len(ap)-1
        if tag=='K':
            bp=bb.path(x);assert bp==row['B_path'] and (len(bp)-1)//2==row['q']
            for j in range(1,row['q']+1):
                d=ds[h,j];g,pold=bp[-1-2*j],bp[-2*j]
                case=('R' if pold>g else 'L')+('R' if x>pold else 'L')
                assert (d['g'],d['p'],d['target'],d['case'])==(g,pold,x,case)
                assert d['F']==bb.m[g]&Sbits and d['physical_frame_interval']==interval(bb.m[g])
        for i in range(row['start_time'],row['end_time']):
            e=p['events'][i];actor='A' if i<row['post_A_time'] else 'B';tree,other=(aa,bb) if actor=='A' else (bb,aa)
            assert e['time']==i+1 and e['id'][0]==e['actor']==actor and e['id'][1]==h and e['target']==x
            before={z&Sbits for z in tree.m[1:]}-{0};otherlabs={z&Sbits for z in other.m[1:]}-{0}
            tree.step(e);after={z&Sbits for z in tree.m[1:]}-{0};lost=before-after;made=after-before
            assert sorted(lost)==e['lost'] and sorted(made)==e['created']
            sign=(sum(z in otherlabs for z in lost)-sum(z in otherlabs for z in made)) if actor=='A' else (sum(z not in otherlabs for z in made)-sum(z not in otherlabs for z in lost))
            assert sign==e['sign'] and e['demoted_label']==tree.m[e['pivot']]&Sbits;bits+=1
            if actor=='A':
                assert not bad&after;abits+=1;azig+=e['case']=='ZIG';steps+=e['id'][3]==0
            else:bzig+=e['case']=='ZIG'
        assert (aa.code(),bb.code())==(int(pool[row['post_A_state']],16),int(pool[row['post_B_state']],16))
        assert aa.root==x and (bb.root==x if tag=='K' else row['q']==0)
        if tag=='K':
            for j in range(1,row['q']+1):
                d=ds[h,j];assert (bb.m[d['g']]&Sbits,bb.m[d['p']]&Sbits)==(d['J'],d['P_output'])
                assert interval(bb.m[d['g']])==d['physical_J_interval'] and interval(bb.m[d['p']])==d['physical_P_interval']
        A+=row['a'];Q+=row['q']
    assert len(p['boundaries'])==len(s['operations']) and bits==len(p['events']) and Q==len(ds)
    aa.recompute();bb.recompute();assert (aa.code(),bb.code())==initial
    assert steps==A and abits==2*A-azig and bits-abits==2*Q+bzig
    assert p['state_pool']['original_event_sha256']==digest(p['events'])
    return {'A':A,'Q_B':Q,'primitives':bits,'real_A_bits':abits,'actual_A_StepEv':steps,'A_terminal_zigs':azig,'B_terminal_zigs':bzig,
        'original_S':sorted(S),'original_genuine_M':sorted(M),'protected_A_labels_verified_at_every_bit':bool(bad),
        'complete_edges_SET_signs_paths_frames_outputs_and_pair_closure':True}

def elision_check():
    p=load(C6/'FRESH_PHYS_00.json');s=load(C6/'FRESH_SOURCE_CATALOG.json')[0];z=load(ROOT/'EXACT_PAID_HIT_ELISION_REFUTATION.json')
    from cohortc import decode_state
    from exp03_core import frame_records
    pre=decode_state(p,p['boundaries'][2]['post_B_state']);x=p['boundaries'][6]['x'];tree=Tree(pre);immutable,events=ind.trace(to_tuple(pre),x)
    Replay.plain_splay(tree,x);assert to_tuple(tree.state())==immutable
    frames=list(frame_records(pre,x,tree.state()).values());assert not any(f['g']==2 for f in frames)
    path=Tree(pre).path(x);assert len(path)-1-path.index(2)==9
    original=next(d for d in p['doubles'] if d['parent']==[7,4]);assert original['g']==2
    acc=load(C6/'FRESH_ORDERED_00.json');assert any(e['consumer']==5 for e in acc['disjoint_original_assignments']['skipped_rank'])
    assert any(e['original_parent']==[7,4] for e in acc['C_old']) and not any(e['original_parent']==[7,4] for e in acc['E_old'])
    return {'source_sha256':digest(s),'shadow_frames_after_elision':frames,'missing_original_old_g':2,'original_parent':[7,4],
        'independent_immutable_and_literal_frame_check':True,'scope':'Pre-H canonical witness; actual residual zero.'}
