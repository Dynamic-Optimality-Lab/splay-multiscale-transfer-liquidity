"""Distinct mutable-parent-pointer verification of ONE existential source.

No producer source/allocator/exchange module is imported. Frozen debt DATA
are inherited, not re-proved. All new source and owner receipts are rebuilt.
"""
import collections,hashlib,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent.parent
CAP=float(sys.argv[1]);START=time.process_time();queries=0;checks=[];pins={}
M=set(range(1,14,2));E=M-{11}
def fr(x):
    if isinstance(x,(list,tuple)):return tuple(fr(y) for y in x)
    if isinstance(x,dict):return {k:fr(v) for k,v in x.items()}
    return x
def read(p):
    raw=p.read_bytes();pins[p.relative_to(P.parent).as_posix()]=hashlib.sha256(raw).hexdigest()
    return json.loads(raw)
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def tick():
    global queries
    queries+=1
    if queries>100000 or time.process_time()-START>=CAP-1:raise TimeoutError('independent cap')
def ok(name):checks.append(name);print(name,flush=True)
def mp(v):return {tuple(z['demand']):tuple(z['unit']) for z in v}

class Node:
    def __init__(self,key,parent=None):self.key=key;self.parent=parent;self.left=self.right=None
class Tree:
    def __init__(self,shape):
        self.nodes={}
        def load(t,p=None):
            if not isinstance(t,(list,tuple)):return None
            n=Node(t[0],p);self.nodes[n.key]=n;n.left=load(t[1],n);n.right=load(t[2],n);return n
        self.root=load(shape)
    def shape(self):
        def dump(n,lo,hi):
            if n is None:return 'F'+str(hi)
            return n.key,dump(n.left,lo,n.key-1),dump(n.right,n.key+1,hi)
        return dump(self.root,1,13)
    def rotate(self,n):
        p=n.parent;g=p.parent
        if p.left is n:
            p.left=n.right
            if n.right:n.right.parent=p
            n.right=p
        else:
            assert p.right is n;p.right=n.left
            if n.left:n.left.parent=p
            n.left=p
        n.parent=g;p.parent=n
        if g is None:self.root=n
        elif g.left is p:g.left=n
        else:assert g.right is p;g.right=n
    def access(self,key):
        tick();x=self.nodes[key];z=x;path=[]
        while z.parent:
            path.append('L' if z.parent.left is z else 'R');z=z.parent
        path=''.join(reversed(path));events=[]
        while x.parent:
            p=x.parent;g=p.parent
            if g is None:
                case='L' if p.left is x else 'R'
                events.append({'case':case,'P':p.key,'target':key,'kind':'ZIG'});self.rotate(x)
            else:
                a='L' if g.left is p else 'R';b='L' if p.left is x else 'R'
                events.append({'case':a+b,'G':g.key,'P':p.key,'target':key,'kind':'DOUBLE'})
                if a==b:self.rotate(p);self.rotate(x)
                else:self.rotate(x);self.rotate(x)
        assert len(events)==(len(path)+1)//2
        return path,events

def execute(state,word,start=1,expected=None):
    tt=[Tree(t) for t in state];rows=[]
    for i,(mode,x) in enumerate(word,start):
        before=tuple(t.shape() for t in tt);paths=['','',''];ev=[[],[],[]]
        paths[0],ev[0]=tt[0].access(x)
        if mode=='K':paths[1],ev[1]=tt[1].access(x)
        if mode=='K' and x!=11:paths[2],ev[2]=tt[2].access(x)
        row={'occurrence':i,'mode':mode,'target':x,'genuine_F':mode=='K' and before[1][0]!=x,
             'before':before,'after':tuple(t.shape() for t in tt),'A_path':paths[0],'BF_path':paths[1],'BE_path':paths[2],
             'A_events':ev[0],'BF_events':ev[1],'BE_events':ev[2],
             'a':len(ev[0]),'qF':len(paths[1])//2,'qE':len(paths[2])//2}
        if expected is not None:assert row==fr_row(expected[i-start]),('row',i)
        rows.append(row)
    return rows,tuple(t.shape() for t in tt)
def fr_row(r):return {k:fr(v) if k in ('before','after') else v for k,v in r.items()}
def parent_map(t):
    ans={}
    def visit(t,p=None):
        if not isinstance(t,(tuple,list)):return
        ans[t[0]]=p;visit(t[1],t[0]);visit(t[2],t[0])
    visit(t);return ans
def core(t,marks):
    if not isinstance(t,(tuple,list)):return set()
    l=core(t[1],marks);r=core(t[2],marks)
    return l|r|{t[0]} if l or r or t[0] in marks else set()
def marked(t,marks):
    pa=parent_map(t);par={};ch={k:[] for k in marks}
    for x in marks:
        p=pa[x]
        while p is not None and p not in marks:p=pa[p]
        par[x]=p
        if p is not None:ch[p].append(x)
    return par,ch
def macro_list(rows,which='F'):
    b=1 if which=='F' else 2;q='q'+which
    ends=[i for i,r in enumerate(rows) if r['mode']=='K' and (which=='F' or r['target']!=11) and r['before'][b][0]!=r['target']]
    mm=[]
    for j,end in enumerate(ends):
        prev=ends[j-1];seg=rows[prev+1:end+1] if prev<end else rows[prev+1:]+rows[:end+1]
        assert all(r[q]==0 for r in seg[:-1])
        mm.append({'rows':seg,'occurrences':[r['occurrence'] for r in seg],'H':sum(r['a'] for r in seg),
                   'Q':sum(r[q] for r in seg),'units':[(r['occurrence'],j,b) for r in seg for j in range(1,r['a']+1) for b in (0,1)],
                   'demands':[(r['occurrence'],k) for r in seg for k in range(1,r[q]+1)]})
    return mm
def leaf_map(rows):
    mm=macro_list(rows);h={};h0={};D=set();U=set();births=[];deaths=collections.defaultdict(list);led=[]
    for i,m in enumerate(mm):
        x=m['rows'][-1]['target'];pa,ch=marked(m['rows'][0]['before'][1],M);_,nc=marked(m['rows'][-1]['after'][1],M)
        anc=[];p=pa[x]
        while p is not None:anc.append(p);p=pa[p]
        assert len(anc)==m['Q'];unary=[a for a in anc if len(ch[a])==1];branch=[a for a in anc if len(ch[a])>1]
        old={a for a in M if not ch[a]};new={a for a in M if not nc[a]};z=int(x in old)
        assert new-old==set(unary) and old-new==({x} if z else set())
        if z:deaths[x].append((i,m['units'][0]))
        bd=[]
        for d,a in zip(m['demands'],anc):
            if a in unary:births.append((i,d,a))
            else:bd.append(d)
        free=m['units'][z:];n=min(len(bd),len(free));h.update(zip(bd[:n],free));h0.update(zip(m['demands'],m['units']))
        led.append({'target':x,'H':m['H'],'Q':m['Q'],'branch':branch,'z':z,'unpaid':bd[n:],'ancestors':anc,'unary':unary})
        D.update(m['demands']);U.update(m['units'])
    channels=[]
    for i,d,x in births:
        ordered=sorted(deaths[x],key=lambda z:(z[0]-i)%len(mm));j,u=ordered[-1]
        assert j!=i;h[d]=u;channels.append({'key':x,'birth':d,'birth_macro':i,'death_macro':j,'unit':u})
    assert len(set(h.values()))==len(h) and set(h.values())<=U
    return mm,led,h,h0,D,U,channels

def creator_stage(rows,mm,led,h,channels):
    births=[]
    for ri,r in enumerate(rows):
        before=parent_map(r['before'][0]);after=parent_map(r['after'][0]);v=r['target'];groups=collections.defaultdict(list)
        for x in sorted(M):
            p=after[x]
            if p is None or p==before[x] or x==v:continue
            outer=True;g=after[p]
            while g is not None:
                if (x<p and g<p) or (x>p and g>p):outer=False
                g=after[g]
            operand=x if p==v else p
            es=[j for j,e in enumerate(r['A_events'],1) if operand in (e.get('G'),e.get('P'))];assert len(es)==1
            z={'ri':ri,'edge':(p,x),'occ':r['occurrence'],'event':es[0],'qualified':p not in M or outer,'unit':None}
            births.append(z)
            if z['qualified']:groups[es[0]].append(z)
        for j,zz in groups.items():
            assert len(zz)<=2
            for bit,z in enumerate(sorted(zz,key=lambda t:t['edge'])):z['unit']=(r['occurrence'],j,bit)
    claims=[];rowpos={r['occurrence']:i for i,r in enumerate(rows)};owner_macro={t:i for i,m in enumerate(mm) for t in m['occurrences']}
    for i,m in enumerate(mm):
        l=led[i]
        if (l['H'],l['Q'],len(l['branch']),l['z'])!=(1,2,2,1):continue
        for d in l['unpaid']:
            rr=[r for r in m['rows'] if r['a']];assert len(rr)==1;r=rr[0];ri=rowpos[r['occurrence']];x=l['target'];pa=parent_map(r['before'][0])
            edge=(pa[x],x) if pa[x] not in M or len(r['A_path'])==1 else (r['before'][0][0],pa[x])
            options=[z for z in births if z['edge']==edge];assert options
            c=max(options,key=lambda z:(z['ri']-ri)%len(rows));assert c['qualified'] and c['ri']!=ri
            claims.append({'frontier':d,'edge':edge,'creator':c,'creator_macro':owner_macro[c['occ']]})
    assert len({c['creator']['unit'] for c in claims})==len(claims)
    paid=[];hc=dict(h)
    for mi in sorted({c['creator_macro'] for c in claims}):
        group=sorted([c for c in claims if c['creator_macro']==mi],key=lambda c:c['frontier']);l=led[mi]
        tail=mm[mi]['units'][min(2*l['H'],len(l['branch'])+l['z']):];n=min(len(group),len(tail))
        for c,u in zip(group[:n],tail[-n:] if n else []):
            d=c['frontier'];assert d not in hc and u not in hc.values();hc[d]=u;paid.append((d,u))
    tr=[]
    for c in sorted(claims,key=lambda c:c['frontier']):
        d=c['frontier']
        if d in hc:continue
        i=next(i for i,l in enumerate(led) if d in l['unpaid']);z=next(z for z in channels if z['death_macro']==i and z['key']==led[i]['target'])
        tr.append({'origin':d,'key':z['key'],'birth':z['birth'],'death_macro':i,'birth_macro':z['birth_macro']})
    return claims,paid,hc,tr

def extend(a,h,D):
    inverse={u:d for d,u in a.items()};new={}
    def endpoint(d,seen):
        assert d not in seen;seen.add(d)
        if d not in h:return None
        u=h[d]
        return u if u not in inverse else endpoint(inverse[u],seen)
    for d in sorted(D-set(a)):
        u=endpoint(d,set())
        if u is not None:new[d]=u
    ans=dict(a);ans.update(new);assert len(set(ans.values()))==len(ans)
    return ans
def natural_extend(lock,h):return extend(lock,h,set(h)|set(lock))
def buffer_peak(a):
    timeline=[]
    for d,u in a.items():timeline.extend([((u[0],0,u[1],u[2]),d),((d[0],1,d[1],0),d)])
    seen=set();peak=0
    for t,d in sorted(timeline):
        if d in seen:seen.remove(d)
        else:seen.add(d);peak=max(peak,len(seen))
    assert not seen;return peak

def debt_function(rows):
    home=P/'SE03_STEP2_UNARY_A_LIFT_14';S=core(rows[0]['before'][2],E);k=len(S);rank={v:i+1 for i,v in enumerate(sorted(S))}
    mask=tuple(sorted(rank[x] for x in E));mir=tuple(sorted(k+1-x for x in mask));flip=mask>mir;rep=mir if flip else mask
    info=read(home/'branch_all_construction.json');entry=next(z for z in info['reports'] if z['core']==k and tuple(z['marks'])==rep)
    assert entry['status']=='CANDIDATE_COMPLETE';cert=read(home/entry['file']);read(home/('audit_'+entry['file']))
    grammar=read(home/'branch_grammar2.json');states=[fr(t) for t in grammar['states']];groups=collections.defaultdict(list)
    for t in states:groups[t[0]//1000].append(t)
    positions={t:j for ts in groups.values() for j,t in enumerate(ts)};offset={};n=0
    for t in cert['BF_trees']:
        t=fr(t);offset[t]=n;n+=len(groups[rep.index(t[0])+1])
    assert n==len(cert['debt']);markrank={x:1000*(i+1) for i,x in enumerate(sorted(E))}
    def aproj(t):
        if not isinstance(t,tuple):return None
        a,b=aproj(t[1]),aproj(t[2])
        if t[0] in E:return markrank[t[0]],a,b
        if a is None:return b
        if b is None:return a
        return 1000*sum(x<t[0] for x in E)+500,a,b
    def bproj(t,hi=k):
        if not isinstance(t,tuple) or t[0] not in S:return 'F'+str(hi)
        a=rank[t[0]];return a,bproj(t[1],a-1),bproj(t[2],hi)
    def ra(t):return None if t is None else (7000-t[0],ra(t[2]),ra(t[1]))
    def rb(t):return 'F'+str(k-int(t[1:])) if isinstance(t,str) else (k+1-t[0],rb(t[2]),rb(t[1]))
    def value(a,b):
        a,b=aproj(a),bproj(b)
        if flip:a,b=ra(a),rb(b)
        return cert['debt'][offset[b]+positions[a]]
    return value,{'core':k,'mask':mask,'representative':rep,'reflected':flip,'certificate':entry['file']}

def audit_bank(rows,report):
    mm=macro_list(rows,'E');used=set();packets=[]
    for i,m in enumerate(mm):
        if m['Q']==5:
            j=(i+1)%len(mm);assert mm[j]['Q']==1 and i not in used and j not in used;used|={i,j};packets.append(([i,j],m['rows']+mm[j]['rows']))
    for i,m in enumerate(mm):
        if i not in used:assert m['Q']<=4;packets.append(([i],m['rows']))
    packets.sort(key=lambda z:min(z[0]));value,meta=debt_function(rows);maxd=0;dd=[]
    for ids,rr in packets:
        ds=value(rr[0]['before'][0],rr[0]['before'][2]);dt=value(rr[-1]['after'][0],rr[-1]['after'][2]);H=sum(r['a'] for r in rr);Q=sum(r['qE'] for r in rr)
        assert 2*min(H,4)-Q+dt-ds>=0;dd.append((ds,dt));maxd=max(maxd,ds)
    assert maxd==report['h6_max_debt']==2 and dd[0][0]==maxd
    natural={d:u for m in mm for d,u in zip(m['demands'],m['units'])};h=dict(natural);bank=[];peak=0
    for pi,((ids,rr),(ds,dt),receipt) in enumerate(zip(packets,dd,report['h6_packet_receipts'])):
        assert len(bank)==maxd-ds
        units=[(r['occurrence'],j,b) for r in rr for j in range(1,r['a']+1) for b in (0,1)]
        demands=[(r['occurrence'],k) for r in rr for k in range(1,r['qE']+1)];owned={natural[d] for d in demands if d in natural};missing=[d for d in demands if d not in natural]
        budget=2*min(sum(r['a'] for r in rr),4);spare=[u for u in units if u not in owned][:budget-len(owned)];pool=spare+bank
        assert len(pool)>=len(missing)+maxd-dt;peak=max(peak,len(pool)+len(owned));new=[]
        for d in missing:u=pool.pop(0);h[d]=u;new.append((d,u))
        bank=pool[:maxd-dt]
        computed={'packet':pi,'macro_indices':ids,'occurrences':[r['occurrence'] for r in rr],'H':sum(r['a'] for r in rr),
                  'Q':sum(r['qE'] for r in rr),'w':budget-sum(r['qE'] for r in rr),'D_before':ds,'D_after':dt,
                  'selected_spares':spare,'fixed_own_units':sorted(owned),'new_pairs':new,'carry':bank[:]}
        assert fr(computed)==fr(receipt),('bank',pi,computed,receipt)
    assert not bank and h==mp(report['f6']) and natural==mp(report['h6_natural'])
    assert len(set(h.values()))==len(h) and peak==report['working_peaks']['raw_h6_working']<=25
    assert len(h)==sum(r['qE'] for r in rows)
    meta.update(max_debt=maxd,working_peak=peak,packets=len(packets));return h,meta

def main():
    report=read(B/'aligned_source_and_owners.json');V=fr(report['original_common_tree']);prefix=report['reaching_prefix'];word=report['period'];start,stop=report['actual_interval'];tags=report['tags']
    assert start==len(prefix)+1 and stop==len(prefix)+len(word) and len(word)==199
    _,initial=execute((V,V,V),prefix);assert initial==fr(report['initial']);rows,end=execute(initial,word,start,report['rows']);assert initial==end
    assert {r['target'] for r in rows if r['mode']=='K'}==M
    for r in rows:
        assert set(parent_map(r['before'][0]))==set(range(1,14));assert core(r['before'][1],M)==set(range(1,14))
        assert len(core(r['before'][2],E))==9
        if r['mode']=='K':
            assert all(ev['case'] in ('LL','RR') and ev['G'] in M and ev['P'] not in M for ev in r['BF_events'])
    ok('S1/S7/S8/S9/S11: actual mutable A/BF/BE prefix, all rotations, ordered inventories, core13/core9 and exact closure')
    by={r['occurrence']:r for r in rows};assert [tags[k] for k in ('j','h','g','s','t','v','p','e')]==list(range(tags['j'],tags['e']+1))
    assert [by[tags[k]]['target'] for k in ('j','h','g','s','t','v','p','e')]==[13,1,13,11,1,13,1,7]
    assert [by[tags[k]]['qF'] for k in ('j','h','g','s','t','v','p','e')]==[1,2,1,3,1,2,1,6]
    assert all(by[tags[k]]['a']==1 for k in ('h','g','s','t','v','p','e'))
    assert [by[tags[k]]['qE'] for k in ('v','p','e')]==[1,1,4]
    ok('S2: consecutive original j,h,g,s,t,v,p,e macros, all DELETEs/root repeats retained')
    f6,bankmeta=audit_bank(rows,report);uv=tuple(report['uv']);ed=(tags['e'],4)
    rv=next(z for z in report['h6_packet_receipts'] if tags['v'] in z['occurrences']);rp=next(z for z in report['h6_packet_receipts'] if tags['p'] in z['occurrences']);re=next(z for z in report['h6_packet_receipts'] if tags['e'] in z['occurrences'])
    assert rp['carry'][1]==list(uv) and len(rp['carry'])==2 and rp['D_before']==0 and rp['D_after']==0
    assert f6[ed]==uv and (ed,uv) in [(tuple(d),tuple(u)) for d,u in re['new_pairs']]
    assert not any(uv==tuple(u) for z in report['h6_packet_receipts'] if z['packet']<re['packet'] for d,u in z['new_pairs'])
    assert by[tags['v']]['before'][2][0]==1 and by[tags['v']]['after'][2][0]==13 and by[tags['p']]['after'][2][0]==1
    ok('S3/S4/S5/S12: actual epsilon1, v/p rank/carry2, e4 first consumption, maximum-debt cut and canonical high-core bank')
    # Independently establish that the special original Step1 core9 domain is
    # not applicable to ANY possible extra erasure of this six-key source.
    domains=[]
    for z in sorted(E):
        t=Tree(V)
        for mode,x in prefix:
            if mode=='K' and x not in (11,z):t.access(x)
        seen={};seq=[]
        while t.shape() not in seen:
            assert len(seq)<30;seen[t.shape()]=len(seq);seq.append(t.shape())
            for mode,x in word:
                if mode=='K' and x not in (11,z):t.access(x)
        rec=seq[seen[t.shape()]:];assert len(rec)==1
        cores={len(core(q,M-{11,z})) for q in rec};assert len(cores)==1 and 9 not in cores
        domains.append({'additional_erasure':z,'recurrent_core':next(iter(cores))})
    assert [z['recurrent_core'] for z in domains]==[z['core'] for z in report['original_Step1_domains']]
    ok('S10 older-common: all six extra erasures checked; original five-key/core9 Step1 domain absent, canonical raw f6 branch is applicable')
    mm,led,h,h0,D,U,channels=leaf_map(rows);assert h==mp(report['leaf_comparison']) and h0==mp(report['full_h0'])
    claims,paid,hc,tr=creator_stage(rows,mm,led,h,channels)
    assert {tuple(z['demand']):tuple(z['unit']) for z in report['creator_pairs']}==dict(paid)
    assert fr(tr)==fr(report['selected_transports'])
    at_e=[z for z in tr if z['birth'][0]==tags['e']];assert len(at_e)==2 and {z['key'] for z in at_e}=={5,9}
    assert {z['birth'][1] for z in at_e}=={1,2} and all(z['origin'][0]<tags['j'] for z in at_e)
    for z in at_e:
        c=next(c for c in claims if c['frontier']==z['origin']);l=led[c['creator_macro']]
        assert l['H']==1 and len(l['branch'])+l['z']>=2
    assert (tags['e'],1,1) not in {u for d,u in paid}
    ok('S6: exactly two selected creator-unpaid original zero lifetimes, keys9/5, next births e1/e2, c_e=0')
    lock={d:u for d,u in f6.items() if d in D};assert lock==mp(report['common_locked']);a=natural_extend(lock,h0);assert a==mp(report['natural_prior'])
    ht=dict(hc)
    for z in tr:ht[z['origin']]=ht.pop(z['birth'])
    hp=dict(ht);groups=collections.defaultdict(list);own=[]
    for z in tr:groups[z['birth_macro']].append(z['birth'])
    for mi,ds in sorted(groups.items()):
        free=[u for u in mm[mi]['units'] if u not in hp.values()]
        for d,u in zip(sorted(ds),free):hp[d]=u;own.append((d,u))
    assert own==[(tuple(z['demand']),tuple(z['unit'])) for z in report['own_tail_pairs']]
    hj=dict(hp);jd=tuple(report['j_donor']);assert jd==next(m for m in mm if tags['j'] in m['occurrences'])['units'][2] and jd not in hp.values()
    missing=[z['birth'] for z in at_e if z['birth'] not in hp];assert len(missing)==1;hj[missing[0]]=jd
    for stage,hx in zip(report['policy_stages'],[h,hc,ht,hp,hj]):
        assert hx==mp(stage['comparison']) and a==mp(stage['prior']);before=dict(a);a=extend(a,hx,D)
        assert a==mp(stage['after']) and all(a[d]==u for d,u in before.items())
    gd=tuple(report['source_gap_donor']);gap=next(m for m in mm if tags['gap1'] in m['occurrences']);assert gap['H']>=8 and gd==gap['units'][8]
    assert gd not in set(f6.values())|set(h0.values())|set(hj.values())|set(a.values())
    unpaid=D-set(a);assert unpaid=={tuple(report['extra_payment']['demand'])};a[next(iter(unpaid))]=gd
    assert a==mp(report['final_full_allocation']) and set(a)==D and len(set(a.values()))==len(a) and set(a.values())<=U
    assert a[ed]==uv and all(a[d]==u for d,u in lock.items())
    assert all(start<=u[0]<=stop and start<=d[0]<=stop for d,u in a.items())
    assert sum(r['a'] for r in rows)==report['A'] and sum(r['qF'] for r in rows)==report['QF'] and sum(r['qE'] for r in rows)==report['QE']
    ok('S10/S13: all full frozen-success policy stages rebuilt, e4 remains effective owner, explicit single-word completion, no duplicate bits')
    sh=Tree(by[tags['h']]['after'][0]);path,events=sh.access(7)
    assert sh.shape()==by[tags['e']]['after'][0] and len(events)==2 and path==report['flip']['shadow_e_path']
    assert sum(by[tags[k]]['a'] for k in ('g','s','t','v','p'))==5
    assert sum(by[tags[k]]['qF'] for k in ('g','s','t','v','p'))==8
    assert {tuple(z) for z in report['flip']['repair_units']}=={(tags['p'],1,0),(tags['p'],1,1)}<=U
    assert report['flip']['corrected_R_balance']==0
    ok('S7 signed comparison: nonidentity R excision, shadow extra event, exact whole-tree rejoin and actual p-bit correction retained')
    assert buffer_peak(f6)==report['working_peaks']['f6_endpoint_buffer']==4
    assert buffer_peak(a)==report['working_peaks']['full_frozen_endpoint_buffer']==6
    assert max(report['working_peaks'].values())<=25
    ok('S12/S13: one absolute period573..771; empty endpoint buffers at seam, raw bank10 and full buffer6 below Bank25')
    # Non-vacuous adversarial receipt controls, without new source search.
    def legal_map(z):return set(z)<=D and set(z.values())<=U and len(set(z.values()))==len(z) and all(z.get(d)==u for d,u in lock.items())
    corrupt=dict(a);keys=sorted(D);corrupt[keys[1]]=corrupt[keys[0]];assert not legal_map(corrupt)
    corrupt=dict(a);corrupt[ed]=(uv[0]-199,uv[1],uv[2]);assert not legal_map(corrupt)
    corrupt=dict(a);corrupt[ed]=gd;assert not legal_map(corrupt)
    assert by[tags['e']]['qE']!=3 and by[tags['zero5']]['a']==1
    ok('Adversarial controls: duplicate donor, neighboring-copy donor and moved frozen e4 owner rejected')
    out('independent_audit2.json',{'status':'PASS_DISTINCT_IMPLEMENTATION_EXACT_EXISTENTIAL_WITNESS',
        'scope':'G27(W*) source nonemptiness, not universal funding or Gate U; inherited debt theorem not re-audited',
        'method':'new mutable parent-pointer splays and independent source, debt-table lookup, bank, leaf/creator/T19 and recursive frozen-owner reconstruction; no producer code imported',
        'trust':'distinct implementation operated by the same research agent; neither external review nor proof-assistant verification',
        'checks':checks,'input_sha256':pins,'interval':[start,stop],'source_length':len(word),'source_queries':queries,
        'A':report['A'],'QF':report['QF'],'QE':report['QE'],'bank':bankmeta,'older_Step1_domains':domains,
        'selected_at_e':at_e,'uv':uv,'uv_owner':ed,'all_frozen_successes_preserved':True,
        'Bank25_peaks':report['working_peaks'],'outcome':'A — E4 SOURCE REALIZABLE'})
    print(json.dumps({'status':'INDEPENDENT_PASS','checks':len(checks),'source_queries':queries}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_independent2_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,
        'source_engine_calls':queries,'source_queries':queries})
