"""Metadata/code edit only; preserve the failed compiler and all its charges."""
from pathlib import Path
F=Path(__file__).resolve().parent
text=(F/'build_branch_H2.py').read_text()
def change(old,new):
    global text
    assert text.count(old)==1,old
    text=text.replace(old,new)
change('import hashlib,json,sys,time','import hashlib,json,sys,time,pickle')
change('CAP=float(sys.argv[1]);START=time.process_time();M=set(range(1000,8000,1000))',
       'CAP=float(sys.argv[1]);START=time.process_time();M=set(range(1000,8000,1000));PHASE=sys.argv[3];BATCH=int(sys.argv[4])')
change('    rel={};contexts=0', '''    if BATCH==1:
        rel={};contexts=0;start_a=0;prior_applications=0
    else:
        with (F/f'branch_H2_frames_{BATCH-1:02d}.pkl').open('rb') as f:checkpoint=pickle.load(f)
        assert checkpoint['status']=='CHECKPOINT'
        rel=checkpoint['rel'];contexts=checkpoint['contexts'];start_a=checkpoint['next_A']
        prior_applications=checkpoint['cached_access_instances']
    next_a=start_a''')
change('    for a,raw in enumerate(aa):\n        T,g=canonical(raw,raw[0])',
       '    for a in range(start_a,len(aa)):\n        raw=aa[a];T,g=canonical(raw,raw[0])')
change('        if a%50==0:assert time.process_time()-START<CAP-3',
       '        next_a=a+1\n        if time.process_time()-START>CAP-5:break')
change("    keys=sorted(rel);out={'status':'COMPLETE_SOURCE_H2_BRANCH_RELATION_PENDING_INDEPENDENT_AUDIT','r':7,'H2_rows':keys,", '''    checkpoint={'status':'COMPLETE' if next_a==len(aa) else 'CHECKPOINT','next_A':next_a,
       'rel':rel,'contexts':contexts,'cached_access_instances':prior_applications+frames.applications,
       'source_queries':0,'source_engine_calls':0}
    with (F/f'branch_H2_frames_{BATCH:02d}.pkl').open('xb') as f:pickle.dump(checkpoint,f,protocol=5)
    report={k:v for k,v in checkpoint.items() if k!='rel'};report['H2_rows_so_far']=len(rel)
    with (F/f'branch_H2_frames_{BATCH:02d}.json').open('x',encoding='utf-8') as f:json.dump(report,f,indent=2)
    print(json.dumps(report),flush=True)
    if next_a!=len(aa):return
    keys=sorted(rel);out={'status':'COMPLETE_SOURCE_H2_BRANCH_RELATION_PENDING_INDEPENDENT_AUDIT','r':7,'H2_rows':keys,''')
change("'symbolic_cached_access_instances':frames.applications,'first_frame_contexts':contexts,",
       "'symbolic_cached_access_instances':prior_applications+frames.applications,'first_frame_contexts':contexts,")
change("(B/'audit_proof213_exit.json')", "(B/f'audit_{PHASE}_exit.json')")
with (F/'build_branch_H2_resumable.py').open('x',encoding='utf-8') as f:f.write(text)
print('RESUMABLE_H2_COMPILER_CREATED_WITH_FAILED_VERSION_RETAINED')
