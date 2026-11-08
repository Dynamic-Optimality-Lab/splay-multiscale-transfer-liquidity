"""Reuse completed inputs; independently check the bounded streaming reader."""
import json,sys,time,hashlib
from pathlib import Path
from stream_values import Values
BASE=Path(__file__).resolve().parent;CAP=min(120,float(sys.argv[1]))
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def signature(name):return list(map(int,name[1:]))
def descriptor(sig):
    occupied=[i for i,n in enumerate(sig) if n]
    return tuple(sorted((n for n in sig if n),reverse=True)),max(occupied)-min(occupied),bool(sig[0]),bool(sig[9])
def main():
    start=time.process_time();old=BASE.parent/'M3_PRED01';assert read(old/'case_000/audit.json')['status']=='FINITE_EXACT_THRESHOLD_PREDICATES_SIGNED_PRESERVATION_PASS'
    build=read(old/'case_001/construction.json');assert sha(old/'case_001/candidate.json')==build['candidate_sha256']
    assert read(old/'case_001/audit_exit.json')['error']['message']=='UNKNOWN independent predicate-audit record cap'
    p=Path(read(old/'case_000/construction.json')['basis_dependencies'][0]['folder'])/'potential.json';expected=read(p);count=0
    with Values(p) as streamed:
        assert streamed.header['N']==expected['N'] and streamed.header['default']==expected['default']
        reference=iter(expected['values'].items())
        for key,value in streamed:
            k,v=next(reference);assert key==int(k) and value==v;count+=1
            if count%16384==0:assert time.process_time()-start<CAP
        assert next(reference,None) is None and count==len(expected['values'])==streamed.count
    del expected
    cases=[{'name':'s3110000000','reused_input':(old/'case_001').as_posix(),'source_coverage_complete':True},
           {'name':'s0311000000','reused_input':None,'source_coverage_complete':True},
           {'name':'s0004001000','reused_input':None,'source_coverage_complete':False}]
    seen={descriptor(signature(n)) for n in ['s4100000000']+[c['name'] for c in cases]};extras=0
    for completed in sorted((BASE.parent/'M3_POP5_RISK01').glob('completed_*.json')):
        sig=read(completed)['sigma'];desc=descriptor(sig)
        if desc in seen:continue
        seen.add(desc);cases.append({'name':'s'+''.join(map(str,sig)),'reused_input':None,'source_coverage_complete':True,'selection_descriptor':[list(desc[0]),*desc[1:]]});extras+=1
        if extras==6:break
    for c in cases:
        folder=BASE.parent/'M3_POP5_RISK01'/c['name'];c['source_folder']=folder.as_posix();assert (folder/'relation.json').exists()
        if c['source_coverage_complete']:assert read(folder/'audit.json')['status']=='INDEPENDENT_RISK_PREFIX_AND_RESIDUAL_PASS'
    config={'basis_path':(old/'basis.json').as_posix(),'basis_sha256':sha(old/'basis.json'),'cases':cases,'first_case_complete_reused_not_repeated':True}
    write(BASE/'config.json',config)
    report={'status':'MEMORY_RETRY_INPUTS_AND_STREAM_READER_PREPARED','parser_equivalence_method':'all entries/order/header compared with independent stdlib json.loads','parser_dictionary_entries_checked':count,'parser_input_sha256':sha(p),'parser_peak_dictionary_records':count,'basis_index_reused':True,'first_completed_formula_audit_reused':True,'old_candidate_construction_reused':True,'registered_cases':[c['name'] for c in cases],'old_source_roots_grammar_or_residual_checks_repeated':0,'CPU_seconds':time.process_time()-start,'CPU_cap':CAP}
    assert report['CPU_seconds']<CAP;write(BASE/'prepare.json',report);print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error={'type':type(e).__name__,'message':str(e)};raise
    finally:write(BASE/'prepare_exit.json',{'whole_process_CPU_seconds':time.process_time(),'CPU_cap':CAP,'error':error})
