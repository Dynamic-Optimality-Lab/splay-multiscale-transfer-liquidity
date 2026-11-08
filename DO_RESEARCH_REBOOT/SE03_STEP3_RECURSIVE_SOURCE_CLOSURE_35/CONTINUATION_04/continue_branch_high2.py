"""Resume proof209; preserve explicit conservative-HIGH2 status."""
import collections,hashlib,json,pickle,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1]
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time();PHASE=sys.argv[3];BATCH=int(sys.argv[4])
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    a=json.loads((F/'branch_H1_r7.json').read_text());m=json.loads((F/'active_a10_model.json').read_text());na=len(a['A_branch_trees']);nb=m['B_count']
    classes=[[i for i,r in enumerate(a['A_roots']) if r==j] for j in range(7)];by=[[[] for j in range(7)] for r in range(7)]
    for rid,(s,x,t) in enumerate(a['H1_rows']):by[a['A_roots'][s]][x].append((s,t,rid))
    be=[[] for _ in range(nb)]
    for eid,e in enumerate(m['B_edges']):be[e['source']].append((e['target'],(e['key']-1)//2,e['q'],eid))
    previous='branch_high2_result.pkl' if BATCH==2 else f'branch_high2_{BATCH-1:02d}.pkl'
    with (F/previous).open('rb') as f:z=pickle.load(f)
    assert z['status']=='CPU_CHECKPOINT'
    for p,h in z['input_sha256'].items():assert sha(F/p)==h
    floors,rows,rp,fp=z['floors'],z['rows'],z['row_parents'],z['floor_parents']
    pending=z['pending'];inq=bytearray(nb)
    for b in pending:inq[b]=1
    done,relax,maxd,cells=z['processed'],z['relaxations'],z['max_D'],z['positive_exception_cells'];cycle=None;capstop=False
    trigger=None
    for b in range(nb):
        if floors[b]==maxd:trigger=b*na+classes[(m['B_roots'][b]-1)//2][0];break
        for aa,v in rows[b].items():
            if v==maxd:trigger=b*na+aa;break
        if trigger is not None:break
    def check_cycle(trigger):
        def pred(code):
            bb,aa=divmod(code,na);return rp[bb].get(aa,fp[bb])
        seen={};walk=[];u=trigger
        while u is not None and u not in seen and pred(u) is not None:
            seen[u]=len(walk);walk.append(u);u=pred(u)[0]
        if u not in seen:return None
        nodes=walk[seen[u]:];steps=[];weight=0
        for vtx in nodes:
            src,h,eid,rid=pred(vtx);e=m['B_edges'][eid];w=2*h-e['q'];weight+=w
            steps.append({'source_code':src,'target_code':vtx,'H':h,'q':e['q'],'weight':w,
              'B_edge_index':eid,'H1_row_index':rid,'kind':'EXACT_SOURCE_H1_QUOTIENT' if h==1 else 'CONSERVATIVE_HIGH2_ARBITRARY_ENDPOINT'})
        return {'nodes':nodes,'steps':steps,'weight':weight} if weight<0 else None
    cycle=check_cycle(trigger)
    while not cycle and pending and time.process_time()-START<CAP-4:
        b=pending.popleft();inq[b]=0;g=(m['B_roots'][b]-1)//2;f=floors[b];row=rows[b]
        ma,md=max(row.items(),key=lambda p:p[1]) if row else (classes[g][0],f)
        raised=False
        for bt,x,q,eid in be[b]:
            target=rows[bt];old=floors[bt]
            for s,t,rid in by[g][x]:
                v=row.get(s,f)+q-2
                if v>target.get(t,old):
                    if t not in target:cells+=1
                    target[t]=v;rp[bt][t]=(b*na+s,1,eid,rid);relax+=1
                    if v>maxd:maxd=v;trigger=bt*na+t;raised=True
                    if not inq[bt]:inq[bt]=1;pending.append(bt)
            v=md+q-4
            if v>floors[bt]:
                floors[bt]=v;fp[bt]=(b*na+ma,2,eid,-1);relax+=1
                drop=[t for t,w in target.items() if w<=v]
                for t in drop:del target[t];del rp[bt][t];cells-=1
                if v>maxd:maxd=v;trigger=bt*na+classes[x][0];raised=True
                if not inq[bt]:inq[bt]=1;pending.append(bt)
        done+=1
        if cells+na+nb>1800000:capstop=True;break
        if raised or done%1000==0:cycle=check_cycle(trigger)
    status='RELAXATION_REFUTED' if cycle else ('COMPLETE_CANDIDATE' if not pending else ('STATE_CAP_CHECKPOINT' if capstop else 'CPU_CHECKPOINT'))
    z.update({'status':status,'floors':floors,'rows':rows,'row_parents':rp,'floor_parents':fp,'pending':pending,
      'processed':done,'relaxations':relax,'max_D':maxd,'positive_exception_cells':cells,'cycle':cycle})
    with (F/f'branch_high2_{BATCH:02d}.pkl').open('xb') as f:pickle.dump(z,f,protocol=5)
    report={k:v for k,v in z.items() if k not in ('floors','rows','row_parents','floor_parents','pending')}
    report['meaning']='conservative quotient model only; not an original-source or CD refutation'
    with (F/f'branch_high2_{BATCH:02d}.json').open('x',encoding='utf-8') as f:json.dump(report,f,indent=2)
    print(json.dumps({k:v for k,v in report.items() if k not in ('cycle','input_sha256')}),flush=True)
    if cycle:print(json.dumps({'cycle_steps':len(cycle['steps']),'weight':cycle['weight'],'HIGH2_edges':sum(e['H']==2 for e in cycle['steps'])}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/f'audit_{PHASE}_exit.json').open('x',encoding='utf-8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
