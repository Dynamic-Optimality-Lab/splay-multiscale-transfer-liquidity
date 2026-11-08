"""Read-only path-set diagnosis; do not repeat completed content checks."""
import json,collections
from pathlib import Path
from entry import BASE
baseline=json.loads((BASE/'entry_baseline.json').read_text())
old={r['path'] for r in baseline['files']}
added=[p for p in Path('DO_RESEARCH_REBOOT').rglob('*') if p.is_file() and BASE not in p.parents and p.as_posix() not in old]
rows=[{'path':p.as_posix(),'bytes':p.stat().st_size,'mtime_ns':p.stat().st_mtime_ns} for p in sorted(added)]
obj={'baseline_old_files':len(old),'new_outside_paths':rows,'no_content_or_source_predicates_rechecked':True}
with (BASE/'integrity_additions.json').open('x',encoding='utf-8') as f:json.dump(obj,f,indent=2)
groups=collections.Counter('/'.join(p.parts[:4]) for p in added)
print(json.dumps({'new_outside_count':len(added),'groups':dict(groups),'sample':[r['path'] for r in rows[:12]]},indent=2))
