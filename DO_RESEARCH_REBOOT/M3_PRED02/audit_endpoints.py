"""Direct independent point evaluation with stdlib dictionaries, not stream flags."""
import json,sys,time,hashlib
from pathlib import Path
BASE=Path(__file__).resolve().parent;CAP=min(300,float(sys.argv[1]));OUT=BASE/'case_000'
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def freeze(v):return tuple(map(freeze,v)) if isinstance(v,list) else v
def mirror(a):return tuple((k,iss,8-v if k==0 and iss else v) for i in (0,2,1,6,5,4,3) for k,iss,v in [a[i]])
def main():
    start=time.process_time();r=read(OUT/'obstruction.json');config=read(BASE/'config.json');B=read(BASE.parent/'M3_UNITPAIR01/B_bank.json');psi=B['psi'];entries=[e for e in read(Path(config['basis_path']))['entries'] if all(a<=b for a,b in zip(e['actual_sigma'],r['sigma']))]
    src=freeze(r['source_alpha']);dst=freeze(r['destination_alpha']);details=[];ds=psi[r['source_B']];dt=psi[r['destination_B']]
    for e in entries:
        folder=Path(e['folder']);m=read(folder/'metadata.json');p=read(folder/'potential.json');N=m['classes'];assert p['N']==N
        sh=[freeze(a) for a in m['shadows']];s=mirror(src) if e['reflected'] else src;t=mirror(dst) if e['reflected'] else dst
        ai=next((i for i,a in enumerate(sh) if a==s),None);aa=next((i for i,a in enumerate(sh) if a==t),None)
        b=B['mirror'][r['source_B']] if e['reflected'] else r['source_B'];bb=B['mirror'][r['destination_B']] if e['reflected'] else r['destination_B']
        sv=psi[b] if ai is None else -p['values'].get(str(b*N+ai),-psi[b]);tv=psi[bb] if aa is None else -p['values'].get(str(bb*N+aa),-psi[bb]);ds=max(ds,sv);dt=max(dt,tv)
        details.append({'tau':e['actual_sigma'],'source_class':ai,'destination_class':aa,'source_debt':sv,'destination_debt':tv,'source_pattern_attains_two':sv==2,'folder':folder.as_posix()})
        del m,p,sh
    H,x,aa,g,fi,code=r['option'];assert H==1 and g is None;bd=B['depths'][r['source_B']][x];bb=B['destinations'][r['source_B']][x];w=2-bd//2
    assert bb==r['destination_B'] and w==r['weight'] and (ds,dt)==(r['source_debt'],r['destination_debt'])==(2,0) and w+dt-ds==-1
    source=BASE.parent/'M3_POP5_RISK01/s3110000000';old=read(source/'potential.json');N=old['N'];js=old['values'].get(str(r['source_B']*N+r['source_A']),-psi[r['source_B']]);jt=old['values'].get(str(r['destination_B']*N+r['destination_A']),-psi[r['destination_B']]);assert w-jt+js>=0
    report={'status':'INDEPENDENT_DIRECT_THRESHOLD_ENDPOINT_OBSTRUCTION_VERIFIED','streaming_parser_used':False,'candidate_label_file_used':False,'construction_imported':False,'sigma':r['sigma'],'eligible_basis_evaluations':details,'source_psi':psi[r['source_B']],'destination_psi':psi[r['destination_B']],'source_debt':ds,'destination_debt':dt,'weight':w,'B_depth':bd,'target':x,'candidate_residual':w+dt-ds,'old_certified_J_source':js,'old_certified_J_destination':jt,'old_certified_residual':w-jt+js,'destination_absent_from_all_eligible_total4_class_banks':all(e['destination_class'] is None for e in details),'source_visible_F':sum(k==0 and not iss for k,iss,v in src),'destination_visible_F':sum(k==0 and not iss for k,iss,v in dst),'original_realizability':'AWAITING_ORIGINAL_LOW_WITNESS','negative_cycle_certified':False,'CPU_seconds':time.process_time()-start,'CPU_cap':CAP}
    assert report['CPU_seconds']<CAP;write(BASE/'endpoint_audit.json',report);print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error={'type':type(e).__name__,'message':str(e)};raise
    finally:write(BASE/'audit_endpoints_exit.json',{'whole_process_CPU_seconds':time.process_time(),'CPU_cap':CAP,'error':error})
