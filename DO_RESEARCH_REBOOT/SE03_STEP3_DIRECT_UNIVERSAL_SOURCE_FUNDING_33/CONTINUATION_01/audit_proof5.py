"""Lift the precise B-only failure to a genuine >=7-support closed B source,
if and only if actual cached native actions provide its closed bridge.
No inference to a full2H-Q violation.
"""
import json,sys,time,collections,itertools
from pathlib import Path
B=Path(__file__).resolve().parent;CAP=float(sys.argv[1]);START=time.process_time()
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    z=json.loads((B/'nine_label_native_action_cache.json').read_text());neg=json.loads((B/'nine_core_B_only_result.json').read_text());cyc=neg['cycle'];s=cyc[0][0];N=len(z['trees']);D=z['destination'];Q=z['Q'];word=[r[1] for r in cyc];base=set(word);answer=None;tries=[]
    for extras in itertools.combinations(sorted(set(range(1,10))-base),2):
        M=base|set(extras);fwd={s:None};queue=collections.deque([s]);reverse=[[] for _ in range(N)]
        for v in range(N):
            for x in M:
                t=D[v][x-1]
                if v!=t:reverse[t].append((v,x))
        while queue:
            v=queue.popleft()
            for x in sorted(M):
                t=D[v][x-1]
                if t not in fwd:fwd[t]=(v,x);queue.append(t)
        back={s:None};queue=collections.deque([s])
        while queue:
            t=queue.popleft()
            for v,x in reverse[t]:
                if v not in back:back[v]=(t,x);queue.append(v)
        component=set(fwd)&back.keys();alphabet={x for v in component for x in M if D[v][x-1] in component and x!=z['trees'][v][0]};tries.append({'M':sorted(M),'component':len(component),'genuine_alphabet':sorted(alphabet)})
        if not set(extras)<=alphabet:continue
        bridge=[]
        for x in extras:
            v=next(v for v in sorted(component) if D[v][x-1] in component and z['trees'][v][0]!=x);prefix=[];p=v
            while p!=s:pr,y=fwd[p];prefix.append(y);p=pr
            prefix.reverse();bridge+=prefix+[x];p=D[v][x-1]
            while p!=s:t,y=back[p];bridge.append(y);p=t
        p=s;bridge_cost=0
        for x in bridge:bridge_cost+=2-Q[p][x-1];p=D[p][x-1]
        assert p==s
        repeat=max(1,bridge_cost//2+1);full=word*repeat+bridge;p=s;qsum=asum=0;genuine=set();rows=[]
        for x in full:
            t=D[p][x-1];q=Q[p][x-1];a=z['H'][p][x-1];rows.append([p,x,t,a,q]);qsum+=q;asum+=a
            if x!=z['trees'][p][0]:genuine.add(x)
            p=t
        assert p==s and genuine==M and 2*len(full)-qsum<0 and 2*asum-qsum>=0
        # A==B throughout; common initial source makes reachability literal.
        answer={'status':'SOURCE_EXACT_SEVEN_KEEP_REFUTATION_OF_B_ONLY_PRICE','initial':z['trees'][s],'M':sorted(M),'B_negative_cycle':cyc,'B_cycle_repetitions':repeat,'closed_bridge':bridge,'word':[['K',x] for x in full],'cached_rows':rows,'period_length':len(full),'A':asum,'Q':qsum,'B_only_price':2*len(full)-qsum,'actual_price':2*asum-qsum,'paired_closed':True,'principal_U33':'OPEN','claim':'no state-defined B-only D satisfies2-Q+DeltaD on every actual support7/core9 source; original2H-Q safe'};break
    out('nine_core_B_only_seven_mark_bridge.json',{'answer':answer,'attempts':tries,'source_queries':0});print(json.dumps({'answer_status':answer['status'] if answer else 'NO_SOURCE_BRIDGE_FOUND','attempts':tries}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof5_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
