"""Actual native11 LOW search with exact subfunction DAG sharing."""
import collections,hashlib,json,pickle,sys,time
from pathlib import Path
import numpy as np
F=Path(__file__).resolve().parent;P=F.parents[1];sys.path.insert(0,str(F));B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
from probe11_decision_dag import DAG
CAP=float(sys.argv[1]);START=time.process_time();PHASE=sys.argv[3];BATCH=int(sys.argv[4])
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    with (F/'global_probe11_LOW_model.pkl').open('rb') as f:m=pickle.load(f)
    initial='global_probe11_DAG_entry.pkl' if BATCH==1 else f'global_probe11_DAG_{BATCH-1:02d}.pkl'
    with (F/initial).open('rb') as f:z=pickle.load(f)
    if BATCH==1:
        au=json.loads((F/'independent_probe11_DAG_conversion.json').read_text());assert au['input_sha256']['global_probe11_DAG_entry.pkl']==sha(F/initial)
    else:assert z['status']=='CHECKPOINT'
    dag=DAG(z['nodes'],z['nextid']);columns=z['columns'];todo=z['pending'];inq=z['inqueue'];parents=z['parents']
    processed,updates,maxd,tracking=(z[k] for k in ('processed','updates','max_D','tracking'));del z
    n=m['A_count'];nb=m['B_count'];roots=m['roots'];classes=m['classes'];groups=m['groups']
    dense=collections.OrderedDict();images=collections.OrderedDict();memo=collections.OrderedDict();densecells=imagecells=hits=0;cycle=None;limit=None
    def get_values(g,root):
        nonlocal densecells
        key=(g,root)
        if key in dense:v=dense.pop(key);dense[key]=v;return v
        v=dag.vector(root,len(classes[g-1]));dense[key]=v;densecells+=len(v)
        while densecells>60000:
            _,a=dense.popitem(last=False);densecells-=len(a)
        return v
    def schedule(b,root):
        if root==columns[b]:return
        columns[b]=root
        if not inq[b]:inq[b]=1;todo.append(b)
    def find_cycle(u):
        seen={};walk=[]
        while u not in seen and u in parents:
            seen[u]=len(walk);walk.append(u);p=parents[u];u=p[0]*n+int(classes[int(roots[p[0]])-1][p[1]])
            if len(walk)%10000==0 and time.process_time()-START>CAP-5:return None
        if u not in seen:return None
        out=[];wtotal=0
        for v in walk[seen[u]:]:
            b,a=divmod(v,n);bs,s,h,x,y=parents[v];asrc=int(classes[int(roots[bs])-1][s]);q=int(m['B_Q'][bs,x-1]);w=2*h-q;wtotal+=w
            assert int(m['B_destination'][bs,x-1])==b
            out.append({'B_source':bs,'B_target':b,'A_source':asrc,'A_target':a,'H':h,'Q':q,'helper_DELETE':y or None,'KEEP':x,'weight':w})
        return {'edges':list(reversed(out)),'weight':wtotal} if wtotal<0 else None
    while todo and time.process_time()-START<CAP-5:
        b=todo.popleft();inq[b]=0;g=int(roots[b]);source=columns[b];values=get_values(g,source);trigger=None
        for x in range(1,12):
            if x==g:continue
            bt=int(m['B_destination'][b,x-1]);q=int(m['B_Q'][b,x-1]);target=columns[bt];mk=(g,source,x,q,target)
            if not tracking and mk in memo:
                result=memo.pop(mk);memo[mk]=result
                if result<0 or result in dag.nodes:schedule(bt,result);hits+=1;continue
            ik=(g,source,x);nt=len(classes[x-1])
            if ik in images:base=images.pop(ik);images[ik]=base
            else:
                base=np.full(nt,-1000000,dtype=np.int32)
                for h in (1,2):
                    data=groups[h,g,x];np.maximum.at(base,data[:,1],values[data[:,0]]-2*h)
                images[ik]=base;imagecells+=nt
                while imagecells>180000:
                    _,v=images.popitem(last=False);imagecells-=len(v)
            before=get_values(x,target);candidate=base+q;changed=np.flatnonzero(candidate>before)
            if len(changed):
                vals=candidate[changed];maxd=max(maxd,int(vals.max()));updates+=len(changed)
                if maxd>8:tracking=True
                if tracking:
                    for t,v in zip(changed.tolist(),vals.tolist()):
                        options=[]
                        for h in (1,2):
                            data=groups[h,g,x];ok=(data[:,1]==t)&(values[data[:,0]]+q-2*h==v)
                            if np.any(ok):r=data[np.flatnonzero(ok)[0]];options.append((int(r[0]),h,int(r[2])))
                        assert options;s,h,y=options[0];code=bt*n+int(classes[x-1][t]);parents[code]=(b,s,h,x,y);trigger=code
                result=dag.changes(target,1<<(nt-1).bit_length(),changed,vals);schedule(bt,result)
            else:result=target
            if not tracking:
                memo[mk]=result
                if len(memo)>10000:memo.popitem(last=False)
        processed+=1
        if tracking and trigger is not None:cycle=find_cycle(trigger)
        if cycle:break
        if len(dag.nodes)>500000:dag.collect(columns)
        live=len(dag.nodes)+imagecells+densecells+len(memo)+n+nb+m['stored_source_rows']
        if live>1900000 or len(parents)>3900000 or 2*len(dag.nodes)+m['stored_source_rows']>3900000:
            dag.collect(columns)
            if len(dag.nodes)+imagecells+densecells+len(memo)+n+nb+m['stored_source_rows']>1900000:limit='LIVE_RECORD_CHECKPOINT';break
    dag.collect(columns)
    status='ACTUAL_SOURCE_NEGATIVE_CYCLE_CANDIDATE' if cycle else ('LOW_ALL_NATIVE11_COMPLETE' if not todo else 'CHECKPOINT')
    out={'status':status,'nodes':dag.nodes,'nextid':dag.nextid,'columns':columns,'pending':todo,'inqueue':inq,'parents':parents,
      'processed':processed,'updates':updates,'max_D':maxd,'tracking':tracking,'cycle':cycle,'limit':limit,'source_queries':0,'source_engine_calls':0,
      'source_model_sha256':sha(F/'global_probe11_LOW_model.pkl'),'JR35':'OPEN','root_or_HIGH_promotion':False}
    with (F/f'global_probe11_DAG_{BATCH:02d}.pkl').open('xb') as f:pickle.dump(out,f,protocol=5)
    report={k:v for k,v in out.items() if k not in ('nodes','nextid','columns','pending','inqueue','parents')}
    report.update({'DAG_nodes':len(dag.nodes),'pending_B_columns':len(todo),'numeric_merge_cache_hits':hits,
      'live_record_upper_bound_before_discarding_derived_caches':len(dag.nodes)+imagecells+densecells+len(memo)+n+nb+m['stored_source_rows']})
    with (F/f'global_probe11_DAG_{BATCH:02d}.json').open('x',encoding='utf8') as f:json.dump(report,f,indent=2)
    print(json.dumps({k:v for k,v in report.items() if k!='cycle'}),flush=True)
    if cycle:print(json.dumps({'weight':cycle['weight'],'edges':len(cycle['edges'])}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/f'audit_{PHASE}_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
