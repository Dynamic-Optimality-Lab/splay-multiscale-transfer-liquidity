"""Exact ownership graph for source-derived local/cluster/level edges."""
import collections,hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;B=F.parents[1]/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time();PHASE=sys.argv[3]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tup(u):return (u[0],tup(u[1]),tup(u[2])) if isinstance(u,list) else u
def labels(t,S):
    out=set()
    def go(u):
        if u is None:return frozenset()
        a=go(u[1])|go(u[2])|({u[0]} if u[0] in S else set())
        if a:out.add(frozenset(a))
        return frozenset(a)
    go(t);return out
def main():
    annpath=F/'independent_core_sector_neutral.json';ann=json.loads(annpath.read_text())
    reports=[];pins=[annpath,F/'CORE_SECTOR_LIABILITY_THEOREM.md',F/'NEUTRAL_DOUBLE_SOURCE_DECOMPOSITION.md']
    for name,path in [('CCR',F/'cluster_collateral_closed_source.json'),('AF',B/'SOURCE_JOINT_REPAIR_03/actual_monotone_return_source.json')]:
        assert ann['input_sha256'][str(path)]==sha(path);pins.append(path)
        src=json.loads(path.read_text());rows=src['period_rows'];control=next(x for x in ann['controls'] if x['source']==name);S=set(control['S'])
        D={(r['t'],k) for r in rows for k in range(1,r['qF']+1)}
        U={(r['t'],j,b) for r in rows for j in range(1,r['a']+1) for b in (0,1)}
        graph={d:set() for d in D};reasons=collections.defaultdict(list);h0={}
        ends=[i for i,r in enumerate(rows) if r['genuine_F']]
        for j,end in enumerate(ends):
            start=(ends[j-1]+1)%len(rows)
            ids=list(range(start,end+1)) if start<=end else list(range(start,len(rows)))+list(range(end+1))
            seg=[rows[i] for i in ids];units=[(r['t'],k,b) for r in seg for k in range(1,r['a']+1) for b in (0,1)]
            ds=[(seg[-1]['t'],k) for k in range(1,seg[-1]['qF']+1)];h0.update(dict(zip(ds,units)))
            initial=labels(tup(seg[0]['A_before']),S);node=tup(seg[0]['BF_before']);x=seg[-1]['key'];pathnodes=[]
            while True:
                pathnodes.append(node)
                if node[0]==x:break
                node=node[1] if x<node[0] else node[2]
            first={}
            for r in seg:
                assert 'A_events' in r
                for ev in r['A_events']:
                    for rot in ev['rotations']:
                        lost=labels(tup(rot['before']),S)-labels(tup(rot['after']),S);assert len(lost)<=1
                        for c in lost:first.setdefault(c,(r['t'],ev['j'],rot['bit']))
            depth=len(pathnodes)-1
            for k,d in enumerate(ds,1):
                for u in units:
                    graph[d].add(u);reasons[d,u].append('SAME_ACTUAL_MACRO')
                for index in (depth-2*k+2,depth-2*k+1):
                    c=frozenset().union(*labels(pathnodes[index],S))
                    assert c and x in c
                    if c in initial:
                        assert c in first;u=first[c];graph[d].add(u);reasons[d,u].append('PRESENT_SECTOR_FIRST_LOSS')
        for a in control['g_plus']:
            d,u=tuple(a['demand']),tuple(a['actual_bit']);assert d in D and u in U
            graph[d].add(u);reasons[d,u].append('CYCLIC_LEVEL_PAYMENT')
        frozen=src.get('h0',src.get('h0_full_own',src.get('funding',{}).get('h0')))
        assert h0=={tuple(a['demand']):tuple(a['unit']) for a in frozen}
        # Determine exact source-neighborhood feasibility. h0 itself is never edited.
        owner={};match={}
        def augment(d,seen):
            for u in sorted(graph[d]):
                if u in seen:continue
                seen.add(u)
                if u not in owner or augment(owner[u],seen):
                    owner[u]=d;match[d]=u;return True
            return False
        for d in sorted(D):augment(d,set())
        unmatched=sorted(D-set(match));cuts=[]
        if unmatched:
            # All alternating descendants of all unmatched starts form an exact Hall cut.
            T=set(unmatched);N=set();todo=list(unmatched)
            while todo:
                d=todo.pop()
                for u in graph[d]:
                    N.add(u)
                    if u in owner and owner[u] not in T:T.add(owner[u]);todo.append(owner[u])
            assert all(u in owner for u in N) and len(N)<len(T) and set.union(*(graph[d] for d in T))==N
            cuts=[{'demands':sorted(T),'actual_bit_neighborhood':sorted(N),'deficiency':len(T)-len(N)}]
            full=None
        else:
            # Convert the full independently chosen comparison to one extending literal h0.
            inv0={u:d for d,u in h0.items()};full=dict(h0)
            for start in sorted(D-set(h0)):
                current=start;seen=set()
                while True:
                    assert current not in seen;seen.add(current);u=match[current]
                    if u not in inv0:break
                    current=inv0[u]
                assert u not in full.values();full[start]=u
            assert set(full)==D and len(set(full.values()))==len(full)
            assert all(full[d]==u for d,u in h0.items())
        reports.append({'source':name,'source_sha256':sha(path),'A':sum(r['a'] for r in rows),'Q':len(D),
          'relation_edges':[{'demand':d,'unit':u,'source_reasons':reasons[d,u]} for d in sorted(D) for u in sorted(graph[d])],
          'maximum_matching':[{'demand':d,'unit':u} for d,u in sorted(match.items())],
          'unmatched':unmatched,'exact_candidate_Hall_cuts':cuts,
          'h0_preserving_comparison':None if full is None else [{'demand':d,'unit':u} for d,u in sorted(full.items())],
          'h0_count':len(h0),'h0_changed':False,'Bank25_or_fE_license':'NOT_ESTABLISHED_BY_GRAPH'})
        assert time.process_time()-START<CAP-2
    result={'status':'EXACT_SOURCE_RELATION_ANALYSIS','source_queries':0,'source_engine_calls':0,
      'relation':'ALL_SAME_MACRO_BITS_UNION_BOTH_PRESENT_SECTOR_FIRST_LOSS_UNION_ND_LEVEL_PAYMENT',
      'controls':reports,'JR35':'OPEN','reservation':'DEFERRED',
      'counterexample_scope':'cuts, if any, refute ONLY this explicitly specified eligibility relation',
      'input_sha256':{str(p):sha(p) for p in pins}}
    with (F/'joint_source_relation.json').open('x',encoding='utf8') as f:json.dump(result,f,indent=2)
    print(json.dumps({'status':result['status'],'controls':[{'source':r['source'],'Q':r['Q'],'matched':len(r['maximum_matching']),'unmatched':r['unmatched'],'cuts':r['exact_candidate_Hall_cuts']} for r in reports],'JR35':'OPEN'}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/f'audit_{PHASE}_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
