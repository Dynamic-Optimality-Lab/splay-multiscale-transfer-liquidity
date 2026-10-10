"""26AO: authoritative replay of 10-key 18-access consecutive-positive candidate."""
import sys, copy, json
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python')
sys.path.insert(0, 'python/independent')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/26AO')
RDIR.mkdir(parents=True, exist_ok=True)
LOG = open(RDIR / '26AO_execution_log.txt', 'w')
def log(s):
    LOG.write(s + "\n"); LOG.flush(); print(s, flush=True)
from wp6_eventflow import to_ptr, splay_A, splay_B_push
import splay as S

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
def canonstr(s):
    if s == '.':
        return '.'
    k, l, r = s
    return "(%d%s%s)" % (k, canonstr(l), canonstr(r))

# ---- exact T0: (2(1..)(3.(6(4.(5..))(9(8(7..).)(10..))))) ----
N1 = [1, None, None]
N5 = [5, None, None]
N4 = [4, None, N5]
N7 = [7, None, None]
N8 = [8, N7, None]
N10 = [10, None, None]
N9 = [9, N8, N10]
N6 = [6, N4, N9]
N3 = [3, None, N6]
T0 = [2, N1, N3]

def bst_ok(t, lo=0, hi=11):
    if t is None:
        return True
    k, l, r = t
    return lo < k < hi and bst_ok(l, lo, k) and bst_ok(r, k, hi)
assert bst_ok(T0), "T0 BST order"
assert sorted(pdepths(to_ptr(copy.deepcopy(T0))).keys()) == list(range(1, 11)), "10 keys"

PREFIX = [('K', 10), ('D', 6), ('D', 8), ('D', 9), ('D', 5), ('D', 9),
          ('K', 1), ('D', 7), ('D', 5)]
CYCLE = [('K', 7), ('K', 5), ('K', 9), ('K', 1), ('K', 2), ('K', 8),
         ('K', 4), ('K', 9), ('K', 6), ('K', 3), ('K', 10), ('K', 1),
         ('D', 2), ('D', 4), ('D', 9), ('D', 1), ('D', 7), ('D', 5)]
EXPECTED = [(1, 7, 1, 7, 1, 3, 1), (2, 5, 1, 6, 1, 3, 1),
            (3, 9, 2, 3, 1, 1, -1), (4, 1, 3, 2, 2, 1, -3),
            (5, 2, 4, 3, 2, 1, -3), (6, 8, 5, 5, 3, 2, -4),
            (7, 4, 2, 4, 1, 2, 0), (8, 9, 2, 2, 1, 1, -1),
            (9, 6, 5, 5, 3, 2, -4), (10, 3, 3, 3, 2, 1, -3),
            (11, 10, 3, 3, 2, 1, -3), (12, 1, 3, 3, 2, 1, -3),
            (13, 2, 2, None, 1, 0, -2), (14, 4, 5, None, 3, 0, -6),
            (15, 9, 3, None, 2, 0, -4), (16, 1, 3, None, 2, 0, -4),
            (17, 7, 6, None, 3, 0, -6), (18, 5, 4, None, 2, 0, -4)]

def astep(A, B, md, x):
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
    A, invA = splay_A(A, x)
    nrotA = len(invA)
    if md == 'K':
        B, outB = splay_B_push(B, x)
        nrotB = len(outB)
    else:
        nrotB = 0
    bchanged = (pserial(B) != bbefore) if md == 'K' else False
    return A, B, {"m": md, "x": x, "dA": dA, "dB": dB, "a": a, "q": q,
                  "delta": q - 2 * a, "ra": ra, "rb": rb,
                  "bchanged": bchanged, "rotA": nrotA, "rotB": nrotB}

A = to_ptr(copy.deepcopy(T0)); B = to_ptr(copy.deepcopy(T0))
assert pserial(A) == pserial(B), "diagonal start"
for (md, x) in PREFIX:
    A, B, _ = astep(A, B, md, x)
SA = canonstr(pserial(A)); SB = canonstr(pserial(B))
log("A_start=%s" % SA)
log("B_start=%s" % SB)
S0 = (pserial(A), pserial(B))
cyc_legs = []
for (md, x) in CYCLE:
    A, B, lg = astep(A, B, md, x)
    cyc_legs.append(lg)
S1 = (pserial(A), pserial(B))
log("A CLOSURE: %s" % ("PASS" if S1[0] == S0[0] else "FAIL"))
log("B CLOSURE: %s" % ("PASS" if S1[1] == S0[1] else "FAIL"))
ok = 0
for i, lg in enumerate(cyc_legs):
    e = EXPECTED[i]
    good = (lg["x"] == e[1] and lg["dA"] == e[2] and lg["dB"] == e[3]
            and lg["a"] == e[4] and lg["q"] == e[5] and lg["delta"] == e[6])
    ok += good
    if not good:
        log("MISMATCH #%d: got dA=%s dB=%s a=%s q=%s d=%s  exp %s" % (
            i + 1, lg["dA"], lg["dB"], lg["a"], lg["q"], lg["delta"], e))
log("CYCLE TABLE: %d/18" % ok)
Atot = sum(l["a"] for l in cyc_legs); Qtot = sum(l["q"] for l in cyc_legs)
log("A=%d Q=%d W=%d (expect 34/19/-49)" % (Atot, Qtot, Qtot - 2 * Atot))
pos = [i + 1 for i, l in enumerate(cyc_legs) if l["delta"] > 0]
log("positive blocks=%s (expect [1, 2])" % pos)
log("packet deltas=%s (expect [1, 1, -1, -3])" % [cyc_legs[i]["delta"] for i in range(4)])
log("K5 genuine=%s K9 genuine=%s (expect True True)" % (
    cyc_legs[1]["bchanged"], cyc_legs[2]["bchanged"]))
log("r-before-K7=%s (expect 1); B-root-before-K5=%s (expect 7)" % (
    cyc_legs[0]["rb"], cyc_legs[1]["rb"]))
# r=1 depth trajectory: after K7 / after K5 / after K9 / before K1
A2 = to_ptr(copy.deepcopy(T0)); B2 = to_ptr(copy.deepcopy(T0))
for (md, x) in PREFIX:
    A2, B2, _ = astep(A2, B2, md, x)
traj = []
for j, (md, x) in enumerate(CYCLE[:4]):
    A2, B2, _ = astep(A2, B2, md, x)
    if j < 3:
        traj.append(pdepths(B2).get(1))
log("depth(1): after-K7=%s after-K5=%s after-K9=%s (expect 1 1 2)" % tuple(traj))

# ---- independent comparison, all 27 ----
A = to_ptr(copy.deepcopy(T0)); B = to_ptr(copy.deepcopy(T0))
IA = to_tup(copy.deepcopy(T0)); IB = to_tup(copy.deepcopy(T0))
agree = 0; total = 0
for (md, x) in PREFIX + CYCLE:
    A, B, lg = astep(A, B, md, x)
    dA2 = idepths(IA).get(x, -1); a2 = (dA2 + 1) // 2
    if md == 'K':
        dB2 = idepths(IB).get(x, -1); q2 = dB2 // 2
    else:
        dB2 = None; q2 = 0
    IA, _ = S.trace(IA, x)
    IB = IB if md == 'D' else S.trace(IB, x)[0]
    total += 1
    if (lg["dA"], lg["dB"], lg["a"], lg["q"]) == (dA2, dB2, a2, q2) \
       and pserial(A) == iserial(IA) and pserial(B) == iserial(IB):
        agree += 1
    else:
        log("ENGINE DIVERGENCE at (%s,%s)" % (md, x))
log("ENGINE COMPARISON: %d/%d (expect 27/27)" % (agree, total))

cert = {"T0": canonstr(pserial(to_ptr(copy.deepcopy(T0)))),
        "prefix": PREFIX, "cycle": CYCLE,
        "A_start": SA, "B_start": SB,
        "a_closure": S1[0] == S0[0], "b_closure": S1[1] == S0[1],
        "table_match": ok, "A": Atot, "Q": Qtot, "W": Qtot - 2 * Atot,
        "positive_blocks": pos, "r_traj": traj,
        "engine_agree": [agree, total], "legs": cyc_legs}
(RDIR / '26AO_ten_key_witness_certificate.json').write_text(json.dumps(cert, indent=1))
log("certificate written")
LOG.close()
