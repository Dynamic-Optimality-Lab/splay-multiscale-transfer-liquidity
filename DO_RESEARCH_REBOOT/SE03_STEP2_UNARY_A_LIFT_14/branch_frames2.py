"""Complete active-frame syntax for the proposed full A branch quotient.
No bounded private inventory; actual operands determine all exposures.
"""
import functools,importlib.util,json,time
from pathlib import Path
B=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('original_branch_frames14',B.parent/'SE03_STEP2_COLD_NEG2_01/source_model.py')
p=importlib.util.module_from_spec(s);s.loader.exec_module(p);M=set(range(1000,6001,1000));calls=0
@functools.lru_cache(None)
def family(lo,hi):
    if lo>hi:return (None,)
    result=[(1000*j,l,r) for j in range(lo,hi+1) for l in family(lo,j-1) for r in family(j+1,hi)]
    result += [(1000*j+500,l,r) for j in range(lo,hi) for l in family(lo,j) for r in family(j+1,hi)]
    return tuple(result)
def bases():return tuple(t for t in family(1,6) if t[0] in M)
def node(t):return isinstance(t,tuple)
def vals(t):return [] if not node(t) else vals(t[1])+[t[0]]+vals(t[2])
def canonical(t,selected=None):
    # Normalize all ordered known private/branch/unary labels within each
    # mark gap; retain six mark labels and return distinguished-target image.
    kk=vals(t);mp={x:x for x in M};groups={}
    for x in kk:
        if x not in M:groups.setdefault(sum(m<x for m in M),[]).append(x)
    for g,ks in groups.items():
        for j,x in enumerate(ks):mp[x]=1000*g+1000*(j+1)//(len(ks)+1)
    count=0
    def go(t):
        nonlocal count
        if not node(t):v='F'+str(count);count+=1;return v
        return (mp[t[0]],go(t[1]),go(t[2]))
    new=go(t);return new,mp.get(selected) if selected is not None else None
def material(t):
    def go(v):return 'gap' if v is None else (v[0],go(v[1]),go(v[2]))
    return canonical(go(t))[0]
def get(t,path):
    for c in path:t=t[1 if c=='L' else 2]
    return t
def put(t,path,v):
    if not path:return v
    return (t[0],put(t[1],path[1:],v),t[2]) if path[0]=='L' else (t[0],t[1],put(t[2],path[1:],v))
def find(t,x,path=''):
    if not node(t):return None
    if t[0]==x:return path
    return find(t[1],x,path+'L') if x<t[0] else find(t[2],x,path+'R')
def bound(t,path):
    lo,hi=0,7000
    for c in path:
        if c=='L':hi=t[0];t=t[1]
        else:lo=t[0];t=t[2]
    return lo,hi
def subpaths(t,path=''):
    if not node(t):return []
    return [(path,t)]+subpaths(t[1],path+'L')+subpaths(t[2],path+'R')
def hasmark(t):return any(x in M for x in vals(t))
def insertions(t,path):
    if not path:return []
    sub=get(t,path)
    if not node(sub) or not hasmark(sub):return []
    lo,hi=bound(t,path);kk=vals(sub);result=[]
    if max(kk)+1<hi:
        u=(max(kk)+hi)//2;result.append((put(t,path,(u,sub,'new')),u))
    if lo+1<min(kk):
        u=(lo+min(kk))//2;result.append((put(t,path,(u,'new',sub)),u))
    return result
def decorations(t,target,depthcap):
    t,y=canonical(t,target);todo=[(t,y)];seen={(t,y)};result=[]
    while todo:
        T,y=todo.pop();path=p.path(T,y);d=len(path)
        if d>depthcap:continue
        result.append((T,y))
        if d==depthcap:continue
        for j in range(1,len(path)+1):
            for TT,u in insertions(T,path[:j]):
                TT,yy=canonical(TT,y)
                if (TT,yy) not in seen:seen.add((TT,yy));todo.append((TT,yy))
    return result
def reduce(t,K=p):
    c=K.core(t,M)
    def go(v):
        if v is None:return None
        l,r=go(v[1]),go(v[2])
        if v[0] in M:return (v[0],l,r)
        if l is None:return r
        if r is None:return l
        return (1000*sum(x<v[0] for x in M)+500,l,r)
    return go(c)
def generate(K=p):
    global calls
    aa=bases();assert len(aa)==974;ids={t:i for i,t in enumerate(aa)};relations={1:set(),2:set()};examples={};local_first=0
    def trace(t,x):
        global calls
        calls+=1;assert calls<1800000;return K.trace(t,x)
    def save(a,H,T,accesses,dest,kind):
        b=ids[reduce(dest,K)];x=accesses[-1]//1000;key=(a,x,b)
        relations[H].add(key)
        if (H,)+key not in examples:examples[(H,)+key]={'H':H,'a':a,'x':x,'b':b,'source':T,'accesses':accesses,'kind':kind}
    for a,raw in enumerate(aa):
        T=material(raw);g=T[0]
        # Single positive marked access with every active unary path.
        for x in sorted(M-{g}):
            for TT,xx in decorations(T,x,4):
                d=len(K.path(TT,xx))
                if not 1<=d<=4:continue
                dest,_,ev=trace(TT,xx);H=len(ev);assert H in (1,2);save(a,H,TT,[xx],dest,'single_marked')
        first={}
        def add(TT,y,kind):
            TT,yy=canonical(TT,y)
            if 1<=len(K.path(TT,yy))<=2:first[TT,yy]=kind
        for y in vals(T):
            if y==g:continue
            for TT,yy in decorations(T,y,2):add(TT,yy,'known_core')
        for path,sub in subpaths(T):
            if not 1<=len(path)<=2:continue
            for TT,y in insertions(T,path):
                for TTT,yy in decorations(TT,y,2):add(TTT,yy,'old_unary_target')
                # A shallow OLD unary parent may carry marks on one side
                # and the private first target on the other. Contracting
                # that parent makes its private side look deep in BASE.
                if len(path)==1:
                    U=get(TT,path)
                    private_side='L' if not node(U[1]) else 'R'
                    pp=path+private_side
                    lo,hi=bound(TT,pp);v=(lo+hi)//2
                    add(put(TT,pp,(v,'a','b')),v,'private_child_of_old_unary_parent')
        for path,sub in [(q,v) for q,v in leafpaths(T) if 1<=len(q)<=2]:
            lo,hi=bound(T,path);mid=(lo+hi)//2;q1=lo+(hi-lo)//3;q2=lo+2*(hi-lo)//3
            add(put(T,path,(mid,'a','b')),mid,'private_root')
            if len(path)==1:
                add(put(T,path,(q2,(q1,'a','b'),'c')),q1,'private_left_grandchild')
                add(put(T,path,(q1,'a',(q2,'b','c'))),q2,'private_right_grandchild')
        local_first+=len(first)
        for (TT,y),kind in first.items():
            mid,_,ev=trace(TT,y);assert len(ev)==1
            e=ev[0];active={e.get('G'),e.get('P'),e.get('target')};active.discard(None)
            for x in sorted(M-{g}):
                path=K.path(mid,x);d=len(path)
                if not 1<=d<=2:continue
                dest,_,ev2=trace(mid,x);assert len(ev2)==1;save(a,2,TT,[y,x],dest,kind)
                # One extra old unary on the second path can only be in
                # an unchanged marked-carrying hanger of the first frame.
                if d!=1:continue
                S=get(mid,path)
                if set(vals(S))&active or not hasmark(S):continue
                original=find(TT,S[0]);assert original is not None and get(TT,original)==S
                for TTT,u in insertions(TT,original):
                    TTT,yy=canonical(TTT,y);middle,_,ee=trace(TTT,yy);assert len(ee)==1
                    assert 1<=len(K.path(middle,x))<=2
                    end,_,ee2=trace(middle,x);assert len(ee2)==1;save(a,2,TTT,[yy,x],end,'second_rigid_hanger_unary')
    return {'status':'COMPLETE_ACTIVE_FRAME_SOURCE_COMPARISON','states':aa,'H1':sorted(relations[1]),'H2':sorted(relations[2]),
        'witnesses':[examples[k] for k in sorted(examples)],'first_frame_contexts':local_first,'source_engine_calls':calls,
        'lifting':'off-operand unary contraction plus complete depth4/one-event-first/rigid-second-hanger exposure; arbitrary original private populations'}
def leafpaths(t,path=''):
    if not node(t):return [(path,t)]
    return leafpaths(t[1],path+'L')+leafpaths(t[2],path+'R')
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
