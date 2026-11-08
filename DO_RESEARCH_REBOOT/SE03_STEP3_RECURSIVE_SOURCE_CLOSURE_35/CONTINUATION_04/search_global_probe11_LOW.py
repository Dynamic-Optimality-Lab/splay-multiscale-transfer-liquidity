"""Literal all-B/full-A LOW cycles; exact immutable profile interning.
Profiles share ONLY equal numeric functions on the SAME root class.
Source states and their actual eligibility/edges are never identified.
Parent recording starts after value8 only as a tracing optimization, not
as a bound or an impossibility certificate. A reported cycle is checked
with literal original A/B endpoints and physical costs.
"""
import collections,hashlib,json,pickle,sys,time
from pathlib import Path
import numpy as np
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time();PHASE=sys.argv[3];BATCH=int(sys.argv[4])
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    with (F/'global_probe11_LOW_model.pkl').open('rb') as f:m=pickle.load(f)
    n=m['A_count'];nb=m['B_count'];groups=m['groups'];classes=m['classes'];roots=m['roots']
    if BATCH==1:
        profiles={g:(g,()) for g in range(1,12)};intern={v:k for k,v in profiles.items()};refs={g:int((roots==g).sum()) for g in range(1,12)}
        columns=roots.astype(np.int64).tolist();pidnext=12;todo=collections.deque(range(nb));inq=bytearray([1])*nb;cells=processed=updates=0;maxd=0;tracking=False;parents={};parentcells=0
    else:
        with (F/f'global_probe11_LOW_{BATCH-1:02d}.pkl').open('rb') as f:z=pickle.load(f)
        assert z['status']=='CHECKPOINT'
        profiles,intern,refs,columns,pidnext,todo,inq,cells,processed,updates,maxd,tracking,parents,parentcells=(z[k] for k in
         ('profiles','intern','refs','columns','pidnext','pending','inqueue','unique_positive_cells','processed','updates','max_D','tracking','parents','parent_cells'))
    cycle=None;limit=None
    def replace(b,values):
        nonlocal pidnext,cells
        key=(int(roots[b]),tuple(sorted(values.items())));old=columns[b]
        if key==profiles[old]:return
        if key in intern:pid=intern[key];refs[pid]+=1
        else:pid=pidnext;pidnext+=1;intern[key]=pid;profiles[pid]=key;refs[pid]=1;cells+=len(key[1])
        columns[b]=pid;refs[old]-=1
        if refs[old]==0:
            keyold=profiles.pop(old);del intern[keyold];del refs[old];cells-=len(keyold[1])
    def cycle_from(u):
        seen={};walk=[]
        while u not in seen and u in parents:
            seen[u]=len(walk);walk.append(u);b,a=divmod(u,n);p=parents[u];u=p[0]*n+int(classes[int(roots[p[0]])-1][p[1]])
            if len(walk)%10000==0 and time.process_time()-START>CAP-5:return None
        if u not in seen:return None
        nodes=walk[seen[u]:];out=[];weight=0
        for v in nodes:
            b,a=divmod(v,n);bs,sl,h,x,y=parents[v];asrc=int(classes[int(roots[bs])-1][sl]);w=2*h-int(m['B_Q'][bs,x-1]);weight+=w
            assert int(m['B_destination'][bs,x-1])==b
            out.append({'B_source':bs,'B_target':b,'A_source':asrc,'A_target':a,'H':h,'Q':int(m['B_Q'][bs,x-1]),
              'helper_DELETE':y or None,'KEEP':x,'weight':w})
        return {'edges':list(reversed(out)),'weight':weight,'same_actual_A_B_endpoints':True} if weight<0 else None
    while todo and time.process_time()-START<CAP-5:
        b=todo.popleft();inq[b]=0;g=int(roots[b]);cl=classes[g-1];ns=len(cl);values=np.zeros(ns,dtype=np.int64)
        for a,v in profiles[columns[b]][1]:values[a]=v
        trigger=None
        for x in range(1,12):
            if x==g:continue
            bt=int(m['B_destination'][b,x-1]);q=int(m['B_Q'][b,x-1]);target=dict(profiles[columns[bt]][1]);nt=len(classes[x-1]);changed=False
            for h in (1,2):
                data=groups[h,g,x];src,dst,helpers=data[:,0],data[:,1],data[:,2]
                candidate=(values[src]+q-2*h+1000)*ns+src;best=np.full(nt,-10**15,dtype=np.int64);np.maximum.at(best,dst,candidate)
                vv=best//ns-1000
                for t in np.flatnonzero(vv>0):
                    t=int(t);v=int(vv[t])
                    if v<=target.get(t,0):continue
                    target[t]=v;changed=True;updates+=1
                    if v>maxd:maxd=v
                    if maxd>8:tracking=True
                    if tracking:
                        s=int(best[t]%ns);rid=int(np.flatnonzero((src==s)&(dst==t))[0]);code=bt*n+int(classes[x-1][t])
                        if code not in parents:parentcells+=1
                        parents[code]=(b,s,h,x,int(helpers[rid]));trigger=code
            if changed:
                replace(bt,target)
                if not inq[bt]:inq[bt]=1;todo.append(bt)
            if cells+len(profiles)+n+nb>1850000 or parentcells>3900000:limit='RECORD_CAP_CHECKPOINT';break
        processed+=1
        if tracking and trigger is not None:cycle=cycle_from(trigger)
        if cycle or limit:break
    status='ACTUAL_SOURCE_NEGATIVE_CYCLE_CANDIDATE' if cycle else ('LOW_ALL_NATIVE11_COMPLETE' if not todo else 'CHECKPOINT')
    z={'status':status,'profiles':profiles,'intern':intern,'refs':refs,'columns':columns,'pidnext':pidnext,'pending':todo,'inqueue':inq,
      'unique_positive_cells':cells,'processed':processed,'updates':updates,'max_D':maxd,'tracking':tracking,'parents':parents,'parent_cells':parentcells,
      'cycle':cycle,'limit':limit,'source_queries':0,'source_engine_calls':0,'model_sha256':sha(F/'global_probe11_LOW_model.pkl'),'JR35':'OPEN'}
    with (F/f'global_probe11_LOW_{BATCH:02d}.pkl').open('xb') as f:pickle.dump(z,f,protocol=5)
    report={k:v for k,v in z.items() if k not in ('profiles','intern','refs','columns','pidnext','pending','inqueue','parents')}
    report.update({'unique_profiles':len(profiles),'pending_B_columns':len(todo),'implicit_synchronized_pairs':sum(int((roots==g).sum())**2 for g in range(1,12)),
      'proof_from_passing_finite_population_search':False,'parents_omitted_before_trigger_does_not_bound_potential':True})
    with (F/f'global_probe11_LOW_{BATCH:02d}.json').open('x',encoding='utf8') as f:json.dump(report,f,indent=2)
    print(json.dumps({k:v for k,v in report.items() if k!='cycle'}),flush=True)
    if cycle:print(json.dumps({'weight':cycle['weight'],'edges':len(cycle['edges'])}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/f'audit_{PHASE}_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
