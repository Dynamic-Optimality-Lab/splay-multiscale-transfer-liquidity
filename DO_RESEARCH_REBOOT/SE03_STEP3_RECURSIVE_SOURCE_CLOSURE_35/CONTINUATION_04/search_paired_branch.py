"""Signed constraints for the complete all-A seven-key maximal-core model."""
import collections,hashlib,json,pickle,sys,time
from pathlib import Path
import numpy as np
F=Path(__file__).resolve().parent;P=F.parents[1]
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time();PHASE=sys.argv[3];BATCH=int(sys.argv[4])
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    with (F/'paired_branch_model.pkl').open('rb') as f:m=pickle.load(f)
    na,nb=m['A_count'],m['B_count'];classes=[[i for i,r in enumerate(m['A_roots']) if r==j] for j in range(7)]
    keys=list(m['groups']);gid={k:i for i,k in enumerate(keys)};groups=[]
    for key in keys:
        rows=m['groups'][key];s=np.array([r[0] for r in rows],dtype=np.int64);t=np.array([r[1] for r in rows],dtype=np.int64)
        lookup={(int(a),int(b)):i for i,(a,b) in enumerate(zip(s,t))};groups.append((s,t,lookup))
    adj=[[] for _ in range(nb)]
    for i,p in enumerate(m['packets']):adj[p['source']].append((i,p))
    if BATCH==1:
        floors=[0]*nb;rows=[{} for _ in range(nb)];rp=[{} for _ in range(nb)];fp=[None]*nb
        pending=collections.deque(range(nb));inq=bytearray([1])*nb;done=relax=cells=0;maxd=0;trigger=None
    else:
        with (F/f'paired_branch_search_{BATCH-1:02d}.pkl').open('rb') as f:z=pickle.load(f)
        assert z['status']=='CHECKPOINT' and z['model_sha256']==sha(F/'paired_branch_model.pkl')
        floors,rows,rp,fp=z['floors'],z['rows'],z['row_parents'],z['floor_parents'];pending=z['pending'];inq=z['inqueue']
        done,relax,cells,maxd,trigger=z['processed'],z['relaxations'],z['positive_cells'],z['max_D'],z['trigger']
    cycle=None;statecap=False
    def check_cycle(code):
        def pred(v):
            bb,aa=divmod(v,na);return rp[bb].get(aa,fp[bb])
        seen={};walk=[];u=code
        while u is not None and u not in seen and pred(u) is not None:
            seen[u]=len(walk);walk.append(u);u=pred(u)[0]
        if u not in seen:return None
        nodes=walk[seen[u]:];steps=[];weight=0
        for dst in nodes:
            src,h,pid,gg,ri=pred(dst);q=m['packets'][pid]['Q'];w=2*h-q;weight+=w
            steps.append({'source_code':src,'target_code':dst,'H':h,'Q':q,'weight':w,'packet':pid,
               'group':gg,'group_row':ri,'kind':'LOW_SOURCE_QUOTIENT' if gg>=0 else 'CONSERVATIVE_HIGH_ENDPOINT'})
        return {'nodes':nodes,'steps':steps,'weight':weight} if weight<0 else None
    while pending and time.process_time()-START<CAP-5:
        b=pending.popleft();inq[b]=0;f=floors[b];row=rows[b];g=(m['B_roots'][b]-1)//2
        values=np.full(na,f,dtype=np.int64)
        for a,v in row.items():values[a]=v
        ma=int(np.argmax(values));md=int(values[ma]);raised=False
        for pid,p in adj[b]:
            bt=p['target'];q=p['Q'];target=rows[bt];floor=floors[bt]
            for h,key in p['low']:
                gg=gid[key];src,dst,lookup=groups[gg]
                if not len(src):continue
                candidate=(values[src]+q-2*h+1000)*na+src
                best=np.full(na,-10**12,dtype=np.int64);np.maximum.at(best,dst,candidate)
                val=best//na-1000
                for t in np.flatnonzero(val>floor):
                    t=int(t);v=int(val[t])
                    if v>target.get(t,floor):
                        s=int(best[t]%na)
                        if t not in target:cells+=1
                        target[t]=v;rp[bt][t]=(b*na+s,h,pid,gg,lookup[s,t]);relax+=1
                        if v>maxd:maxd=v;trigger=bt*na+t;raised=True
                        if not inq[bt]:inq[bt]=1;pending.append(bt)
            h=p['high_H'];v=md+q-2*h
            if v>floors[bt]:
                floors[bt]=v;fp[bt]=(b*na+ma,h,pid,-1,-1);relax+=1
                drop=[t for t,vv in target.items() if vv<=v]
                for t in drop:del target[t];del rp[bt][t];cells-=1
                if v>maxd:maxd=v;trigger=bt*na+classes[(m['B_roots'][bt]-1)//2][0];raised=True
                if not inq[bt]:inq[bt]=1;pending.append(bt)
        done+=1
        if cells+na+nb>1800000:statecap=True;break
        if maxd>4 and (raised or done%1000==0):cycle=check_cycle(trigger)
        if cycle:break
    status='RELAXATION_REFUTED' if cycle else ('COMPLETE_CANDIDATE' if not pending else ('STATE_CAP_CHECKPOINT' if statecap else 'CHECKPOINT'))
    z={'status':status,'floors':floors,'rows':rows,'row_parents':rp,'floor_parents':fp,'pending':pending,'inqueue':inq,
      'processed':done,'relaxations':relax,'positive_cells':cells,'max_D':maxd,'trigger':trigger,'cycle':cycle,
      'model_sha256':sha(F/'paired_branch_model.pkl'),'source_queries':0,'source_engine_calls':0,'JR35':'OPEN'}
    with (F/f'paired_branch_search_{BATCH:02d}.pkl').open('xb') as f:pickle.dump(z,f,protocol=5)
    report={k:v for k,v in z.items() if k not in ('floors','rows','row_parents','floor_parents','pending','inqueue')}
    report.update({'pending_columns':len(pending),'direct_bank_bound_if_complete':maxd+8,
      'scope':'all seven-mark maximal BF sources, arbitrary A unary/private populations IF all source/independent interfaces pass',
      'H2_independent_status':'PENDING','numerical_independent_status':'PENDING',
      'negative_cycle_is_original_source_counterexample':False})
    with (F/f'paired_branch_search_{BATCH:02d}.json').open('x',encoding='utf-8') as f:json.dump(report,f,indent=2)
    print(json.dumps({k:v for k,v in report.items() if k!='cycle'}),flush=True)
    if cycle:print(json.dumps({'cycle_steps':len(cycle['steps']),'weight':cycle['weight'],'HIGH_steps':sum(e['group']<0 for e in cycle['steps'])}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/f'audit_{PHASE}_exit.json').open('x',encoding='utf-8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
