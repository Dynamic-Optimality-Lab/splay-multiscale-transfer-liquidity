"""Fresh namespace/root, no fixture factory; independent parent-map A/B replay."""
import sys,json,time,hashlib,importlib.util
from pathlib import Path
BASE=Path(__file__).resolve().parent;CAP=min(300,float(sys.argv[1]));PC=BASE.parent/'06_CERTIFICATES'
sys.path[:0]=[str(PC/'DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER'),str(PC/'DIRECT_CDK5N_11F_STRICT_CLOSURE'),str(BASE.parent/'M3_TWOGAP_AUD01')]
from PC_TYPED_DAG import DAG
from STRICT_LOW_COMPILER import build_slow
import reference as R
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    start=time.process_time();w=read(BASE/'witness.json');r=read(BASE.parent/'M3_UNIFORM02/case_000/obstruction.json');v=read(BASE.parent/'M3_UNIFORM02/case_000/obstruction_audit.json');identity=read(BASE.parent/'M3_UNIFORM02/case_000/formula_identity_audit.json')
    assert v['status']=='INDEPENDENT_PROMOTION_ENDPOINT_AUDIT_PASS' and identity['status']=='INDEPENDENT_SIGN_RUN_FORMULA_IDENTITY_PASS'
    assert hashlib.sha256((BASE.parent/'M3_UNIFORM02/case_000/C_values.json').read_bytes()).hexdigest()==identity['C_sha256']
    oldenv=w['environment'];assert all(k.startswith('MXL') for k in oldenv)
    dag=DAG();L=build_slow(dag,'ROWV');assert len(dag.nodes)<4000000
    env={'ROWV'+k[3:]:value for k,value in oldenv.items()};assert set(env)==set(dag.vars) and len(env)==len(oldenv)
    for name,n in dag.vars.items():
        nd=dag.nodes[n];value=env[name]
        if nd[1]=='bool':assert value in (False,True)
        else:
            width,signed=nd[3][2:4];assert -(1<<(width-1))<=value<(1<<(width-1)) if signed else 0<=value<(1<<width)
    assert env['ROWVw_p0'] and env['ROWVw_nev']==1 and env['ROWV_H']==1
    assert dag.ev_ground(L['root'],env),'Fresh namespace ORIGINAL root rejected witness'
    def val(n):
        z=dag.nodes[n];assert z[0]=='var';return env[z[3][1]]
    def ordinary(o):return {'mu':val(o.mu),'sigma':[val(x) for x in o.sig],'alpha':[[val(o.ak[i]),int(val(o.aS[i])),val(o.aI[i])] for i in range(7)],'b':{'root':val(o.b.root),**{f:[val(x) for x in getattr(o.b,f)] for f in ('kl','rl','kr','rr','lo','hi')}}}
    def flat(s):
        result=[s['mu'],*s['sigma'],s['b']['root']]
        for f in ('kl','rl','kr','rr','lo','hi'):result+=s['b'][f]
        for a in s['alpha']:result+=a
        assert len(result)==147;return result
    s=ordinary(L['s']);t=ordinary(L['t']);assert flat(s)==flat(w['source']) and flat(t)==flat(w['destination'])
    assert s['mu']==t['mu']==341 and s['sigma']==t['sigma']==[4,1]+[0]*8
    B=read(BASE.parent/'M3_UNITPAIR01/B_bank.json');assert R.core_view(s['b'])==R.frozen(B['trees'][1647]) and R.core_view(t['b'])==R.frozen(B['trees'][2403])
    assert R.raw_normalize(s['alpha'])==R.frozen(r['source_alpha']) and R.raw_normalize(t['alpha'])==R.frozen(r['destination_alpha'])
    wit=L['wit'];seen=set();visible={}
    actualA=R.tree(w['A_source'])
    def inorder(tree):return [] if tree is None else inorder(tree[1])+[tree[0]]+inorder(tree[2])
    keys=inorder(actualA);assert len(keys)==14 and len(set(keys))==14 and {16*i for i in range(9)}<=set(keys)
    sig=[0]*10
    for key in keys:
        if key not in {16*i for i in range(9)}:sig[key//16+1]+=1
    assert sig==s['sigma']
    def prefix(i):
        assert i not in seen and 0<=i<127 and val(wit.p[i]);seen.add(i)
        rank=val(wit.rank[i]);key=keys[rank];iss=val(wit.isS[i]);assert iss==(key in {16*j for j in range(9)})
        if iss:assert key==16*val(wit.sidx[i])
        visible[i]=key;children=[]
        for kk,cc in ((wit.kleft,wit.cleft),(wit.kright,wit.cright)):
            kind,ref=val(kk[i]),val(cc[i]);assert kind in (0,1,2)
            if kind==0:assert ref<127;children.append(prefix(ref))
            else:children.append(None) # opaque/empty erase only in this independent proof view.
        return (key,*children)
    pref=prefix(0);assert seen=={i for i in range(127) if val(wit.p[i])}
    assert R.observations(pref,visible[0])==R.raw_normalize(s['alpha'])
    nev=val(wit.nev);assert nev==1 and val(wit.evK[0]);target_slot=val(wit.evT[0]);target=visible[target_slot];assert target==64
    Adepth=R.depth(pref,target);assert Adepth==val(wit.evd[0])==1
    after=R.splay(pref,target);assert R.observations(after,visible[0])==R.raw_normalize(t['alpha'])
    actualB=R.tree(w['B_source']);depthB=R.depth(actualB,target);Bafter=R.splay(actualB,target)
    def Btree(b):
        used=set()
        def go(i):
            assert 0<=i<19 and i not in used;used.add(i);out=[]
            for kf,rf in (('kl','rl'),('kr','rr')):
                k,ref=b[kf][i],b[rf][i];out.append(go(ref) if k==0 and ref<19 else None)
            return (16*i if i<9 else 16*(i-9)-8,*out)
        return go(b['root'])
    assert Btree(s['b'])==actualB and Btree(t['b'])==Bafter
    H=(Adepth+1)//2;q=depthB//2;weight=2*H-q
    assert (H,q,weight)==(1,1,1) and H==val(L['H']) and q==val(L['bt'].q) and weight==val(L['w']) and depthB==val(L['bt'].bd[0]) and val(L['bt'].bT[0])==4
    ds,dt=v['source']['D_run'],v['destination']['D_run'];assert (ds,dt)==(2,0)
    chi=lambda b:b['kr'][8]==0 and b['rr'][8]==19
    assert chi(s['b'])==chi(t['b']);candidate_res=weight+dt-ds;assert candidate_res==-1
    candidateW_s=-ds-5*int(chi(s['b']));candidateW_t=-dt-5*int(chi(t['b']));assert weight-candidateW_t+candidateW_s==-1
    oldres=weight-r['old_certified_J_destination']+r['old_certified_J_source'];assert oldres==0
    result={'status':'INDEPENDENT_ORIGINAL_LOW_REALIZABILITY_VERIFIED','fresh_namespace':'ROWV','namespace_rename_bijective':True,'original_root':True,'factory_called':False,'all_variable_widths_valid':True,'all147_source_and_destination_coordinates_match':True,'mu':341,'sigma':s['sigma'],'source_B_core_id':1647,'source_A_profile_id':2073,'destination_B_core_id':2403,'destination_A_profile_id':2072,'independent_A_prefix_rotation':True,'independent_B_rotation':True,'A_depth':Adepth,'B_depth':depthB,'H':H,'q':q,'weight':weight,'terminal_target':4,'source_D_run':ds,'destination_D_run':dt,'candidate_residual':candidate_res,'candidate_full_W_residual':-1,'old_certificate_residual':oldres,'chi8':chi(s['b']),'debt_audits_reused_not_recomputed':True,'full_endpoints_close':flat(s)==flat(t),'original_negative_cycle_certified':False,'DAG_nodes':len(dag.nodes),'variables':len(dag.vars),'new_original_root_evaluations':1,'CPU_seconds':time.process_time()-start,'CPU_cap':CAP}
    assert result['CPU_seconds']<CAP;write(BASE/'independent_verification.json',result);print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error={'type':type(e).__name__,'message':str(e)};raise
    finally:write(BASE/'verification_exit.json',{'whole_process_CPU_seconds':time.process_time(),'CPU_cap':CAP,'error':error})
