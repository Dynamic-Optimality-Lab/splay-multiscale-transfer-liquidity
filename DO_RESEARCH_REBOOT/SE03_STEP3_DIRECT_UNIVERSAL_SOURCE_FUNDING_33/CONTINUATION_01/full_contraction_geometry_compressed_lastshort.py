"""Does full contraction GEOMETRY support a nonnegative source debt extension?
Unlike the refuted multiset rule this keeps all labeled old BST contractions.
All edges are original source identities. A passing prefix is not a theorem.
"""
import json,pickle,time,hashlib,collections
from pathlib import Path
from interior_projection_source_tools import *
B=Path(__file__).resolve().parent
def run(serial,cap):
    start=time.process_time();Z=json.loads((B/'native10_source_actions.json').read_text());S=Lift(Z);N=len(S.T);mir=Z['mirror'];blob=(B/'native10_B_modal_factored_debt.pkl').read_bytes();pin=json.loads((B/'native10_modal_oracle_independent_audit.json').read_text());assert hashlib.sha256(blob).hexdigest()==pin['input_sha256']['native10_B_modal_factored_debt.pkl'];O=pickle.loads(blob);del blob
    debt=lambda a,b:O['base'][b]+O['residual'].get(min(a*N+b,mir[a]*N+mir[b]),0)
    with (B/('full_geometry_compressed_work_%02d.pkl'%(serial-1))).open('rb') as f:w=pickle.load(f)
    groups=collections.defaultdict(list)
    for b,t in enumerate(S.T):groups[t[0]].append(b)
    def pis(a):
        if a not in w['projections']:w['projections'][a]=tuple(sorted(S.idx[t] for t in projections(w['A'][a],w['private'])))
        return w['projections'][a]
    def feature(a,b):
        pi=pis(a)
        if len(pi)==1:return ('F',debt(pi[0],b))
        key=b,pi
        if key not in w['feature_index']:
            j=len(w['features']);w['features'].append(key);w['feature_index'][key]=j;w['lower'].append(0);w['upper'].append(None);w['upper_edge'].append(None);w['pred'].append(None);w['depth'].append(0)
        return w['feature_index'][key]
    def chain(j):
        result=[];source=None;lo=None
        while j is not None:
            rec=w['updates'][j];result.append(rec['edge']);source=rec['source_feature'];lo=rec['source_lower'];j=rec['parent']
        result.reverse();return result,source,lo
    def check_bound(v):
        if w['upper'][v] is not None and w['lower'][v]>w['upper'][v]:
            cc,ss,ll=chain(w['pred'][v]);endpoint=w['upper_edge'][v];assert endpoint is not None;cc.append(endpoint);w['counter']={'type':'FULL_LABELED_CONTRACTION_SET_FROZEN_UPPER','start_feature':ss,'start_lower':ll,'end_mutable_feature':v,'required':w['lower'][v],'source_upper_bound':w['upper'][v],'final_fixed_value':endpoint['target_frozen_value']};w['causal_edges']=cc
            assert sum(e['price'] for e in cc)+endpoint['target_frozen_value']-ll<0
    def propagate(seeds):
        todo=collections.deque(seeds);queued=set(seeds)
        while todo and w['counter'] is None:
            if time.process_time()-start>cap-8:w['pending']=list(todo);return
            u=todo.popleft();queued.remove(u)
            for v,e in w['outgoing'].get(u,{}).items():
                new=w['lower'][u]-e['price']
                if new<=w['lower'][v]:continue
                rec={'edge':e,'source_feature':u,'target_feature':v,'source_lower':w['lower'][u],'new_lower':new,'parent':w['pred'][u]};j=len(w['updates']);w['updates'].append(rec);w['lower'][v]=new;w['pred'][v]=j;w['depth'][v]=w['depth'][u]+1
                if new>3 and w['width3_first_candidate'] is None:
                    cc,ss,ll=chain(j);w['width3_first_candidate']={'start_feature':ss,'start_lower':ll,'end_feature':v,'required':new,'edges':cc}
                check_bound(v)
                if w['counter']:return
                if w['depth'][v]>=len(w['features']):
                    cc,ss,ll=chain(j);vertices=[ss]+[a['target_feature'] for a in cc];seen={}
                    for k,f in enumerate(vertices):
                        if f in seen and sum(a['price'] for a in cc[seen[f]:k])<0:
                            w['counter']={'type':'NEGATIVE_FULL_GEOMETRY_FEATURE_CYCLE','price':sum(a['price'] for a in cc[seen[f]:k])};w['causal_edges']=cc[seen[f]:k];return
                        seen[f]=k
                if v not in queued:queued.add(v);todo.append(v)
        w['pending']=list(todo)
    if w['pending']:propagate(w['pending'])
    apos,bpos,xpos=w['cursor'];stop=None
    while apos<len(w['A']) and not w['counter'] and not w['pending'] and time.process_time()-start<cap-8:
        As=w['A'][apos];g=As[0]//2
        if apos not in w['actions']:
            options=[]
            for x in known(As):
                if x in (w['private'],As[0]) or len(path(As,x))>2:continue
                At,H=S.access(As,x);assert H==1
                if At not in w['A_index']:w['A_index'][At]=len(w['A']);w['A'].append(At)
                options.append((x,w['A_index'][At]))
            w['actions'][apos]=options
        if apos not in w['actions2']:
            opts=[]
            if apos>=w['initial_H1_complete_A_count']:opts=[(x,at,1,None) for x,at in w['actions'][apos]]
            def aid(At):
                if At not in w['A_index']:w['A_index'][At]=len(w['A']);w['A'].append(At)
                return w['A_index'][At]
            for x in known(As):
                if x in (w['private'],As[0]) or not 3<=len(path(As,x))<=4:continue
                At,H=S.access(As,x);assert H==2;opts.append((x,aid(At),2,None))
            for y in known(As):
                if y==As[0] or len(path(As,y))>2:continue
                mid,H=S.access(As,y);assert H==1
                for x in known(mid):
                    if x in (w['private'],mid[0],As[0]) or len(path(mid,x))>2:continue
                    At,H=S.access(mid,x);assert H==1;opts.append((x,aid(At),2,y))
            w['actions2'][apos]=opts
        opts=w['actions2'][apos];bb=groups[g]
        if bpos>=len(bb):apos+=1;bpos=xpos=0;continue
        if xpos>=len(opts):bpos+=1;xpos=0;continue
        b=bb[bpos];x,at,H,helper=opts[xpos];bt=Z['destination'][b][x//2-1];q=Z['Q'][b][x//2-1];ss,tt=feature(apos,b),feature(at,bt);sf,tf=isinstance(ss,tuple),isinstance(tt,tuple);s0=None if sf else ss;t0=None if tf else tt;e={'source_A':As,'actual_A_target':w['A'][at],'private_key':w['private'],'source_B_core_index':b,'B_target_core_index':bt,'target_actual_key':x,'H':H,'Q':q,'price':2*H-q,'DELETE_helper':helper,'operation_word':([['D',helper]] if helper is not None else [])+[['K',x]],'source_feature':s0,'target_feature':t0,'source_contraction_indices':pis(apos),'target_contraction_indices':pis(at)};w['source_couplings']+=1
        if sf:e['source_frozen_value']=ss[1]
        if tf:e['target_frozen_value']=tt[1]
        if sf and tf:w['reused_unary_endpoint_packets']=w.get('reused_unary_endpoint_packets',0)+1
        elif sf:
            value=ss[1]-e['price']
            if value>w['lower'][t0]:
                rec={'edge':e,'source_feature':None,'target_feature':t0,'source_lower':ss[1],'new_lower':value,'parent':None};j=len(w['updates']);w['updates'].append(rec);w['lower'][t0]=value;w['pred'][t0]=j;w['depth'][t0]=1;check_bound(t0)
                if not w['counter']:propagate([t0])
        elif tf:
            bound=e['price']+tt[1]
            if w['upper'][s0] is None or bound<w['upper'][s0]:w['upper'][s0]=bound;w['upper_edge'][s0]=e
            check_bound(s0)
        else:
            key=s0,t0
            if key not in w['edges'] or e['price']<w['edges'][key]['price']:w['edges'][key]=e;w['outgoing'].setdefault(s0,{})[t0]=e;propagate([s0])
        xpos+=1
        if len(O['residual'])+len(w['features'])+3*len(w['A'])+len(S.T)>1850000:stop='LIVE_STATE_RESERVE';break
        if len(w['updates'])>3900000 or len(w['edges'])>4900000:stop='DAG_OR_EDGE_RESERVE';break
    w['cursor']=[apos,bpos,xpos]
    with (B/('full_geometry_compressed_work_%02d.pkl'%serial)).open('xb') as f:pickle.dump(w,f,protocol=5)
    result={'status':'FULL_CONTRACTION_GEOMETRY_FORMULA_REFUTATION_CANDIDATE' if w['counter'] else 'FULL_CONTRACTION_GEOMETRY_SOURCE_DISCOVERY_OPEN','serial':serial,'cursor':w['cursor'],'source_A_shapes':len(w['A']),'mutable_features_only':len(w['features']),'reused_unary_endpoint_packets':w.get('reused_unary_endpoint_packets',0),'stored_edges':len(w['edges']),'updates':len(w['updates']),'source_couplings':w['source_couplings'],'maximum_label':max(w['lower'],default=0),'resource_stop':stop,'counter':w['counter'],'causal_edges':w['causal_edges'],'first_width3_candidate':w['width3_first_candidate'],'scope':'F(actual full B, full labeled anchor-contraction SET, fixed one-private gap2 inventory), nonnegative, fixed old D10 only on singleton sets; no width or HIGH upper bound on new states','whole_LOW_helpers_included':True,'source_identity_instantiations':S.calls,'source_queries':0,'source_engine_calls':0,'principal_U33':'OPEN'}
    with (B/('full_geometry_compressed_result_%02d.json'%serial)).open('x') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k not in ('causal_edges','first_width3_candidate')}))
