"""Independent complete original H-source/Pi/physical-bank verification.

No current source producer, bank rule, optimizer or symbolic transducer import.
Original splay is the pinned immutable full-subtree implementation. Physical
parent/child updates are checked locally against each immutable emitted frame.
Carrier closure is constructed with a memoized ancestor union, not inferred
from the witness's demand declarations.
"""
import sys
import bisect
import json
import gzip
import time
import importlib.util
from collections import Counter,defaultdict
from pathlib import Path
sys.dont_write_bytecode=True
sys.setrecursionlimit(50000)
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
spec=importlib.util.spec_from_file_location('physical_bank_pinned_immutable',ROOT/'DO_RESEARCH_REBOOT/COVER_FLOW_AUDIT_20261121_V001/verify.py');V=importlib.util.module_from_spec(spec);sys.modules[spec.name]=V;spec.loader.exec_module(V)


def read(path):
    with (gzip.open(path,'rt',encoding='utf-8') if path.suffix=='.gz' else path.open(encoding='utf-8')) as f:return json.load(f)


def raw(t):
    out={};root=t.k;stack=[t]
    while stack:
        v=stack.pop();out[str(v.k)]=[v.l.k if v.l else None,v.r.k if v.r else None];stack.extend(h for h in (v.l,v.r) if h)
    return {'root':root,'children':out}


def independent_update(stock,e,H):
    order=e['priority'];before=[stock[i] for i in order];mass=sum(before)
    if e['a'] or e['k']:
        after=[H for _ in order];issued=len(order)*H-mass;paid=0
        assert issued<=8*H*e['a']+H*e['k']
    else:
        paid=min(e['q'],mass);remaining=mass-paid
        after=[min(H,max(0,remaining-j*H)) for j in range(len(order))];issued=0
    assert all(0<=v<=H for v in after) and sum(after)-mass==issued-paid
    for i,v in zip(order,after):stock[i]=v
    return {'before':before,'after':after,'issued':issued,'paid':paid,'unpaid':e['q']-paid}


def check_policy(z,ev,saved):
    H=saved['H'];m=len(z['blocks']);full=[H]*m;passes=[]
    for lap in range(m*H+1):
        new=full.copy();paid=0
        for e in ev:paid+=independent_update(new,e,H)['paid']
        assert all(v<=w for v,w in zip(new,full));passes.append({'pass':lap,'mass_before':sum(full),'mass_after':sum(new),'unpaid':sum(e['q'] for e in ev)-paid})
        if new==full:break
        assert sum(new)<sum(full);full=new
    else:raise AssertionError('nontermination of finite monotone descent')
    assert full==saved['initial_greatest_fixed_point'] and passes==saved['period_passes']
    stock=full.copy();issued=paid=0;fail=[];Aissue=Kissue=0;seenA=set();seenB=set();rows=saved['rows'];assert len(rows)==len(ev)
    for j,(e,r) in enumerate(zip(ev,rows)):
        actual=independent_update(stock,e,H)
        assert r=={'event':j,'id':e['id'],'priority':e['priority']}|actual
        issued+=actual['issued'];paid+=actual['paid']
        if e['a']:assert tuple(e['id']) not in seenA;seenA.add(tuple(e['id']));Aissue+=actual['issued']
        if e['k']:Kissue+=actual['issued']
        if e['q']:assert tuple(e['id']) not in seenB;seenB.add(tuple(e['id']))
        if actual['unpaid']:fail.append({'event':j,'id':e['id'],'target':e['target'],'scope':e['scope'],'priority':e['priority'],'before':actual['before'],'q':e['q'],'unpaid':actual['unpaid']})
    assert stock==full and issued==paid==saved['paid']==saved['issued'] and fail==saved['failures']
    assert len(seenA)==z['A'] and Aissue<=8*H*z['A'] and Kissue<=H*z['K_B']
    return {'paid':paid,'requested':sum(e['q'] for e in ev),'unpaid':len(fail),'A_issued':Aissue,'KEEP_issued':Kissue,'max_A_unit_issuance':8*H,'max_KEEP_issuance':H,'greatest_cyclic_balance_checked':True,'failed_original_ids':[f['id'] for f in fail]}


def verify_source(key,trace_path,policy_path,events_path,bulk):
    z=read(trace_path);s=z['source'];gold=read(events_path);saved=read(policy_path);assert gold['source']==s
    N=len(s['initial_A']['children']);p,q=s['p'],s['q'];assert N==2**(p+1)*(q+1)+1 and not s['prefix']
    vine={'root':1,'children':{str(k):[None,k+1 if k<N else None] for k in range(1,N+1)}};assert s['initial_A']==s['initial_B']==s['diagonal']==vine
    marked={N+1-2**j for j in range(p+1)};word=[['D',k] for k in range(2,N+1)]+[['K' if k in marked else 'D',k] for k in range(N,0,-1)]+[['K',k] for k in range(1,N+1)]+[['K',k] for k in range(N-1,0,-1)];assert s['operations']==word and len(word)==4*N-2
    keep=[];previous=1
    for mode,x in word:
        if mode=='K':
            if x!=previous:keep.append(x)
            previous=x
    initial_parent={k:k-1 if k>1 else None for k in range(1,N+1)};support=set()
    for x in keep:
        while x is not None and x not in support:support.add(x);x=initial_parent[x]
    S=sorted(support);assert S==gold['S']==list(range(1,N+1))
    def label(v):
        if v is None:return None
        lo=bisect.bisect_left(S,v.lo);hi=bisect.bisect_right(S,v.hi);return (lo+1,hi) if hi>lo else None
    t=None
    for k in range(N,0,-1):t=V.node(k,None,t)
    initial=t;trees={'A':t,'B':t};maps={a:{k:[None,k+1 if k<N else None] for k in range(1,N+1)} for a in trees};parents={a:initial_parent.copy() for a in trees};roots={'A':1,'B':1}
    initcounts=Counter({(k,N):1 for k in range(1,N+1)});counts={a:initcounts.copy() for a in trees};initial_set=set(initcounts)
    born=defaultdict(list);died=defaultdict(list);changes=defaultdict(list);doubles=[];clock=A=Q=R=KB=0
    parts=z['blocks'];assert parts==[list(range(k,min(k+5,N+1))) for k in range(1,N+1,5)];owner={x:i for i,block in enumerate(parts) for x in block}
    ev=[];actual_steps=[];saved_steps={tuple(st['id']):st for st in z['steps']};byopA=defaultdict(list);critical={N-1+2**j:j for j in range(p+1)};selected_RR=[]
    for op,((mode,target),row) in enumerate(zip(word,z['operations']),1):
        clock+=1;genuine=int(mode=='K' and trees['B'].k!=target);KB+=genuine
        if genuine:ev.append({'id':['K',op],'a':0,'q':0,'k':1,'target':target,'scope':[owner[target]],'priority':[owner[target]]})
        depths={};operation_steps=[]
        for actor in ('A','B') if mode=='K' else ('A',):
            if actor=='B':clock+=1;postA=clock
            step_records={}
            def emit(step,bit,typ,promoted,pivot,demoted):
                nonlocal clock,R
                clock+=1;R+=1;identifier=[actor,op,step,bit];y=promoted.k;parent=pivot.k;ch=maps[actor];pa=parents[actor]
                assert pa[y]==parent and ch[parent]==[pivot.l.k if pivot.l else None,pivot.r.k if pivot.r else None] and ch[y]==[promoted.l.k if promoted.l else None,promoted.r.k if promoted.r else None]
                grand=pa[parent];side=int(y>parent);middle=ch[y][1-side];foot=sorted({owner[v] for v in (y,parent,grand,middle) if v is not None})
                old=label(promoted);new=label(demoted);candidate={v for v in (old,new) if v is not None};before={v:counts[actor][v] for v in candidate}
                if old:counts[actor][old]-=1
                if new:counts[actor][new]+=1
                lost={v for v in candidate if before[v]>0 and not counts[actor][v]};gain={v for v in candidate if not before[v] and counts[actor][v]>0}
                if actor=='A':
                    for v in lost:changes[v].append((clock,False,identifier))
                    for v in gain:changes[v].append((clock,True,identifier))
                else:
                    assert len(lost)==len(gain)==1
                    for v in lost:died[v].append((clock,identifier))
                    for v in gain:born[v].append((clock,identifier))
                ch[parent][side]=middle
                if middle is not None:pa[middle]=parent
                ch[y][1-side]=parent;pa[parent]=y;pa[y]=grand
                if grand is None:roots[actor]=y
                else:ch[grand][int(ch[grand][1]==parent)]=y
                sid=(actor,op,step)
                if sid not in step_records:step_records[sid]={'id':list(sid),'actor':actor,'target':target,'type':typ,'a':int(actor=='A'),'q':int(actor=='B' and typ!='ZIG'),'k':0,'scope':set(),'bits':[]}
                rec=step_records[sid];rec['scope'].update(foot);rec['bits'].append({'id':identifier,'promoted':y,'demoted':parent,'grandparent':grand,'middle':middle,'footprint':foot})
                return 0 if actor=='A' else -int(any(counts['A'][v] for v in gain))
            def double(step,typ,span,left,right):
                if actor=='B':
                    lo=bisect.bisect_left(S,span[0]);hi=bisect.bisect_right(S,span[1]);doubles.append({'id':[op,step],'F':(lo+1,hi),'neutral':left==right==0,'postA':postA})
            trees[actor],depth=V.rebuild(trees[actor],target,emit,double);depths[actor]=depth;assert roots[actor]==trees[actor].k==target
            for st in step_records.values():
                st['scope']=sorted(st['scope']);assert st==saved_steps[tuple(st['id'])];operation_steps.append(st);actual_steps.append(st)
                block=owner[target];priority=[block]+[i for i in st['scope'] if i!=block];cost=st['q']
                if bulk:cost=int(actor=='B' and critical.get(op,-1)>=4 and st['type']=='RR')
                if actor=='B' and critical.get(op,-1)>=4 and st['type']=='RR':selected_RR.append(st['id'])
                ev.append({k:st[k] for k in ('id','a','k','target','scope')}|{'q':cost,'priority':priority})
                if actor=='A':byopA[op].append(st['id']+[0])
            if actor=='A':A+=(depth+1)//2
            else:Q+=depth//2
        if mode!='K':clock+=1
        clock+=1;assert row['id']==op and row['mode']==mode and row['target']==target and row['a']==(depths['A']+1)//2 and row['q']==depths.get('B',0)//2 and row['k']==genuine
    assert actual_steps==z['steps'] and (A,Q,KB,R)==(z['A'],z['Q_B'],z['K_B'],z['real_rotations'])
    assert (A,Q,R,clock)==(gold['A'],gold['Q_B'],gold['real_rotations'],gold['period_clock'])
    assert all(raw(trees[a])==vine and {'root':roots[a],'children':{str(k):v for k,v in maps[a].items()}}==vine and +counts[a]==initcounts for a in trees)
    times={v:[t for t,_ in seq] for v,seq in born.items()};deathtimes={v:[t for t,_ in seq] for v,seq in died.items()};changetimes={v:[t for t,_,_ in seq] for v,seq in changes.items()}
    def previous_event(table,keys,v,end):
        seq=table[v];lap,local=divmod(end,clock);i=bisect.bisect_left(keys[v],local)-1
        if i<0:lap-=1;i=len(seq)-1
        t,eid=seq[i];return t+lap*clock,eid
    U=[]
    for d in doubles:
        f=d['F'];end=d['postA']
        if not d['neutral'] or f[0]<=1 or f[1]>=len(S):continue
        gamma,gid=previous_event(born,times,f,end);kap,kid=previous_event(died,deathtimes,f,gamma);assert 0<end-kap<=clock
        pos=bisect.bisect_right(changetimes.get(f,[]),kap%clock)-1;present=changes[f][pos][1] if pos>=0 else f in initial_set
        exposed=present or any(flag and kap<t+lap*clock<=end for t,flag,_ in changes[f] for lap in (-1,0))
        if not exposed:U.append({'id':d['id'],'span':[S[f[0]-1],S[f[1]-1]],'F':list(f),'Gamma':gid,'Gamma_clock':gamma,'kappa':kid,'kappa_clock':kap,'postA':end})
    assert U==gold['original_U'];uids={tuple(u['id']) for u in U};assert {tuple(v[1:]) for v in selected_RR}<=uids
    policy=check_policy(z,ev,saved);failed={tuple(v[1:]) for v in policy['failed_original_ids']};assert failed and failed<=uids
    # Actual original KEEP vouchers have disjoint incoming cyclic A gaps.
    genuine_ops=[r['id'] for r in z['operations'] if r['k']];used=set()
    for j,op in enumerate(genuine_ops):
        prev=genuine_ops[j-1];gap=list(range(prev+1,op+1)) if prev<op else list(range(prev+1,len(word)+1))+list(range(1,op+1))
        chosen=next((ids[0] for k in gap if (ids:=byopA[k])),None);assert chosen and tuple(chosen) not in used;used.add(tuple(chosen))
    assert len(used)==KB<=A
    return {'key':key,'name':s['name'],'physical_keys':N,'operations':len(word),'A':A,'Q_B':Q,'K_B':KB,'real_rotations':R,'original_U':len(U),'selected_critical_RR_are_original_U':len(selected_RR),'full_carrier_and_cyclic_Pi_checked':True,'full_pair_closure_and_empty_prefix_checked':True,'policy':policy,'all_unpaid_are_genuine_original_U':True,'no_virtual_or_prefix_credit':True}


def main():
    start=time.perf_counter();rows=[]
    for key,t,p,o,bulk in [('H8','scaling_001/trace_08.json.gz','counter_001/H8_H9q5_policy.json.gz','counter_001/H8_original_events.json.gz',False),('W_H1','counter_001/W_H1_complete_trace.json.gz','counter_001/W_H1_relaxed_policy.json.gz','counter_001/W_H1_original_events.json.gz',True)]:
        r=verify_source(key,HERE/t,HERE/p,HERE/o,bulk);rows.append(r);print({k:v for k,v in r.items() if k!='policy'},flush=True)
    out={'passed':True,'witnesses':rows,'seconds':time.perf_counter()-start,'scope':'Two complete original-source counterexamples, all real steps and bank events, original full cyclic Pi, and greatest fixed-point checks. The all-H source proof is separately symbolic.','independence':'No current bank/source/synthesis imports; pinned immutable rotations plus independent physical-parent and clamp bank checks. Same agent, not external peer review.','root_status':'OPEN'}
    if not (HERE/'FINAL_MANIFEST.json').exists():(HERE/'INDEPENDENT_VERIFICATION.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({'passed':True,'witnesses':len(rows),'seconds':out['seconds'],'original_operations':sum(r['operations'] for r in rows),'real_rotations':sum(r['real_rotations'] for r in rows)}))


if __name__=='__main__':main()
