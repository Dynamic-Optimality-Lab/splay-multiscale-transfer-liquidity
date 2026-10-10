"""PHASE 3: exact weighted marked-core graph (5 marks, cores 5..8).

Vertices: valid BST marked cores (all leaves marked). Edges: marked splay +
prune-to-ancestors + order-preserving recompression. Weight w = d//2 - 2*[x!=root].
Both engines, exact ints, deterministic order. No edge discarded except from
invalid (non-leaf-marked) states, which real projections never visit.
"""
import sys, copy, json, itertools
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'python/liquidity')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_LOW')
from wp6_eventflow import to_ptr, splay_A
import splay as S
import wp6_cycle_ratio as O

def pdepths(t):
    out = {}
    def go(nd, d):
        if nd is None:
            return
        out[nd["k"]] = d
        go(nd["l"], d + 1); go(nd["r"], d + 1)
    while t["p"] is not None:
        t = t["p"]
    go(t, 0)
    return out
def pserial(t):
    while t["p"] is not None:
        t = t["p"]
    def go(nd):
        if nd is None:
            return '.'
        return (nd["k"], go(nd["l"]), go(nd["r"]))
    return go(t)
def proot(t):
    while t["p"] is not None:
        t = t["p"]
    return t["k"]
def to_tup(t):
    if t is None:
        return S.LEAF
    return S.node(t[0], to_tup(t[1]), to_tup(t[2]))
def idepths(t):
    out = {}
    def go(nd, d):
        if nd[0] == "leaf":
            return
        _, k, l, r = nd
        out[k] = d; go(l, d + 1); go(r, d + 1)
    go(t, 0)
    return out
def iserial(t):
    if t[0] == "leaf":
        return '.'
    _, k, l, r = t
    return (k, iserial(l), iserial(r))
def leaves(serial):
    if serial == '.':
        return set()
    k, l, r = serial
    if l == '.' and r == '.':
        return {k}
    return leaves(l) | leaves(r)
def keys_of(serial):
    if serial == '.':
        return set()
    k, l, r = serial
    return {k} | keys_of(l) | keys_of(r)
def prune_to_core(serial, M):
    """Keep nodes ancestral to M (incl self); drop maximal mark-free subtrees."""
    if serial == '.':
        return '.'
    k, l, r = serial
    lp, rp = prune_to_core(l, M), prune_to_core(r, M)
    if k in M or lp != '.' or rp != '.':
        return (k, lp, rp)
    return '.'
def recompress(serial):
    """Order-preserving rank relabel; returns (serial, rankmap)."""
    ks = sorted(keys_of(serial))
    rk = {k: i + 1 for i, k in enumerate(ks)}
    def go(nd):
        if nd == '.':
            return '.'
        k, l, r = nd
        return (rk[k], go(l), go(r))
    return go(serial), rk

CACHE = {}
def shapes(n):
    if n not in CACHE:
        CACHE[n] = O.shapes_of(list(range(1, n + 1)))
    return CACHE[n]

LOG = open(RDIR / 'DIRECT_CDK5_LOW_graph_build.log', 'w')
def log(s):
    LOG.write(s + "\n"); LOG.flush(); print(s, flush=True)

vid = {}
verts = []  # (n, shape_str, M_tuple)
def get_vid(key):
    if key not in vid:
        vid[key] = len(verts)
        verts.append(key)
    return vid[key]

raw_total = 0
edges = []  # (u, v, w, d, chg)
eng_bad = 0
size_drop = 0
for n in (5, 6, 7, 8):
    nraw = 0
    nvert_before = len(verts)
    for T0 in shapes(n):
        keys = list(range(1, n + 1))
        for Mc in itertools.combinations(keys, 5):
            M = set(Mc)
            S0 = (T0[0],)  # placeholder
            # build tuple-serial of this shape
            def tup(t):
                if t is None:
                    return '.'
                return (t[0], tup(t[1]), tup(t[2]))
            ser = tup(T0)
            if not leaves(ser) <= M:
                # invalid core state: still counts as raw inventory, no edges
                nraw += 5
                raw_total += 5
                continue
            u = get_vid((n, repr(ser), tuple(sorted(M))))
            for x in sorted(M):
                nraw += 1
                raw_total += 1
                P = to_ptr(copy.deepcopy(T0))
                d0 = pdepths(P); r0 = proot(P)
                P2, _ = splay_A(P, x)
                s1 = pserial(P2)
                T = to_tup(copy.deepcopy(T0))
                T2, _ = S.trace(T, x)
                e0 = idepths(T)
                if not (iserial(T2) == s1 and d0 == e0):
                    eng_bad += 1
                    if eng_bad <= 3:
                        log("ENGINE MISMATCH n=%d" % n)
                    continue
                w = d0[x] // 2 - 2 * (1 if x != r0 else 0)
                pr = prune_to_core(s1, M)
                rc, rk = recompress(pr)
                n2 = len(keys_of(rc))
                M2 = tuple(sorted(rk[m] for m in M))
                v = get_vid((n2, repr(rc), M2))
                if n2 != n:
                    size_drop += 1
                edges.append((u, v, w, d0[x], 1 if x != r0 else 0))
    log("n=%d: raw=%d valid-verts-so-far=%d" % (n, nraw, len(verts) - 0))
log("RAW TOTAL=%d (expect 449615)" % raw_total)
log("vertices=%d edges=%d size_drops=%d eng_bad=%d" % (
    len(verts), len(edges), size_drop, eng_bad))
json.dump({"raw_total": raw_total, "vertices": len(verts), "edges": len(edges),
           "size_drops": size_drop, "eng_bad": eng_bad,
           "vert_table": [{"id": i, "n": v[0], "shape": v[1], "M": list(v[2])}
                          for i, v in enumerate(verts)]},
          open(RDIR / 'DIRECT_CDK5_LOW_graph_manifest.json', 'w'))
# edges compact: list of [u,v,w]
json.dump({"edges": edges},
          open(RDIR / 'DIRECT_CDK5_LOW_graph_edges.json', 'w'), indent=None)
log("graph saved")
LOG.close()
