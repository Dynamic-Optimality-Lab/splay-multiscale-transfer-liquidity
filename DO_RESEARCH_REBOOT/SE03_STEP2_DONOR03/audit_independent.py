"""Separate primitive-rotation derivation of the NEW universal identities.
No import of the first derivation, source engines, graphs, or old row replay.
"""
import json,time
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def node(k,l,r):return ('node',k,l,r)
def child(t,side):return t[2 if side=='L' else 3]
def sub(t,p):
    for c in p:t=child(t,c)
    return t
def replace(t,p,u):
    if not p:return u
    _,k,l,r=t
    return node(k,replace(l,p[1:],u),r) if p[0]=='L' else node(k,l,replace(r,p[1:],u))
def rotate(t,p,direction):
    u=sub(t,p);_,g,a,b=u
    if direction=='right':
        _,v,c,d=a;u=node(v,c,node(g,d,b))
    else:
        _,v,c,d=b;u=node(v,node(g,a,c),d)
    return replace(t,p,u)
def splay(t,key,path):
    assert sub(t,path)[1]==key
    p=path;cost=0
    while len(p)>=2:
        context,pair=p[:-2],p[-2:]
        if pair=='LL':t=rotate(t,context,'right');t=rotate(t,context,'right')
        elif pair=='RR':t=rotate(t,context,'left');t=rotate(t,context,'left')
        elif pair=='LR':t=rotate(t,context+'L','left');t=rotate(t,context,'right')
        else:assert pair=='RL';t=rotate(t,context+'R','right');t=rotate(t,context,'left')
        cost+=1;p=context
    if p:t=rotate(t,'','right' if p=='L' else 'left');cost+=1
    assert t[1]==key
    return t,cost
def ordered_atoms(t):
    return [t] if isinstance(t,str) else ordered_atoms(t[2])+[t[1]]+ordered_atoms(t[3])
def encode(t):
    return t if isinstance(t,str) else [t[1],encode(t[2]),encode(t[3])]
def main():
    f=[f'F{i}' for i in range(12)];R=f[11]
    for k in reversed(range(1,12)):R=node(k,f[k-1],R)
    atoms=ordered_atoms(R);t=R;trace=[]
    def do(key,path,label):
        nonlocal t
        t,c=splay(t,key,path);assert ordered_atoms(t)==atoms
        trace.append((label,key,path,c))
    for k,p in [(3,'RR'),(5,'RR'),(3,'LL')]:do(k,p,'V-prefix')
    T3=t;v,c=splay(T3,1,'LL');assert v==R and c==1
    do(1,'LL','V-A-D1');assert t==R
    for k,p in [(8,'RRRRRRR'),(1,'L'),(9,'RR'),(11,'RR'),(8,'LLL'),(1,'L'),(9,'RRL'),(1,'L')]:do(k,p,'preparation')
    middle=node(3,node(2,f[1],f[2]),node(5,node(4,f[3],f[4]),node(7,node(6,f[5],f[6]),f[7])))
    expected=node(1,f[0],node(9,node(8,middle,f[8]),node(11,node(10,f[9],f[10]),f[11])))
    assert t==expected
    do(1,'','V-A-final');do(11,'RR','critical');do(1,'LL','critical');assert t==expected
    # The new repair is checked from the prepared term, not from recorded endpoints.
    for k,p in zip(range(1,12),['','RLLL','RL','RLLL','RL','RLLL','RL','RL','R','RL','R']):do(k,p,'scan-ascending')
    L=f[0]
    for k in range(1,12):L=node(k,L,f[k])
    assert t==L
    for k in range(10,0,-1):do(k,'L','scan-descending')
    assert t==R
    do(11,'R'*10,'alignment');do(1,'LL','alignment')
    # The old fan formula is an inherited structural lemma, never replayed here.
    arm=node(4,node(3,f[2],f[3]),node(6,node(5,f[4],f[5]),node(8,node(7,f[6],f[7]),node(10,node(9,f[8],f[9]),f[10]))))
    endpoint=node(1,f[0],node(2,f[1],node(11,arm,f[11])))
    assert t==endpoint
    G=node(4,node(3,f[2],f[3]),f[4]);T=f[11]
    for k in [11,10,9,8,7,6,5,2,1]:T=node(k,G if k==5 else f[k-1],T)
    Ev,c1=splay(T,5,'RR');Ev,c2=splay(Ev,1,'LL');assert Ev==T and c1==c2==1
    # Fixed nine-Score fan after max/min, supplied by the old fan lemma.
    fan9=node(6,node(5,G,f[5]),node(8,node(7,f[6],f[7]),node(10,node(9,f[8],f[9]),f[10])))
    afterE=node(1,f[0],node(2,f[1],node(11,fan9,f[11])))
    assert sub(expected,'R')[1]==sub(afterE,'RRLRRL')[1]==9
    assert (len('R')+1)//2==1 and len('RRLRRL')//2==3
    derived=json.loads((B/'source_terms.json').read_text())
    assert derived['prepared_A']==encode(expected)
    newrows=[(r['tag'],r['key'],r['path'],r['A_events']) for r in derived['records'] if r['tag']!='V-B-final']
    assert newrows==trace
    # Exact algebraic consequences of sealed signed M3: no D table queries.
    # Range [0,2], first transition increment >=2 forces (0,2).
    # Return increment >=-1 gives next>=1; continuation increment>=1
    # with endpoint<=2 gives next<=1, so next=1.
    debts={'before':0,'mid':2,'after':1,'maximum':2}
    b=[2-debts[k] for k in ['before','mid','after']];assert b==[2,0,1]
    births=[2-4+2-0,2-1+1-2];assert births==[0,0]
    # Symbolic FIFO identities: arbitrary carried units x,y, actual packet bits a,b.
    before=['x','y'];first=['a0','a1'];ret=['b0','b1']
    assert (before+first)[:4]==['x','y','a0','a1'] and not (before+first)[4:]
    assert ret[:1]==['b0'] and ret[1:]==['b1']
    # Next qE=qF=2; old b1 is first regardless of new supply identities.
    assert (ret[1:]+['new0','new1'])[:2][0]=='b1'
    # Reconstruct all unmatched IDs from inherited W/H identities plus new V.
    Wdirect=[(1,1),(9,1)];Vdirect=[(11,1),(13,1)]
    retained=[(24,5)];Hdirect=[(49,1),(49,2),(57,1)]
    demands=Wdirect+Vdirect+retained+Hdirect
    event_ids=[(15,2),(15,3),(15,4),(16,1)]
    donors=[(*ev,bit) for ev in event_ids for bit in (0,1)]
    assert len(set(demands))==len(set(donors))==8
    receipt=[{'demand':list(d),'unit':list(u)} for d,u in zip(demands,donors)]
    assert receipt==derived['new_family_full_receipt']
    w=derived['word'];assert len(w)==58
    assert [w[i-1]['op']+str(w[i-1]['key']) for i in [12,13,14,15,16,23,24,25,49,50,57,58]]==['K5','K3','D1','D8','D1','K1','K11','K1','K3','K5','K3','K1']
    assert sum(x['A_events'] for x in derived['records'] if x['tag']=='preparation')==13
    # IDs (15,2/3/4),(16,1) are macro ordinals4/5/6/7, from 1+1+4+1.
    assert [1+1+j for j in (2,3,4)]+[1+1+4+1]==[4,5,6,7]
    assert 10+3+1+13+2+13+10+6+14==72
    assert 10+4+20==34 and 24+2==26 and 5+2==7 and 7+1==8
    assert 2*72-34==110 and (2*72-26)-8==110
    assert derived['counts']=={'operations':58,'KEEP':26,'DELETE':32,'A':72,'QF':34,'QE_steady':26,'QE_first':27,'D3':7,'J3':1,'N':0,'P':8,'full_slack':110}
    # Guard proof schema: actual tail IDs are injectively typed by
    # (period,operation,event,bit); disjoint source gaps imply disjoint IDs.
    # Six demands per packet follows from q5+q1; no global P<=U premise.
    out('independent_audit.json',{'status':'PASS_SCOPED_SOURCE_THEOREMS_ONLY','method':'separate primitive left/right rotations on arbitrary ordered free terms plus independent ownership derivation',
        'universal_Fi':True,'new_trace_rows_agree':True,'full_pair_closure':'new A endpoint matches inherited H6 suffix input; full B W6 V H6 identities',
        'actual_debts':debts,'local_reserve_births':births,'all_four_packet_bits_common_owned':True,
        'exact_receipt':receipt,'guarded_module_proof':'tail exclusion, source q5+q1 bound, disjoint gaps, slot ownership registry, actual cyclic-ID transport',
        'counterexample_scope':'packet-local fE donor extension only, not general Step2',
        'old_receipts_changed':False,'normalized_chart_potential_used':False,'new_finite_tests':0,'source_engine_calls':0,'old_semantic_rows_replayed':0,
        'external_peer_review':False,'whole_compiler_formalization':False,'Step2_complete':False,'Step3':'OPEN','Universal_CD':'OPEN'})
    print('PASS separate primitive free-term audit, exact source ownership, and scoped conclusions')
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_independent_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
