"""Distinct pool construction and max-flow check; accepted primitives reused.
No import of retirement_pools; no new original splay/source query.
"""
import collections,hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parent;B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
START=time.process_time();CAP=float(sys.argv[1])
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def tree(t):return isinstance(t,list) and len(t)==3 and isinstance(t[0],(int,float))
def amap(t):
    out={}
    def rec(v,path):
        if tree(v):
            assert v[0] not in out;out[v[0]]=set(path)
            rec(v[1],path+[v[0]]);rec(v[2],path+[v[0]])
    rec(t,[]);return out
def canonical(z,name):
    rr=[]
    for a in (z['period_rows'] if name in ('C33_36','frame13') else z['rows']):
        if name=='C33_36':r=dict(t=a['t'],mode=a['kind'],x=a['key'],a=a['a'],q=a['qF'],A0=a['A_before'],A1=a['A_after'],B0=a['BF_before'],B1=a['BF_after'])
        elif name=='frame13':
            aa=z['A_word_source_rows'][a['word_index']];assert aa['key']==a['key'] and aa['H']==a['H']
            r=dict(t=a['absolute_t'],mode=a['kind'],x=a['key'],a=a['H'],q=a['QF'],A0=aa['before'],A1=aa['after'],B0=a['BF_before'],B1=a['BF_after'])
        else:r=dict(t=a['occurrence'],mode=a['mode'],x=a['target'],a=a['a'],q=a['qF'],A0=a['before'][0],A1=a['after'][0],B0=a['before'][1],B1=a['after'][1])
        r['gen']=r['mode']=='K' and r['B0'][0]!=r['x'];rr.append(r)
    assert len({r['t'] for r in rr})==len(rr)
    for i,r in enumerate(rr):
        nxt=rr[(i+1)%len(rr)];assert r['A1']==nxt['A0'] and r['B1']==nxt['B0']
        assert r['A1'][0]==r['x'] and r['a']>=0
    return rr
def pairmap(p):return {tuple(x['demand']):tuple(x['unit']) for x in p}
def reconstruct(rows):
    n=len(rows);M={r['x'] for r in rows if r['gen']};assert len(M)>=7
    A=[(amap(r['A0']),amap(r['A1'])) for r in rows]
    U={r['t']:{(r['t'],j,b) for j in range(1,r['a']+1) for b in (0,1)} for r in rows}
    events={r['t']:r for r in rows};ends=[i for i,r in enumerate(rows) if r['gen']]
    macros=[];N={};D=set();h0={}
    for mi,e in enumerate(ends):
        prev=ends[mi-1];inds=[];i=(prev+1)%n
        while True:
            inds.append(i)
            if i==e:break
            i=(i+1)%n
        ownops={rows[i]['t'] for i in inds};x=rows[e]['x'];gset=amap(rows[e]['B0'])[x]&M
        assert len(gset)==rows[e]['q'];ret=set();first=collections.Counter();proof={}
        for g in sorted(gset):
            j=(e-1)%n
            while not(rows[j]['gen'] and rows[j]['x']==g):
                j=(j-1)%n;assert j!=e
            assert g in A[j][1][x];born=rows[j]['t'];loss=[];j=(j+1)%n
            while True:
                if g in A[j][0][x] and g not in A[j][1][x]:loss.append(rows[j]['t'])
                if j==e:break
                j=(j+1)%n
            assert loss;ret.update(loss);first[loss[0]]+=1;proof[g]=(born,loss)
        assert all(v<=2*events[t]['a'] for t,v in first.items())
        T=set().union(*(U[t] for t in ret)) if ret else set();nn=T|set().union(*(U[t] for t in ownops))
        dd={(rows[e]['t'],k) for k in range(1,rows[e]['q']+1)};assert len(T)>=len(dd)
        for d in dd:N[d]=nn
        uu=[(rows[i]['t'],j,b) for i in inds for j in range(1,rows[i]['a']+1) for b in (0,1)]
        h0.update(zip(sorted(dd),uu));D.update(dd)
        macros.append(dict(end=rows[e]['t'],Q=len(dd),H=len(uu)//2,own_operations=ownops,retiring_operations=ret,T=T,N=nn,demands=dd,proof=proof))
    return macros,D,set().union(*U.values()),N,h0
def flow(N,D,fixed=None,allowed=None):
    fixed=fixed or {};g=[]
    def node():g.append([]);return len(g)-1
    source=node();sink=node();left={d:node() for d in sorted(D)};units=set().union(*N.values())|set(fixed.values())
    if allowed is not None:units&=set(allowed)|set(fixed.values())
    right={u:node() for u in sorted(units)}
    def edge(a,b,c):
        g[a].append([b,len(g[b]),c]);g[b].append([a,len(g[a])-1,0])
    for d,v in left.items():
        edge(source,v,1);nn=N[d]|({fixed[d]} if d in fixed else set())
        for u in nn&units:edge(v,right[u],1)
    for v in right.values():edge(v,sink,1)
    total=0
    while True:
        level=[-1]*len(g);level[source]=0;q=collections.deque([source])
        while q:
            v=q.popleft()
            for w,_,c in g[v]:
                if c and level[w]<0:level[w]=level[v]+1;q.append(w)
        if level[sink]<0:return total
        cursor=[0]*len(g)
        def send(v):
            if v==sink:return 1
            while cursor[v]<len(g[v]):
                e=g[v][cursor[v]];w,rev,c=e
                if c and level[w]==level[v]+1 and send(w):e[2]-=1;g[w][rev][2]+=1;return 1
                cursor[v]+=1
            return 0
        while send(source):total+=1
def check_result(z,N,D,U,fixed=None,allowed=None):
    fixed=fixed or {};val=flow(N,D,fixed,allowed);assert z['complete']==(val==len(D))
    if not z['complete']:
        X={tuple(d) for d in z['macro_complete_demands']};neigh=set().union(*(N[d]|({fixed[d]} if d in fixed else set()) for d in X))
        if allowed is not None:neigh&=set(allowed)|set(fixed.values())
        assert neigh=={tuple(u) for u in z['macro_complete_neighborhood']} and len(X)-len(neigh)==z['macro_deficiency']>0
        return dict(maxflow=val,complete=False,deficiency=z['macro_deficiency'])
    h=pairmap(z['matching']);assert set(h)==D and len(set(h.values()))==len(D) and set(h.values())<=U
    for d,u in h.items():assert u in N[d] or fixed.get(d)==u
    extra=pairmap(z['extra']);assert set(extra)==D-set(fixed) and not set(extra.values())&set(fixed.values()) and len(set(extra.values()))==len(extra)
    inv={u:d for d,u in fixed.items()};seen=set();roots=set()
    for p in z['paths']:
        root=tuple(p['root']);assert root not in roots;roots.add(root);d=root
        for ii,(dd,uu) in enumerate(p['steps']):
            dd,uu=tuple(dd),tuple(uu);assert dd==d and dd not in seen and uu in N[dd];seen.add(dd)
            if ii+1==len(p['steps']):assert uu not in inv and uu==extra[root]==tuple(p['terminal'])
            else:assert uu in inv;d=inv[uu]
    assert roots==D-set(fixed)
    return dict(maxflow=val,complete=True,unpaid=len(extra),old_values_preserved=len(fixed))
def main():
    result=read(F/'pooled_source_results.json');receipts=[]
    for case in result['cases']:
        assert time.process_time()-START<CAP-2
        path=Path(case['path']);receipt=Path(case['receipt']);assert sha(path)==case['input_sha256'] and sha(receipt)==case['receipt_sha256']
        z=read(path);rr=canonical(z,case['name']);assert rr==case['source_rows']
        mm,D,U,N,h0=reconstruct(rr);assert len(D)==case['D'] and len(U)==case['U']
        for a,b in zip(mm,case['macros']):
            for key in ('end','H','Q'):assert a[key]==b[key]
            for key in ('own_operations','retiring_operations','T','N','demands'):
                expected=set(b[key]) if key.endswith('operations') else {tuple(v) for v in b[key]}
                assert a[key]==expected
            assert a['proof']=={p['g']:(p['born_after'],p['all_retiring_operations']) for p in b['retirement_proof']}
        rec=dict(source=case['name'],source_hash=sha(path),raw=check_result(case['raw_pool'],N,D,U),macro_count=len(mm))
        fixed=None
        if case['name']=='C33_36':
            oz=read(case['owners_path']);assert sha(Path(case['owners_path']))==case['owners_sha256'];fixed=pairmap(oz['full_allocation']);prior=pairmap(oz['old_canonical_effective_a0']);new=pairmap(oz['new_actual_pairs'])
            rec['archive_only']=check_result(case['archived32_control'],N,D,U,prior)
            rec['accepted_four_endpoints']=check_result(case['accepted_four_endpoint_test'],N,D,U,prior,set(new.values()))
            assert set(fixed)==D and fixed==prior|new
        elif case['name']=='W199':fixed=pairmap(z['final_full_allocation'])
        elif case['name']=='W459':fixed=pairmap(z['current_complete_a'])
        if fixed is not None:
            assert len(set(fixed.values()))==len(fixed) and set(fixed.values())<=U
            rec['current_owners']=check_result(case['current_pool_owner_test'],N,D,U,fixed)
        receipts.append(rec)
    collision=B/'SOURCE_JOINT_REPAIR_03/actual_interior_ticket_collision.json'
    assert sha(collision)=='bda474c2e27873aa90aa7c85a78d1a383bb10a0d37ae385f905fb6d9b026079f'
    # Independent physical resolution of the accepted local prefix. These are
    # current-macro alternatives, not invented frozen owners or a new full period.
    collision_resolution=[((2,1),(1,1,0)),((3,1),(3,1,0)),((3,2),(3,1,1)),((4,1),(4,1,0)),((4,2),(4,1,1))]
    cz=read(collision);rows=cz.get('rows',cz.get('local_rows'))
    assert rows is not None
    by={r['t']:r for r in rows};assert set(by)==set(range(5))
    for r,s in zip(rows,rows[1:]):assert r['A_after']==s['A_before'] and r['BF_after']==s['BF_before']
    assert [(r['kind'],r['key'],r['a'],r['qF']) for r in rows]==[('K',13,0,6),('D',7,1,0),('K',1,1,1),('K',3,2,2),('K',5,2,2)]
    DD={(r['t'],k) for r in rows if r['t']>0 and r['kind']=='K' for k in range(1,r['qF']+1)}
    UU={(r['t'],j,b) for r in rows if r['t']>0 for j in range(1,r['a']+1) for b in (0,1)}
    pp=dict(collision_resolution);assert set(pp)==DD and len(set(pp.values()))==len(DD) and set(pp.values())<=UU and len(UU)==12
    for d,u in pp.items():assert (d[0]==2 and u[0] in (1,2)) or d[0]==u[0]
    for x in (1,3,5):assert 13 in amap(by[1]['A_before'])[x] and 13 not in amap(by[1]['A_after'])[x]
    with (F/'independent_pool_audit.json').open('x',encoding='utf-8') as f:json.dump(dict(status='PASS_DISTINCT_POOL_RECONSTRUCTION_AND_MAXFLOW',input_sha256={'pooled_source_results.json':sha(F/'pooled_source_results.json'),'retirement_pools.py':sha(F/'retirement_pools.py')},source_receipts=receipts,collision_source_sha256=sha(collision),local_collision_alternative_pairs=collision_resolution,collision_owner_scope='raw source-prefix alternatives only; no additional frozen map assumed',source_engine_calls=0,source_queries=0,universal_source_expansion='OPEN',original_source_license='NOT_VERIFIED_BY_THIS_STATIC_LAYER',Bank25_universal='OPEN'),f,indent=2)
    print('PASS independent source-pool construction, maxflow and frozen-owner endpoint checks',flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_verify80_exit.json').open('x') as f:json.dump(dict(whole_process_CPU_seconds=time.process_time(),error=error,source_queries=0,source_engine_calls=0),f)
