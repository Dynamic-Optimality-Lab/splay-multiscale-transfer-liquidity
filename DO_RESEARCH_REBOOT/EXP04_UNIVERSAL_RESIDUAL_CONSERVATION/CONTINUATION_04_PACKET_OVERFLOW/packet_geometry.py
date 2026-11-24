from campaign4 import *
from fast_physics import FullTree

if __name__=='__main__':
    meter=Meter('packet_geometry')
    s=json.loads((ROOT/'SOURCE_WITNESSES.json').read_text())[0]
    row=json.loads((ROOT/'WIDTH_RESULTS.json').read_text())[0]
    h=s['target_consumer'];target=s['operations'][h-1][1]
    demands=[e for e in row['original_R_star'] if e['consumer']==h]
    ps=sorted({tuple(e['original_parent']) for e in demands})
    gs=[row['original_U'][str(p)]['g'] for p in ps]
    a=FullTree(s['initial_A']);b=FullTree(s['initial_B']);transfers=[];demotions=[]
    old_rotate=FullTree.rotate;current={};geometry={}
    def tracked(tree,u,side,other,actor):
        before=set(tree.path(target));current['bit_number']+=1;k=current['bit_number']
        eid=[actor,current['t'],(k+1)//2,(k-1)%2]
        out=old_rotate(tree,u,side,other,actor)
        after=set(tree.path(target))
        if actor=='A' and u in gs:demotions.append({'actual_bit':eid,'pivot':u})
        for g in gs:
            was=g in before and g!=target;now=g in after and g!=target
            if was!=now:transfers.append({'actual_bit':eid,'old_g':g,'target':target,
                'ancestor_before':was,'ancestor_after':now,'pivot':u})
        return out
    FullTree.rotate=tracked
    try:
        for t,(tag,x) in enumerate(s['operations'],1):
            current.update(t=t,bit_number=0)
            if t==h:
                geometry={'pre_A_path':a.path(x),'pre_B_path':b.path(x),'target':x,
                    'A_components_at_old_grandparents':[
                        {'g':g,'complete_key_interval':[a.lo[g],a.hi[g]],
                         'complete_internal_children':{str(k):[a.l[k] or None,a.r[k] or None] for k in range(a.lo[g],a.hi[g]+1)}} for g in gs]}
                for p,g in zip(ps,gs):assert geometry['pre_B_path'][-1-2*p[1]]==g
            a.splay(x,b,'A');current['bit_number']=0
            if tag=='K':b.splay(x,a,'B')
        assert a.state()==s['initial_A'] and b.state()==s['initial_B']
    finally:FullTree.rotate=old_rotate
    write('PACKET_GEOMETRY.json',{'source':s['name'],'critical_original_rhos':demands,
        'critical_physical_geometry':geometry,'exact_cyclic_g_to_target_ancestry_transfers':transfers,
        'all_actual_A_demotion_bits_at_these_g':demotions,
        'scope':'Original R_star packet, before F/E_old/hybrid. These are diagnostic complete physical lifecycles, not extra A credit.',
        'complete_physical_closure_verified':True})
    print('PASS distinct original grandparents on exact pre-B path; full cyclic ancestry transfers saved',flush=True)
    meter.success=True
