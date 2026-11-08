"""One original LOW completion of the first new predicate counterexample."""
import json,sys,time,hashlib,importlib.util
from pathlib import Path
BASE=Path(__file__).resolve().parent;CAP=min(300,float(sys.argv[1]))
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def module(name,p):
    sp=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
def main():
    start=time.process_time();r=read(BASE/'case_000/obstruction.json');ep=read(BASE/'endpoint_audit.json');assert ep['status']=='INDEPENDENT_DIRECT_THRESHOLD_ENDPOINT_OBSTRUCTION_VERIFIED'
    helper=module('pred02_source_helpers',BASE.parent/'M3_POP5_RISK01/source_audit_batch.py');IN=helper.IN;S=helper.S;A=helper.A;R=helper.D.R;B=read(BASE.parent/'M3_UNITPAIR01/B_bank.json');sig=r['sigma'];H,x,aa,g,fi,code=r['option'];assert H==1 and g is None
    expanded=helper.color_and_expand(code,sig,None,False,0)
    if expanded is None:
        write(BASE/'source_result.json',{'status':'UNKNOWN_FIRST_PROTECTED_PREFIX_COMPLETION_UNAVAILABLE','original_realizability_proved':False,'CPU_seconds':time.process_time()-start,'CPU_cap':CAP});return
    AA,cuts,assigned=expanded;z=S.LEAF
    def scale(t):return z if t is None else S.node(16*t[0],scale(t[1]),scale(t[2]))
    BB=scale(B['trees'][r['source_B']])
    for gap,n in enumerate(sig):
        if n:BB=IN.V.insert(BB,16*gap-8)
    dag=IN.DAG();L=IN.build_slow(dag,'MXL');assert len(dag.nodes)<4000000
    fixture=helper.proposals(IN);mu=341;assert (mu>>x)&1
    _,_,raw=fixture.low(dag,L,AA,BB,cuts,[['K',16*x]],'pred02_first_plus_one_counterexample',mu)
    env=raw['environment'];assert set(env)==set(dag.vars) and all(n.startswith('MXL') for n in env)
    for name,n in dag.vars.items():
        nd=dag.nodes[n];v=env[name]
        if nd[1]=='bool':assert v in (False,True)
        else:
            width,signed=nd[3][2:4];assert -(1<<(width-1))<=v<(1<<(width-1)) if signed else 0<=v<(1<<width)
    root=bool(dag.ev_ground(L['root'],env));write(BASE/'original_attempt.json',{'original_root':root,'environment':env,'raw_proposal':raw,'A_source':IN.V.serial(AA),'B_source':IN.V.serial(BB),'cuts':cuts})
    if not root:
        write(BASE/'source_result.json',{'status':'UNKNOWN_FIRST_CORRECTLY_BOUND_ORIGINAL_COMPLETION_REJECTED','original_root':False,'unrealizability_proved':False,'CPU_seconds':time.process_time()-start,'CPU_cap':CAP});return
    s=A.ordinary(dag,env,L['s']);t=A.ordinary(dag,env,L['t']);assert s==raw['source'] and t==raw['destination'] and len(A.flat(s))==len(A.flat(t))==147
    assert s['mu']==t['mu']==mu and s['sigma']==t['sigma']==sig
    assert R.raw_normalize(s['alpha'])==R.frozen(r['source_alpha']) and R.raw_normalize(t['alpha'])==R.frozen(r['destination_alpha'])
    assert R.core_view(s['b'])==R.frozen(B['trees'][r['source_B']]) and R.core_view(t['b'])==R.frozen(B['trees'][r['destination_B']])
    hh=A.val(dag,env,L['H']);q=A.val(dag,env,L['bt'].q);w=A.val(dag,env,L['w']);assert hh==H and w==r['weight']==2*hh-q and A.val(dag,env,L['wit'].nev)==1 and A.val(dag,env,L['bt'].bT[0])==x
    chi=lambda b:b['kr'][8]==0 and b['rr'][8]==19
    assert chi(s['b'])==chi(t['b']) and w+ep['destination_debt']-ep['source_debt']==-1
    proof={'status':'SAT_ORIGINAL_LOW_THRESHOLD_PREDICATE_COUNTEREXAMPLE','original_root':True,'tag':'MXL','environment':env,'environment_sha256':hashlib.sha256(json.dumps(env,sort_keys=True).encode()).hexdigest(),'source':s,'destination':t,'source_B':r['source_B'],'source_A':r['source_A'],'destination_B':r['destination_B'],'destination_A':r['destination_A'],'terminal_target':x,'H':hh,'q':q,'weight':w,'source_debt':ep['source_debt'],'destination_debt':ep['destination_debt'],'candidate_residual':-1,'chi8':chi(s['b']),'full_endpoints_close':A.flat(s)==A.flat(t),'A_source':IN.V.serial(AA),'B_source':IN.V.serial(BB),'cuts':cuts,'A_paths':raw['A_paths'],'B_paths':raw['B_paths'],'port_inventory':raw['port_inventory'],'DAG_nodes':len(dag.nodes),'variables':len(dag.vars),'source_predicate_modified':False,'original_negative_cycle_certified':False,'CPU_seconds':time.process_time()-start,'CPU_cap':CAP}
    assert proof['CPU_seconds']<CAP;write(BASE/'witness.json',proof);write(BASE/'source_result.json',{k:v for k,v in proof.items() if k not in ('environment','source','destination','A_source','B_source','cuts','A_paths','B_paths','port_inventory')});print(json.dumps({k:v for k,v in proof.items() if k not in ('environment','source','destination','A_source','B_source','cuts','A_paths','B_paths','port_inventory')},indent=2),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error={'type':type(e).__name__,'message':str(e)};raise
    finally:write(BASE/'construct_witness_exit.json',{'whole_process_CPU_seconds':time.process_time(),'CPU_cap':CAP,'error':error})
