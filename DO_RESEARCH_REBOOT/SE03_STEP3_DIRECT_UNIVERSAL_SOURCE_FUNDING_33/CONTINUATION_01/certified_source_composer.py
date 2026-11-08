"""Finite source-word proof composition from the already checked native kernel.
No engine invocation. This module does not assert arbitrary-n reachability.
"""
import collections,json,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent
class Composer:
    def __init__(self):
        raw=(B/'native10_source_actions.json').read_bytes();audit=json.loads((B/'native10_source_independent_audit.json').read_text());assert hashlib.sha256(raw).hexdigest()==audit['input_sha256'];self.z=json.loads(raw);self.T=self.z['trees'];self.D=self.z['destination'];self.H=self.z['H'];self.Q=self.z['Q'];N=len(self.T);self.root=[t[0] for t in self.T];self.vine=0;forward={0:None};q=collections.deque([0]);rev=[[] for _ in range(N)];incoming={}
        for a in range(N):
            for x,b in enumerate(self.D[a],1):
                rev[b].append((a,x))
                if self.root[a]!=x and b not in incoming:incoming[b]=(a,x)
        while q:
            a=q.popleft()
            for x,b in enumerate(self.D[a],1):
                if b not in forward:forward[b]=(a,x);q.append(b)
        backward={0:None};q=collections.deque([0])
        while q:
            b=q.popleft()
            for a,x in rev[b]:
                if a not in backward:backward[a]=(b,x);q.append(a)
        assert len(forward)==len(backward)==len(incoming)==N;self.forward,self.backward,self.incoming=forward,backward,incoming
    def fromvine(self,t):
        ans=[]
        while t:t,x=self.forward[t];ans.append(x)
        return ans[::-1]
    def tovine(self,s):
        ans=[]
        while s:s,x=self.backward[s];ans.append(x)
        return ans
    def compile(self,a,b,helper,target):
        D,H,Q=self.D,self.H,self.Q;bpre,g=self.incoming[b];assert self.root[a]==self.root[b]==g;prefix=[('D',k) for k in self.tovine(bpre)+self.fromvine(a)]+[('K',g)];packet=([('D',helper)] if helper else [])+[('K',target)];aa=a
        for _,x in packet:aa=D[aa][x-1]
        bb=D[b][target-1];suffix=self.tovine(bb)+list(range(2,11))+list(range(9,0,-1))+self.fromvine(bpre);acur=aa
        for k in suffix:acur=D[acur][k-1]
        word=prefix+packet+[('K',k) for k in suffix]+[('D',k) for k in self.tovine(acur)+self.fromvine(bpre)]
        def one(E,copy):
            A=F=bpre;rows=[]
            for local,(mode,x) in enumerate(word,1):
                oldA,oldF,oldE=A,F,E;A=D[A][x-1];q=qe=0
                if mode=='K':F=D[F][x-1];q=Q[oldF][x-1]
                if mode=='K' and x!=10:E=D[E][x-1];qe=Q[oldE][x-1]
                rows.append([copy*len(word)+local,mode,x,oldA,oldF,oldE,A,F,E,H[oldA][x-1],q,qe])
            assert A==F==bpre;return E,rows
        E=bpre;seen={};copies=[];j=0
        while E not in seen:seen[E]=j;E,rows=one(E,j);copies.append(rows);j+=1
        u0=seen[E];L=j-u0;u=max(u0,1)
        while j<u+L:E,rows=one(E,j);copies.append(rows);j+=1
        rows=sum(copies[u:u+L],[]);lo=u*len(word)+len(prefix)+1;hi=lo+len(packet)-1;rr=[r for r in rows if lo<=r[0]<=hi];assert rr[0][3:5]==[a,b] and rows[0][3:6]==rows[-1][6:9];assert set(r[2] for r in rows if r[1]=='K' and self.root[r[4]]!=r[2])==set(range(1,11));return {'initial_diagonal_index':bpre,'word':word,'u':u,'L':L,'period':[rows[0][0],rows[-1][0]],'rows':rows,'natural_packet':[lo,hi],'H':sum(r[9] for r in rr),'Q':sum(r[10] for r in rr),'A':sum(r[9] for r in rows),'QF':sum(r[10] for r in rows),'QE':sum(r[11] for r in rows)}
