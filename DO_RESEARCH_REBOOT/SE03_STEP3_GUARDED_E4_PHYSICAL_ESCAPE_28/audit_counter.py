"""Attack, rather than assume, the new catchment-forcing bridge.
Reuse saved source transitions to insert a closed NONDEEP native deficit
block before W199. Separate source object; old owners/source unchanged.
"""
import collections,importlib.util,json,pickle,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;OLD=P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time();depth_queries=0
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
C=load('C28_counter_source',OLD/'audit_construct.py')
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def fr(t):return tuple(fr(z) for z in t) if isinstance(t,list) else t
def pack(m):return [{'demand':d,'unit':u} for d,u in sorted(m.items())]
def main():
    global depth_queries
    c=json.loads((OLD/'aligned_source_and_owners.json').read_text());initial=fr(c['initial'])
    with (OLD/'product5_graph_cache.pkl').open('rb') as f:g=pickle.load(f)
    base=g['ids'][initial[1:]];adj,rev,states=g['adj'],g['rev'],g['states'];dc={}
    def q(i,k):
        global depth_queries
        t=states[i][0]
        if t not in dc:
            depth_queries+=1
            assert depth_queries+C.queries<4200 and time.process_time()-START<CAP-2
            v={}
            def dfs(t,d):
                if not isinstance(t,tuple):return
                v[t[0]]=d//2;dfs(t[1],d+1);dfs(t[2],d+1)
            dfs(t,0);dc[t]=v
        return dc[t][k]
    back={base:None};todo=collections.deque([base])
    while todo and len(back)<1000:
        z=todo.popleft()
        for i,k in rev[z]:
            if q(i,k)>5 or i in back:continue
            back[i]=(z,k);todo.append(i)
    forward={base:None};todo=collections.deque([base]);answer=None
    while todo and len(forward)<1000 and answer is None:
        i=todo.popleft()
        for k,z in adj[i]:
            qq=q(i,k)
            if qq>5:continue
            if qq==3 and k!=11 and z in back:answer=(i,k,z);break
            if z not in forward:forward[z]=(i,k);todo.append(z)
    if answer is None:
        out('catchment_source_control_search.json',{'status':'CACHED_COMPONENT_BOUNDED_CONTROL_NOT_FOUND_NOT_EXCLUSION','depth_queries':depth_queries});return
    i,k,z=answer;prefix=[];v=i
    while forward[v] is not None:v,t=forward[v];prefix.append(t)
    prefix.reverse();suffix=[];v=z
    while back[v] is not None:v,t=back[v];suffix.append(t)
    keep=prefix+[k]+suffix;fast=len(prefix);assert fast>0
    a,bf,be=initial;word=[];inserted=[]
    def add(mode,x):
        nonlocal a,bf,be
        assert C.queries+depth_queries<4200
        a,_,_=C.tr(a,x);word.append((mode,x))
        if mode=='K':
            bf,_,_=C.tr(bf,x)
            if x!=11:be,_,_=C.tr(be,x)
    def pad():
        root=a[0];child=(a[2] if C.p.node(a[2]) else a[1])[0]
        for j in range(4):add('D',child);add('D',root)
    for copy in range(4):
        for j,x in enumerate(keep):
            if j!=fast:pad()
            if j==fast-1:add('D',k)
            add('K',x)
            if j==fast:inserted.append(len(word))
        assert (bf,be)==initial[1:]
    inserted_length=len(word);word.extend(tuple(z) for z in c['period'])
    rows,end=C.replay(*initial,word);assert end==initial
    for r in rows:r['occurrence']+=572
    tags={name:t+inserted_length for name,t in c['tags'].items()};by={r['occurrence']:r for r in rows}
    for t in inserted:
        assert by[t+572]['a']==1 and by[t+572]['qF']==3
    assert len([r for r in rows if r['qF']==6])==1
    vv,pp,cp,tr=C.selection(rows);ate=[z for z in tr if z['birth'][0]==tags['e']]
    assert len(ate)==2 and {z['key'] for z in ate}=={5,9}
    sys.path.insert(0,str(P/'SE03_STEP2_CD6_FINAL_ASSEMBLY_14'))
    from cd6_allocator import allocate
    from branch_funding import build
    aux=[]
    for r in rows:
        mode='D' if r['mode']=='K' and r['target']==11 else r['mode'];bb,aa=r['before'],r['after']
        aux.append(dict(r,mode=mode,genuine_F=mode=='K' and bb[2][0]!=r['target'],qF=r['qE'],qE=0,
            before=(bb[0],bb[2],bb[2]),after=(aa[0],aa[2],aa[2])))
    f6=allocate(aux)['f'];raw=build([dict(r,occurrence=i+1) for i,r in enumerate(aux)])
    assert raw['full_cut_before_packet']==0 and f6[(tags['e'],4)]==(tags['v'],1,1)
    mm=C.L.macros(rows);full=C.L.build(rows,C.M);D,U=full['D'],full['U'];common={d:u for d,u in f6.items() if d in D}
    X=load('C28_counter_exchange',P/'SE03_STEP2_FULL_FUNDING_CLOSURE_10/physical_exchange.py');a_map=X.exchange(D,U,common,full['h0'])['allocation'];stages=[]
    def stage(n,h):
        nonlocal a_map
        prior=dict(a_map);r=C.L.augment_partial(D,U,a_map,h);a_map=r['allocation'];assert all(a_map[d]==u for d,u in prior.items())
        stages.append({'name':n,'comparison':pack(h),'prior':pack(prior),'after':pack(a_map)})
    hc=dict(full['h'])
    for z in cp:hc[tuple(z['demand'])]=tuple(z['unit'])
    ht=dict(hc)
    for z in tr:ht[tuple(z['origin'])]=ht.pop(tuple(z['birth']))
    hp=dict(ht);groups=collections.defaultdict(list)
    for z in tr:groups[z['birth_macro']].append(tuple(z['birth']))
    for mi,dd in sorted(groups.items()):
        free=[u for u in mm[mi]['units'] if u not in hp.values()]
        for d,u in zip(sorted(dd),free):hp[d]=u
    for name,h in (('leaf',full['h']),('creator',hc),('T19',ht),('own_tail',hp)):stage(name,h)
    jm=next(m for m in mm if tags['j'] in m['occurrences']);jd=jm['units'][2];hj=dict(hp);missing=[tuple(z['birth']) for z in ate if tuple(z['birth']) not in hj]
    assert jd not in hp.values()
    if missing:hj[missing[0]]=jd;stage('j_ordinal3',hj)
    prior=dict(a_map);residual=sorted(D-set(a_map));images=set(f6.values())|set(full['h0'].values())|set(hj.values());seeds=[]
    for m in mm:
        if any(r['mode']!='D' for r in m['rows'][:-1]):continue
        seeds.extend(u for u in m['units'][8:] if u not in images and u not in set(a_map.values()))
    assert len(seeds)>=len(residual);extra=[]
    for d,u in zip(residual,seeds):a_map[d]=u;extra.append({'demand':d,'unit':u})
    assert set(a_map)==D and len(set(a_map.values()))==len(D)
    timeline=[]
    for d,u in a_map.items():timeline.extend([((u[0],0,u[1],u[2]),d),((d[0],1,d[1],0),d)])
    active=set();peak=0
    for t,d in sorted(timeline):
        if d in active:active.remove(d)
        else:active.add(d);peak=max(peak,len(active))
    assert not active and peak<=25
    native={(r['occurrence'],q) for m in mm for r in m['rows'] for q in range(1,r['qF']+1)}-set(full['h0'])
    frameids={tags[name] for name in ('j','h','g','s','t','v','p','e')};outside=sorted(d for d in native if d[0] not in frameids)
    assert len(outside)>=5
    out('catchment_forcing_countercertificate.json',{'status':'EXACT_SEPARATE_GUARDED_SOURCE_REFUTES_ONE_FRAME_CATCHMENT_FORCING_PENDING_AUDIT',
        'source_id':'C28-nondeep-insertion-01','old_source_unchanged':True,'old_reaching_prefix':c['reaching_prefix'],
        'initial':initial,'period':word,'rows':rows,'tags':tags,'inserted_closed_B_KEEP_cycle':keep,'fast_index':fast,
        'inserted_copies':4,'inserted_native_deficit_occurrences':[t+572 for t in inserted],
        'actual_interval':[573,572+len(word)],'full_q6_count':1,'outside_natural_deficits':outside,
        'selected_at_e':ate,'creator_pairs':cp,'selected_transports':tr,'f6':pack(f6),'raw_cut':0,'raw_working':raw['working_units'],
        'raw_max_debt':raw['max_debt_on_period'],'policy_stages':stages,'prior_before_extra':pack(prior),'extra_payments':extra,
        'current_complete_a':pack(a_map),'endpoint_record_peak':peak,'A':sum(r['a'] for r in rows),'QF':sum(r['qF'] for r in rows),
        'counterclaim_refuted':'every guarded history partitions into catchments each with one such frame and <=3 outside natural deficits',
        'not_refuted':['U28 physical funding','frozen extension architecture','Coarse-Double','Dynamic Optimality'],
        'cached_source_edge_observable_queries':depth_queries,'new_source_queries':C.queries})
    print(json.dumps({'status':'CATCHMENT_FORCING_SOURCE_COUNTEREXAMPLE','KEEP_cycle':keep,'length':len(word),
        'outside':len(outside),'q6':1,'selected2':True,'funding_peak':peak,'new_queries':C.queries+depth_queries}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_counter_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,
        'source_engine_calls':C.calls,'source_queries':C.queries+depth_queries})
