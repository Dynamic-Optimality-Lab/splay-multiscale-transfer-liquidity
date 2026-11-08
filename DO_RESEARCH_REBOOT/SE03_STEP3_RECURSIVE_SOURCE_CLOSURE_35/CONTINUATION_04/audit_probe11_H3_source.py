"""Independent physical replay of newly exposed three-event source paths."""
import hashlib,importlib.util,json,pickle,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();V=None
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tup(t):return (t[0],tup(t[1]),tup(t[2])) if isinstance(t,list) else t
def value(nodes,root,pos,n):
    width=1<<(n-1).bit_length()
    while root>=0:
        l,r=nodes[root];half=width//2
        if pos<half:root=l
        else:root=r;pos-=half
        width=half
    return -root-1
def main():
    global V
    sp=importlib.util.spec_from_file_location('native11_H3_distinct_mutable',B/'audit_verify79.py');V=importlib.util.module_from_spec(sp);sp.loader.exec_module(V)
    V.CAP=CAP;V.START=START;V.QCAP=QCAP;V.CALLS=0
    with (F/'probe11_source_actions.pkl').open('rb') as f:native=pickle.load(f)
    with (F/'global_probe11_LOW_model.pkl').open('rb') as f:m=pickle.load(f)
    with (F/'global_probe11_DAG_07.pkl').open('rb') as f:z=pickle.load(f)
    producer=json.loads((F/'probe11_H3_source_resolution_07.json').read_text());controls=[];primitive_cache={};reused=0
    for wid,w in enumerate(producer['source_constraints_to_add']):
        A=V.Mutable(native['trees'][w['A_source']]);BF=V.Mutable(native['trees'][w['B_source']]);H=Q=0;rows=[]
        for t,op in enumerate(w['A_word'],1):
            ab,bb=A.snapshot(),BF.snapshot();a,_,events=A.splay(op['key'],True);q=0
            if op['kind']=='K':assert bb[0]!=op['key'];_,q,_=BF.splay(op['key'],False)
            else:assert op['kind']=='D'
            H+=a;Q+=q;rows.append({'local_t':t,'kind':op['kind'],'key':op['key'],'a':a,'qF':q,'A_before':ab,'BF_before':bb,
              'A_after':A.snapshot(),'BF_after':BF.snapshot(),'A_events':events})
        assert H==3 and Q==w['Q'] and tup(A.snapshot())==native['trees'][w['A_target']] and tup(BF.snapshot())==native['trees'][w['B_target']]
        g=w['g'];x=w['KEEP'];s=int(m['local'][w['A_source']]);t=int(m['local'][w['A_target']])
        ds=value(z['nodes'],z['columns'][w['B_source']],s,len(m['classes'][g-1]));dt=value(z['nodes'],z['columns'][w['B_target']],t,len(m['classes'][x-1]))
        assert (ds,dt)==(w['D_source'],w['D_target']) and 6-Q+dt-ds==w['signed_margin']==-1
        controls.append({'id':wid,'reference':w,'H':H,'Q':Q,'signed_margin':6-Q+dt-ds,'rows':rows,
          'separate_closed_embedding':'ordinary all-key B source realization; not one negative source cycle'})
    out={'status':'PASS_LITERAL_THREE_EVENT_SOURCE_DEFECTS','source_constraints':len(controls),'controls':controls,
      'source_queries':V.CALLS,'source_engine_calls':V.CALLS,'full_source_cycle_counterexample':False,'JR35':'OPEN',
      'input_sha256':{p:sha(F/p) for p in ('probe11_H3_source_resolution_07.json','probe11_source_actions.pkl','global_probe11_DAG_07.pkl','global_probe11_LOW_model.pkl')}}
    with (F/'independent_probe11_H3_source_07.json').open('x',encoding='utf8') as f:json.dump(out,f,indent=2)
    print(json.dumps({k:v for k,v in out.items() if k not in ('controls','input_sha256')}),flush=True);assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_verify122_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,
          'source_queries':0 if V is None else V.CALLS,'source_engine_calls':0 if V is None else V.CALLS},f)
