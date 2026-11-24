from base1 import *
from physical1 import analyze
import gc

if __name__=='__main__':
    meter=Meter('historical_physical_audit');out=[]
    cat=load(M0/'SOURCE_CATALOG.json')
    for i,z in enumerate(cat):
        s=z['source'];phys=load(M0/f'PHYS_{i:02}.json');forest=load(M0/f'FOREST_{i:02}.json');weights=load(M0/f'WEIGHTS_{i:02}.json')
        assert digest(s)==z['source_sha256']==phys['source_sha256']
        result=analyze(s,phys,forest,weights)
        write(f'HISTORICAL_AUDIT_{i:02}.json',result)
        out.append({'index':i,'source':s['name'],'source_sha256':digest(s),'audit_file':f'HISTORICAL_AUDIT_{i:02}.json',
            **{k:v for k,v in result.items() if k in ('A','Q_B','Z_B','flux_totals','C_parent_count','maximum_C_chain_edges','actual_R_C','actual_R_P')},
            'max_C_fringe_distance':max((v['distance'] for v in result['C_fringe_depths']),default=0),
            'radius2_physical_C_count':result['bounded_fringe_payments'][1]['selected_physical_C_parents'],
            'max_C_ticket_load_per_B_gain':max((v['physical_C_ticket_count'] for v in result['restoration_packets']),default=0)})
        write('HISTORICAL_RESULTS.json',out)
        print('PASS historical',i,s['name'],'C',result['C_parent_count'],'chain',result['maximum_C_chain_edges'],flush=True)
        del phys,forest,weights,result;gc.collect()
    meter.info.update(controls=len(out));meter.ok=True
