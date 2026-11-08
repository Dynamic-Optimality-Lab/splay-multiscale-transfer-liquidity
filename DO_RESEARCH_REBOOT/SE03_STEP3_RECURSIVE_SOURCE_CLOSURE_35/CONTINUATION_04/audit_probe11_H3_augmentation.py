"""Independent source inclusion and incremental-queue audit; no fresh splays."""
import hashlib,json,pickle,sys,time
from pathlib import Path
import numpy as np
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read_value(nodes,i,a,width):
    if i<0:return -i-1
    l,r=nodes[i];half=width//2
    return read_value(nodes,l,a,half) if a<half else read_value(nodes,r,a-half,half)
def main():
    with (F/'global_probe11_LOW_model.pkl').open('rb') as f:old=pickle.load(f)
    with (F/'global_probe11_LOW_H3_model.pkl').open('rb') as f:new=pickle.load(f)
    with (F/'global_probe11_DAG_07.pkl').open('rb') as f:prior=pickle.load(f)
    with (F/'global_probe11_H3_DAG_entry.pkl').open('rb') as f:entry=pickle.load(f)
    accepted=json.loads((F/'independent_probe11_H3_source_07.json').read_text());witnesses=accepted['controls'];words={};wanted={}
    for control in witnesses:
        w=control['reference'];g,x=w['g'],w['KEEP'];s=int(old['local'][w['A_source']]);t=int(old['local'][w['A_target']]);code=1
        for op in w['A_word']:code=12*code+op['key']
        assert code==w['word_code_base12'];words.setdefault((3,g,x),set()).add((s,t,code));wanted.setdefault((3,g,x),set()).add((s,t))
    for key,rows in old['groups'].items():assert np.array_equal(rows,new['groups'][key])
    assert {k for k in new['groups'] if k[0]==3}==set(wanted);count=0
    for key,rows in new['groups'].items():
        if key[0]!=3:continue
        assert {(int(s),int(t)) for s,t,c in rows}==wanted[key] and all(tuple(map(int,row)) in words[key] for row in rows);count+=len(rows)
    assert count==new['H_counts'][3] and new['stored_source_rows']==old['stored_source_rows']+count
    assert prior['nodes']==entry['nodes'] and prior['columns']==entry['columns'] and prior['parents']==entry['parents']
    before=list(prior['pending']);after=list(entry['pending']);assert after[:len(before)]==before and len(set(after))==len(after)
    assert {i for i,v in enumerate(entry['inqueue']) if v}==set(after)
    violating=set();violations=0
    for (h,g,x),rows in new['groups'].items():
        if h!=3:continue
        ns=len(new['classes'][g-1]);nt=len(new['classes'][x-1]);ws=1<<(ns-1).bit_length();wt=1<<(nt-1).bit_length()
        for b in np.flatnonzero((new['roots']==g)&(new['B_Q'][:,x-1]>=3)).tolist():
            bt=int(new['B_destination'][b,x-1]);q=int(new['B_Q'][b,x-1])
            for s,t,c in rows:
                ds=read_value(prior['nodes'],prior['columns'][b],int(s),ws);dt=read_value(prior['nodes'],prior['columns'][bt],int(t),wt)
                if ds+q-6>dt:violating.add(b);violations+=1
    assert violating<=set(after) and violations==entry['H3_initial_violations']
    out={'status':'PASS_SOURCE_H3_AUGMENTATION_AND_ALL_NEEDED_QUEUE_SEEDS','new_distinct_A_rows':count,'literal_initial_violations':violations,
      'violating_source_B_columns':len(violating),'pending_B_columns':len(after),'old_numerical_functions_and_source_rows_unchanged':True,
      'source_queries':0,'source_engine_calls':0,'H3_complete':False,'JR35':'OPEN',
      'input_sha256':{p:sha(F/p) for p in ('global_probe11_LOW_H3_model.pkl','global_probe11_H3_DAG_entry.pkl','global_probe11_LOW_model.pkl','global_probe11_DAG_07.pkl','independent_probe11_H3_source_07.json')}}
    with (F/'independent_probe11_H3_augmentation.json').open('x',encoding='utf8') as f:json.dump(out,f,indent=2)
    print(json.dumps(out),flush=True);assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_verify123_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
