"""Actual global root-entry/ND/own graph, using newly saved traces and old source records."""
import collections,hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;C=F.parent;O=C/'CONTINUATION_04';B=C.parent/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def match(graph):
    owner={};chosen={}
    def go(d,seen):
        for u in sorted(graph[d]):
            if u in seen:continue
            seen.add(u)
            if u not in owner or go(owner[u],seen):owner[u]=d;chosen[d]=u;return True
        return False
    for d in sorted(graph):go(d,set())
    S=set(graph)-set(chosen);todo=list(S);N=set()
    while todo:
        d=todo.pop()
        for u in graph[d]:
            N.add(u);assert u in owner
            if owner[u] not in S:S.add(owner[u]);todo.append(owner[u])
    assert len(S)-len(N)==len(graph)-len(chosen)
    return chosen,{'demands':sorted(S),'units':sorted(N),'deficiency':len(S)-len(N)}
def main():
    p=F/'lifetime_controls.json';life=json.loads(p.read_text());ndp=O/'independent_core_sector_neutral.json';nd=json.loads(ndp.read_text());reports=[]
    for r in life['controls']:
        src=json.loads(Path(r['source_path']).read_text());rows=src['period_rows'];fine=r['fine_steps'];T=len(fine);U={tuple(u) for u in r['U']};D={tuple(d) for d in r['D']};D0={tuple(d) for d in r['D0']};graph={d:set() for d in D};n=len(rows)
        endpoints=[i for i,z in enumerate(rows) if z['genuine_F']];macro={}
        for k,end in enumerate(endpoints):
            ids=[];i=(endpoints[k-1]+1)%n
            while True:
                ids.append(i)
                if i==end:break
                i=(i+1)%n
            units={(rows[i]['t'],j,b) for i in ids for j in range(1,rows[i]['a']+1) for b in (0,1)}
            for j in range(1,rows[end]['qF']+1):d=(rows[end]['t'],j);graph[d]|=units;macro[d]=units
        old=next(c for c in nd['controls'] if c['source']==r['source'])
        for a in r['g_life']:graph[tuple(a['demand'])].add(tuple(a['unit']))
        for a in old['g_plus']:graph[tuple(a['demand'])].add(tuple(a['actual_bit']))
        arot={}
        for z in rows:
            for ev in z.get('A_events',[]):
                for rot in ev['rotations']:arot[(z['t'],ev['j'],rot['bit'])]=(rot['before'][0],rot['after'][0])
        port_records=[]
        for f in fine:
            if not f['neutral_double']:continue
            i=f['index'];d=tuple(f['demand']);I=frozenset(f['removed'][0]);delta=1
            while delta<=T:
                j=(i-delta)%T
                if sorted(I) in fine[j]['added']:break
                delta+=1
            assert delta<=T and sorted(I) not in fine[j]['removed']
            refs=[]
            if fine[j]['kind']=='A':
                a=fine[j];refs=[(a['t'],a['event_j'])];reason='LATEST_ADDITION_A_EVENT'
            else:
                assert fine[j]['access_key'] not in I and f['access_key'] in I
                for step in range(1,delta):
                    a=fine[(j+step)%T]
                    if a['kind']=='A':
                        unit=tuple(a['unit']);before,after=arot[unit]
                        if before not in I and after in I:refs.append((a['t'],a['event_j']))
                assert refs;reason='ACTUAL_A_ROOT_ENTRIES_AFTER_B_ADDITION'
            units={(t,k,b) for t,k in refs for b in (0,1)};assert units<=U;graph[d]|=units
            port_records.append({'demand':d,'B_rotation_index':i,'removed_cluster':sorted(I),'latest_addition':j,'cyclic_distance':delta,'reason':reason,'event_ids':sorted(set(refs)),'physical_units':sorted(units)})
        assert all(us<=U for us in graph.values())
        full,cut=match(graph);fixed={tuple(a['unit']) for a in r['g_life']};sub={d:graph[d]-fixed for d in D0};fixedchosen,fixedcut=match(sub)
        reports.append({'source':r['source'],'Q':len(D),'D0':len(D0),'raw_full_matching_size':len(full),'full_cut':cut,'fixed_lifetime_neutral_matching_size':len(fixedchosen),'fixed_lifetime_cut':fixedcut,
          'matching':[{'demand':d,'unit':u} for d,u in sorted(full.items())],'graph':[{'demand':d,'units':sorted(us)} for d,us in sorted(graph.items())],
          'ports':port_records,'original_owners_modified':False,'source_is_original_accepted_closed_control':True})
    out={'status':'EXACT_ROOT_ENTRY_JOINT_GRAPH_ANALYSIS','controls':reports,'source_queries':0,'source_engine_calls':0,'universal_source_expansion_proved':False,
      'Objective_I':'OPEN','Objective_II':'DEFERRED','input_sha256':{str(s):sha(s) for s in (p,ndp,F/'ROOT_ENTRY_LEMMA.md',F/'derive_root_entry_graph.py')}}
    with (F/'root_entry_graph_controls.json').open('x',encoding='utf8') as f:json.dump(out,f,indent=2)
    print(json.dumps({'status':out['status'],'controls':[{k:r[k] for k in ('source','Q','D0','raw_full_matching_size','full_cut','fixed_lifetime_neutral_matching_size','fixed_lifetime_cut')} for r in reports]}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_proof297_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
