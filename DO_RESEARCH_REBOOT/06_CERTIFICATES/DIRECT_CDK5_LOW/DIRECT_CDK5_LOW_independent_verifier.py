"""Independent verifier v2: tuple-engine-only re-derivation of every edge +
inequality check + vertex-order check. Fails loudly on any mismatch."""
import sys, json, itertools
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_LOW')
import splay as S
import wp6_cycle_ratio as O

def T(t, x):
    return S.trace(t, x)[0]
def dep(t):
    out = {}
    def go(nd, d):
        if nd[0] == "leaf":
            return
        _, k, l, r = nd
        out[k] = d; go(l, d + 1); go(r, d + 1)
    go(t, 0)
    return out
def ser(t):
    if t[0] == "leaf":
        return '.'
    _, k, l, r = t
    return (k, ser(l), ser(r))
def unser(ss):
    if ss == '.':
        return S.LEAF
    k, l, r = ss
    return S.node(k, unser(l), unser(r))
def leaves(s):
    if s == '.':
        return set()
    k, l, r = s
    if l == '.' and r == '.':
        return {k}
    return leaves(l) | leaves(r)
def keys(s):
    if s == '.':
        return set()
    k, l, r = s
    return {k} | keys(l) | keys(r)
def prune(s, M):
    if s == '.':
        return '.'
    k, l, r = s
    lp, rp = prune(l, M), prune(r, M)
    return (k, lp, rp) if (k in M or lp != '.' or rp != '.') else '.'
def recomp(s):
    ks = sorted(keys(s))
    rk = {k: i + 1 for i, k in enumerate(ks)}
    def go(nd):
        if nd == '.':
            return '.'
        k, l, r = nd
        return (rk[k], go(l), go(r))
    return go(s), rk
def totup(t):
    if t is None:
        return S.LEAF
    return S.node(t[0], totup(t[1]), totup(t[2]))

CACHE = {}
def shapes(n):
    if n not in CACHE:
        CACHE[n] = O.shapes_of(list(range(1, n + 1)))
    return CACHE[n]

man = json.load(open(RDIR / 'DIRECT_CDK5_LOW_graph_manifest.json'))
E = json.load(open(RDIR / 'DIRECT_CDK5_LOW_graph_edges.json'))["edges"]
cert = json.load(open(RDIR / 'DIRECT_CDK5_LOW_potential_certificate.json'))
assert cert["positive_cycle"] is False
eta = cert["eta"]
vtab = man["vert_table"]
# vertex correspondence via (n, shape, M) keys (generator ids are discovery-
# ordered, NOT enumeration-ordered)
gen_id_of = {(v["n"], v["shape"], tuple(v["M"])): v["id"] for v in vtab}
assert len(gen_id_of) == man["vertices"]
own_keys = set()
for n in (5, 6, 7, 8):
    for T0 in shapes(n):
        s = ser(totup(T0))
        for Mc in itertools.combinations(range(1, n + 1), 5):
            if leaves(s) <= set(Mc):
                own_keys.add((n, repr(s), Mc))
assert own_keys == set(gen_id_of.keys()), "vertex SET mismatch"
print("vertex set: OK (%d)" % len(own_keys), flush=True)

by_u = {}
for e in E:
    by_u.setdefault(e[0], []).append(e)
mismatch = badineq = 0
tot = 0
for n in (5, 6, 7, 8):
    for T0 in shapes(n):
        s = ser(totup(T0))
        for Mc in itertools.combinations(range(1, n + 1), 5):
            if not (leaves(s) <= set(Mc)):
                continue
            u = gen_id_of[(n, repr(s), Mc)]
            M = set(Mc)
            t = unser(s)
            dd = dep(t)
            root = s[0]
            re_rows = []
            for x in sorted(M):
                t2 = T(t, x)
                pr = prune(ser(t2), M)
                rc, rk = recomp(pr)
                M2 = tuple(sorted(rk[m] for m in M))
                v2 = gen_id_of[(len(keys(rc)), repr(rc), M2)]
                w2 = dd[x] // 2 - 2 * (1 if x != root else 0)
                re_rows.append([u, v2, w2])
            stored = [[e[0], e[1], e[2]] for e in by_u.get(u, [])]
            tot += 1
            if re_rows != stored:
                mismatch += 1
                if mismatch <= 3:
                    print("EDGE MISMATCH u=%d: %s vs %s" % (u, re_rows, stored))
            for (uu, vv, ww, d, chg) in by_u.get(u, []):
                if ww + eta[vv] - eta[uu] > 0:
                    badineq += 1
print("vertices rechecked=%d edge-mismatch=%d inequ-violations=%d" % (
    tot, mismatch, badineq), flush=True)
assert mismatch == 0 and badineq == 0
print("INDEPENDENT VERIFICATION: PASS", flush=True)
json.dump({"vertices": tot, "edge_mismatch": mismatch,
           "inequ_violations": badineq, "verdict": "PASS"},
          open(RDIR / 'DIRECT_CDK5_LOW_independent_verification.json', 'w'), indent=1)
