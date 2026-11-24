from base0 import *
from sources0 import controls
from model0 import replay,prefix_check
from independent0 import scan_forest,audit_forest,KINDS
from forest5 import forest as historical_forest
import gc

def normalize(old):
    ans={}
    for z in old['rows']:
        p=tuple(z['parent']);typ=KINDS[z['kind']]
        ans[p]={'type':typ,'predecessor':None if typ=='R' else tuple(z['predecessor'])}
        if typ=='R':ans[p]['A_donor']=tuple(z['A_bit'])
    return ans

if __name__=='__main__':
    meter=Meter('structural_audit');records=[];catalog=controls()
    write('SOURCE_CATALOG.json',catalog)
    for index,z in enumerate(catalog):
        s=z['source'];prefix=prefix_check(s);r,states=replay(s)
        old=historical_forest(r);candidate=normalize(old)
        independently=scan_forest(r);assert independently==candidate,s['name']
        checked=audit_forest(r,independently)
        N=len(r.ops);cuts=sorted({0,1%max(N,1),N//2,max(N-1,0)})
        for cut in cuts:assert scan_forest(r,cut)==independently,(s['name'],cut)
        write(f'PHYS_{index:02}.json',{'source':s['name'],'source_sha256':digest(s),
            'original_S':sorted(r.S),'original_genuine_M':sorted(r.M),
            'events':r.events,'doubles':[{'parent':p,**q} for p,q in sorted(r.doubles.items())],
            'boundaries':r.boundaries,'state_pool':states})
        vertices=[{'parent':p,**v} for p,v in sorted(independently.items())]
        write(f'FOREST_{index:02}.json',{'source':s['name'],'vertices':vertices,**checked})
        records.append({'source':s['name'],'source_sha256':digest(s),'physical_file':f'PHYS_{index:02}.json',
            'forest_file':f'FOREST_{index:02}.json','prefix_check':prefix,
            'A':r.A,'Q_B':r.Q,'original_operations':len(r.ops),'primitive_bits':r.T,
            'original_S_size':len(r.S),'original_genuine_support_size':len(r.M),
            'original_event_sha256':digest(r.events),'prior_event_sha256_matches':('trace_hash' in s),
            'independent_streaming_matches_historical':True,'cut_invariance_tested_at':cuts,**checked})
        write('STRUCTURAL_RESULTS.json',records)
        print('PASS',s['name'],'Q',r.Q,'roots',checked['root_count'],'types',checked['types'],flush=True)
        del r,states,old,candidate,independently,vertices;gc.collect()
    meter.info.update(controls=len(records));meter.ok=True
