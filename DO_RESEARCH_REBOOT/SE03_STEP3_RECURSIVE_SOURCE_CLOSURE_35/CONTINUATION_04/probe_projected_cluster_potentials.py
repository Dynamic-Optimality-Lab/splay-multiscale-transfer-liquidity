"""New source observable: projected subtree multiplicities on a pinned period."""
import collections,hashlib,importlib.util,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;B=F.parents[1]/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();PHASE=sys.argv[3];V=None
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tup(t):return (t[0],tup(t[1]),tup(t[2])) if isinstance(t,list) else t
def main():
    global V
    srcpath=B/'SOURCE_JOINT_REPAIR_03/actual_monotone_return_source.json'
    annpath=F/'independent_core_sector_neutral.json';ann=json.loads(annpath.read_text())
    assert ann['input_sha256'][str(srcpath)]==sha(srcpath)
    src=json.loads(srcpath.read_text());rows=src['period_rows'];af=next(x for x in ann['controls'] if x['source']=='AF')
    S=af['S'];M=set(af['M']);ids={x:1<<i for i,x in enumerate(S)};m=sum(ids[x] for x in M)
    optional=[ids[x] for x in S if x not in M];carriers=[m+sum(v for i,v in enumerate(optional) if bits>>i&1) for bits in range(1<<len(optional))]
    sp=importlib.util.spec_from_file_location('new_projection_source_primitive',B/'audit_core39.py')
    V=importlib.util.module_from_spec(sp);sp.loader.exec_module(V);V.CAP=CAP;V.START=START;V.QCAP=QCAP;V.CALLS=0
    masked={};raw=[]
    def masks(t):
        if t in masked:return masked[t]
        out=[]
        def go(u):
            if u is None:return 0
            a=go(u[1])|go(u[2])|ids.get(u[0],0)
            if u[0] in ids:out.append(a)
            return a
        go(t);masked[t]=tuple(out);return masked[t]
    A0=tup(rows[0]['A_before']);B0=tup(rows[0]['BF_before']);A=A0;BF=B0
    for r in rows:
        assert A==tup(r['A_before']) and BF==tup(r['BF_before'])
        for e in r['A_events']:
            for rot in e['rotations']:
                a,z=tup(rot['before']),tup(rot['after']);assert a==A
                raw.append(('A',(r['t'],e['j'],rot['bit']),masks(a),masks(z),masks(BF),masks(BF),None,None))
                A=z
        assert A==tup(r['A_after'])
        if r['genuine_F']:
            assert A[0]==r['key'] and BF[0]!=r['key']
            z,_,q,events=V.splay(BF,r['key'],True);assert z==tup(r['BF_after']) and q==r['qF']
            stored=r['BF_events']
            assert len(events)==len(stored)
            for ev,prev in zip(events,stored):
                assert ev['pattern']==prev['pattern'] and len(ev['rotations'])==len(prev['rotations'])
                for a,b in zip(ev['rotations'],prev['rotations']):
                    assert all(a[k]==b[k] for k in ('bit','pivot','direction'))
            double=0;g=BF[0];x=r['key']
            for e in events:
                d=None
                if len(e['pattern'])==2:double+=1;d=(r['t'],double)
                for rot in e['rotations']:
                    a,z=tup(rot['before']),tup(rot['after']);assert BF==a
                    lost=collections.Counter(masks(a))-collections.Counter(masks(z))
                    gained=collections.Counter(masks(z))-collections.Counter(masks(a))
                    assert sum(lost.values())==sum(gained.values())==1
                    old=next(iter(lost));assert old&ids[x] and not old&ids[g]
                    raw.append(('B',d,masks(A),masks(A),masks(a),masks(z),g,x));BF=z
            assert double==q
        assert BF==tup(r['BF_after'])
    assert A==A0 and BF==B0
    D={(r['t'],j) for r in rows for j in range(1,r['qF']+1)}
    graphs={d:set() for d in D};survivors=set(D);summaries=[];fixed_full=None
    for c in carriers:
        cache={}
        def phi(a,b):
            key=(a,b)
            if key not in cache:
                aa=collections.Counter(v&c for v in a);bb=collections.Counter(v&c for v in b)
                cache[key]=sum((bb-aa).values())
            return cache[key]
        ups=collections.defaultdict(list);downs=collections.defaultdict(list);drops=collections.defaultdict(int)
        prev=None
        for j,(kind,identity,ab,az,bb,bz,g,x) in enumerate(raw):
            a,z=phi(ab,bb),phi(az,bz)
            if prev is not None:assert prev==a
            else:start=a
            prev=z
            if kind=='A':
                assert z-a in (-1,0,1)
                if z>a:ups[z].append(identity)
            else:
                assert z-a in (-1,0)
                if z<a and identity is not None:drops[identity]+=1;downs[a].append(identity)
        assert prev==start
        for level,ds in downs.items():
            assert len(ups[level])>=len(ds)
            for d in ds:graphs[d].update(ups[level])
        neutral=D-set(drops);survivors.intersection_update(neutral)
        summaries.append({'carrier':[x for x in S if ids[x]&c],'B0':len(neutral),'B1':sum(n==1 for n in drops.values()),
          'B2':sum(n==2 for n in drops.values()),'neutral_demands':sorted(neutral)})
        if c==(1<<len(S))-1:fixed_full=neutral
        assert time.process_time()-START<CAP-3
    assert fixed_full==D-{tuple(x['demand']) for x in af['g_plus']}
    # Add every local bit (strictly more generous than first-loss selection).
    ends=[i for i,r in enumerate(rows) if r['genuine_F']];local={};h0={}
    for j,e in enumerate(ends):
        a=(ends[j-1]+1)%len(rows);rr=rows[a:e+1] if a<=e else rows[a:]+rows[:e+1]
        U=[(r['t'],k,b) for r in rr for k in range(1,r['a']+1) for b in (0,1)]
        dd=[(rows[e]['t'],k) for k in range(1,rows[e]['qF']+1)];h0.update(zip(dd,U))
        for d in dd:local[d]=U;graphs[d].update(U)
    owner={};match={}
    def add(d,seen):
        for u in sorted(graphs[d]):
            if u in seen:continue
            seen.add(u)
            if u not in owner or add(owner[u],seen):owner[u]=d;match[d]=u;return True
        return False
    for d in sorted(D):add(d,set())
    pending=list(D-set(match));T=set(pending);N=set()
    while pending:
        d=pending.pop()
        for u in graphs[d]:
            N.add(u);assert u in owner
            if owner[u] not in T:T.add(owner[u]);pending.append(owner[u])
    assert len(T)-len(N)==len(D)-len(match)
    result={'status':'AF_ALL_MARK_RETAINING_PROJECTION_RELATION_CHECKED','source_sha256':sha(srcpath),
      'accepted_annotation_sha256':sha(annpath),'source_queries':V.CALLS,'source_engine_calls':V.CALLS,
      'M':sorted(M),'S':S,'carriers':summaries,'all_projection_neutral_demands':sorted(survivors),
      'all_projection_all_level_donor_edges':sum(map(len,graphs.values())),'Q':len(D),
      'maximum_matching_size':len(match),'cut':{'demands':sorted(T),'neighborhood':sorted(N),'deficiency':len(T)-len(N)},
      'cut_rows':[{'demand':d,'actual_candidate_units':sorted(graphs[d]),'same_macro_units':local[d]} for d in sorted(T)],
      'original_h0':[{'demand':d,'unit':u} for d,u in sorted(h0.items())],
      'root_JR35':'OPEN','Bank25_or_extra_lock_promotion':False}
    with (F/'projected_cluster_AF_control.json').open('x',encoding='utf8') as f:json.dump(result,f,indent=2)
    print(json.dumps({'status':result['status'],'source_queries':V.CALLS,'carriers':len(carriers),'min_B0':min(z['B0'] for z in summaries),
      'all_projection_neutral_demands':result['all_projection_neutral_demands'],'matched':len(match),'Q':len(D),'cut':result['cut']}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        n=0 if V is None else V.CALLS
        with (B/f'audit_{PHASE}_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':n,'source_engine_calls':n},f)
