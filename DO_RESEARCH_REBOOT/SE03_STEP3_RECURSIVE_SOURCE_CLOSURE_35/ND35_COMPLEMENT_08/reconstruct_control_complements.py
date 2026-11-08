"""Construct actual complement maps by the proved complete-matching normalization.

This uses explicit complete source-control matchings, not assumed universal
matchings. It is not a new source-domain CD coverage theorem.
"""
import hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;B=F.parent.parent/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ep=F/'root_entry_graph_controls.json';tp=F/'terminal_neutral_controls.json';E=json.loads(ep.read_text());T=json.loads(tp.read_text());reports=[]
    for e in E['controls']:
        t=next(x for x in T['controls'] if x['source']==e['source']);h={tuple(x['demand']):tuple(x['unit']) for x in e['matching']};g={tuple(x['demand']):tuple(x['unit']) for x in t['g_T']};inverse={u:d for d,u in g.items()};graph={tuple(x['demand']):{tuple(u) for u in x['units']} for x in e['graph']}
        assert set(h)==set(graph) and len(set(h.values()))==len(h)
        full=dict(g);traces=[]
        for root in sorted(set(h)-set(g)):
            current=root;seen=set();steps=[]
            while True:
                assert current not in seen;seen.add(current);u=h[current];owner=inverse.get(u);steps.append({'comparison_demand':current,'comparison_bit':u,'provisional_gT_owner':owner})
                if owner is None:break
                current=owner
            full[root]=u;traces.append({'internal_neutral_root':root,'steps':steps,'terminal_bit':u,'terminal_outside_root_entry_graph':u not in graph[root]})
        assert set(full)==set(h) and len(set(full.values()))==len(full) and all(full[d]==u for d,u in g.items())
        reports.append({'source':e['source'],'full_matching':[{'demand':d,'unit':u} for d,u in sorted(full.items())],
          'constructed_complement':[{'demand':d,'unit':full[d]} for d in sorted(set(h)-set(g))],'paths':traces,'gT_values_preserved':len(g),
          'outside_single_step_entry_neighborhoods':sum(x['terminal_outside_root_entry_graph'] for x in traces),'original_owner_maps_modified':False})
    result={'status':'COMPLETE_ACTUAL_CONTROL_COMPLEMENTS_CONSTRUCTED','controls':reports,'source_queries':0,'source_engine_calls':0,
      'universal_endpoint_existence_proved':False,'all_source_Objective_I':'OPEN','Objective_II':'DEFERRED',
      'input_sha256':{str(p):sha(p) for p in (ep,tp,F/'COMPLETE_MATCHING_NORMALIZATION.md',F/'reconstruct_control_complements.py')}}
    with (F/'control_complete_complements.json').open('x',encoding='utf8') as f:json.dump(result,f,indent=2)
    print(json.dumps({'status':result['status'],'controls':[{'source':r['source'],'complement_size':len(r['constructed_complement']),'outside_entry_neighborhoods':r['outside_single_step_entry_neighborhoods'],'paths':[p for p in r['paths'] if p['terminal_outside_root_entry_graph']]} for r in reports]}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_proof301_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
