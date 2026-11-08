"""Systematic closure of ALL original LOW packet rules, not a local patch.
Conservative HIGH hyperedges cover every A6 endpoint shape at H>=3
singletons or Hsum>=4 pairs. Domain still excludes anonymous A ancestors.
"""
import collections,importlib.util,json,time
from pathlib import Path
B=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('original_packet_source13',B.parent/'SE03_STEP2_COLD_NEG2_01/source_model.py')
p=importlib.util.module_from_spec(s);s.loader.exec_module(p);calls=0
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def freeze(v):return tuple(map(freeze,v)) if isinstance(v,list) else v
def tree(t,hi=6):return 'F'+str(hi) if t is None else (t[0],tree(t[1],t[0]-1),tree(t[2],hi))
def compact(t):return None if isinstance(t,str) else (t[0],compact(t[1]),compact(t[2]))
def main():
    global calls
    source=json.loads((B/'cheap_A_comparison.json').read_text())['reports'][2];A=source['A_trees'];ai={freeze(t):i for i,t in enumerate(A)}
    one=collections.defaultdict(set);two=collections.defaultdict(set)
    for a,t in enumerate(A):
        T=tree(t)
        for x in range(1,7):
            if 1<=len(p.path(T,x))<=2:
                calls+=1;dest,_,ev=p.trace(T,x);assert len(ev)==1;one[a,x].add(ai[compact(dest)])
    for a,x,b in json.loads((B/'h2_transition_basis.json').read_text())['transition_basis']:two[a,x].add(b)
    states=[tuple(v) for v in source['states']];ix={v:i for i,v in enumerate(states)};by=collections.defaultdict(list)
    for i,(a,b) in enumerate(states):by[b].append((a,i))
    bf=json.loads((B/'bf11_comparison.json').read_text());marks=source['BF_marks'];rank={x:i+1 for i,x in enumerate(marks)}
    adj=collections.defaultdict(list)
    for s,t,x,q in bf['edges']:adj[s].append((t,x,q))
    low=[];high=set();types=collections.Counter()
    for s,t,x,q in bf['edges']:
        xx=rank[x]
        if q<=4:
            high.add((s,t,6-q))
            for a,i in by[s]:
                for H,trans in ((1,one),(2,two)):
                    for b in trans[a,xx]:low.append((i,ix[b,t],2*H-q));types['singleton_H'+str(H)]+=1
        else:
            for end,y,q1 in adj[t]:
                if q1!=1 or y not in (marks[0],marks[-1]):continue
                yy=rank[y];high.add((s,end,2))
                for a,i in by[s]:
                    for H1,H2,first,second in ((1,1,one,one),(1,2,one,two),(2,1,two,one)):
                        for mid in first[a,xx]:
                            for final in second[mid,yy]:
                                low.append((i,ix[final,end],2*(H1+H2)-6));types['pair_'+str(H1)+str(H2)]+=1
    d=[0]*len(states);iterations=0;updates=0;reason=None
    while True:
        changed=False;iterations+=1
        for a,b,w in low:
            new=d[a]-w
            if new>d[b]:d[b]=new;changed=True;updates+=1
        maximum={b:max(d[i] for a,i in ii) for b,ii in by.items()}
        for s,t,w in high:
            new=maximum[s]-w
            for a,i in by[t]:
                if new>d[i]:d[i]=new;changed=True;updates+=1
        if not changed:break
        if max(d)>16:
            reason='candidate needs range above16 on this conservative source comparison; no negative source cycle claimed';break
    if reason is None:
        assert all(w+d[b]-d[a]>=0 for a,b,w in low)
        assert all(w+min(d[i] for a,i in by[t])-max(d[i] for a,i in by[s])>=0 for s,t,w in high)
    out('core11_A6_packet_completion.json',{'status':'EXACT_ORIGINAL_PACKET_SOURCE_INEQUALITIES' if reason is None else 'CONSERVATIVE_TEMPLATE_UNRESOLVED',
        'domain':'only A marked core6 at EVERY natural macro boundary, full core11 original q5/q1 packets',
        'all_unbounded_A_core_sources':'OPEN_NOT_COVERED','states':states,'A_trees':A,'BF_trees':source['BF_trees'],
        'BF_marks':marks,'debt':d,'max_debt':max(d),'low_edges':low,'HIGH_hyperedges':sorted(high),
        'edge_types':dict(types),'iterations':iterations,'updates':updates,'unresolved_reason':reason,
        'source_engine_calls':calls,'not_claimed':'arbitrary full source physical funding or original CD6; HIGH hyperedges are sufficient overapproximations'})
    print(json.dumps({'status':'PACKET_CLOSURE_COMPLETE' if reason is None else 'PACKET_CLOSURE_OPEN','states':len(states),
        'low_edges':len(low),'high_hyperedges':len(high),'Dmax':max(d),'iterations':iterations,'types':dict(types)}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_packet_completion_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':calls})
