"""Pointwise max of exact ordered-index decision functions."""
import collections
class Apply:
    def __init__(self,dag):self.dag=dag;self.cache=collections.OrderedDict();self.maxcache={};self.hits=0
    def maximum(self,i):
        if i<0:return -i-1
        if i not in self.maxcache:
            l,r=self.dag.nodes[i];self.maxcache[i]=max(self.maximum(l),self.maximum(r))
        return self.maxcache[i]
    def combine(self,a,b):
        if a==b:return a
        if a==-1:return b
        if b==-1:return a
        if a<0 and b<0:return min(a,b)
        if a<0 and -a-1>=self.maximum(b):return a
        if b<0 and -b-1>=self.maximum(a):return b
        key=(min(a,b),max(a,b))
        if key in self.cache:
            v=self.cache.pop(key);self.cache[key]=v
            if v<0 or v in self.dag.nodes:self.hits+=1;return v
        al,ar=(a,a) if a<0 else self.dag.nodes[a];bl,br=(b,b) if b<0 else self.dag.nodes[b]
        v=self.dag.pair(self.combine(al,bl),self.combine(ar,br));self.cache[key]=v
        if len(self.cache)>100000:self.cache.popitem(last=False)
        return v
    def collect(self,columns):
        self.dag.collect(columns);self.cache.clear();self.maxcache={i:v for i,v in self.maxcache.items() if i in self.dag.nodes}
