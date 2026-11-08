"""One pre-registered proper-prefix lift attempt; no substitute obstruction."""
import json,sys,time,hashlib,importlib.util
from pathlib import Path
BASE=Path(__file__).resolve().parent;INDEX=int(sys.argv[1]);CAP=min(300,float(sys.argv[2]));OUT=BASE/f'case_{INDEX:03d}'
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def module(name,path):
    sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
def main():
    start=time.process_time();r=read(OUT/'obstruction.json');check=read(OUT/'obstruction_audit.json');assert check['status']=='INDEPENDENT_DIRECT_COUNTEREXAMPLE_AUDIT_PASS'
    source=Path(read(OUT/'construction.json')['source_folder']);c=read(source/'relation.json');B=read(BASE.parent/'M3_UNITPAIR01/B_bank.json');op=r['option'];H,x,aa,g,fi,code=op;sig=c['sigma']
    if 'b' in code:
        write(OUT/'original_control.json',{'status':'NO_PROPER_PREFIX_LIFT_FROM_THIS_FIRST_OBSTRUCTION','reason':'Stored first row contains G/slot0. A literal physical-node replacement is not a valid lift. No alternate row was searched.','original_counterexample_to_J1':False,'original_negative_cycle_certified':False,'CPU_seconds':time.process_time()-start,'CPU_cap':CAP});return
    helper=module('uniform_registered_fixture_helpers',BASE.parent/'M3_POP5_RISK01/source_audit_batch.py');IN=helper.IN;A=helper.A;S=helper.S
    expanded=helper.color_and_expand(code,sig,r['family']['word'][0] if H==2 else None,False,g if H==2 else 0)
    if expanded is None:
        write(OUT/'original_control.json',{'status':'NO_PROPER_PREFIX_LIFT_FROM_THIS_FIRST_OBSTRUCTION','reason':'No exact population-preserving expansion from the first stored code. No replacement row was searched.','original_counterexample_to_J1':False,'original_negative_cycle_certified':False,'CPU_seconds':time.process_time()-start,'CPU_cap':CAP});return
    AA,cuts,assigned=expanded;z=S.LEAF
    def scale(t):return z if t is None else S.node(16*t[0],scale(t[1]),scale(t[2]))
    BB=scale(B['trees'][r['source_B']])
    for gap,n in enumerate(sig):
        if n:BB=IN.V.insert(BB,16*gap-8)
    tree=AA;targets=[]
    for path in r['family']['word']:
        node=tree
        for side in path:node=node[2+side]
        targets.append(node[1]);tree=S.trace(tree,node[1])[0]
    marks={x};marks.update(k for k in range(9) if len(marks)<5);mu=sum(1<<k for k in marks)
    dag=IN.DAG();L=IN.build_slow(dag,'UNIFL');assert len(dag.nodes)<4000000
    fixture=helper.proposals(helper.OUT if sig[9] else IN)
    _,_,raw=fixture.low(dag,L,AA,BB,cuts,[['K',key] for key in targets],'uniform_one_step_first_obstruction',mu)
    env=raw['environment'];assert set(dag.vars)<=set(env)
    for name,n in dag.vars.items():
        nd=dag.nodes[n];v=env[name]
        if nd[1]=='bool':assert v in (False,True)
        else:
            width,signed=nd[3][2:4];assert (-(1<<(width-1))<=v<(1<<(width-1))) if signed else 0<=v<(1<<width)
    assert dag.ev_ground(L['root'],env),'First expansion is not an accepted ORIGINAL root'
    s=A.ordinary(dag,env,L['s']);t=A.ordinary(dag,env,L['t']);assert s==raw['source'] and t==raw['destination'] and len(A.flat(s))==len(A.flat(t))==147
    R=helper.D.R
    assert R.raw_normalize(s['alpha'])==R.frozen(r['source_alpha']) and R.raw_normalize(t['alpha'])==R.frozen(r['destination_alpha'])
    assert R.core_view(s['b'])==R.frozen(B['trees'][r['source_B']]) and R.core_view(t['b'])==R.frozen(B['trees'][r['destination_B']])
    nev=A.val(dag,env,L['wit'].nev);hh=sum((A.val(dag,env,L['wit'].evd[i])+1)//2 for i in range(nev));q=A.val(dag,env,L['bt'].q);weight=2*hh-q
    assert hh==H and weight==r['weight'] and q==raw['q']
    ds=check['source']['D1'];dt=check['destination']['D1'];res=weight+dt-ds;assert res==r['candidate_residual']<0
    report={'status':'ORIGINAL_LOW_COUNTEREXAMPLE_TO_ONE_STEP_J1','original_root':True,'source':s,'destination':t,'environment':env,'environment_sha256':hashlib.sha256(json.dumps(env,sort_keys=True).encode()).hexdigest(),'mu':mu,'sigma':sig,'H':hh,'q':q,'weight':weight,'source_D1':ds,'destination_D1':dt,'candidate_residual':res,'D1_endpoint_values_independently_audited':True,'new_original_root_evaluations':1,'full_O_coordinate_count':147,'source_and_destination_close':A.flat(s)==A.flat(t),'DAG_nodes':len(dag.nodes),'CPU_seconds':time.process_time()-start,'CPU_cap':CAP,'original_negative_cycle_certified':False,'refutes_M3':False,'old_source_controls_repeated':0}
    assert report['CPU_seconds']<CAP
    write(OUT/'original_control.json',report);print(json.dumps({k:v for k,v in report.items() if k not in ('source','destination','environment')},indent=2),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error={'type':type(e).__name__,'message':str(e)};raise
    finally:write(OUT/'original_lift_exit.json',{'whole_process_CPU_seconds':time.process_time(),'CPU_cap':CAP,'error':error})
