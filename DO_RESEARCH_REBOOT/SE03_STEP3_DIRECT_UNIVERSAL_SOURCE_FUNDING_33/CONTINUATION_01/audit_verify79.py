"""Independent mutable-parent source replay and source-owner audit.
No producer imports; actual fresh source queries are counted cumulatively.
"""
import hashlib,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;F=B/'SOURCE_JOINT_REPAIR_03';START=time.process_time();CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);CALLS=0
def out(n,z):
    with (F/n).open('x',encoding='utf-8') as f:json.dump(z,f,indent=2)
def pin(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def eq(a,b):return json.dumps(a,sort_keys=True)==json.dumps(b,sort_keys=True)
def tree(t):return None if t is None else (t[0],tree(t[1]),tree(t[2]))
def mp(v):return {tuple(z['demand']):tuple(z['unit']) for z in v}
class Node:
    def __init__(self,k):self.k=k;self.left=self.right=self.parent=None
class Mutable:
    def __init__(self,t):
        self.nodes={}
        def make(t,p=None):
            if t is None:return None
            v=Node(t[0]);self.nodes[v.k]=v;v.parent=p;v.left=make(t[1],v);v.right=make(t[2],v);return v
        self.root=make(t)
    def snapshot(self):
        def get(v):return None if v is None else (v.k,get(v.left),get(v.right))
        return get(self.root)
    def rotate(self,x,b,detail):
        p=x.parent;g=p.parent;before=self.snapshot() if detail else None;right=x is p.left;d='right' if right else 'left'
        if right:
            p.left=x.right
            if p.left:p.left.parent=p
            x.right=p
        else:
            p.right=x.left
            if p.right:p.right.parent=p
            x.left=p
        p.parent=x;x.parent=g
        if g is None:self.root=x
        elif g.left is p:g.left=x
        else:assert g.right is p;g.right=x
        z={'pivot':p.k,'direction':d,'bit':b}
        if detail:z.update(before=before,after=self.snapshot())
        return z
    def splay(self,k,detail=False):
        global CALLS
        assert CALLS<QCAP and time.process_time()-START<CAP-1;CALLS+=1
        x=self.nodes[k];v=x;depth=0
        while v.parent:depth+=1;v=v.parent
        events=[]
        while x.parent:
            p=x.parent;g=p.parent;j=len(events)+1
            if g is None:
                pattern='L' if p.left is x else 'R';gp=p.k;pk=None;rot=[self.rotate(x,0,detail)]
            else:
                a=p is g.left;b=x is p.left;pattern=('L' if a else 'R')+('L' if b else 'R');gp=g.k;pk=p.k
                if a==b:rot=[self.rotate(p,0,detail),self.rotate(x,1,detail)]
                else:rot=[self.rotate(x,0,detail),self.rotate(x,1,detail)]
            events.append({'j':j,'pattern':pattern,'grandparent':gp,'parent':pk,'rotations':rot})
        assert len(events)==(depth+1)//2
        return len(events),depth//2,events
def ancestor(t,g,x):
    # Independent parent reconstruction, not the producer's BST search test.
    parents={}
    def fill(v,p):
        if v is None:return
        parents[v[0]]=p;fill(v[1],v[0]);fill(v[2],v[0])
    fill(t,None);v=parents[x]
    while v is not None:
        if v==g:return True
        v=parents[v]
    return False
def independently_first_loss(rows,g,mu,start,end):
    pos={z['t']:i for i,z in enumerate(rows)};i=(pos[start]+1)%len(rows)
    while True:
        z=rows[i]
        for e in z['A_events']:
            for a in e['rotations']:
                if ancestor(a['before'],g,mu) and not ancestor(a['after'],g,mu):
                    assert a['pivot']==g
                    return (z['t'],e['j'],a['bit']),a['direction'],z
        if z['t']==end:break
        i=(i+1)%len(rows)
    raise AssertionError('no independent retirement')
def macros(rows,field):
    ends=[i for i,z in enumerate(rows) if z['genuine_'+field]];mm=[];h0={};D=set();U=set();member={}
    for j,end in enumerate(ends):
        prev=ends[j-1];ix=list(range(prev+1,end+1)) if prev<end else list(range(prev+1,len(rows)))+list(range(end+1))
        rr=[rows[i] for i in ix];u=[(z['t'],a,b) for z in rr for a in range(1,z['a']+1) for b in (0,1)];d=[(z['t'],k) for z in rr for k in range(1,z['q'+field]+1)]
        h0.update(zip(d,u));D.update(d);U.update(u);member.update((z['t'],j) for z in rr)
        mm.append({'rows':rr,'H':len(u)//2,'Q':len(d),'units':u,'demands':d,'target':rows[end]['key'],'end':rows[end]['t']})
    return mm,h0,D,U,member
def source_replay(z):
    A=Mutable(z['initial_diagonal']);BF=Mutable(z['initial_diagonal']);BE=Mutable(z['initial_diagonal']);cf=[];ce=[];initial_period=None
    allrows=z['prefix_rows']+z['period_rows'];actual=[]
    for expected in allrows:
        t=expected['t'];kind=expected['kind'];k=expected['key']
        if t==z['period'][0]:initial_period=(A.snapshot(),BF.snapshot(),BE.snapshot(),tuple(cf),tuple(ce))
        assert eq(A.snapshot(),expected['A_before']) and eq(BF.snapshot(),expected['BF_before']) and eq(BE.snapshot(),expected['BE_before'])
        a,_,ae=A.splay(k,True);q=qe=0;g=ge=False;fe=[]
        if kind=='K':
            g=BF.root.k!=k;_,q,fe=BF.splay(k)
            if g:cf=[k]+[x for x in cf if x!=k]
            if k!=3:
                ge=BE.root.k!=k;_,qe,_=BE.splay(k)
                if ge:ce=[k]+[x for x in ce if x!=k]
        assert (a,q,qe,g,ge)==(expected['a'],expected['qF'],expected['qE'],expected['genuine_F'],expected['genuine_E'])
        assert eq(ae,expected['A_events']) and eq(fe,expected['BF_events'])
        assert eq(A.snapshot(),expected['A_after']) and eq(BF.snapshot(),expected['BF_after']) and eq(BE.snapshot(),expected['BE_after'])
        assert cf==expected['chart_F'] and ce==expected['chart_E']
        actual.append({**expected,'A_events':ae,'BF_events':fe})
    assert initial_period==(A.snapshot(),BF.snapshot(),BE.snapshot(),tuple(cf),tuple(ce))
    assert eq(initial_period,z['period_boundary'])
    period=[r for r in actual if r['t']>=z['period'][0]];assert len(period)==z['period'][1]-z['period'][0]+1
    return period
def verify_funding(z,rows):
    f=z['funding'];mm,h0,D,U,tm=macros(rows,'F');h=mp(f['full_h']);assert h0==mp(f['h0'])
    assert set(h)==D and len(set(h.values()))==len(h) and set(h.values())<=U and all(h[d]==u for d,u in h0.items())
    blocks={int(i):name for i,name in f['block_by_macro'].items()}
    for p in f['return_blocks']:
        members=p['macro_indices'];close=members[-1];passes=members[:-1];k=len(passes);mu=p['target'];selected=[]
        for w in p['witnesses']:
            unit,direction,_=independently_first_loss(rows,w['retired_key'],mu,w['born_at'],w['closing_at']);assert unit==tuple(w['unit']) and direction==w['direction']
            assert direction==('right' if mu==1 else 'left');selected.append(unit)
        assert len(set(selected))==k
        outside=[u for u in selected if tm[u[0]]!=close];assert len(outside)>=len([d for d in mm[close]['demands'] if d not in h0])
        G=0
        for m in passes:
            rr=mm[m]['rows'];last=[q for q in rr if q['key']==mm[m]['target'] and q['a']>0][-1];other=mm[m]['H']-last['a'];G+=other
            assert all(q['a']==0 for q in rr[rr.index(last)+1:])
            cnt=sum(tm[u[0]]==m for u in outside);assert cnt<=2*other<=len(mm[m]['units'])-mm[m]['Q']
        assert 2*(G+mm[close]['H'])>=k
        assert sum(2*mm[m]['H']-mm[m]['Q'] for m in members)>=1
    for seed in f['seed_assignments']:
        d=tuple(seed['demand']);u=tuple(seed['unit']);assert d not in h0 and u not in set(h0.values()) and h[d]==u
        assert blocks[tm[d[0]]]==blocks[tm[u[0]]]==seed['block']
    assert all(blocks[tm[d[0]]]==blocks[tm[u[0]]] for d,u in h.items())
    used=set();paid={}
    for event in f['bank_events']:
        assert (event['before'],event['admitted'],event['after'])==(0,2,0)
        for b,act in enumerate(event['actions']):
            u=(event['t'],event['j'],b);assert tuple(act['unit'])==u and u not in used;used.add(u)
            if act['action']=='emit':
                d=tuple(act['demand']);assert d not in paid and h[d]==u;paid[d]=u
            else:assert act['action']=='release' and act['demand'] is None and u not in h.values()
    assert used==U and paid==h
    extreme=[]
    for pair in f['raw_extreme_ticket_map']:
        d=tuple(pair['demand']);w=pair['witness'];u,direction,row=independently_first_loss(rows,w['retired_key'],w['target'],w['born_at'],w['closing_at'])
        assert u==tuple(w['unit']) and (row['kind']=='D' or row['t']==d[0]);assert direction==('right' if w['target']==1 else 'left');extreme.append(u)
    assert len(set(extreme))==len(extreme)==16*z['period_copies']
    return mm,h0,h,D,U,set(extreme)
def verify_owners(rows,h0,h,D,U):
    owners=F/'actual_auxiliary_owner_extension.json';z=json.loads(owners.read_text())
    for p,sha in z['input_sha256'].items():assert pin(Path(p))==sha
    em,fe,E,_,_=macros(rows,'E');assert fe==mp(z['fE']) and all(m['Q']<=2 and m['H']>=1 and m['Q']<=2*m['H'] for m in em)
    C=D&E;l={d:fe[d] for d in C};ih0={u:d for d,u in h0.items()};prior=dict(l)
    # Reverse-component derivation of the canonical original natural prior.
    for terminal in set(h0.values())-set(l.values()):
        u=terminal;seen=set()
        while u in ih0:
            assert u not in seen;seen.add(u);d=ih0[u]
            if d not in l:prior[d]=terminal;break
            u=l[d]
    assert prior==mp(z['old_canonical_effective_a0']) and len(prior)==32
    extra=mp(z['new_actual_pairs']);ih={u:d for d,u in h.items()}
    for root,terminal in extra.items():
        assert terminal in U-set(prior.values());u=terminal;seen=set()
        while True:
            assert u in ih and u not in seen;seen.add(u);d=ih[u]
            if d not in prior:assert d==root;break
            u=prior[d]
    assert set(extra)==D-set(prior) and len(set(extra.values()))==len(extra)==4
    assert {**prior,**extra}==mp(z['full_allocation']) and all(prior[d]==fe[d] for d in C)
    return {'old_frozen_values':len(prior),'newly_funded':len(extra),'fE_demands':len(E),'auxiliary_core':z['auxiliary_core_size'],'all_old_preserved':True},set(prior.values())
def collision_audit():
    z=json.loads((F/'actual_interior_ticket_collision.json').read_text());expected=z['local_rows'];A=Mutable(expected[0]['A_before']);BF=Mutable(expected[0]['BF_before']);rr=[]
    for e in expected:
        a,_,ae=A.splay(e['key'],True);q=0;be=[]
        if e['kind']=='K':_,q,be=BF.splay(e['key'])
        assert (a,q)==(e['a'],e['qF']) and eq(A.snapshot(),e['A_after']) and eq(BF.snapshot(),e['BF_after']) and eq(ae,e['A_events']) and eq(be,e['BF_events'])
        rr.append({**e,'A_events':ae})
    units=[]
    for x,t in ((1,2),(3,3),(5,4)):
        u,direction,_=independently_first_loss(rr,13,x,0,t);units.append(u);assert direction=='right' and rr[t]['BF_events'][0]['grandparent']==13
    assert units==[(1,1,0)]*3
    return {'distinct_demands':3,'first_removal_units':1,'unrestricted_rule_refuted':True,'full_closed_embedding':'mathematical inherited realization theorem; new numerical Gamma not replayed','not_a_CD_counterexample':True}
def main():
    source=F/'actual_monotone_return_source.json';z=json.loads(source.read_text());rows=source_replay(z);mm,h0,h,D,U,raw=verify_funding(z,rows);ownership,occupied=verify_owners(rows,h0,h,D,U);collision=collision_audit()
    # Exact symbolic generic rotation loss, independent from numeric trees.
    old={'g':{'p','A','B','C'},'p':{'A','B'}};new={'g':{'B','C'},'p':{'A','g','B','C'}}
    assert old['g']-new['g']=={'p','A'} and not old['p']-new['p']
    docs=('ANCESTOR_RETIREMENT_LEMMA.md','MONOTONE_RETURN_SOURCE_FUNDING.md','EXTREME_TARGET_JOINT_TICKETS.md','INTERIOR_TICKET_COLLISION.md','SOURCE_ONLY_B_BOUND.md')
    result={'status':'PASS_SOURCE_RETIREMENT_FUNDING_GLOBAL_EXTREME_TICKETS_OWNERS_AND_BANK',
      'literal_period':z['period'],'A':sum(r['a'] for r in rows),'QF':len(D),'QE':ownership['fE_demands'],'actual_natural_excess_paid':len(D-set(h0)),
      'genuine_full_KEEPS_with_zero_A_events':sum(r['genuine_F'] and r['a']==0 for r in rows),
      'global_extreme_raw_tickets':len(raw),'raw_extreme_bits_already_frozen_owned':len(raw&occupied),'raw_tickets_not_assumed_unowned':True,
      'ownership':ownership,'bank_peak':2,'local_unrestricted_ticket_collision':collision,
      'uniform_scope':'written MR proof for arbitrary A/helpers and Qi<=2,Qc<=k; raw extreme theorem on maximal closed core; no finite passing test promoted to all sources',
      'universal_C33_closed':False,'distinct_source_implementations_same_agent':True,'external_or_formal_verification':False,
      'source_queries':CALLS,'source_engine_calls':CALLS,
      'input_sha256':{str(source):pin(source),str(F/'actual_auxiliary_owner_extension.json'):pin(F/'actual_auxiliary_owner_extension.json'),str(F/'actual_interior_ticket_collision.json'):pin(F/'actual_interior_ticket_collision.json'),**{d:pin(F/d) for d in docs}}}
    assert time.process_time()-START<CAP-1;out('independent_source_audit.json',result)
    print(json.dumps({k:v for k,v in result.items() if k!='input_sha256'}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_verify79_exit.json').open('x') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':CALLS,'source_engine_calls':CALLS},f)
