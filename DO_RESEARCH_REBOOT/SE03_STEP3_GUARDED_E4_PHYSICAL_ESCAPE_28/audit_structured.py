"""Attack a missing source bridge: is a ninth-unit j reserve forced?
Search a separate exact source; never alter W199 or its successful map.
"""
import collections,heapq,importlib.util,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;OLD=P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
C=load('C28_source_structured',OLD/'audit_construct.py');entry=json.loads((B/'entry.json').read_text())
previous=sum(json.loads(p.read_text()).get('source_queries',0) for p in B.glob('run_*_result.json'))
LIMIT=min(155000,entry['remaining_conservative_queries']-previous-10000)
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def fr(x):return tuple(fr(z) for z in x) if isinstance(x,list) else x
def pack(m):return [{'demand':d,'unit':u} for d,u in sorted(m.items())]
def goal(t):
    try:return t[0]==1 and t[2][0]==13 and t[2][1][0]==11 and t[2][1][1][0]==7
    except (TypeError,IndexError):return False
def main():
    data=json.loads((OLD/'construction_candidate.json').read_text());body=[tuple(z) for z in data['period']];jidx=data['tags']['j']-1;a=jidx
    while a and body[a-1][0]=='D':a-=1
    origin=fr(data['rows'][a]['before'][0]);dist={origin:0};parent={origin:None};queue=[(0,0,origin)];serial=0;winner=None
    while queue:
        cost,_,t=heapq.heappop(queue)
        if cost!=dist[t]:continue
        if goal(t):winner=t;break
        if C.queries>=LIMIT-2000 or time.process_time()-START>CAP-3:break
        for key in range(1,14):
            if key==t[0]:continue
            z,path,ev=C.tr(t,key);nc=cost+len(ev)
            if nc>=dist.get(z,1000000):continue
            dist[z]=nc;parent[z]=(t,key);serial+=1;heapq.heappush(queue,(nc,serial,z))
    if winner is None:
        out('short_j_search.json',{'status':'BOUNDED_SEARCH_NO_WITNESS_NOT_EXCLUSION','states':len(dist),'queries':C.queries});return
    route=[];t=winner
    while parent[t] is not None:t,key=parent[t];route.append(key)
    route.reverse();newbody=body[:a]+[('D',x) for x in route]+body[jidx:]
    initial=(fr(data['initial_A']),fr(data['initial_BF']),fr(data['initial_BE']));rows,end=C.replay(*initial,newbody);assert end==initial
    jnew=a+len(route)+1;tags0={k:(v if v<=a else v-(jidx-a)+len(route)) for k,v in data['tags'].items()}
    assert tags0['j']==jnew
    sys.path.insert(0,str(P/'SE03_STEP2_CD6_FINAL_ASSEMBLY_14'))
    from cd6_allocator import allocate
    from branch_funding import build
    def auxiliary(rr):
        aux=[]
        for r in rr:
            mode='D' if r['mode']=='K' and r['target']==11 else r['mode'];bb,aa=r['before'],r['after']
            aux.append(dict(r,mode=mode,genuine_F=mode=='K' and bb[2][0]!=r['target'],qF=r['qE'],qE=0,
                before=(bb[0],bb[2],bb[2]),after=(aa[0],aa[2],aa[2])))
        return aux
    raw0=build(auxiliary(rows));cut=raw0['packet_receipt'][0]['occurrences'][0]-1;T=len(newbody)
    reach=[tuple(z) for z in data['original_reaching_prefix']]+newbody*2+newbody[:cut]
    _,start=C.replay(C.V,C.V,C.V,reach);word=newbody[cut:]+newbody[:cut];rows,end=C.replay(*start,word);assert end==start;base=len(reach)
    for r in rows:r['occurrence']+=base
    def tau(t):return base+(t-cut if t>cut else T+t-cut)
    tags={k:tau(v) for k,v in tags0.items()};aux=auxiliary(rows);small=allocate(aux);f6=small['f'];v,profile,cp,tr=C.selection(rows)
    ate=[z for z in tr if z['birth'][0]==tags['e']];assert len(ate)==2 and {z['key'] for z in ate}=={5,9}
    assert f6[(tags['e'],4)]==(tags['v'],1,1)
    mm=C.L.macros(rows);jm=next(m for m in mm if tags['j'] in m['occurrences']);Hj=jm['H']
    assert all(next(m['H'] for m in mm if tags[k] in m['occurrences'])==1 for k in ('h','g','s','t','v','p','e'))
    full=C.L.build(rows,C.M);D,U=full['D'],full['U'];locked={d:u for d,u in f6.items() if d in D}
    X=load('C28_physical_exchange',P/'SE03_STEP2_FULL_FUNDING_CLOSURE_10/physical_exchange.py');a_map=X.exchange(D,U,locked,full['h0'])['allocation'];stages=[]
    def stage(name,h):
        nonlocal a_map
        old=dict(a_map);z=C.L.augment_partial(D,U,a_map,h);a_map=z['allocation'];assert all(a_map[d]==u for d,u in old.items())
        stages.append({'name':name,'comparison':pack(h),'before':pack(old),'after':pack(a_map)})
    hc=dict(full['h'])
    for z in cp:hc[tuple(z['demand'])]=tuple(z['unit'])
    ht=dict(hc)
    for z in tr:ht[tuple(z['origin'])]=ht.pop(tuple(z['birth']))
    hp=dict(ht);bg=collections.defaultdict(list)
    for z in tr:bg[z['birth_macro']].append(tuple(z['birth']))
    for mi,dd in sorted(bg.items()):
        free=[u for u in mm[mi]['units'] if u not in hp.values()]
        for d,u in zip(sorted(dd),free):hp[d]=u
    for name,h in (('leaf',full['h']),('protected_creator',hc),('T19',ht),('own_tail',hp)):stage(name,h)
    jd=jm['units'][2];assert jd not in hp.values();hj=dict(hp);births=[tuple(z['birth']) for z in ate if tuple(z['birth']) not in hj]
    if births:hj[births[0]]=jd;stage('j_ordinal3',hj)
    partial=dict(a_map);residual=sorted(D-set(a_map));suppliers=[];occupied=set(a_map.values());images=set(f6.values())|set(full['h0'].values())|set(hj.values())
    for m in mm:
        if any(r['mode']!='D' for r in m['rows'][:-1]):continue
        for u in m['units'][8:]:
            if u not in images and u not in occupied:suppliers.append(u)
    assert len(suppliers)>=len(residual)
    extra=[]
    for d,u in zip(residual,suppliers):a_map[d]=u;extra.append({'demand':d,'unit':u})
    assert set(a_map)==D and len(set(a_map.values()))==len(D) and a_map[(tags['e'],4)]==(tags['v'],1,1)
    events=[]
    for d,u in a_map.items():events.extend([((u[0],0,u[1],u[2]),d),((d[0],1,d[1],0),d)])
    active=set();peak=0
    for point,d in sorted(events):
        if d in active:active.remove(d)
        else:active.add(d);peak=max(peak,len(active))
    assert not active and peak<=25
    by={r['occurrence']:r for r in rows};shadow,path,events=C.tr(by[tags['h']]['after'][0],7)
    assert shadow==by[tags['e']]['after'][0] and len(events)==2
    out('short_j_source_certificate.json',{'status':'PRODUCER_EXACT_SEPARATE_GUARDED_SOURCE_FULL_OWNER_RECEIPT_PENDING_AUDIT',
        'source_id':'C28-short-j-01','body':newbody,'reaching_prefix':reach,'period':word,'initial':start,'rows':rows,'tags':tags,
        'actual_interval':[base+1,base+T],'j_delete_route':route,'H_j':Hj,'j_A_endpoint':winner,'cut':cut,
        'f6':pack(f6),'raw6_max_debt':raw0['max_debt_on_period'],'raw6_working_peak':raw0['working_units'],
        'full_natural':pack(full['h0']),'leaf_comparison':pack(full['h']),'common':pack(locked),
        'creator_pairs':cp,'selected_transports':tr,'selected_at_e':ate,'policy_stages':stages,
        'partial_before_extra':pack(partial),'extra_payments':extra,'final_full_a':pack(a_map),'full_endpoint_peak':peak,
        'scalar_A':sum(r['a'] for r in rows),'scalar_QF':sum(r['qF'] for r in rows),
        'source_search_states':len(dist),'source_queries':C.queries,
        'refutation_scope':'a ninth A-bit is not forced at j if H_j<5; no refutation of U28 or original Coarse-Double'})
    print(json.dumps({'status':'NEW_SHORT_J_FULL_SOURCE','H_j':Hj,'j_route':route,'length':T,'selected':ate,
        'new_extra_payments':extra,'peak':peak,'queries':C.queries,'states':len(dist)}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_structured_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,
        'source_engine_calls':C.calls,'source_queries':C.queries})
