"""Independent all-concrete-edge verification of the nonlinear joint-depth table.

Reads the table only. Rebuilds all physical splay transitions with the pointer
engine, all features and all inequalities without the quotient generator or
its label-correction code. No finite-to-universal promotion.
"""
from pathlib import Path
from functools import lru_cache
from collections import Counter
import json,sys,time,hashlib
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
sys.path.insert(0,str(ROOT/'python'))
from liquidity import legacy_embedding as P
N=7

def ck(x,msg):
    if not x:raise AssertionError(msg)

@lru_cache(None)
def alltrees(lo,hi):
    if lo==hi:return (None,)
    return tuple((r,l,t) for r in range(lo,hi) for l in alltrees(lo,r) for t in alltrees(r+1,hi))

def pointer(t):
    if t is None:return None
    q=P.mknode(t[0],pointer(t[1]),pointer(t[2]))
    if q['l'] is not None:q['l']['p']=q
    if q['r'] is not None:q['r']['p']=q
    return q

def immutable(q):return None if q is None else (q['k'],immutable(q['l']),immutable(q['r']))
def raw(t):return None if t is None else [t[0],raw(t[1]),raw(t[2])]

def depths(t):
    out={};stack=[(t,0)]
    while stack:
        node,d=stack.pop()
        if node is None:continue
        k,l,r=node;out[k]=d;stack.append((l,d+1));stack.append((r,d+1))
    return [out[x] for x in range(1,N+1)]

def main():
    output=OUT/'independent_certificate_audit.json';ck(not output.exists(),'append-only audit exists')
    start=time.process_time();source=OUT/'finite_summary_potential.json';c=json.loads(source.read_text(encoding='utf-8'))
    ck(c['n']==N and c['all_size_claim']==False,'scope')
    table={tuple(f):v for f,v in zip(c['encoded_class_features'],c['labels'])}
    ck(len(table)==len(c['labels'])==90812,'all distinct complete feature keys')
    ck(min(table.values())==-3 and max(table.values())==0 and all(type(v) is int for v in table.values()),'exact label range')
    trees=alltrees(1,N+1);index={t:i for i,t in enumerate(trees)};m=len(trees)
    tr=[];ds=[];asteps=[];bdoubles=[]
    for i,t in enumerate(trees):
        tt=[];aa=[];qq=[]
        d=depths(t);ds.append(d)
        for x in range(1,N+1):
            q=pointer(t);after,events=P.splay_trace(q,x)
            tt.append(index[immutable(after)]);aa.append(len(events));qq.append(sum(e['case']!='ZIG' for e in events))
            ck(aa[-1]==(d[x-1]+1)//2 and qq[-1]==d[x-1]//2,'source event count')
        tr.append(tt);asteps.append(aa);bdoubles.append(qq)
    features=[];values=[]
    for ai,a in enumerate(trees):
        for bi,b in enumerate(trees):
            f=(a[0],b[0],*sorted(N*x+y for x,y in zip(ds[ai],ds[bi])))
            ck(f in table,('complete physical summary',ai,bi))
            features.append(f);values.append(table[f])
    checked=0;residuals=Counter();maximum=0
    for ai in range(m):
        for bi in range(m):
            u=ai*m+bi;ps=values[u]
            for k in range(N):
                an=tr[ai][k];a=asteps[ai][k]
                for keep in (False,True):
                    bn=tr[bi][k] if keep else bi;reward=(bdoubles[bi][k] if keep else 0)-2*a
                    residual=ps-values[an*m+bn]-reward
                    ck(residual>=0,('finite potential inequality',ai,bi,k,keep,residual))
                    residuals[residual]+=1;maximum=max(maximum,residual);checked+=1
        ck(time.process_time()-start<120,'UNKNOWN independent finite audit cap')
    ck(checked==2576574,'all concrete edges covered')
    old=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/run_20261030_v001/u4_counterexample_certificate.json'
    witness=json.loads(old.read_text(encoding='utf-8'));walk=[];total_reward=0;total_drop=0
    for r in witness['full_state_replay']:
        def decode(t):return None if t is None else (t[0],decode(t[1]),decode(t[2]))
        a0=decode(r['source_A']);b0=decode(r['source_B']);a1=decode(r['destination_A']);b1=decode(r['destination_B'])
        u=index[a0]*m+index[b0];v=index[a1]*m+index[b1]
        reward=r['q']-2*r['a'];drop=values[u]-values[v]
        ck(drop>=reward,('overwritten-setup potential',r['access']))
        walk.append({'access':r['access'],'operation':r['mode']+str(r['key']),'a':r['a'],'q':r['q'],
                     'potential_source':values[u],'potential_destination':values[v],'drop':drop,'reward':reward,'residual':drop-reward})
        total_reward+=reward;total_drop+=drop
    ck(total_reward==-16 and total_drop==0,'closed cyclic accounting')
    ck(walk[2]['drop']==3 and walk[2]['q']==3,'K7 fully paid by actual state potential')
    result={'status':'PASS_FINITE_EXACT','n':N,'all_size_proof':False,'source_certificate_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'pointer_shape_accesses_rederived':m*N,'physical_pairs':m*m,'summary_states':len(table),
            'concrete_edge_inequalities_checked':checked,'minimum_residual':min(residuals),'maximum_residual':maximum,
            'residual_histogram':dict(sorted(residuals.items())),'potential_range':[-3,0],
            'overwritten_setup_walk':walk,'closed_walk_reward':total_reward,'closed_walk_potential_drop':total_drop,
            'K7_potential_drop':3,'independence':'No quotient builder/solver or tuple transition engine imported. Pointer rotations, features, costs and all concrete inequalities regenerated.',
            'CPU_seconds':round(time.process_time()-start,3)}
    with output.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k not in ('overwritten_setup_walk','residual_histogram')},indent=2))

if __name__=='__main__':main()
