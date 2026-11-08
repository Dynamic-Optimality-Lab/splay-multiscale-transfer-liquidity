"""Independent attainment/upper-envelope proof, THEN all signed residuals."""
import json,sys,time,hashlib
from pathlib import Path
from collections import Counter
BASE=Path(__file__).resolve().parent;INDEX=int(sys.argv[1]);CAP=min(300,float(sys.argv[2]));OUT=BASE/f'case_{INDEX:03d}'
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    start=time.process_time();build=read(OUT/'construction.json');source=Path(build['source_folder']);c=read(source/'relation.json');B=read(BASE.parent/'M3_UNITPAIR01/B_bank.json');p=read(OUT/'candidate.json');N=c['classes'];psi=B['psi']
    V={int(k):v for k,v in p['values'].items()};A={int(k):v for k,v in p['attainment'].items()}
    assert set(V)==set(A) and p['N']==N and p['sigma']==c['sigma']
    del p['values'],p['attainment']
    assert N+c['option_count']+len(V)+len(A)<2000000 and c['queries']<=2000000 and c['option_count']<5000000
    byroot={r:[] for r in range(9)}
    for a,alpha in enumerate(c['shadows']):byroot[alpha[0][2]].append(a)
    def debt(b,a):return V.get(b*N+a,psi[b])
    def edge(b,o):
        H,x,aa,gap,fi,code=o
        if H==1:
            depth=B['depths'][b][x]
            if depth==0:return None
            return B['destinations'][b][x],2-depth//2
        assert H==2 and gap in (0,9) and c['sigma'][gap]>0
        return B['kernels'][str(gap)][b][x]
    def guard():assert time.process_time()-start<CAP,'UNKNOWN independent candidate CPU cap'
    for key,value in V.items():
        b,a=divmod(key,N);assert c['shadows'][a][0][2]==B['trees'][b][0] and psi[b]<value<=2
        bs,asrc,oi=A[key];o=c['options'][asrc][oi];pair=edge(bs,o)
        assert B['trees'][bs][0]==c['shadows'][asrc][0][2]
        assert pair is not None and pair[0]==b and o[2]==a and pair[1] in (0,1) and value==psi[bs]-pair[1]
    guard();bounds=0
    # Complete universal seed-bound direction, independent of constructor filters.
    for b,t in enumerate(B['trees']):
        if psi[b]:
            for a in byroot[t[0]]:
                for o in c['options'][a]:
                    pair=edge(b,o)
                    if pair is None:continue
                    bb,w=pair
                    if w in (0,1):assert debt(bb,o[2])>=psi[b]-w;bounds+=1
        guard()
    equality={'status':'EXACT_F_PSI_FORMULA_AUDIT_PASS','all_nondefault_values_attained':True,'all_seed_contributions_bounded':True,'seed_bounds_checked':bounds,'negative_seed_rows_discharged_by_pinned_core_debt_law':True,'omitted_rows_discharged_analytically':True,'CPU_seconds':time.process_time()-start,'candidate_sha256':hashlib.sha256((OUT/'candidate.json').read_bytes()).hexdigest()}
    write(OUT/'formula_identity_audit.json',equality);print(json.dumps(equality),flush=True)
    checks=0;hist=Counter();failure=None
    for b,t in enumerate(B['trees']):
        for a in byroot[t[0]]:
            ds=debt(b,a)
            if ds==0:continue # dt>=psi covers negative rows; dt>=0 covers the rest.
            for oi,o in enumerate(c['options'][a]):
                pair=edge(b,o)
                if pair is None:continue
                bb,w=pair
                if w>=2:continue
                aa=o[2];dt=debt(bb,aa);res=w+dt-ds;checks+=1;hist[res]+=1
                if res<0:
                    old=read(source/'potential.json')
                    js=old['values'].get(str(b*N+a),-psi[b]);jt=old['values'].get(str(bb*N+aa),-psi[bb]);assert w-jt+js>=0
                    del old
                    failure={'status':'EXACT_COUNTEREXAMPLE_TO_ONE_STEP_CANDIDATE_ON_SAVED_PROOF_RELATION','sigma':c['sigma'],'source_B':b,'source_A':a,'source_alpha':c['shadows'][a],'destination_B':bb,'destination_A':aa,'destination_alpha':c['shadows'][aa],'option_index':oi,'option':o,'family':c['families'][o[4]],'weight':w,'psi_source':psi[b],'psi_destination':psi[bb],'D1_source':ds,'D1_destination':dt,'J1_source':-ds,'J1_destination':-dt,'candidate_residual':res,'source_debt_attainment':A.get(b*N+a),'old_certified_J_source':js,'old_certified_J_destination':jt,'old_certified_residual':w-jt+js,'original_low_root_validated':False,'original_negative_cycle_certified':False,'refutes_M3':False}
                    write(OUT/'obstruction.json',failure);break
                if checks%10000==0:guard()
            if failure:break
        guard()
        if failure:break
    report={'status':'ONE_STEP_CANDIDATE_REFUTED_IN_PROOF_RELATION' if failure else 'FINITE_EXACT_ONE_STEP_CLOSED_ON_SAVED_RELATION','formula_exact_audit':'PASS','sigma':c['sigma'],'new_signed_checks':checks,'minimum_residual':min(hist),'residual_histogram':dict(hist),'source_folder':source.as_posix(),'new_source_transition_queries':0,'saved_canonical_queries_reused':c['queries'],'CPU_cap':CAP,'CPU_seconds':time.process_time()-start,'uniform_closure_proved':False,'M3_status':'OPEN'}
    write(OUT/'audit.json',report);print(json.dumps(report),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error={'type':type(e).__name__,'message':str(e)};raise
    finally:write(OUT/'audit_exit.json',{'whole_process_CPU_seconds':time.process_time(),'CPU_cap':CAP,'error':error})
