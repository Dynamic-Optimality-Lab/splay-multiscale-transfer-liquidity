"""Two full original witnesses refute literal port-inventory determinacy at sigma0=2."""
import sys,json,time,copy
from pathlib import Path
sys.path.insert(0,'DO_RESEARCH_REBOOT/M3_ACL01')
from original_controls import S,V,DAG,build_slow,low
BASE=Path('DO_RESEARCH_REBOOT/M3_SIG02')

def main():
    out=BASE/'obstruction.json';assert not out.exists();start=time.process_time();V.start=start;V.MU=341
    d=DAG();L=build_slow(d,'MXL');assert len(d.nodes)<4000000
    z=S.LEAF;tail=S.node(2,S.node(1,z,z),S.balanced(range(3,9)))
    aa=S.node(0,S.node(-2,z,S.node(-1,z,z)),tail)
    ab=S.node(0,S.node(-1,S.node(-2,z,z),z),tail)
    B=S.node(0,S.node(-1,z,z),S.node(8,S.node(6,S.node(4,
      S.node(2,S.node(1,z,z),S.node(3,z,z)),S.node(5,z,z)),S.node(7,z,z)),z))
    records=[]
    for A,f,label in ((aa,-2,'anonymous_is_lower_key'),(ab,-1,'anonymous_is_upper_key')):
        ac,bc,r=low(d,L,A,B,[(f,0),(f,1)],[['K',2]],label)
        assert r['source']['sigma']==[2]+[0]*9 and r['H']==1 and r['q']==2 and r['w']==0
        r['literal_completed_source_alpha']=V.shadow(A);r['literal_completed_destination_alpha']=V.shadow(ac)
        r['two_frontier_bills']=[v['population'][0] for v in sorted(r['port_inventory'],key=lambda v:v['side']) if v['slot']==1]
        assert len(r['two_frontier_bills'])==2
        records.append(r);print(json.dumps({'label':label,'root':True,'q':r['q'],'w':r['w'],'bills':r['two_frontier_bills']}),flush=True)
        assert time.process_time()-start<300
    a,b=records
    assert a['source']==b['source'] and a['destination']==b['destination']
    assert a['source']!=a['destination']
    assert a['literal_completed_source_alpha']!=b['literal_completed_source_alpha']
    assert a['two_frontier_bills']==[0,1] and b['two_frontier_bills']==[1,0]
    faults=[]
    for r in records:
        e=dict(r['environment']);p=next(v for v in r['port_inventory'] if v['population'][0]==1)
        key=f'MXLv_z0_{p["slot"]}_{p["side"]}';e[key]=2
        assert not d.ev_ground(L['root'],e);faults.append({'label':r['label'],'mutation':key,'wrong_total_root':False})
    res={'status':'REFUTED_EXACT_LITERAL_INVENTORY_DETERMINACY','scope':{'mu':341,'sigma':[2]+[0]*9,'chi8':True},
      'original_roots':2,'same_full_source_state':True,'same_full_destination_state':True,
      'different_literal_port_contents':True,'different_literal_completed_source_alpha':True,
      'source_equals_destination':False,'low_DAG_nodes':len(d.nodes),'invalid_population_controls':faults,
      'counterexample_to_M3':False,'negative_cycle_certified':False,'all_mask_signature_theorem':'OPEN',
      'cpu_seconds':round(time.process_time()-start,3),'records':records}
    with out.open('x',encoding='utf-8') as f:json.dump(res,f,indent=2)
    print(json.dumps({k:v for k,v in res.items() if k!='records'}),flush=True)
if __name__=='__main__':main()
