"""Same exact pointwise max, with a bounded derived maximum-value cache."""
import collections
class Apply:
    def __init__(self,dag):self.dag=dag;self.cache=collections.OrderedDict();self.maxcache=collections.OrderedDict();self.hits=0
    def maximum(self,i):
        if i<0:return -i-1
        if i in self.maxcache:v=self.maxcache.pop(i);self.maxcache[i]=v;return v
        l,r=self.dag.nodes[i];v=max(self.maximum(l),self.maximum(r));self.maxcache[i]=v
        if len(self.maxcache)>100000:self.maxcache.popitem(last=False)
        return v
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
        if len(self.cache)>75000:self.cache.popitem(last=False)
        return v
    def collect(self,columns):
        self.dag.collect(columns);self.cache.clear();self.maxcache=collections.OrderedDict((i,v) for i,v in self.maxcache.items() if i in self.dag.nodes)
