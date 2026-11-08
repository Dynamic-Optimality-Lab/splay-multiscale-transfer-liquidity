"""Exact diagnostic evaluation of unchanged frozen B functions; no solver."""
import sys,json,time,argparse,itertools,hashlib
from pathlib import Path
ROOT=Path.cwd()
PC=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER'
sys.path.insert(0,str(PC))
from PC_B_CONTROLLER import BState,BTrace,b_parent_of,b_side_of,verify_bpath,b_splay_event
class V:
    __slots__=('v',)
    def __init__(self,v):self.v=v
    def __bool__(self):return True # a DAG handle is truthy even when its VALUE is zero
class Exact:
    def const_int(self,v,*a,**k):return V(v)
    def const_bool(self,v):return V(bool(v))
    def var_int(self,*a,**k):return V(0)
    def var_bool(self,*a,**k):return V(False)
    def EQ(self,a,b):return V(a.v==b.v)
    def LT(self,a,b):return V(a.v<b.v)
    def LE(self,a,b):return V(a.v<=b.v)
    def ADD(self,a,b,*args):return V(a.v+b.v)
    def SUB(self,a,b,*args):return V(a.v-b.v)
    def NOT(self,a):return V(not a.v)
    def AND(self,*args):return V(all(a.v for a in args))
    def OR(self,*args):return V(any(a.v for a in args))
    def ITE(self,c,a,b):return a if c.v else b
D=Exact()
FIELDS=('kl','rl','kr','rr','lo','hi')
def unpack(b):
    return {'root':b.root.v,**{f:[v.v for v in getattr(b,f)] for f in FIELDS}}
def pack(m):
    b=BState.__new__(BState);b.d=D;b.root=V(m['root'])
    for f in FIELDS:setattr(b,f,[V(v) for v in m[f]])
    return b
def structure(m):return (m['root'],*(tuple(m[f]) for f in FIELDS[:4]))
def fullkey(m):return (m['root'],*(tuple(m[f]) for f in FIELDS))
def chi(m):return m['kr'][8]==0 and m['rr'][8]==19
def annotate(raw):
    """Fresh canonical endpoint annotations, sig=0; reject invalid real topology."""
    m={'root':raw['root'],**{f:list(raw[f]) for f in FIELDS[:4]}}
    if m['root'] not in range(9):return None
    if any(m[f][i]!=2 for f in ('kl','kr') for i in range(9,19)):return None
    counts=[0]*19
    for i in range(19):
        for k,r in (('kl','rl'),('kr','rr')):
            if m[k][i]==0 and m[r][i]<19:counts[m[r][i]]+=1
    if counts[m['root']] or any(counts[i]!=(i!=m['root']) for i in range(9)):return None
    if any(counts[9:]):return None
    m['lo']=[2*i+1 if i<9 else 2*(i-9) for i in range(19)]
    m['hi']=list(m['lo']);par=[19]*19;dep=[0]*19;seen=set()
    def visit(i,l,h,p,z):
        if i in seen or not l<=2*i+1<=h:raise ValueError()
        seen.add(i);m['lo'][i]=l;m['hi'][i]=h;par[i]=p;dep[i]=z
        for side,k,r in ((0,'kl','rl'),(1,'kr','rr')):
            c=m[r][i]
            if m[k][i]==0 and c<19:
                if c>=9:raise ValueError()
                visit(c,l if side==0 else 2*i+2,2*i if side==0 else h,i,z+1)
    try:visit(m['root'],0,18,19,0)
    except (ValueError,RecursionError):return None
    if seen!=set(range(9)):return None
    m['bpar']=par;m['bdep']=dep
    return m
def chain(root=8,phantom=True):
    m={'root':root,'kl':[2]*19,'rl':[19]*19,'kr':[2]*19,'rr':[19]*19}
    for i in range(1,root+1):m['kl'][i]=0;m['rl'][i]=i-1
    if root==7:m['kr'][7]=0;m['rr'][7]=8
    if phantom:m['kr'][8]=0;m['rr'][8]=19
    ans=annotate(m);assert ans is not None
    return ans
def trace(m,x,d):
    b=pack(m);bt=BTrace(D,'E');bt.bT[0]=V(x);bt.bd[0]=V(d)
    p=x;path=[p];dirs=[]
    for k in range(18):
        par=b_parent_of(D,b,V(p));side=b_side_of(D,b,V(p),par)
        dirs.append(side.v);p=par.v;path.append(p)
    bt.bpath[0]=[V(v) for v in path];bt.bdir[0]=[V(v) for v in dirs]
    return b,bt,path,dirs
def edge(m,x,d):
    b,bt,path,dirs=trace(m,x,d)
    if not verify_bpath(D,b,bt,0).v:return None,'STATIC'
    out=unpack(b_splay_event(D,b,bt,0,D.const_bool(False)))
    if structure(out)==structure(m):return None,'DIFF'
    dest=annotate(out)
    if dest is None:return None,'ENDPOINT'
    return {'target':x,'d':d,'q':d//2,'w':6-d//2,'path':path[:d+1],
            'dirs':dirs[:d],'source':m,'destination':dest},'VALID'
def probe():
    start=chain()
    first,status=edge(start,0,8);assert status=='VALID' and first['w']==2
    after=first['destination'];rows=[]
    for d in range(19):
        e,status=edge(after,8,d)
        rows.append({'d':d,'w':6-d//2,'status':status,
                     'destination_chi8':chi(e['destination']) if e else None})
    print(json.dumps({'source':after,'after_smaller_target':0,'smaller_weight':2,
                      'key8_rows':rows},indent=2))
def patterns():
    rows=[]
    for h in range(9):
        root=8-h
        raw={'root':root,'kl':[2]*19,'rl':[19]*19,'kr':[2]*19,'rr':[19]*19}
        for i in range(1,root+1):raw['kl'][i]=0;raw['rl'][i]=i-1
        for i in range(root,8):raw['kr'][i]=0;raw['rr'][i]=i+1
        raw['kr'][8]=0;raw['rr'][8]=19
        state=annotate(raw);assert state is not None
        valid=[];rejections={}
        for length in range(19):
            e,status=edge(state,8,length)
            if e:valid.append({'d':length,'w':e['w'],'chi8':chi(e['destination'])})
            else:rejections[length]=status
        rows.append({'h':h,'valid':valid,'rejections':rejections})
    print(json.dumps(rows,indent=2))
def symbolic_patterns():
    rows=[]
    for h in range(9):
        spine=list(range(8,7-h,-1));period=spine+[19]
        for length in range(19):
            m={'root':spine[-1],**{f:[f'S.{f}{i}' for i in range(19)] for f in FIELDS}}
            m['kr'][8]=0;m['rr'][8]=19
            for j in range(1,h+1):m['kr'][spine[j]]=0;m['rr'][spine[j]]=spine[j-1]
            b=pack(m);bt=BTrace(D,'S');bt.bT[0]=V(8);bt.bd[0]=V(length)
            bt.bpath[0]=[V(period[k%len(period)]) for k in range(19)]
            bt.bdir[0]=[V(k%len(period)!=h) for k in range(18)]
            out=unpack(b_splay_event(D,b,bt,0,V(False)))
            links=[]
            for i in range(19):
                for side,k,r in ((0,'kl','rl'),(1,'kr','rr')):
                    child=out[r][i]
                    if out[k][i]==0 and isinstance(child,int) and child<19:links.append((i,child,side))
            claim=[a for a in links if a[1]==out['root']]
            graph={i:[] for i in range(19)}
            for a,c,_ in links:graph[a].append(c)
            def findcycle():
                active=[];done=set()
                def dfs(i):
                    if i in active:return active[active.index(i):]+[i]
                    if i in done:return None
                    active.append(i)
                    for j in graph[i]:
                        answer=dfs(j)
                        if answer:return answer
                    active.pop();done.add(i)
                for i in range(19):
                    answer=dfs(i)
                    if answer:return answer
            cycle=findcycle()
            identity=structure(out)==structure(m)
            status='DIFF' if identity else ('ROOT_CLAIM' if claim else ('CYCLE' if cycle else 'UNDECIDED'))
            rows.append({'h':h,'d':length,'status':status,'cycle':cycle,'root_claims':claim,
                         'chi8_output':out['kr'][8]==0 and out['rr'][8]==19})
    bad=[r for r in rows if r['d']>r['h']+1 and r['status']=='UNDECIDED']
    print(json.dumps({'rows':rows,'excess_cases':sum(r['d']>r['h']+1 for r in rows),
                     'unresolved_excess':bad},indent=2))
if __name__=='__main__':
    mode=sys.argv[1] if len(sys.argv)>1 else 'probe'
    {'patterns':patterns,'symbolic':symbolic_patterns,'probe':probe}[mode]()

