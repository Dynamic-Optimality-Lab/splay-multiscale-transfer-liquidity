"""Closure child for symbolic BF contexts, with actual full-support necessity."""
import collections,json,sys,time
from pathlib import Path
import audit_grammar as g
c=g.c;B=Path(__file__).resolve().parent
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def freeze(v):return tuple(map(freeze,v)) if isinstance(v,list) else v
def main():
    states=[t for t in g.BF(1,11) if t[0] in c.MM];idx={t:i for i,t in enumerate(states)}
    adj=[[] for _ in states];rev=[[] for _ in states];edges=[]
    for i,t in enumerate(states):
        for x in c.M:
            if x==t[0]:continue
            n=c.bm(t,x)
            if n is None or n[0] not in idx:continue
            j=idx[n[0]];adj[i].append(j);rev[j].append(i);edges.append((i,j,x,n[1]))
    visited=set();order=[]
    for start in range(len(states)):
        if start in visited:continue
        visited.add(start);stack=[(start,0)]
        while stack:
            v,k=stack[-1]
            if k==len(adj[v]):order.append(v);stack.pop();continue
            u=adj[v][k];stack[-1]=(v,k+1)
            if u not in visited:visited.add(u);stack.append((u,0))
    comp={};components=[]
    for start in reversed(order):
        if start in comp:continue
        cid=len(components);nodes=[];stack=[start];comp[start]=cid
        while stack:
            v=stack.pop();nodes.append(v)
            for u in rev[v]:
                if u not in comp:comp[u]=cid;stack.append(u)
        components.append(nodes)
    support=[set() for _ in components]
    for i,j,x,q in edges:
        if comp[i]==comp[j]:support[comp[i]].add(x)
    admissible={i for i in range(len(states)) if support[comp[i]]==c.MM}
    report=[]
    q=json.loads((B/'grammar.json').read_text())
    for row in q['order_profiles']:
        if not row['A_compatible']:continue
        ex=row['example'];i=idx[freeze(ex['previous_BF'])]
        report.append({'rank_word':row['rank_word'],'example':ex['word'],'previous_Q':ex['previous_Q'],
            'example_component_size':len(components[comp[i]]),'example_component_support':sorted(support[comp[i]]),
            'example_admitted_by_full_support_closure':i in admissible})
    # Reclassify ALL tails, not just a selected representative of each profile.
    incoming=collections.defaultdict(list);fwd=collections.defaultdict(list)
    for i,j,x,q in edges:incoming[j].append((i,x,q));fwd[i].append((j,x,q))
    remaining=[];profiles=collections.Counter()
    def leaf_at(t,x):
        u=c.core(t,c.MM)
        def kids(v):
            if v is None:return None
            if v[0]==x:return c.labels(v)-{x}
            a=kids(v[1]);return a if a is not None else kids(v[2])
        return not kids(u)
    for i in admissible:
        pre=states[i]
        if c.leaves(pre)!=3:continue
        for j,a,q in fwd[i]:
            if j not in admissible or q!=2 or c.leaves(states[j])!=2:continue
            for k,b,q2 in fwd[j]:
                if k not in admissible or q2!=2 or c.leaves(states[k])!=2:continue
                for z,x,q3 in fwd[k]:
                    if z not in admissible or q3!=4 or x in (pre[0],a,b) or not leaf_at(pre,x):continue
                    for old,gg,q0 in incoming[i]:
                        if old not in admissible or q0 not in (1,2) or states[old][0]==x:continue
                        word=(states[old][0],gg,a,b,x);pat=g.normal(word);profiles[pat]+=1
                        if next(r for r in qdata['order_profiles'] if tuple(r['rank_word'])==pat)['A_compatible']:
                            remaining.append({'word':word,'previous_Q':q0,'previous_BF':states[old],
                                'pre_loss_BF':pre,'component':comp[i]})
    result={'status':'FULL_SUPPORT_CLOSURE_SEPARATES_ALL_LOCAL_FRAMES' if not remaining else 'SURVIVING_SOURCE_PROFILES',
        'symbolic_BF_contexts':len(states),'original_BF_edges':len(edges),'SCC_count':len(components),
        'full_six_support_components':[{'size':len(v),'support':sorted(support[i])} for i,v in enumerate(components) if support[i]==c.MM],
        'full_six_support_contexts':len(admissible),'compatible_profile_examples':report,
        'remaining_compatible_tails':remaining,'full_support_profiles':[{'word':p,'count':v} for p,v in sorted(profiles.items())],
        'source_engine_calls':c.account['source_engine_calls'],'new_finite_tests':0,
        'coverage_requires':'source exact grammar, gap substitution, and closed-walk SCC necessity proofs'}
    out('sourceclosure.json',result);print(json.dumps({k:v for k,v in result.items() if k not in ('remaining_compatible_tails','full_support_profiles')}),flush=True)
if __name__=='__main__':
    error=None
    try:qdata=json.loads((B/'grammar.json').read_text());main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_sourceclosure_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,**c.account})
