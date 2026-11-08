"""Complete unmodified low/high roots, full shared states and mixed-cycle controls."""
import sys,json,time
from pathlib import Path
sys.path[:0]=['python/independent',
 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER',
 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE',
 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE']
import splay as S
from PC_TYPED_DAG import DAG,BOOL
from PC_B_CONTROLLER import crank
from PC_CONCRETIZE import AModel,build_envA,build_envI,build_envBT,build_envW,depths_keys
from STRICT_CERTIFY import alpha7_of
from STRICT_LOW_COMPILER import build_slow
from STRICT_HIGH_COMPILER import build_shigh
OUT=Path('DO_RESEARCH_REBOOT/M3_PHI01/full_mixed_controls.json')
FIELDS=('kl','rl','kr','rr','lo','hi');MARKED=(0,2,4,6,8);MU=sum(1<<i for i in MARKED)
start=time.process_time()

def from_serial(t):return S.LEAF if t is None else S.node(t[0],from_serial(t[1]),from_serial(t[2]))
def serial(t):return None if t==S.LEAF else [t[1],serial(t[2]),serial(t[3])]

def bmodel(t,phantom=False):
    raw={'root':t[1] if t[1] in range(9) else (9 if t[1]==-1 else 18),
         'kl':[2]*19,'rl':[19]*19,'kr':[2]*19,'rr':[19]*19}
    def idx(k):return k if k in range(9) else (9 if k==-1 else 18)
    present=set();par=[19]*19;dep=[0]*19;lo=[crank(i) for i in range(19)];hi=list(lo)
    def go(n,l,h,p,z):
        i=idx(n[1]);assert i not in present and l<=crank(i)<=h
        present.add(i);par[i]=p;dep[i]=z;lo[i]=l;hi[i]=h
        for side,k,r,child in ((0,'kl','rl',n[2]),(1,'kr','rr',n[3])):
            if child!=S.LEAF:
                raw[k][i]=0;raw[r][i]=idx(child[1])
                go(child,l if side==0 else crank(i)+1,crank(i)-1 if side==0 else h,i,z+1)
    go(t,0,18,19,0)
    if phantom:
        assert raw['kr'][8]==2;raw['kr'][8]=0;raw['rr'][8]=19
    raw.update(lo=lo,hi=hi,bpar=par,bdep=dep)
    return raw

def shadow(t):return [list(alpha7_of(t,set(range(9)),list(range(9)))[p]) for p in ('root','L','R','LL','LR','RL','RR')]
def state(a,b,sig):return {'mu':MU,'b':{k:b[k] for k in ('root',)+FIELDS},'alpha':shadow(a),'sigma':list(sig)}
def phi(s):return -3*int(s['b']['kr'][8]==0 and s['b']['rr'][8]==19)
def blank(d):return {nm:False if d.nodes[n][1]==BOOL else 0 for nm,n in d.vars.items()}
def put(d,e,n,v):e[d.nodes[n][3][1]]=v
def fillB(d,e,b,m):
    put(d,e,b.root,m['root'])
    for f in FIELDS:
        for n,v in zip(getattr(b,f),m[f]):put(d,e,n,v)
def aux(e,prefix,m):
    for i in range(19):e[f'{prefix}_bpar{i}']=m['bpar'][i];e[f'{prefix}_bdep{i}']=m['bdep'][i]
def fillState(d,e,obj,a,b,sig):
    put(d,e,obj.mu,MU);fillB(d,e,obj.b,b)
    for p,(k,s,i) in enumerate(shadow(a)):
        put(d,e,obj.ak[p],k);put(d,e,obj.aS[p],bool(s));put(d,e,obj.aI[p],i)
    for n,v in zip(obj.sig,sig):put(d,e,n,v)
def bounds(d,e):
    for nm,n in d.vars.items():
        _,typ,_,z=d.nodes[n]
        if typ!=BOOL:
            width=z[2];signed=z[3]
            assert (-(1<<(width-1))<=e[nm]<(1<<(width-1))) if signed else (0<=e[nm]<(1<<width)),(nm,e[nm])
def path(t,x):
    dk=depths_keys(t);p=[x];dr=[]
    while dk[p[-1]][1] is not None:
        _,parent,side=dk[p[-1]];p.append(parent);dr.append(bool(side))
    return p,dr

def low(d,L,A,B,word,phantom,label):
    assert time.process_time()-start<300,'UNKNOWN: controls cap'
    am=AModel(A,set(range(9)));sig=am.sig;env=blank(d)
    build_envA(env,am,set(range(9)),'MXLw');build_envI(env,am,set(range(9)),'MXLv')
    key2slot={v['key']:i for i,v in am.slots.items()}
    aw=[];bw=[];ac=A;bc=B;boundaries=[bmodel(B,phantom)];H=0
    for mode,x in word:
        ap,ad=path(ac,x);assert len(ap)<=5
        aw.append({'isK':mode=='K','slot':key2slot[x],'d':len(ad),
                   'path':[key2slot[k] for k in ap],'dirs':ad})
        H+=(len(ad)+1)//2;ac=S.trace(ac,x)[0]
        bp,bd=path(bc,x)
        ix=lambda k:k if k in range(9) else (9 if k==-1 else 18)
        bw.append({'T':ix(x),'d':len(bd),'path':[ix(k) for k in bp],'dirs':bd})
        if mode=='K':bc=S.trace(bc,x)[0]
        boundaries.append(bmodel(bc,phantom))
    assert 1<=H<=2
    build_envW(env,aw,'MXLw');build_envBT(env,bw,'MXLbt')
    q=bw[-1]['d']//2;w=2*H-q
    env['MXL_H']=H;env['MXL_w']=w;env['MXLbt_q']=q
    source=boundaries[0];dest=boundaries[-1]
    fillState(d,env,L['s'],A,source,sig);fillState(d,env,L['t'],ac,dest,sig)
    for j in range(6):aux(env,f'MXLsb{j}',boundaries[min(j,len(boundaries)-1)])
    bounds(d,env);accepted=d.ev_ground(L['root'],env)
    if not accepted:
        bad=[]
        # The conjunction chain's direct leaves localize a failed control without changing source.
        vals={}
        def leaves(n):
            k,t,a,z=d.nodes[n]
            if k=='and':yield from leaves(a[0]);yield from leaves(a[1])
            else:yield n
        sys.setrecursionlimit(100000)
        for n in leaves(L['root']):
            if not d.ev_ground(n,env):bad.append([n,repr(d.nodes[n])])
            if len(bad)==5:break
        raise AssertionError((label,'full low FALSE',bad))
    s=state(A,source,sig);t=state(ac,dest,sig)
    assert phi(s)==phi(t)
    if phantom:assert all(m['kr'][8]==0 and m['rr'][8]==19 for m in boundaries)
    record={'label':label,'kind':'LOW','root':True,'source':s,'destination':t,
            'word':word,'A_source':serial(A),'A_destination':serial(ac),
            'B_source':serial(B),'B_destination':serial(bc),'H':H,'q':q,'w':w,
            'phi_source':phi(s),'phi_destination':phi(t),'B_event_boundaries':boundaries,
            'A_paths':aw,'B_paths':bw,'environment':{nm:env[nm] for nm in d.vars}}
    print(json.dumps({'control':label,'w':w,'phi':phi(s),'elapsed_cpu':round(time.process_time()-start,3)}),flush=True)
    return ac,bc,record

def high(d,L,A,B,Ad,Bd,phantom,label):
    assert time.process_time()-start<300
    sig=[0]*10;source=bmodel(B,phantom);dest=bmodel(Bd,phantom);env=blank(d)
    fillState(d,env,L['s'],A,source,sig);fillState(d,env,L['t'],Ad,dest,sig)
    put(d,env,L['g'].mu,MU);fillB(d,env,L['g'].b,dest)
    for n,v in zip(L['g'].sig,sig):put(d,env,n,v)
    put(d,env,L['g'].v,Ad[1])
    aux(env,'MXHsbs',source);aux(env,'MXHsbt',dest);aux(env,'MXHsbg',dest)
    x=Bd[1];bp,bd=path(B,x);length=len(bd);assert S.trace(B,x)[0]==Bd
    env['MXHbt_bT0']=x;env['MXHbt_bd0']=length
    for k,v in enumerate(bp):env[f'MXHbt_bp0_{k}']=v
    for k,v in enumerate(bd):env[f'MXHbt_bdir0_{k}']=v
    put(d,env,L['q'],length//2);put(d,env,L['w1'],6-length//2)
    bounds(d,env);assert d.ev_ground(L['root'],env),label
    s=state(A,source,sig);t=state(Ad,dest,sig);w=6-length//2
    assert phi(t)-phi(s)<=w
    return {'label':label,'kind':'HIGH','root':True,'source':s,'destination':t,
            'd':length,'q':length//2,'w':w,'target':x,
            'shared_midpoint':{'mu':MU,'sigma':sig,'b':t['b'],'v':Ad[1]},
            'phi_source':phi(s),'phi_destination':phi(t),
            'environment':{nm:env[nm] for nm in d.vars}}

def insert(t,x):
    if t==S.LEAF:return S.node(x,S.LEAF,S.LEAF)
    return S.node(t[1],insert(t[2],x),t[3]) if x<t[1] else S.node(t[1],t[2],insert(t[3],x))

def main():
    assert not OUT.exists()
    d=DAG();L=build_slow(d,'MXL');low_nodes=len(d.nodes);assert low_nodes<=4000000
    print(json.dumps({'low_DAG_nodes':low_nodes,'build_cpu':round(time.process_time()-start,3)}),flush=True)
    dh=DAG();HH=build_shigh(dh,'MXH');assert len(dh.nodes)<=4000000
    search=json.loads(Path('DO_RESEARCH_REBOOT/M3_PHI01/mixed_search.json').read_text())
    records=[];cycles=[]
    for phantom in (False,True):
        for k in ('1','2','3'):
            candidate=search['best_candidates'][k];A0=from_serial(candidate['A0']);B0=from_serial(candidate['B0'])
            a=A0;b=B0;legs=[]
            for j,e in enumerate(candidate['low_legs']):
                a,b,r=low(d,L,a,b,[('K',e['target'])],phantom,f'cycle_{k}_p{int(phantom)}_low{j}')
                records.append(r);legs.append(r)
            r=high(dh,HH,a,b,A0,B0,phantom,f'cycle_{k}_p{int(phantom)}_high')
            records.append(r);legs.append(r)
            for left,right in zip(legs,legs[1:]+legs[:1]):assert left['destination']==right['source']
            weight=sum(e['w'] for e in legs);assert weight==candidate['total_weight']>=0
            cycles.append({'labels':[r['label'] for r in legs],'total_weight':weight,
                           'low_weight':sum(e['w'] for e in legs if e['kind']=='LOW'),
                           'high_weight':sum(e['w'] for e in legs if e['kind']=='HIGH'),
                           'full_state_closure':True,'chi8':phantom})
    neg=search['most_negative_low_edge']
    for phantom in (False,True):
        _,_,r=low(d,L,from_serial(neg['A']),from_serial(neg['B']),[('K',neg['leg']['target'])],phantom,
                  f'negative_low_phi_obstruction_p{int(phantom)}')
        assert r['w']==-2 and r['phi_source']==r['phi_destination'];records.append(r)
    # An actual internal gap at the intermediate boundary; its identity and population persist.
    A=S.node(4,S.node(-1,S.LEAF,S.node(0,S.LEAF,S.balanced(range(1,4)))),S.balanced(range(5,9)))
    B=insert(S.balanced(range(9)),-1)
    _,_,r=low(d,L,A,B,[('K',-1),('K',0)],True,'fringe_internal_gap_macro')
    assert r['B_event_boundaries'][1]['root']==9
    assert r['B_event_boundaries'][1]['kr'][9]==0
    assert r['source']['sigma'][0]==1;records.append(r)
    c=search['best_candidates']['1']
    _,_,r=low(d,L,insert(from_serial(c['A0']),9),insert(from_serial(c['B0']),9),[('K',4)],False,
              'present_outer_gap9_phi_zero')
    assert r['source']['sigma'][9]==1 and phi(r['source'])==phi(r['destination'])==0
    records.append(r)
    assert time.process_time()-start<300
    result={'status':'COMPLETE','low_DAG_nodes':low_nodes,'high_DAG_nodes':len(dh.nodes),
            'queries':len(records),'low_queries':sum(r['kind']=='LOW' for r in records),
            'high_queries':sum(r['kind']=='HIGH' for r in records),'cycles':cycles,
            'potential_obstruction':'M2 Phi has delta zero on valid w=-2 low edges; it is not a full-graph potential',
            'cpu_seconds':round(time.process_time()-start,3),'records':records}
    with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='records'}),flush=True)
if __name__=='__main__':main()
