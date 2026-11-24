"""Exact full-support physical screening. No original Pi or R6 is inferred.

The complete key universe is1..n and S is explicitly full for these sources.
Each SET label is its exact inorder interval, stored as lo*(n+1)+hi.
All pointer changes and complete state identities are exact integer encodings.
"""
from campaign import *


class FullTree:
    def __init__(self,st):
        self.n=len(st['children']);self.b=(self.n+1).bit_length();self.root=st['root']
        self.l=[0]*(self.n+1);self.r=self.l.copy();self.p=self.l.copy();self.lo=self.l.copy();self.hi=self.l.copy()
        self.code=self.root<<(2*self.n*self.b)
        for k in range(1,self.n+1):
            ll,rr=st['children'][str(k)];self.l[k]=ll or 0;self.r[k]=rr or 0
            if ll:self.p[ll]=k
            if rr:self.p[rr]=k
            self.code^=self.l[k]<<((2*k-2)*self.b);self.code^=self.r[k]<<((2*k-1)*self.b)
        todo=[(self.root,False)]
        while todo:
            k,done=todo.pop()
            if done:self.lo[k]=self.lo[self.l[k]] if self.l[k] else k;self.hi[k]=self.hi[self.r[k]] if self.r[k] else k
            else:
                todo.append((k,True))
                if self.l[k]:todo.append((self.l[k],False))
                if self.r[k]:todo.append((self.r[k],False))
        self.carriers={self.label(k) for k in range(1,self.n+1)}
        assert len(self.carriers)==self.n
    def label(self,k):return self.lo[k]*(self.n+1)+self.hi[k]
    def pointer(self,k,side,v):
        arr=self.r if side else self.l;old=arr[k]
        if hasattr(self,'touched'):self.touched.add(k)
        self.code^=(old^v)<<((2*k-2+side)*self.b);arr[k]=v
    def path(self,x):
        path=[];k=self.root
        while k!=x:
            assert k;path.append(k);k=self.l[k] if x<k else self.r[k]
        return path+[x]
    def state(self):return {'root':self.root,'children':{str(k):[self.l[k] or None,self.r[k] or None] for k in range(1,self.n+1)}}
    def rotate(self,u,side,other,actor):
        v=(self.r if side else self.l)[u];c=self.p[u];middle=(self.l if side else self.r)[v]
        oldchild=self.label(v);flo,fhi=self.lo[u],self.hi[u]
        if c:self.pointer(c,int(self.r[c]==u),v)
        else:self.code^=(self.root^v)<<(2*self.n*self.b);self.root=v
        self.p[v]=c;self.pointer(u,side,middle)
        if middle:self.p[middle]=u
        self.pointer(v,1-side,u);self.p[u]=v
        self.lo[u]=self.lo[self.l[u]] if self.l[u] else u
        self.hi[u]=self.hi[self.r[u]] if self.r[u] else u
        self.lo[v],self.hi[v]=flo,fhi;new=self.label(u)
        assert oldchild in self.carriers and new not in self.carriers
        sign=(int(oldchild in other.carriers)-int(new in other.carriers)) if actor=='A' else (int(new not in other.carriers)-int(oldchild not in other.carriers))
        if actor=='B':assert sign in (-1,0)
        self.carriers.remove(oldchild);self.carriers.add(new)
        return sign
    def splay(self,x,other,actor):
        steps=0;q=0;neutral_internal=False;details=[]
        while self.p[x]:
            steps+=1;p=self.p[x];g=self.p[p];side=int(x>p)
            if not g:
                sign=self.rotate(p,side,other,actor)
                if actor=='B':assert sign==-1
                details.append(('ZIG',p,None,(sign,)))
            else:
                q+=1;z=int(p>g);internal=self.lo[g]>1 and self.hi[g]<self.n
                case=('R' if z else 'L')+('R' if side else 'L')
                rotations=((g,z),(p,side)) if side==z else ((p,side),(g,z))
                signs=tuple(self.rotate(u,s,other,actor) for u,s in rotations)
                if actor=='B' and internal and signs==(0,0):neutral_internal=True
                details.append((case,p,g,signs))
        return steps,q,neutral_internal,details


def decode(code,n):
    b=(n+1).bit_length();mask=(1<<b)-1
    return {'root':(code>>(2*n*b))&mask,'children':{str(k):[((code>>((2*k-2)*b))&mask) or None,
                ((code>>((2*k-1)*b))&mask) or None] for k in range(1,n+1)}}


def physical_replay(s,keep_codes=True,collect_A=False):
    a=FullTree(s['initial_A']);b=FullTree(s['initial_B']);ac0,bc0=a.code,b.code
    rows=[];codes={b.code:b.code};A=Q=0
    for t,(tag,x) in enumerate(s['operations'],1):
        aa,_,_,_=a.splay(x,b,'A');A+=aa
        qq=0;guard=False;detail=[]
        if tag=='K':_,qq,guard,detail=b.splay(x,a,'B');Q+=qq
        code=codes.setdefault(b.code,b.code) if keep_codes else None
        rows.append({'t':t,'tag':tag,'x':x,'a':aa,'q':qq,'guard_G':guard,'B_code':code,'B_steps':detail})
        if collect_A:rows[-1]['A_code']=a.code
    assert a.code==ac0 and b.code==bc0,(s['name'],'not complete paired closure')
    ks=[i for i,r in enumerate(rows) if r['tag']=='K'];T=len(rows)
    for k,i in enumerate(ks):
        prev=ks[k-1];length=(i-prev)%T or T;agap=sum(rows[(prev+j)%T]['a'] for j in range(1,length+1))
        rows[i]['A_gap']=agap;rows[i]['guard_H']=rows[i]['guard_G'] and rows[i]['q']>2*agap
    assert sum(rows[i]['A_gap'] for i in ks)==A
    return {'source':s,'rows':rows,'A':A,'Q_B':Q,'initial_B_code':bc0,'complete_paired_closure':True,
            'distinct_full_B_codes':len(codes),'full_support_assumption':'source must independently guarantee S=all physical keys'}


def skeleton_indices(replay,cut=0,variant='H'):
    rows=replay['rows'];T=len(rows);order=[(cut+i)%T for i in range(T)]
    if variant=='raw':return [i for i in order if rows[i]['tag']=='K']
    initial=rows[(cut-1)%T]['B_code'];locations={initial:0};stack=[];records=[(0,initial)]
    for i in order:
        row=rows[i]
        if row['tag']!='K':continue
        state=row['B_code']
        if row['guard_'+variant]:
            stack.append(i);locations={state:len(stack)};records=[(len(stack),state)]
        elif state in locations:
            j=locations[state];del stack[j:]
            while records[-1][0]>j:
                _,old=records.pop();del locations[old]
        else:stack.append(i);locations[state]=len(stack);records.append((len(stack),state))
    return stack


def skeleton_cost(replay,cut=0,variant='H'):
    indices=skeleton_indices(replay,cut,variant);rows=replay['rows'];n=len(replay['source']['initial_B']['children'])
    initial=decode(rows[(cut-1)%len(rows)]['B_code'],n);tree=Tree(initial)
    targets=[]
    for i in indices:
        x=rows[i]['x']
        if not targets or targets[-1]!=x:targets.append(x)
    J=path_hull(tree,set(targets));z=periodic_cost(targets,J)
    return {**z,'A':replay['A'],'eligible_periodic':z['B_cyclic']<=10*replay['A'],
        'J_size':len(J),'retained_KEEP_count':len(indices),'guard_count':sum(r.get('guard_'+variant,False) for r in rows),
        'retained_original_Q':sum(rows[i]['q'] for i in indices),'cut_before':cut+1,'variant':variant,
        'retained_original_operations':[i+1 for i in indices]}


def path_hull(tree,targets):
    J=set()
    for x in targets:
        while x is not None and x not in J:J.add(x);x=tree.par[x]
    return J
