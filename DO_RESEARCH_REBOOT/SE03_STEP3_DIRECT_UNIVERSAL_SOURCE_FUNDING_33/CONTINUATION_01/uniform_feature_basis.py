"""Support-independent integer source features; no source simulation here."""
def metadata(trees,n):
    import numpy as np
    dd=[];mm=[];pp=[];ss=[];rr=[]
    for tree in trees:
        d=[0]*n;m=[0]*n;p=[0]*n
        def walk(t,dep,par):
            if isinstance(t,str):return 0
            k,l,r=t;p[k-1]=par;d[k-1]=dep;m[k-1]=(1<<(k-1))|walk(l,dep+1,k)|walk(r,dep+1,k);return m[k-1]
        walk(tree,0,0);s=[v.bit_count() for v in m];dd.append(d);mm.append(m);pp.append(p);ss.append(s);rr.append([v.bit_length()-1 for v in s])
    return tuple(np.array(v,dtype=np.int16) for v in (dd,mm,pp,ss,rr))
def features(meta,a,b,n):
    import numpy as np
    d,m,p,s,rank=meta;da,db=d[a],d[b];ma,mb=m[a],m[b];sa,sb=s[a],s[b];ra,rb=rank[a],rank[b];F=[]
    for va,vb in ((da,db),(da*da,db*db),(sa*sa,sb*sb),(ra,rb)):F.extend((va.sum(1),vb.sum(1)))
    pop=np.array([v.bit_count() for v in range(1<<n)]);F.extend(((p[a]==p[b]).sum(1),(ma==mb).sum(1),pop[ma&mb].sum(1),abs(da-db).sum(1),(da*db).sum(1),(sa*sb).sum(1),np.minimum(sa,sb).sum(1),(ra*rb).sum(1),abs(ra-rb).sum(1),(da==db).sum(1),(da<db).sum(1),(sa==sb).sum(1)));return np.stack(F,axis=1).astype(np.int16)
