"""Add only independently replayed literal H3 source words; no fake HIGHs."""
import collections,copy,hashlib,json,pickle,sys,time
from pathlib import Path
import numpy as np
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def point(nodes,root,pos,n):
    size=1<<(n-1).bit_length()
    while root>=0:
        l,r=nodes[root];half=size//2
        if pos<half:root=l
        else:root=r;pos-=half
        size=half
    return -root-1
def main():
    with (F/'global_probe11_LOW_model.pkl').open('rb') as f:old=pickle.load(f)
    with (F/'global_probe11_DAG_07.pkl').open('rb') as f:entry=pickle.load(f)
    aud=json.loads((F/'independent_probe11_H3_source_07.json').read_text());assert aud['status']=='PASS_LITERAL_THREE_EVENT_SOURCE_DEFECTS'
    data=json.loads((F/'probe11_H3_source_resolution_07.json').read_text());assert aud['input_sha256']['probe11_H3_source_resolution_07.json']==sha(F/'probe11_H3_source_resolution_07.json')
    extra={}
    for r in data['source_constraints_to_add']:
        g,x=r['g'],r['KEEP'];s=int(old['local'][r['A_source']]);t=int(old['local'][r['A_target']])
        extra.setdefault((3,g,x),{}).setdefault((s,t),r['word_code_base12'])
    model=copy.copy(old);model['groups']=dict(old['groups']);count=0
    for key,rows in extra.items():
        a=np.array([(s,t,c) for (s,t),c in sorted(rows.items())],dtype=np.int32);model['groups'][key]=a;count+=len(a)
    model['stored_source_rows']+=count;model['H_counts']=dict(old['H_counts']);model['H_counts'][3]=count;model['H3_complete']=False
    model['source_status']='literal H1/H2 complete; independently replayed H3 subset';model['parent_model_sha256']=sha(F/'global_probe11_LOW_model.pkl')
    model['H3_audit_sha256']=sha(F/'independent_probe11_H3_source_07.json')
    modelpath=F/'global_probe11_LOW_H3_model.pkl'
    with modelpath.open('xb') as f:pickle.dump(model,f,protocol=5)
    todo=collections.deque(entry['pending']);inq=bytearray(entry['inqueue']);violations=seeded=0
    for (h,g,x),rows in extra.items():
        nsrc=len(model['classes'][g-1]);ntgt=len(model['classes'][x-1]);ns=1<<(nsrc-1).bit_length()
        for b in np.flatnonzero((model['roots']==g)&(model['B_Q'][:,x-1]>=3)).tolist():
            bt=int(model['B_destination'][b,x-1]);q=int(model['B_Q'][b,x-1]);bad=False
            for (s,t),code in rows.items():
                ds=point(entry['nodes'],entry['columns'][b],s,nsrc);dt=point(entry['nodes'],entry['columns'][bt],t,ntgt)
                if ds+q-6>dt:bad=True;violations+=1
            if bad and not inq[b]:inq[b]=1;todo.append(b);seeded+=1
    entry['pending']=todo;entry['inqueue']=inq;entry['status']='AUGMENTED_SOURCE_CHECKPOINT_NOT_COMPLETE';entry['source_model_sha256']=sha(modelpath)
    entry['H3_initial_violations']=violations;entry['new_H3_source_B_columns_seeded']=seeded
    entry['input_sha256']={'prior_checkpoint':sha(F/'global_probe11_DAG_07.pkl'),'H3_audit':sha(F/'independent_probe11_H3_source_07.json')}
    with (F/'global_probe11_H3_DAG_entry.pkl').open('xb') as f:pickle.dump(entry,f,protocol=5)
    report={'status':'ACTUAL_H3_ROWS_AUGMENTED_NOT_A_ROOT_PROOF','new_distinct_A_rows':count,'new_source_groups':len(extra),
      'initial_literal_inequality_violations':violations,'new_B_columns_seeded':seeded,'pending_B_columns':len(todo),
      'H3_complete':False,'source_queries':0,'source_engine_calls':0,'JR35':'OPEN',
      'input_sha256':{p:sha(F/p) for p in ('global_probe11_LOW_H3_model.pkl','global_probe11_H3_DAG_entry.pkl','independent_probe11_H3_source_07.json')}}
    with (F/'global_probe11_H3_augmentation.json').open('x',encoding='utf8') as f:json.dump(report,f,indent=2)
    print(json.dumps(report),flush=True);assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_proof243_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
