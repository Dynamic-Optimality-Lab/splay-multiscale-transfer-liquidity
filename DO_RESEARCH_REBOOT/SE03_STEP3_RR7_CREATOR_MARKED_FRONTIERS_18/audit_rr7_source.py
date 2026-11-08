"""Bounded ACTUAL-source falsification construction, not a universal graph.
An unqualified source packet is never promoted to the full RR7 counterclaim.
"""
import collections,hashlib,importlib.util,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
def module(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
p=module('original_source18',B.parent/'SE03_STEP2_COLD_NEG2_01/source_model.py')
L=module('leaf_channels18',B.parent/'SE03_STEP3_UNIFORM_DONOR_GROUPING_15/leaf_channels.py')
C=module('creator18',B.parent/'SE03_STEP3_SOURCE_FORCED_MULTICOMPONENT_ESCAPE_17/audit_lineage.py')
M=set(range(1,14,2));R=p.vine(13);calls=queries=0
def tr(t,x):
    global calls,queries
    calls+=1;queries+=1;assert queries<100000
    return p.trace(t,x)
def moves(t):
    global queries
    ans={}
    for x in sorted(M-{t[0]}):
        queries+=1;w=p.path(t,x)
        if len(w)%2 or any(w[j:j+2] not in ('LL','RR') for j in range(0,len(w),2)):continue
        z,pa,ev=tr(t,x)
        if all(e['kind']=='DOUBLE' and e['G'] in M and e['P'] not in M for e in ev):ans[x]=z
    return ans
def branch(t,x):
    par,ch=L.marked_tree(t,M);anc=[];v=par[x]
    while v is not None:anc.append(v);v=par[v]
    return len(anc),sum(len(ch[v])>=2 for v in anc),int(not ch[x])
def out(n,x):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(x,f,indent=2)
def freeze(t):return tuple(freeze(x) for x in t) if isinstance(t,list) else t
def replay(a,b,word,start=1):
    rows=[]
    for i,(mode,x) in enumerate(word,start):
        before=(a,b,b);a,pa,ea=tr(a,x);genuine=mode=='K' and b[0]!=x;pb='';eb=[]
        if mode=='K':b,pb,eb=tr(b,x)
        rows.append({'occurrence':i,'mode':mode,'target':x,'genuine_F':genuine,'A_path':pa,'A_events':ea,
            'BF_path':pb,'BF_events':eb,'BE_path':pb,'BE_events':eb,
            'a':len(ea),'qF':len(eb),'qE':len(eb),'before':before,'after':(a,b,b)})
    return rows,(a,b)
def main():
    started=time.process_time();forward={R:None};todo=collections.deque([R]);graph={};rev=collections.defaultdict(list)
    while todo and len(forward)<12000 and time.process_time()-started<1.6:
        t=todo.popleft();ed=moves(t);graph[t]=ed
        for x,z in ed.items():
            rev[z].append((t,x))
            if z not in forward:forward[z]=(t,x);todo.append(z)
    back={R:None};qq=collections.deque([R])
    while qq:
        t=qq.popleft()
        for z,x in rev[t]:
            if z not in back:back[z]=(t,x);qq.append(z)
    def from_R(t):
        w=[]
        while forward[t] is not None:t,x=forward[t];w.append(('K',x))
        return w[::-1]
    def to_R(t):
        w=[]
        while back[t] is not None:t,x=back[t];w.append(('K',x))
        return w
    candidates=[]
    for t in graph:
        if t[0]!=3 or t not in back or 13 not in graph[t]:continue
        z=graph[t][13]
        if branch(t,13)!=(2,2,1):continue
        if z not in graph or 5 not in graph[z]:continue
        zz=graph[z][5]
        if zz not in back or branch(z,5)!=(2,2,1):continue
        for g,s in graph[t].items():
            if len(p.path(t,g))==2 and s in back:
                inv=moves(s)
                if inv.get(3)==t:candidates.append((t,z,zz,g,s));break
    receipt={'status':'SOURCE_GRAPH_CONSTRUCTION_ONLY_NO_UNIVERSAL_PROMOTION',
        'states_discovered':len(forward),'states_expanded':len(graph),'known_return_states':len(back),
        'construction_exhausted_this_actual_component':not todo,'candidate_states':len(candidates),
        'source_engine_calls':calls,'source_queries':queries,'CPU_to_source_search':time.process_time()-started}
    if not candidates:
        out('rr7_construction_result.json',receipt);print(json.dumps(receipt),flush=True);return
    t,z,zz,g,s=candidates[0]
    old=json.loads((B.parent/'SE03_STEP3_UNIFORM_DONOR_GROUPING_15/leaf_source_certificates2.json').read_text())['reports'][0]
    gamma=[tuple(q) for q in old['base_word'][:32]]
    reset=[('D',x) for x in range(13,0,-1)]
    prefix=from_R(s)+reset
    prep=[('D',12),('D',5),('D',4),('D',3)]
    word=prep+[('K',3),('D',5),('D',13),('K',13),('K',5)]
    word+=to_R(zz)+reset+gamma+from_R(s)+reset
    prefix_rows,ab=replay(R,R,prefix);assert ab==(R,s)
    rows,end=replay(R,s,word);assert end==(R,s)
    assert {r['target'] for r in rows if r['genuine_F']}==M
    v=L.build(rows,M);cc=C.creator_records(rows,M)
    frontier=(9,2);assert frontier in v['R']
    targetrow=rows[8];assert targetrow['target']==5 and targetrow['A_path']=='LL' and targetrow['a']==1 and targetrow['qF']==2
    edge=(12,5);creator=max((c for c in cc if tuple(c['edge'])==edge and c['row_index']<8),key=lambda c:c['row_index'])
    unit=tuple(creator['unit']);hi={u:d for d,u in v['h'].items()};assert unit in hi
    def pack(m):return [{'demand':d,'unit':u} for d,u in sorted(m.items())]
    out('rr7_source_candidate.json',{'status':'REACHABLE_CLOSED_SOURCE_CREATOR_COLLISION_OWNER_PATH_QUALIFICATION_PENDING',
        'initial_common_tree':R,'reaching_prefix':prefix,'prefix_rows':prefix_rows,
        'initial_A':R,'initial_BF':s,'word':word,'rows':rows,'full_A_BF_closed':True,
        'full_support':sorted(M),'full_core_size':13,'un_erased_B_comparison_only':True,
        'frontier':frontier,'creator':creator,'colliding_comparison_demand':hi[unit],
        'leaf_comparison':pack(v['h']),'natural_h0':pack(v['h0']),
        'branch_frontiers':sorted(v['R']),'deep_packets':v['deep'],
        'new_source_engine_calls_so_far':calls,
        'qualification':'LL reflection of RR target; actual erased f6/deep-anchored first path must still be constructed'})
    receipt.update({'status':'REACHABLE_CLOSED_SOURCE_PACKET_COLLISION_FOUND_NOT_YET_FULL_RR7_REFUTATION',
        'prefix_length':len(prefix),'word_length':len(word),'creator_unit':unit,
        'colliding_demand':hi[unit],'source_engine_calls':calls,'source_queries':queries})
    out('rr7_construction_result.json',receipt);print(json.dumps(receipt),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_rr7_source_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,
        'source_engine_calls':calls,'source_queries':queries,'new_finite_tests':0,'old_semantic_rows_replayed':0})
