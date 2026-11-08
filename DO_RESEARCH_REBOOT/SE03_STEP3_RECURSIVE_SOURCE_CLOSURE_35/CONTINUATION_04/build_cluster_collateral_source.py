"""Actual closed dirty source with two cluster-funded three-debt blocks.
Fresh original source calls are charged; old native7/B actions are reused.
"""
import collections,hashlib,importlib.util,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1]
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();S=None
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def freeze(t):return None if t is None else (t[0],freeze(t[1]),freeze(t[2]))
def main():
    global S
    spec=importlib.util.spec_from_file_location('new_CCR_source',B/'audit_core39.py');S=importlib.util.module_from_spec(spec);spec.loader.exec_module(S)
    S.CAP=CAP;S.START=START;S.QCAP=min(QCAP,1600);S.CALLS=0
    m=read(F/'complete_product_model_k0.json');bt=read(F/'full_B_actions.json');bg=read(F/'maximal_B_grammar.json');diag=read(F/'high2_source_work_diagnosis.json')
    M=set(m['A_keys']);aids={freeze(t):i for i,t in enumerate(m['A_trees'])}
    ar1=(7,(3,(2,(1,None,None),None),(5,(4,None,None),(6,None,None))),None)
    ar2=(7,(4,(1,None,(2,None,(3,None,None))),(6,(5,None,None),None)),None)
    a1,a2=aids[ar1],aids[ar2]
    def follow(a,keys):
        for k in keys:a=m['A_destination'][a][m['A_keys'].index(k)]
        return a
    t1=follow(a1,[5,9,3]);t2=follow(a2,[7,11,1]);assert m['A_trees'][t2][0]==1
    def transform(s,t):
        if s==t:return []
        queue=collections.deque([s]);parent={s:None}
        while queue:
            u=queue.popleft()
            for x,k in enumerate(m['A_keys']):
                v=m['A_destination'][u][x]
                if v in parent:continue
                parent[v]=(u,k)
                if v==t:
                    path=[]
                    while parent[v] is not None:u,k=parent[v];path.append(k);v=u
                    return list(reversed(path))
                queue.append(v)
        raise AssertionError('accepted native7 transformation graph disconnected')
    def expand(t):
        gap=0
        def go(v):
            nonlocal gap
            if v is None:
                j=gap;gap+=1;return None if j in (0,7) else (2*j,None,None)
            return (2*v[0]-1,go(v[1]),go(v[2]))
        out=go(t);assert gap==8;return out
    b0=diag['steps_forward'][0]['source_B'];initial=freeze(bg['trees'][b0]);assert initial[0]==1
    cache={};search_log=[]
    def action(t,k):
        key=(t,k)
        if key in cache:return cache[key]
        if t[0]==k:return (t,0,0,[])
        value=S.splay(t,k,True);cache[key]=value;return value
    def countcore(t):
        if t is None:return 0,False
        l,lm=countcore(t[1]);r,rm=countcore(t[2]);yes=t[0] in M or lm or rm
        return (l+r+int(yes),yes)
    A=initial;prefix_ops=[]
    while countcore(A)[0]>7:
        limit=countcore(A)[0];queue=collections.deque([A]);parents={A:None};found=None
        while queue and found is None:
            u=queue.popleft()
            for k in sorted(M):
                if k==u[0]:continue
                assert S.CALLS<900
                v,h,q,ev=action(u,k);c=countcore(v)[0]
                search_log.append({'before_sha256':hashlib.sha256(repr(u).encode()).hexdigest(),'key':k,'A_events':h,'core_after':c})
                if v in parents:continue
                parents[v]=(u,k)
                if c<limit:found=v;break
                queue.append(v)
            assert time.process_time()-START<CAP-5
        assert found is not None,'bounded prefix compiler did not find a core reduction'
        path=[];v=found
        while parents[v] is not None:u,k=parents[v];path.append(k);v=u
        for k in reversed(path):prefix_ops.append(('D',k));A=action(A,k)[0]
    def project(t):
        if t is None:return None
        l,r=project(t[1]),project(t[2])
        if t[0] in M:return ((t[0]+1)//2,l,r)
        assert l is None and r is None;return None
    current=aids[project(A)];assert A==expand(m['A_trees'][current])
    for k in transform(current,t2):prefix_ops.append(('D',k));A=action(A,k)[0]
    assert A==expand(m['A_trees'][t2])
    g1=transform(t2,a1);g2=transform(t1,a2)
    period_ops=[('D',k) for k in g1]+[('K',13),('K',5),('K',9),('K',3)]+[('D',k) for k in g2]+[('K',13),('K',7),('K',11),('K',1)]
    rows=[];A=initial;BF=initial;BE=initial;bi={freeze(t):i for i,t in enumerate(bg['trees'])};cf=[];ce=[];erased=3
    def push(chart,k):return [k]+[x for x in chart if x!=k]
    def append(kind,k):
        nonlocal A,BF,BE,cf,ce
        t=len(rows)+1;before=(A,BF,BE);A,h,qa,ae=action(A,k);q=qe=0;gf=ge=False
        if kind=='K':
            gf=BF[0]!=k;bb=bi[BF];entry=bt['actions'][bb][m['A_keys'].index(k)];assert entry['admissible']
            q=entry['q'];BF=freeze(bg['trees'][entry['destination']])
            if gf:cf=push(cf,k)
            if k!=erased:
                ge=BE[0]!=k
                if ge:BE,he,qe,ee=action(BE,k)
                if ge:ce=push(ce,k)
        row={'t':t,'kind':kind,'key':k,'A_before':before[0],'BF_before':before[1],'BE_before':before[2],
          'A_after':A,'BF_after':BF,'BE_after':BE,'a':h,'qF':q,'qE':qe,'genuine_F':gf,'genuine_E':ge,
          'A_events':ae,'chart_F':cf[:5],'chart_E':ce[:5]};rows.append(row)
    for kind,k in prefix_ops:append(kind,k)
    a0=A;assert BF==initial and BE==initial
    seen={};copy=0;period_start_row=None
    while True:
        key=(BE,tuple(cf[:5]),tuple(ce[:5]))
        if key in seen:period_start_row=seen[key];break
        seen[key]=len(rows)+1
        for kind,k in period_ops:append(kind,k)
        copy+=1;assert copy<=20 and A==a0 and BF==initial
        assert time.process_time()-START<CAP-4
    prefix=[r for r in rows if r['t']<period_start_row];period=[r for r in rows if r['t']>=period_start_row]
    assert period and freeze(period[0]['A_before'])==A and freeze(period[0]['BF_before'])==BF and freeze(period[0]['BE_before'])==BE
    ends=[i for i,r in enumerate(period) if r['genuine_F']];mm=[];h0={};start=0
    for end in ends:
        rr=period[start:end+1];units=[(r['t'],j,b) for r in rr for j in range(1,r['a']+1) for b in (0,1)]
        demands=[(r['t'],k) for r in rr for k in range(1,r['qF']+1)];h0.update(zip(demands,units))
        mm.append({'times':[r['t'] for r in rr],'H':len(units)//2,'Q':len(demands),'units':units,'demands':demands});start=end+1
    assert start==len(period) and len(mm)%8==0
    def clusters(t,out):
        if t is None:return 0
        bits=clusters(t[1],out)|clusters(t[2],out)
        if t[0] in M:bits|=1<<((t[0]-1)//2)
        if bits:out.add(bits)
        return bits
    by={r['t']:r for r in period};h=dict(h0);blocks=[]
    for i in range(0,len(mm),4):
        recovery=mm[i];lows=mm[i+1:i+4];assert recovery['Q']==2 and all(p['H']==1 and p['Q']==3 for p in lows)
        rr=[by[t] for t in recovery['times']];before=set();after=set();clusters(rr[0]['A_before'],before);clusters(rr[-1]['A_after'],after)
        lost=before-after;assert len(lost)==6
        first={}
        for r in rr:
            for e in r['A_events']:
                for rot in e['rotations']:
                    old=set();new=set();clusters(rot['before'],old);clusters(rot['after'],new)
                    for c in lost&(old-new):first.setdefault(c,(r['t'],e['j'],rot['bit']))
        assert set(first)==lost and len(set(first.values()))==6
        owned={h0[d] for d in recovery['demands']};spare=sorted(u for u in first.values() if u not in owned);assert len(spare)>=3
        missing=[d for p in lows for d in p['demands'] if d not in h0];assert len(missing)==3
        pairs=list(zip(missing,spare[:3]));h.update(pairs)
        blocks.append({'macro_indices':list(range(i,i+4)),'recovery_times':recovery['times'],'H_recovery':recovery['H'],'Q_recovery':2,
          'lost_clusters':sorted(lost),'first_removal_units':[{'cluster':c,'unit':u} for c,u in sorted(first.items())],
          'fixed_own_units':sorted(owned),'new_pairs':[{'demand':d,'unit':u} for d,u in pairs]})
    U={(r['t'],j,b) for r in period for j in range(1,r['a']+1) for b in (0,1)};D={(r['t'],k) for r in period for k in range(1,r['qF']+1)}
    assert set(h)==D and len(set(h.values()))==len(h) and set(h.values())<=U and all(h[d]==u for d,u in h0.items())
    out={'status':'ACTUAL_PAIRED_CLOSED_CLUSTER_COLLATERAL_SOURCE_PENDING_INDEPENDENT_AUDIT','initial_diagonal':initial,'erased_key':erased,
      'prefix_rows':prefix,'period_rows':period,'period':[period_start_row,len(rows)],'word_copies_in_period':len(mm)//8,
      'source_A_preparation_words':{'to_first_frame':g1,'to_second_frame':g2},'prefix_core_reduction_search':search_log,
      'A_events':len(U)//2,'QF':len(D),'QE':sum(r['qE'] for r in period),'h0':[{'demand':d,'unit':u} for d,u in sorted(h0.items())],
      'full_h':[{'demand':d,'unit':u} for d,u in sorted(h.items())],'blocks':blocks,'proved_source_working_bound':5,
      'source_engine_calls':S.CALLS,'source_queries':S.CALLS,'auxiliary_numerical_allocation':'NOT_CONSTRUCTED_OR_SUBSTITUTED',
      'historical_owners_changed':False,'JR35':'OPEN','Coarse_Double_counterexample':False,
      'input_sha256':{p:sha(F/p) for p in ('CLUSTER_COLLATERAL_REPAYMENT.md','complete_product_model_k0.json','full_B_actions.json','high2_source_work_diagnosis.json')}}
    with (F/'cluster_collateral_closed_source.json').open('x',encoding='utf-8') as f:json.dump(out,f,indent=2)
    print(json.dumps({k:v for k,v in out.items() if k in ('status','period','A_events','QF','QE','proved_source_working_bound','source_queries','word_copies_in_period','source_A_preparation_words')}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        calls=0 if S is None else S.CALLS
        with (B/'audit_core46_exit.json').open('x',encoding='utf-8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':calls,'source_engine_calls':calls},f)
