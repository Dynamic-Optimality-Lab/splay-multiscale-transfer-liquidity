"""Independent immutable original-event, predicate and allocation verification.

Imports only source data extraction and the previous sealed immutable primitive
library. No mutable replay, optimizer or eligibility predicate is imported.
"""
import bisect
import importlib.util
import json
import sys
import time
from collections import Counter,defaultdict
from pathlib import Path

sys.dont_write_bytecode=True
sys.setrecursionlimit(50000)
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
from sources import canonical
spec=importlib.util.spec_from_file_location('theta1_sealed_immutable',ROOT/'DO_RESEARCH_REBOOT/COVER_FLOW_AUDIT_20261121_V001/verify.py')
V=importlib.util.module_from_spec(spec);sys.modules[spec.name]=V;spec.loader.exec_module(V)
START=time.process_time()


def tree(state):
    ch={int(k):v for k,v in state['children'].items()};values={None:None};stack=[(state['root'],False)]
    while stack:
        k,done=stack.pop()
        if done:
            l,r=ch[k];values[k]=V.node(k,values[l],values[r])
        else:
            stack.append((k,True));stack.extend((c,False) for c in ch[k] if c is not None)
    return values[state['root']]


def state(t):
    root=t.k;out={};stack=[t]
    while stack:
        q=stack.pop();out[str(q.k)]=[q.l.k if q.l else None,q.r.k if q.r else None]
        if q.l:stack.append(q.l)
        if q.r:stack.append(q.r)
    return {'root':root,'children':out}


def walk(t,x):
    result=[]
    while t:
        result.append(t.k)
        if t.k==x:return result
        t=t.l if x<t.k else t.r
    raise AssertionError('missing key')


def cover(t,a,b):
    while t.k<a or t.k>b:t=t.r if t.k<a else t.l
    return t


def validate(file):
    saved=json.loads(file.read_text(encoding='utf-8'));s=canonical(saved['ref'])
    keys=sorted(map(int,s['initial_A']['children']));initial={a:tree(s['initial_'+a]) for a in ('A','B')}
    keep=[];previous=initial['B'].k
    for mode,x in s['operations']:
        if mode=='K':
            if x!=previous:keep.append(x)
            previous=x
    S=sorted({k for x in set(keep) for k in walk(initial['B'],x)})
    assert S==saved['S']
    def label(t):
        lo=bisect.bisect_left(S,t.lo);hi=bisect.bisect_right(S,t.hi)
        return (lo+1,hi) if hi>lo else None
    def census(t):
        out=Counter();stack=[t]
        while stack:
            v=stack.pop();z=label(v)
            if z:out[z]+=1
            if v.l:stack.append(v.l)
            if v.r:stack.append(v.r)
        return out
    if s.get('diagonal') is not None:
        reaching={a:tree(s['diagonal']) for a in ('A','B')};reachrot=0
        for mode,x in s['prefix']:
            for a in ('A','B') if mode=='K' else ('A',):
                reaching[a],depth=V.rebuild(reaching[a],x,lambda *z:0,lambda *z:None);reachrot+=depth
        assert all(state(reaching[a])==s['initial_'+a] for a in ('A','B'))
    else:
        assert s['initial_A']==s['initial_B'] and not s['prefix'];reachrot=0
    assert reachrot==saved['prefix_rotations']
    trees=initial.copy();counts={a:census(t) for a,t in trees.items()};initial_set=set(counts['A'])
    assignment=saved['allocation']['assignment'];K=saved['allocation']['K']
    assert len(assignment)==len(saved['demands'])
    demands_by_unit=defaultdict(list);assigned=set();load=Counter()
    for idx,unit in assignment:
        assert idx not in assigned and unit[0]=='A' and unit[3]==0
        assigned.add(idx);demands_by_unit[tuple(unit)].append(idx);load[tuple(unit)]+=1
    assert (max(load.values()) if load else 0)<=K
    eligibility={i:False for i in assigned};unit_pivots=defaultdict(set)
    lower=saved['allocation']['lower_cut'];cutspans=set()
    if lower:
        cutspans={tuple(saved['demands'][i]['span']) for i in lower['demand_indices']}
    cut_neighbors=set();clock=A=Q=R=0;root_only=True
    born,removed,changes=defaultdict(list),defaultdict(list),defaultdict(list)
    doubles=[]
    for op,(mode,target) in enumerate(s['operations'],1):
        clock+=1
        for actor in ('A','B') if mode=='K' else ('A',):
            if actor=='B':clock+=1;postA=clock
            def emit(step,bit,typ,promoted,pivot,demoted):
                nonlocal clock,R,root_only
                clock+=1;R+=1
                identifier=[actor,op,step,bit]
                old=label(promoted);new=label(demoted);h=label(pivot)
                possibilities={x for x in (old,new) if x is not None}
                before={x:counts[actor][x] for x in possibilities}
                if old:counts[actor][old]-=1
                if new:counts[actor][new]+=1
                lost={x for x in possibilities if before[x] and not counts[actor][x]}
                gain={x for x in possibilities if not before[x] and counts[actor][x]}
                if actor=='A':
                    for x in lost:changes[x].append((clock,False,identifier))
                    for x in gain:changes[x].append((clock,True,identifier))
                    unit=('A',op,step,0);unit_pivots[unit].update((promoted.k,pivot.k))
                    root_only &= (pivot.lo,pivot.hi)==(keys[0],keys[-1])
                    def actual(a,b):
                        if a<=promoted.k<=b and a<=pivot.k<=b:return True
                        if not (pivot.lo<=a and b<=pivot.hi):return False
                        changed=V.right(pivot) if promoted.k<pivot.k else V.left(pivot)
                        # Literal physical LCA on each whole bit frame; if an
                        # endpoint is outside it, the unchanged external LCA
                        # handles both snapshots and no cover change occurs.
                        return label(cover(pivot,a,b))!=label(cover(changed,a,b))
                    for idx in demands_by_unit.get(unit,[]):
                        eligibility[idx] |= actual(*saved['demands'][idx]['span'])
                    if cutspans and any(actual(a,b) for a,b in cutspans):cut_neighbors.add(unit)
                    return 0
                assert promoted.k in S and pivot.k in S and len(lost)==len(gain)==1
                for x in lost:removed[x].append((clock,identifier))
                for x in gain:born[x].append((clock,identifier))
                out=next(iter(gain));delta=-int(counts['A'][out]>0)
                return delta
            def double(step,typ,span,a,b):
                if actor=='B':
                    lo=bisect.bisect_left(S,span[0]);hi=bisect.bisect_right(S,span[1])
                    doubles.append({'id':[op,step],'F':(lo+1,hi),'neutral':a==b==0,'postA':postA})
            trees[actor],depth=V.rebuild(trees[actor],target,emit,double)
            if actor=='A':A+=(depth+1)//2
            else:Q+=depth//2
        if mode!='K':clock+=1
        clock+=1
        assert time.process_time()-START<=360
    assert all(state(trees[a])==s['initial_'+a] for a in ('A','B'))
    assert (A,Q,R,clock)==(saved['A'],saved['Q_B'],saved['period_rotations'],saved['period_clock'])
    assert len(unit_pivots)==A and all(x in unit_pivots for x in load)
    assert all(eligibility.values()) and root_only==saved['root_rotations_only']
    def previous(seq,end):
        cycle,local=divmod(end,clock);i=bisect.bisect_left([t for t,_ in seq],local)-1
        if i<0:cycle-=1;i=len(seq)-1
        t,eid=seq[i];return cycle*clock+t,eid
    actual_demands=[]
    for d in doubles:
        F=d['F']
        if not d['neutral'] or F[0]<=1 or F[1]>=len(S):continue
        end=d['postA'];g,gid=previous(born[F],end);kap,kid=previous(removed[F],g)
        assert 0<end-kap<=clock
        pos=bisect.bisect_right([t for t,_,_ in changes[F]],kap%clock)-1
        present=changes[F][pos][1] if pos>=0 else F in initial_set
        acquired=present or any(v and kap<t+lap*clock<=end for t,v,_ in changes[F] for lap in (-1,0))
        if not acquired:
            actual_demands.append({'id':d['id'],'span':[S[F[0]-1],S[F[1]-1]],'F':list(F),'Gamma':gid,'Gamma_clock':g,'kappa':kid,'kappa_clock':kap,'postA':end})
    assert actual_demands==saved['demands']
    if lower:
        assert cut_neighbors==set(map(tuple,lower['neighbor_ids']))
        assert len(lower['demand_indices'])>lower['capacity']*len(cut_neighbors)
        assert lower['capacity']==K-1
    elif actual_demands:assert K==1
    else:assert K==0
    interval=saved['split_pivot_interval_test']
    if interval:
        assert S==keys and interval['exact_for_theta_1_split_resources']==root_only
        caps=Counter(x for points in unit_pivots.values() for x in points)
        assert sum(caps.values())==interval['total_pivot_copies']<=3*A
        available=[caps[x] for x in keys]+[0];parent=list(range(len(keys)+1))
        def find(i):
            while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
            return i
        for i in range(len(keys)-1,-1,-1):
            if not available[i]:parent[i]=find(i+1)
        passed=True
        for d in sorted(actual_demands,key=lambda z:(z['span'][1],z['span'][0])):
            a,b=d['span'];i=find(bisect.bisect_left(keys,a))
            if i==len(keys) or keys[i]>b:passed=False;break
            available[i]-=1
            if not available[i]:parent[i]=find(i+1)
        assert passed==interval['all_intervals_pass']
        if not passed:
            w=interval['worst'];a,b=w['span']
            demand=sum(a<=d['span'][0] and d['span'][1]<=b for d in actual_demands)
            capacity=sum(v for x,v in caps.items() if a<=x<=b)
            assert demand-capacity==w['deficiency']>0
    return {'case':saved['index'],'name':saved['name'],'A':A,'Q_B':Q,'U_int':len(actual_demands),'K':K,
            'period_real_rotations':R,'prefix_real_rotations':reachrot,'original_ops':len(s['operations']),
            'full_original_closure':True,'reaching_prefix_checked':True,'all_Pi_memberships':True,
            'literal_LCA_or_internal_predicate_for_every_assignment':True,'integer_optimum_verified':True}


def verify_shortcut():
    cert=json.loads((HERE/'REJECTED_PIVOT_SHORTCUT.json').read_text(encoding='utf-8'));s=canonical(cert['source_ref'])
    trees={a:tree(s['initial_'+a]) for a in ('A','B')};wanted=tuple(cert['unit']['id']);a,b=cert['demand']['span'];bits=[];extra_bits=[];costA=costQ=0;snapshots=[]
    def turn(t,parent,promoted):
        if t.k==parent:return V.right(t) if promoted<parent else V.left(t)
        return V.node(t.k,turn(t.l,parent,promoted),t.r) if parent<t.k else V.node(t.k,t.l,turn(t.r,parent,promoted))
    def path(t,x):
        out=[]
        while t:
            out.append(t)
            if t.k==x:return out
            t=t.l if x<t.k else t.r
        raise AssertionError()
    for op,(mode,target) in enumerate(s['operations'],1):
        for actor in ('A','B') if mode=='K' else ('A',):
            tr=path(trees[actor],target);depth=len(tr)-1
            if actor=='A':costA+=(depth+1)//2
            else:costQ+=depth//2
            step=0
            while len(tr)>1:
                step+=1
                if len(tr)==2:pivots=[target]
                else:
                    g,p,x=tr[-3:];pivots=[p.k,target] if (p.k<g.k)==(target<p.k) else [target,target]
                for bit,promoted in enumerate(pivots):
                    pr=path(trees[actor],promoted)[-2]
                    old=cover(trees[actor],a,b);oldlab=[old.lo,old.hi]
                    if (actor,op,step,0)==wanted and bit==0:snapshots.append(state(trees[actor]))
                    trees[actor]=turn(trees[actor],pr.k,promoted)
                    new=cover(trees[actor],a,b);newlab=[new.lo,new.hi]
                    if (actor,op,step,0)==wanted:
                        snapshots.append(state(trees[actor]))
                        bits.append({'bit':bit,'promoted':promoted,'demoted':pr.k,'old_LCA':old.k,'new_LCA':new.k,'old_cover':oldlab,'new_cover':newlab,
                                     'internal':a<=promoted<=b and a<=pr.k<=b})
                    if (actor,op,step,0)==('A',21,6,0):
                        extra_bits.append({'bit':bit,'promoted':promoted,'demoted':pr.k,'old_LCA':old.k,'new_LCA':new.k,
                                           'old_cover':oldlab,'new_cover':newlab,'internal':a<=promoted<=b and a<=pr.k<=b})
                tr=path(trees[actor],target)
    assert all(state(trees[z])==s['initial_'+z] for z in ('A','B'))
    assert (costA,costQ)==(cert['A'],cert['Q_B']) and len(bits)==2
    assert any(a<=v<=b for bit in bits for v in (bit['promoted'],bit['demoted']))
    assert all(not bit['internal'] and bit['old_cover']==bit['new_cover'] for bit in bits)
    assert len(extra_bits)==2 and any(bit['internal'] for bit in extra_bits)
    assert all(bit['old_cover']==bit['new_cover'] for bit in extra_bits)
    out={'passed':True,'source':s['name'],'demand':cert['demand']['id'],'frame':[a,b],'unit':list(wanted),'literal_original_bits':bits,
         'genuine_added_internal_donor':{'unit':['A',21,6,0],'bits':extra_bits,'theta_1_eligible':True,'cover_only_eligible':False},
         'scope':'Refutes the pivot-incidence shortcut only; theta_1 and Universal CD are not refuted.'}
    if not (HERE/'FINAL_MANIFEST.json').exists():
        (HERE/'SHORTCUT_INDEPENDENT_VERIFICATION.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
        (HERE/'SHORTCUT_SNAPSHOTS.json').write_text(json.dumps({'source':s['name'],'snapshots':snapshots,'frame':[a,b]},indent=2),encoding='utf-8')
    return out


def main():
    out=[]
    for path in sorted(HERE.glob('case_*.json')):
        result=validate(path);out.append(result)
        if len(out)%25==0:print(json.dumps({'independently_checked':len(out),'cpu':round(time.process_time()-START,3)}),flush=True)
    assert len(out)==273
    shortcut=verify_shortcut()
    result={'passed':True,'cases':out,'case_count':len(out),'period_real_rotations':sum(x['period_real_rotations'] for x in out),
            'prefix_real_rotations':sum(x['prefix_real_rotations'] for x in out),'original_ops':sum(x['original_ops'] for x in out),
            'shortcut_refutation':shortcut,'cpu_seconds':time.process_time()-START,
            'scope':'Independent immutable implementation within the same agent, not external/formal certification. Finite allocations and exact refutation do not prove universal conservation.'}
    if not (HERE/'FINAL_MANIFEST.json').exists():
        (HERE/'INDEPENDENT_VERIFICATION.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('cases','shortcut_refutation')}),flush=True)


if __name__=='__main__':main()
