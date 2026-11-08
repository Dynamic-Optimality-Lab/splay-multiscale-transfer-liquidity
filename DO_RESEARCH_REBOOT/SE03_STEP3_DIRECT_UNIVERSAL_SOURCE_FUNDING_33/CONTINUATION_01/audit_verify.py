"""Distinct complete eight-core checker; producer source engine not imported."""
import json,time,sys,importlib.util,functools,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent.parent;CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();queries=0
def rd(p):return json.loads(p.read_text())
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def out(n,v):
    with (B/n).open('x') as f:json.dump(v,f,indent=2)
def main():
    global queries
    z=rd(B/'eight_core_B_source_relation.json');cert=rd(B/'eight_core_B_law_result.json');assert cert['status']=='B_ONLY_SOURCE_LAW_PROVED'
    T=list(map(fr,z['trees']));D=cert['D'];idx={t:i for i,t in enumerate(T)};assert len(idx)==1430
    # Independent Catalan grammar validation by leaf/node intervals and
    # cardinality, not reading producer transition counts as evidence.
    def valid(t,lo,hi):
        if lo>hi:assert t=='F'+str(hi);return
        k,l,r=t;assert lo<=k<=hi;valid(l,lo,k-1);valid(r,k+1,hi)
    for t in T:valid(t,1,8)
    sp=importlib.util.spec_from_file_location('mutable_core8_verify33',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_independent2.py')
    I=importlib.util.module_from_spec(sp);sp.loader.exec_module(I)
    def tick():
        global queries
        if queries>=QCAP or time.process_time()-START>=CAP-2:raise TimeoutError('INDEPENDENT_CAP')
        queries+=1
    I.tick=tick
    def shape(tree):
        def go(v,lo,hi):return 'F'+str(hi) if v is None else (v.key,go(v.left,lo,v.key-1),go(v.right,v.key+1,hi))
        return go(tree.root,1,8)
    actual=set();minimum=99
    for b,t in enumerate(T):
        for x in range(1,9):
            tree=I.Tree(t);path,events=tree.access(x);dest=idx[shape(tree)];q=sum(e['kind']=='DOUBLE' for e in events)
            row=(b,x,dest,q);actual.add(row);margin=2-q+D[dest]-D[b];assert margin>=0;minimum=min(minimum,margin)
    assert actual==set(map(tuple,z['relation'])) and set(D)=={0,1} and len(D)==1430
    result={'status':'PASS_COMPLETE_EIGHT_CORE_B_ONLY_CERTIFICATE','shapes':1430,'all_source_rows':len(actual),'D_width':1,'minimum_margin':minimum,
        'source_scope':'any original fixed full core8, any marked subset of its labels; source A arbitrary with genuine macro H>=1; arbitrary ordered private gaps',
        'new_source_queries':queries,'external_or_formal_audit':False,
        'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('eight_core_B_source_relation.json','eight_core_B_law_result.json')}}
    out('eight_core_independent_audit.json',result);print(json.dumps(result))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':queries})
