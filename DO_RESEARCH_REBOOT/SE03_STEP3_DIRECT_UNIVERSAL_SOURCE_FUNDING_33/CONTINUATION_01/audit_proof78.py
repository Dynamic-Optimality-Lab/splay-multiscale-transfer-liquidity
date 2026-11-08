import json,time,hashlib
from pathlib import Path
from finite_source_word_compiler import Compiler
B=Path(__file__).resolve().parent
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    old=json.loads((B/'geodesic_seven_metric_table.json').read_text());native={'trees':old['trees'],'destination':old['source_destinations'],'H':old['source_H'],'Q':old['source_Q']};c=Compiler(native);result=json.loads((B/'directed_source_distance_family_candidate.json').read_text());records=[]
    for kind in ('constant_negative_edge','unchanged_both_directed_distances_negative_edge'):
        e=result[kind];assert e;w=c.compile(e['A'],e['B'],e['DELETE_helper_or_0'],e['KEEP_target']);assert (w['H'],w['Q'])==(e['H'],e['Q']) and 2*w['A']>=w['QF'];records.append({'kind':kind,'source_edge':e,'closed_history':w})
    out('directed_source_distance_closed_sources.json',{'status':'DIRECTED_PREPARATION_DISTANCE_SOURCE_REFUTATION_CANDIDATE','native_keys':7,'records':records,'original_cost':'actual ceil(edge-depth/2) splay events; not arbitrary single rotations or paper node costs','refuted_candidates':['entire DELETE-safe directed-distance cone','any fixed function of the ordered pair of directed preparation distances alone'],'uniform_DELETE_lemma_preserved':True,'new_source_queries':0,'principal_U33':'OPEN','independent_audit':'PENDING','input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('directed_source_event_distances7.json','directed_source_distance_family_candidate.json','geodesic_seven_metric_table.json','DIRECTED_SOURCE_DISTANCE_DELETE_LEMMA.md','DIRECTED_SOURCE_DISTANCE_DELETE_CONE.md','finite_source_word_compiler.py')}});print(json.dumps({'status':'DIRECTED_DISTANCE_CLOSED_SOURCES_COMPILED','histories':len(records),'costs':[(r['closed_history']['H'],r['closed_history']['Q']) for r in records]}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof78_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
