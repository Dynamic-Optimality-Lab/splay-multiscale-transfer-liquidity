import sys,json,time,copy
from pathlib import Path
sys.path.insert(0,'DO_RESEARCH_REBOOT/M3_GAPINT01')
from interior_original import S,V,DAG,build_slow,low
from framework_v2 import rho
BASE=Path('DO_RESEARCH_REBOOT/M3_GAPMULTI01')
def main():
    out=BASE/'obstruction.json';assert not out.exists();start=time.process_time();d=DAG();L=build_slow(d,'MXL');z=S.LEAF
    right=S.balanced([16*k for k in range(3,9)])
    A0=S.node(32,S.node(-8,z,S.node(0,z,S.node(16,S.node(8,z,z),z))),right)
    A1=S.node(32,S.node(8,S.node(0,S.node(-8,z,z),z),S.node(16,z,z)),right)
    R=z
    for k in reversed(range(3,9)):R=S.node(16*k,z,R)
    B=S.node(32,S.node(0,z,S.node(16,z,z)),R);B=V.insert(V.insert(B,-8),8);records=[]
    for A,f,label in ((A0,-8,'visible_fringe_in_gap0'),(A1,8,'visible_fringe_in_gap1')):
        _,_,r=low(d,L,A,B,[(f,0),(f,1)],[['K',96]],label,341);assert r['source']['sigma']==[1,1]+[0]*8 and r['H']==1 and r['q']==2 and r['w']==0
        r['visible_fringe_gap']=0 if f==-8 else 1;r['fixed_gap0_image']=[list(q) for q in rho(r['source']['alpha'],0)];r['fixed_gap1_image']=[list(q) for q in rho(r['source']['alpha'],1)];records.append(r)
    a,b=records;assert a['source']==b['source'] and a['destination']==b['destination'];assert a['fixed_gap0_image']!=a['fixed_gap1_image']
    bills=[]
    for r in records:
        left=next(p for p in r['port_inventory'] if p['slot']==1 and p['side']==0);right=next(p for p in r['port_inventory'] if p['slot']==1 and p['side']==1)
        bills.append([left['hidden_S_indices'],right['hidden_S_indices']]);assert d.ev_ground(L['root'],r['environment'])
    assert bills==[[[],[0,1]],[[0],[1]]]
    result={'status':'REFUTED_EXACT_SHARED_PORT_CORE_SPLIT_DETERMINACY','mu':341,'sigma':[1,1]+[0]*8,
      'complete_original_roots':2,'independent_replays':2,'same_full_source_state':True,'same_full_destination_state':True,
      'hidden_core_bills':bills,'different_required_literal_core_completions':True,
      'negative_original_cycle_certified':False,'counterexample_to_M3':False,'DAG_nodes':len(d.nodes),
      'cpu_seconds':round(time.process_time()-start,3),'records':records}
    assert result['cpu_seconds']<300
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2),flush=True)
if __name__=='__main__':main()
