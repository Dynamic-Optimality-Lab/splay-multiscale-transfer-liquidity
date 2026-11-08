"""SOURCE discovery for F(full B, FULL contraction-debt multiset).
Only nonnegative values and exact single-projection compatibility are assumed.
No optional HIGH envelopes or upper width on new non-singleton states.
Every source edge uses original primitive identities, not arbitrary graph rows.
"""
import json,pickle,time,hashlib,collections,itertools
from pathlib import Path
from interior_projection_source_tools import *
B=Path(__file__).resolve().parent
def run(serial,cap):
    start=time.process_time();Z=json.loads((B/'native10_source_actions.json').read_text());S=Lift(Z);T=S.T;N=len(T);mir=Z['mirror'];path=B/'native10_B_modal_factored_debt.pkl';raw=path.read_bytes();receipt=json.loads((B/'native10_modal_oracle_independent_audit.json').read_text());assert hashlib.sha256(raw).hexdigest()==receipt['input_sha256'][path.name];factored=pickle.loads(raw);pin=factored['old_sha256'];L=factored['residual'];baseline=factored['base'];del raw,factored
    def debt(a,b):return baseline[b]+L.get(min(a*N+b,mir[a]*N+mir[b]),0)
    corpus_path=B/'B_sensitive_contraction_work_02.pkl'
    with corpus_path.open('rb') as f:corpus=list(pickle.load(f)['edges'].values())
    if serial==1:
        w={'source_pin':pin,'features':[],'feature_index':{},'labels':[],'upper':[],'base':[],'pred':[],'depth':[],'edges':{},'outgoing':{},'updates':[],'pending':[],'contradiction':None,'causal_edges':[],'seed_cursor':0,'next_coefficient':0,'positive_stream_complete':False,'motifs':{},'projection_cache':{},'source_couplings':0}
    else:
        with (B/('B_full_spectrum_work_%02d.pkl'%(serial-1))).open('rb') as f:w=pickle.load(f)
        assert w['source_pin']==pin and w['contradiction'] is None
    def project_indices(t):
        t=fr(t)
        if t not in w['projection_cache']:w['projection_cache'][t]=tuple(S.idx[a] for a in projections(t,3))
        return w['projection_cache'][t]
    def feature(b,values):
        counts=tuple(values.count(d) for d in range(4));key=b,counts
        if key not in w['feature_index']:
            k=len(w['features']);w['feature_index'][key]=k;w['features'].append(key);singleton=len(values)==1;initial=values[0] if singleton else 0;w['labels'].append(initial);w['base'].append(initial);w['upper'].append(initial if singleton else None);w['pred'].append(None);w['depth'].append(0)
        assert len(L)+N+len(w['features'])+len(w['projection_cache'])+len(w['motifs'])<2000000
        return w['feature_index'][key]
    def extract(j):
        chain=[];lower=None;source=None
        while j is not None:
            u=w['updates'][j];chain.append(u['edge']);lower=u['source_label'];source=u['source_feature'];j=u['parent']
        chain.reverse();return chain,source,lower
    def propagate(seeds):
        q=collections.deque(seeds);pending=set(seeds)
        while q and w['contradiction'] is None:
            if time.process_time()-start>cap-2:w['pending']=list(q);return
            u=q.popleft();pending.remove(u)
            for v,e in w['outgoing'].get(u,{}).items():
                value=w['labels'][u]-e['price']
                if value<=w['labels'][v]:continue
                parent=w['pred'][u];depth=w['depth'][u]+1;rec={'edge':e,'source_feature':u,'target_feature':v,'source_label':w['labels'][u],'new_label':value,'parent':parent};w['updates'].append(rec);assert len(w['updates'])<=4000000;j=len(w['updates'])-1;w['pred'][v]=j;w['depth'][v]=depth;w['labels'][v]=value
                if w['upper'][v] is not None and value>w['upper'][v]:
                    chain,s,lo=extract(j);w['contradiction']={'type':'FROZEN_SINGLE_PROJECTION_UPPER','end_feature':v,'end_value':w['upper'][v],'required':value,'start_feature':s,'start_lower':lo};w['causal_edges']=chain;return
                if depth>=len(w['features']):
                    chain,s,lo=extract(j);nodes=[s]+[a['target_feature'] for a in chain];positions={};cycle=None
                    for pos,k in enumerate(nodes):
                        if k in positions:
                            part=chain[positions[k]:pos]
                            if sum(a['price'] for a in part)<0:cycle=part;break
                        positions[k]=pos
                    if cycle:w['contradiction']={'type':'NEGATIVE_FULL_SPECTRUM_FEATURE_CYCLE','price':sum(a['price'] for a in cycle)};w['causal_edges']=cycle;return
                if v not in pending:q.append(v);pending.add(v)
        w['pending']=list(q)
    def add(e):
        src=[debt(a,e['source_B_core_index']) for a in project_indices(e['source_A'])];dst=[debt(a,e['B_target_core_index']) for a in project_indices(e['actual_A_target'])];s,t=feature(e['source_B_core_index'],src),feature(e['B_target_core_index'],dst);key=s,t
        if key in w['edges'] and w['edges'][key]['price']<=e['price']:return
        e=e.copy();e.update(source_feature=s,target_feature=t,source_value_multiset=sorted(src),target_value_multiset=sorted(dst));w['edges'][key]=e;w['outgoing'].setdefault(s,{})[t]=e;assert len(w['edges'])<=5000000;propagate([s])
    if w['pending']:propagate(w['pending'])
    while w['seed_cursor']<len(corpus) and not w['pending'] and w['contradiction'] is None and time.process_time()-start<cap-2:
        add(corpus[w['seed_cursor']]);w['seed_cursor']+=1
    if w['seed_cursor']==len(corpus) and not w['pending'] and w['contradiction'] is None and not w['positive_stream_complete']:
        begin=w['next_coefficient']
        for j,(code,ds) in enumerate(itertools.islice(L.items(),begin,None),begin):
            if time.process_time()-start>cap-2 or w['contradiction'] or w['pending']:break
            a,b=divmod(code,N)
            for aa,bb in ((a,b),(mir[a],mir[b])):
                if T[aa][0]!=1:continue
                if aa not in w['motifs']:
                    g,A,R=T[aa]
                    if not isnode(R) or not isnode(R[1]):w['motifs'][aa]=None
                    else:
                        x=R[0];As=(2,scale(A),(3,'new_gap',scale(R)));At,h=S.access(As,2*x);assert h==1;successors=[]
                        for y in known(At):
                            if y==3 or y==At[0] or len(path(At,y))>2:continue
                            Att,hy=S.access(At,y);assert hy==1;successors.append((y,Att))
                        w['motifs'][aa]=x,As,At,successors
                m=w['motifs'][aa]
                if m is None:continue
                x,As,At,successors=m;bt=Z['destination'][bb][x-1];q=Z['Q'][bb][x-1];w['source_couplings']+=1
                add({'source_A':As,'actual_A_target':At,'private_key':3,'source_B_core_index':bb,'B_target_core_index':bt,'target_actual_key':2*x,'H':1,'Q':q,'price':2-q,'source_kind':'unary_RR'})
                if w['contradiction'] or w['pending']:break
                for y,Att in successors:
                    btt=Z['destination'][bt][y//2-1];qy=Z['Q'][bt][y//2-1];add({'source_A':At,'actual_A_target':Att,'private_key':3,'source_B_core_index':bt,'B_target_core_index':btt,'target_actual_key':y,'H':1,'Q':qy,'price':2-qy,'source_kind':'actual_successor'})
                    if w['contradiction'] or w['pending']:break
                if w['contradiction'] or w['pending']:break
            # Revisit this coefficient if its orientation/successor list was
            # interrupted. Duplicate source inequalities are safely reused.
            w['next_coefficient']=j if w['pending'] else j+1
        else:w['positive_stream_complete']=True
    # New source class: immediate-left anonymous branch at EVERY compatible B,
    # with no assumption that B has just arrived from the creator access.
    if w['positive_stream_complete'] and not w['pending'] and w['contradiction'] is None:
        groups=collections.defaultdict(list)
        for a,m in w['motifs'].items():
            if m is not None:groups[m[0]].append(a)
        assert sum(map(len,groups.values()))==3432
        for g in groups:groups[g].sort(key=lambda a:(len(project_indices(w['motifs'][a][2])),a))
        if 'branch_B_order' not in w:
            has_positive={b for (b,c),v in zip(w['features'],w['labels']) if sum(c)>1 and v>0};w['branch_B_order']=sorted(range(N),key=lambda b:(b not in has_positive,-Z['Q'][b][0],b));w['branch_cursor']=[0,0];w['branch_pairs_visited']=0
        bpos,apos=w['branch_cursor']
        while bpos<N and w['contradiction'] is None and not w['pending']:
            if time.process_time()-start>cap-2:break
            b=w['branch_B_order'][bpos];aa=groups.get(T[b][0],[])
            if apos>=len(aa):bpos+=1;apos=0;continue
            a=aa[apos];g,oldAs,sourceA,successors=w['motifs'][a];assert sourceA[0]==2*T[b][0]
            for y,At in successors:
                bt=Z['destination'][b][y//2-1];q=Z['Q'][b][y//2-1];add({'source_A':sourceA,'actual_A_target':At,'private_key':3,'source_B_core_index':b,'B_target_core_index':bt,'target_actual_key':y,'H':1,'Q':q,'price':2-q,'source_kind':'anonymous_branch_at_arbitrary_B'})
                if w['contradiction'] or w['pending']:break
            w['branch_pairs_visited']+=1
            if w['pending']:break
            apos+=1
        w['branch_cursor']=[bpos,apos];w['branch_stream_complete']=bpos==N
    with (B/('B_full_spectrum_work_%02d.pkl'%serial)).open('xb') as f:pickle.dump(w,f,protocol=5)
    result={'status':'FULL_B_AND_FULL_DEBT_MULTISET_FORMULA_REFUTATION_CANDIDATE' if w['contradiction'] else 'FULL_B_FULL_MULTISET_SOURCE_DISCOVERY_OPEN','serial':serial,'seed_cursor':w['seed_cursor'],'seed_total':len(corpus),'next_coefficient':w['next_coefficient'],'positive_stream_complete':w['positive_stream_complete'],'source_couplings':w['source_couplings'],'variables':len(w['features']),'edge_records':len(w['edges']),'updates':len(w['updates']),'maximum_discovery_label':max(w['labels'],default=0),'contradiction':w['contradiction'],'causal_edges':w['causal_edges'],'optional_HIGH_bounds_used':False,'upper_width_used_on_new_states':False,'exact_single_projection_compatibility':True,'source_identity_instantiations':S.calls,'source_queries':0,'source_engine_calls':0,'not_a_universal_passing_test':True,'principal_U33':'OPEN'}
    result.update(branch_pairs_visited=w.get('branch_pairs_visited',0),branch_cursor=w.get('branch_cursor'),branch_stream_complete=w.get('branch_stream_complete',False),oracle='independently checked lossless modal-B factor of unchanged old debt')
    with (B/('B_full_spectrum_result_%02d.json'%serial)).open('x') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='causal_edges'}))
