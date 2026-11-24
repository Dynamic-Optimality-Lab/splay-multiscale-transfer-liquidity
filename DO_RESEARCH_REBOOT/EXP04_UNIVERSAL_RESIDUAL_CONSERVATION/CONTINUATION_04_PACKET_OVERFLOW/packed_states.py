"""Lossless boundary-state storage only. Original rotations/SET/Pi code unchanged.

Mapping values decode complete labelled child pointers; equality is extensional.
No hash digest is used as a substitute for complete physical identity.
"""
from collections.abc import Mapping
import json

class Children(Mapping):
    def __init__(self,code,n,b):self.code=code;self.n=n;self.b=b;self.mask=(1<<b)-1
    def __iter__(self):return (str(k) for k in range(1,self.n+1))
    def __len__(self):return self.n
    def __getitem__(self,key):
        k=int(key)
        if not 1<=k<=self.n or str(k)!=key:raise KeyError(key)
        shift=(2*k-2)*self.b
        return [(self.code>>shift)&self.mask or None,(self.code>>(shift+self.b))&self.mask or None]

def install(Tree):
    old_rotate=Tree.rotate;old_state=Tree.state;old_labels=Tree.labels
    old_default=json.JSONEncoder.default;pool={}
    def default(encoder,obj):
        if isinstance(obj,Children):return dict(obj.items())
        return old_default(encoder,obj)
    json.JSONEncoder.default=default
    def labels(tree,bits):
        if getattr(tree,'_label_bits',None) is not bits:
            tree._label_bits=bits;tree._label_values=old_labels(tree,bits)
        return tree._label_values
    def state(tree):
        n=len(tree.keys)
        assert tree.keys==list(range(1,n+1))
        b=(n+1).bit_length()
        if not hasattr(tree,'packed_code'):
            code=tree.root<<(2*n*b)
            for k in tree.keys:
                l,r=tree.ch[k];code|=(l or 0)<<((2*k-2)*b);code|=(r or 0)<<((2*k-1)*b)
            tree.packed_code=code
        key=(n,tree.packed_code)
        if key not in pool:pool[key]={'root':tree.root,'children':Children(tree.packed_code,n,b)}
        return pool[key]
    def rotate(tree,u,side):
        cached=getattr(tree,'_label_values',None)
        v0=tree.ch[u][side]
        if hasattr(tree,'packed_code'):
            n=len(tree.keys);b=(n+1).bit_length();oldroot=tree.root
            v=tree.ch[u][side];c=tree.par[u]
            touched={u,v}|({c} if c is not None else set())
            old={k:tuple(tree.ch[k]) for k in touched}
            out=old_rotate(tree,u,side)
            tree.packed_code^=(oldroot^tree.root)<<(2*n*b)
            for k,pair in old.items():
                for s in (0,1):tree.packed_code^=((pair[s] or 0)^(tree.ch[k][s] or 0))<<((2*k-2+s)*b)
        else:out=old_rotate(tree,u,side)
        if cached is not None:
            # Only the two rotated vertices change descendant labels. Keep
            # the old dictionary immutable for callers holding a pre-state.
            updated=cached.copy();bits=tree._label_bits
            for k in (u,v0):
                l,r=tree.ch[k]
                updated[k]=bits.get(k,0)|updated.get(l,0)|updated.get(r,0)
            tree._label_values=updated
        return out
    Tree.state=state;Tree.rotate=rotate;Tree.labels=labels
    return pool,lambda:(setattr(Tree,'state',old_state),setattr(Tree,'rotate',old_rotate),
        setattr(Tree,'labels',old_labels),setattr(json.JSONEncoder,'default',old_default))

def materialize(st):return {'root':st['root'],'children':dict(st['children'].items())}
