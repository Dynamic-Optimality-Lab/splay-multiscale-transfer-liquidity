"""Resume the same audit with the inherited seed sentinel parsed correctly.

V001 completed its declared source search but read the seed predecessor [-1,0]
as an edge. It stopped before writing the result certificate. This wrapper
changes only that loop guard and verifies, rather than overwrites, entry pins.
No source class, selection order, reservation or theorem is changed.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
original = HERE / 'audit_first_return.py'
source = original.read_text(encoding='utf-8')
old = "while graph['predecessors'][state] is not None:"
new = "while graph['predecessors'][state][0] >= 0:"
assert source.count(old) == 1
namespace = {'__file__': str(original), '__name__': 'first_return_audit_v002'}
exec(compile(source.replace(old, new), str(original), 'exec'), namespace)
exclusive_save = namespace['save']


def resume_save(name, value):
    if name == 'entry_source_pins.json':
        assert json.loads((HERE / name).read_text(encoding='utf-8')) == value
    else:
        exclusive_save(name, value)


namespace['save'] = resume_save
namespace['main']()
