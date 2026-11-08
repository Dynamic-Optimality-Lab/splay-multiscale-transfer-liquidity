"""Independent kernel regeneration of every A6 packet certificate row."""
import collections,importlib.util,json,time,types
from pathlib import Path
B=Path(__file__).resolve().parent
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
V=load('independent_A6_adapter13',B/'audit_A6_independent.py');calls=0;m=None
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    global calls,m
    m=load('H2_basis_immutable13',B/'audit_h2_basis.py')
    m.p=types.SimpleNamespace(trace=V.trace,path=V.trace_path,core=V.core,labels=V.labels)
    m.out=lambda n,v:out('packet_independent_'+n,v);m.main()
    independent=json.loads((B/'packet_independent_h2_transition_basis.json').read_text())
    primary=json.loads((B/'h2_transition_basis.json').read_text())
    assert independent['transition_basis']==primary['transition_basis']
    c=json.loads((B/'core11_A6_packet_completion.json').read_text());assert c['status']=='EXACT_ORIGINAL_PACKET_SOURCE_INEQUALITIES'
    A=c['A_trees'];aid={V.freeze(t):i for i,t in enumerate(A)};one=collections.defaultdict(set);two=collections.defaultdict(set)
    for a,t in enumerate(A):
        T=V.expand(t)
        for x in range(1,7):
            if 1<=len(V.trace_path(T,x))<=2:
                calls+=1;dest,_,ev=V.trace(T,x);assert len(ev)==1;one[a,x].add(aid[V.freeze(V.compact(dest))])
    for a,x,b in independent['transition_basis']:two[a,x].add(b)
    bf=json.loads((B/'bf11_comparison.json').read_text());states=[tuple(v) for v in c['states']];ix={v:i for i,v in enumerate(states)}
    by=collections.defaultdict(list)
    for i,(a,b) in enumerate(states):by[b].append((a,i))
    marks=c['BF_marks'];rank={x:i+1 for i,x in enumerate(marks)};adj=collections.defaultdict(list)
    for s,t,x,q in bf['edges']:
        calls+=1;dest,_,ev=V.trace(V.freeze(bf['trees'][s]),x)
        assert dest==V.freeze(bf['trees'][t]) and sum(e[0]!='ZIG' for e in ev)==q
        adj[s].append((t,x,q))
    expected=collections.Counter();high=set();pairsectors=0
    for s,t,x,q in bf['edges']:
        xx=rank[x]
        if q<=4:
            high.add((s,t,6-q))
            for a,i in by[s]:
                for H,trans in ((1,one),(2,two)):
                    for b in trans[a,xx]:expected[i,ix[b,t],2*H-q]+=1
        else:
            for end,y,q1 in adj[t]:
                if q1!=1 or y not in (marks[0],marks[-1]):continue
                pairsectors+=1;yy=rank[y];high.add((s,end,2))
                for a,i in by[s]:
                    for H1,H2,first,second in ((1,1,one,one),(1,2,one,two),(2,1,two,one)):
                        for mid in first[a,xx]:
                            for final in second[mid,yy]:expected[i,ix[final,end],2*(H1+H2)-6]+=1
    assert expected==collections.Counter(map(tuple,c['low_edges'])) and high==set(map(tuple,c['HIGH_hyperedges']))
    D=c['debt'];assert min(D)==0 and max(D)==3
    assert all(w+D[b]-D[a]>=0 for a,b,w in expected)
    assert all(w+min(D[i] for a,i in by[t])-max(D[i] for a,i in by[s])>=0 for s,t,w in high)
    out('core11_A6_packet_audit.json',{'status':'INDEPENDENT_EXACT_RESTRICTED_PACKET_COMPARISON_VERIFIED',
        'LOW_rows_with_multiplicity':sum(expected.values()),'HIGH_hyperedges':len(high),'actual_q5_q1_sectors':pairsectors,
        'H2_basis_exactly_identical_across_kernels':True,'D_range':[0,3],
        'source_lifting_scope':'A marked core6 at EACH natural boundary only, arbitrary interior helpers/private gaps',
        'full_core11':'OPEN; no arbitrary-A boundary erasure/augmentation theorem proved',
        'proof_class':'finite exact symbolic comparison with restricted free-gap lifting; not full multicore funding',
        'source_engine_calls':calls+m.calls})
    print(json.dumps({'status':'PASS_CORRECT_ORIGINAL_PACKET_AUDIT','LOW':sum(expected.values()),'HIGH':len(high),'pairs':pairsectors,'calls':calls+m.calls}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_packet_verify_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':calls+(m.calls if m else 0)})
