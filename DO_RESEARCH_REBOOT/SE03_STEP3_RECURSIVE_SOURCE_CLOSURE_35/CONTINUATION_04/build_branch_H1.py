"""Source-uniform branch H1 relation via certified symbolic cache frames.
No new source trace/splay evaluation. See SOURCE_CACHE_FRAME_LIFT first.
"""
import functools,hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1]
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time();R=7;M=set(range(1000,8000,1000))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def freeze(t):return tuple([t[0],freeze(t[1]),freeze(t[2])]) if isinstance(t,list) else t
@functools.lru_cache(None)
def family(lo,hi):
    if lo>hi:return (None,)
    a=[(1000*j,l,r) for j in range(lo,hi+1) for l in family(lo,j-1) for r in family(j+1,hi)]
    a.extend((1000*j+500,l,r) for j in range(lo,hi) for l in family(lo,j) for r in family(j+1,hi))
    return tuple(a)
def core_reduce(t):
    if t is None:return None
    l,r=core_reduce(t[1]),core_reduce(t[2]);v=t[0]
    if v in M:return (v,l,r)
    if l is None:return r
    if r is None:return l
    return (1000*sum(m<v for m in M)+500,l,r)
def path(t,x):
    dirs=[]
    while t[0]!=x:
        c=1 if x<t[0] else 2;dirs.append(c);t=t[c]
    return dirs
def replace_max(t,k,sub):
    if t is None:return None
    if t[0]==k:assert t[2] is None;return (t[0],t[1],sub)
    return (t[0],replace_max(t[1],k,sub),replace_max(t[2],k,sub))
def vine(lo):return None if lo>10 else (lo,None,vine(lo+1))
def material(t):
    counter=0
    def go(v):
        nonlocal counter
        if v is None:q='F'+str(counter);counter+=1;return q
        return (v[0],go(v[1]),go(v[2]))
    out=go(t);assert counter==11;return out
def main():
    native=json.loads((B/'native10_source_actions.json').read_text());trees=[freeze(t) for t in native['trees']];ni={t:i for i,t in enumerate(trees)}
    patterns=[('L',(2,(1,None,None),None),1,2),('R',(1,None,(2,None,None)),2,2),
      ('LL',(3,(2,(1,None,None),None),None),1,3),('LR',(3,(1,None,(2,None,None)),None),2,3),
      ('RL',(1,None,(3,(2,None,None),None)),2,3),('RR',(1,None,(2,None,(3,None,None))),3,3)]
    templates={}
    for name,bare,x,k in patterns:
        t=material(replace_max(bare,k,vine(k+1)));i=ni[t];j=native['destination'][i][x-1]
        assert native['H'][i][x-1]==1
        def strip(v):
            if isinstance(v,str):
                p=int(v[1:]);assert p<k;return '$'+str(p)
            if v[0]==k+1:return '$'+str(k)
            assert v[0]<=k;return (v[0],strip(v[1]),strip(v[2]))
        templates[name]={'native_input':i,'native_output':j,'target_rank':x,'operand_count':k,'H':1,
           'symbolic_input':strip(t),'symbolic_output':strip(trees[j])}
    applications=0
    def apply(t,x):
        nonlocal applications
        dd=path(t,x);assert 1<=len(dd)<=2
        name=''.join('L' if c==1 else 'R' for c in dd);spec=templates[name]
        active=[];u=t;active.append(u[0])
        for c in dd:u=u[c];active.append(u[0])
        ss=set(active);keys=sorted(active);ports=[]
        def collect(u):
            if u is None or u[0] not in ss:ports.append(u);return
            collect(u[1]);collect(u[2])
        collect(t);assert len(ports)==len(active)+1
        def instantiate(v):
            if isinstance(v,str):return ports[int(v[1:])]
            return (keys[v[0]-1],instantiate(v[1]),instantiate(v[2]))
        assert instantiate(spec['symbolic_input'])==t
        applications+=1;return instantiate(spec['symbolic_output']),name
    aa=[t for t in family(1,R) if t[0] in M];assert len(aa)==5947
    index={t:i for i,t in enumerate(aa)};rel={};operands=set()
    for a,t in enumerate(aa):
        for x in sorted(M-{t[0]}):
            dd=path(t,x)
            if len(dd)>2:continue
            u,name=apply(t,x);b=index[core_reduce(u)];key=(a,x//1000-1,b)
            rel.setdefault(key,{'source':t,'target':u,'template':name,'kind':'retained_path'})
            if len(dd)!=1:continue
            side=dd[0];sub=t[side];values=[]
            def inorder(v):
                if v is not None:inorder(v[1]);values.append(v[0]);inorder(v[2])
            inorder(sub);lo,hi=(0,t[0]) if side==1 else (t[0],8000)
            choices=[]
            if lo+1<min(values):choices.append(((lo+min(values))//2,None,sub))
            if max(values)+1<hi:choices.append(((max(values)+hi)//2,sub,None))
            for new in choices:
                tt=(t[0],new,t[2]) if side==1 else (t[0],t[1],new)
                u,name=apply(tt,x);b=index[core_reduce(u)];key=(a,x//1000-1,b)
                rel.setdefault(key,{'source':tt,'target':u,'template':name,'kind':'one_active_unary'})
        if a%100==0:assert time.process_time()-START<CAP-2
    rows=sorted(rel);out={'status':'COMPLETE_SOURCE_H1_BRANCH_RELATION_PENDING_INDEPENDENT_AUDIT','r':R,
      'A_branch_trees':aa,'A_roots':[t[0]//1000-1 for t in aa],'H1_rows':rows,
      'witnesses':[rel[k] for k in rows],'templates':templates,'symbolic_cache_substitutions':applications,
      'source_engine_calls':0,'source_queries':0,'JR35':'OPEN',
      'source_scope':'all seven-mark original A H1 macros, arbitrary anonymous unary populations and private BSTs, full marked-rooted branch quotient',
      'not_a_path_realization_bridge':True,
      'input_sha256':{'SOURCE_CACHE_FRAME_LIFT.md':sha(F/'SOURCE_CACHE_FRAME_LIFT.md')},
      'native_cache_sha256':sha(B/'native10_source_actions.json')}
    with (F/'branch_H1_r7.json').open('x',encoding='utf-8') as f:json.dump(out,f)
    print(json.dumps({k:out[k] for k in ('status','r','symbolic_cache_substitutions','source_queries','source_scope')}),flush=True)
    print(json.dumps({'branch_shapes':len(aa),'H1_rows':len(rows)}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_proof208_exit.json').open('x',encoding='utf-8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
