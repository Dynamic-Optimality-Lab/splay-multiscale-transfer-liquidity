"""Independent threshold-envelope attainment/upper bound and signed-rule audit."""
import json,sys,time,hashlib
from pathlib import Path
from collections import Counter
BASE=Path(__file__).resolve().parent;INDEX=int(sys.argv[1]);CAP=min(300,float(sys.argv[2]));OUT=BASE/f'case_{INDEX:03d}'
sys.path.insert(0,str(BASE.parent/'M3_TWOGAP_AUD01'))
import reference as R
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def mirror(a):
    out=[]
    for path in R.SHADOW:
        opposite=tuple(1-x for x in path);j=R.SHADOW.index(opposite);kind,iss,label=a[j]
        out.append((kind,iss,8-label if iss and kind==0 else label))
    return tuple(out)
def main():
    start=time.process_time();build=read(OUT/'construction.json');source=Path(build['source_folder']);c=read(source/'relation.json');cp=read(OUT/'candidate.json');B=read(BASE.parent/'M3_UNITPAIR01/B_bank.json');N=c['classes'];psi=B['psi'];cv=cp['values']
    assert sha(source/'relation.json')==build['relation_sha256'] and sha(OUT/'candidate.json')==build['candidate_sha256'] and cp['N']==N and cp['sigma']==c['sigma']
    shadows=list(map(R.frozen,c['shadows']));aid={a:i for i,a in enumerate(shadows)};remaining=set(cv);peak=0;bounds=0
    def D(b,a):return cv.get(str(b*N+a),psi[b])
    def guard(extra=0):
        nonlocal peak
        peak=max(peak,2*N+c['option_count']+len(cv)+len(remaining)+extra+705)
        assert peak<2000000,'UNKNOWN independent predicate-audit record cap'
        assert time.process_time()-start<CAP,'UNKNOWN independent predicate-audit CPU cap'
    for key,v in cv.items():
        b,a=divmod(int(key),N);assert shadows[a][0][1] and shadows[a][0][2]==B['trees'][b][0] and psi[b]<v<=2
    # Every candidate exception must be attained. Every eligible nondefault
    # basis pattern must lie below it, including previously omitted keys.
    expected=[]
    for e in read(BASE/'basis.json')['entries']:
        if all(a<=b for a,b in zip(e['actual_sigma'],c['sigma'])):expected.append((e['folder'],e['reflected'],e['actual_sigma']))
    assert expected==[(e['folder'],e['reflected'],e['actual_sigma']) for e in build['basis_dependencies']]
    for e in build['basis_dependencies']:
        folder=Path(e['folder']);assert sha(folder/'metadata.json')==e['metadata_sha256'] and sha(folder/'potential.json')==e['potential_sha256']
        m=read(folder/'metadata.json');p=read(folder/'potential.json');smallN=m['classes'];assert p['N']==smallN
        routes=[aid.get(mirror(R.frozen(a)) if e['reflected'] else R.frozen(a)) for a in m['shadows']]
        for k,v in p['values'].items():
            qb,qa=divmod(int(k),smallN);b=B['mirror'][qb] if e['reflected'] else qb;a=routes[qa]
            if a is not None:
                key=str(b*N+a);assert -v<=D(b,a),'ENVELOPE_UPPER_BOUND_FAILED'
                if -v==D(b,a):remaining.discard(key)
                bounds+=1
            if bounds%8192==0:guard(2*smallN+len(p['values']))
        guard(2*smallN+len(p['values']));del m,p,routes
    assert not remaining,'UNATTAINED_CANDIDATE_PATTERN'
    identity={'status':'INDEPENDENT_EXACT_THRESHOLD_PREDICATE_IDENTITY_PASS','candidate_sha256':sha(OUT/'candidate.json'),'all_exceptions_attained':True,'all_eligible_basis_contributions_bounded':True,'basis_bound_comparisons':bounds,'nested_P2_subset_P1':True,'psi_le_D_le_2':True,'actual_new_source_queries':0,'CPU_seconds':time.process_time()-start}
    write(OUT/'predicate_identity_audit.json',identity)
    byroot={r:[] for r in range(9)}
    for a,s in enumerate(shadows):byroot[s[0][2]].append(a)
    checks=0;rules=Counter();hist=Counter();failure=None;zero_sources=states=0
    for b,t in enumerate(B['trees']):
        trans={}
        for x in range(9):
            d=B['depths'][b][x];bb=B['destinations'][b][x];w=2-d//2
            if d and w<2 and w+psi[bb]<2:trans[1,x,None]=(bb,w)
            for g in (0,9):
                pair=B['kernels'][str(g)][b][x]
                if c['sigma'][g] and pair is not None and pair[1]<2 and pair[1]+psi[pair[0]]<2:trans[2,x,g]=tuple(pair)
        for a in byroot[t[0]]:
            ds=D(b,a);states+=1
            if ds==0:
                zero_sources+=1;continue # nonnegative rows automatic; negative rows by pinned core debt law and D>=psi.
            for oi,o in enumerate(c['options'][a]):
                pair=trans.get((o[0],o[1],o[3]))
                if pair is None:continue
                bb,w=pair;aa=o[2];dt=D(bb,aa);res=w+dt-ds;checks+=1;rules[w]+=1;hist[res]+=1
                if w==1:ok=ds<2 or dt>=1
                elif w==0:ok=dt>=ds
                elif w==-1:ok=ds<=1 and dt>=ds+1
                else:assert w==-2;ok=ds==0 and dt==2
                assert ok==(res>=0)
                if res<0:
                    failure={'status':'EXACT_THRESHOLD_PREDICATE_SIGNED_RULE_COUNTEREXAMPLE','sigma':c['sigma'],'source_B':b,'source_A':a,'source_alpha':shadows[a],'destination_B':bb,'destination_A':aa,'destination_alpha':shadows[aa],'option_index':oi,'option':o,'family':c['families'][o[4]],'weight':w,'source_debt':ds,'destination_debt':dt,'P1_source':ds>=1,'P2_source':ds>=2,'P1_destination':dt>=1,'P2_destination':dt>=2,'candidate_residual':res,'original_realizability':'NOT_YET_AUDITED','original_negative_cycle_certified':False,'refutes_M3':False}
                    write(OUT/'obstruction.json',failure);break
                if checks%16384==0:guard()
            if failure:break
        guard()
        if failure:break
    regression=None
    if INDEX==0:
        ds=D(1647,2073);dt=D(2403,2072);regression={'source_debt':ds,'destination_debt':dt,'residual':1+dt-ds,'original_edge_provenance':'M3_ROW_AUD01/independent_verification.json','old_original_root_replayed':False}
        if regression['residual']<0 and failure is None:raise AssertionError('regression violates row outside signed scan')
    report={'status':'THRESHOLD_PREDICATES_REFUTED_IN_SAVED_RELATION' if failure else 'FINITE_EXACT_THRESHOLD_PREDICATES_SIGNED_PRESERVATION_PASS','predicate_identity':'PASS','case':build['case'],'sigma':c['sigma'],'signed_rows_checked':checks,'signed_rule_histogram':dict(rules),'residual_histogram':dict(hist),'minimum_residual':min(hist) if hist else 0,'zero_debt_sources_analytically_discharged':zero_sources,'compatible_states_streamed':states,'peak_conservative_records':peak,'original_plus1_regression':regression,'CPU_seconds':time.process_time()-start,'CPU_cap':CAP,'source_grammar_reused_not_repeated':True,'unpromoted_stress_input':INDEX==3,'new_source_transition_queries':0,'universal_preservation_proved':False,'M3_status':'OPEN'}
    write(OUT/'audit.json',report);print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error={'type':type(e).__name__,'message':str(e)};raise
    finally:write(OUT/'audit_exit.json',{'whole_process_CPU_seconds':time.process_time(),'CPU_cap':CAP,'error':error})
