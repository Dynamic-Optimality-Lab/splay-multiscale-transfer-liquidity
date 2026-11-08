from pathlib import Path
F=Path(__file__).resolve().parent
code=(F/'audit_branch_H2_resumable.py').read_text()
old="    for name in ('vals','canonical','hasmark','reduce'):setattr(g,name,functools.lru_cache(maxsize=20000)(getattr(g,name)))\n    g.p.frames.apply=functools.lru_cache(maxsize=20000)(g.p.frames.apply)\n"
assert code.count(old)==1;code=code.replace(old,'')
assert code.count('end=min(start+100,5947)')==1;code=code.replace('end=min(start+100,5947)','end=min(start+200,5947)')
with (F/'audit_branch_H2_resumable_v3.py').open('x',encoding='utf-8') as f:f.write(code)
print('PURE_GRAMMAR_AUDITOR_WITH_SMALL_SAVED_INTERVALS_CREATED')
