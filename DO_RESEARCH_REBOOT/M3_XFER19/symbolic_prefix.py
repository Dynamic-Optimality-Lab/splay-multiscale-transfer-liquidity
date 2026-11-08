"""Universal protected-prefix formula, not finite source/population tests.

Every variable ranges over ALL grammar productions at its protected
address. Equal-gap anonymous nodes may occur on both sides. The original
source-owner lookup is updated by the exact A constructor permutation.
"""
import z3
P=10;F=9;G=11
OBS=((),(0,),(1,),(0,0),(0,1),(1,0),(1,1))
PATHS=OBS[1:]
def node(k,l=None,r=None):return (k,l,r)
def full(d=5,p=()):return None if len(p)>d else node(p,full(d,p+(0,)),full(d,p+(1,)))
def at(t,p):
    for b in p:t=t[1+b]
    return t
def locate(t,k):
    if t is None:return None
    if t[0]==k:return t
    return locate(t[1],k) or locate(t[2],k)
def rot(t,b):
    k,l,r=t
    if b==0:
        p,a,c=l;return node(p,a,node(k,c,r))
    p,a,c=r;return node(p,node(k,l,a),c)
def move(t,p):
    if len(p)==1:return rot(t,p[0])
    a,b=p
    if a==b:return rot(rot(t,a),b)
    k,l,r=t
    return rot(node(k,rot(l,b),r),a) if a==0 else rot(node(k,l,rot(r,b)),a)
def specification(path):
    t=full();out=move(t,path);need={path[:i] for i in range(len(path)+1)}
    obs=set(OBS)|{at(out,p)[0] for p in OBS}
    owner=locate(out,());obs.update(t[0] for t in owner[1:])
    obs|=need
    for p in tuple(obs):obs.update(p[:i] for i in range(len(p)))
    return obs,need,out
def prefix(path,root,target,prefix_name='u'):
    obs,need,out=specification(path)
    typ={p:z3.Int(prefix_name+'_t_'+(''.join(map(str,p)) or 'r')) for p in obs}
    gap={p:z3.Int(prefix_name+'_g_'+(''.join(map(str,p)) or 'r')) for p in obs}
    constraints=[]
    def build(p,lo,hi):
        if p not in obs:return
        t=typ[p];g=gap[p]
        constraints.extend([t>=0,t<=G,
          z3.Implies(t<9,z3.And(lo<=t,t<=hi)),
          z3.Implies(t==F,z3.And(lo<=g,g<=hi+1)),
          z3.Implies(t==G,lo>hi)])
        if p in need:constraints.append(t<=F)
        if p==():constraints.append(t==root)
        if p==path:constraints.append(t==target)
        pivot=z3.If(t<9,t,g)
        # For inactive P/G descendants the intervals are immaterial,
        # because lookup stops/resets there. They still admit P.
        build(p+(0,),lo,pivot-1)
        build(p+(1,),z3.If(t<9,pivot+1,pivot),hi)
    build((),z3.IntVal(0),z3.IntVal(8))
    source=full();owner0=source
    def observe(tree,owner):
        def follow(ref,word):
            if ref is None:return z3.IntVal(P)
            label=typ.get(ref[0],z3.IntVal(P))
            if not word:return z3.If(label==G,typ[()],label)
            ordinary=follow(ref[1+word[0]],word[1:])
            alias=follow(owner[1+word[0]],word[1:])
            return z3.If(label==P,z3.IntVal(P),z3.If(label==G,alias,ordinary))
        return tuple(follow(tree,p) for p in OBS)
    return {'constraints':constraints,'source':observe(source,owner0),
      'target':observe(out,locate(out,())),'types':typ,'gaps':gap,
      'observed':obs,'required':need,'word':path}
