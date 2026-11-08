"""Complete single-fringe-leaf port commutation and pullback of the existing joint certificate."""
import sys,json,time
from pathlib import Path
from collections import defaultdict,Counter
from array import array
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_H1F01','DO_RESEARCH_REBOOT/M3_FRC01',
             'DO_RESEARCH_REBOOT/M3_H2R01','DO_RESEARCH_REBOOT/M3_PHI01','python/independent']
import splay as S
import verify_full_mixed as V
from one_gap_potential import OneGapPotential
M=(0,2,4,6,8);BASE=Path('DO_RESEARCH_REBOOT/M3_G0P01');PORT=('leaf','gap0')
def port_tree(t):
    if t==S.LEAF:return t
    k=t[1];l=port_tree(t[2]);r=port_tree(t[3])
    if k==0:assert l==S.LEAF;l=PORT
    return S.node(k,l,r)
def shadow(t):
    def at(path):
        z=t
        for side in path:
            if z[0]=='leaf':return (1,0,0) if z==PORT else (2,0,0)
            z=z[2+side]
        if z[0]=='leaf':return (1,0,0) if z==PORT else (2,0,0)
        return (0,1,z[1])
    return tuple(at(path) for path in ((),(0,),(1,),(0,0),(0,1),(1,0),(1,1)))
def rho(a):
    a=tuple(tuple(r) for r in a)
    ports={i for i,r in enumerate(a) if r[0]==1}
    if not ports:return a,'identity'
    out=list(a)
    if a[0]==(0,1,0) and ports=={1,3,4}:
        out[1]=(0,0,0);out[3]=out[4]=(2,0,0);return tuple(out),'L_under_root0'
    if a[1]==(0,1,0) and ports=={3}:
        out[3]=(0,0,0);return tuple(out),'LL_under_left0'
    return None,'outside_class'
def main():
    assert not (BASE/'refinement_certificate.json').exists();start=time.process_time();P=OneGapPotential()
    c=P.c;a=P.a;physical=[tuple(tuple(r) for r in s) for s in c['shadows']];oldids={s:i for i,s in enumerate(physical)}
    assert all(rho(s)==(s,'identity') for s in physical)
    union=list(physical);uids=dict(oldids);family={};commute=[];source_shapes=set();rules=Counter();queries=0
    for tid,t in enumerate(P.old.old.trees):
        pt=port_tree(t);sa=shadow(pt);rs,rule=rho(sa);assert rs==tuple(tuple(r) for r in V.shadow(V.insert(t,-1)))
        source_shapes.add(sa);rules[rule]+=1
        if sa not in uids:uids[sa]=len(union);union.append(sa)
        for x in M:
            queries+=1;h=S.lookup(pt,x)[1]
            if h not in (1,2):continue
            dt=S.trace(pt,x)[0];ta=shadow(dt);rt,trule=rho(ta)
            physical_dest=S.trace(V.insert(t,-1),x)[0]
            assert rt==tuple(tuple(r) for r in V.shadow(physical_dest))
            assert S.lookup(V.insert(t,-1),x)[1]==h
            if ta not in uids:uids[ta]=len(union);union.append(ta)
            oldai=oldids[rs];oldaj=oldids[rt]
            oi=next(j for j,o in enumerate(c['low_options'][oldai]) if o['H']==1 and o['target']==x and o['destination_shadow']==oldaj)
            key=(uids[sa],x,uids[ta])
            family.setdefault(key,{'source_shadow':uids[sa],'target':x,'destination_shadow':uids[ta],
                                  'A_core_tree':tid,'A_depth':h,'image_source_shadow':oldai,
                                  'image_destination_shadow':oldaj,'old_option':oi})
            commute.append({'A_core_tree':tid,'target':x,'depth':h,'source_rule':rule,'destination_rule':trule,
                            'source_shadow':uids[sa],'destination_shadow':uids[ta],'commutes':True})
        assert time.process_time()-start<120,'UNKNOWN: commutation cap'
    opts=list(family.values());byroot={r:[i for i,s in enumerate(union) if s[0]==(0,1,r)] for r in range(9)}
    local={ai:j for r in range(9) for j,ai in enumerate(byroot[r])}
    oldlocal={ai:j for r in range(9) for j,ai in enumerate(c['shadows_by_root'][str(r)])}
    bases=[-1]*4862;ob=array('H');oa=array('H');images=array('I');pot=array('i');refined=[]
    for s in union:
        rs,rule=rho(s);assert rs in oldids;refined.append(oldids[rs])
    for bi,b in enumerate(P.old.old.trees):
        if b[1] not in M:continue
        bases[bi]=len(ob)
        for ai in byroot[b[1]]:
            image=c['B_bases'][bi]+oldlocal[refined[ai]]
            ob.append(bi);oa.append(ai);images.append(image);pot.append(P.p[image])
            assert -2<=pot[-1]<=-c['psi'][bi]
    assert len(ob)<=2000000,'UNKNOWN: state cap'
    arrays={k:array('I') for k in ('source','destination','image_source','image_destination','image_edge','option')};arrays['weights']=array('b')
    badold=Counter();directions=Counter();samples={};optsbyroot=defaultdict(list)
    for j,o in enumerate(opts):optsbyroot[union[o['source_shadow']][0][2]].append((j,o))
    Bdest=json.loads(Path('DO_RESEARCH_REBOOT/M3_H1F01/cheap_census.json').read_text())
    for bi,b in enumerate(P.old.old.trees):
        if b[1] not in M:continue
        for j,o in optsbyroot[b[1]]:
            si=o['source_shadow'];ti=o['destination_shadow'];x=o['target']
            if si<len(physical) and ti<len(physical):continue # unchanged old physical edge
            h=Bdest['B_depth'][bi][x]
            if not h:continue
            bj=Bdest['B_destination'][bi][x];u=bases[bi]+local[si];v=bases[bj]+local[ti];w=2-h//2
            iu=images[u];iv=images[v]
            ee=next(e for e in range(a['offsets'][iu],a['offsets'][iu+1]) if a['meta'][e]==o['old_option'])
            assert a['targets'][ee]==iv and a['weights'][ee]==w
            residual=w+pot[u]-pot[v];assert residual>=0
            oldsu=P.p[iu] if si<len(physical) else c['initial_by_B'][bi]
            oldtv=P.p[iv] if ti<len(physical) else c['initial_by_B'][bj]
            oldres=w+oldsu-oldtv
            direction=('physical' if si<len(physical) else 'port')+'_to_'+('physical' if ti<len(physical) else 'port')
            directions[direction]+=1
            if oldres<0:badold[(w,oldres)]+=1
            row=len(arrays['weights'])
            for k,val in (('source',u),('destination',v),('image_source',iu),('image_destination',iv),('image_edge',ee),('option',j),('weights',w)):arrays[k].append(val)
            if direction not in samples or (oldres<0 and samples[direction]['old_residual']>=0):
                samples[direction]={'edge':row,'old_residual':oldres,'new_residual':residual,'source_B':bi,'destination_B':bj,**o}
            assert c['edges']+len(arrays['weights'])<=5000000,'UNKNOWN: combined edge cap'
        assert time.process_time()-start<120,'UNKNOWN: joint map cap'
    arrays.update(ordinary_b=ob,ordinary_a=oa,images=images,potential=pot)
    for name,values in arrays.items():
        with (BASE/(name+'.bin')).open('xb') as f:values.tofile(f)
    cat={'format':'G0P01-pullback-v1','byteorder':sys.byteorder,'mu':341,'sigma':[1]+[0]*9,'chi8':True,
         'shadows':union,'old_physical_shadow_count':len(physical),'refined_shadow':refined,
         'shadows_by_root':byroot,'B_bases':bases,'family_options':opts,'samples':samples,
         'nodes':len(ob),'new_edges':len(arrays['weights']),'old_edges_retained':c['edges'],
         'combined_edges':c['edges']+len(arrays['weights'])}
    with (BASE/'port_catalog.json').open('x',encoding='utf-8') as f:json.dump(cat,f,indent=2)
    result={'status':'COMPLETE','A_core_trees':4862,'access_queries':queries,'commuting_accesses':len(commute),
         'partial_shadow_classes':len(source_shapes),'extra_port_shadow_classes':len(union)-len(physical),
         'joint_nodes':len(ob),'new_interface_edges':cat['new_edges'],'combined_edges':cat['combined_edges'],
         'refinement_rules':dict(rules),'directions':dict(directions),
         'old_extension_failures_repaired':[{'w':w,'old_residual':r,'edges':n} for (w,r),n in sorted(badold.items())],
         'new_range':[min(pot),max(pot)],'new_label_fit':False,'old_physical_values_unchanged':True,
         'samples':samples,'commutation_rows':commute,'cpu_seconds':round(time.process_time()-start,3)}
    with (BASE/'refinement_certificate.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k not in ('commutation_rows','samples')},indent=2),flush=True)
def load():
    c=json.loads((BASE/'port_catalog.json').read_text());arrays={}
    types={k:'I' for k in ('source','destination','image_source','image_destination','image_edge','option','images')}
    types.update(weights='b',potential='i',ordinary_b='H',ordinary_a='H')
    for name,typ in types.items():
        x=array(typ);x.frombytes((BASE/(name+'.bin')).read_bytes())
        if c['byteorder']!=sys.byteorder and x.itemsize>1:x.byteswap()
        arrays[name]=x
    return c,arrays
if __name__=='__main__':main()
