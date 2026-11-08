"""Independent diagnostic reconstruction after failed core41/core42.
It checks actual old B transitions and the new A reset, not nonexistent
producer snapshots. It is not reported as a completed producer/auditor pair.
"""
import importlib.util,json,sys,time,collections
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parent;B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();CALLS=0
sp=importlib.util.spec_from_file_location('distinct_pool_audit',F/'audit_pools.py');I=importlib.util.module_from_spec(sp);sp.loader.exec_module(I)
class Node:
    def __init__(self,k):self.k=k;self.left=self.right=self.parent=None
class State:
    def __init__(self,t):
        self.nodes={}
        def rec(v,parent=None):
            if not I.tree(v):return v
            u=Node(v[0]);u.parent=parent;self.nodes[u.k]=u;u.left=rec(v[1],u);u.right=rec(v[2],u);return u
        self.root=rec(t)
    def snapshot(self):
        def rec(u):return (u.k,rec(u.left),rec(u.right)) if isinstance(u,Node) else u
        return rec(self.root)
    def rotate(self,x):
        p=x.parent;g=p.parent
        if p.left is x:
            p.left=x.right
            if isinstance(p.left,Node):p.left.parent=p
            x.right=p
        else:
            assert p.right is x;p.right=x.left
            if isinstance(p.right,Node):p.right.parent=p
            x.left=p
        x.parent=g;p.parent=x
        if g is None:self.root=x
        elif g.left is p:g.left=x
        else:assert g.right is p;g.right=x
    def access(self,k):
        global CALLS
        assert CALLS<QCAP and time.process_time()-START<CAP-1;CALLS+=1
        x=self.nodes[k];d=0;u=x
        while u.parent:d+=1;u=u.parent
        while x.parent:
            p=x.parent;g=p.parent
            if g is None:self.rotate(x)
            elif (g.left is p)==(p.left is x):self.rotate(p);self.rotate(x)
            else:self.rotate(x);self.rotate(x)
        return (d+1)//2,d//2
def matching(N,D):
    # Independent shortest augmenting-path flow with unit capacities.
    h={};iv={}
    while True:
        queue=collections.deque([('d',d) for d in D-set(h)]);pred={('d',d):None for d in D-set(h)};terminal=None
        while queue and terminal is None:
            typ,v=queue.popleft()
            if typ=='d':
                for u in sorted(N[v]):
                    if ('u',u) in pred:continue
                    pred['u',u]=('d',v)
                    if u not in iv:terminal=('u',u);break
                    if ('d',iv[u]) not in pred:pred['d',iv[u]]=('u',u);queue.append(('d',iv[u]))
        if terminal is None:
            X={d for typ,d in pred if typ=='d'};NX=set().union(*(N[d] for d in X)) if X else set()
            return dict(complete=set(h)==D,matching=[dict(demand=d,unit=u) for d,u in sorted(h.items())],cut_demands=sorted(X),cut_units=sorted(NX),deficiency=len(X)-len(NX))
        v=terminal;changes=[]
        while pred[v] is not None:
            dv=pred[v];assert dv[0]=='d';changes.append((dv[1],v[1]));v=pred[dv]
            if v is None:break
        for d,u in changes:
            if d in h:iv.pop(h[d],None)
        for d,u in changes:h[d]=u;iv[u]=d
def main():
    path=P/'SE03_STEP3_NONEXTREMAL_SHALLOW_HELPER_REPAYMENT_30/nonextremal_source_countercertificate.json';assert I.sha(path)=='43a3d38a5cf157c0aa049411700351641597d8fed27babf1ebf41a3ad14b01b3'
    z=I.read(path);erase=z['erased_key'];assert erase==11
    A,BF,BE=[State(t) for t in z['rows'][0]['before']];cf=[];ce=[]
    for r in z['prefix_rows']:
        if r['mode']=='K' and r['before'][1][0]!=r['target']:cf=[r['target']]+[v for v in cf if v!=r['target']]
        if r['mode']=='K' and r['target']!=erase and r['before'][2][0]!=r['target']:ce=[r['target']]+[v for v in ce if v!=r['target']]
    initial=tuple(v.snapshot() for v in (A,BF,BE)),tuple(cf),tuple(ce)
    t0=z['prefix_rows'][-1]['occurrence'];reset=list(range(1,14))+list(range(12,0,-1));prefix=[]
    def step(t,kind,x):
        nonlocal cf,ce
        aa,bf,be=A.snapshot(),BF.snapshot(),BE.snapshot();a,_=A.access(x);q=qe=0
        if kind=='K':
            g=BF.root.k!=x;_,q=BF.access(x)
            if g:cf=[x]+[v for v in cf if v!=x]
            if x!=erase:
                g=BE.root.k!=x;_,qe=BE.access(x)
                if g:ce=[x]+[v for v in ce if v!=x]
        return dict(t=t,kind=kind,key=x,a=a,qF=q,qE=qe,A_before=aa,BF_before=bf,BE_before=be,A_after=A.snapshot(),BF_after=BF.snapshot(),BE_after=BE.snapshot(),chart_F=cf[:],chart_E=ce[:])
    for x in reset:prefix.append(step(t0+len(prefix)+1,'D',x))
    boundary=tuple(v.snapshot() for v in (A,BF,BE)),tuple(cf),tuple(ce);rows=[]
    for old in z['rows']:
        if not old['genuine_F']:continue
        r=step(t0+len(prefix)+len(rows)+1,'K',old['target']);rows.append(r)
        assert json.dumps([r['BF_before'],r['BE_before']])==json.dumps(old['before'][1:])
        assert json.dumps([r['BF_after'],r['BE_after']])==json.dumps(old['after'][1:])
        assert (r['qF'],r['qE'])==(old['qF'],old['qE'])
    for x in reset:rows.append(step(t0+len(prefix)+len(rows)+1,'D',x))
    end=tuple(v.snapshot() for v in (A,BF,BE)),tuple(cf),tuple(ce);assert boundary==end
    obj=dict(period_rows=rows);rr=I.canonical(obj,'C33_36');M={r['x'] for r in rr if r['gen']};assert len(M)==7
    assert all(len(M|set().union(*(I.amap(r['B0'])[x] for x in M)))==13 for r in rr)
    mm,D,U,N,h0=I.reconstruct(rr);h=matching(N,D);assert I.flow(N,D)==len(h['matching'])
    h.update(scope='candidate pool only; no all-route architecture conclusion')
    result=dict(status='PASS_INDEPENDENT_DIAGNOSTIC_MAXIMAL_SOURCE_RECONSTRUCTION',accepted_reaching_source=str(path),accepted_reaching_source_sha256=I.sha(path),original_accepted_prefix_reused=True,initial_after_accepted_prefix=initial,reset_prefix=prefix,period_rows=rows,period=[rows[0]['t'],rows[-1]['t']],period_boundary=boundary,source_engine_calls=CALLS,source_queries=CALLS,erased_key=erase,A=sum(r['a'] for r in rr),Q_F=sum(r['q'] for r in rr),D=len(D),U=len(U),raw_pool=h,current_fixed_auxiliary_input='NOT_SUPPLIED; no existing source owner is overwritten',producer_attempts=['core41 failed before source queries: wrong erased key','core42 failed after185 queries: absent genuine_E field left initial E chart empty'],verification_scope='distinct mutable-parent reconstruction and accepted B states; no saved successful producer A trace exists to compare',principal_JIO34='OPEN')
    with (F/'maximal_diagnostic_source.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:result[k] for k in ('status','period','A','Q_F','D','U','source_queries')}|{'pool_complete':h['complete']}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_verify82_exit.json').open('x') as f:json.dump(dict(whole_process_CPU_seconds=time.process_time(),error=error,source_queries=CALLS,source_engine_calls=CALLS),f)
