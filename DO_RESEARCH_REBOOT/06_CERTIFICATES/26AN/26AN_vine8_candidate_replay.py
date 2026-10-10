"""26AN: authoritative replay of 8-key 13-access double-positive candidate."""
import sys, copy, json
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python')
sys.path.insert(0, 'python/independent')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/26AN')
RDIR.mkdir(parents=True, exist_ok=True)
LOG = open(RDIR / '26AN_execution_log.txt', 'w')
def log(s):
    LOG.write(s + "\n"); LOG.flush(); print(s, flush=True)
from wp6_eventflow import to_ptr, splay_A, splay_B_push
import splay as S

# ---- ptr-tree helpers (authoritative engine) ----
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

# ---- independent engine helpers ----
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

# ---- exact initial BST: (1.(2.(3.(4.(5.(8(7(6..).).)))))) ----
N6 = [6, None, None]
N7 = [7, N6, None]
N8 = [8, N7, None]
N5 = [5, None, N8]
N4 = [4, None, N5]
N3 = [3, None, N4]
N2 = [2, None, N3]
T0 = [1, None, N2]

PREFIX = [('D', 2), ('D', 8), ('D', 4), ('D', 6), ('D', 3)]
CYCLE = [('K', 6), ('K', 8), ('K', 4), ('K', 1), ('K', 2), ('K', 5),
         ('K', 8), ('K', 2), ('K', 3), ('K', 1),
         ('D', 6), ('D', 4), ('D', 3)]
EXPECTED = [(1, 6, 2, 7, 1, 3, 1), (2, 8, 1, 2, 1, 1, -1),
            (3, 4, 2, 6, 1, 3, 1), (4, 1, 3, 1, 2, 0, -4),
            (5, 2, 2, 3, 1, 1, -1), (6, 5, 3, 5, 2, 2, -2),
            (7, 8, 2, 3, 1, 1, -1), (8, 2, 3, 2, 2, 1, -3),
            (9, 3, 4, 3, 2, 1, -3), (10, 1, 2, 2, 1, 1, -1),
            (11, 6, 6, None, 3, 0, -6), (12, 4, 4, None, 2, 0, -4),
            (13, 3, 2, None, 1, 0, -2)]
EXP_A_START = "(3(2(1..).)(4.(6(5..)(8(7..).))))"
EXP_B_START = "(1.(2.(3.(4.(5.(8(7(6..).).))))))"

def canonstr(s):
    if s == '.':
        return '.'
    k, l, r = s
    return "(%d%s%s)" % (k, canonstr(l), canonstr(r))

def astep(A, B, md, x):
    """Authoritative single access. Returns (A,B,leg)."""
    dA = pdepths(A).get(x, -1)
    assert dA >= 0, ("absent A key", x)
    a = (dA + 1) // 2
    ra, rb = proot(A), proot(B)
    bbefore = pserial(B)
    if md == 'K':
        dB = pdepths(B).get(x, -1)
        assert dB >= 0, ("absent B key", x)
        q = dB // 2
    else:
        dB = None; q = 0
    A, _ = splay_A(A, x)
    if md == 'K':
        B, _ = splay_B_push(B, x)
    bchanged = (pserial(B) != bbefore) if md == 'K' else False
    return A, B, {"m": md, "x": x, "dA": dA, "dB": dB, "a": a, "q": q,
                  "delta": q - 2 * a, "ra": ra, "rb": rb,
                  "bchanged": bchanged}

def istep(A, B, md, x):
    dA = idepths(A).get(x, -1)
    a = (dA + 1) // 2
    if md == 'K':
        dB = idepths(B).get(x, -1)
        q = dB // 2
    else:
        dB = None; q = 0
    A2, _ = S.trace(A, x)
    B2 = B if md == 'D' else S.trace(B, x)[0]
    return A2, B2, (dA, dB, a, q)

# ---- run authoritative ----
A = to_ptr(copy.deepcopy(T0)); B = to_ptr(copy.deepcopy(T0))
assert pserial(A) == pserial(B), "diagonal start"
pre_legs = []
for (md, x) in PREFIX:
    A, B, lg = astep(A, B, md, x)
    pre_legs.append(lg)
SA = canonstr(pserial(A)); SB = canonstr(pserial(B))
log("A_start=%s" % SA)
log("B_start=%s" % SB)
log("PREFIX A-OK=%s B-OK=%s" % (SA == EXP_A_START, SB == EXP_B_START))
S0 = (pserial(A), pserial(B))
cyc_legs = []
for (md, x) in CYCLE:
    A, B, lg = astep(A, B, md, x)
    cyc_legs.append(lg)
S1 = (pserial(A), pserial(B))
log("EXACT A CLOSURE: %s" % ("PASS" if S1[0] == S0[0] else "FAIL"))
log("EXACT B CLOSURE: %s" % ("PASS" if S1[1] == S0[1] else "FAIL"))

ok = 0
for i, lg in enumerate(cyc_legs):
    e = EXPECTED[i]
    good = (lg["x"] == e[1] and lg["dA"] == e[2] and lg["dB"] == e[3]
            and lg["a"] == e[4] and lg["q"] == e[5]
            and lg["delta"] == e[6])
    ok += good
    if not good:
        log("MISMATCH #%d: got %s expected %s" % (i + 1, lg, e))
log("CYCLE TABLE: %d/13" % ok)
Atot = sum(l["a"] for l in cyc_legs)
Qtot = sum(l["q"] for l in cyc_legs)
log("A=%d Q=%d W=%d (expect 20/14/-26)" % (Atot, Qtot, Qtot - 2 * Atot))
log("all-a-positive=%s" % all(l["a"] >= 1 for l in cyc_legs))
pos = [i + 1 for i, l in enumerate(cyc_legs) if l["delta"] > 0]
log("positive blocks=%s deltas=%s" % (pos, [cyc_legs[i - 1]["delta"] for i in pos]))
log("K8 genuine=%s K4 genuine=%s" % (cyc_legs[1]["bchanged"], cyc_legs[2]["bchanged"]))
log("r-before-K6=%s (expect 1)" % cyc_legs[0]["rb"])
# former-root depth after K6: replay prefix+K6 on fresh trees, measure depth of 1
A2 = to_ptr(copy.deepcopy(T0)); B2 = to_ptr(copy.deepcopy(T0))
for (md, x) in PREFIX:
    A2, B2, _ = astep(A2, B2, md, x)
A2, B2, _ = astep(A2, B2, 'K', 6)
log("depth-of-1-after-K6=%s" % pdepths(B2).get(1))
log("B-root-before-K4=%s (expect 8)" % cyc_legs[2]["rb"])

# ---- independent comparison (all 18 transitions) ----
IA = to_tup(copy.deepcopy(T0)); IB = to_tup(copy.deepcopy(T0))
agree = 0; total = 0
for k, word in (("pre", PREFIX), ("cyc", CYCLE)):
    for (md, x) in word:
        IA2, IB2, (dA2, dB2, a2, q2) = istep(IA, IB, md, x)
        IA, IB = IA2, IB2
        total += 1
# recompute side-by-side with authoritative states for exact comparison
A = to_ptr(copy.deepcopy(T0)); B = to_ptr(copy.deepcopy(T0))
IA = to_tup(copy.deepcopy(T0)); IB = to_tup(copy.deepcopy(T0))
for (md, x) in PREFIX + CYCLE:
    A, B, lg = astep(A, B, md, x)
    IA, IB, (dA2, dB2, a2, q2) = istep(IA, IB, md, x)
    if (lg["dA"], lg["dB"], lg["a"], lg["q"]) == (dA2, dB2, a2, q2) \
       and pserial(A) == iserial(IA) and pserial(B) == iserial(IB):
        agree += 1
    else:
        log("ENGINE DIVERGENCE at (%s,%s)" % (md, x))
log("ENGINE COMPARISON: %d/%d" % (agree, total))

cert = {"T0": canonstr(pserial(to_ptr(copy.deepcopy(T0)))),
        "prefix": PREFIX, "cycle": CYCLE,
        "A_start": SA, "B_start": SB,
        "A_start_ok": SA == EXP_A_START, "B_start_ok": SB == EXP_B_START,
        "a_closure": S1[0] == S0[0], "b_closure": S1[1] == S0[1],
        "table_match": ok, "A": Atot, "Q": Qtot, "W": Qtot - 2 * Atot,
        "positive_blocks": pos, "engine_agree": [agree, total],
        "legs": [{k: (list(v) if isinstance(v, tuple) else v)
                  for k, v in lg.items() if k != "bchanged"}
                 for lg in cyc_legs]}
(RDIR / '26AN_vine8_witness_certificate.json').write_text(json.dumps(cert, indent=1))
log("certificate written")
LOG.close()
