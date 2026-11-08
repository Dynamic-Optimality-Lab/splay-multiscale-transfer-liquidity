"""Safe nonnegative closure, then the exact capped negative-run promotion."""
import json,sys,time,hashlib
from pathlib import Path
from collections import deque
BASE=Path(__file__).resolve().parent;INDEX=int(sys.argv[1]);CAP=min(120,float(sys.argv[2]));OUT=BASE/f'case_{INDEX:03d}'
CASES=['s4100000000','s3110000000','s0311000000']
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    OUT.mkdir(exist_ok=False);start=time.process_time();source=BASE.parent/'M3_POP5_RISK01'/CASES[INDEX];c=read(source/'relation.json');B=read(BASE.parent/'M3_UNITPAIR01/B_bank.json');N=c['classes'];psi=B['psi'];byroot={r:[] for r in range(9)}
    assert c['queries']<=2000000 and c['option_count']<5000000
    for a,x in enumerate(c['shadows']):byroot[x[0][2]].append(a)
    peak=checks=0
    def guard(extra=0):
        nonlocal peak
        live=N+c['option_count']+extra;peak=max(peak,live)
        assert live<2000000,'UNKNOWN live record cap'
        assert time.process_time()-start<CAP,'UNKNOWN sign-run construction CPU cap'
    if INDEX==0:
        p=BASE.parent/'M3_UNIFORM01/case_000/candidate.json';audit=read(p.parent/'formula_identity_audit.json');assert audit['status']=='EXACT_F_PSI_FORMULA_AUDIT_PASS' and digest(p)==audit['candidate_sha256']
        initial=read(p);cv={int(k):v for k,v in initial['values'].items()};assert initial['sigma']==c['sigma'] and initial['N']==N;del initial
        write(OUT/'initial.json',{'kind':'REUSED_AUDITED_ONE_STEP_SEED','path':p.as_posix(),'sha256':digest(p),'identity_audit':(p.parent/'formula_identity_audit.json').as_posix()})
    else:
        cv={};attain={}
        for b,t in enumerate(B['trees']):
            if not psi[b]:continue
            trans={}
            for x in range(9):
                d=B['depths'][b][x];bb=B['destinations'][b][x];w=2-d//2
                if d and w in (0,1):trans[1,x,None]=(bb,w)
                for g in (0,9):
                    pair=B['kernels'][str(g)][b][x]
                    if c['sigma'][g] and pair is not None and pair[1] in (0,1):trans[2,x,g]=pair
            for a in byroot[t[0]]:
                for oi,o in enumerate(c['options'][a]):
                    pair=trans.get(tuple(o[i] for i in (0,1,3)))
                    if pair is None:continue
                    bb,w=pair;key=bb*N+o[2];alt=psi[b]-w
                    if alt>cv.get(key,psi[bb]):cv[key]=alt;attain[key]=[b,a,oi]
            guard(len(cv)+len(attain))
        write(OUT/'initial.json',{'kind':'ONE_CHEAP_SEED_PASS','N':N,'values':cv,'attainment':attain});del attain
    # Every seed row is covered by the existing one-step seed pass. Process
    # only increased sources; no old seed-bound audit is repeated in case0.
    queue=deque(cv);queued=set(cv);history=[];latest={};updates=0
    nonnegative=[];pops=0
    for b in range(4862):
        trans={}
        for x in range(9):
            depth=B['depths'][b][x];bb=B['destinations'][b][x];w=2-depth//2
            if depth and w in (0,1):trans[1,x,None]=(bb,w)
            for g in (0,9):
                pair=B['kernels'][str(g)][b][x]
                if c['sigma'][g] and pair is not None and pair[1] in (0,1):trans[2,x,g]=pair
        nonnegative.append(trans)
    trans_count=sum(len(row) for row in nonnegative)+4862
    guard(len(cv)+len(history)+len(latest)+len(queue)+len(queued)+trans_count)
    while queue:
        key=queue.popleft();queued.remove(key);b,a=divmod(key,N);ds=cv.get(key,psi[b]);trans=nonnegative[b]
        pops+=1
        for oi,o in enumerate(c['options'][a]):
            pair=trans.get((o[0],o[1],o[3]))
            if pair is None:continue
            bb,w=pair;v=bb*N+o[2];alt=ds-w;checks+=1
            if alt<=cv.get(v,psi[bb]):continue
            assert 0<alt<=2
            history.append([key,v,oi,ds,alt,latest.get(key,-1)]);latest[v]=len(history)-1;cv[v]=alt;updates+=1
            if v not in queued:queue.append(v);queued.add(v)
        if pops%512==0 or not queue:guard(len(cv)+len(history)+len(latest)+len(queue)+len(queued)+trans_count)
    guard(len(cv)+len(history)+len(latest)+trans_count)
    write(OUT/'C_values.json',{'N':N,'default':'psi(B)','values':cv})
    write(OUT/'C_attainment.json',{'history':history,'latest':latest,'initial_reference':'initial.json'})
    ch=len(history);del history,latest,queue,queued,nonnegative
    nv=dict(cv);promotion={};negvisits=0
    for b,t in enumerate(B['trees']):
        if psi[b]!=0:continue
        trans={x:B['destinations'][b][x] for x in range(9) if B['depths'][b][x] and 2-B['depths'][b][x]//2==-1 and psi[B['destinations'][b][x]]==1}
        if trans:
            for a in byroot[t[0]]:
                if cv.get(b*N+a,0)==0:continue
                for oi,o in enumerate(c['options'][a]):
                    if o[0]!=1 or o[1] not in trans:continue
                    bb=trans[o[1]];v=bb*N+o[2];negvisits+=1
                    if nv.get(v,psi[bb])<2:nv[v]=2;promotion[v]=[b,a,oi]
        guard(len(cv)+len(nv)+len(promotion)+4862)
    write(OUT/'candidate.json',{'N':N,'sigma':c['sigma'],'default':'psi(B)','values':nv,'promotion':promotion})
    report={'status':'SIGN_RUN_CANDIDATE_CONSTRUCTED_UNAUDITED','source_folder':source.as_posix(),'case':CASES[INDEX],'sigma':c['sigma'],'classes':N,'C_exceptions':len(cv),'new_nonnegative_updates':updates,'nonnegative_history_records':ch,'nonnegative_row_visits':checks,'D_exceptions':len(nv),'negative_promotions':len(promotion),'negative_trigger_visits':negvisits,'peak_conservative_live_records':peak,'saved_canonical_profiles_reused':c['queries'],'new_source_word_queries':0,'CPU_seconds':time.process_time()-start,'CPU_cap':CAP,'C_sha256':digest(OUT/'C_values.json'),'candidate_sha256':digest(OUT/'candidate.json'),'uniform_closure_proved':False}
    write(OUT/'construction.json',report);print(json.dumps(report),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error={'type':type(e).__name__,'message':str(e)};raise
    finally:
        OUT.mkdir(exist_ok=True);write(OUT/'construct_exit.json',{'whole_process_CPU_seconds':time.process_time(),'CPU_cap':CAP,'error':error})
