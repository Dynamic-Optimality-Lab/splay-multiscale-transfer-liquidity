"""Complete-production-high checks, including fringe and exact positive cycles."""
import sys,json,itertools,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from experiment import FIELDS,structure,fullkey,chain,trace,chi
sys.path[:0]=[
'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER',
'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE',
'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE']
from PC_TYPED_DAG import DAG,BOOL
from PC_B_CONTROLLER import BTrace,b_splay_event,crank
from STRICT_HIGH_COMPILER import build_shigh
OUT=Path('DO_RESEARCH_REBOOT/M2_SEP01/full_high_controls.json')
assert not OUT.exists()
def annotate_full(raw,sig):
    m={'root':raw['root'],**{f:list(raw[f]) for f in FIELDS[:4]}}
    present=set(range(9))|{9+g for g in range(10) if sig[g]!=0}
    lo=[crank(i) for i in range(19)];hi=list(lo);par=[19]*19;dep=[0]*19;seen=set()
    counts=[0]*19
    for i in range(19):
        for k,r in (('kl','rl'),('kr','rr')):
            if m[k][i]==0 and m[r][i]<19:counts[m[r][i]]+=1
    for i in range(19):
        assert counts[i]==(i in present and i!=m['root']),(i,counts[i])
    def dfs(i,l,h,p,z):
        assert i in present and i not in seen and l<=crank(i)<=h,(i,l,h)
        seen.add(i);lo[i]=l;hi[i]=h;par[i]=p;dep[i]=z
        if i>=9:assert m['kl'][i]==m['kr'][i]==2
        for side,k,r in ((0,'kl','rl'),(1,'kr','rr')):
            c=m[r][i]
            if m[k][i]==0 and c<19:dfs(c,l if side==0 else crank(i)+1,crank(i)-1 if side==0 else h,i,z+1)
    dfs(m['root'],0,18,19,0)
    assert seen==present
    m.update(lo=lo,hi=hi,bpar=par,bdep=dep)
    return m
def initial(h,sig,phantom=True):
    root=8-h
    m={'root':root,'kl':[2]*19,'rl':[19]*19,'kr':[2]*19,'rr':[19]*19}
    for i in range(1,root+1):m['kl'][i]=0;m['rl'][i]=i-1
    for i in range(root,8):m['kr'][i]=0;m['rr'][i]=i+1
    if phantom:m['kr'][8]=0;m['rr'][8]=19
    for g in range(10):
        if not sig[g]:continue
        i=root
        while True:
            side='l' if 2*g<crank(i) else 'r';k='k'+side;r='r'+side
            if m[k][i]==0 and m[r][i]<19:i=m[r][i]
            else:
                assert m[k][i]==2,('occupied phantom gap',g,i)
                m[k][i]=0;m[r][i]=9+g;break
    return annotate_full(m,sig)
d=DAG();H=build_shigh(d,'SEPF');bt=BTrace(d,'SEPFbt')
out=b_splay_event(d,H['s'].b,bt,0,d.const_bool(False))
def name(n):return d.nodes[n][3][1]
def put(e,n,v):e[name(n)]=v
def fill_b(e,b,m):
    put(e,b.root,m['root'])
    for f in FIELDS:
        for n,v in zip(getattr(b,f),m[f]):put(e,n,v)
def aux(e,prefix,m):
    for i in range(19):e[f'{prefix}_bpar{i}']=m['bpar'][i];e[f'{prefix}_bdep{i}']=m['bdep'][i]
def check(source,x,length,sig,label):
    env={nm:False if d.nodes[n][1]==BOOL else 0 for nm,n in d.vars.items()}
    mu=391
    for obj in (H['s'],H['t'],H['g']):
        put(env,obj.mu,mu)
        for n,v in zip(obj.sig,sig):put(env,n,v)
    for obj in (H['s'],H['t']):
        for n in obj.ak:put(env,n,2)
        put(env,obj.aS[0],True);put(env,obj.aI[0],8)
    put(env,H['g'].v,8)
    fill_b(env,H['s'].b,source);aux(env,'SEPFsbs',source)
    _,_,path,dirs=trace(source,x,length)
    env['SEPFbt_bT0']=x;env['SEPFbt_bd0']=length
    for k,v in enumerate(path):env[f'SEPFbt_bp0_{k}']=v
    for k,v in enumerate(dirs):env[f'SEPFbt_bdir0_{k}']=v
    put(env,H['q'],length//2);put(env,H['w1'],6-length//2)
    raw={'root':d.ev_ground(out.root,env),
         **{f:[d.ev_ground(n,env) for n in getattr(out,f)] for f in FIELDS[:4]}}
    dest=annotate_full(raw,sig)
    fill_b(env,H['t'].b,dest);fill_b(env,H['g'].b,dest)
    aux(env,'SEPFsbt',dest);aux(env,'SEPFsbg',dest)
    assert d.ev_ground(H['root'],env),label
    for nm,n in d.vars.items():
        k,t,a,e=d.nodes[n]
        if t!=BOOL:
            width=e[2];signed=e[3]
            assert -(1<<(width-1))<=env[nm]<(1<<(width-1)) if signed else 0<=env[nm]<(1<<width),(nm,env[nm])
    return {'label':label,'source':source,'destination':dest,'target':x,
            'd':length,'q':length//2,'w':6-length//2,'path':path[:length+1],
            'dirs':dirs[:length],'mu':mu,'sigma':sig,'alpha_root':8,
            'complete_high_root':True}
start=time.process_time();records=[]
profiles=[[0]*10,[266 if g%2 else 1 for g in range(9)]+[0]]
for profile,sig in enumerate(profiles):
    for h in range(1,9):
        source=initial(h,sig)
        for length in (h,h+1):
            record=check(source,8,length,sig,f'profile{profile}_h{h}_d{length}')
            assert chi(record['destination'])
            records.append(record)
    source=initial(0,sig,False)
    control=check(source,8,18,sig,f'clean_h0_profile{profile}')
    assert control['source']['root']==control['destination']['root']==8 and chi(control['destination'])
    records.append(control)
sig=[0]*10
entry=initial(0,sig)
lead=check(entry,0,8,sig,'lead_to_cycle')
forward=check(lead['destination'],8,2,sig,'cycle_edge_8')
back=check(forward['destination'],0,2,sig,'cycle_edge_0')
assert fullkey(back['destination'])==fullkey(forward['source'])
assert fullkey(forward['destination'])==fullkey(back['source'])
assert sum(r['w'] for r in (forward,back))==10
result={'status':'COMPLETE','complete_high_controls':len(records)+3,
        'cpu_seconds':round(time.process_time()-start,3),'records':records,
        'lead':lead,'positive_closed_cycle':[forward,back],'cycle_weight':10,
        'full_B_closure':True,'fixed_alpha_closure':True}
with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
print(json.dumps({k:v for k,v in result.items() if k not in ('records','lead','positive_closed_cycle')}))

