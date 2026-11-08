"""Use realizable LOW two-macro witnesses, rather than quotient chaining."""
import collections,hashlib,json,pickle,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1];sys.path.insert(0,str(F))
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
from cached_low_frames import Frames,freeze,node
CAP=float(sys.argv[1]);START=time.process_time();M=set(range(1000,8000,1000))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def reduce(t):
    if not node(t):return None
    v,l,r=t[0],reduce(t[1]),reduce(t[2])
    if v in M:return (v,l,r)
    if l is None:return r
    if r is None:return l
    return (1000*sum(m<v for m in M)+500,l,r)
def main():
    a=json.loads((F/'branch_H1_r7.json').read_text());a2=json.loads((F/'branch_H2_r7.json').read_text())
    ids={freeze(t):i for i,t in enumerate(a['A_branch_trees'])};frames=Frames(B/'native10_source_actions.json')
    with (F/'paired_branch_model.pkl').open('rb') as f:pm=pickle.load(f)
    wanted={key for p in pm['packets'] for h,key in p['low'] if p['kind']=='pair_q6_q1'}
    groups={}
    for h,src in ((1,a),(2,a2)):
        for rid,(s,x,t) in enumerate(src[f'H{h}_rows']):
            key=('s',h,a['A_roots'][s],x);groups.setdefault(key,[]).append((s,t,('single',h,rid)))
    pairs={key:{} for key in wanted}
    for h,src in ((1,a),(2,a2)):
        for rid,(s,x,t) in enumerate(src[f'H{h}_rows']):
            g=a['A_roots'][s]
            if not any(('p',total,g,x,y) in wanted for total in (2,3) for y in range(7)):continue
            mid=freeze(src['witnesses'][rid]['target'])
            for y in range(7):
                if y==x:continue
                key1=('p',h+1,g,x,y);key2=('p',h+2,g,x,y)
                if key1 not in wanted and key2 not in wanted:continue
                d=len(frames.path(mid,1000*(y+1)))
                if not 1<=d<=4:continue
                hh=(d+1)//2;key=('p',h+hh,g,x,y)
                if key not in wanted:continue
                end,cost=frames.apply(mid,1000*(y+1));assert cost==hh
                t2=ids[reduce(end)]
                pairs[key].setdefault((s,t2),('actual_pair',h,rid,hh,y,t))
            if rid%1000==0:assert time.process_time()-START<CAP-3
    for key,data in pairs.items():groups[key]=[(s,t,w) for (s,t),w in sorted(data.items())]
    out={'status':'ACTUAL_SOURCE_PACKET_SUBRELATION','groups':groups,'packets':pm['packets'],
      'cached_source_substitutions':frames.applications,'source_queries':0,'source_engine_calls':0,
      'pair_scope':'first macro is a complete pinned LOW source witness; second is its literal KEEP at actual depth1..4',
      'source_complete':False,'sufficient_for_information_class_refutation':True,
      'input_sha256':{p:sha(F/p) for p in ('branch_H1_r7.json','branch_H2_r7.json','paired_branch_model.pkl','leaf_profile_inputs.pkl')}}
    with (F/'real_leaf_profile_packets.pkl').open('xb') as f:pickle.dump(out,f,protocol=5)
    report={k:v for k,v in out.items() if k not in ('groups','packets')}
    report.update({'stored_source_edges':sum(len(v) for v in groups.values()),'pair_source_edges':sum(len(v) for k,v in groups.items() if k[0]=='p')})
    with (F/'real_leaf_profile_packets.json').open('x',encoding='utf8') as f:json.dump(report,f,indent=2)
    print(json.dumps(report),flush=True);assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_proof224_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
