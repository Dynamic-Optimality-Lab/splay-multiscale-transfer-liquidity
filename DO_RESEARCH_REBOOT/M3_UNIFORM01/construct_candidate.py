"""Exact F(psi): ONE cheap-edge pass, no propagation queue or fitted labels."""
import json,sys,time,hashlib
from pathlib import Path
BASE=Path(__file__).resolve().parent
CASES=['s4100000000','s3110000000','s0311000000']
INDEX=int(sys.argv[1]);CAP=min(120,float(sys.argv[2]));OUT=BASE/f'case_{INDEX:03d}'
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    OUT.mkdir(exist_ok=False);start=time.process_time();source=BASE.parent/'M3_POP5_RISK01'/CASES[INDEX]
    c=read(source/'relation.json');B=read(BASE.parent/'M3_UNITPAIR01/B_bank.json');N=c['classes'];psi=B['psi']
    assert c['queries']<=2000000 and c['option_count']<5000000
    roots={r:[] for r in range(9)}
    for ai,a in enumerate(c['shadows']):roots[a[0][2]].append(ai)
    values={};attain={};visits=updates=peak=0
    def guard():
        nonlocal peak
        live=N+c['option_count']+len(values)+len(attain);peak=max(peak,live)
        assert live<2000000,'UNKNOWN live record cap'
        assert time.process_time()-start<CAP,'UNKNOWN one-step construction CPU cap'
    for b,t in enumerate(B['trees']):
        if psi[b]==0:continue
        transfers={}
        for x in range(9):
            dep=B['depths'][b][x];w=2-dep//2;bb=B['destinations'][b][x]
            if dep and w in (0,1) and psi[b]-w>psi[bb]:transfers[1,x,None]=(bb,w)
            for gap in (0,9):
                pair=B['kernels'][str(gap)][b][x]
                if c['sigma'][gap] and pair is not None:
                    bb,w=pair
                    if w in (0,1) and psi[b]-w>psi[bb]:transfers[2,x,gap]=(bb,w)
        if transfers:
            for a in roots[t[0]]:
                for oi,(H,x,aa,gap,fi,code) in enumerate(c['options'][a]):
                    pair=transfers.get((H,x,gap))
                    if pair is None:continue
                    bb,w=pair;visits+=1;key=bb*N+aa;alt=psi[b]-w
                    if alt>values.get(key,psi[bb]):
                        assert psi[bb]<alt<=2;values[key]=alt;attain[key]=[b,a,oi];updates+=1
                    if visits%10000==0:guard()
        guard()
    write(OUT/'candidate.json',{'sigma':c['sigma'],'N':N,'default':'psi(B)','values':values,'attainment':attain})
    report={'status':'ONE_STEP_CANDIDATE_CONSTRUCTED_UNAUDITED','case':CASES[INDEX],'source_folder':source.as_posix(),'sigma':c['sigma'],'classes':N,'exception_values':len(values),'seed_transport_visits':visits,'strict_updates':updates,'peak_conservative_live_records':peak,'saved_canonical_queries_reused':c['queries'],'new_source_transition_queries':0,'no_fixed_point_iterations':True,'CPU_cap':CAP,'CPU_seconds':time.process_time()-start,'candidate_sha256':hashlib.sha256((OUT/'candidate.json').read_bytes()).hexdigest(),'uniform_closure_proved':False}
    write(OUT/'construction.json',report);print(json.dumps(report),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error={'type':type(e).__name__,'message':str(e)};raise
    finally:
        OUT.mkdir(exist_ok=True)
        write(OUT/'construct_exit.json',{'whole_process_CPU_seconds':time.process_time(),'CPU_cap':CAP,'error':error})
