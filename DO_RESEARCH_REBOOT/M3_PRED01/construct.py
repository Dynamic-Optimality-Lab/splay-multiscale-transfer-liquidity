"""Explicit current-state patterns with certified population thresholds."""
import json,sys,time,hashlib
from pathlib import Path
BASE=Path(__file__).resolve().parent;INDEX=int(sys.argv[1]);CAP=min(120,float(sys.argv[2]));OUT=BASE/f'case_{INDEX:03d}'
CASES=['s4100000000','s3110000000','s0311000000','s0004001000']
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def freeze(x):return tuple(map(freeze,x)) if isinstance(x,list) else x
def reflect(a):return tuple((k,iss,8-v if k==0 and iss else v) for j in (0,2,1,6,5,4,3) for k,iss,v in [a[j]])
def main():
    OUT.mkdir(exist_ok=False);start=time.process_time();source=BASE.parent/'M3_POP5_RISK01'/CASES[INDEX];c=read(source/'relation.json');B=read(BASE.parent/'M3_UNITPAIR01/B_bank.json');basis=read(BASE/'basis.json');N=c['classes'];psi=B['psi'];sig=c['sigma']
    assert c['queries']<=2000000 and c['option_count']<5000000
    if INDEX<3:assert read(source/'audit.json')['status']=='INDEPENDENT_RISK_PREFIX_AND_RESIDUAL_PASS'
    sid={freeze(a):i for i,a in enumerate(c['shadows'])};assert len(sid)==N
    chosen=[e for e in basis['entries'] if all(a<=b for a,b in zip(e['actual_sigma'],sig))];assert chosen
    values={};visits=matches=peak=0;deps=[]
    def guard(extra=0):
        nonlocal peak
        peak=max(peak,2*N+c['option_count']+len(values)+extra+705)
        assert peak<2000000,'UNKNOWN live pattern-construction record cap'
        assert time.process_time()-start<CAP,'UNKNOWN pattern construction CPU cap'
    for ei,e in enumerate(chosen):
        folder=Path(e['folder']);m=read(folder/'metadata.json');p=read(folder/'potential.json');smallN=m['classes'];assert p['N']==smallN and p['default']=='-psi(B)'
        sh=list(map(freeze,m['shadows']));mapping=[sid.get(reflect(a) if e['reflected'] else a) for a in sh]
        for key,j in p['values'].items():
            b,a=divmod(int(key),smallN);bb=B['mirror'][b] if e['reflected'] else b;aa=mapping[a];visits+=1
            if aa is not None:
                debt=-j;assert psi[bb]<debt<=2
                k=bb*N+aa
                if debt>values.get(k,psi[bb]):values[k]=debt;matches+=1
            if visits%8192==0:guard(2*smallN+len(p['values']))
        guard(2*smallN+len(p['values']))
        deps.append({**e,'metadata_sha256':sha(folder/'metadata.json'),'potential_sha256':sha(folder/'potential.json'),'basis_changed_patterns':len(p['values'])})
        del m,p,sh,mapping
    write(OUT/'candidate.json',{'N':N,'sigma':sig,'scope':'values on this saved relation class bank only; global formula is the threshold envelope','default_on_catalog':'psi(B)','values':values})
    regression=None
    if INDEX==0:
        old=read(BASE.parent/'M3_ROW_AUD01/certificate.json');ds=values.get(1647*N+2073,psi[1647]);dt=values.get(2403*N+2072,psi[2403]);regression={'source_debt':ds,'destination_debt':dt,'residual':1+dt-ds,'original_edge_reused':True,'original_root_replayed':False}
    report={'status':'POPULATION_THRESHOLD_PREDICATES_CONSTRUCTED_UNAUDITED','source_folder':source.as_posix(),'case':CASES[INDEX],'sigma':sig,'N':N,'eligible_total4_signatures':len(chosen),'basis_dependencies':deps,'changed_pattern_states':len(values),'P1_new_patterns':sum(psi[k//N]<1<=v for k,v in values.items()),'P2_new_patterns':sum(psi[k//N]<2<=v for k,v in values.items()),'basis_pattern_visits':visits,'candidate_max_updates':matches,'peak_conservative_records':peak,'original_plus1_regression':regression,'canonical_source_profiles_reused':c['queries'],'new_source_transition_queries':0,'new_case_source_coverage_reused':INDEX<3,'unpromoted_stress_input':INDEX==3,'CPU_seconds':time.process_time()-start,'CPU_cap':CAP,'relation_sha256':sha(source/'relation.json'),'candidate_sha256':sha(OUT/'candidate.json'),'uniform_preservation_proved':False}
    assert report['CPU_seconds']<CAP;write(OUT/'construction.json',report);print(json.dumps({k:v for k,v in report.items() if k!='basis_dependencies'},indent=2),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error={'type':type(e).__name__,'message':str(e)};raise
    finally:
        OUT.mkdir(exist_ok=True);write(OUT/'construct_exit.json',{'whole_process_CPU_seconds':time.process_time(),'CPU_cap':CAP,'error':error})
