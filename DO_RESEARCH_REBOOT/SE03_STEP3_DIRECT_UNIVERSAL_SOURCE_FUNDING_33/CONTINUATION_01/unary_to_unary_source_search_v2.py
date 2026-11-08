"""Actual coupled source paths; test extension compatibility, not profile paths."""
import json,pickle,time,hashlib,collections
from pathlib import Path
from interior_projection_source_tools import *
B=Path(__file__).resolve().parent
def run(serial,cap):
    start=time.process_time();Z=json.loads((B/'native10_source_actions.json').read_text());S=Lift(Z);N=len(S.T);mir=Z['mirror'];blob=(B/'native10_B_modal_factored_debt.pkl').read_bytes();pin=json.loads((B/'native10_modal_oracle_independent_audit.json').read_text());assert hashlib.sha256(blob).hexdigest()==pin['input_sha256']['native10_B_modal_factored_debt.pkl'];O=pickle.loads(blob);del blob
    debt=lambda a,b:O['base'][b]+O['residual'].get(min(a*N+b,mir[a]*N+mir[b]),0)
    if serial==1:
        e=json.loads((B/'B_full_spectrum_result_02.json').read_text())['causal_edges'][0];a=fr(e['source_A']);p=e['private_key'];b=e['source_B_core_index'];w={'A':[a],'A_index':{a:0},'private':p,'best':{(0,b):0},'pred':{(0,b):None},'queue':collections.deque([(0,b)]),'queued':{(0,b)},'actions':{},'updates':[],'start_B':b,'start_old_debt':1,'edges':0,'counter':None,'mode':'genuine H1 KEEP packets only','maximum_layer':0}
    else:
        with (B/('unary_source_path_work_%02d.pkl'%(serial-1))).open('rb') as f:w=pickle.load(f)
    if serial==2:
        w['queue']=collections.deque(w['best']);w['queued']=set(w['best']);w['low1_expanded_cost']=dict(w['best']);w['actions2']={};w['mode']='ALL whole H1/H2 genuine packets, including every private/marked H1 DELETE helper'
    def unique(t):
        if not isnode(t):return t
        L,R=unique(t[1]),unique(t[2])
        if L is None or R is None:return None
        if t[0]==w['private']:
            if not isnode(L):return R
            if not isnode(R):return L
            return None
        return t[0],L,R
    def olddebt(a,b):
        t=unique(w['A'][a])
        return None if t is None else debt(S.idx[normalize(t,{2*k:k for k in range(1,11)})],b)
    def path_to(state):
        path=[];j=w['pred'][state]
        while j is not None:
            r=w['updates'][j];path.append(r['edge']);j=r['parent']
        return list(reversed(path))
    while w['queue'] and w['counter'] is None and time.process_time()-start<cap-3 and not w.get('resource_stop'):
        a,b=w['queue'].popleft();w['queued'].remove((a,b));As=w['A'][a];assert As[0]==2*S.T[b][0]
        if a not in w['actions']:
            options=[]
            for x in known(As):
                if x==w['private'] or x==As[0] or len(path(As,x))>2:continue
                At,H=S.access(As,x);assert H==1
                if At not in w['A_index']:w['A_index'][At]=len(w['A']);w['A'].append(At)
                options.append((x,w['A_index'][At]))
            w['actions'][a]=options
        def aid(At):
            if At not in w['A_index']:w['A_index'][At]=len(w['A']);w['A'].append(At)
            return w['A_index'][At]
        if a not in w['actions2']:
            options=[]
            for x in known(As):
                if x==w['private'] or x==As[0] or not 3<=len(path(As,x))<=4:continue
                At,H=S.access(As,x);assert H==2;options.append((x,aid(At),2,None))
            for y in known(As):
                if y==As[0] or len(path(As,y))>2:continue
                mid,Hy=S.access(As,y);assert Hy==1
                for x in known(mid):
                    if x in (w['private'],mid[0],As[0]) or len(path(mid,x))>2:continue
                    At,Hx=S.access(mid,x);assert Hx==1;options.append((x,aid(At),2,y))
            w['actions2'][a]=options
        options=list(w['actions2'][a])
        if (a,b) not in w['low1_expanded_cost'] or w['best'][a,b]<w['low1_expanded_cost'][a,b]:
            options += [(x,at,1,None) for x,at in w['actions'][a]]
            w['low1_expanded_cost'][a,b]=w['best'][a,b]
        for x,at,H,helper in options:
            bt=Z['destination'][b][x//2-1];q=Z['Q'][b][x//2-1];price=2*H-q;st=at,bt;candidate=w['best'][a,b]+price;w['edges']+=1
            if st in w['best'] and candidate>=w['best'][st]:continue
            edge={'source_A':As,'actual_A_target':w['A'][at],'source_B_core_index':b,'B_target_core_index':bt,'target_actual_key':x,'private_key':w['private'],'H':H,'Q':q,'price':price,'DELETE_helper':helper,'operation_word':([['D',helper]] if helper is not None else [])+[['K',x]]}
            j=len(w['updates']);w['updates'].append({'edge':edge,'parent':w['pred'][a,b]});w['pred'][st]=j;w['best'][st]=candidate
            targetD=olddebt(at,bt)
            if targetD is not None and candidate+targetD-w['start_old_debt']<0:
                w['counter']={'type':'OLD_UNARY_BOUNDARY_COMPATIBILITY_PATH','total_price':candidate,'D_start':w['start_old_debt'],'D_end':targetD,'edges':path_to(st)};break
            if candidate<-3:
                w['counter']={'type':'WIDTH_THREE_SOURCE_PATH','total_price':candidate,'edges':path_to(st)};break
            if st not in w['queued']:w['queue'].append(st);w['queued'].add(st)
            if len(w['best'])+len(O['residual'])+2*len(w['A'])+len(S.T)>1900000:w['resource_stop']='EXPLICIT_STATE_RESERVE';break
            assert len(w['updates'])<=4000000 
    with (B/('unary_source_path_work_%02d.pkl'%serial)).open('xb') as f:pickle.dump(w,f,protocol=5)
    z={'status':'ACTUAL_SOURCE_PATH_COUNTERCERTIFICATE_CANDIDATE' if w['counter'] else 'PARTIAL_SOURCE_PATH_DISCOVERY' if w['queue'] else 'COMPLETE_REACHABLE_LOW_PACKET_COMPONENT_CHECK','serial':serial,'mode':w['mode'],'A_shapes':len(w['A']),'coupled_states':len(w['best']),'stored_parent_updates':len(w['updates']),'edges_examined':w['edges'],'frontier':len(w['queue']),'lowest_price':min(w['best'].values()),'counter':w['counter'],'source_identity_instantiations_this_phase':S.calls,'source_queries':0,'source_engine_calls':0,'finite_no_failure_is_not_a_universal_proof':True,'principal_U33':'OPEN'}
    with (B/('unary_source_path_result_%02d.json'%serial)).open('x') as f:json.dump(z,f,indent=2)
    print(json.dumps({k:v for k,v in z.items() if k!='counter'}));print(json.dumps(w['counter']))
