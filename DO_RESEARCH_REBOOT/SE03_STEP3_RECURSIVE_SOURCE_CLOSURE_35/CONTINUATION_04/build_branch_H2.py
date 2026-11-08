"""Complete C14 LOW2 grammar with seven marks and cached source identities."""
import hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1];sys.path.insert(0,str(F))
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
from cached_low_frames import Frames,freeze,node
CAP=float(sys.argv[1]);START=time.process_time();M=set(range(1000,8000,1000))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def vals(t):return [] if not node(t) else vals(t[1])+[t[0]]+vals(t[2])
def canonical(t,selected):
    mp={x:x for x in M};groups={}
    for x in vals(t):
        if x not in M:groups.setdefault(sum(m<x for m in M),[]).append(x)
    for g,ks in groups.items():
        for j,x in enumerate(ks):mp[x]=1000*g+1000*(j+1)//(len(ks)+1)
    i=0
    def go(v):
        nonlocal i
        if not node(v):s='F'+str(i);i+=1;return s
        return (mp[v[0]],go(v[1]),go(v[2]))
    return go(t),mp[selected]
def get(t,path):
    for c in path:t=t[c]
    return t
def put(t,path,v):
    if not path:return v
    c=path[0];return (t[0],put(t[1],path[1:],v),t[2]) if c==1 else (t[0],t[1],put(t[2],path[1:],v))
def bound(t,path):
    lo,hi=0,8000
    for c in path:
        if c==1:hi=t[0]
        else:lo=t[0]
        t=t[c]
    return lo,hi
def subpaths(t,p=()):
    if not node(t):return []
    return [(p,t)]+subpaths(t[1],p+(1,))+subpaths(t[2],p+(2,))
def leaves(t,p=()):
    if not node(t):return [(p,t)]
    return leaves(t[1],p+(1,))+leaves(t[2],p+(2,))
def hasmark(t):return any(v in M for v in vals(t))
def insertions(t,path):
    if not path:return []
    sub=get(t,path)
    if not node(sub) or not hasmark(sub):return []
    lo,hi=bound(t,path);kk=vals(sub);out=[]
    if max(kk)+1<hi:
        u=(max(kk)+hi)//2;out.append((put(t,path,(u,sub,'new')),u))
    if lo+1<min(kk):
        u=(lo+min(kk))//2;out.append((put(t,path,(u,'new',sub)),u))
    return out
def reduce(t):
    if not node(t):return None
    l,r=reduce(t[1]),reduce(t[2]);v=t[0]
    if v in M:return (v,l,r)
    if l is None:return r
    if r is None:return l
    return (1000*sum(m<v for m in M)+500,l,r)
def main():
    frames=Frames(B/'native10_source_actions.json');old=json.loads((F/'branch_H1_r7.json').read_text());aa=[freeze(t) for t in old['A_branch_trees']];ids={t:i for i,t in enumerate(aa)}
    def decorations(t,x,cap):
        t,x=canonical(t,x);todo=[(t,x)];seen=set(todo);out=[]
        while todo:
            tt,y=todo.pop();dd=frames.path(tt,y)
            if len(dd)>cap:continue
            out.append((tt,y))
            if len(dd)==cap:continue
            for j in range(1,len(dd)+1):
                for ttt,u in insertions(tt,dd[:j]):
                    ttt,yy=canonical(ttt,y)
                    if (ttt,yy) not in seen:seen.add((ttt,yy));todo.append((ttt,yy))
        return out
    rel={};contexts=0
    def save(a,T,accesses,end,kind):
        key=(a,accesses[-1]//1000-1,ids[reduce(end)])
        if key not in rel:rel[key]={'source':T,'accesses':accesses,'target':end,'kind':kind}
    for a,raw in enumerate(aa):
        T,g=canonical(raw,raw[0])
        for x in sorted(M-{g}):
            for tt,xx in decorations(T,x,4):
                if len(frames.path(tt,xx)) not in (3,4):continue
                end,h=frames.apply(tt,xx);assert h==2;save(a,tt,[xx],end,'single_depth3_or4')
        first={}
        def add(tt,y,kind):
            tt,yy=canonical(tt,y)
            if 1<=len(frames.path(tt,yy))<=2:first[tt,yy]=kind
        for y in vals(T):
            if y==g:continue
            for tt,yy in decorations(T,y,2):add(tt,yy,'known_core')
        for path,sub in subpaths(T):
            if not 1<=len(path)<=2:continue
            for tt,y in insertions(T,path):
                for ttt,yy in decorations(tt,y,2):add(ttt,yy,'old_unary_target')
                if len(path)==1:
                    u=get(tt,path);private=1 if not node(u[1]) else 2;pp=path+(private,);lo,hi=bound(tt,pp)
                    add(put(tt,pp,((lo+hi)//2,'a','b')),(lo+hi)//2,'private_child_of_old_unary_parent')
        for path,sub in leaves(T):
            if not 1<=len(path)<=2:continue
            lo,hi=bound(T,path);mid=(lo+hi)//2;q1=lo+(hi-lo)//3;q2=lo+2*(hi-lo)//3
            add(put(T,path,(mid,'a','b')),mid,'private_root')
            if len(path)==1:
                add(put(T,path,(q2,(q1,'a','b'),'c')),q1,'private_left_grandchild')
                add(put(T,path,(q1,'a',(q2,'b','c'))),q2,'private_right_grandchild')
        contexts+=len(first)
        for (tt,y),kind in first.items():
            dd=frames.path(tt,y);active={tt[0]};v=tt
            for c in dd:v=v[c];active.add(v[0])
            middle,h=frames.apply(tt,y);assert h==1
            for x in sorted(M-{g}):
                path=frames.path(middle,x)
                if not 1<=len(path)<=2:continue
                end,h=frames.apply(middle,x);assert h==1;save(a,tt,[y,x],end,kind)
                if len(path)!=1:continue
                sub=get(middle,path)
                if set(vals(sub))&active or not hasmark(sub):continue
                orig=frames.path(tt,sub[0]);assert get(tt,orig)==sub
                for ttt,u in insertions(tt,orig):
                    ttt,yy=canonical(ttt,y);mid,h=frames.apply(ttt,yy);assert h==1
                    end,h=frames.apply(mid,x);assert h==1;save(a,ttt,[yy,x],end,'second_rigid_hanger_unary')
        if a%50==0:assert time.process_time()-START<CAP-3
    keys=sorted(rel);out={'status':'COMPLETE_SOURCE_H2_BRANCH_RELATION_PENDING_INDEPENDENT_AUDIT','r':7,'H2_rows':keys,
      'witnesses':[rel[k] for k in keys],'symbolic_cached_access_instances':frames.applications,'first_frame_contexts':contexts,
      'source_queries':0,'source_engine_calls':0,'JR35':'OPEN',
      'source_scope':'all original seven-mark H2 natural macros, arbitrary anonymous ancestors/helpers/private BSTs; necessary branch quotient',
      'input_sha256':{p:sha(F/p) for p in ('branch_H1_r7.json','SOURCE_LOW2_CACHE_LIFT.md','cached_low_frames.py')},
      'native_cache_sha256':frames.cache_sha256}
    with (F/'branch_H2_r7.json').open('x',encoding='utf-8') as f:json.dump(out,f)
    print(json.dumps({k:out[k] for k in ('status','symbolic_cached_access_instances','first_frame_contexts','source_queries')}),flush=True)
    print(json.dumps({'H2_rows':len(keys)}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_proof213_exit.json').open('x',encoding='utf-8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
