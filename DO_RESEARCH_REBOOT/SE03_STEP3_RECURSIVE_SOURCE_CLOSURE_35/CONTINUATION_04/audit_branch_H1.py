"""Independent symbolic-frame coverage; no new source-engine evaluation."""
import functools,hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1]
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time();M=set(range(1000,8000,1000))
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tup(t):return (t[0],tup(t[1]),tup(t[2])) if isinstance(t,list) else t
def reduce(t):
    if t is None:return None
    v,l,r=t[0],reduce(t[1]),reduce(t[2])
    if v in M:return (v,l,r)
    if l is None:return r
    if r is None:return l
    return (500+1000*sum(k<v for k in M),l,r)
def formula(t,x):
    # Literal instantiations of the six independently pinned root identities.
    g,l,r=t
    if l and l[0]==x:return (x,l[1],(g,l[2],r))
    if r and r[0]==x:return (x,(g,l,r[1]),r[2])
    if x<g:
        p,a,b=l
        if x<p:
            z,c,d=a;assert z==x;return (z,c,(p,d,(g,b,r)))
        z,c,d=b;assert z==x;return (z,(p,a,c),(g,d,r))
    p,a,b=r
    if x<p:
        z,c,d=a;assert z==x;return (z,(g,l,c),(p,d,b))
    z,c,d=b;assert z==x;return (z,(p,(g,l,a),c),d)
@functools.lru_cache(None)
def interval(a,b):
    if not a:return (None,)
    # a is a contiguous mark tuple; b is unused compatibility parameter.
    out=[]
    for i,key in enumerate(a):
        for l in interval(a[:i],0):
            for r in interval(a[i+1:],0):out.append((key,l,r))
    for i in range(1,len(a)):
        cut=(a[i-1]+a[i])//2
        for l in interval(a[:i],0):
            for r in interval(a[i:],0):out.append((cut,l,r))
    return tuple(out)
def values(t):return [] if t is None else values(t[1])+[t[0]]+values(t[2])
def main():
    c=read(F/'branch_H1_r7.json');native=read(B/'native10_source_actions.json')
    assert c['native_cache_sha256']==sha(B/'native10_source_actions.json')
    for p,h in c['input_sha256'].items():assert sha(F/p)==h
    expected={
      'L':(1,'$0',(2,'$1','$2')),
      'R':(2,(1,'$0','$1'),'$2'),
      'LL':(1,'$0',(2,'$1',(3,'$2','$3'))),
      'LR':(2,(1,'$0','$1'),(3,'$2','$3')),
      'RL':(2,(1,'$0','$1'),(3,'$2','$3')),
      'RR':(3,(2,(1,'$0','$1'),'$2'),'$3')}
    for name,v in c['templates'].items():
        assert tup(v['symbolic_output'])==expected[name]
        i,j,x=v['native_input'],v['native_output'],v['target_rank']
        assert native['destination'][i][x-1]==j and native['H'][i][x-1]==1
        src=tup(v['symbolic_input']);assert formula(src,x)==expected[name]
    aa=tuple(t for t in interval(tuple(sorted(M)),0) if t[0] in M)
    assert len(aa)==5947 and set(aa)==set(map(tup,c['A_branch_trees']))
    ids={t:i for i,t in enumerate(map(tup,c['A_branch_trees']))};relations=set();applications=0
    for t in aa:
        a=ids[t];targets=[]
        for side in (1,2):
            child=t[side]
            if child is None:continue
            if child[0] in M:targets.append(child[0])
            for s in (1,2):
                v=child[s]
                if v is not None and v[0] in M:targets.append(v[0])
        for x in targets:
            u=formula(t,x);relations.add((a,x//1000-1,ids[reduce(u)]));applications+=1
        for side in (1,2):
            child=t[side]
            if child is None or child[0] not in M:continue
            x=child[0];keys=values(child);bounds=(0,t[0]) if side==1 else (t[0],8000)
            variants=[]
            for orientation in (0,1):
                if orientation==0:
                    lo,hi=bounds[0],keys[0]
                    if hi-lo<2:continue
                    insert=((lo+hi)//2,None,child)
                else:
                    lo,hi=keys[-1],bounds[1]
                    if hi-lo<2:continue
                    insert=((lo+hi)//2,child,None)
                tt=(t[0],insert,t[2]) if side==1 else (t[0],t[1],insert)
                u=formula(tt,x);relations.add((a,x//1000-1,ids[reduce(u)]));applications+=1
    assert relations==set(map(tuple,c['H1_rows']))
    for row,w in zip(c['H1_rows'],c['witnesses']):
        a,x,b=row;src=tup(w['source']);dst=tup(w['target'])
        assert reduce(src)==tup(c['A_branch_trees'][a]) and formula(src,1000*(x+1))==dst
        assert reduce(dst)==tup(c['A_branch_trees'][b])
    # All B states are in the actual all-seven closed B component.
    bm=read(F/'active_a10_model.json');out=[[] for _ in range(3876)];back=[[] for _ in range(3876)]
    for e in bm['B_edges']:out[e['source']].append(e['target']);back[e['target']].append(e['source'])
    for adj in (out,back):
        seen={0};stack=[0]
        while stack:
            for t in adj[stack.pop()]:
                if t not in seen:seen.add(t);stack.append(t)
        assert len(seen)==3876
    r={'status':'PASS_SOURCE_UNIFORM_BRANCH_H1_COVERAGE','r':7,'branch_states':5947,'H1_rows':len(relations),
       'independent_symbolic_substitutions':applications,'source_queries':0,'source_engine_calls':0,
       'A_populations':'arbitrary, no cap on active unary ancestors or private inventories',
       'scope':'H1 source coverage only, not signed credit or quotient-path realizability',
       'B_all7_closed_component_checked':True,'JR35':'OPEN',
       'verification':'different interval grammar/explicit root identity instantiation and all witness reductions; cached primitive replay reused, same agent not external/formal',
       'input_sha256':{'branch_H1_r7.json':sha(F/'branch_H1_r7.json'),'SOURCE_CACHE_FRAME_LIFT.md':sha(F/'SOURCE_CACHE_FRAME_LIFT.md'),
         'C14_FULL_PROOF':sha(P/'SE03_STEP2_UNARY_A_LIFT_14/FULL_PROOF.md')}}
    with (F/'independent_branch_H1_audit.json').open('x',encoding='utf-8') as f:json.dump(r,f,indent=2)
    print(json.dumps({k:v for k,v in r.items() if k!='input_sha256'}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_verify105_exit.json').open('x',encoding='utf-8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
