from base7 import *

def known_inputs():
    out=[]
    for i,z in enumerate(load(M0/'RESIDUAL_AUDIT.json')):
        if 'C_old' in z:
            s=load(M0/'SOURCE_CATALOG.json')[i]['source']
            out.append({'source':s,'physical':str(M0/f'PHYS_{i:02}.json'),'birth':str(C1/f'BIRTH_{i:02}.json'),'accounting':z,'origin':'M0_native'})
    for i,s in enumerate(load(C2/'RUN_B_SOURCE_CATALOG.json')[:3]):
        out.append({'source':s,'physical':str(C2/f'RUN_B_PHYS_{i:02}.json'),'accounting_path':str(C2/f'ORDERED_{i:02}.json'),'origin':'C2_native'})
    for root,stem in ((C3,'NEW'),(C3,'PROTECTED'),(C4,'DEFORM'),(C4,'SHARED'),(C5,'NEW'),(C5,'RENEW'),(C5,'FRINGE')):
        for i,s in enumerate(load(root/f'{stem}_SOURCE_CATALOG.json')):
            out.append({'source':s,'physical':str(root/f'{stem}_PHYS_{i:02}.json'),'accounting_path':str(root/f'{stem}_ORDERED_{i:02}.json'),'origin':root.name+'_'+stem})
    s=load(C4/'PROBE_SHORT_SOURCE.json')
    out.append({'source':s,'physical':str(C4/'PROBE_SHORT_PHYS.json'),'accounting_path':str(C4/'PROBE_SHORT_ORDERED.json'),'origin':'C4_short_native'})
    for i,s in enumerate(load(C6/'FRESH_SOURCE_CATALOG.json')):
        out.append({'source':s,'physical':str(C6/f'FRESH_PHYS_{i:02}.json'),'accounting_path':str(C6/f'FRESH_ORDERED_{i:02}.json'),'origin':'C6_native'})
    assert len(out)==48 and len({digest(e['source']) for e in out})==48
    return out

def accounting(e):return e['accounting'] if 'accounting' in e else load(e['accounting_path'])

def complete_controls():
    out=load(C5/'ALL_CONTROL_REFERENCES_FINAL.json')
    for i,s in enumerate(load(C6/'FRESH_SOURCE_CATALOG.json')):
        out.append({'source':s,'source_sha256':digest(s),'physical':str(C6/f'FRESH_PHYS_{i:02}.json'),
            'physical_sha256':hfile(C6/f'FRESH_PHYS_{i:02}.json'),'origin':'C6_native'})
    assert len(out)==110;return out
