"""Complete core3 singleton-leaf port pullback, including the existing fringe leaf port."""
import sys,json,time
from pathlib import Path
from collections import Counter,defaultdict
from array import array
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_G0P01','DO_RESEARCH_REBOOT/M3_H1F01',
             'DO_RESEARCH_REBOOT/M3_FRC01','DO_RESEARCH_REBOOT/M3_H2R01',
             'DO_RESEARCH_REBOOT/M3_PHI01','python/independent']
import splay as S
import verify_full_mixed as V
from port_potential import PortPotential
from certify_refinement import load as load_previous,rho as fringe_rho
BASE=Path('DO_RESEARCH_REBOOT/M3_S3P01');M=(0,2,4,6,8)
def node_at(t,x):
    while t!=S.LEAF:
        if t[1]==x:return t
        t=t[2] if x<t[1] else t[3]
    raise KeyError(x)
def leaf_key(t,x):return node_at(t,x)[2:]==(S.LEAF,S.LEAF)
def hide(t,keys):
    if t==S.LEAF:return t
    if t[1] in keys:
        assert t[2:]==(S.LEAF,S.LEAF)
        return ('leaf',t[1]) # private test payload; rho never reads it
    return S.node(t[1],hide(t[2],keys),hide(t[3],keys))
def expand(t):
    if t[0]=='leaf':return S.node(t[1],S.LEAF,S.LEAF) if len(t)>1 else S.LEAF
    return S.node(t[1],expand(t[2]),expand(t[3]))
def shadow(t):
    def at(path):
        z=t
        for side in path:
            if z[0]=='leaf':return (1,0,0) if len(z)>1 else (2,0,0)
            z=z[2+side]
        if z[0]=='leaf':return (1,0,0) if len(z)>1 else (2,0,0)
        return (0,int(z[1]>=0),z[1] if z[1]>=0 else 0)
    return tuple(at(p) for p in ((),(0,),(1,),(0,0),(0,1),(1,0),(1,1)))
def rho(a):
    a=tuple(tuple(r) for r in a);out=list(a);rule=[]
    if a[0]==(0,1,2) and a[2]==(0,1,4) and a[5]==(1,0,0):
        out[5]=(0,1,3);rule.append('S3_RL')
    elif a[0]==(0,1,4) and a[1]==(0,1,2) and a[4]==(1,0,0):
        out[4]=(0,1,3);rule.append('S3_LR')
    refined,g0rule=fringe_rho(out)
    if refined is None:return None,'outside_class'
    if g0rule!='identity':rule.append('G0_'+g0rule)
    return refined,'+'.join(rule) if rule else 'identity'
def main():
    assert not (BASE/'core3_certificate.json').exists();start=time.process_time();prior=PortPotential();J=prior.old
    pc,pa=load_previous();oc=J.c;oa=J.a
    physical=[tuple(tuple(r) for r in s) for s in oc['shadows']];pids={s:i for i,s in enumerate(physical)}
    union=[tuple(tuple(r) for r in s) for s in pc['shadows']];uids={s:i for i,s in enumerate(union)};oldn=len(union)
    assert oldn==1444
    for i,s in enumerate(union):assert rho(s)[0]==physical[pc['refined_shadow'][i]]
    full=[V.from_serial(t) for t in oc['A_trees']];cases=[];modecounts=Counter()
    for i,t in enumerate(full):
        if not leaf_key(t,3):continue
        cases.append((i,(3,)));modecounts['S3_only']+=1
        if leaf_key(t,-1):cases.append((i,(-1,3)));modecounts['S3_and_G0']+=1
    assert modecounts=={'S3_only':4862,'S3_and_G0':1430}
    family={};commute=[];rules=Counter();queries=0
    for tid,hidden in cases:
        t=full[tid];pt=hide(t,hidden);assert expand(pt)==t
        sa=shadow(pt);rs,srule=rho(sa);assert rs==tuple(tuple(r) for r in V.shadow(t));rules[srule]+=1
        if sa not in uids:uids[sa]=len(union);union.append(sa)
        def add(H,x,depths,result,expected_tree):
            assert expand(result)==expected_tree
            ta=shadow(result);rt,trule=rho(ta);assert rt==tuple(tuple(r) for r in V.shadow(expected_tree))
            if ta not in uids:uids[ta]=len(union);union.append(ta)
            pi=pids[rs];pj=pids[rt]
            oi=next(j for j,o in enumerate(oc['low_options'][pi]) if o['H']==H and o['target']==x and o['destination_shadow']==pj)
            key=(uids[sa],H,x,uids[ta])
            family.setdefault(key,{'source_shadow':uids[sa],'destination_shadow':uids[ta],
                'H':H,'target':x,'A_tree':tid,'hidden_leaves':list(hidden),'A_depths':depths,
                'image_source_shadow':pi,'image_destination_shadow':pj,'old_option':oi,
                'word':[['K',x]] if H==1 else [['K',-1],['K',x]]})
            commute.append({'A_tree':tid,'hidden_leaves':list(hidden),'H':H,'target':x,
                'source_shadow':uids[sa],'destination_shadow':uids[ta],'source_rule':srule,
                'destination_rule':trule,'whole_tree_commutes':True})
        for x in M:
            queries+=1;found,h=S.lookup(pt,x)
            if found and h in (1,2):add(1,x,[h],S.trace(pt,x)[0],S.trace(t,x)[0])
        if -1 not in hidden:
            found,h0=S.lookup(pt,-1)
            if found and h0 in (1,2):
                pp=S.trace(pt,-1)[0];fp=S.trace(t,-1)[0];assert expand(pp)==fp
                for x in M:
                    queries+=1;found,h=S.lookup(pp,x)
                    if found and h in (1,2):add(2,x,[h0,h],S.trace(pp,x)[0],S.trace(fp,x)[0])
        assert time.process_time()-start<120,'UNKNOWN: finite commutation cap'
    opts=list(family.values());byroot={r:[i for i,s in enumerate(union) if s[0]==(0,1,r)] for r in range(9)}
    local={ai:j for r in range(9) for j,ai in enumerate(byroot[r])}
    oldlocal={ai:j for r in range(9) for j,ai in enumerate(oc['shadows_by_root'][str(r)])}
    refined=[pids[rho(s)[0]] for s in union];ob=array('H');aa=array('H');images=array('I');potential=array('i');bases=[-1]*4862
    bt=J.old.old.trees
    for bi,b in enumerate(bt):
        if b[1] not in M:continue
        bases[bi]=len(ob)
        for ai in byroot[b[1]]:
            image=oc['B_bases'][bi]+oldlocal[refined[ai]]
            ob.append(bi);aa.append(ai);images.append(image);potential.append(J.p[image])
            assert -2<=potential[-1]<=-oc['psi'][bi]
    assert len(ob)<=2000000 and len(union)<65536,'UNKNOWN: state cap'
    for u,(bi,ai) in enumerate(zip(pa['ordinary_b'],pa['ordinary_a'])):
        v=bases[bi]+local[ai];assert pa['potential'][u]==potential[v] and pa['images'][u]==images[v]
    arrays={k:array('I') for k in ('source','destination','image_source','image_destination','image_edge','option')};arrays['weights']=array('b')
    optsbyroot=defaultdict(list)
    for j,o in enumerate(opts):
        rootrow=union[o['source_shadow']][0]
        if rootrow[0]==0 and rootrow[1]:
            optsbyroot[rootrow[2]].append((j,o))
    binfo=json.loads(Path('DO_RESEARCH_REBOOT/M3_H1F01/cheap_census.json').read_text())
    kernel=json.loads(Path('DO_RESEARCH_REBOOT/M3_H2R01/fringe_kernel_certificate.json').read_text())
    h2={(r['entry_core'],r['target']):r for r in kernel['rows'] if r['gap0_childless_at_exit']}
    counts=Counter();failures=Counter();samples={}
    for bi,b in enumerate(bt):
        if b[1] not in M:continue
        for j,o in optsbyroot[b[1]]:
            si=o['source_shadow'];ti=o['destination_shadow'];x=o['target'];H=o['H']
            if si<oldn and ti<oldn:continue
            if H==1:
                h=binfo['B_depth'][bi][x]
                if h==0:continue
                bj=binfo['B_destination'][bi][x];q=h//2
            else:
                r=h2.get((bi,x))
                if r is None:continue
                bj=r['exit_core'];q=r['q']
            u=bases[bi]+local[si];v=bases[bj]+local[ti];w=2*H-q;iu=images[u];iv=images[v]
            ee=next(e for e in range(oa['offsets'][iu],oa['offsets'][iu+1]) if oa['meta'][e]==o['old_option'])
            assert oa['targets'][ee]==iv and oa['weights'][ee]==w
            red=w+potential[u]-potential[v];assert red>=0
            oldsu=J.p[iu] if si<oldn else oc['initial_by_B'][bi]
            oldtv=J.p[iv] if ti<oldn else oc['initial_by_B'][bj]
            oldred=w+oldsu-oldtv
            if oldred<0:failures[(H,w,oldred)]+=1
            idx=len(arrays['weights'])
            for k,val in (('source',u),('destination',v),('image_source',iu),('image_destination',iv),('image_edge',ee),('option',j),('weights',w)):arrays[k].append(val)
            direction=('old' if si<oldn else 'S3port')+'_to_'+('old' if ti<oldn else 'S3port');counts[(H,w,direction)]+=1
            row={'edge':idx,'source_B':bi,'destination_B':bj,'q':q,'w':w,'old_residual':oldred,'new_residual':red,**o}
            samples.setdefault(direction,row)
            srule=rho(union[si])[1]
            if 'S3_RL' in srule:samples.setdefault('orientation_RL',row)
            if 'S3_LR' in srule:samples.setdefault('orientation_LR',row)
            if 'S3_' in srule and 'G0_' in srule:samples.setdefault('both_visible_ports',row)
            if H==2 and w in (0,1):samples.setdefault('H2_w'+str(w),row)
            if oldred<0:samples.setdefault(f'repaired_H{H}_w{w}_r{oldred}',row)
            assert pc['combined_edges']+len(arrays['weights'])<=5000000,'UNKNOWN: combined edge cap'
        assert time.process_time()-start<120,'UNKNOWN: edge-image cap'
    arrays.update(ordinary_b=ob,ordinary_a=aa,images=images,potential=potential)
    for name,x in arrays.items():
        with (BASE/(name+'.bin')).open('xb') as f:x.tofile(f)
    catalog={'format':'S3P01-pullback-v1','byteorder':sys.byteorder,'mu':341,'sigma':[1]+[0]*9,'chi8':True,
        'shadows':union,'prior_shadow_count':oldn,'refined_shadow':refined,'B_bases':bases,'shadows_by_root':byroot,
        'family_options':opts,'samples':samples,'nodes':len(ob),'new_edges':len(arrays['weights']),
        'old_edges_retained':pc['combined_edges'],'combined_edges':pc['combined_edges']+len(arrays['weights'])}
    with (BASE/'core3_catalog.json').open('x',encoding='utf-8') as f:json.dump(catalog,f,indent=2)
    result={'status':'COMPLETE','physical_A10_trees_filtered':len(full),'family_counts':dict(modecounts),
        'source_access_queries':queries,'whole_tree_commutations':len(commute),'source_rule_counts':dict(rules),
        'new_shadow_classes':len(union)-oldn,'joint_nodes':len(ob),'old_joint_nodes_unchanged':len(pa['potential']),
        'new_joint_states':len(ob)-len(pa['potential']),'new_low_edges':len(arrays['weights']),
        'combined_low_edges':catalog['combined_edges'],'range':[min(potential),max(potential)],
        'new_label_fit':False,'all_old_G0P01_values_unchanged':True,
        'edge_counts':[{'H':H,'w':w,'direction':dr,'count':n} for (H,w,dr),n in sorted(counts.items())],
        'old_extension_failures_repaired':[{'H':H,'w':w,'old_residual':r,'count':n} for (H,w,r),n in sorted(failures.items())],
        'samples':samples,'commutation_rows':commute,'cpu_seconds':round(time.process_time()-start,3)}
    with (BASE/'core3_certificate.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k not in ('samples','commutation_rows','edge_counts')},indent=2),flush=True)
def load():
    c=json.loads((BASE/'core3_catalog.json').read_text());a={}
    types={k:'I' for k in ('source','destination','image_source','image_destination','image_edge','option','images')}
    types.update(weights='b',potential='i',ordinary_b='H',ordinary_a='H')
    for name,typ in types.items():
        x=array(typ);x.frombytes((BASE/(name+'.bin')).read_bytes())
        if c['byteorder']!=sys.byteorder and x.itemsize>1:x.byteswap()
        a[name]=x
    return c,a
if __name__=='__main__':main()


