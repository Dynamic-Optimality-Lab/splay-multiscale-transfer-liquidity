"""Same fixed predicate, with only streamed source pattern values resident."""
import json,sys,time,hashlib
from pathlib import Path
from stream_values import Values
BASE=Path(__file__).resolve().parent;INDEX=int(sys.argv[1]);CAP=min(120,float(sys.argv[2]));OUT=BASE/f'case_{INDEX:03d}'
BANK_RESERVE=300000;SCRATCH=8192
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def freeze(x):return tuple(map(freeze,x)) if isinstance(x,list) else x
def reflected(a):return tuple((kind,iss,8-k if kind==0 and iss else k) for j in (0,2,1,6,5,4,3) for kind,iss,k in [a[j]])
def main():
    OUT.mkdir(exist_ok=False);start=time.process_time();config=read(BASE/'config.json');case=config['cases'][INDEX];assert case['reused_input'] is None
    source=Path(case['source_folder']);status=read(source/'build_status.json');N=status['classes'];options=status['option_count']
    assert status['queries']<=2000000 and options<5000000
    assert 2*N+options+BANK_RESERVE+SCRATCH+705<2000000
    c=read(source/'relation.json');B=read(BASE.parent/'M3_UNITPAIR01/B_bank.json');psi=B['psi'];assert (c['classes'],c['option_count'])==(N,options)
    for i,a in enumerate(c['shadows']):c['shadows'][i]=freeze(a)
    aid={a:i for i,a in enumerate(c['shadows'])};sig=c['sigma'];basis=read(Path(config['basis_path']));assert sha(Path(config['basis_path']))==config['basis_sha256']
    eligible=[e for e in basis['entries'] if all(x<=y for x,y in zip(e['actual_sigma'],sig))];values={};deps=[];peak=0;visits=updates=0
    for e in eligible:
        folder=Path(e['folder']);smallN=read(folder/'build_status.json')['classes'];base=2*N+options+2*smallN+BANK_RESERVE+SCRATCH+705
        assert base+len(values)<2000000,'UNKNOWN planned construction live records'
        m=read(folder/'metadata.json');assert m['classes']==smallN
        routes=[aid.get(reflected(freeze(a)) if e['reflected'] else freeze(a)) for a in m['shadows']]
        with Values(folder/'potential.json') as reader:
            assert reader.header['N']==smallN
            for key,j in reader:
                b,a=divmod(key,smallN);bb=B['mirror'][b] if e['reflected'] else b;aa=routes[a];visits+=1
                if aa is not None:
                    debt=-j;assert psi[bb]<debt<=2;k=bb*N+aa
                    if debt>values.get(k,psi[bb]):
                        if k not in values:assert base+len(values)+1<2000000,'UNKNOWN construction live record cap'
                        values[k]=debt;updates+=1
                if visits%8192==0:assert time.process_time()-start<CAP,'UNKNOWN construction CPU cap'
            count=reader.count
        peak=max(peak,base+len(values));del m,routes
        deps.append({**e,'metadata_sha256':sha(folder/'metadata.json'),'potential_sha256':sha(folder/'potential.json'),'basis_changed_patterns':count})
    write(OUT/'candidate.json',{'N':N,'sigma':sig,'scope':'values on saved relation class bank; global formula remains PRED01 threshold envelope','default_on_catalog':'psi(B)','values':values})
    report={'status':'STREAMED_THRESHOLD_PREDICATE_CONSTRUCTED_UNAUDITED','source_folder':source.as_posix(),'case':case['name'],'sigma':sig,'N':N,'eligible_total4_signatures':len(eligible),'basis_dependencies':deps,'changed_pattern_states':len(values),'basis_pattern_visits':visits,'candidate_max_updates':updates,'peak_conservative_records':peak,'streamed_basis_values':True,'source_coverage_complete_reused':case['source_coverage_complete'],'new_source_transition_queries':0,'CPU_seconds':time.process_time()-start,'CPU_cap':CAP,'relation_sha256':sha(source/'relation.json'),'candidate_sha256':sha(OUT/'candidate.json'),'uniform_preservation_proved':False}
    assert report['CPU_seconds']<CAP;write(OUT/'construction.json',report);print(json.dumps({k:v for k,v in report.items() if k!='basis_dependencies'},indent=2),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error={'type':type(e).__name__,'message':str(e)};raise
    finally:
        OUT.mkdir(exist_ok=True);write(OUT/'construct_exit.json',{'whole_process_CPU_seconds':time.process_time(),'CPU_cap':CAP,'error':error})
