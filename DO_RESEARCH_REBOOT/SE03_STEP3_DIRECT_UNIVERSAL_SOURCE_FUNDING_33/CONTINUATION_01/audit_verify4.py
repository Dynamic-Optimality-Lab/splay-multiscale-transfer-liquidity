"""Separate pointer-rotation check of the closed unary projection witness."""
import json,time,sys,importlib.util,collections,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent.parent;CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();queries=0
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def main():
    global queries
    z=json.loads((B/'unary_projection_source_countercertificate.json').read_text());sp=importlib.util.spec_from_file_location('independent_unary_projection33',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_independent2.py');I=importlib.util.module_from_spec(sp);sp.loader.exec_module(I)
    def tick():
        global queries
        if queries>=QCAP or time.process_time()-START>CAP-3:raise TimeoutError('INDEPENDENT_RESERVE')
        queries+=1
    I.tick=tick
    def shape(tree,n):
        def go(v,lo,hi):return 'F'+str(hi) if v is None else (v.key,go(v.left,lo,v.key-1),go(v.right,v.key+1,hi))
        return go(tree.root,1,n)
    T=fr(z['initial_diagonal']);A=I.Tree(T);F=I.Tree(T);counts=[0,0];actual=set()
    for r in z['rows']:
        assert (shape(A,10),shape(F,10))==fr(r['before']);x=r['target'];pa,ea=A.access(x);pb='';eb=[]
        if r['mode']=='K':pb,eb=F.access(x)
        assert (shape(A,10),shape(F,10))==fr(r['after']) and pa==r['A_path'] and pb==r['BF_path']
        q=sum(e['kind']=='DOUBLE' for e in eb);assert (len(ea),q)==(r['a'],r['qF']);counts[0]+=len(ea);counts[1]+=q
        if r['genuine_F']:actual.add(x)
    assert shape(A,10)==shape(F,10)==T and actual==set(z['marks']) and counts==[30,2]
    source=fr(z['projected_A_before']);target=fr(z['projected_A_after']);best={source:0};todo=collections.deque([source]);accesses=0
    while todo:
        src=todo.popleft();cost=best[src];tree=I.Tree(src);depth={}
        def walk(v,d):
            if v is None:return
            depth[v.key]=d;walk(v.left,d+1);walk(v.right,d+1)
        walk(tree.root,0)
        for x,d in depth.items():
            step=(d+1)//2
            if step==0 or cost+step>2:continue
            native=I.Tree(src);pa,ev=native.access(x);accesses+=1;dst=shape(native,9);assert len(ev)==step
            if cost+step<best.get(dst,999):best[dst]=cost+step;todo.append(dst)
    assert target not in best
    tree=I.Tree(source);attained=0
    for x in (4,3):pa,ev=tree.access(x);attained+=len(ev)
    assert shape(tree,9)==target and attained==3
    # The symbolic proof only uses the first three/four Scores. The ordered
    # tail and all untouched gap terms are preserved operands. Zero-cost
    # root repetitions cannot evade the two-positive-access classification.
    result={'status':'PASS_CLOSED_SOURCE_AND_UNARY_PROJECTION_COST_GAP','genuine_KEEP_keys':len(actual),'full_B_core':9,'original_critical_A_events':2,'native_minimum_A_events':3,'physical_period_counts':counts,'all_source_rows_replayed':len(z['rows']),'native_bounded_cost_accesses':accesses,'uniform_proof_scope':'n>=5 explicit labels, arbitrary ordered rigid gap substitution, reflection and finite repetition; active anonymous key3','failed_attempt_preserved':'core5 used an incorrect D5 reset; core6 corrects it to D4 and is independently checked here','new_source_queries':queries,'principal_U33':'OPEN','external_or_formal_verification':False,'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('UNARY_PROJECTION_BRIDGE_REFUTATION.md','unary_projection_source_countercertificate.json')}}
    out('unary_projection_independent_audit.json',result);print(json.dumps(result))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify4_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':queries})
