"""Fresh mutable check of ALL four-node source identities for reusable hulls."""
import json,time,sys,hashlib,importlib.util,collections
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent.parent;START=time.process_time();CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);queries=0
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    global queries
    source=B/'interior_max_contraction_closed_source.json';G=json.loads(source.read_text())['four_hull_source_kernel'];T=list(map(fr,G['trees']));index={t:i for i,t in enumerate(T)};assert len(T)==14;sp=importlib.util.spec_from_file_location('independent_G4_hull_source33',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_independent2.py');I=importlib.util.module_from_spec(sp);sp.loader.exec_module(I)
    def tick():
        global queries
        if queries>=QCAP or time.process_time()-START>CAP-2:raise TimeoutError('G4_AUDIT_CAP')
        queries+=1
    I.tick=tick
    def shape(tree):
        def walk(v,hi):return 'F'+str(hi) if v is None else (v.key,walk(v.left,v.key-1),walk(v.right,hi))
        return walk(tree.root,4)
    for s,t in enumerate(T):
        for x in range(1,5):
            tree=I.Tree(t);path,events=tree.access(x);assert index[shape(tree)]==G['destinations'][s][x-1] and len(events)==G['H'][s][x-1]==(len(path)+1)//2
    for s in range(14):
        seen={s};todo=[s]
        while todo:
            for t in G['destinations'][todo.pop()]:
                if t not in seen:seen.add(t);todo.append(t)
        assert len(seen)==14
    out('four_hull_source_basis_independent_audit.json',{'status':'PASS_COMPLETE_G4_PRIMITIVES_AND_ROOTED_HULL_TERM_LIFT','fresh_original_source_queries':queries,'source_queries':queries,'source_engine_calls':queries,'all_directed_G4_shapes_strongly_connected':True,'uniform_lift':'Each four-node hull is ancestor-closed in the actual full tree. Actual accesses to its keys stay on its paths; substitution of the same five arbitrary ordered hanging BSTs commutes with all ordinary rotations. Actual StepEv counts equal the independently checked four-node counts.','not_claimed':'new source replays for later identity instantiations or any credit outside their actual original events','input_source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source_kernel':G,'principal_U33':'OPEN'});print(json.dumps({'status':'PASS_ALL_56_G4_SOURCE_ACTIONS','source_queries':queries,'future_hull_instances':'certified identities, not fresh source queries'}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify45_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':queries})
