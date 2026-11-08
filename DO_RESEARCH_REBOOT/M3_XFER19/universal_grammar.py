"""Universal all-population symbolic source word, up to two A charges."""
import z3
from symbolic_prefix import full,move,locate,at,OBS
P=10;F=9;G=11;EMPTY=12
def build(word,root,target,helper=None,name='w'):
    tree=full(7);need={()};forced={():('S',root)}
    for j,path in enumerate(word):
        need.update(at(tree,path[:i])[0] for i in range(len(path)+1))
        where=at(tree,path)[0]
        forced[where]=('F',helper) if j<len(word)-1 else ('S',target)
        tree=move(tree,path)
    obs=set(OBS)|{at(tree,p)[0] for p in OBS}|need
    owner=locate(tree,());obs.update(c[0] for c in owner[1:] if c is not None)
    for p in tuple(obs):obs.update(p[:i] for i in range(len(p)))
    typ={p:z3.Int(name+'_type_'+(''.join(map(str,p)) or 'r')) for p in obs}
    gap={p:z3.Int(name+'_gap_'+(''.join(map(str,p)) or 'r')) for p in obs}
    C=[]
    def descend(p,lo,hi):
        if p not in obs:return
        t=typ[p];g=gap[p]
        C.extend([t>=0,t<=EMPTY,z3.Implies(t<9,z3.And(lo<=t,t<=hi)),
          z3.Implies(t==F,z3.And(lo<=g,g<=hi+1)),
          z3.Implies(z3.Or(t==G,t==EMPTY),lo>hi)])
        if p in need:C.append(t<=F)
        if p in forced:
            kind,label=forced[p]
            C.extend([t==F,g==label] if kind=='F' else [t==label])
        pivot=z3.If(t<9,t,g)
        descend(p+(0,),lo,pivot-1)
        descend(p+(1,),z3.If(t<9,pivot+1,pivot),hi)
    descend((),z3.IntVal(0),z3.IntVal(8))
    def observe(root,owner):
        def follow(ref,p):
            if ref is None:return z3.IntVal(P)
            t=typ.get(ref[0],z3.IntVal(P))
            if not p:return z3.If(t==G,typ[()],t)
            return z3.If(z3.Or(t==P,t==EMPTY),t,
              z3.If(t==G,follow(owner[1+p[0]],p[1:]),follow(ref[1+p[0]],p[1:])))
        return tuple(follow(root,p) for p in OBS)
    return {'constraints':C,'source':observe(full(7),full(7)),
      'target':observe(tree,owner),'private_variables':list(typ.values())+list(gap.values()),
      'observed':obs,'required':need,'forced':forced,'terminal_source_address':tree[0]}
