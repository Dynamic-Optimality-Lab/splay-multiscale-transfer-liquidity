"""Independent branch-quotient state enumeration and immutable LOW kernels."""
import functools,importlib.util,itertools,json,time,types
from pathlib import Path
import branch_frames2 as G
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
s=importlib.util.spec_from_file_location('immutable_branch14',ROOT/'python/independent/splay.py')
I=importlib.util.module_from_spec(s);s.loader.exec_module(I)
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def itree(t):return ('leaf',t) if isinstance(t,str) else I.node(t[0],itree(t[1]),itree(t[2]))
def plain(t):return t[1] if t[0]=='leaf' else (t[1],plain(t[2]),plain(t[3]))
def path_keys(t,x):
    u=itree(t);letters='';keys=[]
    while u[0]!='leaf':
        keys.append(u[1])
        if u[1]==x:return letters,keys
        c='L' if x<u[1] else 'R';letters+=c;u=u[2 if c=='L' else 3]
    raise AssertionError('absent source key')
def trace(t,x):
    path,kk=path_keys(t,x);dest,events=I.trace(itree(t),x);pe=[];j=len(path);i=0
    while j>=2:
        case=path[j-2:j];assert events[i][0]==case
        pe.append({'case':case,'G':kk[j-2],'P':kk[j-1],'target':x,'kind':'DOUBLE'});j-=2;i+=1
    if j:
        assert events[i][0]=='ZIG';pe.append({'case':path[0],'P':kk[0],'target':x,'kind':'ZIG'});i+=1
    assert i==len(events)
    return plain(dest),path,pe
def core(t,M):
    def go(u):
        if u[0]=='leaf':return None
        l,r=go(u[2]),go(u[3]);return (u[1],l,r) if u[1] in M or l is not None or r is not None else None
    return go(itree(t))
@functools.lru_cache(None)
def alltrees(kk):
    if not kk:return (None,)
    return tuple((x,l,r) for j,x in enumerate(kk) for l in alltrees(kk[:j]) for r in alltrees(kk[j+1:]))
def valid(t,M):
    if t is None:return True
    if t[0] not in M and (t[1] is None or t[2] is None):return False
    return valid(t[1],M) and valid(t[2],M)
def freeze(v):return tuple(map(freeze,v)) if isinstance(v,list) else v
def main():
    M=set(range(1000,6001,1000));derived=set()
    for n in range(5):
        for gaps in itertools.combinations(range(1,6),n):
            kk=tuple(sorted(M|{1000*g+500 for g in gaps}))
            derived.update(t for t in alltrees(kk) if t[0] in M and valid(t,M))
    primary=json.loads((B/'branch_grammar2.json').read_text());assert set(map(freeze,primary['states']))==derived and len(derived)==974
    adapter=types.SimpleNamespace(path=lambda t,x:path_keys(t,x)[0],trace=trace,core=core)
    G.p=adapter;result=G.generate(adapter)
    assert result['states']==tuple(map(freeze,primary['states']))
    assert result['H1']==list(map(tuple,primary['H1'])) and result['H2']==list(map(tuple,primary['H2']))
    assert result['first_frame_contexts']==primary['first_frame_contexts']
    out('branch_independent_audit2.json',{'status':'PASS_COMPLETE_REVISED_ACTIVE_FRAME_RELATION',
        'branch_cores_independently_derived':974,'H1_relations':len(result['H1']),'H2_relations':len(result['H2']),
        'full_private_child_of_old_unary_parent_case':True,
        'uniform_scope':'all actual A boundary trees through branch quotient; arbitrary unary/private populations via operand erasure and lazy exposure',
        'trust':'same agent, independent enumeration/primitive rotations/marked-core traversal; shared case syntax, no formal kernel',
        'source_engine_calls':G.calls})
    print(json.dumps({'status':'PASS_GENERAL_BRANCH_FRAME_AUDIT','states':974,'H1':len(result['H1']),'H2':len(result['H2']),'calls':G.calls}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_branch_independent2_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':G.calls})
