"""Adversarial original low witness mutations, with shadows derived afresh."""
import sys,json,time,copy
from pathlib import Path
sys.path.insert(0,'DO_RESEARCH_REBOOT/M3_ACL01')
from original_controls import V,DAG,build_slow,exact_witness,AState,ED,alpha_prefix,splay_event,Box,CompleteOneGapPotential
BASE=Path('DO_RESEARCH_REBOOT/M3_ACL_AUD02')
def main():
    out=BASE/'dangling_audit.json';assert not out.exists();start=time.process_time();d=DAG();L=build_slow(d,'MXL');P=CompleteOneGapPotential()
    c=json.loads(Path('DO_RESEARCH_REBOOT/M3_ACL01/original_controls.json').read_text());queries=0;accepted=[];rejected=0;fail=[]
    for r in c['records']:
        if r['kind']!='LOW' or r['unused_alpha_junk'] or r['B_padding_variant']:continue
        ee=r['environment']
        for i in range(127):
            if not ee[f'MXLw_p{i}']:continue
            for b,kf,rf in ((0,'kl','cl'),(1,'kr','cr')):
                if ee[f'MXLw_{kf}{i}']!=2:continue
                for ref in (127,255):
                    e=dict(ee);e[f'MXLw_{kf}{i}']=0;e[f'MXLw_{rf}{i}']=ref
                    w=exact_witness(e);st=AState(ED,w);sa=alpha_prefix(w,st)
                    for j in range(len(r['word'])):st=splay_event(ED,w,st,j,Box(True))
                    ta=alpha_prefix(w,st)
                    for tag,a in (('MXLs',sa),('MXLt',ta)):
                        for j,(kk,ss,ii) in enumerate(a):e[f'{tag}_ak{j}']=kk;e[f'{tag}_aS{j}']=bool(ss);e[f'{tag}_aI{j}']=ii
                    queries+=1;ok=d.ev_ground(L['root'],e)
                    if not ok:rejected+=1;continue
                    s=copy.deepcopy(r['source']);t=copy.deepcopy(r['destination']);s['alpha']=sa;t['alpha']=ta
                    ps=P.inspect(s);pt=P.inspect(t);res=r['w']+ps['value']-pt['value']
                    row={'seed':r['label'],'slot':i,'side':b,'ref':ref,'root':True,'source':s,'destination':t,
                      'H':r['H'],'q':r['q'],'w':r['w'],'potential_source':ps,'potential_destination':pt,'residual':res}
                    accepted.append(row)
                    if res<0 or len(accepted)==1:
                        row['environment']=e
                    if res<0:fail.append(row)
                    assert time.process_time()-start<300,'UNKNOWN audit cap'
    result={'status':'CLAIMED_Q_REFUTED_EXACT' if fail else 'AUDIT_COMPLETE',
      'queries':queries,'accepted':len(accepted),'rejected':rejected,'negative_residuals':len(fail),
      'minimum_residual':min((r['residual'] for r in accepted),default=None),
      'source_completeness_refuted':any(r['potential_source']['rule']=='invalid_low_shape_zero' or r['potential_destination']['rule']=='invalid_low_shape_zero' for r in accepted),
      'DAG_nodes':len(d.nodes),'cpu_seconds':round(time.process_time()-start,3),'failures':fail,'accepted_rows':accepted}
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k not in ('failures','accepted_rows')},indent=2),flush=True)
if __name__=='__main__':main()
