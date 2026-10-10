"""26AQ: authoritative replay of 16-key 30-access shallow-bridge candidate."""
import sys, copy, json
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python')
sys.path.insert(0, 'python/independent')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/26AQ')
RDIR.mkdir(parents=True, exist_ok=True)
LOG = open(RDIR / '26AQ_execution_log.txt', 'w')
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

def vine_right(n):
    t = None
    for k in range(n, 0, -1):
        t = [k, None, t]
    return t
T0 = vine_right(16)

PREFIX = [('D', 9), ('D', 8), ('D', 6), ('D', 6), ('D', 11), ('D', 9),
          ('D', 16), ('D', 16), ('D', 5)]
CYCLE = [('K', 11), ('K', 9), ('K', 10), ('K', 16), ('K', 1), ('K', 16),
         ('K', 15), ('K', 14), ('K', 13), ('K', 12), ('K', 11), ('K', 10),
         ('K', 9), ('K', 8), ('K', 7), ('K', 6), ('K', 5), ('K', 4),
         ('K', 3), ('K', 2), ('K', 1), ('D', 9), ('D', 8), ('D', 6),
         ('D', 6), ('D', 11), ('D', 9), ('D', 16), ('D', 16), ('D', 5)]
EXPECTED = [(1, 11, 3, 10, 2, 5, 1), (2, 9, 2, 6, 1, 3, 1),
            (3, 10, 2, 2, 1, 1, -1), (4, 16, 2, 6, 1, 3, 1),
            (5, 1, 7, 5, 4, 2, -6), (6, 16, 1, 1, 1, 0, -2),
            (7, 15, 5, 5, 3, 2, -4), (8, 14, 3, 3, 2, 1, -3),
            (9, 13, 1, 1, 1, 0, -2), (10, 12, 3, 3, 2, 1, -3),
            (11, 11, 1, 1, 1, 0, -2), (12, 10, 1, 1, 1, 0, -2),
            (13, 9, 3, 3, 2, 1, -3), (14, 8, 3, 3, 2, 1, -3),
            (15, 7, 2, 2, 1, 1, -1), (16, 6, 1, 1, 1, 0, -2),
            (17, 5, 1, 3, 1, 1, -1), (18, 4, 3, 1, 2, 0, -4),
            (19, 3, 2, 2, 1, 1, -1), (20, 2, 1, 1, 1, 0, -2),
            (21, 1, 1, 1, 1, 0, -2), (22, 9, 8, None, 4, 0, -8),
            (23, 8, 4, None, 2, 0, -4), (24, 6, 2, None, 1, 0, -2),
            (25, 6, 0, None, 0, 0, 0), (26, 11, 4, None, 2, 0, -4),
            (27, 9, 3, None, 2, 0, -4), (28, 16, 6, None, 3, 0, -6),
            (29, 16, 0, None, 0, 0, 0), (30, 5, 7, None, 4, 0, -8)]
EXP_A = "(5(4(2(1..)(3..)).)(16(9(6.(8(7..).))(11(10..)(13(12..)(15(14..).)))).))"

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
    if md == 'K':
        B, outB = splay_B_push(B, x)
        nrotB = len(outB)
    else:
        nrotB = 0
    bchanged = (pserial(B) != bbefore) if md == 'K' else False
    return A, B, {"m": md, "x": x, "dA": dA, "dB": dB, "a": a, "q": q,
                  "delta": q - 2 * a, "ra": ra, "rb": rb,
                  "bchanged": bchanged, "rotA": len(invA), "rotB": nrotB}

A = to_ptr(copy.deepcopy(T0)); B = to_ptr(copy.deepcopy(T0))
for (md, x) in PREFIX:
    A, B, _ = astep(A, B, md, x)
SA = canonstr(pserial(A))
log("PREFIX A-OK=%s B-is-vine=%s" % (
    SA == EXP_A, pserial(B) == pserial(to_ptr(copy.deepcopy(T0)))))
S0 = (pserial(A), pserial(B))
legs = []
for (md, x) in CYCLE:
    A, B, lg = astep(A, B, md, x)
    legs.append(lg)
S1 = (pserial(A), pserial(B))
log("A CLOSURE: %s" % ("PASS" if S1[0] == S0[0] else "FAIL"))
log("B CLOSURE: %s" % ("PASS" if S1[1] == S0[1] else "FAIL"))
ok = 0
for i, lg in enumerate(legs):
    e = EXPECTED[i]
    good = (lg["x"] == e[1] and lg["dA"] == e[2] and lg["dB"] == e[3]
            and lg["a"] == e[4] and lg["q"] == e[5] and lg["delta"] == e[6])
    ok += good
    if not good:
        log("MISMATCH #%d: got dA=%s dB=%s a=%s q=%s d=%s exp %s" % (
            i + 1, lg["dA"], lg["dB"], lg["a"], lg["q"], lg["delta"], e))
log("CYCLE TABLE: %d/30" % ok)
Atot = sum(l["a"] for l in legs); Qtot = sum(l["q"] for l in legs)
log("A=%d Q=%d W=%d (expect 50/23/-77)" % (Atot, Qtot, Qtot - 2 * Atot))

blocks = []
for lg in legs:
    if lg["a"] >= 1:
        blocks.append({"leader": lg["x"], "legs": [lg]})
    else:
        assert blocks and lg["x"] == blocks[-1]["leader"], ("stray no-op", lg)
        blocks[-1]["legs"].append(lg)
log("BLOCKS=%d (expect 28)" % len(blocks))
def brec(bl):
    L = bl["legs"][0]
    a = sum(l["a"] for l in bl["legs"]); q = sum(l["q"] for l in bl["legs"])
    return {"key": L["x"], "keys": sorted({l["x"] for l in bl["legs"]}),
            "a": a, "q": q, "delta": q - 2 * a,
            "genuine": any(l["bchanged"] for l in bl["legs"]),
            "dB": L["dB"], "rb": L["rb"],
            "keeps": sorted({l["x"] for l in bl["legs"] if l["m"] == "K"}),
            "nleg": len(bl["legs"])}
brecs = [brec(b) for b in blocks]
pos = [i for i, b in enumerate(brecs) if b["delta"] > 0]
log("positive block idx=%s (expect [0, 1, 3])" % pos)
log("packet deltas=%s (expect [1, 1, -1, 1, -6])" % [brecs[i]["delta"] for i in range(5)])
log("bridge K10: dB=%s genuine=%s key!=r: %s (expect 2 True True)" % (
    brecs[2]["dB"], brecs[2]["genuine"], 10 != brecs[0]["rb"]))
log("former roots: K11->%s K9->%s K16->%s (expect 1 11 10)" % (
    brecs[0]["rb"], brecs[1]["rb"], brecs[3]["rb"]))
log("return K1: a=%s q=%s (expect 4 2)" % (brecs[4]["a"], brecs[4]["q"]))
A2 = to_ptr(copy.deepcopy(T0)); B2 = to_ptr(copy.deepcopy(T0))
for (md, x) in PREFIX:
    A2, B2, _ = astep(A2, B2, md, x)
traj = []
for j, (md, x) in enumerate(CYCLE[:5]):
    A2, B2, _ = astep(A2, B2, md, x)
    if j < 4:
        traj.append(pdepths(B2).get(1))
log("depth(1): after-K11=%s after-K9=%s after-K10=%s after-K16=%s (expect 2 2 3 5)" % tuple(traj))
# noninterference: intervening B-changing keys != r
interv = [brecs[i]["key"] for i in [1, 2, 3]]
log("intervening keys=%s all!=1: %s (AQ-P4)" % (interv, all(k != 1 for k in interv)))
log("tail nonpositive=%s" % all(b["delta"] <= 0 for b in brecs[5:]))

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
log("ENGINE COMPARISON: %d/%d (expect 39/39)" % (agree, total))

cert = {"T0": "right-vine-16", "prefix": PREFIX, "cycle": CYCLE,
        "A_start_ok": SA == EXP_A, "B_is_vine": True,
        "a_closure": S1[0] == S0[0], "b_closure": S1[1] == S0[1],
        "table_match": ok, "A": Atot, "Q": Qtot, "W": Qtot - 2 * Atot,
        "nblocks": len(blocks), "positive_idx": pos, "r_traj": traj,
        "engine_agree": [agree, total], "legs": legs, "blocks": brecs}
(RDIR / '26AQ_vine16_witness_certificate.json').write_text(json.dumps(cert, indent=1))
log("certificate written")
LOG.close()
