"""A fully closed original mixed cycle with an observed fringe port on both high endpoints."""
import sys,json,time
sys.path.insert(0,'DO_RESEARCH_REBOOT/M3_G0P01')
from original_port_controls import S,V,DAG,build_slow,build_shigh,low,high,PortPotential,BASE
OUT=BASE/'visible_port_cycle.json'
def main():
    assert not OUT.exists();start=time.process_time();V.start=start;V.MU=341;P=PortPotential()
    z=S.LEAF;core=S.node(0,z,S.node(2,S.node(1,z,z),S.balanced(range(3,9))))
    A=V.insert(core,-1);B=A;d=DAG();L=build_slow(d,'MXL');dh=DAG();H=build_shigh(dh,'MXH')
    ac,bc,l=low(d,L,A,B,[['K',2]],'visible_port_cycle_low')
    h=high(dh,H,ac,bc,A,0,[1]+[0]*9,341,'visible_port_cycle_high')
    assert V.from_serial(h['B_destination'])==B
    h['source']['alpha']=l['destination']['alpha'];h['destination']['alpha']=l['source']['alpha'];env=h['environment']
    for tag,s in (('MXHs',h['source']),('MXHt',h['destination'])):
        for j,(k,ss,ii) in enumerate(s['alpha']):env[f'{tag}_ak{j}']=k;env[f'{tag}_aS{j}']=bool(ss);env[f'{tag}_aI{j}']=ii
    V.bounds(dh,env);assert dh.ev_ground(H['root'],env)
    records=[l,h]
    for r in records:
        a=P.inspect(r['source']);b=P.inspect(r['destination']);res=r['w']+a['port_joint']-b['port_joint'];assert res>=0
        r.update(potential_source=a,potential_destination=b,port_residual=res)
        assert any(row[0]==1 for row in r['source']['alpha']) and any(row[0]==1 for row in r['destination']['alpha'])
        if r['kind']=='HIGH':
            r.update(OM_reduced_weight=r['w']+a['port_joint'],MO_reduced_weight=-b['port_joint'])
            assert r['OM_reduced_weight']>=0 and r['MO_reduced_weight']>=0
    assert l['source']==h['destination'] and l['destination']==h['source']
    assert sum(r['w'] for r in records)==sum(r['port_residual'] for r in records)==8
    out={'status':'COMPLETE','controls':2,'low_DAG_nodes':len(d.nodes),'high_DAG_nodes':len(dh.nodes),
         'weight':8,'full_state_closure':True,'shared_midpoint':True,'visible_port_at_every_ordinary_vertex':True,
         'cpu_seconds':round(time.process_time()-start,3),'records':records}
    assert out['cpu_seconds']<300
    with OUT.open('x',encoding='utf-8') as f:json.dump(out,f,indent=2)
    print(json.dumps({k:v for k,v in out.items() if k!='records'},indent=2),flush=True)
if __name__=='__main__':main()
