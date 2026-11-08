"""Same authorized query cap; retain eight queries for a candidate replay.

The former thirty-query worker guard was a search scheduling reserve,
not a user allowance. All controller query/CPU limits stay unchanged.
"""
from pathlib import Path
p=Path(__file__).with_name('search_full_source15_beam_fullAB.py');s=p.read_text()
s=s.replace("exec(compile(s,str(Path(__file__).resolve()),'exec'))",'')
env={'__file__':str(p),'__name__':'source_builder_only'};exec(compile(s,str(p),'exec'),env);s=env['s']
assert s.count('QCAP-30')==1;s=s.replace('QCAP-30','QCAP-8')
s=s.replace("F/'search_full_source15_beam_fullAB.py')}}", "F/'search_full_source15_beam_fullAB.py',F/'search_full_source15_beam_fullAB_reserve8.py')}}")
exec(compile(s,str(Path(__file__).resolve()),'exec'))
