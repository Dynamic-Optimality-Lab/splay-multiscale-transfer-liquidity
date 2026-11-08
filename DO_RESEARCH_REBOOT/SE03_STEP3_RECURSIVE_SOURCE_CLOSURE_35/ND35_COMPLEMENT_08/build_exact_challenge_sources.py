"""New deterministic source challenges for terminal-neutral and projection proofs."""
import hashlib,importlib.util,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;B=F.parent.parent/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();V=None
def N(k,l=None,r=None):return (k,l,r)
def vine(keys,right=True):
    t=None
    for k in (keys[::-1] if right else keys):t=N(k,None,t) if right else N(k,t,None)
    return t
def labels(t):
    out=set()
    def go(v):
        if v is None:return frozenset()
        s=go(v[1])|go(v[2])|{v[0]};out.add(s);return s
    go(t);return out
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    global V
    spec=importlib.util.spec_from_file_location('new_TNE_projection_controls',B/'audit_core39.py');V=importlib.util.module_from_spec(spec);spec.loader.exec_module(V)
    V.CAP=CAP;V.START=START;V.QCAP=QCAP;V.CALLS=0
    r=8;initial=vine(list(range(1,r+1)));a=b=initial;word=[('D',x) for x in range(2,r+1)]+[('K',r)]+[('K',x) for x in range(1,r+1)]+[('K',x) for x in range(r-1,0,-1)];rows=[];qtotal=0
    for t,(kind,x) in enumerate(word,1):
        ab,bb=a,b;a,H,_,ae=V.splay(a,x,True)
        if kind=='K':b,_,q,be=V.splay(b,x,True)
        else:q=0;be=[]
        rows.append({'t':t,'kind':kind,'key':x,'A_before':ab,'A_after':a,'BF_before':bb,'BF_after':b,'H':H,'Q':q,'A_events':ae,'BF_events':be});qtotal+=q
    assert a==b==initial and qtotal==r-2 and len(rows)==3*r-1
    primary=rows[r-1];assert primary['key']==r and primary['kind']=='K' and primary['H']==0 and primary['Q']==3
    drops=[]
    for e in primary['BF_events']:
        dd=[]
        for rot in e['rotations']:
            old=labels(rot['before'])-labels(primary['A_after']);new=labels(rot['after'])-labels(primary['A_after']);dd.append(len(old)-len(new))
        drops.append({'pattern':e['pattern'],'rotation_drops':dd})
    assert all(e['rotation_drops']==[0,0] for e in drops[:-1]) and drops[-1]['rotation_drops']==[1]
    T=N(4,None,N(6,None,N(8,N(7),None)));projected=N(4,None,N(6,None,N(7)))
    full,h,q,ev=V.splay(T,7,True);trim=N(7,N(4,None,N(6)),None);small,ph,pq,pev=V.splay(projected,7,True)
    assert full==N(7,N(4,None,N(6)),N(8)) and (h,q)==(2,1) and [e['pattern'] for e in ev]==['RL','R']
    assert small==N(7,N(6,N(4),None),None) and (ph,pq)==(1,1) and small!=trim
    right=vine([4,6,7,8]);prefix=[];state=right
    for x in (8,6,4):
        before=state;state,h,q,e=V.splay(state,x,True);prefix.append({'key':x,'before':before,'after':state,'H':h,'Q':q,'events':e})
    assert state==T;period=[]
    for x in (7,4,6,7,8,7,6,4,8,6,4):
        before=state;state,h,q,e=V.splay(state,x,True);period.append({'key':x,'before':before,'after':state,'H':h,'Q':q,'events':e})
    assert state==T
    out={'status':'NEW_EXACT_CLOSED_SOURCE_CHALLENGES','vine_family_control':{'r':r,'initial':initial,'word':word,'rows':rows,'Q':qtotal,'primary_B_drops':drops,'primary_neutral_last_demand':[r,3],'TNE_seed':[1,1,0]},
      'projection_control':{'initial':T,'projected_initial':projected,'target':7,'full_after':full,'trimmed_full_after':trim,'projected_ordinary_after':small,'full_H':2,'projected_H':1,'reaching_prefix':prefix,'closed_period':period},
      'source_queries':V.CALLS,'source_engine_calls':V.CALLS,'universal_proofs_not_inferred_from_controls':True,'Objective_I':'OPEN',
      'input_sha256':{str(p):sha(p) for p in (F/'SEQUENTIAL_VINE_NEUTRAL_FAMILY.md',F/'INTERVAL_PROJECTION_OBSTRUCTION.md',F/'TERMINAL_NEUTRAL_ELIMINATION.md',F/'build_exact_challenge_sources.py')}}
    with (F/'exact_challenge_sources.json').open('x',encoding='utf8') as f:json.dump(out,f,indent=2)
    print(json.dumps({'status':out['status'],'source_queries':V.CALLS,'vine_Q':qtotal,'primary_neutral_double_count':primary['Q'],'projected_splay_commutes':False}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        calls=0 if V is None else V.CALLS
        with (B/'audit_core79_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':calls,'source_engine_calls':calls},f)
