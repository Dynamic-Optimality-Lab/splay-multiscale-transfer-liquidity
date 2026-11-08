"""Construct ONE original witness with a matched namespace; no source edits."""
import json,sys,time,hashlib,importlib.util
from pathlib import Path
BASE=Path(__file__).resolve().parent;CAP=min(300,float(sys.argv[1]))
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def module(name,p):
    s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main():
    start=time.process_time();assert read(BASE/'binding_audit.json')['status']=='EXACT_OLD_ADAPTER_BINDING_MISMATCH_CONFIRMED'
    r=read(BASE.parent/'M3_UNIFORM02/case_000/obstruction.json');ind=read(BASE.parent/'M3_UNIFORM02/case_000/obstruction_audit.json');assert ind['status']=='INDEPENDENT_PROMOTION_ENDPOINT_AUDIT_PASS'
    helper=module('rowaudit_witness_helpers',BASE.parent/'M3_POP5_RISK01/source_audit_batch.py');IN=helper.IN;S=helper.S;A=helper.A;R=helper.D.R
    B=read(BASE.parent/'M3_UNITPAIR01/B_bank.json');sig=r['sigma'];H,x,aa,g,fi,code=r['option'];assert (H,x,g,code)==(1,4,None,'10aa42aa6aa')
    expanded=helper.color_and_expand(code,sig,None,False,0);assert expanded is not None
    AA,cuts,assigned=expanded;z=S.LEAF
    def scale(t):return z if t is None else S.node(16*t[0],scale(t[1]),scale(t[2]))
    BB=scale(B['trees'][r['source_B']])
    for gap,n in enumerate(sig):
        if n:BB=IN.V.insert(BB,16*gap-8)
    now=AA;targets=[]
    for path in r['family']['word']:
        node=now
        for side in path:node=node[2+side]
        targets.append(node[1]);now=S.trace(now,node[1])[0]
    assert targets==[64]
    dag=IN.DAG();L=IN.build_slow(dag,'MXL');assert len(dag.nodes)<4000000 and all(n.startswith('MXL') for n in dag.vars)
    fixture=helper.proposals(IN)
    _,_,raw=fixture.low(dag,L,AA,BB,cuts,[['K',k] for k in targets],'weight_plus_one_original_row_audit',341)
    env=raw['environment'];assert set(env)==set(dag.vars)
    assert env['MXLw_p0'] and env['MXLw_nev']==1 and env['MXL_H']==1 and env['MXLbt_q']==1 and env['MXL_w']==1
    for name,n in dag.vars.items():
        nd=dag.nodes[n];v=env[name]
        if nd[1]=='bool':assert isinstance(v,(bool,int)) and v in (False,True)
        else:
            w,sg=nd[3][2:4];assert -(1<<(w-1))<=v<(1<<(w-1)) if sg else 0<=v<(1<<w)
    root=bool(dag.ev_ground(L['root'],env));write(BASE/'attempt.json',{'original_root':root,'environment':env,'raw_proposal':raw,'A_source':IN.V.serial(AA),'B_source':IN.V.serial(BB),'cuts':cuts,'tag':'MXL'})
    if not root:
        write(BASE/'source_result.json',{'status':'UNKNOWN_ONE_CORRECTLY_BOUND_COMPLETION_REJECTED','original_root':False,'unrealizability_proved':False,'CPU_seconds':time.process_time()-start,'CPU_cap':CAP});return
    s=A.ordinary(dag,env,L['s']);t=A.ordinary(dag,env,L['t']);assert s==raw['source'] and t==raw['destination'] and len(A.flat(s))==len(A.flat(t))==147
    assert s['mu']==t['mu']==341 and s['mu'].bit_count()==5 and s['sigma']==t['sigma']==sig
    assert R.raw_normalize(s['alpha'])==R.frozen(r['source_alpha']) and R.raw_normalize(t['alpha'])==R.frozen(r['destination_alpha'])
    assert R.core_view(s['b'])==R.frozen(B['trees'][1647]) and R.core_view(t['b'])==R.frozen(B['trees'][2403])
    nv=A.val(dag,env,L['wit'].nev);hh=sum((A.val(dag,env,L['wit'].evd[j])+1)//2 for j in range(nv));q=A.val(dag,env,L['bt'].q);weight=A.val(dag,env,L['w'])
    assert (nv,hh,A.val(dag,env,L['H']),q,weight)==(1,1,1,1,1) and weight==2*hh-q
    assert A.val(dag,env,L['bt'].bT[0])==4 and A.val(dag,env,L['wit'].evK[0])
    ds=ind['source']['D_run'];dt=ind['destination']['D_run'];assert (ds,dt)==(2,0)
    chis=lambda b:b['kr'][8]==0 and b['rr'][8]==19
    assert chis(s['b'])==chis(t['b']);res=weight+dt-ds;assert res==-1
    proof={'status':'SAT_ORIGINAL_LOW_WEIGHT_PLUS_ONE_ROW','original_root':True,'tag':'MXL','source':s,'destination':t,'environment':env,'environment_sha256':hashlib.sha256(json.dumps(env,sort_keys=True).encode()).hexdigest(),'source_B_core_id':1647,'source_A_profile_id':2073,'destination_B_core_id':2403,'destination_A_profile_id':2072,'H':hh,'q':q,'weight':weight,'terminal_target':4,'source_D_run':ds,'destination_D_run':dt,'candidate_J_source':-ds,'candidate_J_destination':-dt,'candidate_residual':res,'same_chi8':True,'chi8':chis(s['b']),'full_O_coordinate_count':147,'full_endpoints_close':A.flat(s)==A.flat(t),'DAG_nodes':len(dag.nodes),'variables':len(dag.vars),'source_predicate_changed':False,'one_original_root_evaluation':True,'original_negative_cycle_certified':False,'A_source':IN.V.serial(AA),'B_source':IN.V.serial(BB),'cuts':cuts,'A_paths':raw['A_paths'],'B_paths':raw['B_paths'],'port_inventory':raw['port_inventory'],'word_codes':raw['word_codes'],'CPU_seconds':time.process_time()-start,'CPU_cap':CAP}
    assert proof['CPU_seconds']<CAP;write(BASE/'witness.json',proof)
    write(BASE/'source_result.json',{k:v for k,v in proof.items() if k not in ('source','destination','environment','A_source','B_source','cuts','A_paths','B_paths','port_inventory')});print(json.dumps({k:v for k,v in proof.items() if k not in ('source','destination','environment','A_source','B_source','cuts','A_paths','B_paths','port_inventory')},indent=2),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error={'type':type(e).__name__,'message':str(e)};raise
    finally:write(BASE/'source_exit.json',{'whole_process_CPU_seconds':time.process_time(),'CPU_cap':CAP,'error':error})
