"""Sequential independent source inclusion check under the live-record cap."""
import hashlib,json,pickle,sys,time
from pathlib import Path
import numpy as np
F=Path(__file__).resolve().parent;B=F.parents[1]/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(x):return hashlib.sha256(pickle.dumps(x,protocol=5)).hexdigest()
def at(nodes,i,a,n):
    w=1<<(n-1).bit_length()
    while i>=0:
        x,y=nodes[i];h=w//2
        if a<h:i=x
        else:i=y;a-=h
        w=h
    return -i-1
def main():
    with (F/'global_probe11_LOW_H3_model.pkl').open('rb') as f:old=pickle.load(f)
    oldrows={k:(len(v),hashlib.sha256(v.tobytes()).hexdigest()) for k,v in old['groups'].items()}
    oldcount=old['stored_source_rows'];oldh=old['H_counts'][3];del old
    with (F/'global_probe11_H3_DAG_14.pkl').open('rb') as f:prior=pickle.load(f)
    ph={k:digest(prior[k]) for k in ('nodes','columns','parents','pending','inqueue')};assert not prior['pending'];del prior
    with (F/'global_probe11_LOW_H3B_model.pkl').open('rb') as f:new=pickle.load(f)
    acc=json.loads((F/'independent_probe11_H3_source_14.json').read_text())
    wanted={}
    for c in acc['controls']:
        w=c['reference'];k=(3,w['g'],w['KEEP']);a=int(new['local'][w['A_source']]);b=int(new['local'][w['A_target']])
        wanted.setdefault(k,{})
        wanted[k].setdefault((a,b),w['word_code_base12'])
    total=0;extra={}
    for k,rows in new['groups'].items():
        n,h=oldrows.get(k,(0,hashlib.sha256(b'').hexdigest()))
        assert hashlib.sha256(rows[:n].tobytes()).hexdigest()==h
        tail=rows[n:]
        if len(tail):
            assert k in wanted
            assert {(int(a),int(b)):int(c) for a,b,c in tail}==wanted[k]
            extra[k]=tail.copy();total+=len(tail)
        else:assert k not in wanted
    assert set(extra)==set(wanted) and set(oldrows)<=set(new['groups'])
    assert new['H_counts'][3]==oldh+total and new['stored_source_rows']==oldcount+total
    # Drop all old source rows before loading a second coefficient object.
    model={k:v for k,v in new.items() if k in ('classes','roots','B_Q','B_destination')};del new
    with (F/'global_probe11_H3B_DAG_entry.pkl').open('rb') as f:z=pickle.load(f)
    for k in ('nodes','columns','parents'):assert digest(z[k])==ph[k]
    pending=set(z['pending']);assert len(pending)==len(z['pending'])
    assert pending=={i for i,x in enumerate(z['inqueue']) if x}
    needed=set();count=0
    for (h,g,x),rows in extra.items():
        for bs in np.flatnonzero((model['roots']==g)&(model['B_Q'][:,x-1]>=3)).tolist():
            bt=int(model['B_destination'][bs,x-1]);q=int(model['B_Q'][bs,x-1])
            for a,b,c in rows:
                da=at(z['nodes'],z['columns'][bs],int(a),len(model['classes'][g-1]))
                db=at(z['nodes'],z['columns'][bt],int(b),len(model['classes'][x-1]))
                if da+q-6>db:needed.add(bs);count+=1
    assert pending==needed and count==z['H3_initial_violations']
    r={'status':'PASS_SOURCE_H3_AUGMENTATION_AND_ALL_NEEDED_QUEUE_SEEDS','new_distinct_A_rows':total,
      'new_groups':len(extra),'literal_initial_violations':count,'pending_B_columns':len(pending),
      'old_numerical_functions_and_source_rows_unchanged':True,'source_queries':0,'source_engine_calls':0,
      'H3_complete':False,'JR35':'OPEN','input_sha256':{p:sha(F/p) for p in (
        'global_probe11_LOW_H3B_model.pkl','global_probe11_H3B_DAG_entry.pkl','global_probe11_LOW_H3_model.pkl',
        'global_probe11_H3_DAG_14.pkl','independent_probe11_H3_source_14.json')}}
    with (F/'independent_probe11_H3B_augmentation.json').open('x',encoding='utf8') as f:json.dump(r,f,indent=2)
    print(json.dumps(r),flush=True);assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_verify134_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
