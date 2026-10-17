# G01_INDEPENDENT_GRAPH_ORACLE.py — Phase K independent oracle (no production code).
# Explicit finite digraphs with sorts; contraction; Bellman-Ford negative-cycle
# detection with super-source; potential construction (shortest paths) +
# verification; sector-tagged graphs. K1-K12 executed by G01_ORACLE_RUN.py.
import itertools

INF = 10 ** 18


class IGraph:
    def __init__(self, O, M, edges):
        # edges: {(i,j,w): set((x,y))}, i,j in {0,1}
        self.O, self.M = list(O), list(M)
        self.edges = {(i, j, w): set(v) for (i, j, w), v in edges.items()}

    def verts(self):
        return [(0, x) for x in self.O] + [(1, x) for x in self.M]

    def all_edges(self):
        out = []
        for (i, j, w), ps in self.edges.items():
            for (x, y) in ps:
                out.append(((i, x), (j, y), w))
        return out

    def contract(self):
        """Contract O->M (any w) + M->O (w=0 only) into O->O parallel edges."""
        new = dict(self.edges)
        for (i, j, w), ps in list(self.edges.items()):
            if (i, j) == (0, 1):
                for (s, m) in ps:
                    for (m2, t) in self.edges.get((1, 0, 0), set()):
                        if m2 == m:
                            new.setdefault((0, 0, w), set()).add((s, t))
        return new

    def has_negative_cycle(self):
        """Bellman-Ford with super-source; returns (has_neg, cycle_or_None)."""
        V = self.verts()
        idx = {v: k for k, v in enumerate(V)}
        E = self.all_edges()
        dist = {v: 0 for v in V}  # super-source: all zero-initialized
        pred = {}
        x = None
        for _ in range(len(V)):
            x = None
            for (u, v, w) in E:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    pred[v] = (u, w)
                    x = v
        if x is None:
            return (False, None)
        y = x
        for _ in range(len(V)):
            y = pred[y][0]
        cyc, cur = [], y
        while True:
            p, w = pred[cur]
            cyc.append((p, cur, w))
            cur = p
            if cur == y or len(cyc) > len(V) + 1:
                break
        return (True, cyc)

    def potential(self):
        """Shortest-path potential from super-source (None iff negative cycle)."""
        V = self.verts()
        E = self.all_edges()
        dist = {v: 0 for v in V}
        for _ in range(max(1, len(V) - 1)):
            for (u, v, w) in E:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
        for (u, v, w) in E:
            if dist[u] + w < dist[v]:
                return None
        return dist

    def check_potential(self, phi):
        bad = []
        for (u, v, w) in self.all_edges():
            if not (phi[v] - phi[u] <= w):
                bad.append((u, v, w))
        return bad

    def closed_walk_weight(self, seq):
        """seq: list of vertices with seq[0]==seq[-1]; None if an edge missing."""
        tot = 0
        E = {}
        for (u, v, w) in self.all_edges():
            E.setdefault((u, v), []).append(w)
        for a, b in zip(seq[:-1], seq[1:]):
            ws = E.get((a, b))
            if not ws:
                return None
            tot += min(ws)
        return tot


def all_subsets(s):
    out = []
    for r in range(len(s) + 1):
        for c in itertools.combinations(s, r):
            out.append(set(c))
    return out
