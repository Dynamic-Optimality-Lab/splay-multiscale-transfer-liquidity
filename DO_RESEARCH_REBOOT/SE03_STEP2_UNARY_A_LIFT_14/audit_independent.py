"""Independent seven-node completeness and opposite-kernel unary replay."""
import functools,hashlib,importlib.util,json,time,types
from pathlib import Path
import unary_grammar as G
B=Path(__file__).resolve().parent;ROOT=B.parent.parent;OLD=B.parent/'SE03_STEP2_MULTICORE_FUNDING_CLOSURE_13'
s=importlib.util.spec_from_file_location('immutable_unary14',ROOT/'python/independent/splay.py')
I=importlib.util.module_from_spec(s);s.loader.exec_module(I)
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def itree(t):return ('leaf',t) if isinstance(t,str) else I.node(t[0],itree(t[1]),itree(t[2]))
def plain(t):return t[1] if t[0]=='leaf' else (t[1],plain(t[2]),plain(t[3]))
def path(t,x):
    u=itree(t);p=''
    while u[0]!='leaf' and u[1]!=x:
        c='L' if x<u[1] else 'R';p+=c;u=u[2 if c=='L' else 3]
    assert u[0]!='leaf';return p
def trace(t,x):
    u=itree(t);assert I.lookup(u,x)[0];v,e=I.trace(u,x);return plain(v),path(t,x),e
def core(t,M):
    def go(u):
        if u[0]=='leaf':return None
        l,r=go(u[2]),go(u[3]);return (u[1],l,r) if u[1] in M or l is not None or r is not None else None
    return go(itree(t))
@functools.lru_cache(None)
def shapes(keys):
    if not keys:return (None,)
    return tuple((k,l,r) for i,k in enumerate(keys) for l in shapes(keys[:i]) for r in shapes(keys[i+1:]))
def main():
    g=json.loads((B/'unary_grammar.json').read_text());aa=list(map(G.freeze,g['states']));mm=set(range(1000,6001,1000));derived=set(shapes(tuple(sorted(mm))))
    for gap in range(7):
        u=1000*gap+500
        for t in shapes(tuple(sorted(mm|{u}))):
            if t[0] not in mm:continue
            def locate(v):
                if v is None:return None
                if v[0]==u:return v
                return locate(v[1]) or locate(v[2])
            v=locate(t)
            if (v[1] is None)!=(v[2] is None):derived.add(t)
    assert set(aa)==derived and len(derived)==1452
    base=json.loads((OLD/'cheap_A_comparison.json').read_text())['reports'][0]
    generated=G.generate(base['A_trees'],types.SimpleNamespace(path=path,trace=trace,core=core))
    assert generated['states']==aa and generated['H1']==list(map(tuple,g['H1'])) and generated['H2']==list(map(tuple,g['H2']))
    nB=len(base['BF_trees']);old={(a,b):d for (a,b),d in zip(base['states'],base['debt'])}
    byA={}
    for H,name in ((1,'H1'),(2,'H2')):
        for a,x,b in generated[name]:byA.setdefault((a,x),[]).append((b,H))
    counts={1:0,2:0}
    for s,t,key,Q in json.loads((OLD/'bf9_comparison.json').read_text())['edges']:
        if s>=nB:continue
        x=base['BF_marks'].index(key)+1
        for a,T in enumerate(aa):
            if T[0]//1000!=base['BF_marks'].index(base['BF_trees'][s][0])+1:continue
            ds=old[generated['contract_ids'][a],s]
            for b,H in byA.get((a,x),()):
                dt=old[generated['contract_ids'][b],t];assert 2*H-Q+dt-ds>=0;counts[H]+=1
    assert counts=={1:437068,2:1225153}
    out('independent_unary_audit.json',{'status':'PASS_UNIVERSAL_UNARY_ZERO_CORRECTION_SOURCE_CERTIFICATE',
        'boundary_cores_independently_enumerated':1452,'H1_syntax':len(generated['H1']),'H2_syntax':len(generated['H2']),
        'LOW_rows':counts,'correction':0,'old_A6_debt_unchanged':True,'range':[0,2],
        'HIGH':'H>=3,Q<=4 -> raw>=2, range-safe without helper population bound',
        'universal_lifting':'complete free-gap LOW syntax and endpoint-core classification, not finite private populations',
        'trust':'same agent, distinct rotation kernel/core traversal/state enumeration; not formal/external review',
        'source_engine_calls':G.calls,'grammar_sha256':hashlib.sha256((B/'unary_grammar.json').read_bytes()).hexdigest()})
    print(json.dumps({'status':'PASS_ZERO_CORRECTION_UNARY_LIFT','states':1452,'LOW_rows':counts,'calls':G.calls}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_independent_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':G.calls})
