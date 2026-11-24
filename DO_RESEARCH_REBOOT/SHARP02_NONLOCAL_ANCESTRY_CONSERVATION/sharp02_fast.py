"""Complete-tree search replay. Indexes are order-preserving physical labels.
No key is contracted. Important candidates are replayed by the frozen full oracle.
"""
from sharp02_common import *
from sharp02_graph import solve

class FastTree:
    def __init__(self,state):
        self.keys=sorted(map(int,state['children']));self.rank={k:i for i,k in enumerate(self.keys)};n=len(self.keys)
        self.l=[-1]*n;self.r=[-1]*n;self.p=[-1]*n
        self.root=-1 if state['root'] is None else self.rank[state['root']]
        for key,(l,r) in state['children'].items():
            k=self.rank[int(key)]
            for side,c in enumerate((l,r)):
                if c is not None:
                    v=self.rank[c];(self.l if side==0 else self.r)[k]=v;self.p[v]=k
    def code(self):return self.root,tuple(self.l),tuple(self.r)
    def state(self):return {'root':None if self.root<0 else self.keys[self.root],'children':{str(k):[None if self.l[i]<0 else self.keys[self.l[i]],None if self.r[i]<0 else self.keys[self.r[i]]] for i,k in enumerate(self.keys)}}
    def path(self,x):
        out=[];k=self.root
        while k!=x:
            assert k>=0
            out.append(k);k=self.l[k] if x<k else self.r[k]
        return out+[x]
    def mask(self,k):
        ans=0;todo=[] if k<0 else [k]
        while todo:
            k=todo.pop();ans|=1<<k
            if self.l[k]>=0:todo.append(self.l[k])
            if self.r[k]>=0:todo.append(self.r[k])
        return ans
    def rotate(self,u,side,collect=False):
        same=self.l if side==0 else self.r;other=self.r if side==0 else self.l
        v=same[u];assert v>=0;g=self.p[u];middle=other[v]
        gain=(1<<u)|self.mask(other[u]) if collect else 0
        if g<0:self.root=v
        elif self.l[g]==u:self.l[g]=v
        else:assert self.r[g]==u;self.r[g]=v
        self.p[v]=g;same[u]=middle
        if middle>=0:self.p[middle]=u
        other[v]=u;self.p[u]=v
        return v,gain
    def splay(self,x,op=0,collect=False):
        units=[];step=0
        while self.p[x]>=0:
            step+=1;p=self.p[x];g=self.p[p];side=int(x>p)
            if g<0:rot=[(p,side)]
            else:
                z=int(p>g);rot=[(g,z),(p,side)] if side==z else [(p,side),(g,z)]
            ee=[]
            for bit,(u,s) in enumerate(rot):
                y,mask=self.rotate(u,s,collect)
                if collect:ee.append({'id':['A',op,step,bit],'rotation_witness':['A',op,step,bit],
                                      'virtual':False,'created_ancestor':self.keys[y],'created_mask':mask})
            if collect:
                units.extend(ee)
                if len(ee)==1:units.append({**ee[0],'id':['A',op,step,1],'virtual':True})
        return units

def evaluate(source):
    a,b=FastTree(source['initial_A']),FastTree(source['initial_B']);initial=(a.code(),b.code());ks=a.keys
    ops=source['operations'];keeps=[i for i,(tag,x) in enumerate(ops) if tag=='K'];ng=len(keeps)
    endgap={k:i for i,k in enumerate(keeps)};opgap={};segments=[]
    for i,t in enumerate(keeps):
        prev=keeps[i-1];inds=[];k=(prev+1)%len(ops)
        while True:
            inds.append(k);opgap[k]=i
            if k==t:break
            k=(k+1)%len(ops)
        segments.append(inds)
    costs=[];raw=[];starts={};totalQ=0
    for k,(tag,xkey) in enumerate(ops):
        x=a.rank[xkey];ap=a.path(x);costs.append(len(ap)//2)
        raw.append(a.splay(x,k+1,True))
        if tag=='K':
            totalQ+=(len(b.path(x))-1)//2;b.splay(x)
            gi=endgap[k];nextgi=(gi+1)%ng;xx=a.rank[ops[keeps[nextgi]][1]]
            pa=a.path(xx);pb=b.path(xx);Y=set(pb[:-1])-set(pa[:-1])
            starts[nextgi]=(len(pa)//2,(len(pb)-1)//2,Y,pa,pb)
    assert (a.code(),b.code())==initial,('nonclosed source',source['name'])
    units={};free={};caps={};gaps=[];uid=0
    for i,inds in enumerate(segments):
        p,q,Y,pa,pb=starts[i];H=sum(costs[k] for k in inds);u=max(q-2*p,0);c=2*H-min(q,2*p)
        assert H>=p and c>=0
        reserve=min(q,2*p);ordinal=0
        for k in inds:
            for unit in raw[k]:
                unit={**unit,'gap_index':i+1,'reserved_chronological':ordinal<reserve}
                units[uid]=unit
                if ordinal>=reserve:free[uid]=unit
                uid+=1;ordinal+=1
        caps[i+1]=c
        gaps.append({'gap_index':i+1,'KEEP_operation_id':keeps[i]+1,'target':ops[keeps[i]][1],
                     'H':H,'p':p,'q':q,'u':u,'c':c,'Y':sorted(ks[y] for y in Y),
                     'A_path':[ks[y] for y in pa],'B_path':[ks[y] for y in pb]})
    weights={str(g['gap_index']):g['u'] for g in gaps if g['u']};adj={};alladj={}
    for g in gaps:
        if not g['u']:continue
        i=str(g['gap_index']);Y=set(g['Y']);bit=1<<a.rank[g['target']]
        adj[i]={j for j,v in free.items() if v['created_ancestor'] in Y and v['created_mask']&bit}
        alladj[i]={j for j,v in units.items() if v['created_ancestor'] in Y and v['created_mask']&bit}
    A=sum(costs);U=sum(weights.values());C=sum(caps.values())
    if ng:assert U-C==totalQ-2*A
    else:assert totalQ==0
    return {'name':source['name'],'A':A,'Q':totalQ,'U':U,'C':C,'Delta':totalQ-2*A,'n':len(ks),'operations':len(ops),
            'gaps':gaps,'weights':weights,'adj':adj,'all_adj':alladj,'units':units,'free':free,'capacities':caps}

def recurrent(seed,word,name,max_orbit=32):
    if not word:return None
    a,b=FastTree(seed['initial_A']),FastTree(seed['initial_B']);seen={}
    for v in range(max_orbit+1):
        code=(a.code(),b.code())
        if code in seen:
            u=seen[code];L=v-u
            if len(word)*L>20000:return None
            return {'name':name,'family':'SHARP02_targeted_recurrent','initial_A':a.state(),'initial_B':b.state(),
                    'diagonal_initial':seed.get('diagonal_initial',seed['initial_A']),
                    'reaching_prefix':seed.get('reaching_prefix',[])+word*u,'operations':word*L,
                    'seed_source':seed['name'],'orbit_preperiod':u,'orbit_period':L,'generating_word':word}
        seen[code]=v
        if v==max_orbit:return None
        for tag,key in word:
            x=a.rank[key];a.splay(x)
            if tag=='K':b.splay(x)

if __name__=='__main__':
    with Run('fast_oracle_validation_v001',limit=60) as run:
        old=read(OLD/'SHARP01_RESULTS.json')['sources'];sources=read(OLD/'SHARP01_SOURCE_WITNESSES.json')['sources']
        idx=read(OLD/'SHARP01_GAP_LEDGER.json')['ledgers']
        from sharp02_graph import graph_data
        for num,(src,sm,it) in enumerate(zip(sources,old,idx)):
            z=evaluate(src)
            assert all(z[k]==sm[k] for k in ('A','Q','U','C','Delta'))
            orig=graph_data(read(OLD/it['path']))
            assert z['weights']==orig['weights'] and z['adj']==orig['adj'] and z['all_adj']==orig['all_adj']
            assert set(z['free'])==set(orig['free'])
            ranks={k:i for i,k in enumerate(sorted(map(int,src['initial_A']['children'])))}
            for j,v in z['units'].items():
                ov=orig['units'][j]
                assert all(v[k]==ov[k] for k in ('id','rotation_witness','virtual','gap_index','created_ancestor','reserved_chronological'))
                assert v['created_mask']==sum(1<<ranks[x] for x in ov['created_targets'])
            if num%10==0:run.check(sources_verified=num+1)
        write(BASE/'SHARP02_FAST_ORACLE_VALIDATION.json',{'status':'PASS','sources':len(sources),'all_costs_and_every_actual_unit_and_both_adjacencies_match':True})
        print('PASS: full-key search oracle equals frozen exact ledgers on all 79 sources')
