"""Full original low control for a zero-cost two-unit recurrence reset."""
import sys,json,time
from pathlib import Path
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_LDR01','DO_RESEARCH_REBOOT/M3_PHI01','python/independent']
import verify_full_mixed as V
from search_helpers import child_tree,step
from PC_TYPED_DAG import DAG
from STRICT_LOW_COMPILER import build_slow
OUT=Path('DO_RESEARCH_REBOOT/M3_LDR01/zero_reset_control.json')
def main():
    assert not OUT.exists();start=time.process_time();V.start=start
    c=json.loads(Path('DO_RESEARCH_REBOOT/M3_LDR01/negative_run_census.json').read_text())
    psi={V.from_serial(n['tree']):n['psi'] for n in c['nodes']};point=None
    for b,p in psi.items():
        if p!=2 or b[1] not in V.MARKED:continue
        for x in V.MARKED:
            h,bn=step(b,x)
            if h in (4,5) and psi[bn]==0:
                point=(child_tree(b[1],x),b,x,bn);break
        if point:break
    assert point,'No zero reset: this boundary candidate is unavailable'
    a,b,x,bn=point;d=DAG();L=build_slow(d,'MXL');assert len(d.nodes)<4000000
    _,actual,r=V.low(d,L,a,b,[('K',x)],True,'zero_reset_two_units')
    assert actual==bn and r['w']==0
    r.update(psi_source=2,psi_destination=0,Xi_change=2,Xi_edge_residual=-2)
    result={'status':'COMPLETE','queries':1,'low_DAG_nodes':len(d.nodes),
            'full_original_low_root':True,'Xi_global_extension_refuted':True,
            'cpu_seconds':round(time.process_time()-start,3),'record':r}
    assert result['cpu_seconds']<300
    with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='record'}),flush=True)
if __name__=='__main__':main()
