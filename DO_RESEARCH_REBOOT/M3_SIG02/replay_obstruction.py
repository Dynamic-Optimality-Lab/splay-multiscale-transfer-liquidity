"""Independent complete-DAG replay; compare raw states, rather than a projected key."""
import sys,json,time,hashlib
from pathlib import Path
sys.path.insert(0,'DO_RESEARCH_REBOOT/M3_ACL01')
from original_controls import DAG,build_slow,S,V
BASE=Path('DO_RESEARCH_REBOOT/M3_SIG02')
def main():
    out=BASE/'audit.json';assert not out.exists();start=time.process_time();d=DAG();L=build_slow(d,'MXL')
    c=json.loads((BASE/'obstruction.json').read_text());aa,bb=c['records']
    for r in c['records']:
        assert d.ev_ground(L['root'],r['environment']);V.bounds(d,r['environment'])
        A=V.from_serial(r['A_source']);D=S.trace(A,2)[0]
        assert V.shadow(A)==r['literal_completed_source_alpha'] and V.serial(D)==r['A_destination']
        assert r['source']['b']['kr'][8]==0 and r['source']['b']['rr'][8]==19
        assert r['destination']['b']['kr'][8]==0 and r['destination']['b']['rr'][8]==19
    for field in ('mu','sigma','alpha','b'):
        assert aa['source'][field]==bb['source'][field] and aa['destination'][field]==bb['destination'][field]
    assert set(aa['source']['b'])=={'root','kl','rl','kr','rr','lo','hi'}
    a,b=aa['literal_completed_source_alpha'],bb['literal_completed_source_alpha'];different=[p for p in range(7) if a[p]!=b[p]]
    assert different==[3,4]
    res={'status':'PASS','original_low_roots_independently_replayed':2,'full_shared_fields_compared':True,
      'different_physical_source_positions':different,'bills':[aa['two_frontier_bills'],bb['two_frontier_bills']],
      'is_closed_walk':False,'is_M3_counterexample':False,'cpu_seconds':round(time.process_time()-start,3)}
    assert res['cpu_seconds']<300
    with out.open('x',encoding='utf-8') as f:json.dump(res,f,indent=2)
    print(json.dumps(res),flush=True)
if __name__=='__main__':main()
