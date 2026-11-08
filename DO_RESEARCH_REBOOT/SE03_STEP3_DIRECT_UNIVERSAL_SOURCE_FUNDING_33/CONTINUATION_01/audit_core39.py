"""Bounded actual source replay for a named all-r source theorem.
Functional full-tree bottom-up implementation; every fresh splay charged.
"""
import hashlib,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;F=B/'SOURCE_JOINT_REPAIR_03'
START=time.process_time();CAP=float(sys.argv[1]);QCAP=min(500,int(sys.argv[2]));CALLS=0
def out(n,z):
    with (F/n).open('x',encoding='utf-8') as f:json.dump(z,f,indent=2)
def pin(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def vine(lo,hi):return None if lo>hi else (lo,None,vine(lo+1,hi))
def at(t,p):
    for s in p:t=t[s]
    return t
def put(t,p,z):
    if not p:return z
    return (t[0],put(t[1],p[1:],z),t[2]) if p[0]==1 else (t[0],t[1],put(t[2],p[1:],z))
def search(t,x):
    p=[]
    while t[0]!=x:
        s=1 if x<t[0] else 2;p.append(s);t=t[s];assert t is not None
    return p
def anc(t,g,x):return g!=x and g in [at(t,search(t,x)[:j])[0] for j in range(len(search(t,x)))]
def splay(t,x,detail=False):
    global CALLS
    assert CALLS<QCAP and time.process_time()-START<CAP-1;CALLS+=1
    depth=len(search(t,x));ev=[]
    while t[0]!=x:
        p=search(t,x);j=len(ev)+1;rot=[]
        if len(p)==1:
            scope=[];pattern='L' if p[0]==1 else 'R';seq=[(scope,'right' if p[0]==1 else 'left')];g=t[0];parent=None
        else:
            scope=p[:-2];a,b=p[-2:];u=at(t,scope);g=u[0];parent=u[a][0];pattern=('L' if a==1 else 'R')+('L' if b==1 else 'R')
            if a==b:seq=[(scope,'right' if a==1 else 'left')]*2
            else:seq=[(scope+[a],'left' if b==2 else 'right'),(scope,'right' if a==1 else 'left')]
        for bit,(where,direction) in enumerate(seq):
            before=t;u=at(t,where);pivot=u[0]
            if direction=='right':
                k,A,C=u;y,L,M=A;z=(y,L,(k,M,C))
            else:
                k,A,C=u;y,M,R=C;z=(y,(k,A,M),R)
            t=put(t,where,z);item={'pivot':pivot,'direction':direction,'bit':bit}
            if detail:item.update(before=before,after=t)
            rot.append(item)
        ev.append({'j':j,'pattern':pattern,'grandparent':g,'parent':parent,'rotations':rot})
    assert len(ev)==(depth+1)//2
    return t,len(ev),depth//2,ev

def family_word(r):
    n=2*r-1;P=[n,1]+list(range(3,n+1,2));V=P+[n+1-x for x in P];w=[]
    for i,x in enumerate(V):
        if 2<=i<=r:w.extend([('D',1),('D',x)])
        if r+3<=i<=2*r+1:w.extend([('D',n),('D',x)])
        w.append(('K',x))
    w.extend(('D',x) for x in list(range(1,n+1))+list(range(n-1,0,-1)))
    return w,V
def replay(r):
    n=2*r-1;w,V=family_word(r);initial=vine(1,n);A=BF=BE=initial;cf=ce=();seen={(A,BF,BE,cf,ce):0};copies=[];boundaries=[(A,BF,BE,cf,ce)]
    for copy in range(5):
        rows=[]
        for i,(kind,x) in enumerate(w):
            t=copy*len(w)+i+1;ba,bf,be=A,BF,BE;A,a,_,ae=splay(A,x,True);q=qe=0;g=ge=False;fe=[]
            if kind=='K':
                g=BF[0]!=x;BF,_,q,fe=splay(BF,x)
                if g:cf=(x,)+tuple(y for y in cf if y!=x)
                if x!=3:
                    ge=BE[0]!=x;BE,_,qe,_=splay(BE,x)
                    if ge:ce=(x,)+tuple(y for y in ce if y!=x)
            rows.append({'t':t,'kind':kind,'key':x,'A_before':ba,'BF_before':bf,'BE_before':be,'A_after':A,'BF_after':BF,'BE_after':BE,'a':a,'qF':q,'qE':qe,'genuine_F':g,'genuine_E':ge,'A_events':ae,'BF_events':fe,'chart_F':cf,'chart_E':ce})
        assert A==BF==initial and sum(z['qF'] for z in rows)==6*r-6
        copies.append(rows);state=(A,BF,BE,cf,ce);boundaries.append(state)
        if state in seen:
            u=seen[state];L=copy+1-u;period=sum(copies[u:u+L],[])
            assert boundaries[u]==boundaries[u+L]
            return w,V,copies,period,u,L,boundaries[u],initial
        seen[state]=copy+1
    raise AssertionError('named replay erasure/chart recurrence not closed within five copies')

def macro_data(rows):
    ends=[i for i,z in enumerate(rows) if z['genuine_F']];mm=[];h0={};D=set();U=set();tm={}
    for k,end in enumerate(ends):
        prev=ends[k-1];ii=list(range(prev+1,end+1)) if prev<end else list(range(prev+1,len(rows)))+list(range(end+1))
        rr=[rows[i] for i in ii];uu=[(z['t'],j,b) for z in rr for j in range(1,z['a']+1) for b in (0,1)];dd=[(z['t'],j) for z in rr for j in range(1,z['qF']+1)]
        h0.update(zip(dd,uu));D.update(dd);U.update(uu);tm.update((z['t'],k) for z in rr)
        mm.append({'end_t':rows[end]['t'],'target':rows[end]['key'],'H':len(uu)//2,'Q':len(dd),'units':uu,'demands':dd,'rows_t':[z['t'] for z in rr]})
    return mm,h0,D,U,tm
def between(rows,start,end):
    by={z['t']:i for i,z in enumerate(rows)};j=(by[start]+1)%len(rows);ans=[]
    while True:
        z=rows[j];ans.append(z)
        if z['t']==end:return ans
        j=(j+1)%len(rows);assert len(ans)<=len(rows)
def loss(rows,g,mu,start,end):
    for z in between(rows,start,end):
        for e in z['A_events']:
            for a in e['rotations']:
                if anc(a['before'],g,mu) and not anc(a['after'],g,mu):
                    assert a['pivot']==g
                    return {'born_at':start,'closing_at':end,'retired_key':g,'target':mu,'unit':(z['t'],e['j'],a['bit']),'operation_kind':z['kind'],'operation_key':z['key'],'direction':a['direction']}
    raise AssertionError('missing actual first ancestor retirement')
def construct(rows,r):
    n=2*r-1;mm,h0,D,U,tm=macro_data(rows);N=len(mm);assert N%(2*r+2)==0
    h=dict(h0);blocks={};proofs=[];seeds=[]
    for base in range(0,N,2*r+2):
        for name,passes,close,mu in (
          ('inc',list(range(base+2,base+r+1)),base+r+1,1),
          ('dec',list(range(base+r+3,base+2*r+2)),(base+2*r+2)%N,n)):
            close%=N;BID=name+str(base);members=passes+[close]
            for m in members:assert m not in blocks;blocks[m]=BID
            witnesses=[loss(rows,mm[m]['target'],mu,mm[m]['end_t'],mm[close]['end_t']) for m in passes]
            assert len({tuple(w['unit']) for w in witnesses})==r-1
            outside=[w for w in witnesses if tm[w['unit'][0]]!=close]
            local_spares={};distinguished={}
            for m in passes:
                mr=[next(z for z in rows if z['t']==t) for t in mm[m]['rows_t']];x=mm[m]['target'];pos=[z for z in mr if z['key']==x and z['a']>0];assert pos
                star=pos[-1];assert all(z['a']==0 for z in mr[mr.index(star)+1:]);G=mm[m]['H']-star['a']
                ww=[w for w in outside if tm[w['unit'][0]]==m];assert all(w['unit'][0]!=star['t'] for w in ww)
                sp=mm[m]['units'][mm[m]['Q']:];assert mm[m]['Q']<=2 and len(sp)>=2*G>=len(ww)
                for rank,w in enumerate(ww):local_spares[tuple(w['unit'])]=sp[rank]
                distinguished[m]={'positive_access_t':star['t'],'positive_cost':star['a'],'other_events':G,'retirement_tickets':len(ww),'spares':len(sp)}
            missing=[d for d in mm[close]['demands'] if d not in h0];assert len(outside)>=len(missing)
            for d,w in zip(missing,outside):
                u=local_spares[tuple(w['unit'])];assert u not in h.values();h[d]=u;seeds.append({'demand':d,'unit':u,'first_retirement_ticket':w,'block':BID})
            H=sum(mm[m]['H'] for m in members);Q=sum(mm[m]['Q'] for m in members);G=sum(z['other_events'] for z in distinguished.values())
            assert 2*(G+mm[close]['H'])>=r-1 and 2*H-Q>=1
            proofs.append({'block':BID,'macro_indices':members,'target':mu,'H':H,'Q':Q,'margin':2*H-Q,'witnesses':witnesses,'outside_ticket_count':len(outside),'natural_excess_paid':len(missing),'distinguished':distinguished})
        for m in (base+1,base+r+2):assert m not in blocks;blocks[m]='bridge'+str(m);assert mm[m]['Q']==1 and mm[m]['H']>=1
    assert set(h)==D and len(set(h.values()))==len(h) and set(h.values())<=U and all(h[d]==u for d,u in h0.items())
    # New all-extreme raw ticket theorem checked on the complete actual period.
    extreme=[]
    for z in rows:
        if not z['genuine_F'] or z['key'] not in (1,n):continue
        for k,e in enumerate(z['BF_events'],1):
            assert len(e['rotations'])==2 and e['grandparent']%2==1 and e['parent']%2==0
            g=e['grandparent'];j=next((j for j,q in enumerate(rows) if q['t']==z['t']));p=(j-1)%len(rows)
            while not (rows[p]['genuine_F'] and rows[p]['key']==g):p=(p-1)%len(rows);assert p!=j
            w=loss(rows,g,z['key'],rows[p]['t'],z['t']);assert w['operation_kind']=='D' or w['unit'][0]==z['t']
            assert w['direction']==('right' if z['key']==1 else 'left');extreme.append({'demand':(z['t'],k),'witness':w})
    assert len({tuple(x['witness']['unit']) for x in extreme})==len(extreme)
    um={u:blocks[tm[u[0]]] for u in U};dm={d:blocks[tm[d[0]]] for d in D};assert all(um[u]==dm[d] for d,u in h.items())
    inv={u:d for d,u in h.items()};events=[]
    for z in rows:
        for j in range(1,z['a']+1):events.append({'t':z['t'],'j':j,'before':0,'admitted':2,'after':0,'actions':[{'unit':(z['t'],j,b),'demand':inv.get((z['t'],j,b)),'action':'emit' if (z['t'],j,b) in inv else 'release'} for b in (0,1)]})
    pairs=lambda mp:[{'demand':d,'unit':u} for d,u in sorted(mp.items())]
    return {'macros':mm,'h0':pairs(h0),'full_h':pairs(h),'seed_assignments':seeds,'return_blocks':proofs,'block_by_macro':blocks,'raw_extreme_ticket_map':extreme,'bank_events':events,'working_peak':2,'D':len(D),'U':len(U),'natural_excess':len(D-set(h0)),'actual_owner_map':'no new fE/a0 invented; original full comparison exchange theorem reused parametrically'}
def collision():
    n=13;A=(13,(7,vine(1,6),vine(8,12)),None);BF=vine(1,n);rows=[]
    for t,(kind,x) in enumerate((('K',13),('D',7),('K',1),('K',3),('K',5))):
        aa=A;bb=BF;A,a,_,ae=splay(A,x,True);q=0;be=[]
        if kind=='K':BF,_,q,be=splay(BF,x)
        rows.append({'t':t,'kind':kind,'key':x,'A_before':aa,'BF_before':bb,'A_after':A,'BF_after':BF,'a':a,'qF':q,'A_events':ae,'BF_events':be})
    ww=[loss(rows,13,x,0,t) for x,t in ((1,2),(3,3),(5,4))]
    assert all(w['unit']==(1,1,0) for w in ww) and [rows[t]['qF'] for t in (2,3,4)]==[1,2,2]
    assert all(rows[t]['BF_events'][0]['grandparent']==13 for t in (2,3,4))
    return {'status':'SOURCE_REALIZABLE_UNRESTRICTED_FIRST_RETIREMENT_COLLISION','coordinate':'relative to initial genuine K13; absolute t=t0+offset in the mathematical closed embedding','local_rows':rows,'distinct_demands':[(2,1),(3,1),(4,1)],'same_unit':(1,1,0),'witnesses':ww,'closed_embedding':'accepted uniform A-realization over the explicit closed V7 B cycle; new finite Gamma prefix not executed','not_a_CD_or_frozen_extension_counterexample':True}
def main():
    r=7;w,V,copies,rows,u,L,boundary,initial=replay(r);built=construct(rows,r);c=collision()
    out('actual_monotone_return_source.json',{'status':'ACTUAL_R7_DIRTY_SOURCE_AND_RETIREMENT_FUNDING_PRODUCER','r':r,'physical_keys':13,'word':w,'genuine_B_word':V,'initial_diagonal':initial,'prefix_copies':u,'period_copies':L,'prefix_rows':sum(copies[:u],[]),'period_rows':rows,'period':[rows[0]['t'],rows[-1]['t']],'period_boundary':boundary,'A':sum(z['a'] for z in rows),'QF':sum(z['qF'] for z in rows),'QE':sum(z['qE'] for z in rows),'genuine_full':sum(z['genuine_F'] for z in rows),'funding':built,'source_queries':CALLS,'principal_C33':'OPEN'})
    out('actual_interior_ticket_collision.json',c)
    assert time.process_time()-START<CAP-1
    print(json.dumps({'status':'ACTUAL_SOURCE_RETIREMENT_FUNDING_READY','period':[rows[0]['t'],rows[-1]['t']],'source_queries':CALLS,'QF':built['D'],'natural_excess_paid':built['natural_excess'],'global_extreme_tickets':len(built['raw_extreme_ticket_map']),'working_peak':2,'principal_C33':'OPEN'}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_core39_exit.json').open('x') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':CALLS,'source_engine_calls':CALLS},f)
