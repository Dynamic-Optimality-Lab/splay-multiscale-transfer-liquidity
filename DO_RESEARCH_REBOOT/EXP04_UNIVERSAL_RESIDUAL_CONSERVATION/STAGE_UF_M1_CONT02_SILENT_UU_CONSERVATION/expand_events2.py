"""Lossless original-event decoder and read-only expansion audit.

Use --jsonl PATH to materialize every original long-source primitive.
No output file is needed for --audit; full source and short full states remain pinned.
"""
from base2 import *
import gc

def expanded(short,rule):
    lo,hi=rule['template_primitive_slice_zero_based'];T=rule['copies_in_long'];start=rule['template_original_operations'][0]
    yield from short['events'][:lo]
    for c in range(T):
        for e in short['events'][lo:hi]:
            z={**e,'id':list(e['id']),'time':e['time']+4*c};z['id'][1]+=2*c;yield z
    for e in short['events'][hi:]:
        z={**e,'id':list(e['id']),'time':e['time']+4*(T-1)};z['id'][1]+=2*(T-1);yield z

if __name__=='__main__':
    assert sys.argv[1:]==['--audit'] or len(sys.argv)==3 and sys.argv[1]=='--jsonl'
    meter=Meter('expanded_original_event_audit') if sys.argv[1]=='--audit' else None
    s=load(ROOT/'BOOST_SOURCE_CATALOG.json')[1];p=load(ROOT/'BOOST_SHORT_PHYS.json');rule=load(ROOT/'BOOST_EVENT_EXPANSION.json')
    assert digest(s)==rule['long_source_sha256']
    sink=open(sys.argv[2],'w',encoding='utf-8') if sys.argv[1]=='--jsonl' else None
    sha=hashlib.sha256();count=0;Asteps=set();Bdouble=set();sign=Counter();lastt=0
    for e in expanded(p,rule):
        count+=1;assert e['time']==count
        actor,h,j,bit=e['id'];tag,x=s['operations'][h-1]
        assert e['actor']==actor and e['target']==x and (actor=='A' or tag=='K')
        assert h>=lastt;lastt=h
        if actor=='A':Asteps.add((h,j))
        elif e['case']!='ZIG':Bdouble.add((h,j))
        sign[actor,e['sign']]+=1
        line=json.dumps(e,sort_keys=True,separators=(',',':'))+'\n';sha.update(line.encode())
        if sink:sink.write(line)
    if sink:sink.close()
    assert len(Asteps)==s['expected_A']
    result=load(ROOT/'BOOST_RESULTS.json')['long'];assert len(Bdouble)==result['Q_B']
    assert sign['B',-1]==sign['A',1]-sign['A',-1]
    if meter:
        write('EXPANDED_EVENT_AUDIT.json',{'source_sha256':digest(s),'event_JSONL_sha256':sha.hexdigest(),
            'original_primitives':count,'real_A_StepEv':len(Asteps),'original_B_doubles':len(Bdouble),
            'signed_counts':{str(k):v for k,v in sign.items()},
            'every_decoded_original_event_id_target_time_checked':True,
            'full_tree_scope':'Full independent short replay plus exact complete-state identity template and whole-long-word fast incremental physical replay.',
            'full_long_native_Pi_R_star_rerun':False});meter.ok=True
    print('PASS lossless original-event expansion',count,'primitives; A',len(Asteps),'Q',len(Bdouble),flush=True)
