"""Independent checks of new source tags/loss edges, reusing closed traces."""
import collections,hashlib,importlib.util,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;B=F.parents[1]/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();V=None
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tup(t):return (t[0],tup(t[1]),tup(t[2])) if isinstance(t,list) else t
def path(t,x):
    p=[]
    while True:
        p.append(t[0])
        if t[0]==x:return p
        t=t[1] if x<t[0] else t[2]
def core(t,M):return set().union(*(set(path(t,x)) for x in M))
def match(g):
    own={};out={}
    def go(d,seen):
        for u in sorted(g[d]):
            if u in seen:continue
            seen.add(u)
            if u not in own or go(own[u],seen):own[u]=d;out[d]=u;return True
        return False
    for d in sorted(g):go(d,set())
    S=set(g)-set(out);todo=list(S);N=set()
    while todo:
        d=todo.pop()
        for u in g[d]:
            N.add(u);assert u in own
            if own[u] not in S:S.add(own[u]);todo.append(own[u])
    assert len(S)-len(N)==len(g)-len(out)
    return out,{'demands':sorted(S),'neighborhood':sorted(N),'deficiency':len(S)-len(N)}
def main():
    global V
    pp=F/'FRESH_PROXY_LOSS_THEOREM.md';ti=F/'TOP_INTERVAL_AND_MARKED_DEMOTION.md'
    ann=F/'independent_core_sector_neutral.json';accepted=json.loads(ann.read_text())
    mdp=F/'marked_demotion_relation.json';md=json.loads(mdp.read_text())
    for p,h in md['input_sha256'].items():assert sha(Path(p))==h
    pins=[pp,ti,ann,mdp];reports=[]
    for name,p in [('AF',B/'SOURCE_JOINT_REPAIR_03/actual_monotone_return_source.json'),('CCR',F/'cluster_collateral_closed_source.json')]:
        assert accepted['input_sha256'][str(p)]==sha(p);pins.append(p)
        src=json.loads(p.read_text());rows=src['period_rows'];n=len(rows);by={r['t']:i for i,r in enumerate(rows)}
        ends=[i for i,r in enumerate(rows) if r['genuine_F']];g={};local={};perkey=collections.defaultdict(set);details=[];mdg={}
        def arc(a,b):
            length=(b-a)%n or n
            return [rows[(a+z)%n] for z in range(1,length+1)]
        def losses(start,end,y,x):
            rr=[]
            for r in arc(start,end):
                for e in r['A_events']:
                    for a in e['rotations']:
                        old=path(a['before'],x);new=path(a['after'],x)
                        if y in old[:-1] and y not in new[:-1]:
                            assert a['pivot']==y
                            rr.append((r['t'],e['j'],a['bit']))
            return rr
        for j,end in enumerate(ends):
            row=rows[end];t=row['t'];x=row['key'];p0=next(ends[(j-i)%len(ends)] for i in range(1,len(ends)+1) if rows[ends[(j-i)%len(ends)]]['key']==x)
            assert rows[p0]['BF_after'][0]==x
            Vset={x};tags={};cur={x};prior={}
            for w in arc(p0,end)[:-1]:
                assert core(w['BF_before'],Vset)==cur
                y=w['key'];first=w['genuine_F'] and y not in Vset
                if w['genuine_F']:prior[y]=by[w['t']]
                Vnew=Vset|{y} if first else Vset
                new=core(w['BF_after'],Vnew);growth=new-cur
                if first:
                    pp0=path(w['BF_before'],y);i=next((k for k,z in enumerate(pp0) if z not in cur),len(pp0))
                    allowed={y,pp0[i]} if i<len(pp0) else set()
                    assert growth<=allowed and len(growth)<=2
                    for z in growth:
                        if z!=x:tags.setdefault(z,(w['t'],y))
                else:assert not growth
                Vset=Vnew;cur=new
            bs=path(row['BF_before'],x);d=len(bs)-1;q=row['qF'];assert d//2==q and set(bs)<=cur
            own={(z['t'],a,b) for z in arc(ends[j-1],end) for a in range(1,z['a']+1) for b in (0,1)}
            tg={};options={};occ=collections.Counter()
            for k in range(1,q+1):
                D=(t,k);i=d-2*k;u,v=bs[i:i+2];a,b=tags[u],tags[v];occ.update((a,b));tg[D]={a,b}
                opts={}
                for label in tg[D]:
                    y=label[1];rr=losses(prior[y],end,y,x);assert rr;opts[label]=rr
                options[D]=opts;g[D]={z for rr in opts.values() for z in rr};local[D]=own
                G=u
                gs=next(ends[(j-a)%len(ends)] for a in range(1,len(ends)) if rows[ends[(j-a)%len(ends)]]['key']==G)
                mdg[D]=losses(gs,end,G,x);assert mdg[D]
            assert max(occ.values(),default=0)<=2
            chosen,cut=match(tg);assert len(chosen)==q and not cut['deficiency']
            picked=[options[d][tag][0] for d,tag in sorted(chosen.items())]
            assert len(set(picked))==q and not (set(picked)&perkey[x]);perkey[x].update(picked)
            details.append({'t':t,'target':x,'previous_x_t':rows[p0]['t'],'Q':q,'proxies':[{'demand':d,'tag':tag,'actual_first_loss_bit':options[d][tag][0]} for d,tag in sorted(chosen.items())]})
        mm=next(z for z in md['controls'] if z['source']==name)
        assert len(mdg)==len(g)==mm['Q']
        for z in mm['source_demands']:
            d=tuple(z['demand']);assert mdg[d]==[tuple(u) for u in z['loss_rotations']]
        mdonly={d:{(u[0],u[1],b) for u in us for b in (0,1)} for d,us in mdg.items()}
        cert=mm['comparisons']['all_loss_bits']['cut'];cs={tuple(d) for d in cert['demands']}
        assert set().union(*(mdonly[d] for d in cs))=={tuple(u) for u in cert['neighborhood']}
        assert len(cs)-len(cert['neighborhood'])==cert['deficiency']>0
        comp=mm['comparisons']['all_loss_and_local_bits']['matching'];seen=set();out=set()
        for a in comp:
            d,u=tuple(a['demand']),tuple(a['unit']);assert u in (mdonly[d]|local[d]) and u not in seen and d not in out;seen.add(u);out.add(d)
        assert out==set(g)
        fpm,fp_cut=match(g);fpl,fpl_cut=match({d:g[d]|local[d] for d in g})
        combo,combo_cut=match({d:g[d]|local[d]|mdonly[d] for d in g})
        reports.append({'source':name,'Q':len(g),'macros':details,'fixed_target_noncollision_verified':True,
          'FP_only':{'size':len(fpm),'cut':fp_cut},'FP_and_local':{'size':len(fpl),'cut':fpl_cut},
          'FP_MD_and_local':{'size':len(combo),'cut':combo_cut},
          'old_MD_loss_only_cut_verified':True,'old_MD_local_matching_verified':True})
    # Independent packet geometry for the n=17 joint obstruction.
    sp=importlib.util.spec_from_file_location('TI35_mutable',B/'audit_verify79.py');V=importlib.util.module_from_spec(sp);sp.loader.exec_module(V)
    V.CAP=CAP;V.START=START;V.QCAP=QCAP;V.CALLS=0
    n=17;BF=None;U=None
    for g0 in range(n,0,-2):BF=(g0,(g0-1,None,None) if g0>1 else None,BF)
    for g0 in range(n-1,1,-2):U=(g0,(g0-1,None,None) if g0>2 else None,U)
    A=(1,None,(n,U,None));a=V.Mutable(A);h,_,_=a.splay(n,True);az=tup(a.snapshot())
    b=V.Mutable(BF);_,q,ev=b.splay(n,True);bz=tup(b.snapshot());assert (h,q)==(1,4)
    def labels(t):
        ans=[]
        def go(u):
            if u is None:return frozenset()
            z=go(u[1])|go(u[2])|{u[0]};ans.append(z);return z
        go(t);return ans
    def top(t,lo,hi):
        while not lo<=t[0]<=hi:t=t[1] if t[0]>hi else t[2]
        return t[0]
    def measures(A,BF):
        bb=labels(BF)
        return (len(set(bb)-set(labels(A))),len(bb)-len({top(A,min(c),max(c)) for c in bb}))
    start=measures(A,BF);middle=measures(az,BF);end=measures(az,bz)
    drops=[]
    for e in ev:
        assert e['pattern']=='RR';rr=e['rotations'];a,z=measures(az,tup(rr[0]['before'])),measures(az,tup(rr[-1]['after']))
        drops.append((a[0]-z[0],a[1]-z[1]))
    assert start==end and middle==tuple(z+1 for z in start) and drops==[(0,0)]*3+[(1,1)]
    result={'status':'PASS_FP35_ORIGINAL_SOURCE_TAGS_AND_TI35_PACKET_CONTROL',
      'source_queries':V.CALLS,'source_engine_calls':V.CALLS,'controls':reports,
      'TI35_packet':{'n':n,'H':h,'Q':q,'PC_T_before':start,'PC_T_after_A':middle,'PC_T_after_B':end,
        'B_double_decreases':drops,'source_embedding':'symbolic family proof, not an enumerated 17-key closed replay',
        'new_CD_counterexample':False},'JR35':'OPEN','reservation':'DEFERRED',
      'input_sha256':{str(p):sha(p) for p in pins}}
    with (F/'independent_fresh_proxy_loss.json').open('x',encoding='utf8') as f:json.dump(result,f,indent=2)
    print(json.dumps({'status':result['status'],'source_queries':V.CALLS,'TI35_packet':result['TI35_packet'],
      'controls':[{k:v for k,v in r.items() if k!='macros'} for r in reports]}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        n=0 if V is None else V.CALLS
        with (B/'audit_verify128_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':n,'source_engine_calls':n},f)
