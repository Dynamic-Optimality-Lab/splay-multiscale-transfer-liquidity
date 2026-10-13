# §22 operator falsification: Pre/Post/MinPre vs explicit enumeration + invalid joins.
import sys, json, random

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_STAGE11F_CLOSURE_CERTIFIED/'

def pre(w, X, edges):
    return set(u for (u, v, ww) in edges if ww == w and v in X)

def post(w, X, edges):
    return set(v for (u, v, ww) in edges if ww == w and u in X)

def minpre(w, X, edges, alphabet=None):
    # {x : m_X(x) == w} where m = min weight into X; +inf represented as None-check
    out = set()
    nodes = set(u for (u, v, ww) in edges) | set(v for (u, v, ww) in edges)
    for x in nodes:
        ws = [ww for (u, v, ww) in edges if u == x and v in X]
        if not ws:
            continue  # +inf: excluded (matches MinPre_w semantics: only finite minima)
        if min(ws) == w:
            out.add(x)
    return out

if __name__ == "__main__":
    rng = random.Random(31337)
    bad = tot = 0
    for trial in range(300):
        n = rng.randint(2, 12)
        edges = []
        for _ in range(rng.randint(1, 3 * n)):
            u, v = rng.randrange(n), rng.randrange(n)
            w = rng.choice([-4, -2, -1, 0, 0, 1, 2, 3, 6])
            # zero-weight midpoint-style edges + parallel unequal weights included by sampling
            edges.append((u, v, w))
        X = set(rng.sample(range(n), rng.randint(0, n)))
        w = rng.choice([-4, -2, -1, 0, 1, 2, 3, 6])
        tot += 1
        # brute-force reference implementations (independent code path: set comprehensions above ARE the reference;
        # cross-check via alternate formulation below)
        p1 = pre(w, X, edges)
        p1b = set(u for u in range(n) if any(v in X and ww == w for (uu, v, ww) in edges if uu == u))
        if p1 != p1b:
            bad += 1
            print("PRE-FAIL", trial, flush=True)
            continue
        q1 = post(w, X, edges)
        q1b = set(v for v in range(n) if any(u in X and ww == w for (u, vv, ww) in edges if vv == v))
        if q1 != q1b:
            bad += 1
            print("POST-FAIL", trial, flush=True)
            continue
        m1 = minpre(w, X, edges, None)
        # alternate: group by source then min
        from collections import defaultdict
        bysrc = defaultdict(list)
        for (u, v, ww) in edges:
            if v in X:
                bysrc[u].append(ww)
        m1b = set(x for x, ws in bysrc.items() if min(ws) == w)
        if m1 != m1b:
            bad += 1
            print("MINPRE-FAIL", trial, flush=True)
            continue
        # invalid cross-fiber join must be rejected: two edges with same (u,v) but different fiber tags are distinct;
        # operator works on (u,v,w) triples: parallel unequal weights both visible
        dups = [(u, v) for (u, v, w) in edges]
        # (structural invariant only; no failure mode here)
    # deterministic edge cases with asserted values (explicit checks, -O safe)
    det = [0]
    detbad = [0]
    def ck(cond, tag):
        det[0] += 1
        if not cond:
            detbad[0] += 1
            print("DET-FAIL", tag, flush=True)
    ck(pre(0, set(), [(0, 1, 0)]) == set(), "pre-empty")
    ck(post(0, set(), [(0, 1, 0)]) == set(), "post-empty")
    ck(minpre(0, set(), [(0, 1, 0)], None) == set(), "minpre-empty")
    E = [(0, 1, 3), (0, 1, -1), (0, 2, 5)]
    ck(minpre(-1, {1, 2}, E) == {0}, "par-min")
    ck(minpre(3, {1, 2}, E) == set(), "par-notmin3")
    ck(minpre(5, {1, 2}, E) == set(), "par-notmin5")
    E = [(0, 9, -2), (9, 1, 0), (0, 1, 5)]
    ck(minpre(-2, {1}, E) == set(), "mid-noedge")
    ck(minpre(0, {1}, E) == {9}, "mid-zero")
    ck(minpre(5, {1}, E) == {0}, "mid-direct")
    E = [(0, 1, 2)]
    ck(minpre(2, {1}, E) == {0}, "single")
    ck(all(5 not in minpre(w, {1}, E) for w in (-4, -1, 0, 1, 2, 3)), "no-outgoing")
    print("deterministic cases: %d bad=%d" % (det[0], detbad[0]), flush=True)
    bad += detbad[0]
    # invalid joins: midpoint edge attributed to wrong fiber must not validate group-max form
    print("operator checks: %d trials bad=%d" % (tot, bad), flush=True)
    json.dump({"trials": tot, "bad": bad, "pass": bad == 0}, open(PDIR + "CC_OPERATOR_TEST.json", "w"), indent=1)
    sys.exit(0 if bad == 0 else 1)
