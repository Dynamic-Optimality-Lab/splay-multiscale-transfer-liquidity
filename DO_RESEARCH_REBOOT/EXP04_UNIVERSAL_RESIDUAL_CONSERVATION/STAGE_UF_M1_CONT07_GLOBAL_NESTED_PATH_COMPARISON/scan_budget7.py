from base7 import *
from catalog7 import known_inputs
from global7 import fresh_sources

if __name__=='__main__':
    unsealed();m=Meter('non_U_scan_class_budget');entries=known_inputs();work={z['source']:z for z in load(ROOT/'INHERITED_PATH_WORKLOADS.json')}
    for i,s in enumerate(fresh_sources()):
        entries.append({'source':s,'physical':str(ROOT/f'FRESH_PHYS_{i:02}.json')});work[s['name']]=load(ROOT/f'FRESH_RESULT_{i:02}.json')
    out=[]
    for e in entries:
        z=work[e['source']['name']];b=load(e.get('birth',e['physical'].replace('PHYS','BIRTH')));U={ast.literal_eval(v) for v in b['U']}
        outside=z['Q_B']-len(U);assert outside>=0 and outside<=12*z['A'];uses=Counter();hitU=[];hitNon=[]
        for path in z['maximal_PF_paths']:
            for eid in path['unique_original_inside_pivot_bits']:
                v=tuple(eid[1:3]);uses[v]+=1
                (hitU if v in U else hitNon).append(eid)
        assert max(uses.values(),default=0)<=2 and len(hitNon)<=2*outside<=24*z['A']
        out.append({'source':z['source'],'source_sha256':digest(e['source']),'original_non_U_doubles':outside,'inherited_non_U_bound_12A':12*z['A'],
            'canonical_inside_U_pivot_bits':hitU,'canonical_inside_non_U_pivot_bits':hitNon,
            'M_hit_U':len(hitU),'M_hit_non_U':len(hitNon),'proved_non_U_scan_budget_24A':24*z['A'],
            'maximum_hits_per_original_double':max(uses.values(),default=0)})
    write('NON_U_SCAN_BUDGET_AUDIT.json',out);m.info['full_original_native_sources']=len(out);m.ok=True
    print('PASS exact U/non-U scan partition and24A exception budget on',len(out),'native sources',flush=True)
