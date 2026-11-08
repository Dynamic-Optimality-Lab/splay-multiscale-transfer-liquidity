"""Metadata-only exact index of the completed total-four pattern basis."""
import json,sys,time,hashlib
from pathlib import Path
from itertools import product
BASE=Path(__file__).resolve().parent;CAP=min(120,float(sys.argv[1]))
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def compositions(n,k):
    if k==1:yield(n,);return
    for a in range(n+1):
        for rest in compositions(n-a,k-1):yield(a,)+rest
def main():
    start=time.process_time();index={};canonical={}
    for i in range(1,8):
        phase=BASE.parent/f'M3_POP4_RISK{i:02d}'
        for cp in sorted(phase.glob('completed_*.json')):
            r=read(cp);assert r['independent_audit']=='PASS';sig=tuple(r['sigma']);folder=phase/('s'+''.join(map(str,sig)))
            assert sum(sig)==4 and sum(n>0 for n in sig)>=2
            assert (folder/'potential.json').exists() and (folder/'metadata.json').exists()
            canonical[sig]={'folder':folder.as_posix(),'completion':cp.as_posix(),'completion_sha256':sha(cp),'sigma':sig}
    for sig,item in canonical.items():
        for actual,reflected in ((sig,False),(tuple(reversed(sig)),True)):
            if actual in index:assert index[actual]['folder']==item['folder'];continue
            index[actual]={**item,'actual_sigma':actual,'reflected':reflected}
    expected={s for s in compositions(4,10) if sum(n>0 for n in s)>=2}
    assert set(index)==expected and len(index)==705
    out={'status':'EXACT_705_COMPLETED_TOTAL4_PATTERN_BASIS_INDEXED','signature_count':len(index),'canonical_tables':len(canonical),'entries':[index[s] for s in sorted(index)],'new_source_queries':0,'old_certificates_reused_not_reaudited':True,'CPU_seconds':time.process_time()-start,'CPU_cap':CAP}
    assert out['CPU_seconds']<CAP;write(BASE/'basis.json',out);print(json.dumps({k:v for k,v in out.items() if k!='entries'},indent=2),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error={'type':type(e).__name__,'message':str(e)};raise
    finally:write(BASE/'basis_exit.json',{'whole_process_CPU_seconds':time.process_time(),'CPU_cap':CAP,'error':error})
