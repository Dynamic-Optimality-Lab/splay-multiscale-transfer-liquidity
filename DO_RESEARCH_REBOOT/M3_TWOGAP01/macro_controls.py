"""Two-gap DELETE/zero-charge KEEP source controls for the normal-form proof."""
import sys,json,time,importlib.util
from pathlib import Path
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_TWOGAP01','DO_RESEARCH_REBOOT/M3_OUT01','DO_RESEARCH_REBOOT/M3_GAPINT01']
from prefix_profiles import BASE,normalize
from candidate import TwoGapCandidate
import interior_original as IN
import outside_original as OUT
spec=importlib.util.spec_from_file_location('twogap_controls_local',BASE/'original_controls.py');TC=importlib.util.module_from_spec(spec);spec.loader.exec_module(TC)
def main():
    start=time.process_time();out=BASE/'macro_controls.json';assert not out.exists();P=TwoGapCandidate()
    c=json.loads((BASE/'relation.json').read_text());old=json.loads((BASE/'original_controls.json').read_text())['records']
    d=IN.DAG();L=IN.build_slow(d,'MXL');records=[]
    for H,w in ((1,-1),(2,1)):
        r=next(r for r in old if r.get('H')==H and r.get('w')==w and r.get('ghost_pairs'))
        a=r['prefix_source_class'];b=r['prefix_destination_class'];o=next(o for o in c['options'][a] if o['H']==H and o['destination']==b and o['target']==r['destination']['alpha'][0][2])
        wit=c['witnesses'][o['witness']];A,cuts,ghosts=TC.expand(wit['tree']);B=IN.V.from_serial(r['B_source_codes'])
        targets=wit['targets'];word=[['D',targets[0]],['K',targets[0]]]+[['K',x] for x in targets[1:]]
        helper=OUT if H==1 else IN;Ad,Bd,rr=helper.low(d,L,A,B,cuts,word,f'whole_H{H}_DELETE_KEEP_normalization',r['source']['mu'])
        e=rr['environment'];am=helper.model(A,cuts);slots={v['key']:i for i,v in am.slots.items()}
        for k,side in ghosts:
            i=slots[k];e[f'MXLw_k{"l" if side==0 else "r"}{i}']=0;e[f'MXLw_c{"l" if side==0 else "r"}{i}']=255
        ww=IN.exact_witness(e);st=IN.AState(IN.ED,ww);sa=IN.alpha_prefix(ww,st)
        for j in range(len(word)):st=IN.splay_event(IN.ED,ww,st,j,IN.Box(True))
        ta=IN.alpha_prefix(ww,st)
        for state,obj,alpha in ((rr['source'],L['s'],sa),(rr['destination'],L['t'],ta)):
            state['alpha']=alpha
            for i,(k,s,x) in enumerate(alpha):IN.V.put(d,e,obj.ak[i],k);IN.V.put(d,e,obj.aS[i],bool(s));IN.V.put(d,e,obj.aI[i],x)
        assert d.ev_ground(L['root'],e)
        assert normalize(sa)==tuple(map(tuple,c['shadows'][a])) and normalize(ta)==tuple(map(tuple,c['shadows'][b]))
        assert rr['H']==r['H'] and rr['q']==r['q'] and rr['w']==r['w']
        js=P.ordinary_J(rr['source'])['value'];jt=P.ordinary_J(rr['destination'])['value'];assert w-jt+js>=0
        rr.update(J_source=js,J_destination=jt,residual=w-jt+js,zero_charge_event_depth=rr['A_paths'][1]['d'],original_root=True)
        assert rr['A_paths'][1]['d']==0;records.append(rr)
    result={'status':'FULL_ORIGINAL_MACRO_NORMALIZATION_CONTROLS_PASS','full_roots':2,'DAG_nodes':len(d.nodes),
      'unchanged_H_q_weight_and_shared_profile':True,'cpu_seconds':round(time.process_time()-start,3),'records':records}
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,separators=(',',':'))
    print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2),flush=True)
if __name__=='__main__':main()
