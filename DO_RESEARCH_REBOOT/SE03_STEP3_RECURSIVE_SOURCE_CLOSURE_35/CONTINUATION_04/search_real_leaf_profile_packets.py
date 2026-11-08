"""Explicitly derive the paired-source information test from proof223.
The only graph edges are actual single macros or pinned realized pairs.
The old natural-macro search and its evidence remain unchanged.
"""
from pathlib import Path
source=Path(__file__).with_name('search_leaf_pruning_profile.py').read_text()
changes=[
('''    groups={}
    for h in (1,2):
        for rid,(s,x,t) in enumerate(z[f'H{h}_rows']):groups.setdefault((h,z['A_roots'][s],x),[]).append((s,t,rid))
    groups={k:np.array(v,dtype=np.int32) for k,v in groups.items()}
''','''    with (F/'real_leaf_profile_packets.pkl').open('rb') as f:pm=pickle.load(f)
    groups={k:np.array([(s,t,i) for i,(s,t,w) in enumerate(v)],dtype=np.int32).reshape((-1,3)) for k,v in pm['groups'].items()}
'''),
('''    for eid,e in enumerate(z['B_edges']):bedges[e['source']].append((eid,e))''',
 '''    for eid,e in enumerate(pm['packets']):bedges[e['source']].append((eid,e))'''),
('''            bt,x=e['target'],(e['key']-1)//2;ft=features(bt)
            for h in (1,2):
                aa=groups[h,g,x];src,dst=aa[:,0],aa[:,1];assert np.all(fs[src]>=0) and np.all(ft[dst]>=0)''',
 '''            bt=e['target'];ft=features(bt)
            for h,key in e['low']:
                aa=groups[key]
                if len(aa)==0:continue
                src,dst=aa[:,0],aa[:,1];assert np.all(fs[src]>=0) and np.all(ft[dst]>=0)'''),
("edge=(s,t,2*h-e['q'],eid,h,int(aa[j,2]),int(src[j]),int(dst[j]))",
 "edge=(s,t,2*h-e['Q'],eid,h,int(aa[j,2]),int(src[j]),int(dst[j]),key)"),
("'source_row':edges[i][5],'A_source':edges[i][6],'A_target':edges[i][7]}",
 "'source_row':edges[i][5],'A_source':edges[i][6],'A_target':edges[i][7],'source_group':edges[i][8]}"),
("'B_edge':edges[i][3]","'packet_id':edges[i][3]"),
("leaf_profile_search_","real_leaf_profile_search_"),
("'scope':'ALL functions of full B and the complete leaf-indexed unchanged D6 vector'",
 "'scope':'ALL functions of full B and complete leaf-indexed unchanged D6 vector, EVEN WITH actual q6/q1 PAIRING'")]
for old,new in changes:
    assert source.count(old)>=1,(old[:70],source.count(old))
    source=source.replace(old,new)
exec(compile(source,str(Path(__file__).resolve()),'exec'))
