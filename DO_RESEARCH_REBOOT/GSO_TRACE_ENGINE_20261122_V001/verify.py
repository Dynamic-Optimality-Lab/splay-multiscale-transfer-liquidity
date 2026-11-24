"""Independent immutable trace/port/projection and resource verification.

Imports none of the new trace, learner, bank producer or network builders.
Uses sealed immutable physical rotations; projection is two BST splits.
Exact bank conservation is checked from the original StepEv inventory.
"""
import sys
import json
import gzip
import importlib.util
import time
from pathlib import Path
from collections import Counter,defaultdict
from fractions import Fraction
sys.dont_write_bytecode=True
sys.setrecursionlimit(20000)
HERE=Path(__file__).resolve().parent;PREV=HERE.parent/'GSO_COMPOSITION_AUDIT_20261121_V001'
spec=importlib.util.spec_from_file_location('trace_pinned_independent_primitives',PREV/'verify.py');C=importlib.util.module_from_spec(spec);sys.modules[spec.name]=C;spec.loader.exec_module(C)
P=C.P;V=P.V


def read(p):
    with (gzip.open(p,'rt',encoding='utf-8') if p.suffix=='.gz' else p.open(encoding='utf-8')) as f:return json.load(f)


def canon(v):return json.loads(json.dumps(v))


def describe(t):
    ch={};parent={};stack=[(t,None)]
    while stack:
        v,p=stack.pop();parent[v.k]=p;ch[v.k]=[v.l.k if v.l else None,v.r.k if v.r else None];stack.extend((h,v.k) for h in (v.l,v.r) if h)
    return ch,parent


def ports(t,part,owner):
    out=[];members=set(part)
    if t.k in members:out.append(['root',t.k])
    stack=[t]
    while stack:
        v=stack.pop()
        for side,h in enumerate((v.l,v.r)):
            if not h:continue
            stack.append(h)
            if owner[v.k]==owner[h.k]:continue
            if v.k in members:out.append(['out',v.k,h.k,'LR'[side]])
            if h.k in members:out.append(['in',v.k,h.k,'LR'[side]])
    return sorted(out,key=str)


def signature(pair,part,owner):
    rank={x:i for i,x in enumerate(part)}
    def one(t):
        ch,pa=describe(t)
        def ref(x):return 'nil' if x is None else rank[x] if x in rank else 'lo' if x<part[0] else 'hi'
        def rel(z):return [rank[z.k],rel(z.l),rel(z.r)] if z else None
        shape=rel(C.restrict(t,part[0],part[-1]));stub=[[ref(pa[x]),ref(ch[x][0]),ref(ch[x][1])] for x in part]
        return [shape,stub]
    return json.dumps([len(part),one(pair['A']),one(pair['B'])],separators=(',',':'))


def bank_check(z,cert):
    owner={x:i for i,p in enumerate(z['blocks']) for x in p};ev=[]
    for r in z['operations']:
        if r['k']:ev.append({'id':['K',r['id']],'a':0,'q':0,'k':1,'scope':[owner[r['target']]]})
        ev.extend(z['steps'][r['steps'][0]:r['steps'][1]])
    c,d,H=cert['c'],cert['d'],cert['capacity'];assert all(type(v)==int and v>=0 for v in (c,d,H))
    inf=z['Q_B']+c*z['A']+d*z['K_B']+1;edges={};vertices={'s','t'};initial={i:f'b{i}:0' for i in range(len(z['blocks']))};last=initial.copy();cnt=Counter();demand_edges=[];supplies=[]
    def add(u,v,cap):assert (u,v) not in edges;edges[u,v]=cap;vertices.update((u,v))
    for j,e in enumerate(ev):
        hub=f'e{j}'
        for i in e['scope']:
            add(last[i],hub,inf);cnt[i]+=1;last[i]=f'b{i}:{cnt[i]}';add(hub,last[i],H)
        supply=c*e['a']+d*e.get('k',0)
        if supply:add('s',hub,supply);supplies.append((hub,e))
        if e['q']:add(hub,'t',e['q']);demand_edges.append(hub)
    for i in initial:
        if last[i]!=initial[i]:add(last[i],initial[i],H)
    inc=Counter();out=Counter();seen=set();flow={}
    for u,v,w in cert['positive_flows']:
        assert (u,v) not in seen and type(w)==int and 0<w<=edges[u,v];seen.add((u,v));flow[u,v]=w;out[u]+=w;inc[v]+=w
    assert all(inc[v]==out[v] for v in vertices if v not in ('s','t'))
    assert inc['t']==out['s']==cert['paid']==cert['issued_credit']
    assert out['s']<=c*z['A']+d*z['K_B']
    if cert['status']=='FINITE_EXACT_BANK':assert all(flow.get((u,'t'),0)==1 for u in demand_edges) and cert['paid']==z['Q_B']
    else:
        cut=cert['cut'];left=set(cut['left']);right=set(cut['right']);assert left|right==vertices and not left&right and 's' in left and 't' in right
        assert sum(cap for (u,v),cap in edges.items() if u in left and v in right)==cert['paid']<z['Q_B']
    return {'status':cert['status'],'paid':cert['paid'],'Q_B':z['Q_B'],'cyclic_balances_conserved':True,'A_issuance_units':sum(e['a'] for e in ev),'KEEP_vouchers':sum(e.get('k',0) for e in ev),'prefix_credit':0}


def verify_trace(i,original=True):
    z=read(HERE/f'run_001/trace_{i:02d}.json.gz');s=z['source'];parts=z['blocks'];owner={x:j for j,b in enumerate(parts) for x in b}
    assert all(b==list(range(b[0],b[-1]+1)) for b in parts)
    if original:
        comp=PREV/'original_event_companions'/f'source_{i:02d}.json.gz' if i<13 else HERE/'original_event_companions'/f'trace_{i:02d}.json.gz'
        orig=P.verify_source(comp);saved=read(comp);assert saved['source']==s and saved['original_U']==z['original_U'] and saved['original_S']==z['original_S']
    trees={a:P.from_state(s['initial_'+a]) for a in ('A','B')};pos=0;A=Q=KB=R_A=messages=0;mask=Counter();zero_ops=[]
    for op,((mode,x),r) in enumerate(zip(s['operations'],z['operations']),1):
        assert [op,mode,x]==[r['id'],r['mode'],r['target']]
        before=trees.copy();bh=Counter(signature(trees,b,owner) for b in parts);k=int(mode=='K' and trees['B'].k!=x);KB+=k;opa=opq=0;assert r['steps'][0]==pos
        for actor in ('A','B') if mode=='K' else ('A',):
            emitted=[]
            def emit(step,bit,typ,promoted,pivot,demoted):emitted.append([step,bit,typ,promoted.k,pivot.k]);return 0
            expected,depth=P.splay(trees[actor],x,emit)
            if actor=='A':opa=(depth+1)//2
            else:opq=depth//2
            for step in sorted({v[0] for v in emitted}):
                row=z['steps'][pos];pos+=1;bits=[v for v in emitted if v[0]==step]
                assert row['id']==[actor,op,step] and row['type']==bits[0][2] and row['target']==x
                assert row['a']==int(actor=='A') and row['q']==int(actor=='B' and len(bits)==2) and row['k']==0
                old=trees.copy();scope=set();inside=[]
                for st,bit,typ,y,p in bits:
                    ch,pa=describe(trees[actor]);grand=pa[p];middle=ch[y][int(y<p)];footprint={owner[v] for v in (y,p,grand,middle) if v is not None};scope|=footprint
                    bp={j:ports(trees[actor],parts[j],owner) for j in footprint};new=C.rotated(trees[actor],p,y);ap={j:ports(new,parts[j],owner) for j in footprint}
                    packet=[{'block':j,'before':bp[j],'after':ap[j]} for j in sorted(footprint) if bp[j]!=ap[j]]
                    idx=owner[y] if owner[y]==owner[p] else None;inside.append(idx)
                    saved_bit=row['bits'][bit]
                    assert saved_bit=={'id':[actor,op,step,bit],'promoted':y,'demoted':p,'grandparent':grand,'middle':middle,'internal_block':idx,'footprint':sorted(footprint),'port_packets':packet}
                    assert len(packet)<=4
                    for j,b in enumerate(parts):
                        earlier=C.restrict(trees[actor],b[0],b[-1]);later=C.restrict(new,b[0],b[-1]);exp=C.rotated(earlier,p,y) if idx==j else earlier
                        assert P.raw(later)==P.raw(exp)
                        if j not in footprint:assert ports(trees[actor],b,owner)==ports(new,b,owner)
                    if actor=='A':messages+=len(packet);R_A+=1
                    trees[actor]=new
                assert sorted(scope)==row['scope']
                assert row['retained_bit_masks']=={str(j):[int(v==j) for v in inside] for j in sorted(scope)}
                assert len({j for j in inside if j is not None})<=1
                for j in scope:
                    assert row['before_local'][str(j)]=={a:canon(P.raw(C.restrict(old[a],parts[j][0],parts[j][-1]))) for a in trees}
                    assert row['after_local'][str(j)]=={a:canon(P.raw(C.restrict(trees[a],parts[j][0],parts[j][-1]))) for a in trees}
                    assert row['signature_before'][str(j)]==signature(old,parts[j],owner) and row['signature_after'][str(j)]==signature(trees,parts[j],owner)
                if row['q']:mask.update(''.join(map(str,v)) for v in row['retained_bit_masks'].values())
            assert P.raw(trees[actor])==P.raw(expected)
        A+=opa;Q+=opq;assert [r['a'],r['q'],r['k'],r['steps'][1]]==[opa,opq,k,pos]
        assert all(P.raw(trees[a])==P.raw(P.from_state(r['full_after'][a])) and P.raw(before[a])==P.raw(P.from_state(r['full_before'][a])) for a in trees)
        ah=Counter(signature(trees,b,owner) for b in parts);delta=ah.copy();delta.subtract(bh);assert {s:v for s,v in delta.items() if v}==r['delta']
        unchanged=all(P.raw(C.restrict(before[a],b[0],b[-1]))==P.raw(C.restrict(trees[a],b[0],b[-1])) for a in trees for b in parts);assert unchanged==r['local_only_unchanged']
        if unchanged and opq>opa:zero_ops.append({'op':op,'a':opa,'q':opq,'k':k})
    assert pos==len(z['steps']) and (A,Q,KB,R_A,messages)==(z['A'],z['Q_B'],z['K_B'],z['R_A'],z['A_port_packets'])
    assert KB<=A and R_A<=2*A and messages<=4*R_A<=8*A
    assert all(P.raw(trees[a])==P.raw(P.from_state(s['initial_'+a])) for a in trees)
    b=bank_check(z,read(HERE/f'run_001/bank_{i:02d}.json.gz'))
    return {'index':i,'name':s['name'],'A':A,'Q_B':Q,'K_B':KB,'operations':len(z['operations']),'steps':pos,'real_rotations':sum(len(s['bits']) for s in z['steps']),'literal_U':len(z['original_U']),'A_port_packets':messages,'masks':dict(mask),'invisible_costly':zero_ops,'bank':b,'full_original_Pi_checked':original}


def main():
    start=time.perf_counter();rows=[]
    for i in range(18):
        row=verify_trace(i);rows.append(row);print(json.dumps({'verified':i,'name':row['name'],'steps':row['steps']}),flush=True)
    pot=read(HERE/'run_001/FINITE_RELAXED_CANDIDATE.json');data=read(HERE/'run_001/POTENTIAL_ROWS.json.gz')
    if pot['status']=='FINITE_EXACT':
        pp={s:Fraction(v) for s,v in pot['values'].items()};c=Fraction(pot['c']);d=Fraction(pot['d']);assert c>=0 and d>=0
        assert all(r['q']+sum(v*pp[s] for s,v in r['delta'].items())<=c*r['a']+d*r['k'] for r in data)
    out={'passed':True,'sources':rows,'original_operations':sum(r['operations'] for r in rows),'original_steps':sum(r['steps'] for r in rows),'real_rotations':sum(r['real_rotations'] for r in rows),'literal_U':sum(r['literal_U'] for r in rows),'finite_potential_exact':pot['status']=='FINITE_EXACT','seconds':time.perf_counter()-start,'trust':'Independent immutable physical implementation, two-split projection and separately reconstructed bank network. Same agent, not external peer review; no universal proof inferred.','root_status':'OPEN'}
    if not (HERE/'FINAL_MANIFEST.json').exists():(HERE/'INDEPENDENT_VERIFICATION.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k!='sources'}))


if __name__=='__main__':main()
