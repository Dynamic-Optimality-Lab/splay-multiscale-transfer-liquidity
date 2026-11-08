"""Bounded exact-source adversarial starts from NEW negative-two source preparations.
Every start is embedded in an explicitly closed original Gamma-type word.
Failure to find a return in this finite action family is not a universal proof.
"""
import collections,functools,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;OLD=B.parent/'SE03_STEP2_COLD_NEG2_01';PREV=B.parent/'SE03_STEP2_FORCED_ZERO_INCOMING_02'
sys.path.insert(0,str(OLD))
from source_model import trace,core,labels,replay,packets,charts,SCAN,vine
M=(1,3,5,7,9,11);account={'source_engine_calls':0,'new_finite_tests':0};started=time.process_time();CAP=min(25,float(sys.argv[1])-3)
states_total=proposals=0
class Bound(Exception):pass
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def freeze(v):return tuple(freeze(q) for q in v) if isinstance(v,list) else v
def limit():
    if time.process_time()-started>=CAP or states_total>=10000 or proposals>=100000 or account['source_engine_calls']>=500000:raise Bound()
@functools.lru_cache(maxsize=60000)
def move(t,x):
    account['source_engine_calls']+=1
    if account['source_engine_calls']%128==0:limit()
    return trace(t,x)
def bmove(t,x):
    z,p,ev=move(t,x)
    if any(q['kind']!='DOUBLE' or q['case'] not in ('LL','RR') or q['G'] not in M or q['P'] in M for q in ev):return None
    if labels(core(z,set(M)))!=set(range(1,12)):return None
    return z,len(ev)
def lru(v,x):return (x,)+tuple(q for q in v if q!=x)
def macro(s,x,H):
    a,b,e,r=s;bn=bmove(b,x)
    if not bn:return
    nb,q=bn;forms=[];na,_,ev=move(a,x)
    if len(ev)==H:forms.append((na,[('K',x)]))
    if H==2:
        for y in range(1,12):
            ay,_,ey=move(a,y)
            if len(ey)!=1:continue
            ax,_,ex=move(ay,x)
            if len(ex)==1:forms.append((ax,[('D',y),('K',x)]))
    variants=[(e,[])];g=b[0]
    if g!=3:
        ne=move(e,g)[0]
        if ne!=e:variants.append((ne,[('K',g)]))
    seen=set()
    for ep,pre in variants:
        ee=move(ep,x)[0] if x!=3 else ep
        for aa,word in forms:
            t=(aa,nb,ee,lru(r,x))
            if t not in seen:seen.add(t);yield t,pre+word,q
def trigger(s):
    a,b,e,r=s;x=r[-1];bn=bmove(b,x)
    if not bn or len(move(a,x)[2])!=1:return None
    if bn[1]==4:return [('K',x)]
    if bn[1]==5:
        aa=move(a,x)[0]
        for y in (1,11):
            ret=bmove(bn[0],y)
            if y!=x and ret and ret[1]==1 and len(move(aa,y)[2])==1:return [('K',x),('K',y)]
    return None
def edges(s):
    global proposals
    for x in M:
        if x==s[1][0]:continue
        bn=bmove(s[1],x)
        if not bn:continue
        for H in (1,2):
            w=2*H-bn[1]
            if w not in (0,1) or bn[1]==5:continue
            for t,word,q in macro(s,x,H):
                proposals+=1;limit();yield t,word,w,H,q
        if bn[1]==5:
            for h1,h2 in ((1,2),(2,1)):
                for mid,w1,_ in macro(s,x,h1):
                    for y in (1,11):
                        bm=bmove(mid[1],y) if y!=x else None
                        if not bm or bm[1]!=1:continue
                        for end,w2,_ in macro(mid,y,h2):
                            proposals+=1;limit();yield end,w1+w2,0,3,6
def main():
    global states_total
    old=json.loads((OLD/'symbolic_replay.json').read_text())['families'][1]
    known=json.loads((PREV/'forced_regions.json').read_text())['records'];oldAs={freeze(q['T_state']['A']) for q in known}
    R=vine(11);E=freeze(old['auxiliary_recurrent_start']);warm=[3,5,7,9,11,9,7,5,3,1]
    starts=[];seenA=set(oldAs)
    for u in range(1,12):
        for v in range(1,12):
            prep=[u,v,11,1];a=R
            for x in prep:a=move(a,x)[0]
            ax,_,ev=move(a,11);end,_,ret=move(ax,1)
            assert len(ev)==len(ret)==1
            if end in seenA:continue
            seenA.add(end)
            word=[('K',x) for x in warm[:-1]]+[('D',x) for x in SCAN+prep]+[('K',1),('K',11),('K',1)]
            critical_end=len(word);word += [('D',x) for x in SCAN+[11,1]]+[('K',x) for x in warm]
            rows,closed=replay(R,word,3,E)
            account['source_engine_calls']+=sum(1+(r['mode']=='K')+(r['mode']=='K' and r['target']!=3) for r in rows)
            assert closed==(R,R,E)
            cc=charts(rows,list(M));pp=packets(rows);pk=next(p for p in pp if p['end']==critical_end)
            assert (pk['H'],pk['Q'],pk['w'])==(2,6,-2) and cc[critical_end-2]['cold']
            rr=rows[critical_end-1];s0=(rr['after'][0],rr['after'][1],rr['after'][2],tuple(cc[critical_end-1]['recent_after']))
            starts.append({'prep':prep,'word':word,'initial':R,'erased_start':E,'negative_packet':pk,'start_T':s0})
            if len(starts)>=32:break
        if len(starts)>=32:break
    reports=[];found=None;loss_edges=0;positional={'plus_before_loss':0,'plus_after_loss':0}
    for j,start in enumerate(starts):
        s0=start['start_T'];best={s0:0};parent={s0:None};todo=collections.deque([(s0,0)]);states_total+=1
        try:
            while todo:
                limit();s,c=todo.popleft()
                if best.get(s)!=c:continue
                neg=trigger(s)
                if neg:
                    steps=[];t=s
                    while parent[t] is not None:
                        p,word,w,H,Q=parent[t];steps.append({'word':word,'w':w,'H':H,'Q':Q,'start':p,'end':t});t=p
                    found={'start_index':j,'start':start,'return_packets':steps[::-1],'return_weight':c,'negative_trigger':neg,
                        'status':'EXACT_REACHABLE_SOURCE_CANDIDATE_CLOSED_EDGE_EMBEDDING_STILL_REQUIRED'};break
                for t,word,w,H,Q in edges(s):
                    nc=c+w
                    if nc>1 or best.get(t,2)<=nc:continue
                    if t not in best:states_total+=1
                    best[t]=nc;parent[t]=(s,word,w,H,Q)
                    (todo.appendleft if w==0 else todo.append)((t,nc))
            reports.append({'start':j,'states':len(best),'queue':len(todo),'reason':'CANDIDATE_FOUND' if found else 'FINITE_ACTION_FAMILY_EXHAUSTED'})
        except Bound:reports.append({'start':j,'states':len(best),'queue':len(todo),'reason':'PREDECLARED_LIMIT'});break
        if found:break
    out('varied_sources.json',{'status':'CANDIDATE_FOUND' if found else 'FINITE_EXACT_NO_CHEAP_RETURN_FOUND',
        'starts':starts,'reports':reports,'candidate':found,'states_total':states_total,'candidate_packet_proposals':proposals,
        'scope':'new explicitly closed arbitrary-fringe source families, but only11 distinguished helper targets searched',
        'universal_main_barrier_proved':False,'limits':{'CPU':CAP,'states':10000,'proposals':100000,'splay_calls':500000},**account})
    print(json.dumps({'status':'CANDIDATE_FOUND' if found else 'FINITE_EXACT_NO_CHEAP_RETURN_FOUND',
        'new_starts':len(starts),'reports':reports,'states_total':states_total,'proposals':proposals,**account}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_varied_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,**account})
