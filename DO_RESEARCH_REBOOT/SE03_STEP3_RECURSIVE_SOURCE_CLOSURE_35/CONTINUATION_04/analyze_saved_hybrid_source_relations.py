"""Exact new eligibility graphs on saved original sources; no replay."""
import collections,hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time();PHASE=sys.argv[3]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tup(t):return (t[0],tup(t[1]),tup(t[2])) if isinstance(t,list) else t
def path(t,x):
    a=[]
    while True:
        assert isinstance(t,tuple);a.append(t[0])
        if t[0]==x:return a
        t=t[1] if x<t[0] else t[2]
def core(t,M):return set().union(*(set(path(t,x)) for x in M))
def edge(t,p,x):
    while isinstance(t,tuple) and t[0]!=p:t=t[1] if p<t[0] else t[2]
    return isinstance(t,tuple) and any(isinstance(c,tuple) and c[0]==x for c in t[1:])
def maximum(graph):
    inv={};out={}
    def aug(d,seen):
        for u in sorted(graph[d]):
            if u in seen:continue
            seen.add(u)
            if u not in inv or aug(inv[u],seen):inv[u]=d;out[d]=u;return True
        return False
    for d in sorted(graph):aug(d,set())
    S=set(graph)-set(out);todo=list(S);N=set()
    while todo:
        for u in graph[todo.pop()]:
            N.add(u);assert u in inv
            if inv[u] not in S:S.add(inv[u]);todo.append(inv[u])
    assert len(S)-len(N)==len(graph)-len(out)
    return {'matched':len(out),'cut':{'demands':sorted(S),'neighborhood':sorted(N),'deficiency':len(S)-len(N)}}
def main():
    sources=[];pins=[]
    for filename in ('zero_run_source_certificates.json','leaf_source_certificates2.json'):
        p=P/'SE03_STEP3_UNIFORM_DONOR_GROUPING_15'/filename;j=json.loads(p.read_text());pins.append(p)
        for k,s in enumerate(j['reports']):sources.append((filename+':'+str(k),s['rows'],'accepted C15 independent source audit'))
    p=P/'SE03_STEP3_RR7_CREATOR_MARKED_FRONTIERS_18/overfull_source_result.json';j=json.loads(p.read_text());pins.append(p)
    sources.append(('C18_OVERFULL',j['rows'],'C18 derivation audit pending; diagnostic only'))
    for name,p in [('AF',B/'SOURCE_JOINT_REPAIR_03/actual_monotone_return_source.json'),('CCR',F/'cluster_collateral_closed_source.json')]:
        j=json.loads(p.read_text());pins.append(p);sources.append((name,j['period_rows'],'accepted current source receipt'))
    reports=[]
    for name,raw,status in sources:
        rows=[]
        for r in raw:
            if 'before' in r:
                rows.append({'t':r['occurrence'],'kind':r['mode'],'x':r['target'],'H':r['a'],'Q':r['qF'],'genuine':r['genuine_F'],
                  'Ab':tup(r['before'][0]),'Az':tup(r['after'][0]),'Bb':tup(r['before'][1]),'Bz':tup(r['after'][1])})
            else:
                rows.append({'t':r['t'],'kind':r['kind'],'x':r['key'],'H':r['a'],'Q':r['qF'],'genuine':r['genuine_F'],
                  'Ab':tup(r['A_before']),'Az':tup(r['A_after']),'Bb':tup(r['BF_before']),'Bz':tup(r['BF_after'])})
        assert rows[0]['Ab']==rows[-1]['Az'] and rows[0]['Bb']==rows[-1]['Bz']
        n=len(rows);by={r['t']:i for i,r in enumerate(rows)};assert len(by)==n
        ends=[i for i,r in enumerate(rows) if r['genuine']];M={rows[i]['x'] for i in ends}
        def arc(a,b,inc=True):
            length=(b-a)%n or n
            return [rows[(a+j)%n] for j in range(1,length+int(inc))]
        def units(rr):return {(r['t'],j,b) for r in rr for j in range(1,r['H']+1) for b in (0,1)}
        macros=[];macro_for={};h0={}
        for j,e in enumerate(ends):
            rr=arc(ends[j-1],e);uu=sorted(units(rr),key=lambda u:((by[u[0]]-by[rr[0]['t']])%n,u[1],u[2]))
            dd=[(rows[e]['t'],k) for k in range(1,rows[e]['Q']+1)];h0.update(zip(dd,uu))
            macros.append({'rows':rr,'units':uu,'demands':dd,'H':sum(r['H'] for r in rr),'Q':len(dd),'end':e})
            for r in rr:macro_for[r['t']]=j
        graphs={v:{} for v in ('FP_FIRST_OWN','FP_CREATOR_TAIL_OWN','FP_ALL_WINDOW')}
        selected=[]
        for j,e in enumerate(ends):
            row=rows[e];x=row['x'];prev=next(ends[(j-d)%len(ends)] for d in range(1,len(ends)+1) if rows[ends[(j-d)%len(ends)]]['x']==x)
            marks={x};cur={x};tags={};latest={}
            for r in arc(prev,e,False):
                y=r['x'];assert core(r['Bb'],marks)==cur
                first=r['genuine'] and y not in marks
                if r['genuine']:latest[y]=by[r['t']]
                new=core(r['Bz'],marks|{y} if first else marks);growth=new-cur
                if first:
                    assert len(growth)<=2
                    for z in growth:tags.setdefault(z,y)
                else:assert not growth
                if first:marks.add(y)
                cur=new
            pp=path(row['Bb'],x);depth=len(pp)-1;assert depth//2==row['Q']
            mac=macros[j];creators=set();watch=None;creator_t=None
            if mac['H']==1:
                positive=next(r for r in mac['rows'] if r['H'])
                ap=path(positive['Ab'],x);assert len(ap) in (2,3)
                watch=(ap[-2],x) if len(ap)==2 or ap[-2] not in M else (ap[0],ap[1])
                assert edge(positive['Ab'],*watch) and not edge(positive['Az'],*watch)
                di=by[positive['t']]
                birth=next(rows[(di-k)%n] for k in range(1,n+1) if not edge(rows[(di-k)%n]['Ab'],*watch) and edge(rows[(di-k)%n]['Az'],*watch))
                creator_t=birth['t'];creators=units([birth])
                cm=macros[macro_for[creator_t]];creators|=set(cm['units'][cm['Q']:])
            for k,d in enumerate(mac['demands'],1):
                a,b=pp[depth-2*k:depth-2*k+2];proxies={tags[a],tags[b]};first=set(mac['units']);window=set(first)
                for y in proxies:
                    period=arc(latest[y],e);window|=units(period)
                    loss=next(r for r in period if y in path(r['Ab'],x)[:-1] and y not in path(r['Az'],x)[:-1])
                    first|=units([loss])
                graphs['FP_FIRST_OWN'][d]=first
                graphs['FP_CREATOR_TAIL_OWN'][d]=first|creators
                graphs['FP_ALL_WINDOW'][d]=window
            if mac['Q']>2*mac['H']:selected.append({'end_t':row['t'],'H':mac['H'],'Q':mac['Q'],'watch':watch,'creator_t':creator_t})
        outcomes={k:maximum(g) for k,g in graphs.items()}
        reports.append({'source':name,'source_status':status,'r':len(M),'A':sum(r['H'] for r in rows),'Q':sum(r['Q'] for r in rows),
          'actual_rows':n,'natural_unpaid_macros':selected,'relations':outcomes,'old_owners_or_source_mutated':False})
        assert time.process_time()-START<CAP-2
    r={'status':'SAVED_ORIGINAL_SOURCE_HYBRID_RELATIONS_ANALYZED','controls':reports,
      'source_queries':0,'source_engine_calls':0,'passing_cases_are_not_universal':True,'JR35':'OPEN',
      'input_sha256':{str(p):sha(p) for p in pins}}
    with (F/'saved_hybrid_source_relations.json').open('x',encoding='utf8') as f:json.dump(r,f,indent=2)
    print(json.dumps({'status':r['status'],'sources':[{'source':s['source'],'r':s['r'],'Q':s['Q'],
      'relations':s['relations']} for s in reports]}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/f'audit_{PHASE}_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
