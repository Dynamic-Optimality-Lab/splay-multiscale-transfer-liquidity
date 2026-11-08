"""Independent original-root replay of the old Q failures and a new invalid ref."""
import sys,json,time,copy
from pathlib import Path
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_AER01','DO_RESEARCH_REBOOT/M3_ACL01']
from empty_interval_potential import EmptyIntervalPotential
from original_controls import V,DAG,build_slow,exact_witness,AState,ED,alpha_prefix,splay_event,Box
BASE=Path('DO_RESEARCH_REBOOT/M3_AER01')
def main():
    out=BASE/'original_replay.json';assert not out.exists();start=time.process_time();d=DAG();L=build_slow(d,'MXL');P=EmptyIntervalPotential()
    c=json.loads(Path('DO_RESEARCH_REBOOT/M3_ACL_AUD02/dangling_audit.json').read_text());records=[]
    rows=copy.deepcopy(c['failures']);r=copy.deepcopy(rows[0]);rf='cl' if r['side']==0 else 'cr'
    r['ref']=128;r['environment'][f'MXLw_{rf}{r["slot"]}']=128;rows.append(r)
    for r in rows:
        e=r['environment'];w=exact_witness(e);st=AState(ED,w);sa=alpha_prefix(w,st)
        for j in range(e['MXLw_nev']):st=splay_event(ED,w,st,j,Box(True))
        ta=alpha_prefix(w,st);assert sa==r['source']['alpha'] and ta==r['destination']['alpha']
        V.bounds(d,e);assert d.ev_ground(L['root'],e)
        ps=P.inspect(r['source']);pt=P.inspect(r['destination']);v=r['w']+ps['value']-pt['value'];assert v>=0
        records.append({'ref':r['ref'],'root':True,'w':r['w'],'old_residual':r['residual'],'new_residual':v,
          'source':r['source'],'destination':r['destination'],'new_source':ps,'new_destination':pt,'environment':e})
    result={'status':'PASS','complete_original_roots':len(records),'refs':[r['ref'] for r in records],
      'old_minimum_residual':min(r['old_residual'] for r in records),'new_minimum_residual':min(r['new_residual'] for r in records),
      'DAG_nodes':len(d.nodes),'cpu_seconds':round(time.process_time()-start,3),'records':records}
    assert result['cpu_seconds']<300
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='records'}),flush=True)
if __name__=='__main__':main()
