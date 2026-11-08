"""Complete the fixed source provenance audit; preserve V001 and its output."""
import importlib.util
import json
from collections import deque
from pathlib import Path

HERE=Path(__file__).resolve().parent
original=HERE/'build_paired_certificates.py'
source=original.read_text(encoding='utf-8')
old="root_child_DELETE_connector=connector,connector_visited_shapes=visited,connector_shape_bound=42,"
new="A_DELETE_connector=connector,connector_method='original_A_splays_with_B_frozen',connector_visited_shapes=visited,connector_shape_bound=42,reachability_refinement_sha256=sha(HERE/'PC00B_REACHABILITY_REFINEMENT_GATE.md'),"
assert source.count(old)==1
namespace={'__file__':str(original),'__name__':'paired_certificate_resume_v002'}
exec(compile(source.replace(old,new),str(original),'exec'),namespace)
exclusive_save=namespace['save']


def resume_save(name,value):
    if name=='walk_deep_certificate.json':
        assert json.loads((HERE/name).read_text(encoding='utf-8'))==value
    else:exclusive_save(name,value)


def legal_DELETE_connector(start,target):
    encode=lambda t:json.dumps(t,separators=(',',':'))
    first,goal=encode(start),encode(target);parent={first:None};trees={first:start};queue=deque([first])
    while queue and goal not in parent:
        key=queue.popleft();t=trees[key]
        for access in [1,2,3,4,5]:
            dest,events=namespace['splay'](t,access);k=encode(dest)
            if k not in parent:parent[k]=(key,access);trees[k]=dest;queue.append(k)
        assert len(parent)<=42
    if goal not in parent:
        exclusive_save('fixed_A_only_reachability_absence.json',dict(status='TARGET_ABSENT_FROM_FIXED_A_ONLY_SOURCE_COMPONENT',
            start=start,target=target,visited_shapes=len(parent),states=[trees[k] for k in parent],
            queue_exhausted=True,no_universal_unreachability_claim=True))
        raise RuntimeError('fixed original A-only connector absent; paired provenance audit required by PC00B')
    accesses=[];at=goal
    while parent[at] is not None:
        at,access=parent[at];accesses.append(access)
    return accesses[::-1],len(parent)


namespace['save']=resume_save
namespace['root_child_connector']=legal_DELETE_connector
namespace['main']()
