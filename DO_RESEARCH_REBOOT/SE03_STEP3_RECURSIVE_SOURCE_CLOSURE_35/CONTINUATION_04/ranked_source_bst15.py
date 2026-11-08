"""Same lossless source representation through n=15, with bounded caches."""
from pathlib import Path
p=Path(__file__).with_name('ranked_source_bst.py');s=p.read_text()
assert s.count('range(1,14)')==2
s=s.replace('range(1,14)','range(1,16)')
exec(compile(s,str(Path(__file__).resolve()),'exec'))
