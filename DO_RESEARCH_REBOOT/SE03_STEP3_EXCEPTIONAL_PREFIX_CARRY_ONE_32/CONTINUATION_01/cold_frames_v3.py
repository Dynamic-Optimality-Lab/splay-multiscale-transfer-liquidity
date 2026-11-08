"""Prepared complete cold9 LOW source-frame compiler. DO NOT RUN at Q=0.

Invoked by a capped phase wrapper: run(backend,start,stop,phase,cap,qcap).
All original path/splay invocations are charged; no historical file edited.
The generic active-frame syntax is inherited, while BOTH old7/new9 are
retained until the actual source operation completes. Source and destination
are projected onto DIFFERENT six-mark sets only after exact rotations.
"""
import importlib.util,json,time,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent.parent;ROOT=P.parent
M7=set(range(1000,7001,1000));OLD=M7-{5000};NEW=M7-{4000}
def fr(v):return tuple(fr(x) for x in v) if isinstance(v,list) else v
def run(backend,start,stop,phase,cap,qcap):
    began=time.process_time();queries=traces=0;query_classes={};relations={1:set(),2:set()};witness={};completed=[];depth_excluded=[];halt=None;raw_index=None
    def out(n,v):
        with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
    def charge(kind):
        nonlocal queries
        if queries>=qcap:raise TimeoutError('AUTHORIZED_SOURCE_QUERY_CAP')
        if time.process_time()-began>=cap-2:raise TimeoutError('CPU_RESERVE')
        queries+=1;query_classes[kind]=query_classes.get(kind,0)+1
    sp=importlib.util.spec_from_file_location('cold7_frame_helpers_'+phase,P/'SE03_STEP2_UNARY_A_LIFT_14/branch_frames2.py')
    F=importlib.util.module_from_spec(sp);sp.loader.exec_module(F);F.M=M7
    # Only a local module binding is changed. The frozen source is untouched.
    original_path=F.p.path
    def producer_path(t,x):charge('original_path');return original_path(t,x)
    F.p.path=producer_path
    class Kernel:pass
    K=Kernel()
    if backend=='producer':K.path=producer_path;K.trace=F.p.trace;K.core=F.p.core
    else:
        si=importlib.util.spec_from_file_location('cold7_mutable_'+phase,P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_independent2.py')
        I=importlib.util.module_from_spec(si);si.loader.exec_module(I)
        I.tick=lambda:charge('distinct_original_access')
        def ipath(t,x):
            charge('distinct_original_path');result=''
            while isinstance(t,tuple) and t[0]!=x:
                c='L' if x<t[0] else 'R';result+=c;t=t[1 if c=='L' else 2]
            if not isinstance(t,tuple):raise ValueError('target absent')
            return result
        def itrace(t,x):
            # The inherited witness verifier's dump labels gaps for actual
            # keys1..13. These source frames use order-scaled keys1000..7000.
            # Preserve the input's ordered opaque gap payloads instead of
            # using that13-key display adapter; rotations remain unchanged.
            gaps=[]
            def leaves(v):
                if not isinstance(v,tuple):gaps.append(v)
                else:leaves(v[1]);leaves(v[2])
            leaves(t);it=iter(gaps)
            T=I.Tree(t);path,events=T.access(x)
            def dump(n):return next(it) if n is None else (n.key,dump(n.left),dump(n.right))
            shape=dump(T.root)
            assert next(it,None) is None
            return shape,path,events
        K.path=ipath;K.trace=itrace
        # Helpers' depth predicates must use the DISTINCT path kernel too.
        F.p.path=ipath
    def bound(t,path):
        lo,hi=0,8000
        for c in path:
            if c=='L':hi=t[0];t=t[1]
            else:lo=t[0];t=t[2]
        return lo,hi
    F.bound=bound
    original_find=F.find
    def charged_find(t,x,path=''):
        charge('rigid_hanger_source_lookup');return original_find(t,x,path)
    F.find=charged_find
    def project(t,marks):
        rank={m:1000*(i+1) for i,m in enumerate(sorted(marks))}
        if backend=='producer':
            core=F.p.core(t,marks)
            def norm(v):
                if v is None:return None
                l,r=norm(v[1]),norm(v[2])
                if v[0] in marks:return (rank[v[0]],l,r)
                if l is None:return r
                if r is None:return l
                return (1000*sum(m<v[0] for m in marks)+500,l,r)
            return norm(core)
        def independent(v):
            if not isinstance(v,tuple):return None
            left,right=independent(v[1]),independent(v[2])
            if v[0] in marks:return (rank[v[0]],left,right)
            if left is None or right is None:return left if right is None else right
            return (500+1000*len([m for m in marks if m<v[0]]),left,right)
        return independent(t)
    grammar=json.loads((P/'SE03_STEP2_UNARY_A_LIFT_14/branch_grammar2.json').read_text());ids={fr(t):i for i,t in enumerate(grammar['states'])}
    bases=[t for t in F.family(1,7) if t[0] in M7 and t[0] not in (4000,5000)]
    assert len([t for t in F.family(1,7) if t[0] in M7])==5947
    assert 0<=start<stop<=len(bases)
    def trace(t,x):
        nonlocal traces
        traces+=1;return K.trace(t,x)
    def save(a,H,T,accesses,dest,kind):
        b=ids[project(dest,NEW)];key=(a,b);relations[H].add(key)
        witness.setdefault((H,a,b),{'H':H,'a_old':a,'b_new':b,'source':T,'accesses':accesses,'kind':kind})
    error=None
    try:
        for raw_index in range(start,stop):
            raw=bases[raw_index];T=F.material(raw);a=ids[project(T,OLD)];g=T[0];x=5000
            # Every actual H<=2 macro has at most four rotations, so its
            # terminal key's INITIAL depth is<=4. Quotient pruning can only
            # decrease that depth. This excludes impossible source bases,
            # without a population cutoff or a change to any legal LOW row.
            if len(K.path(T,x))>4:
                completed.append(raw_index);depth_excluded.append(raw_index);continue
            for TT,xx in F.decorations(T,x,4):
                d=len(K.path(TT,xx))
                if 1<=d<=4:
                    dest,_,ev=trace(TT,xx);assert len(ev) in (1,2);save(a,len(ev),TT,[xx],dest,'single_cold_target')
            first={}
            def add(TT,y,kind):
                TT,yy=F.canonical(TT,y)
                if 1<=len(K.path(TT,yy))<=2:first[TT,yy]=kind
            for y in F.vals(T):
                if y==g:continue
                for TT,yy in F.decorations(T,y,2):add(TT,yy,'known_seven_core')
            for path,sub in F.subpaths(T):
                if not 1<=len(path)<=2:continue
                for TT,y in F.insertions(T,path):
                    for TTT,yy in F.decorations(TT,y,2):add(TTT,yy,'old_unary_target')
                    if len(path)==1:
                        U=F.get(TT,path);side='L' if not F.node(U[1]) else 'R';pp=path+side;lo,hi=bound(TT,pp)
                        v=(lo+hi)//2;add(F.put(TT,pp,(v,'a','b')),v,'private_child_old_unary_parent')
            for path,sub in F.leafpaths(T):
                if not 1<=len(path)<=2:continue
                lo,hi=bound(T,path);mid=(lo+hi)//2;q1=lo+(hi-lo)//3;q2=lo+2*(hi-lo)//3
                add(F.put(T,path,(mid,'a','b')),mid,'private_root')
                if len(path)==1:
                    add(F.put(T,path,(q2,(q1,'a','b'),'c')),q1,'private_left_grandchild')
                    add(F.put(T,path,(q1,'a',(q2,'b','c'))),q2,'private_right_grandchild')
            for (TT,y),kind in first.items():
                middle,_,ev=trace(TT,y);assert len(ev)==1
                active={ev[0].get(k) for k in ('G','P','target')};active.discard(None)
                path=K.path(middle,x);d=len(path)
                if not 1<=d<=2:continue
                dest,_,ev2=trace(middle,x);assert len(ev2)==1;save(a,2,TT,[y,x],dest,kind)
                if d!=1:continue
                S=F.get(middle,path)
                if set(F.vals(S))&active or not F.hasmark(S):continue
                original=F.find(TT,S[0]);assert original is not None and F.get(TT,original)==S
                for TTT,u in F.insertions(TT,original):
                    TTT,yy=F.canonical(TTT,y);mid2,_,ev1=trace(TTT,yy);assert len(ev1)==1
                    assert 1<=len(K.path(mid2,x))<=2
                    end,_,ev2=trace(mid2,x);assert len(ev2)==1;save(a,2,TTT,[yy,x],end,'second_rigid_hanger_unary')
            completed.append(raw_index)
    except TimeoutError as ex:halt=str(ex)
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:
        out(phase+'_source_relation.json',{'status':'COMPLETE_BATCH' if halt is None and error is None else 'PARTIAL_BATCH',
            'backend':backend,'requested_range':[start,stop],'completed_source_bases':completed,'incomplete_base':raw_index if halt else None,
            'total_seven_source_bases':len(bases),'depth_excluded_source_bases':depth_excluded,'LOW':{str(h):sorted(relations[h]) for h in (1,2)},
            'witnesses':[witness[k] for k in sorted(witness)],'queries':queries,'query_classes':query_classes,'traces':traces,'halt':halt,
            'source_projection':'seven distinguished A keys, source retires9, destination retires7; actual source rotations unchanged',
            'is_original_source_counterexample':False})
        out('audit_'+phase+'_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':traces,'source_queries':queries})
    print(json.dumps({'status':'COMPLETE_BATCH' if halt is None else 'PARTIAL_BATCH','backend':backend,'range':[start,stop],
        'completed':len(completed),'queries':queries,'halt':halt}),flush=True)
