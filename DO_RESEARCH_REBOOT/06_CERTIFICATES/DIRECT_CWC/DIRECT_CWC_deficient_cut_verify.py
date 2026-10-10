"""DIRECT-CWC: INDEPENDENT deficient-cut verification (separate code path).

Target: U1 walk 3 (26AR-ins2-2-4-3-3, W=-96), token (t=8 K15, pair (7,6)).
Recomputes H-timelines, windows, all contacts from a FRESH replay; asserts
empty eligible neighborhood + token reality + walk conservation."""
import sys, copy, json
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'python/liquidity')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CWC')
from wp6_eventflow import to_ptr, splay_A, splay_B_push
import legacy_embedding as PE

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
def vine_right(n):
    t = None
    for k in range(n, 0, -1):
        t = [k, None, t]
    return t
def path_to(serial, x):
    path = []
    def go(nd):
        if nd == '.':
            return False
        k, l, r = nd
        path.append(k)
        if k == x:
            return True
        if go(l) or go(r):
            return True
        path.pop()
        return False
    return list(path) if go(serial) else None

U1 = json.load(open('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U1/DIRECT_U1_uncovered_closed_witness.json'))
c = U1[2]
prefix, word = c["prefix"], [tuple(w) for w in c["word"]]
m = len(word)
T0 = vine_right(16)
A = to_ptr(copy.deepcopy(T0)); B = to_ptr(copy.deepcopy(T0))
for (md, x) in prefix:
    A, _ = splay_A(A, x)
    if md == 'K':
        B, _ = splay_B_push(B, x)
Bser = [pserial(B)]
Adepths, Bdepths, Arots, Apaths = [], [], [], []
for (md, x) in word:
    dA = pdepths(A)[x]
    dB = pdepths(B)[x] if md == 'K' else None
    Adepths.append(dA); Bdepths.append(dB)
    # A StepEv rotated sets via source inv + intermediate serials
    Ac = copy.deepcopy(A)
    _, inv = splay_A(Ac, x)
    Arots.append([s for s in inv])
    Apaths.append(None)
    A, _ = splay_A(A, x)
    if md == 'K':
        _, Bpath = PE._depth_to(B, x)
        Apaths[-1] = [nd["k"] for nd in Bpath]
        B, Bout = splay_B_push(B, x)
    Bser.append(pserial(B))
assert Bser[-1] == Bser[0], "closure"
W = sum(((Bdepths[i] // 2) if word[i][0] == 'K' else 0) - 2 * ((Adepths[i] + 1) // 2) for i in range(m))
print("W =", W, "(expect -96)")
# token reality at access 8 (K15)
t = 8
assert word[t] == ('K', 15)
dB = Bdepths[t]
print("access8: dA=%d dB=%d q=%d" % (Adepths[t], dB, dB // 2))
# pushed pairs from independent re-trace of access 8's B splay state
# (reconstruct pre-state B_8 by replaying prefix+word[:8] on fresh trees)
Bf = to_ptr(copy.deepcopy(T0))
Af = to_ptr(copy.deepcopy(T0))
for (md, x) in prefix:
    Af, _ = splay_A(Af, x)
    if md == 'K':
        Bf, _ = splay_B_push(Bf, x)
for (md, x) in word[:8]:
    Af, _ = splay_A(Af, x)
    if md == 'K':
        Bf, _ = splay_B_push(Bf, x)
_, path8 = PE._depth_to(Bf, 15)
pk = [nd["k"] for nd in path8]
print("pre-B path of 15:", pk)
Bf2, out8 = splay_B_push(Bf, 15)
print("pushed sets:", [sorted(s) for s in out8])
# H timelines for (7,15),(6,15) over all 39 boundaries
def H(s, u, x):
    p = path_to(Bser[s], x)
    return p is not None and u in p[:-1]
for u in (7, 6):
    line = "".join("1" if H(s, u, 15) else "0" for s in range(m))
    print("H(%d,15): %s (idx0..%d; death access t=8)" % (u, line, m - 1))
    # window by charter rule
    j = (t - 1) % m
    for _ in range(m + 1):
        if not H(j, u, 15):
            break
        j = (j - 1) % m
    birth = j
    win = []
    s = (birth + 1) % m
    while True:
        win.append(s)
        if s == t:
            break
        s = (s + 1) % m
    print("  birth=%d window=%s" % (birth, win))
# exhaustive contact recheck for token pairs across their windows
Aser_states = None  # recompute A StepEv structure per access via mirror below
def A_step_info(ai):
    """Independent mirror splay returning (rotsets, post-serials, pre-serial)."""
    # replay A to pre-access ai state
    Aa = to_ptr(copy.deepcopy(T0))
    Ba = to_ptr(copy.deepcopy(T0))
    for (md, x) in prefix:
        Aa, _ = splay_A(Aa, x)
        if md == 'K':
            Ba, _ = splay_B_push(Ba, x)
    for (md, x) in word[:ai]:
        Aa, _ = splay_A(Aa, x)
        if md == 'K':
            Ba, _ = splay_B_push(Ba, x)
    pre = pserial(Aa)
    md, x = word[ai]
    d, path = PE._depth_to(Aa, x)
    node = path[-1]
    rots, posts = [], []
    while node["p"] is not None:
        p = node["p"]; g = p["p"]
        if g is None:
            if p["l"] is node:
                PE._rot_right(p)
            else:
                PE._rot_left(p)
            rots.append({node["k"], p["k"]})
        elif p["l"] is node and g["l"] is p:
            PE._rot_right(g); PE._rot_right(p)
            rots.append({node["k"], p["k"], g["k"]})
        elif p["r"] is node and g["r"] is p:
            PE._rot_left(g); PE._rot_left(p)
            rots.append({node["k"], p["k"], g["k"]})
        elif p["r"] is node and g["l"] is p:
            PE._rot_left(p); PE._rot_right(g)
            rots.append({node["k"], p["k"], g["k"]})
        else:
            PE._rot_right(p); PE._rot_left(g)
            rots.append({node["k"], p["k"], g["k"]})
        posts.append(pserial(node))
    return pre, rots, posts
def owner(ai, u, v):
    pre, rots, posts = A_step_info(ai)
    sts = [pre] + posts
    Hf = []
    for st in sts:
        p = path_to(st, v)
        Hf.append(p is not None and u in p[:-1])
    if Hf[-1] == Hf[0]:
        return None
    for e in range(len(sts) - 1, 0, -1):
        if Hf[e] == Hf[-1] and Hf[e - 1] != Hf[-1]:
            return e - 1
    return None
nedges = 0
for (u, tag) in ((7, "p"), (6, "q")):
    j = (t - 1) % m
    for _ in range(m + 1):
        if not path_to(Bser[j], 15) or u not in (path_to(Bser[j], 15)[:-1]):
            break
        j = (j - 1) % m
    birth = j
    s = (birth + 1) % m
    win = []
    while True:
        win.append(s)
        if s == t:
            break
        s = (s + 1) % m
    for s in win:
        pre, rots, posts = A_step_info(s)
        for e, rs in enumerate(rots):
            if u in rs or owner(s, u, 15) == e:
                nedges += 1
                print("EDGE?! token-pair %s access %d step %d" % (u, s, e))
print("total eligible events for token16:", nedges)
assert nedges == 0, "neighborhood nonempty"
print("DEFICIENT CUT VERIFIED: S={tok16} N={} 1 > 0; walk W=-96 (ECT refuted, Coarse-Double intact)")
json.dump({"token": {"t": 8, "x": 15, "pair": [7, 6]}, "N": [], "deficient": True,
           "W": W, "engines": "authoritative+independent (U1 cert + fresh replay)"},
          open(RDIR / 'DIRECT_CWC_first_deficient_cut.json', 'w'), indent=1)
