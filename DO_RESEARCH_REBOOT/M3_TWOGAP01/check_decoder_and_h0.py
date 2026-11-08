"""Exercise the usable decoder and retain the full original high h=0 case."""
import sys,json,time
from pathlib import Path
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_TWOGAP01','DO_RESEARCH_REBOOT/M3_OUT01','DO_RESEARCH_REBOOT/M3_GAPINT01','DO_RESEARCH_REBOOT/M2_SEP01']
from candidate import TwoGapCandidate,SIG
from prefix_profiles import BASE
import outside_original as O
from experiment import trace,FIELDS
from PC_B_CONTROLLER import BTrace,b_splay_event
def main():
    start=time.process_time();out=BASE/'decoder_and_h0.json';assert not out.exists();P=TwoGapCandidate()
    lows=json.loads((BASE/'original_controls.json').read_text())['records'];lowchecks=[]
    for r in lows:
        s=P.ordinary_J(r['source']);t=P.ordinary_J(r['destination']);assert s['value']==r['J_source'] and t['value']==r['J_destination']
        assert r['w']-P.ordinary(r['destination'])+P.ordinary(r['source'])==r['residual']
        lowchecks.append({'label':r['label'],'residual':r['residual']})
    d=O.DAG();H=O.build_shigh(d,'MXH');bt=BTrace(d,'MXHbt');replay=b_splay_event(d,H['s'].b,bt,0,d.const_bool(False))
    T=O.S.LEAF
    for k in range(9):T=O.S.node(16*k,T,O.S.LEAF)
    T=O.V.insert(O.V.insert(T,-8),8);source=O.bmodel(T);assert source['root']==8 and source['kr'][8]==2
    records=[]
    for v in (8,4):
        e=O.V.blank(d);mu=341;a=[[2,0,0] for _ in range(7)];a[0]=[2,1,8];ta=[list(x) for x in a];ta[0][2]=v
        _,_,path,dirs=trace(source,8,18);e['MXHbt_bT0']=8;e['MXHbt_bd0']=18
        for i,x in enumerate(path):e[f'MXHbt_bp0_{i}']=x
        for i,x in enumerate(dirs):e[f'MXHbt_bdir0_{i}']=x
        O.fill(d,e,H['s'],mu,SIG,source,a);O.V.aux(e,'MXHsbs',source)
        O.V.put(d,e,H['q'],9);O.V.put(d,e,H['w1'],-3)
        raw={'root':d.ev_ground(replay.root,e),**{f:[d.ev_ground(n,e) for n in getattr(replay,f)] for f in FIELDS[:4]}}
        dest={**source,**raw};assert raw['root']==8 and raw['kr'][8]==0 and raw['rr'][8]==19
        # Only ghost child pairs change: the proper B topology and intervals stay valid.
        O.fill(d,e,H['t'],mu,SIG,dest,ta);O.V.fillB(d,e,H['g'].b,dest)
        O.V.put(d,e,H['g'].mu,mu);O.V.put(d,e,H['g'].v,v)
        for var,x in zip(H['g'].sig,SIG):O.V.put(d,e,var,x)
        O.V.aux(e,'MXHsbt',dest);O.V.aux(e,'MXHsbg',dest);O.V.bounds(d,e);assert d.ev_ground(H['root'],e)
        s=O.state(mu,SIG,source,a);t=O.state(mu,SIG,dest,ta);m={'mu':mu,'sigma':SIG,'b':t['b'],'v':v}
        om=-3-P.midpoint(m)+P.ordinary(s);mo=-P.ordinary(t)+P.midpoint(m);assert om>=0 and mo>=0
        records.append({'kind':'HIGH','source':s,'destination':t,'shared_midpoint':m,'actual_depth':0,'declared_depth':18,
          'q':9,'w_OM':-3,'w_MO':0,'target':8,'fiber_v':v,'root_stays8':True,'enters_chi8':True,
          'OM_residual':om,'MO_residual':mo,'original_root':True,'environment':e})
    result={'status':'DECODER_AND_CORRECTED_HIGH_CONTROLS_PASS','low_decoder_checks':len(lowchecks),'low_checks':lowchecks,
      'full_original_high_roots':len(records),'h0_correction_retained':True,'independent_fiber_v_retained':True,
      'DAG_nodes':len(d.nodes),'cpu_seconds':round(time.process_time()-start,3),'records':records}
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,separators=(',',':'))
    print(json.dumps({k:v for k,v in result.items() if k not in ('records','low_checks')},indent=2),flush=True)
if __name__=='__main__':main()
