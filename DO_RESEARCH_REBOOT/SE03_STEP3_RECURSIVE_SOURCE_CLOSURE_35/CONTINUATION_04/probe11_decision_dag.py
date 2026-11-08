"""Exact numerical index-interval functions, not an A/B source quotient."""
import bisect
import numpy as np
class DAG:
    def __init__(self,nodes=None,nextid=0):
        self.nodes={} if nodes is None else nodes;self.nextid=nextid;self.intern={p:i for i,p in self.nodes.items()}
    @staticmethod
    def terminal(v):return -int(v)-1
    def pair(self,l,r):
        if l==r and l<0:return l
        key=(l,r)
        if key not in self.intern:
            i=self.nextid;self.nextid+=1;self.intern[key]=i;self.nodes[i]=key
        return self.intern[key]
    def changes(self,root,size,indices,values):
        ii=list(map(int,indices));vv=list(map(int,values))
        def go(node,lo,hi,a,b):
            if a==b:return node
            if hi-lo==1:assert b==a+1 and ii[a]==lo;return self.terminal(vv[a])
            mid=(lo+hi)//2;j=bisect.bisect_left(ii,mid,a,b);l,r=(node,node) if node<0 else self.nodes[node]
            return self.pair(go(l,lo,mid,a,j),go(r,mid,hi,j,b))
        return go(root,0,size,0,len(ii))
    def vector(self,root,n):
        size=1<<(n-1).bit_length();out=np.zeros(n,dtype=np.int32)
        def go(node,lo,hi):
            if lo>=n:return
            if node<0:out[lo:min(n,hi)]=-node-1;return
            mid=(lo+hi)//2;l,r=self.nodes[node];go(l,lo,mid);go(r,mid,hi)
        go(root,0,size);return out
    def collect(self,roots):
        live=set();todo=[r for r in roots if r>=0]
        while todo:
            n=todo.pop()
            if n in live:continue
            live.add(n);todo.extend(c for c in self.nodes[n] if c>=0)
        self.nodes={n:self.nodes[n] for n in live};self.intern={p:i for i,p in self.nodes.items()}
