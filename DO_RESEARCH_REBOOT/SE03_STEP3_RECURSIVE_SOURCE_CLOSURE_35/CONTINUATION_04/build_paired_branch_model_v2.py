import collections,hashlib,json,pickle,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1]
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    a=json.loads((F/'branch_H1_r7.json').read_text());h2=json.loads((F/'branch_H2_r7.json').read_text());b=json.loads((F/'active_a10_model.json').read_text())
    groups={};base={};row_by_source={}
    for h,rows in ((1,a['H1_rows']),(2,h2['H2_rows'])):
        for g in range(7):
            for x in range(7):
                data=[(s,t,rid) for rid,(s,k,t) in enumerate(rows) if a['A_roots'][s]==g and k==x]
                base[h,g,x]=data;d=collections.defaultdict(list)
                for s,t,rid in data:d[s].append((t,rid))
                row_by_source[h,g,x]=d
                if g!=x:groups['s',h,g,x]=[(s,t,(h,rid)) for s,t,rid in data]
    outgoing=[[] for _ in range(b['B_count'])]
    for eid,e in enumerate(b['B_edges']):outgoing[e['source']].append((eid,e))
    packets=[];six=followers=0
    for eid,e in enumerate(b['B_edges']):
        g=(b['B_roots'][e['source']]-1)//2;x=(e['key']-1)//2
        if e['q']!=6:
            packets.append({'kind':'singleton','source':e['source'],'target':e['target'],'Q':e['q'],
              'B_edges':[eid],'low':[(1,('s',1,g,x)),(2,('s',2,g,x))],'high_H':3})
            continue
        six+=1;assert outgoing[e['target']]
        for eid2,e2 in outgoing[e['target']]:
            assert e2['q']==1;followers+=1;y=(e2['key']-1)//2
            for total in (2,3):
                key=('p',total,g,x,y)
                if key in groups:continue
                candidates={}
                for ha,hb in (((1,1),) if total==2 else ((1,2),(2,1))):
                    for s,mid,rid1 in base[ha,g,x]:
                        for t,rid2 in row_by_source[hb,x,y].get(mid,()):candidates.setdefault((s,t),(ha,rid1,hb,rid2,mid))
                groups[key]=[(s,t,w) for (s,t),w in sorted(candidates.items())]
            packets.append({'kind':'pair_q6_q1','source':e['source'],'middle':e['target'],'target':e2['target'],'Q':7,
              'B_edges':[eid,eid2],'low':[(2,('p',2,g,x,y)),(3,('p',3,g,x,y))],'high_H':4})
    assert six==64 and followers>0
    edges=sum(len(v) for v in groups.values());assert edges<5000000 and edges<4000000
    out={'status':'COMPLETE_PAIRED_SOURCE_RELAXATION_CANDIDATE','A_count':5947,'A_roots':a['A_roots'],'B_roots':b['B_roots'],'B_count':3876,
      'groups':groups,'packets':packets,'stored_A_relation_edges':edges,'q6_rows':six,'q6_q1_sectors':followers,
      'source_queries':0,'source_engine_calls':0,'JR35':'OPEN','H2_independent_status':'PENDING',
      'input_sha256':{p:sha(F/p) for p in ('branch_H1_r7.json','branch_H2_r7.json','active_a10_model.json','PAIRED_BRANCH_SOURCE_BOX_V2.md')}}
    with (F/'paired_branch_model.pkl').open('xb') as f:pickle.dump(out,f,protocol=5)
    report={k:v for k,v in out.items() if k not in ('groups','packets','A_roots','B_roots')};report['packet_edges']=len(packets)
    with (F/'paired_branch_model.json').open('x',encoding='utf-8') as f:json.dump(report,f,indent=2)
    print(json.dumps(report),flush=True);assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_proof218_exit.json').open('x',encoding='utf-8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
