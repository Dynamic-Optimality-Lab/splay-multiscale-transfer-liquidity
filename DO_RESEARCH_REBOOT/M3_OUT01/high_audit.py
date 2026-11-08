"""Full original high-relation controls for dirty smaller-key families."""
import sys,json,time
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'DO_RESEARCH_REBOOT/M2_SEP01'))
from experiment import annotate,trace,FIELDS,chi
sys.path[:0]=[
'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER',
'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE',
'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE']
from PC_TYPED_DAG import DAG,BOOL
from PC_B_CONTROLLER import BTrace,b_splay_event,verify_bpath,crank
from STRICT_HIGH_COMPILER import build_shigh
from STRICT_B_CONTROLLER import BStruct,b_tree_valid
OUT=Path('DO_RESEARCH_REBOOT/M3_OUT01/high_controls.json')
assert not OUT.exists()
def annotation(raw,sig):
    m={'root':raw['root'],**{f:list(raw[f]) for f in FIELDS[:4]}}
    present=set(range(9))|{9+g for g,v in enumerate(sig) if v}
    lo=[crank(i) for i in range(19)];hi=list(lo);par=[19]*19;dep=[0]*19;seen=set();cnt=[0]*19
    for i in range(19):
        for k,r in (('kl','rl'),('kr','rr')):
            if m[k][i]==0 and m[r][i]<19:cnt[m[r][i]]+=1
    assert all(cnt[i]==(i in present and i!=m['root']) for i in range(19))
    def visit(i,l,h,p,z):
        assert i in present and i not in seen and l<=crank(i)<=h
        seen.add(i);lo[i]=l;hi[i]=h;par[i]=p;dep[i]=z
        if i>=9:assert m['kl'][i]==m['kr'][i]==2
        for side,k,r in ((0,'kl','rl'),(1,'kr','rr')):
            c=m[r][i]
            if m[k][i]==0 and c<19:visit(c,l if side==0 else crank(i)+1,crank(i)-1 if side==0 else h,i,z+1)
    visit(m['root'],0,18,19,0);assert seen==present
    m.update(lo=lo,hi=hi,bpar=par,bdep=dep);return m
def model(tree):
    m={'root':tree[0],'kl':[2]*19,'rl':[19]*19,'kr':[2]*19,'rr':[19]*19}
    def visit(n):
        i,l,r=n
        for child,k,f in ((l,'kl','rl'),(r,'kr','rr')):
            if child is not None:m[k][i]=0;m[f][i]=child[0];visit(child)
    visit(tree);return m
d=DAG();H=build_shigh(d,'DSKF');bt=BTrace(d,'DSKFbt')
replayed=b_splay_event(d,H['s'].b,bt,0,d.const_bool(False))
srcvalid=b_tree_valid(d,H['s'].b,BStruct(d,H['s'].b,'DSKFsbs'),H['s'].sig)
pathvalid=verify_bpath(d,H['s'].b,bt,0)
def put(e,n,v):e[d.nodes[n][3][1]]=v
def fill(e,b,m):
    put(e,b.root,m['root'])
    for f in FIELDS:
        for n,v in zip(getattr(b,f),m[f]):put(e,n,v)
def aux(e,prefix,m):
    for i in range(19):e[f'{prefix}_bpar{i}']=m['bpar'][i];e[f'{prefix}_bdep{i}']=m['bdep'][i]
def check(source,x,length,sig,label,expected):
    env={nm:False if d.nodes[n][1]==BOOL else 0 for nm,n in d.vars.items()}
    marked={x,8}
    for i in range(9):
        if len(marked)<5:marked.add(i)
    mu=sum(1<<i for i in marked)
    for obj in (H['s'],H['t'],H['g']):
        put(env,obj.mu,mu)
        for n,v in zip(obj.sig,sig):put(env,n,v)
    for obj in (H['s'],H['t']):
        for n in obj.ak:put(env,n,2)
        put(env,obj.aS[0],True);put(env,obj.aI[0],8)
    put(env,H['g'].v,8)
    fill(env,H['s'].b,source);aux(env,'DSKFsbs',source)
    _,_,path,dirs=trace(source,x,length)
    env['DSKFbt_bT0']=x;env['DSKFbt_bd0']=length
    for k,v in enumerate(path):env[f'DSKFbt_bp0_{k}']=v
    for k,v in enumerate(dirs):env[f'DSKFbt_bdir0_{k}']=v
    put(env,H['q'],length//2);put(env,H['w1'],6-length//2)
    assert d.ev_ground(srcvalid,env) and d.ev_ground(pathvalid,env),label
    raw={'root':d.ev_ground(replayed.root,env),
         **{f:[d.ev_ground(n,env) for n in getattr(replayed,f)] for f in FIELDS[:4]}}
    if expected:
        dest=annotation(raw,sig);claimants=[]
    else:
        claimants=[(i,side) for i in range(19) for side,k,r in (('L','kl','rl'),('R','kr','rr'))
                   if raw[k][i]==0 and raw[r][i]==raw['root']]
        assert claimants,(label,'no final root claim')
        dest={**raw,'lo':[0 if i<9 else 2*(i-9) for i in range(19)],
              'hi':[18 if i<9 else 2*(i-9) for i in range(19)],
              'bpar':[19]*19,'bdep':[0]*19}
    fill(env,H['t'].b,dest);fill(env,H['g'].b,dest)
    aux(env,'DSKFsbt',dest);aux(env,'DSKFsbg',dest)
    accepted=d.ev_ground(H['root'],env)
    assert accepted==expected,(label,accepted,expected)
    for nm,n in d.vars.items():
        k,t,a,e=d.nodes[n]
        if t!=BOOL:
            width=e[2];signed=e[3]
            assert (-(1<<(width-1))<=env[nm]<(1<<(width-1))) if signed else (0<=env[nm]<(1<<width))
    w=6-length//2;ps=-3*chi(source);pt=-3*chi(dest)
    if accepted:assert pt-ps<=w
    return {'label':label,'target':x,'d':length,'q':length//2,'w':w,
            'source_valid':True,'path_valid':True,'high_root':accepted,'expected':expected,
            'forced_final_root_claims':claimants,'source':source,'destination':dest,
            'path':path[:length+1],'dirs':dirs[:length],'mu':mu,'sigma':sig,
            'alpha_root':8,'phi_source':ps,'phi_destination':pt,
            'environment':env,'potential_checked':accepted,'reduced_cost':w-(pt-ps) if accepted else None}

start=time.process_time();records=[]
prior=json.loads(Path('DO_RESEARCH_REBOOT/M2_DSK01/full_high_controls.json').read_text())
points=[r for r in prior['records'] if r['label'].startswith('positive_')]
for j,r in enumerate(points):
    for depth in range(10,14):
        records.append(check(r['source'],r['target'],depth,r['sigma'],f'outside_cheap_candidate_{j}_d{depth}',False))
    records.append(check(r['source'],r['target'],r['d'],r['sigma'],f'positive_boundary_{j}',True))
    assert time.process_time()-start<300,'UNKNOWN high-control cap'
for r in prior['records']:
    if not r['label'].startswith('potential_boundary_clean_h0'):continue
    for depth in (10,11,12,13,18):
        records.append(check(r['source'],r['target'],depth,r['sigma'],r['label']+f'_newd{depth}',True))
        assert chi(records[-1]['destination'])
for r in records:
    assert d.ev_ground(H['root'],r['environment'])==r['expected']
res={'status':'PASS','queries':len(records),'accepted':sum(r['high_root'] for r in records),
     'rejected_cheap_dirty_candidates':sum(not r['high_root'] for r in records),
     'clean_h0_correction_retained':True,'DAG_nodes':len(d.nodes),
     'cpu_seconds':round(time.process_time()-start,3),'records':records}
with OUT.open('x',encoding='utf-8') as f:json.dump(res,f,indent=2)
print(json.dumps({k:v for k,v in res.items() if k!='records'},indent=2))
