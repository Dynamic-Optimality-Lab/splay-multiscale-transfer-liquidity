"""Common-diagonal closed witnesses over a proposed finite ordinary kernel."""
import collections
class Compiler:
    def __init__(self,native):
        self.z=native;self.T=native['trees'];self.D=native['destination'];self.H=native['H'];self.Q=native['Q'];self.n=len(self.D[0]);N=len(self.T);self.root=[t[0] for t in self.T];self.forward={0:None};q=collections.deque([0]);reverse=[[] for _ in range(N)];self.incoming={}
        for a in range(N):
            for x,b in enumerate(self.D[a],1):
                reverse[b].append((a,x))
                if self.root[a]!=x and b not in self.incoming:self.incoming[b]=(a,x)
        while q:
            a=q.popleft()
            for x,b in enumerate(self.D[a],1):
                if b not in self.forward:self.forward[b]=(a,x);q.append(b)
        self.backward={0:None};q=collections.deque([0])
        while q:
            b=q.popleft()
            for a,x in reverse[b]:
                if a not in self.backward:self.backward[a]=(b,x);q.append(a)
        assert len(self.forward)==len(self.backward)==len(self.incoming)==N
    def outward(self,t):
        p=[]
        while t:t,x=self.forward[t];p.append(x)
        return p[::-1]
    def inward(self,s):
        p=[]
        while s:s,x=self.backward[s];p.append(x)
        return p
    def compile(self,a,b,y,x):
        n=self.n;D,H,Q=self.D,self.H,self.Q;bpre,g=self.incoming[b];assert self.root[a]==self.root[b]==g;prefix=[('D',k) for k in self.inward(bpre)+self.outward(a)]+[('K',g)];packet=([('D',y)] if y else [])+[('K',x)];aa=a
        for _,k in packet:aa=D[aa][k-1]
        bb=D[b][x-1];suffix=self.inward(bb)+list(range(2,n+1))+list(range(n-1,0,-1))+self.outward(bpre);acur=aa
        for k in suffix:acur=D[acur][k-1]
        word=prefix+packet+[('K',k) for k in suffix]+[('D',k) for k in self.inward(acur)+self.outward(bpre)]
        def one(E,copy):
            A=F=bpre;rows=[]
            for local,(mode,k) in enumerate(word,1):
                oldA,oldF,oldE=A,F,E;A=D[A][k-1];q=qe=0
                if mode=='K':F=D[F][k-1];q=Q[oldF][k-1]
                if mode=='K' and k!=n:E=D[E][k-1];qe=Q[oldE][k-1]
                rows.append([copy*len(word)+local,mode,k,oldA,oldF,oldE,A,F,E,H[oldA][k-1],q,qe])
            assert A==F==bpre;return E,rows
        E=bpre;seen={};copies=[];j=0
        while E not in seen:seen[E]=j;E,rows=one(E,j);copies.append(rows);j+=1
        u0=seen[E];L=j-u0;u=max(1,u0)
        while j<u+L:E,rows=one(E,j);copies.append(rows);j+=1
        rows=sum(copies[u:u+L],[]);lo=u*len(word)+len(prefix)+1;hi=lo+len(packet)-1;rr=[r for r in rows if lo<=r[0]<=hi];assert rr[0][3:5]==[a,b] and rows[0][3:6]==rows[-1][6:9];return {'initial_diagonal_index':bpre,'word':word,'u':u,'L':L,'period':[rows[0][0],rows[-1][0]],'rows':rows,'natural_packet':[lo,hi],'H':sum(r[9] for r in rr),'Q':sum(r[10] for r in rr),'A':sum(r[9] for r in rows),'QF':sum(r[10] for r in rows),'QE':sum(r[11] for r in rows)}
