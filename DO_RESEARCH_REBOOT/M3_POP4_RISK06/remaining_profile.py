"""Describe the already verified scope boundary; no mathematical checks replayed."""
import json
from pathlib import Path
BASE=Path(__file__).resolve().parent
comb=json.loads((BASE/'combination_check.json').read_text())
run=json.loads((BASE/'run_result.json').read_text())
remaining=comb['unresolved_total4_signatures'];assert len(remaining)==7
rows=[];representatives=set()
for sig in remaining:
    gaps=[i for i,n in enumerate(sig) if n]
    assert len(gaps)==4 and sum(sig)==4 and gaps[-1]-gaps[0]==9
    canonical=max(tuple(sig),tuple(sig[::-1]));representatives.add(canonical)
    interrupted=list(canonical)==run['failure']['sigma']
    rows.append({'sigma':sig,'gap_indices':gaps,'canonical_sigma':canonical,'self_reflecting':sig==sig[::-1],
      'status':'INDEPENDENT_AUDIT_CPU_CAP_UNKNOWN' if interrupted else 'UNSTARTED',
      'complete_enumeration_and_construction_saved':interrupted,'original_negative_cycle_certified':False})
assert len(representatives)==5
obj={'total4_covered':708,'total4_unresolved':7,'remaining_reflection_representatives':5,
  'all_total4_support_at_most_three_covered':True,'all_total4_support_span_at_most_eight_covered':True,
  'sectors':rows,'mathematical_checks_or_source_predicates_replayed':0}
with (BASE/'remaining_sectors.json').open('x',encoding='utf-8') as f:json.dump(obj,f,indent=2)
print(json.dumps({'remaining_original_sectors':7,'canonical_cases':5,'gap_sets':[r['gap_indices'] for r in rows]}))
