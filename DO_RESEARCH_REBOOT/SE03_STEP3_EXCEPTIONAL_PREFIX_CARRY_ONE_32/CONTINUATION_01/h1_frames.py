"""Complete H1 active-frame closure retaining BOTH 7 and9, no H2 search."""
import json,time,importlib.util,collections
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent.parent
def run(backend,phase,cap,qcap):
    start=time.process_time();queries=traces=0;error=None;halt=None
    def load(name,p):
        s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
    F=load('h1frame_'+phase,P/'SE03_STEP2_UNARY_A_LIFT_14/branch_frames2.py');F.M=set(range(1000,7001,1000))
    def tick():
        nonlocal queries
        if queries>=qcap or time.process_time()-start>cap-2:raise TimeoutError('QUERY_OR_CPU_RESERVE')
        queries+=1
    op=F.p.path
    def path(t,x):tick();return op(t,x)
    trace=F.p.trace
    if backend=='independent':
        I=load('h1mutable_'+phase,P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_independent2.py');I.tick=tick
        def path(t,x):
            tick();s=''
            while isinstance(t,tuple) and t[0]!=x:
                c='L' if x<t[0] else 'R';s+=c;t=t[1 if c=='L' else 2]
            assert isinstance(t,tuple);return s
        def trace(t,x):
            gaps=[]
            def leaves(v):
                if not isinstance(v,tuple):gaps.append(v)
                else:leaves(v[1]);leaves(v[2])
            leaves(t);it=iter(gaps);a=I.Tree(t);pa,ev=a.access(x)
            def dump(n):return next(it) if n is None else (n.key,dump(n.left),dump(n.right))
            return dump(a.root),pa,ev
    F.p.path=path
    def bound(t,p):
        lo,hi=0,8000
        for c in p:
            if c=='L':hi=t[0];t=t[1]
            else:lo=t[0];t=t[2]
        return lo,hi
    F.bound=bound
    states=tuple(t for t in F.family(1,7) if t[0] in F.M);ids={t:i for i,t in enumerate(states)}
    # Distinct quotient projection for independent kernel.
    def reduce(t):
        if not isinstance(t,tuple):return None
        l,r=reduce(t[1]),reduce(t[2])
        if t[0] in F.M:return (t[0],l,r)
        if l is None:return r
        if r is None:return l
        return (500+1000*sum(x<t[0] for x in F.M),l,r)
    initial=[]
    for small in [(1500,(1000,None,None),(2000,None,None)),(1000,None,(2000,None,None)),(2000,(1000,None,None),None)]:
        initial.append(ids[(6000,(4000,(3000,small,None),(5000,None,None)),(7000,None,None))])
    reached=set(initial);todo=collections.deque(initial);done=[];rel=set();witness={}
    try:
        while todo:
            a=todo.popleft();T=F.material(states[a]);g=T[0]
            for x in sorted(F.M-{g}):
                for TT,xx in F.decorations(T,x,2):
                    if not 1<=len(path(TT,xx))<=2:continue
                    dest,_,ev=trace(TT,xx);traces+=1;assert len(ev)==1
                    b=ids[reduce(dest)];rel.add((a,x//1000,b));witness.setdefault((a,x//1000,b),{'source':TT,'access':xx})
                    if x!=4000 and b not in reached:reached.add(b);todo.append(b)
            done.append(a)
    except TimeoutError as e:halt=str(e)
    except BaseException as e:error=repr(e);raise
    finally:
        result={'status':'COMPLETE_H1_CLOSURE' if not halt and not error else 'PARTIAL','backend':backend,'states':states,'initial':initial,
                'H1':sorted(rel),'completed_A_states':done,'reached_A_states':sorted(reached),'halt':halt,'queries':queries,'traces':traces,
                'witnesses':[dict(a=k[0],x=k[1],b=k[2],**v) for k,v in sorted(witness.items())]}
        with (B/(phase+'_h1_relation.json')).open('x') as f:json.dump(result,f,indent=2)
        with (B/('audit_'+phase+'_exit.json')).open('x') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':traces},f)
    print(json.dumps({k:result[k] for k in ('status','queries','traces','halt')}))
