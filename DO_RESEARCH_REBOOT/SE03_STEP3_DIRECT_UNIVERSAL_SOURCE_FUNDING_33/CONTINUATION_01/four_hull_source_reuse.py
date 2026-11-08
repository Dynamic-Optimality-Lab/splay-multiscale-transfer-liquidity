"""Reuse the already produced four-node primitive identities, not new queries."""
import collections
from four_hull_source_compiler import HullCompiler
from interior_projection_source_tools import fr
def from_kernel(data):
    G=HullCompiler.__new__(HullCompiler);G.T=tuple(map(fr,data['trees']));G.idx={t:i for i,t in enumerate(G.T)};G.dest=data['destinations'];G.H=data['H'];G.words={};G.instantiations=0
    for s in range(14):
        seen={s:[]};q=collections.deque([s])
        while q:
            v=q.popleft()
            for k,u in enumerate(G.dest[v],1):
                if u not in seen:seen[u]=seen[v]+[k];q.append(u)
        assert len(seen)==14
        for u,w in seen.items():G.words[s,u]=w
    return G
