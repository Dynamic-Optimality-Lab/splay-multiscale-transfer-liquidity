"""Exact anchor-set comparisons for ordered free terms, not population counts."""
def node(t):return isinstance(t,tuple)
def atoms(t,P,bounds):
    if not node(t):return {} if t=='E' else {('X',t):bounds[t]}
    z=atoms(t[1],P,bounds);z.update(atoms(t[2],P,bounds))
    if t[0] not in P:z['K',t[0]]=(t[0],t[0])
    return z
def allowed_tags(t,P,bounds):
    total=atoms(t,P,bounds);result={}
    def walk(v):
        if not node(v):return
        k=v[0]
        if k in P:
            L,R=atoms(v[1],P,bounds),atoms(v[2],P,bounds)
            if not L or not R:result[k]={'L','R'}
            else:
                below={a for a,(lo,hi) in total.items() if (hi<k if a[0]=='K' else hi<=k)};above={a for a,(lo,hi) in total.items() if (lo>k if a[0]=='K' else lo>=k)};assert below|above==set(total) and not below&above
                result[k]=({'L'} if set(L)==below else set())|({'R'} if set(R)==above else set())
        walk(v[1]);walk(v[2])
    walk(t);return result
