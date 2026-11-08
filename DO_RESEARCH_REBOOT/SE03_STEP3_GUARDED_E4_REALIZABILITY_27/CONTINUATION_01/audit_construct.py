"""Bounded PRODUCER search for one exact guarded source, never a universal test."""
import collections,importlib.util,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent.parent
CAP=float(sys.argv[1]);START=time.process_time();calls=queries=0
def mod(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
p=mod('source27c',P/'SE03_STEP2_COLD_NEG2_01/source_model.py')
L=mod('leaf27c',P/'SE03_STEP3_UNIFORM_DONOR_GROUPING_15/leaf_channels.py')
W=mod('watched27c',P/'SE03_STEP3_RR7_CREATOR_MARKED_FRONTIERS_18/audit_marked.py')
M=set(range(1,14,2));E=M-{11};original_trace=p.trace;original_path=p.path
def check():
    if queries>=1000000 or time.process_time()-START>=CAP-.6:raise TimeoutError('bounded producer limit')
def path(t,x):
    global queries
    queries+=1
    if queries%512==0:check()
    return original_path(t,x)
def tr(t,x):
    global calls
    calls+=1;check();return original_trace(t,x)
p.path=path;p.trace=tr
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def N(k,l=None,r=None):return (k,l,r)
def fill(t,c=None):
    if c is None:c=[0]
    if t is None:v='F'+str(c[0]);c[0]+=1;return v
    return (t[0],fill(t[1],c),fill(t[2],c))
S=fill(N(1,None,N(4,N(2,None,N(3)),N(13,N(6,N(5),N(8,N(7),N(10,N(9),N(12,N(11)))))))))
V=p.vine(13)
def signature(t):
    par,ch=L.marked_tree(t,M)
    return {x:tuple(ch[x]) for x in M}
def ss(t,x):
    w=path(t,x)
    return bool(w) and len(w)%2==0 and all(w[j:j+2] in ('LL','RR') for j in range(0,len(w),2))
def moves(t):
    for x in sorted(M-{t[0]}):
        if ss(t,x):
            z,w,ev=tr(t,x)
            if all(e['G'] in M and e['P'] not in M for e in ev):yield x,z
def guard_goal(t):
    ch=signature(t);root=t[0]
    if root not in {3,5,7,9} or set(ch[root])!={1,11,13,*([x for x in ch[root] if x not in {1,11,13}])}:return None
    if len(ch[root])!=4 or any(ch[x] for x in (1,11,13)):return None
    chain=[root];u=[x for x in ch[root] if x not in {1,11,13}]
    if len(u)!=1:return None
    y=u[0]
    while True:
        chain.append(y)
        if not ch[y]:break
        if len(ch[y])!=1:return None
        y=ch[y][0]
    if set(chain)!={3,5,7,9} or chain[-1] not in (3,5):return None
    z=t
    for x,q in zip((13,1,13,11,1,13,1,chain[-1]),(1,2,1,3,1,2,1,6)):
        w=path(z,x)
        if len(w)!=2*q or any(w[j:j+2] not in ('LL','RR') for j in range(0,len(w),2)):return None
        z,_,_=tr(z,x)
    return chain[-1]
def inverse(a):
    if not a:return []
    return [a[0]]+[y for z in inverse(a[1:]) for y in (z,a[0])]
def build(route,x):
    a=V;b=S;word=[];kept=[];tag={}
    def add(mode,k,label=None):
        nonlocal a,b
        if label:tag[label]=len(word)+1
        before=b;a,_,_=tr(a,k);word.append((mode,k))
        if mode=='K':
            w=path(b,k)
            assert not w or (len(w)%2==0 and all(w[j:j+2] in ('LL','RR') for j in range(0,len(w),2)))
            ancestors=[p.at(b,w[:j])[0] for j in range(0,len(w),2)]
            b,_,_=tr(b,k);kept.append((k,ancestors))
    def pad():
        r=a[0];child=a[2] if p.node(a[2]) else a[1];y=child[0]
        for _ in range(2):add('D',y);add('D',r)
    def deletions(kk):
        for k in kk:add('D',k)
    add('K',13)
    deletions(range(13,0,-1))
    deletions((12,1,11,1,13,1,12,1,11,13,1))
    deletions((7,5,11,13,1))
    # Source preparation, not an arbitrarily stitched A tree.
    assert a[0]==1 and a[2][0]==11 and a[2][1][0]==5 and a[2][1][2][0]==7 and a[2][1][2][2][0]==9
    add('K',1,'prep_end')
    for k in (5,7,9):add('K',k,'zero'+str(k))
    for k in route:pad();add('K',k)
    assert guard_goal(b)==x
    deletions(range(13,0,-1));deletions((12,1,11,1,13,1,12,1,11,13,1))
    if x==3:deletions((3,1,13,11,1,12,1,11,13,1))
    for label,k in zip(('j','h','g','s','t','v','p','e'),(13,1,13,11,1,13,1,x)):add('K',k,label)
    before_return=list(kept)
    for k,anc in reversed(before_return):
        for y in inverse(anc):pad();add('K',y)
    assert b==S
    deletions(range(13,0,-1));assert a==V
    return word,tag
def erase_transition(t,word):
    for mode,x in word:
        if mode=='K' and x!=11:t,_,_=tr(t,x)
    return t
def replay(a,b,e,word):
    rows=[]
    for occ,(mode,x) in enumerate(word,1):
        before=(a,b,e);a,pa,ea=tr(a,x);pb=pe='';eb=ee=[];gen=mode=='K' and x!=b[0]
        if mode=='K':b,pb,eb=tr(b,x)
        if mode=='K' and x!=11:e,pe,ee=tr(e,x)
        rows.append({'occurrence':occ,'mode':mode,'target':x,'genuine_F':gen,'A_path':pa,'BF_path':pb,'BE_path':pe,
            'A_events':ea,'BF_events':eb,'BE_events':ee,'a':len(ea),'qF':sum(q['kind']=='DOUBLE' for q in eb),
            'qE':sum(q['kind']=='DOUBLE' for q in ee),'before':before,'after':(a,b,e)})
    return rows,(a,b,e)
def selection(rows):
    v=L.build(rows,M);pp=W.analyze('C27 candidate',rows);groups=collections.defaultdict(list)
    by={t:i for i,m in enumerate(v['macros']) for t in m['occurrences']}
    mm=L.macros(rows);h=dict(v['h']);pairs=[]
    for c in pp['claims']:groups[by[c['creator']['source_occurrence']]].append(c)
    for mi,cs in groups.items():
        m=v['macros'][mi];tail=mm[mi]['units'][min(2*m['H'],len(m['branch'])+m['z']):]
        cs=sorted(cs,key=lambda c:tuple(c['frontier']));n=min(len(cs),len(tail))
        for c,u in zip(cs[:n],tail[-n:] if n else []):
            d=tuple(c['frontier']);assert d not in h and u not in h.values();h[d]=u;pairs.append({'demand':d,'unit':u,'creator_macro':mi})
    unpaid={tuple(c['frontier']) for c in pp['claims'] if tuple(c['frontier']) not in h}
    transported=[]
    for d in sorted(unpaid):
        i=next(i for i,m in enumerate(v['macros']) if d in m['branch_unpaid'])
        ch=next(ch for ch in v['channels'] if ch['death_macro']==i and ch['marked_key']==v['macros'][i]['target'])
        transported.append({'origin':d,'key':ch['marked_key'],'birth':ch['demand'],'death_macro':i,'birth_macro':ch['birth_macro']})
    return v,pp,pairs,transported
def main():
    assert p.labels(p.core(S,M))==set(range(1,14))
    start=S
    for x in (5,7,9):
        par,ch=L.marked_tree(start,M);u=par[x];anc=[]
        while u is not None:anc.append(u);u=par[u]
        assert len(anc)==2 and all(len(ch[u])>=2 for u in anc) and not ch[x] and ss(start,x)
        start,_,_=tr(start,x)
    parents={start:None};queue=collections.deque([start]);goals=[]
    while queue and len(parents)<12000 and len(goals)<15:
        check();t=queue.popleft();goal=guard_goal(t)
        if goal:
            route=[];z=t
            while parents[z] is not None:z,k=parents[z];route.append(k)
            goals.append((route[::-1],goal,t))
        for k,z in moves(t):
            if z in parents:continue
            ch=signature(z)
            if not ch[7] or not ch[9]:continue
            parents[z]=(t,k);queue.append(z)
    out('B_source_routes.json',{'status':'CONCRETE_SOURCE_ROUTES_NOT_UNIVERSAL_CERTIFICATE','source_start':S,
        'after_three_zeros':start,'states_seen':len(parents),'search_queue_exhausted':not queue,
        'goals':[{'route':a,'x':x,'tree':t} for a,x,t in goals]})
    trials=[]
    for gi,(route,x,t) in enumerate(goals):
        check();word,tags=build(route,x);states={};e=S;history=[]
        while e not in states and len(history)<30:
            states[e]=len(history);history.append(e);e=erase_transition(e,word)
        if e not in states:
            trials.append({'goal':gi,'route':route,'x':x,'word':word,'status':'ERASED_RECURRENCE_NOT_FOUND_WITHIN30'});continue
        u=states[e];ell=len(history)-u;period=word*ell;rows,end=replay(V,S,e,period)
        assert end==(V,S,e)
        target=[rows[tags[k]-1] for k in ('v','p','e')]
        ke=len(p.labels(p.core(e,E)));qs=[r['qE'] for r in target]
        trial={'goal':gi,'route':route,'x':x,'word':word,'tags':tags,'u':u,'L':ell,'auxiliary_core':ke,'critical_qE':qs,
            'critical_e_depth':len(target[-1]['BE_path']),'status':'NOT_GUARDED_COSTS'}
        trials.append(trial)
        print(json.dumps({k:trial[k] for k in ('goal','route','x','u','L','auxiliary_core','critical_qE','critical_e_depth')}),flush=True)
        if qs!=[1,1,4] or ke not in (9,10,11):continue
        for j in range(ell):
            for k in ('h','g','s','t','v','p','e'):assert rows[j*len(word)+tags[k]-1]['a']==1
        v,pp,pairs,transport=selection(rows)
        recovered=[q for q in transport if q['birth'][0]==tags['e']]
        if len(recovered)!=2 or {q['key'] for q in recovered}!={7,9}:
            trial['status']='SELECTION_GUARD_FAILED';trial['transported']=transport;continue
        assert {q['birth'][1] for q in recovered}<={1,2,3}
        trial['status']='GUARDED_SOURCE_CANDIDATE_FOUND_PENDING_BACKEND_AND_INDEPENDENT_AUDIT'
        out('construction_candidate.json',{'status':trial['status'],'original_common_tree':S,'original_reaching_prefix':[('D',k) for k in range(13,0,-1)]+word*u,
            'body':word,'u':u,'L':ell,'period':period,'initial_A':V,'initial_BF':S,'initial_BE':e,'rows':rows,
            'tags':tags,'route':route,'x':x,'full_marks':sorted(M),'erased':11,'auxiliary_core':ke,
            'creator_pairs':pairs,'creator_claims':pp['claims'],'selected_transports':transport,'selected_at_e':recovered,
            'physical_owner_receipt':'NOT_YET_CONSTRUCTED','independent_audit':False})
        break
    out('construction_trials.json',{'status':'BOUNDED_CONSTRUCTION_LEDGER','trials':trials,'source_engine_calls':calls,'source_queries':queries})
    print(json.dumps({'status':'CONSTRUCTION_FINISHED','goals':len(goals),'trials':len(trials),
        'candidate_written':(B/'construction_candidate.json').exists(),'source_engine_calls':calls,'source_queries':queries}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_construct_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,
        'source_engine_calls':calls,'source_queries':queries,'mathematical_scope':'one original witness construction, no finite universal proof'})
