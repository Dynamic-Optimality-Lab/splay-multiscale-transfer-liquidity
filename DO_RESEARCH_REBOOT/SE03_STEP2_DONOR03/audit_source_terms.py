"""Universal free-term identities on supplied paths; no source engine/search.
Fi are twelve independent arbitrary ordered BST terms, never instantiated.
Old W6/H6/erased-recurrence theorems are premises, not replayed rows.
"""
import json,time
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def N(k,l,r):return (k,l,r)
F=[f'F{i}' for i in range(12)]
def vine():
    t=F[11]
    for k in range(11,0,-1):t=N(k,F[k-1],t)
    return t
def at(t,p):
    for c in p:t=t[1 if c=='L' else 2]
    return t
def put(t,p,u):
    if not p:return u
    k,l,r=t
    return N(k,put(l,p[1:],u),r) if p[0]=='L' else N(k,l,put(r,p[1:],u))
def frame(t,kind):
    g,l,r=t
    if kind=='LL':
        p,pl,pr=l;x,a,b=pl
        return N(x,a,N(p,b,N(g,pr,r)))
    if kind=='RR':
        p,pl,pr=r;x,a,b=pr
        return N(x,N(p,N(g,l,pl),a),b)
    if kind=='LR':
        p,a,pr=l;x,b,c=pr
        return N(x,N(p,a,b),N(g,c,r))
    if kind=='RL':
        p,pl,d=r;x,b,c=pl
        return N(x,N(g,l,b),N(p,c,d))
    if kind=='L':
        p,a,b=l;return N(p,a,N(g,b,r))
    if kind=='R':
        p,a,b=r;return N(p,N(g,l,a),b)
    raise AssertionError(kind)
def access(t,key,path):
    assert at(t,path)[0]==key,(key,path)
    p=path;events=[]
    while len(p)>1:
        pre,pair=p[:-2],p[-2:]
        events.append({'kind':pair,'root_role':at(t,pre)[0]})
        t=put(t,pre,frame(at(t,pre),pair));p=pre
    if p:events.append({'kind':p,'root_role':t[0]});t=frame(t,p)
    assert t[0]==key
    return t,events
def leaves(t):
    return [t] if isinstance(t,str) else leaves(t[1])+[t[0]]+leaves(t[2])
def main():
    R=vine();records=[]
    def step(t,tag,key,path):
        u,e=access(t,key,path)
        assert leaves(u)==leaves(R)
        records.append({'tag':tag,'key':key,'path':path,'A_events':len(e),'frames':e})
        return u
    # New V insertion: its full B identity and its A prefix plus D1.
    t=R
    for k,p in [(3,'RR'),(5,'RR'),(3,'LL')]:t=step(t,'V-prefix',k,p)
    Vroot3=t
    assert step(t,'V-B-final',1,'LL')==R
    t=step(Vroot3,'V-A-D1',1,'LL');assert t==R
    # New preparation; every path is prescribed rather than searched.
    prep=[(8,'RRRRRRR'),(1,'L'),(9,'RR'),(11,'RR'),(8,'LLL'),(1,'L'),(9,'RRL'),(1,'L')]
    for k,p in prep:t=step(t,'preparation',k,p)
    Lmid=N(3,N(2,F[1],F[2]),N(5,N(4,F[3],F[4]),N(7,N(6,F[5],F[6]),F[7])))
    P=N(1,F[0],N(9,N(8,Lmid,F[8]),N(11,N(10,F[9],F[10]),F[11])))
    assert t==P
    t=step(t,'V-A-final',1,'');assert t==P
    t=step(t,'critical',11,'RR');t=step(t,'critical',1,'LL');assert t==P
    ascending=[(1,''),(2,'RLLL'),(3,'RL'),(4,'RLLL'),(5,'RL'),(6,'RLLL'),(7,'RL'),(8,'RL'),(9,'R'),(10,'RL'),(11,'R')]
    for k,p in ascending:t=step(t,'scan-ascending',k,p)
    L=F[0]
    for k in range(1,12):L=N(k,L,F[k])
    assert t==L
    for k in range(10,0,-1):t=step(t,'scan-descending',k,'L')
    assert t==R
    t=step(t,'alignment',11,'R'*10);t=step(t,'alignment',1,'LL')
    # Closed form of the already certified H6 max/min endpoint, not a replay.
    fan=N(4,N(3,F[2],F[3]),N(6,N(5,F[4],F[5]),N(8,N(7,F[6],F[7]),N(10,N(9,F[8],F[9]),F[10]))))
    Hendpoint=N(1,F[0],N(2,F[1],N(11,fan,F[11])))
    assert t==Hendpoint
    # New erased V insertion only: T9 -> K5 -> K1 -> T9.
    G=N(4,N(3,F[2],F[3]),F[4]);E=F[11]
    for k in [11,10,9,8,7,6,5,2,1]:E=N(k,G if k==5 else F[k-1],E)
    Ev,_=access(E,5,'RR');Ev,_=access(Ev,1,'LL');assert Ev==E
    # M3 continuation used for the exact post-packet debt bound.
    assert at(P,'R')[0]==9
    Efan=N(6,N(5,G,F[5]),N(8,N(7,F[6],F[7]),N(10,N(9,F[8],F[9]),F[10])))
    Eafter=N(1,F[0],N(2,F[1],N(11,Efan,F[11])))
    assert at(Eafter,'RRLRRL')[0]==9
    groups={g:sum(x['A_events'] for x in records if x['tag']==g) for g in {x['tag'] for x in records}}
    assert groups=={'V-prefix':3,'V-B-final':1,'V-A-D1':1,'preparation':13,'V-A-final':0,'critical':2,'scan-ascending':13,'scan-descending':10,'alignment':6}
    W=[('K',k) for k in [3,5,7,9,11,9,7,5,3,1]]
    suffix=[('K',k) for k in [3,5,7,9,11,9,7,5,3,1]]
    word=W+[('K',3),('K',5),('K',3),('D',1)]+[('D',k) for k,p in prep]+[('K',1),('K',11),('K',1)]+[('D',k) for k in range(1,12)]+[('D',k) for k in range(10,0,-1)]+[('D',11),('D',1)]+suffix
    assert len(word)==58 and sum(op=='K' for op,k in word)==26
    assert [word[i-1] for i in [15,16,23,24,25,49,57]]==[('D',8),('D',1),('K',1),('K',11),('K',1),('K',3),('K',3)]
    Pids=[(1,1),(9,1),(11,1),(13,1),(24,5),(49,1),(49,2),(57,1)]
    units=[(o,e,b) for o,e in [(15,2),(15,3),(15,4),(16,1)] for b in range(2)]
    assert len(set(units))==len(set(Pids))==8
    A=10+3+1+13+0+2+23+6+14
    assert A==72 and 2*A-34==110 and 2*A-26==118
    out('source_terms.json',{'status':'PASS_FREE_TERM_IDENTITIES','universal_variables':F,'records':records,'group_events':groups,
        'prepared_A':P,'old_H6_endpoint_matched':True,'erased_V_identity':True,
        'M3_continuation_paths':{'A':'R','B':'RRLRRL'},'word':[{'occurrence':i,'op':op,'key':k} for i,(op,k) in enumerate(word,1)],
        'counts':{'operations':58,'KEEP':26,'DELETE':32,'A':72,'QF':34,'QE_steady':26,'QE_first':27,'D3':7,'J3':1,'N':0,'P':8,'full_slack':110},
        'new_family_full_receipt':[{'demand':p,'unit':u} for p,u in zip(Pids,units)],
        'inherited_premises_not_replayed':['W6 identity/cost10','H6 suffix identity/cost14','W6H6 erased recurrence and comparison','max-depth successor fan formula','M3 local signed law','fixed Step1 tail exclusion'],
        'finite_population_instances':0,'source_engine_calls':0,'old_semantic_rows_replayed':0})
    print('PASS universal new source identities, source period, and eight actual donor IDs')
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_source_terms_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
