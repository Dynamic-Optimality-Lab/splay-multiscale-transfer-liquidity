"""Same literal source graph; adaptive garbage collection under fixed caps."""
from pathlib import Path
parent=Path(__file__).with_name('search_global_probe11_DAG_H3.py').read_text()
marker="source=source.replace('LOW_ALL_NATIVE11_COMPLETE','LOW_AND_ADDED_H3_SUBGRAPH_COMPLETE')"
extra=r"""
needle='cycle=None;limit=None;ap=Apply(dag);candidate_roots=collections.OrderedDict()'
assert source.count(needle)==1
source=source.replace(needle,needle+';gc_threshold=max(450000,len(dag.nodes)+100000)')
needle='if len(dag.nodes)>400000:ap.collect(columns);candidate_roots.clear()'
assert source.count(needle)==1
source=source.replace(needle,'if len(dag.nodes)>gc_threshold:\n            ap.collect(columns);candidate_roots.clear();gc_threshold=min(1000000,len(dag.nodes)+100000)')
needle='            ap.collect(columns);candidate_roots.clear()\n'
assert source.count(needle)==1
source=source.replace(needle,'            ap.collect(columns);candidate_roots.clear();images.clear();imagecells=0;dense.clear();densecells=0;memo.clear();ap.cache.clear();ap.maxcache.clear();gc_threshold=min(1000000,len(dag.nodes)+100000)\n')
"""
assert parent.count(marker)==1
parent=parent.replace(marker,marker+'\n'+extra)
exec(compile(parent,str(Path(__file__).resolve()),'exec'))
