"""Use only the remaining authorized queries; no prospective replay reserve.

Any new source candidate must await its distinct replay allowance before
acceptance. This changes no source cost or cumulative query authorization.
"""
from pathlib import Path
p=Path(__file__).with_name('search_full_source15_beam_diverse.py');s=p.read_text()
s=s.replace("exec(compile(s,str(Path(__file__).resolve()),'exec'))",'')
env={'__file__':str(p),'__name__':'source_builder_only'};exec(compile(s,str(p),'exec'),env);s=env['s']
assert s.count('QCAP-8')==1;s=s.replace('QCAP-8','QCAP')
s=s.replace("F/'search_full_source15_beam_diverse.py')}}", "F/'search_full_source15_beam_diverse.py',F/'search_full_source15_beam_last_queries.py')}}")
exec(compile(s,str(Path(__file__).resolve()),'exec'))
