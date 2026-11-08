"""Add the exact resource-stop explanation to packaging; no tests replayed."""
from pathlib import Path
BASE=Path(__file__).resolve().parent
s=(BASE/'finalize.py').read_text()
old="      'failure':run['failure'],'source_failure':cert['failure'],'finite_only_unpromoted_signatures':cert['finite_only_signatures'],"
assert s.count(old)==1
s=s.replace(old,"      'failure':run['failure'],'resource_stop_details':read(BASE/'RESOURCE_STOP.json'),'source_failure':cert['failure'],'finite_only_unpromoted_signatures':cert['finite_only_signatures'],")
old="      'Current unpromoted finite-only cases:'+json.dumps(cert['finite_only_signatures'])+'.',"
assert s.count(old)==1
s=s.replace(old,"      'RESOURCE STOP: e0+e1+e4+e8 completed 960889 canonical queries. The next whole word family would exceed the fixed 1000000-query cap, so admission stopped before its queries. This is NOT CPU exhaustion, a refuted potential template or a negative original cycle. See RESOURCE_STOP.json.',\n      'To continue under unchanged caps, first prove a complete representation requiring fewer canonical queries for the capped signature. Further CPU renewal alone does not remove this limit.',\n"+old)
compile(s,str(BASE/'finalize_v2.py'),'exec')
with (BASE/'finalize_v2.py').open('x',encoding='utf-8') as f:f.write(s)
print('Prepared resource-explanation packaging v2; all mathematical checks unchanged.')
