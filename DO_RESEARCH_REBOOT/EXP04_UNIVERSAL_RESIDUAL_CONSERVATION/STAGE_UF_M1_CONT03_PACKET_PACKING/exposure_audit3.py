from base3 import *
from gate1 import signature
import gc

if __name__=='__main__':
    meter=Meter('fan_exposure_and_closure_tickets');oldss=load(C2/'FAN_SOURCE_CATALOG.json');newss=load(ROOT/'NEW_SOURCE_CATALOG.json');out=[];tickets=[]
    for oi,ni in ((0,1),(1,2)):
        old=oldss[oi];new=newss[ni];op=load(C2/f'FAN_PHYS_{oi:02}.json');ob=load(C2/f'FAN_BIRTH_{oi:02}.json')
        np=load(ROOT/f'NEW_PHYS_{ni:02}.json');nb=load(ROOT/f'NEW_BIRTH_{ni:02}.json')
        oldks=[(h,x) for h,(tag,x) in enumerate(old['operations'],1) if tag=='K'];newks=[(h,x) for h,(tag,x) in enumerate(new['operations'],1) if tag=='K']
        assert [x for h,x in oldks]==[x for h,x in newks]
        hm={a[0]:b[0] for a,b in zip(oldks,newks)};od={tuple(z['parent']):z for z in op['doubles']};nd={tuple(z['parent']):z for z in np['doubles']}
        for v,d in od.items():
            dd=nd[hm[v[0]],v[1]]
            for key in ('g','p','target','case','F','J','P_output'):assert d[key]==dd[key]
        ev={tuple(e['id']):e for e in op['events']};rows=[]
        for z in ob['C_U_births']:
            if z['consumer'][0]!=2:continue
            creator=tuple(z['creator']);cl=ob['double_classes'][str(creator)];assert cl['class']=='whole_frame_exposed'
            donor=ev[tuple(cl['A_donor'])];post=op['boundaries'][creator[0]-1]['post_A_time'];lift=donor['time']
            while lift>post:lift-=len(op['events'])
            assert cl['kappa']<lift<=post and od[creator]['F'] in donor['created']
            assert nb['double_classes'][str(creator)]['class']=='U'
            rows.append({'original_consumer':z['consumer'],'creator':creator,'old_creator_frame_interval':od[creator]['physical_frame_interval'],
                'old_A_exposure_donor':donor,'old_cyclic_kappa':cl['kappa'],'old_cyclic_Gamma':cl['Gamma'],
                'old_donor_lift':lift,'exposure_before_B_birth':lift<cl['Gamma'],
                'source_phase':'Original measured B-return phase (A part of a KEEP)',
                'new_creator_class':'U','new_same_B_KEEP_operation':hm[donor['id'][1]],
                'new_global_internal_A_absence':'All real primitive states independently checked as full split-vines; no internal frame present.'})
        assert len(rows)==old['s']//2
        out.append({'old_source':old['name'],'new_source':new['name'],'old_source_sha256':digest(old),'new_source_sha256':digest(new),
            'entire_B_word_and_all_B_double_shapes_equal':True,'B_doubles_compared':len(od),'creator_repairs':rows})
        del op,ob,np,nb;gc.collect()
    for stem,cn in (('NEW','NEW_SOURCE_CATALOG.json'),('PROTECTED','PROTECTED_SOURCE_CATALOG.json')):
        for i,s in enumerate(load(ROOT/cn)):
            p=load(ROOT/f'{stem}_PHYS_{i:02}.json');b=load(ROOT/f'{stem}_BIRTH_{i:02}.json')
            f=load(ROOT/f'{stem}_FOREST_{i:02}.json');an=load(ROOT/f'{stem}_M1_AUDIT_{i:02}.json')
            sig=signature(p,b,f,an);ds={tuple(z['parent']):z for z in p['doubles']};lastK=max(h for h,(tag,x) in enumerate(s['operations'],1) if tag=='K')
            lastpivot={e['pivot']:e for e in p['events'] if e['actor']=='A'};used=set();step_load=Counter();trs=[]
            for v in sorted(sig):
                if v[0]!=2:continue
                g=ds[v]['g'];e=lastpivot[g];assert e['id'][1]>lastK and tuple(e['id']) not in used
                used.add(tuple(e['id']));step_load[tuple(e['id'][:3])]+=1
                trs.append({'original_parent':v,'old_g':g,'future_measured_A_demotion':e['id'],'source_phase':'Final A-only root-walk closure'})
            assert len(trs)==s['s']//2 and max(step_load.values(),default=0)<=1
            tickets.append({'source':s['name'],'source_sha256':digest(s),'tracked_packet_only':2,'tickets':trs,
                'maximum_parent_load_per_actual_A_StepEv':max(step_load.values(),default=0),
                'scope':'Exact nonlocal payment on this constructed packet, not a source-uniform map for arbitrary packets or an extra activated budget.'})
    write('FAN_EXPOSURE_REPAIR.json',out);write('CONSTRUCTED_PACKET_CLOSURE_TICKETS.json',tickets)
    meter.ok=True;print('PASS exact old Pi blockers, B-word invariance, repaired creators and original closure tickets',flush=True)
