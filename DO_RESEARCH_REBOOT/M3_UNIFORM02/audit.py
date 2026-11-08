"""Independent path-attainment/C-closure, promotion identity, then signed rows."""
import json,sys,time,hashlib
from pathlib import Path
from collections import Counter
BASE=Path(__file__).resolve().parent;INDEX=int(sys.argv[1]);CAP=min(300,float(sys.argv[2]));OUT=BASE/f'case_{INDEX:03d}'
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    start=time.process_time();build=read(OUT/'construction.json');source=Path(build['source_folder']);c=read(source/'relation.json');B=read(BASE.parent/'M3_UNITPAIR01/B_bank.json');psi=B['psi'];N=c['classes'];cp=read(OUT/'C_values.json');dp=read(OUT/'candidate.json');cv=cp.pop('values');nv=dp.pop('values');prom=dp.pop('promotion');initial=read(OUT/'initial.json');cached=initial['kind']=='REUSED_AUDITED_ONE_STEP_SEED'
    assert c['queries']<=2000000 and c['option_count']<5000000
    if cached:
        p=Path(initial['path']);assert sha(p)==initial['sha256'];q=read(Path(initial['identity_audit']));assert q['status']=='EXACT_F_PSI_FORMULA_AUDIT_PASS' and q['candidate_sha256']==initial['sha256']
        ip=read(p);iv=ip.pop('values');del ip['attainment'];assert ip['sigma']==c['sigma'] and ip['N']==N
    else:iv=initial.pop('values')
    def C(b,a):return cv.get(str(b*N+a),psi[b])
    def D(b,a):return nv.get(str(b*N+a),psi[b])
    def I(key):return iv.get(str(key),psi[key//N])
    def edge(b,o):
        H,x,aa,g,fi,code=o
        if H==1:
            depth=B['depths'][b][x]
            return None if depth==0 else (B['destinations'][b][x],2-depth//2)
        assert H==2 and g in (0,9) and c['sigma'][g]
        return B['kernels'][str(g)][b][x]
    base_live=N+c['option_count']+len(cv)+len(nv)+len(iv)+len(prom);peak=base_live
    def guard(extra=0):
        nonlocal peak
        peak=max(peak,base_live+extra);assert base_live+extra<2000000,'UNKNOWN independent live-record cap'
        assert time.process_time()-start<CAP,'UNKNOWN independent sign-run audit CPU cap'
    for key,value in iv.items():
        b,a=divmod(int(key),N);assert psi[b]<value<=2 and C(b,a)>=value
        if not cached:
            bs,asrc,oi=initial['attainment'][key];o=c['options'][asrc][oi];pair=edge(bs,o)
            assert pair is not None and pair[1] in (0,1) and pair[0]==b and o[2]==a and value==psi[bs]-pair[1]
    if not cached:del initial['attainment']
    hp=read(OUT/'C_attainment.json');history=hp.pop('history');latest=hp.pop('latest');seen={}
    for idx,(u,v,oi,ds,dt,prior) in enumerate(history):
        b,a=divmod(u,N);bb,aa=divmod(v,N);o=c['options'][a][oi];pair=edge(b,o)
        assert pair is not None and pair[0]==bb and o[2]==aa and pair[1] in (0,1) and ds-pair[1]==dt and 0<dt<=2
        assert prior<idx
        if prior>=0:assert history[prior][1]==u and history[prior][4]==ds
        else:assert ds==I(u)
        prev=seen.get(v);previous=I(v) if prev is None else history[prev][4];assert dt>previous;seen[v]=idx
        if idx%512==0:guard(len(history)+len(latest)+len(seen))
    assert len(seen)==len(latest) and all(latest[str(k)]==v for k,v in seen.items())
    for key,value in cv.items():
        k=int(key);b,a=divmod(k,N);assert c['shadows'][a][0][2]==B['trees'][b][0] and psi[b]<value<=2
        if key in latest:assert history[latest[key]][1]==k and history[latest[key]][4]==value
        else:assert value==I(k)
    for k in latest:assert cv[k]==history[latest[k]][4]
    derivations=len(history);del history,latest,seen
    roots={r:[] for r in range(9)}
    for a,alpha in enumerate(c['shadows']):roots[alpha[0][2]].append(a)
    cchecks=0
    for b,t in enumerate(B['trees']):
        for a in roots[t[0]]:
            ds=C(b,a)
            if ds==0 or (cached and ds==psi[b]):continue
            for o in c['options'][a]:
                pair=edge(b,o)
                if pair is not None and pair[1] in (0,1):
                    bb,w=pair;assert w+C(bb,o[2])-ds>=0,'NONNEGATIVE_CLOSURE_PREMISE_FAILED';cchecks+=1
        guard()
    for key,value in nv.items():
        b,a=divmod(int(key),N);assert c['shadows'][a][0][2]==B['trees'][b][0] and psi[b]<value<=2 and value>=C(b,a)
        if value>C(b,a):
            assert value==2 and psi[b]==C(b,a)==1
            bs,asrc,oi=prom[key];o=c['options'][asrc][oi];pair=edge(bs,o)
            assert psi[bs]==0 and C(bs,asrc)>0 and o[0]==1 and pair is not None and pair[0]==b and pair[1]==-1 and o[2]==a
        else:assert key not in prom
    assert all(D(*divmod(int(key),N))>=v for key,v in cv.items())
    triggers=0
    for b,t in enumerate(B['trees']):
        if psi[b]!=0:continue
        for a in roots[t[0]]:
            if C(b,a)==0:continue
            for o in c['options'][a]:
                if o[0]!=1:continue
                pair=edge(b,o)
                if pair is not None and pair[1]==-1 and psi[pair[0]]==1:assert D(pair[0],o[2])==2;triggers+=1
        guard()
    identity={'status':'INDEPENDENT_SIGN_RUN_FORMULA_IDENTITY_PASS','C_attainment_history_rows':derivations,'nonnegative_closure_rows':cchecks,'legacy_seed_bound_audit_reused':cached,'negative_promotion_triggers':triggers,'all_promotions_attained':True,'C_is_exact_nonnegative_path_envelope':True,'D_is_exact_capped_negative_run_formula':True,'peak_conservative_live_records':peak,'C_sha256':sha(OUT/'C_values.json'),'candidate_sha256':sha(OUT/'candidate.json'),'CPU_seconds':time.process_time()-start}
    if INDEX==0:
        old=read(BASE.parent/'M3_UNIFORM01/case_000/obstruction.json');ds=D(old['source_B'],old['source_A']);dt=D(old['destination_B'],old['destination_A']);assert (ds,dt)==(1,2) and old['weight']+dt-ds==0
        identity['old_plus1_minus1_regression']={'source_debt':ds,'destination_debt':dt,'residual':0,'old_original_lift_repeated':False}
    write(OUT/'formula_identity_audit.json',identity);print(json.dumps(identity),flush=True)
    checks=0;hist=Counter();failure=None
    for b,t in enumerate(B['trees']):
        for a in roots[t[0]]:
            ds=D(b,a)
            if ds==psi[b]:continue # seed-source rows already sound by C closure/core law.
            for oi,o in enumerate(c['options'][a]):
                pair=edge(b,o)
                if pair is None or pair[1]>=2:continue
                bb,w=pair;aa=o[2];dt=D(bb,aa);res=w+dt-ds;checks+=1;hist[res]+=1
                if res<0:
                    old=read(source/'potential.json');js=old['values'].get(str(b*N+a),-psi[b]);jt=old['values'].get(str(bb*N+aa),-psi[bb]);assert w-jt+js>=0;del old
                    failure={'status':'EXACT_SIGN_RUN_COUNTEREXAMPLE_IN_SAVED_PROOF_RELATION','sigma':c['sigma'],'source_B':b,'source_A':a,'source_alpha':c['shadows'][a],'destination_B':bb,'destination_A':aa,'destination_alpha':c['shadows'][aa],'option_index':oi,'option':o,'family':c['families'][o[4]],'weight':w,'psi_source':psi[b],'psi_destination':psi[bb],'C_source':C(b,a),'C_destination':C(bb,aa),'D_run_source':ds,'D_run_destination':dt,'J_run_source':-ds,'J_run_destination':-dt,'candidate_residual':res,'source_promotion':prom.get(str(b*N+a)),'destination_promotion':prom.get(str(bb*N+aa)),'old_certified_J_source':js,'old_certified_J_destination':jt,'old_certified_residual':w-jt+js,'original_low_root_validated':False,'original_negative_cycle_certified':False,'refutes_M3':False}
                    write(OUT/'obstruction.json',failure);break
                if checks%10000==0:guard()
            if failure:break
        guard()
        if failure:break
    report={'status':'SIGN_RUN_CANDIDATE_REFUTED_IN_PROOF_RELATION' if failure else 'FINITE_EXACT_SIGN_RUN_CLOSED_ON_SAVED_RELATION','formula_identity_audit':'PASS','signed_rows_until_stop':checks,'minimum_residual':min(hist) if hist else 0,'residual_histogram':dict(hist),'source_folder':source.as_posix(),'saved_canonical_profiles_reused':c['queries'],'new_source_word_queries':0,'CPU_seconds':time.process_time()-start,'CPU_cap':CAP,'uniform_original_closure_proved':False}
    write(OUT/'audit.json',report);print(json.dumps(report),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error={'type':type(e).__name__,'message':str(e)};raise
    finally:write(OUT/'audit_exit.json',{'whole_process_CPU_seconds':time.process_time(),'CPU_cap':CAP,'error':error})
