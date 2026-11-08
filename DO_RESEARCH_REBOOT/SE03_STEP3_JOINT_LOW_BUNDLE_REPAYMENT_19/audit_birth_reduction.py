"""Producer projection of the source-derived leaf-birth grouping reduction.
Uses only NEW19 comparison/transposition records; no source replay/audit.
"""
import json,time
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,x):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(x,f,indent=2)
def pack(v):return [{'demand':d,'unit':u} for d,u in sorted(v.items())]
def main():
    source=json.loads((B/'zero_leaf_transposition.json').read_text(encoding='utf-8'));reports=[]
    for r in source['reports']:
        h={tuple(z['demand']):tuple(z['unit']) for z in r['alternative_partial_comparison']};pairs=[];remaining=[]
        for g in r['transported_birth_groups']:
            ds=[tuple(d) for d in g['transported_demands']];us=[tuple(u) for u in g['available_own_tail']]
            n=min(len(ds),len(us))
            for d,u in zip(ds[:n],us[:n]):
                assert d not in h and u not in set(h.values());h[d]=u;pairs.append((d,u))
            remaining.extend(ds[n:])
        assert len(set(h.values()))==len(h) and len(remaining)==1
        reports.append({'source':r['source'],'own_birth_tail_pairs':pairs,
          'remaining_actual_birth_demands':remaining,'extended_partial_comparison':pack(h),
          'source_engine_calls':0,'all_original_effective_owners_untouched':True,
          'not_a_new_capacity_unit_from_recoloring':True})
    out('birth_group_reduction.json',{'status':'SOURCE_DERIVATION_AUDIT_PENDING','reports':reports,
      'universal_rule':'After source transposition, group by actual unary B-leaf-birth macro and inject first min(arrivals,actual unused own tail) into its first unused physical units. Source inventories are disjoint.',
      'arbitrary_source_remaining_supply':'OPEN'})
    print(json.dumps({'status':'BIRTH_GROUP_REDUCTION_PASS','reports':[{'source':r['source'],
      'pairs':r['own_birth_tail_pairs'],'remaining':r['remaining_actual_birth_demands']} for r in reports]}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_birth_reduction_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,
      'source_engine_calls':0,'new_finite_tests':0,'old_semantic_rows_replayed':0})
