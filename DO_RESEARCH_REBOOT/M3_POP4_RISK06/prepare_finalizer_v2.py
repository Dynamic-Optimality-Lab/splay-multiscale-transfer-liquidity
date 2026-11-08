"""Explain the CPU stop in packaging; do not change or repeat mathematical checks."""
from pathlib import Path
BASE=Path(__file__).resolve().parent
s=(BASE/'finalize.py').read_text()
needle="      'failure':run['failure'],'source_failure':cert['failure'],'finite_only_unpromoted_signatures':cert['finite_only_signatures'],"
assert s.count(needle)==1
s=s.replace(needle,"      'failure':run['failure'],'audit_stop_details':read(BASE/'AUDIT_STOP_NOTE.json'),'source_failure':cert['failure'],'finite_only_unpromoted_signatures':cert['finite_only_signatures'],")
needle="      'Current unpromoted finite-only cases:'+json.dumps(cert['finite_only_signatures'])+'.',"
assert s.count(needle)==1
s=s.replace(needle,"      'AUDIT STOP: e0+e2+e7+e9 completed all independent grammar/count/family and potential-range checks at1,314,758 queries, below2m. The120 CPU-second computation guard stopped residual checking. Its candidate is NOT certified; no mathematical contradiction or original negative cycle was established.',\n      'The renewed cumulative allowance was not exhausted:3411.6875/7200 CPU seconds charged. This is a per-phase audit CPU stop; no later case was started, and no failed audit was retried or split. See AUDIT_STOP_NOTE.json.',\n"+needle)
compile(s,str(BASE/'finalize_v2.py'),'exec')
with (BASE/'finalize_v2.py').open('x',encoding='utf-8') as f:f.write(s)
print('Prepared explicit CPU-stop report; all mathematical checks unchanged.')
