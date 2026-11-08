"""Exact sparse LOW source discovery. Not a complete source funding proof."""
import collections,hashlib,json,pickle,time
from pathlib import Path
from interior_projection_source_tools import Lift,known,isnode,path,projections
B=Path(__file__).resolve().parent
def pre(t):return () if not isnode(t) else (t[0],)+pre(t[1])+pre(t[2])
def run(serial,cap):
    start=time.process_time();Z=json.loads((B/'native10_source_actions.json').read_text());S=Lift(Z);N=len(S.T);mir=Z['mirror'];raw=(B/'native10_B_modal_factored_debt.pkl').read_bytes();pin=json.loads((B/'native10_modal_oracle_independent_audit.json').read_text());assert hashlib.sha256(raw).hexdigest()==pin['input_sha256']['native10_B_modal_factored_debt.pkl'];O=pickle.loads(raw);del raw
    def D(a,b):return O['base'][b]+O['residual'].get(min(a*N+b,mir[a]*N+mir[b]),0)
    with (B/('full_geometry_sparse_work_%02d.pkl'%(serial-1))).open('rb') as f:w=pickle.load(f)
    assert json.loads((B/'sparse_source_conversion_independent_audit.json').read_text())['status']=='PASS_EXACT_SPARSE_SOURCE_PREFIX_CONVERSION'
    geom={pre(t):i for i,t in enumerate(w['A'])};assert len(geom)==len(w['A'])
    fixed=w.setdefault('unary_projection',{});groups=collections.defaultdict(list)
    for b,t in enumerate(S.T):groups[t[0]].append(b)
    def aid(t):
        key=pre(t)
        if key not in geom:
            a=len(w['A']);geom[key]=a;w['A_index'][t]=a;w['A'].append(t)
        return geom[key]
    def unary(a):
        if a not in fixed:
            t=S.sub(w['A'][a],w['private'])
            if isnode(t[1]) and isnode(t[2]):fixed[a]=None
            else:
                pi=projections(w['A'][a],w['private']);assert len(pi)==1;fixed[a]=S.idx[pi[0]]
        return fixed[a]
    def value(a,b):
        v=unary(a)
        return D(v,b) if v is not None else w['lower'].get(a*N+b,0)
    def actions(a,all_h1=False):
        As=w['A'][a]
        if a not in w['actions']:
            one=[]
            for x in known(As):
                if x in (w['private'],As[0]) or len(path(As,x))>2:continue
                At,H=S.access(As,x);assert H==1;one.append((x,aid(At)))
            w['actions'][a]=one
        if a not in w['actions2']:
            two=[]
            if a>=w['initial_H1_complete_A_count']:two=[(x,at,1,None) for x,at in w['actions'][a]]
            for x in known(As):
                if x in (w['private'],As[0]) or not 3<=len(path(As,x))<=4:continue
                At,H=S.access(As,x);assert H==2;two.append((x,aid(At),2,None))
            for y in known(As):
                if y==As[0] or len(path(As,y))>2:continue
                mid,H=S.access(As,y);assert H==1
                for x in known(mid):
                    if x in (w['private'],mid[0],As[0]) or len(path(mid,x))>2:continue
                    At,H=S.access(mid,x);assert H==1;two.append((x,aid(At),2,y))
            w['actions2'][a]=two
        result=w['actions2'][a]
        if all_h1 and a<w['initial_H1_complete_A_count']:return [(x,at,1,None) for x,at in w['actions'][a]]+result
        return result
    def chain(j):
        rows=[]
        while j is not None:r=w['updates'][j];rows.append(r);j=r['parent']
        rows.reverse();return rows
    pending=collections.deque(w['pending']);queued=set(pending);regenerated=0;fresh_rows=0;stop=None
    def edge(a,b,opt):
        x,at,H,helper=opt;bt=Z['destination'][b][x//2-1];q=Z['Q'][b][x//2-1]
        # Different free-hanger spellings with the same known-key skeleton
        # are aliases under the proved full-Pi geometry lemma.
        e={'source_A':w['A'][a],'actual_A_target':w['A'][at],'private_key':w['private'],'source_B_core_index':b,'B_target_core_index':bt,'target_actual_key':x,'H':H,'Q':q,'price':2*H-q,'DELETE_helper':helper,'operation_word':([['D',helper]] if helper is not None else [])+[['K',x]]}
        return e,at,bt
    def check(a,b,opt):
        e,at,bt=edge(a,b,opt);sf=unary(a);tf=unary(at);sv=value(a,b);requested=sv-e['price'];sc=None if sf is not None else a*N+b;tc=None if tf is not None else at*N+bt
        if sf is not None:e['source_frozen_value']=sv
        if tf is not None:
            tv=D(tf,bt);e['target_frozen_value']=tv
            if sf is not None:w['reused_unary_endpoint_packets']+=1;return
            if requested>tv:
                cc=chain(w['pred'].get(sc));w['counter']={'type':'SPARSE_FULL_GEOMETRY_FROZEN_UPPER_FAILURE','source_code':sc,'source_lower':sv,'target_frozen_value':tv,'required':requested};w['causal_edges']=[r['edge'] for r in cc]+[e]
            return
        old=w['lower'].get(tc,0)
        if requested<=old:return
        r={'edge':e,'source_code':sc,'target_code':tc,'source_lower':sv,'new_lower':requested,'parent':None if sc is None else w['pred'].get(sc)};j=len(w['updates']);w['updates'].append(r);w['lower'][tc]=requested;w['pred'][tc]=j
        if requested>3 and w['width3_first_candidate'] is None:w['width3_first_candidate']={'required':requested,'target_code':tc,'derivation':chain(j)}
        if requested>3:
            cc=chain(j);seen={};prices=[0]
            for k,r0 in enumerate(cc):
                c=r0['source_code'];prices.append(prices[-1]+r0['edge']['price'])
                if c is not None and c in seen and prices[k]-prices[seen[c]]<0:
                    w['counter']={'type':'NEGATIVE_SPARSE_FULL_GEOMETRY_CYCLE','price':prices[k]-prices[seen[c]]};w['causal_edges']=[r1['edge'] for r1 in cc[seen[c]:k]];return
                if c is not None:seen[c]=k
        if tc not in queued:queued.add(tc);pending.append(tc)
    def caps():
        if len(O['residual'])+len(w['lower'])+3*len(w['A'])+N>1850000:return 'LIVE_STATE_RESERVE'
        if len(w['updates'])>3900000:return 'DAG_RESERVE'
        if sum(map(len,w['actions2'].values()))+len(w['updates'])>4900000:return 'REGENERATED_ACTION_CACHE_RESERVE'
        return None
    ap,bp,xp=w['cursor'];iterations=0
    while not w['counter'] and time.process_time()-start<cap-4:
        if pending:
            c=pending.popleft();queued.remove(c);a,b=divmod(c,N)
            for opt in actions(a,True):
                check(a,b,opt);regenerated+=1
                if w['counter']:break
        else:
            if ap>=len(w['A']):w['source_generation_complete']=True;break
            opts=actions(ap);bb=groups[w['A'][ap][0]//2]
            if bp>=len(bb):ap+=1;bp=xp=0;continue
            if xp>=len(opts):bp+=1;xp=0;continue
            check(ap,bb[bp],opts[xp]);xp+=1;fresh_rows+=1;w['source_couplings']+=1
        iterations+=1
        if iterations%1024==0:
            stop=caps()
            if stop:break
    w['cursor']=[ap,bp,xp];w['pending']=list(pending);w['regenerated_source_rows']=w.get('regenerated_source_rows',0)+regenerated;w['schema_alias_rule']='identical known-key preorder with arbitrary rigid ordered hanger renaming'
    with (B/('full_geometry_sparse_work_%02d.pkl'%serial)).open('xb') as f:pickle.dump(w,f,protocol=5)
    result={'status':'SPARSE_FULL_GEOMETRY_SOURCE_REFUTATION_CANDIDATE' if w['counter'] else 'SPARSE_FULL_GEOMETRY_SOURCE_DISCOVERY_OPEN','serial':serial,'cursor':w['cursor'],'A_shapes':len(w['A']),'positive_labels':len(w['lower']),'causal_records':len(w['updates']),'pending_positive_source_rows':len(pending),'source_couplings':w['source_couplings'],'new_seed_rows':fresh_rows,'new_regenerated_source_rows':regenerated,'total_regenerated_source_rows':w['regenerated_source_rows'],'maximum_label':max(w['lower'].values(),default=0),'source_generation_complete':w['source_generation_complete'],'counter':w['counter'],'causal_edges':w['causal_edges'],'first_width3_candidate':w['width3_first_candidate'],'resource_stop':stop,'source_identity_instantiations':S.calls,'source_queries':0,'source_engine_calls':0,'principal_U33':'OPEN'}
    with (B/('full_geometry_sparse_result_%02d.json'%serial)).open('x') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k not in ('causal_edges','first_width3_candidate')}))
