"""Assess the universal terminal rearrangement against the frozen joint candidate graph."""
import hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;B=F.parent.parent/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def match(g):
    own={};chosen={}
    def visit(d,seen):
        for u in sorted(g[d]):
            if u in seen:continue
            seen.add(u)
            if u not in own or visit(own[u],seen):own[u]=d;chosen[d]=u;return True
        return False
    for d in sorted(g):visit(d,set())
    S=set(g)-set(chosen);todo=list(S);N=set()
    while todo:
        for u in g[todo.pop()]:
            N.add(u);assert u in own
            if own[u] not in S:S.add(own[u]);todo.append(own[u])
    return chosen,{'demands':sorted(S),'units':sorted(N),'deficiency':len(S)-len(N)}
def main():
    ep=F/'root_entry_graph_controls.json';tp=F/'terminal_neutral_controls.json';entry=json.loads(ep.read_text());term=json.loads(tp.read_text());reports=[]
    for e in entry['controls']:
        t=next(r for r in term['controls'] if r['source']==e['source']);paid={tuple(x['unit']) for x in t['g_T']};internal={tuple(d) for d in t['D_internal_neutral']};graph={tuple(x['demand']):{tuple(u) for u in x['units']} for x in e['graph']}
        graph={d:graph[d]-paid for d in internal};out,cut=match(graph)
        reports.append({'source':e['source'],'internal_demands':len(internal),'fixed_gT_entry_matching_size':len(out),'cut':cut,'matching':[{'demand':d,'unit':u} for d,u in sorted(out.items())],
          'fixed_partial_source_matching':'g_T, not any frozen owner input','failure_is_only_this_restricted_complement_rule':True})
    data={'status':'EXACT_TERMINAL_COMPLEMENT_GRAPH_CONTROL','controls':reports,'source_queries':0,'source_engine_calls':0,'Objective_I':'OPEN',
      'input_sha256':{str(p):sha(p) for p in (ep,tp,F/'COMPLETE_MATCHING_NORMALIZATION.md',F/'analyze_terminal_complement_graph.py')}}
    with (F/'terminal_complement_graph_controls.json').open('x',encoding='utf8') as f:json.dump(data,f,indent=2)
    print(json.dumps({'status':data['status'],'controls':[{k:r[k] for k in ('source','internal_demands','fixed_gT_entry_matching_size','cut')} for r in reports]}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_proof300_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
