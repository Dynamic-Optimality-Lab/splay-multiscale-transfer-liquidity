"""Exact independent identity/signed audit: in-place attainment, streamed basis."""
import json,sys,time,hashlib
from pathlib import Path
from collections import Counter
from stream_values import Values
BASE=Path(__file__).resolve().parent;INDEX=int(sys.argv[1]);CAP=min(300,float(sys.argv[2]));OUT=BASE/f'case_{INDEX:03d}'
sys.path.insert(0,str(BASE.parent/'M3_TWOGAP_AUD01'))
import reference as R
BANK_RESERVE=300000;SCRATCH=8192;FLAG=4;MASK=3
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def mirrored(a):
    return tuple((kind,iss,8-label if kind==0 and iss else label) for path in R.SHADOW for kind,iss,label in [a[R.SHADOW.index(tuple(1-x for x in path))]])
def containers(v):
    if isinstance(v,list):return 1+sum(map(containers,v))
    if isinstance(v,dict):return 1+sum(map(containers,v.values()))
    return 0
def main():
    OUT.mkdir(exist_ok=True);start=time.process_time();config=read(BASE/'config.json');case=config['cases'][INDEX];inputdir=Path(case['reused_input']) if case['reused_input'] else OUT
    build=read(inputdir/'construction.json');source=Path(build['source_folder']);meta=read(source/'build_status.json');N=meta['classes'];options=meta['option_count'];exception_count=build['changed_pattern_states']
    baseline=2*N+options+exception_count+BANK_RESERVE+SCRATCH+705;assert baseline<2000000,'UNKNOWN initial planned live record cap'
    plans=[]
    for e in build['basis_dependencies']:
        smallN=read(Path(e['folder'])/'build_status.json')['classes'];records=baseline+2*smallN
        assert records<2000000,'UNKNOWN planned independent live record cap';plans.append(records)
    write(OUT/'memory_plan.json',{'status':'PREFLIGHT_WITHIN_UNCHANGED_LIVE_RECORD_CAP','cap':2000000,'planned_peak':max(plans+[baseline]),'candidate_key_set_allocated':False,'basis_values_dictionary_allocated':False,'in_place_audit_flag':FLAG,'immutable_bank_container_reserve':BANK_RESERVE,'scratch_reserve':SCRATCH})
    c=read(source/'relation.json');cp=read(inputdir/'candidate.json');cv=cp['values'];B=read(BASE.parent/'M3_UNITPAIR01/B_bank.json');psi=B['psi'];bank_containers=containers(B);assert bank_containers<BANK_RESERVE
    assert sha(source/'relation.json')==build['relation_sha256'] and sha(inputdir/'candidate.json')==build['candidate_sha256'] and cp['N']==N and cp['sigma']==c['sigma'] and len(cv)==exception_count
    for i,a in enumerate(c['shadows']):c['shadows'][i]=R.frozen(a)
    shadows=c['shadows'];aid={a:i for i,a in enumerate(shadows)};bounds=marked=0;peak=baseline
    def D(b,a):return cv.get(str(b*N+a),psi[b])&MASK
    def guard(records=baseline):
        nonlocal peak
        peak=max(peak,records);assert records<2000000,'UNKNOWN independent live record cap'
        assert time.process_time()-start<CAP,'UNKNOWN independent CPU cap'
    for key,value in cv.items():
        b,a=divmod(int(key),N);assert psi[b]<value<=2 and value in (1,2) and shadows[a][0][1] and shadows[a][0][2]==B['trees'][b][0]
    expected=[(e['folder'],e['reflected'],e['actual_sigma']) for e in read(Path(config['basis_path']))['entries'] if all(x<=y for x,y in zip(e['actual_sigma'],c['sigma']))]
    assert expected==[(e['folder'],e['reflected'],e['actual_sigma']) for e in build['basis_dependencies']]
    for e,records in zip(build['basis_dependencies'],plans):
        folder=Path(e['folder']);guard(records)
        assert sha(folder/'metadata.json')==e['metadata_sha256'] and sha(folder/'potential.json')==e['potential_sha256']
        m=read(folder/'metadata.json');smallN=m['classes'];routes=[aid.get(mirrored(R.frozen(a)) if e['reflected'] else R.frozen(a)) for a in m['shadows']]
        with Values(folder/'potential.json') as reader:
            assert reader.header['N']==smallN
            for key,j in reader:
                qb,qa=divmod(key,smallN);b=B['mirror'][qb] if e['reflected'] else qb;a=routes[qa]
                if a is not None:
                    k=str(b*N+a);debt=D(b,a);assert -j<=debt,'THRESHOLD_ENVELOPE_UPPER_BOUND_FAILED'
                    if -j==debt:
                        assert k in cv
                        if not(cv[k]&FLAG):marked+=1
                        cv[k]|=FLAG
                    bounds+=1
                if reader.count%8192==0:guard(records)
            assert reader.count==e['basis_changed_patterns']
        del m,routes
    assert marked==len(cv)
    for key,value in cv.items():assert value&FLAG;cv[key]=value&MASK
    identity={'status':'INDEPENDENT_STREAMED_THRESHOLD_PREDICATE_IDENTITY_PASS','candidate_sha256':build['candidate_sha256'],'all_exceptions_attained':True,'all_eligible_basis_contributions_bounded':True,'basis_bound_comparisons':bounds,'attainment_flags_set_and_cleared':marked,'no_duplicate_candidate_key_set':True,'no_materialized_basis_values':True,'nested_P2_subset_P1':True,'psi_le_D_le_2':True,'peak_conservative_records':peak,'immutable_bank_containers':bank_containers,'old_constructed_candidate_reused':bool(case['reused_input']),'CPU_seconds':time.process_time()-start};write(OUT/'predicate_identity_audit.json',identity)
    del aid
    byroot={r:[] for r in range(9)}
    for a,shadow in enumerate(shadows):byroot[shadow[0][2]].append(a)
    fcounts=[sum(kind==0 and not iss for kind,iss,label in a) for a in shadows]
    signed_baseline=baseline+N # one small F-count index, no pattern/basis bank is resident
    checks=states=zero_sources=0;rules=Counter();residuals=Counter();features=Counter();failure=None
    for b,tree in enumerate(B['trees']):
        trans={}
        for x in range(9):
            dep=B['depths'][b][x];bb=B['destinations'][b][x];w=2-dep//2
            if dep and w<2 and w+psi[bb]<2:trans[1,x,None]=(bb,w)
            for g in (0,9):
                pair=B['kernels'][str(g)][b][x]
                if c['sigma'][g] and pair is not None and pair[1]<2 and pair[1]+psi[pair[0]]<2:trans[2,x,g]=tuple(pair)
        for a in byroot[tree[0]]:
            ds=D(b,a);states+=1
            if ds==0:zero_sources+=1;continue # pinned negative-core floor + nonnegative range, as in completed audit
            for oi,o in enumerate(c['options'][a]):
                pair=trans.get((o[0],o[1],o[3]))
                if pair is None:continue
                bb,w=pair;aa=o[2];dt=D(bb,aa);res=w+dt-ds;checks+=1;rules[w]+=1;residuals[res]+=1
                if ds-w>psi[bb]:features[w,ds,dt,fcounts[a],fcounts[aa],psi[b],psi[bb]]+=1
                if w==1:ok=ds<2 or dt>=1
                elif w==0:ok=dt>=ds
                elif w==-1:ok=ds<=1 and dt>=ds+1
                else:assert w==-2;ok=ds==0 and dt==2
                assert ok==(res>=0)
                if res<0:
                    failure={'status':'EXACT_THRESHOLD_PREDICATE_SIGNED_RULE_COUNTEREXAMPLE','sigma':c['sigma'],'source_B':b,'source_A':a,'source_alpha':shadows[a],'destination_B':bb,'destination_A':aa,'destination_alpha':shadows[aa],'option_index':oi,'option':o,'family':c['families'][o[4]],'weight':w,'source_debt':ds,'destination_debt':dt,'candidate_residual':res,'source_visible_F':fcounts[a],'destination_visible_F':fcounts[aa],'original_realizability':'NOT_YET_AUDITED','original_negative_cycle_certified':False,'refutes_M3':False};write(OUT/'obstruction.json',failure);break
                if checks%16384==0:guard(signed_baseline+len(features))
            if failure:break
        guard(signed_baseline+len(features))
        if failure:break
    write(OUT/'structural_features.json',{'schema':['weight','source_debt','destination_debt','source_visible_F','destination_visible_F','source_psi','destination_psi'],'nondefault_demand_rows':[{'features':k,'count':v} for k,v in sorted(features.items())],'finite_evidence_only':True})
    report={'status':'THRESHOLD_PREDICATES_REFUTED_IN_SAVED_RELATION' if failure else 'FINITE_EXACT_STREAMED_THRESHOLD_SIGNED_PRESERVATION_PASS','case':case['name'],'sigma':c['sigma'],'signed_rows_checked':checks,'signed_rule_histogram':dict(rules),'residual_histogram':dict(residuals),'minimum_residual':min(residuals) if residuals else 0,'compatible_states_streamed':states,'zero_debt_sources_analytically_discharged':zero_sources,'peak_conservative_records':peak,'source_coverage_complete_reused':case['source_coverage_complete'],'unpromoted_stress_input':not case['source_coverage_complete'],'new_source_transition_queries':0,'new_original_root_evaluations':0,'memory_retry_authorized':bool(case['reused_input']),'old_first_case_not_repeated':True,'CPU_seconds':time.process_time()-start,'CPU_cap':CAP,'universal_preservation_proved':False,'M3_status':'OPEN'}
    write(OUT/'audit.json',report);print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error={'type':type(e).__name__,'message':str(e)};raise
    finally:
        OUT.mkdir(exist_ok=True);write(OUT/'audit_exit.json',{'whole_process_CPU_seconds':time.process_time(),'CPU_cap':CAP,'error':error})
