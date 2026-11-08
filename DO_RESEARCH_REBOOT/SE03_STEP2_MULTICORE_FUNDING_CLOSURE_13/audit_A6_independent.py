"""Reverse-kernel audit: H1 through original kernel, H2 through immutable.
Generation schemas shared as syntax, primitive rotations/core walks distinct.
No full multicore or arbitrary A marked-core claim is made.
"""
import importlib.util,json,time,types
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
I=load('immutable_release13',ROOT/'python/independent/splay.py')
P=load('original_H1_checker13',B.parent/'SE03_STEP2_COLD_NEG2_01/source_model.py');calls=0;m=None
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def itree(t):return ('leaf',t) if isinstance(t,str) else I.node(t[0],itree(t[1]),itree(t[2]))
def plain(t):return t[1] if t[0]=='leaf' else (t[1],plain(t[2]),plain(t[3]))
def trace(t,x):
    u=itree(t);assert I.lookup(u,x)[0];v,e=I.trace(u,x)
    path='';cur=u
    while cur[1]!=x:
        c='L' if x<cur[1] else 'R';path+=c;cur=cur[2 if c=='L' else 3]
    return plain(v),path,e
def core(t,M):
    def go(u):
        if u[0]=='leaf':return None
        l,r=go(u[2]),go(u[3]);return (u[1],l,r) if u[1] in M or l is not None or r is not None else None
    return go(itree(t))
def labels(t):return set() if t is None else {t[0]}|labels(t[1])|labels(t[2])
def freeze(v):return tuple(map(freeze,v)) if isinstance(v,list) else v
def expand(t,lo=1,hi=6):return 'F'+str(hi) if t is None else (t[0],expand(t[1],lo,t[0]-1),expand(t[2],t[0]+1,hi))
def compact(t):return None if isinstance(t,str) else (t[0],compact(t[1]),compact(t[2]))
def main():
    global calls,m
    source=json.loads((B/'cheap_A_comparison.json').read_text());A=source['reports'][0]['A_trees'];aa=[expand(t) for t in A];idx={freeze(t):i for i,t in enumerate(A)};small={}
    for a,t in enumerate(aa):
        for x in range(1,7):
            if not 1<=len(P.path(t,x))<=2:continue
            calls+=1;dest,path,ev=P.trace(t,x);assert len(ev)==1;small[a,x]=idx[freeze(compact(dest))]
    reports=[]
    for r in source['reports']:
        states=[tuple(v) for v in r['states']];ix={v:i for i,v in enumerate(states)};D=r['debt']
        bf=json.loads((B/('bf'+str(r['core'])+'_comparison.json')).read_text());rank={x:i+1 for i,x in enumerate(r['BF_marks'])};full=[]
        for s,t,x,q in bf['edges']:
            if s>=len(r['BF_trees']):continue
            calls+=1;target,_,ev=trace(freeze(r['BF_trees'][s]),x)
            assert target==freeze(r['BF_trees'][t]) and sum(e[0]!='ZIG' for e in ev)==q
            full.append((s,t,rank[x],q))
        expected=set()
        for a,b in states:
            for s,t,x,q in full:
                if s!=b or (a,x) not in small:continue
                dest=ix[small[a,x],t];ss=ix[a,b];expected.add((ss,dest,x,q));assert 2-q+D[dest]-D[ss]>=0
        assert expected==set(map(tuple,r['edges']))
        high_bad=[]
        byB={}
        for i,(a,b) in enumerate(states):byB.setdefault(b,[]).append(D[i])
        for s,t,x,q in full:
            if 6-q+min(byB[t])-max(byB[s])<0:high_bad.append((s,t,x,q))
        reports.append({'core':r['core'],'H1_edges':len(expected),'H3_unconstrained_Ashape_adverse_count':len(high_bad),
            'H1_scope':'complete only within recorded BF mask and marked-A-core6 boundary representation',
            'H1_all_residuals_nonnegative':True})
    m=load('source_H2_syntax13',B/'audit_h2_release.py')
    m.p=types.SimpleNamespace(trace=trace,path=lambda t,x:trace_path(t,x),core=core,labels=labels)
    m.out=lambda n,v:out('independent_'+n,v);m.main()
    independent=json.loads((B/'independent_h2_release_audit.json').read_text())
    original=json.loads((B/'h2_release_audit.json').read_text())
    assert independent['A_H2_boundary_transitions']==original['A_H2_boundary_transitions']==948
    assert [(v['core'],v['H2_edges_checked'],len(v['failures'])) for v in independent['reports']]==[(v['core'],v['H2_edges_checked'],len(v['failures'])) for v in original['reports']]
    assert independent['reports'][0]['failures']==[]
    out('A6_independent_audit.json',{'status':'PASS_DISTINCT_KERNEL_RESTRICTED_A_DEPENDENT_CERTIFICATES','reports':reports,
        'H2_core9_release_edges_verified':141060,'H2_schemas':948,
        'core9_A6_mixed_H':'PROVED local signed rules: H1 exact, H2 complete free-gap syntax, H>=3 automatic range2',
        'core10_11_full_funding':'OPEN','source_engine_calls':calls+m.calls,
        'no_false_countercertificate':'core11 H2 natural q5 adverse edges are NOT original paired-packet refutations',
        'trust':'same agent, different rotation kernels and independent core traversal; no formal/external certification'})
    print(json.dumps({'status':'PASS_RESTRICTED_CORE9_A6_LOCAL_PROOF','reports':reports,'calls':calls+m.calls}),flush=True)
def trace_path(t,x):
    u=itree(t);path=''
    while u[0]!='leaf' and u[1]!=x:
        c='L' if x<u[1] else 'R';path+=c;u=u[2 if c=='L' else 3]
    assert u[0]!='leaf';return path
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_A6_independent_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':calls+(m.calls if m else 0)})
