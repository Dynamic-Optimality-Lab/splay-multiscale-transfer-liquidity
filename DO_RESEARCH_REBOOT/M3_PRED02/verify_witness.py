"""Fresh original predicate, all raw fields, no factory; independent rotations."""
import json,sys,time,hashlib
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
    start=time.process_time();w=read(BASE/'witness.json');r=read(BASE/'case_000/obstruction.json');ep=read(BASE/'endpoint_audit.json');B=read(BASE.parent/'M3_UNITPAIR01/B_bank.json');tag='P2V';dag=DAG();L=build_slow(dag,tag);assert len(dag.nodes)<4000000
    assert all(k.startswith('MXL') for k in w['environment']);env={tag+k[3:]:v for k,v in w['environment'].items()};assert set(env)==set(dag.vars) and len(env)==len(w['environment'])
    assert hashlib.sha256(json.dumps(w['environment'],sort_keys=True).encode()).hexdigest()==w['environment_sha256']
    for name,n in dag.vars.items():
        nd=dag.nodes[n];v=env[name]
        if nd[1]=='bool':assert v in (False,True)
        else:
            width,signed=nd[3][2:4];assert -(1<<(width-1))<=v<(1<<(width-1)) if signed else 0<=v<(1<<width)
    assert dag.ev_ground(L['root'],env),'Fresh unchanged original LOW root rejects witness'
    def val(n):
        nd=dag.nodes[n];assert nd[0]=='var';return env[nd[3][1]]
    def ordinary(o):return {'mu':val(o.mu),'sigma':[val(v) for v in o.sig],'alpha':[[val(o.ak[i]),int(val(o.aS[i])),val(o.aI[i])] for i in range(7)],'b':{'root':val(o.b.root),**{f:[val(v) for v in getattr(o.b,f)] for f in ('kl','rl','kr','rr','lo','hi')}}}
    def flat(s):
        out=[s['mu'],*s['sigma'],s['b']['root']]
        for f in ('kl','rl','kr','rr','lo','hi'):out+=s['b'][f]
        for a in s['alpha']:out+=a
        assert len(out)==147;return out
    s=ordinary(L['s']);t=ordinary(L['t']);assert flat(s)==flat(w['source']) and flat(t)==flat(w['destination'])
    assert s['sigma']==t['sigma']==r['sigma'] and s['mu']==t['mu']==341
    assert R.raw_normalize(s['alpha'])==R.frozen(r['source_alpha']) and R.raw_normalize(t['alpha'])==R.frozen(r['destination_alpha'])
    assert R.core_view(s['b'])==R.frozen(B['trees'][r['source_B']]) and R.core_view(t['b'])==R.frozen(B['trees'][r['destination_B']])
    actualA=R.tree(w['A_source']);actualB=R.tree(w['B_source'])
    def inorder(n):return [] if n is None else inorder(n[1])+[n[0]]+inorder(n[2])
    keys=inorder(actualA);assert len(keys)==len(set(keys))==14 and {16*i for i in range(9)}<=set(keys)
    sig=[0]*10
    for key in keys:
        if key not in {16*i for i in range(9)}:sig[key//16+1]+=1
    assert sig==r['sigma'];wit=L['wit'];seen=set();visible={}
    def prefix(i):
        assert 0<=i<127 and i not in seen and val(wit.p[i]);seen.add(i);key=keys[val(wit.rank[i])];visible[i]=key;iss=val(wit.isS[i]);assert iss==(key in {16*j for j in range(9)})
        if iss:assert key==16*val(wit.sidx[i])
        children=[]
        for kk,cc in ((wit.kleft,wit.cleft),(wit.kright,wit.cright)):
            kind,ref=val(kk[i]),val(cc[i]);assert kind in (0,1,2)
            if kind==0:assert ref<127;children.append(prefix(ref))
            else:children.append(None)
        return (key,*children)
    pref=prefix(0);assert seen=={i for i in range(127) if val(wit.p[i])};assert R.observations(pref,visible[0])==R.raw_normalize(s['alpha'])
    assert val(wit.nev)==1 and val(wit.evK[0]);target=visible[val(wit.evT[0])];assert target==16*r['option'][1]
    ad=R.depth(pref,target);assert ad==val(wit.evd[0]);after=R.splay(pref,target);assert R.observations(after,visible[0])==R.raw_normalize(t['alpha'])
    bd=R.depth(actualB,target);bafter=R.splay(actualB,target)
    def physical_B(b):
        used=set()
        def visit(i):
            assert i in range(19) and i not in used;used.add(i);ch=[]
            for kf,rf in (('kl','rl'),('kr','rr')):
                kind,ref=b[kf][i],b[rf][i];ch.append(visit(ref) if kind==0 and ref<19 else None)
            return (16*i if i<9 else 16*(i-9)-8,*ch)
        return visit(b['root'])
    assert physical_B(s['b'])==actualB and physical_B(t['b'])==bafter
    H=(ad+1)//2;q=bd//2;weight=2*H-q;assert (H,q,weight)==(w['H'],w['q'],w['weight']) and H==val(L['H']) and q==val(L['bt'].q) and bd==val(L['bt'].bd[0]) and weight==val(L['w'])
    assert (ep['source_debt'],ep['destination_debt'])==(2,0) and weight+ep['destination_debt']-ep['source_debt']==-1
    chi=lambda b:b['kr'][8]==0 and b['rr'][8]==19
    assert chi(s['b'])==chi(t['b'])
    result={'status':'INDEPENDENT_ORIGINAL_LOW_THRESHOLD_COUNTEREXAMPLE_VERIFIED','fresh_namespace':tag,'namespace_rename_bijective':True,'factory_called':False,'original_root':True,'all_variable_widths_valid':True,'all147_source_and_destination_coordinates_match':True,'mu':s['mu'],'sigma':s['sigma'],'source_B':r['source_B'],'destination_B':r['destination_B'],'target':target//16,'A_depth':ad,'B_depth':bd,'H':H,'q':q,'weight':weight,'source_debt':2,'destination_debt':0,'candidate_residual':-1,'candidate_full_W_residual':-1,'old_certified_residual':ep['old_certified_residual'],'independent_A_and_B_parent_map_replays':True,'chi8':chi(s['b']),'full_endpoints_close':flat(s)==flat(t),'original_negative_cycle_certified':False,'M3_status':'OPEN','DAG_nodes':len(dag.nodes),'variables':len(dag.vars),'CPU_seconds':time.process_time()-start,'CPU_cap':CAP}
    assert result['CPU_seconds']<CAP;write(BASE/'independent_original_verification.json',result);print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error={'type':type(e).__name__,'message':str(e)};raise
    finally:write(BASE/'verify_witness_exit.json',{'whole_process_CPU_seconds':time.process_time(),'CPU_cap':CAP,'error':error})
